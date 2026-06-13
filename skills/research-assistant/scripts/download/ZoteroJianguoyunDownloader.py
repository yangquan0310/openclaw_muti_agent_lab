"""ZoteroJianguoyunDownloader.py - 老板专属的 Zotero + 坚果云 WebDAV 同步下载器

流水线：
1. find_paper(DOI/key) → Zotero API 拿 item + attachment + MD5
2. download_pdf(meta) → 坚果云 WebDAV GET {attachment_key}.zip → 解压出 PDF
3. archive_to_wiki(pdf, meta) → 按 YYYY-MM[-DD]_作者_关键词_期刊.pdf 归档

关键发现（2026-06-05 Diehl 2026 实战）：
- WebDAV 8 字符 hash 文件名 = Zotero attachment key（不是 MD5 前 8 位）
- 老板 Zotero 库 attachment 模式多为 imported_url，PDF 缓存到 Zotero Storage
- 反查路径：MD5 → 8 字符 hash（用 .prop 文件建索引）

凭据：
- Zotero: ZOTERO_USER_ID + ZOTERO_API_KEY（v5.12.0 优先级: key > config.json > .env）
- 坚果云: JIANGUOYUN_USER（默认 yangquan0310@qq.com）+ JIANGUOYUN_PASSWORD（v5.12.0 优先级: key > config.json > .env）
- 目标: WIKI_RAW_PAPERS_DIR（默认 /root/.openclaw/wiki/raw/papers）
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
from typing import Dict, Optional

from .Downloader import Downloader
from .paper_metadata import PaperMetadata
from .utils import basic_auth_header, load_env_file, parse_zotero_date


class ZoteroJianguoyunDownloader(Downloader):
    """Zotero 库 + 坚果云 WebDAV 同步下载器（老板专属）"""

    ZOTERO_API_BASE = "https://api.zotero.org"
    DEFAULT_ZOTERO_USER_ID = "8891501"
    DEFAULT_WEBDAV_URL = "https://dav.jianguoyun.com/dav/quanquanzi/zotero"
    DEFAULT_WEBDAV_USER = "yangquan0310@qq.com"
    DEFAULT_WIKI_RAW_DIR = "/root/.openclaw/wiki/raw/papers"
    DEFAULT_ENV_FILE = "/root/.openclaw/.env"

    def __init__(
        self,
        zotero_user_id: Optional[str] = None,
        zotero_api_key: Optional[str] = None,
        webdav_url: Optional[str] = None,
        webdav_user: Optional[str] = None,
        webdav_password: Optional[str] = None,
        wiki_raw_dir: Optional[str] = None,
        env_file: Optional[str] = None,
    ):
        """初始化下载器

        凭据读取优先级（v5.12.0）: key > config.json > .env > DEFAULT
        - key: __init__ 显式传入的参数（最高）
        - config.json: scripts/config.json（v5.12.0 新增，比 .env 优先）
        - .env: ~/.openclaw/.env（兜底）
        - DEFAULT_*：硬编码兜底（仅对 user/url，password 不兜底）
        """
        env_file = env_file or self.DEFAULT_ENV_FILE
        env = load_env_file(env_file)

        # 加载 config.json（v5.12.0 新增）— Zotero + jianguoyun 段
        dl_config = self._load_download_config()
        zotero_cfg = dl_config.get("zotero", {})
        jgy_cfg = dl_config.get("jianguoyun", {})

        # Zotero 凭据：key > config > env > DEFAULT
        self.zotero_user_id = (
            zotero_user_id
            or zotero_cfg.get("user_id", "")
            or env.get("ZOTERO_USER_ID")
            or self.DEFAULT_ZOTERO_USER_ID
        )
        self.zotero_api_key = (
            zotero_api_key
            or zotero_cfg.get("api_key", "")
            or env.get("ZOTERO_API_KEY")
        )
        # 坚果云凭据：key > config > env > DEFAULT（password 无 DEFAULT）
        self.webdav_url = (
            webdav_url
            or jgy_cfg.get("url", "")
            or self.DEFAULT_WEBDAV_URL
        )
        self.webdav_user = (
            webdav_user
            or jgy_cfg.get("user", "")
            or self.DEFAULT_WEBDAV_USER
        )
        self.webdav_password = (
            webdav_password
            or jgy_cfg.get("password", "")
            or env.get("JIANGUOYUN_PASSWORD")
        )
        self.wiki_raw_dir = Path(wiki_raw_dir or self.DEFAULT_WIKI_RAW_DIR)

        if not self.zotero_api_key:
            raise ValueError(
                f"ZOTERO_API_KEY 未在 config.json / {env_file} 中找到，也未显式传入"
            )
        if not self.webdav_password:
            raise ValueError(
                f"JIANGUOYUN_PASSWORD 未在 config.json / {env_file} 中找到，也未显式传入"
            )

        # 缓存：{md5_full: hash_8char}
        self._md5_to_hash: Dict[str, str] = {}

    def _load_download_config(self) -> dict:
        """从 scripts/config.json 加载 download 段配置（v5.12.0 新增）"""
        try:
            _cfg_path = Path(__file__).parent.parent / "config.json"
            if _cfg_path.exists():
                with open(_cfg_path, "r", encoding="utf-8") as _f:
                    return json.load(_f)
        except Exception:
            pass
        return {}

    # ==================== find_paper ====================

    def find_paper(self, identifier: str) -> PaperMetadata:
        """根据 identifier 找到论文元数据"""
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
        """Zotero API 通用 GET 调用（503 自动 retry，指数退避）"""
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
        """按 DOI 在 Zotero 库查找

        Zotero API 的 `q` 参数是全文搜，不索引 DOI 字段。需多策略级联：
        1) 先试 `q=<doi>` 全文搜（极少命中，但成本低）
        2) fallback：全库扫描（分页拉所有 items，检查 DOI 字段精确匹配）

        小型库（<500 items）走全库扫描可行；大型库建议加缓存。
        """
        from urllib.parse import quote

        doi_lower = doi.lower()

        # 策略 1：全文搜
        items = self._zotero_api(
            f"items?q={quote(doi)}&format=json&limit=20"
        )
        for it in items:
            d = it.get("data", {})
            if (d.get("DOI") or "").lower() == doi_lower:
                return self._build_metadata(d)

        # 策略 2：全库扫描
        all_items = self._zotero_api("items?format=json&limit=500")
        for it in all_items:
            d = it.get("data", {})
            if (d.get("DOI") or "").lower() == doi_lower:
                return self._build_metadata(d)

        raise RuntimeError(f"Zotero 库未找到 DOI: {doi}")

    def _find_by_item_key(self, key: str) -> PaperMetadata:
        """按 Zotero item key 查找"""
        data = self._zotero_api(f"items/{key}?format=json")
        return self._build_metadata(data.get("data", data))

    def _build_metadata(self, data: dict) -> PaperMetadata:
        """从 Zotero item data 构建 PaperMetadata"""
        item_key = data.get("key")
        if not item_key:
            raise RuntimeError(f"Zotero data 缺 key 字段: {data}")

        # 找 attachment children
        children = self._zotero_api(
            f"items/{item_key}/children?format=json"
        )
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

        # 解析作者（提取姓氏）
        authors = []
        for c in data.get("creators", []):
            if c.get("lastName"):
                authors.append(c["lastName"])
            elif c.get("name"):
                # 单字段 name（如 "Barasch, Alixandra"）
                last = c["name"].split(",")[0].strip()
                if last:
                    authors.append(last)

        # 解析日期
        year, month, day = parse_zotero_date(data.get("date", ""))

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

    # ==================== download_pdf ====================

    def download_pdf(self, meta: PaperMetadata, dest_dir: Path) -> Path:
        """从坚果云 WebDAV 下载 PDF

        流程：
        1) 用 PROPFIND + .prop 索引建立 {MD5: 8字符 hash} 反查表
        2) 拿 hash → GET {hash}.zip
        3) 解压 zip → 找 PDF → 移动到 dest_dir
        4) 清理 .zip
        """
        dest_dir.mkdir(parents=True, exist_ok=True)

        if not meta.md5:
            raise RuntimeError(
                f"Paper {meta.zotero_item_key or meta.doi} 没有 MD5，无法定位 WebDAV 文件"
            )

        # 1) 构建 MD5 → hash 索引
        self._build_hash_index()
        hash_8 = self._md5_to_hash.get(meta.md5)
        if not hash_8:
            raise RuntimeError(
                f"MD5 {meta.md5} 不在坚果云 WebDAV 上"
            )

        # 2) 下载 .zip
        zip_url = f"{self.webdav_url}/{hash_8}.zip"
        zip_path = dest_dir / f"{hash_8}.zip"
        self._webdav_get(zip_url, zip_path)

        # 3) 解压找 PDF
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

        # 4) 清理 .zip
        zip_path.unlink()
        return pdf_path

    def _build_hash_index(self):
        """构建 {md5_full: hash_8char} 索引（首次调用后缓存）"""
        import time

        if self._md5_to_hash:
            return

        # PROPFIND 列目录（含 503 retry）
        xml_data = None
        for attempt in range(3):
            req = urllib.request.Request(self.webdav_url, method="PROPFIND")
            req.add_header("Authorization", basic_auth_header(self.webdav_user, self.webdav_password))
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

        # 列出所有 .prop 文件，下载并解析 hash
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
                    "Authorization",
                    basic_auth_header(self.webdav_user, self.webdav_password),
                )
                with urllib.request.urlopen(prop_req, timeout=10) as prop_resp:
                    prop_xml = prop_resp.read().decode("utf-8", errors="replace")
                m = re.search(r"<hash>([a-f0-9]+)</hash>", prop_xml)
                if m:
                    self._md5_to_hash[m.group(1)] = hash_8
            except Exception:
                continue

    def _webdav_get(self, url: str, dest: Path) -> Path:
        """WebDAV GET 请求（含 503/429 retry）"""
        import time

        for attempt in range(3):
            req = urllib.request.Request(url)
            req.add_header(
                "Authorization",
                basic_auth_header(self.webdav_user, self.webdav_password),
            )
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

    # ==================== archive_to_wiki ====================

    def archive_to_wiki(
        self, pdf: Path, meta: PaperMetadata, wiki_raw_dir: Optional[Path] = None
    ) -> Path:
        """按命名约定归档到 wiki/raw/papers/"""
        target_dir = Path(wiki_raw_dir) if wiki_raw_dir else self.wiki_raw_dir
        target_dir.mkdir(parents=True, exist_ok=True)

        target_name = meta.archive_filename()
        target_path = target_dir / target_name

        # 已存在则跳过（幂等）
        if target_path.exists():
            return target_path

        shutil.move(str(pdf), str(target_path))
        return target_path
