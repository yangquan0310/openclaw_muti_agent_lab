"""zotero_jianguoyun.py - ZoteroJianguoyunDownloader（老板专属 Zotero + 坚果云 WebDAV）

流水线：
1. find(identifier) → Zotero API 拿 item + attachment + MD5
2. pull(meta) → 坚果云 WebDAV GET {attachment_key}.zip → 解压出 PDF
3. save(pdf, meta) → 按 YYYY-MM[-DD]_作者_关键词_期刊.pdf 归档
"""

from __future__ import annotations

import base64
import json
import re
import shutil
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path
from typing import Optional

from scripts.utils import config
from scripts.download.base import Downloader
from scripts.download.paper import PaperMetadata


def _basic_auth(user: str, password: str) -> str:
    if not user or not password:
        raise ValueError("basic_auth: user 和 password 都必填")
    token = base64.b64encode(f"{user}:{password}".encode()).decode()
    return f"Basic {token}"


def _parse_zotero_date(date_str: str):
    if not date_str:
        return None, None, None
    s = str(date_str).strip()
    m = re.match(r"^(\d{4})(?:-(\d{1,2}))?(?:-(\d{1,2}))?", s)
    if m:
        y, mo, d = int(m.group(1)), m.group(2), m.group(3)
        return y, int(mo) if mo else None, int(d) if d else None
    m = re.match(r"^(\d{1,2})/(\d{4})", s)
    if m:
        return int(m.group(2)), int(m.group(1)), None
    return None, None, None


class ZoteroJianguoyunDownloader(Downloader):
    """Zotero 库 + 坚果云 WebDAV 同步下载器（老板专属）"""

    ZOTERO_API_BASE = "https://api.zotero.org"
    DEFAULT_WEBDAV_URL = "https://dav.jianguoyun.com/dav/quanquanzi/zotero"
    DEFAULT_WEBDAV_USER = "yangquan0310@qq.com"
    DEFAULT_WIKI_RAW_DIR = "/root/.openclaw/wiki/raw/papers"

    def __init__(
        self,
        cfg: dict | None = None,
        archive_dir: Path | None = None,
    ):
        self.cfg = cfg or config()

        # 兑底从 ~/.openclaw/.env 读凭据
        import os
        from pathlib import Path as _P
        env_path = _P.home() / ".openclaw" / ".env"
        env = {}
        if env_path.exists():
            for line in env_path.read_text(encoding="utf-8").splitlines():
                if "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip().strip('"').strip("'")

        self.zotero_user_id = (
            self.cfg.get("zotero", {}).get("user_id", "")
            or env.get("ZOTERO_USER_ID", "")
        )
        self.zotero_api_key = (
            self.cfg.get("zotero", {}).get("api_key", "")
            or env.get("ZOTERO_API_KEY", "")
        )
        self.webdav_url = self.cfg.get("jianguoyun", {}).get("url", self.DEFAULT_WEBDAV_URL)
        self.webdav_user = self.cfg.get("jianguoyun", {}).get("user", self.DEFAULT_WEBDAV_USER)
        self.webdav_password = (
            self.cfg.get("jianguoyun", {}).get("password", "")
            or env.get("JIANGUOYUN_PASSWORD", "")
        )
        self.archive_dir = Path(archive_dir or self.DEFAULT_WIKI_RAW_DIR)

        if not self.zotero_api_key:
            raise ValueError("ZOTERO_API_KEY 未在 config.json 中找到，也未显式传入")
        if not self.webdav_password:
            raise ValueError("JIANGUOYUN_PASSWORD 未在 config.json 中找到，也未显式传入")

        # 缓存：{md5_full: hash_8char}
        self._md5_to_hash: dict[str, str] = {}

    # ==================== find ====================

    def find(self, identifier: str) -> PaperMetadata:
        if not identifier:
            raise ValueError("identifier 不能为空")
        if identifier.startswith("10."):
            return self._find_by_doi(identifier)
        elif len(identifier) == 8 and identifier.isalnum():
            return self._find_by_item_key(identifier)
        else:
            raise ValueError(
                f"无法识别 identifier: {identifier}（需 DOI '10.xxx' 或 8 字符 Zotero key）"
            )

    def _zotero_api(self, path: str, max_retries: int = 3, retry_delay: float = 2.0) -> dict:
        import time
        url = f"{self.ZOTERO_API_BASE}/users/{self.zotero_user_id}/{path}"
        for attempt in range(max_retries):
            req = urllib.request.Request(url)
            req.add_header("Zotero-API-Key", self.zotero_api_key)
            req.add_header("Zotero-API-Version", "3")
            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    return json.loads(resp.read().decode("utf-8"))
            except urllib.error.HTTPError as e:
                if e.code == 503 and attempt < max_retries - 1:
                    time.sleep(retry_delay * (attempt + 1))
                    continue
                raise RuntimeError(
                    f"Zotero API 失败 {e.code}: {e.read().decode('utf-8', errors='replace')}"
                )

    def _find_by_doi(self, doi: str) -> PaperMetadata:
        from urllib.parse import quote
        doi_lower = doi.lower()
        items = self._zotero_api(f"items?q={quote(doi)}&format=json&limit=20")
        for it in items:
            d = it.get("data", {})
            if (d.get("DOI") or "").lower() == doi_lower:
                return self._build_meta(d)
        all_items = self._zotero_api("items?format=json&limit=500")
        for it in all_items:
            d = it.get("data", {})
            if (d.get("DOI") or "").lower() == doi_lower:
                return self._build_meta(d)
        raise RuntimeError(f"Zotero 库未找到 DOI: {doi}")

    def _find_by_item_key(self, key: str) -> PaperMetadata:
        data = self._zotero_api(f"items/{key}?format=json")
        return self._build_meta(data.get("data", data))

    def _build_meta(self, data: dict) -> PaperMetadata:
        item_key = data.get("key")
        if not item_key:
            raise RuntimeError(f"Zotero data 缺 key 字段: {data}")
        children = self._zotero_api(f"items/{item_key}/children?format=json")
        attachment = None
        for c in children:
            cd = c.get("data", {})
            if cd.get("itemType") == "attachment":
                attachment = cd
                break
        if not attachment:
            raise RuntimeError(
                f"Zotero item {item_key} 没有 PDF 附件（请先在 Zotero 客户端添加）"
            )
        authors = []
        for c in data.get("creators", []):
            if c.get("lastName"):
                authors.append(c["lastName"])
            elif c.get("name"):
                last = c["name"].split(",")[0].strip()
                if last:
                    authors.append(last)
        year, month, day = _parse_zotero_date(data.get("date", ""))
        return PaperMetadata(
            zotero_item_key=item_key,
            zotero_attachment_key=attachment.get("key"),
            doi=data.get("DOI"),
            title=data.get("title", ""),
            authors=authors,
            year=year,
            month=month,
            day=day,
            venue=data.get("publicationTitle"),
            md5=attachment.get("md5"),
            source_url=attachment.get("url"),
            link_mode=attachment.get("linkMode", "imported_url"),
        )

    # ==================== pull ====================

    def pull(self, meta: PaperMetadata, dest_dir: Path) -> Path:
        dest_dir.mkdir(parents=True, exist_ok=True)
        if not meta.md5:
            raise RuntimeError(
                f"Paper {meta.zotero_item_key or meta.doi} 没有 MD5，无法定位 WebDAV 文件"
            )
        self._build_hash_index()
        hash_8 = self._md5_to_hash.get(meta.md5)
        if not hash_8:
            raise RuntimeError(f"MD5 {meta.md5} 不在坚果云 WebDAV 上")
        zip_url = f"{self.webdav_url}/{hash_8}.zip"
        zip_path = dest_dir / f"{hash_8}.zip"
        self._webdav_get(zip_url, zip_path)
        pdf_name = None
        with zipfile.ZipFile(zip_path, "r") as zf:
            for n in zf.namelist():
                if n.lower().endswith(".pdf"):
                    pdf_name = n
                    break
        if not pdf_name:
            raise RuntimeError(f".zip 中未找到 PDF: {zip_path}")
        pdf_path = dest_dir / pdf_name
        with zipfile.ZipFile(zip_path, "r") as zf:
            with zf.open(pdf_name) as src, open(pdf_path, "wb") as dst:
                shutil.copyfileobj(src, dst)
        zip_path.unlink()
        return pdf_path

    def _build_hash_index(self):
        import time
        if self._md5_to_hash:
            return
        xml_data = None
        for attempt in range(3):
            req = urllib.request.Request(self.webdav_url, method="PROPFIND")
            req.add_header("Authorization", _basic_auth(self.webdav_user, self.webdav_password))
            req.add_header("Depth", "1")
            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    xml_data = resp.read()
                break
            except urllib.error.HTTPError as e:
                if e.code in (429, 503) and attempt < 2:
                    time.sleep(5 * (attempt + 1))
                    continue
                raise RuntimeError(
                    f"WebDAV PROPFIND 失败 {e.code}: {e.read().decode('utf-8', errors='replace')}"
                )
        if xml_data is None:
            raise RuntimeError("WebDAV PROPFIND 连续 3 次 503")
        ns = {"d": "DAV:"}
        root = ET.fromstring(xml_data)
        from urllib.parse import urljoin
        for resp_el in root.findall("d:response", ns):
            href = resp_el.find("d:href", ns)
            if href is None:
                continue
            url = href.text or ""
            name = url.rstrip("/").split("/")[-1]
            if not name.endswith(".prop"):
                continue
            hash_8 = name.replace(".prop", "")
            prop_url = urljoin(self.webdav_url + "/", f"{hash_8}.prop")
            try:
                prop_req = urllib.request.Request(prop_url)
                prop_req.add_header(
                    "Authorization", _basic_auth(self.webdav_user, self.webdav_password)
                )
                with urllib.request.urlopen(prop_req, timeout=10) as prop_resp:
                    prop_xml = prop_resp.read().decode("utf-8", errors="replace")
                m = re.search(r"<hash>([a-f0-9]+)</hash>", prop_xml)
                if m:
                    self._md5_to_hash[m.group(1)] = hash_8
            except Exception:
                continue

    def _webdav_get(self, url: str, dest: Path) -> Path:
        import time
        for attempt in range(3):
            req = urllib.request.Request(url)
            req.add_header("Authorization", _basic_auth(self.webdav_user, self.webdav_password))
            try:
                with urllib.request.urlopen(req, timeout=120) as resp:
                    data = resp.read()
                dest.write_bytes(data)
                return dest
            except urllib.error.HTTPError as e:
                if e.code in (429, 503) and attempt < 2:
                    time.sleep(5 * (attempt + 1))
                    continue
                raise
        raise RuntimeError(f"WebDAV GET 连续 3 次失败: {url}")

    # ==================== save ====================

    def save(self, pdf: Path, meta: PaperMetadata, dest_dir: Path) -> Path:
        target_dir = Path(dest_dir)
        target_dir.mkdir(parents=True, exist_ok=True)
        target_name = meta.archive_filename()
        target_path = target_dir / target_name
        if target_path.exists():
            return target_path
        shutil.move(str(pdf), str(target_path))
        return target_path