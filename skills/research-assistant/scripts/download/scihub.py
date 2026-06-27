"""scihub.py - SciHubDownloader（绕过付费墙下载 PDF）

设计原则：
- 论文不在 Zotero 库时可用 SciHub 替代（直接落 wiki/raw/papers，不动老板坚果云）
- 默认走 ZoteroJianguoyunDownloader（避免乱下载到老板的坚果云）
- SciHub 域名经常变，提供多个 fallback + 状态语义（FOUND / NOT_FOUND / OA_LINK / MIRROR_ERROR）
- 只下载 DOI 标识的论文（不下载任意 URL，避免版权风险）
- 零外部依赖：纯 Python stdlib（与被整合的 scihub-paper-downloader 技能行为一致）

流水线：
1. find(doi)        → resolve_pdf(doi) 拿 PDF URL + 元数据（title/authors/year/venue 从 SciHub 页面解析）
2. pull(meta)        → 下载 PDF URL 到临时目录
3. save(pdf, meta)   → 按 YYYY-MM[-DD]_作者_关键词_期刊.pdf 归档到 wiki/raw/papers

注意：本模块替代了原独立的 scihub-paper-downloader 技能（v6.0.7+ 整合到 download）。
"""

from __future__ import annotations

import base64
import hashlib
import http.client
import http.cookiejar
import json
import os
import re
import shutil
import time
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urljoin, urlsplit, urlunsplit
from urllib.request import (
    HTTPCookieProcessor,
    HTTPRedirectHandler,
    Request,
    build_opener,
)

from scripts.download.base import Downloader
from scripts.download.paper import PaperMetadata


# ─── SciHub 解析核心（来自被整合的 scihub-paper-downloader 技能）───────────

TIMEOUT = 20
PDF_TIMEOUT = 120
MIN_PDF_SIZE = 1024
STATUS_FOUND = "FOUND"
STATUS_NOT_FOUND = "NOT_FOUND"
STATUS_MIRROR_ERROR = "MIRROR_ERROR"
STATUS_INVALID_INPUT = "INVALID_INPUT"
DEFAULT_MIRRORS = (
    "https://sci-hub.st",
    "https://sci-hub.ru",
    "https://sci-hub.se",
    "https://sci-hub.ren",
    "https://sci-hub.box",
    "https://sci-hub.workflow",
)


class SciHubAllMirrorsFailedError(RuntimeError):
    """SciHub 所有镜像都不可访问——携带 mirrors_tried / last_errors 给上层反馈

    与普通 RuntimeError 的区别：CLI 层可以 isinstance 判断后返结构化 JSON
    （含 mirrors_tried 列表 + suggestion 建议），而不是单纯错误字符串。
    """

    def __init__(self, mirrors_tried: list[str], last_errors: list[str], doi: str = ""):
        self.mirrors_tried = list(mirrors_tried)
        self.last_errors = list(last_errors)
        self.doi = doi
        suffix = f"（DOI: {doi}）" if doi else ""
        super().__init__(
            f"SciHub 所有 {len(mirrors_tried)} 个镜像都不可访问{suffix}: {', '.join(mirrors_tried)}"
        )
UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)
PDF_PATTERNS = (
    re.compile(r'<(?:iframe|embed|object)[^>]+(?:src|data)=["\']([^"\']+)["\']', re.I),
    re.compile(r'["\']((?:https?:)?//[^"\']+?(?:\.pdf|/pdf)[^"\']*)["\']', re.I),
)
OA_HINT_PATTERN = re.compile(
    r'<block-rounded[^>]+class\s*=\s*["\'][^"\']*\bopenaccess\b[^"\']*["\'][^>]*>(?:(?!</block-rounded>).)*?<a[^>]+href\s*=\s*["\']([^"\']+)["\']',
    re.I | re.S,
)


class _Browser:
    """轻量 HTTP 客户端（cookielib + redirect handler）"""

    def __init__(self) -> None:
        jar = http.cookiejar.CookieJar()
        self.opener = build_opener(HTTPCookieProcessor(jar), HTTPRedirectHandler())

    def open(
        self,
        url: str,
        *,
        data: bytes | None = None,
        headers: dict[str, str] | None = None,
    ) -> http.client.HTTPResponse:
        req = Request(url, data=data, headers=headers or {})
        return self.opener.open(req, timeout=TIMEOUT)


def _headers(extra: dict[str, str] | None = None) -> dict[str, str]:
    base = {
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    if extra:
        base.update(extra)
    return base


def _canonicalize(url: str) -> str:
    parts = urlsplit(url.strip().replace("\\/", "/"))
    return urlunsplit((parts.scheme, parts.netloc, parts.path, parts.query, ""))


def _normalize_doi(raw: str) -> str:
    doi = raw.strip()
    doi = re.sub(r"^(?:doi:\s*)", "", doi, flags=re.I)
    doi = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", doi, flags=re.I)
    return doi.strip()


def _extract_title(html: str) -> str:
    m = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
    if not m:
        return ""
    return " ".join(m.group(1).split())


def _iter_pdf_candidates(html: str, page_url: str) -> Iterable[str]:
    seen: set[str] = set()
    for pattern in PDF_PATTERNS:
        for raw in pattern.findall(html):
            candidate = raw.strip()
            if not candidate:
                continue
            if candidate.startswith("//"):
                candidate = f"https:{candidate}"
            else:
                candidate = urljoin(page_url, candidate)
            candidate = _canonicalize(candidate)
            if candidate in seen:
                continue
            seen.add(candidate)
            yield candidate


def _has_altcha(html: str) -> bool:
    return bool(re.search(r"/captcha/challenge/\d+", html))


def _hexdigest(data: str, algorithm: str) -> str:
    digest = hashlib.new(algorithm.strip().lower().replace("-", ""))
    digest.update(data.encode("utf-8"))
    return digest.hexdigest()


def _solve_altcha(browser: _Browser, page_url: str, html: str) -> bool:
    challenge_id = re.search(r"/captcha/challenge/(\d+)", html)
    if not challenge_id:
        return False
    parts = urlsplit(page_url)
    base_url = f"{parts.scheme}://{parts.netloc}"
    challenge_url = urljoin(base_url, f"/captcha/challenge/{challenge_id.group(1)}")
    solution_url = urljoin(base_url, f"/captcha/solution/{challenge_id.group(1)}")
    try:
        with browser.open(challenge_url, headers=_headers({"Accept": "application/json"})) as resp:
            challenge = json.loads(resp.read().decode("utf-8", errors="replace"))
        algorithm = str(challenge["algorithm"])
        salt = str(challenge["salt"])
        target = str(challenge["challenge"])
        max_number = int(challenge["maxNumber"])
    except (HTTPError, URLError, OSError, KeyError, TypeError, ValueError, json.JSONDecodeError):
        return False
    number = None
    try:
        for value in range(max_number + 1):
            if _hexdigest(f"{salt}{value}", algorithm) == target:
                number = value
                break
    except ValueError:
        return False
    if number is None:
        return False
    payload = base64.b64encode(
        json.dumps(
            {
                "algorithm": algorithm,
                "challenge": target,
                "number": number,
                "salt": salt,
                "signature": challenge.get("signature", ""),
                "took": 0,
            },
            separators=(",", ":"),
        ).encode("utf-8")
    ).decode("ascii")
    body = json.dumps({"captcha": payload}).encode("utf-8")
    try:
        with browser.open(
            solution_url,
            data=body,
            headers=_headers(
                {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Origin": base_url,
                    "Referer": page_url,
                }
            ),
        ) as resp:
            response = json.loads(resp.read().decode("utf-8", errors="replace"))
    except (HTTPError, URLError, OSError, TypeError, ValueError, json.JSONDecodeError):
        return False
    return bool(response.get("success"))


def _fetch_page(browser: _Browser, doi_url: str) -> tuple[str, str]:
    current_url = doi_url
    for _ in range(3):
        with browser.open(current_url, headers=_headers()) as resp:
            final_url = resp.geturl()
            html = resp.read().decode("utf-8", errors="replace")
        if not _has_altcha(html):
            return final_url, html
        if not _solve_altcha(browser, final_url, html):
            break
        current_url = doi_url
    return "", ""


def _is_pdf_url(browser: _Browser, url: str) -> bool:
    headers = _headers(
        {
            "Accept": "application/pdf,*/*;q=0.8",
            "Range": "bytes=0-7",
        }
    )
    try:
        with browser.open(url, headers=headers) as resp:
            content_type = (resp.headers.get("Content-Type") or "").lower()
            if "application/pdf" in content_type:
                return True
            prefix = resp.read(8)
            return prefix.startswith(b"%PDF-")
    except (HTTPError, URLError, OSError):
        return False


def _extract_oa_link(html: str, page_url: str) -> str:
    m = OA_HINT_PATTERN.search(html)
    if not m:
        return ""
    candidate = m.group(1).strip()
    if not candidate:
        return ""
    if candidate.startswith("//"):
        candidate = f"https:{candidate}"
    else:
        candidate = urljoin(page_url, candidate)
    return _canonicalize(candidate)


def _mirror_list(cfg: dict | None = None) -> tuple[str, ...]:
    """镜像列表解析（优先级：config.json → 环境变量 → hardcoded 兑底）

    v6.0.7+ 老板 05:16 指令：默认走 config.json，避免临时改 env；env 主要用于 CI/调试。
    """
    # 1. config.json 优先（持久化、可控）
    cfg_mirrors = (cfg or {}).get("scihub", {}).get("mirrors")
    if cfg_mirrors and isinstance(cfg_mirrors, list):
        cleaned = tuple(
            str(m).strip().rstrip("/")
            for m in cfg_mirrors
            if str(m).strip()
        )
        if cleaned:
            return cleaned
    # 2. 环境变量（CI/调试快速覆盖）
    raw = os.environ.get("SCIHUB_MIRRORS", "")
    if raw.strip():
        return tuple(item.strip().rstrip("/") for item in raw.split(",") if item.strip())
    # 3. hardcoded 兑底
    return DEFAULT_MIRRORS


def resolve_pdf(doi: str, cfg: dict | None = None) -> tuple[str, str]:
    """通过 SciHub 解析 DOI → PDF URL

    Returns:
        (status, url_or_oa_link) — status 取值：
        - STATUS_FOUND + url: 找到 PDF 链接
        - STATUS_NOT_FOUND + "": SciHub 库内无此论文
        - STATUS_NOT_FOUND + oa_link: SciHub 没有，但页面提示 OA 链接（可能是 publisher 主页）
        - STATUS_MIRROR_ERROR + "": 所有镜像都不可访问（结果不确定）
        - STATUS_INVALID_INPUT + "": DOI 格式无效
    """
    normalized = _normalize_doi(doi)
    if not normalized:
        return STATUS_INVALID_INPUT, ""
    safe_doi = quote(normalized, safe="/:().-_")
    saw_not_found = False
    saw_mirror_error = False
    oa_link = ""
    for mirror in _mirror_list(cfg):
        browser = _Browser()
        try:
            page_url, html = _fetch_page(browser, f"{mirror}/{safe_doi}")
        except (HTTPError, URLError, OSError):
            saw_mirror_error = True
            continue
        if not html:
            saw_mirror_error = True
            continue
        title = _extract_title(html).lower()
        if "not available through sci-hub" in title or "no articles found" in title:
            saw_not_found = True
            if not oa_link:
                oa_link = _extract_oa_link(html, page_url)
            continue
        for candidate in _iter_pdf_candidates(html, page_url):
            if _is_pdf_url(browser, candidate):
                return STATUS_FOUND, candidate
        saw_mirror_error = True
    if saw_not_found:
        return STATUS_NOT_FOUND, oa_link
    if saw_mirror_error:
        return STATUS_MIRROR_ERROR, ""
    return STATUS_NOT_FOUND, ""


# ─── SciHub 页面元数据解析（cite_title / cite_author / cite_journal / cite_date） ──

_META_CITE_TITLE = re.compile(r'<meta name="citation_title" content="([^"]+)"')
_META_CITE_AUTHOR = re.compile(r'<meta name="citation_author" content="([^"]+)"')
_META_CITE_JOURNAL = re.compile(r'<meta name="citation_journal_title" content="([^"]+)"')
_META_CITE_DATE = re.compile(r'<meta name="citation_publication_date" content="(\d{4})')


def _parse_page_metadata(html: str, doi: str) -> PaperMetadata:
    """从 SciHub 页面提取元数据（用作 PaperMetadata 字段填充）"""
    title = ""
    m = _META_CITE_TITLE.search(html)
    if m:
        title = m.group(1).strip()
    else:
        m = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
        if m:
            title = re.sub(r"\s*\|\s*Sci-Hub.*$", "", m.group(1)).strip()
    authors = _META_CITE_AUTHOR.findall(html)
    venue = ""
    m = _META_CITE_JOURNAL.search(html)
    if m:
        venue = m.group(1)
    year = None
    m = _META_CITE_DATE.search(html)
    if m:
        try:
            year = int(m.group(1))
        except ValueError:
            pass
    return PaperMetadata(
        doi=doi,
        title=title,
        authors=authors,
        year=year,
        venue=venue,
        source_url=doi,
        link_mode="scihub",
    )


# ─── SciHubDownloader（实现 Downloader ABC） ──────────────────────────────


class SciHubDownloader(Downloader):
    """SciHub 下载器（绕过付费墙，落 wiki/raw/papers，不动老板坚果云）

    与 ZoteroJianguoyunDownloader 的核心区别：
    - 不需要论文先在 Zotero 库（设计原则：避免乱下载到老板的坚果云）
    - 不写 Zotero 库 / 不写 WebDAV（仅落 wiki/raw/papers 本地归档）
    - 仅支持 DOI（不支持 Zotero item key——没元数据源）
    """

    DEFAULT_ARCHIVE_DIR = "/root/.openclaw/wiki/raw/papers"

    def __init__(self, cfg: dict | None = None, archive_dir: Path | None = None):
        # 不调 super().__init__()，无需 Zotero/WebDAV 凭据
        self.cfg = cfg or {}
        self.archive_dir = Path(archive_dir or self.DEFAULT_ARCHIVE_DIR)
        # 读 config.json / env 的镜像列表 + 超时配置（v6.0.7+ 优先级链）
        self.mirrors: tuple[str, ...] = _mirror_list(self.cfg)
        self.request_timeout: int = int(self.cfg.get("scihub", {}).get("request_timeout", TIMEOUT))
        self.pdf_timeout: int = int(self.cfg.get("scihub", {}).get("pdf_timeout", PDF_TIMEOUT))
        self.min_pdf_size: int = int(self.cfg.get("scihub", {}).get("min_pdf_size", MIN_PDF_SIZE))

    def _try_mirrors(self, doi: str) -> tuple[list[str], list[str]]:
        """遍历 self.mirrors，返回 (mirrors_tried, last_errors) 给上层判断

        用于 find() / pull() 共用：所有镜像都走 SSL/网络/超时/空页 错误时，
        携带结构化信息 raise SciHubAllMirrorsFailedError。
        """
        mirrors_tried: list[str] = []
        last_errors: list[str] = []
        for mirror in self.mirrors:
            mirrors_tried.append(mirror)
            doi_url = f"{mirror}/{quote(doi, safe='/:().-_')}"
            try:
                browser = _Browser()
                page_url, html = _fetch_page(browser, doi_url)
            except (HTTPError, URLError, OSError) as e:
                last_errors.append(f"{mirror} → {type(e).__name__}: {e}")
                continue
            if not html:
                last_errors.append(f"{mirror} → empty page (可能验证码未解/被 ban)")
                continue
            return mirrors_tried, last_errors  # 成功拿到 html（调用方继续处理）
        raise SciHubAllMirrorsFailedError(mirrors_tried, last_errors, doi=doi)

    # ==================== find ====================

    def find(self, identifier: str) -> PaperMetadata:
        """根据 DOI 解析元数据（SciHub 页面）

        Args:
            identifier: DOI（必须以 '10.' 开头）

        Returns:
            PaperMetadata（title/authors/year/venue 从 SciHub 页面 citation_* meta 解析）

        Raises:
            ValueError: identifier 不是 DOI 格式
            SciHubAllMirrorsFailedError: 所有镜像都不可访问（带 mirrors_tried + last_errors）
            LookupError: SciHub 库无此论文（且没有 OA 链接）
        """
        if not identifier or not identifier.startswith("10."):
            raise ValueError(f"SciHub 仅支持 DOI（以 '10.' 开头）: {identifier!r}")
        # 遍历镜像拿页面（self.mirrors 走完都失败时 raise SciHubAllMirrorsFailedError）
        oa_link = ""
        last_errors: list[str] = []
        for mirror in self.mirrors:
            doi_url = f"{mirror}/{quote(identifier, safe='/:().-_')}"
            try:
                browser = _Browser()
                page_url, html = _fetch_page(browser, doi_url)
            except (HTTPError, URLError, OSError) as e:
                last_errors.append(f"{mirror} → {type(e).__name__}: {e}")
                continue
            if not html:
                last_errors.append(f"{mirror} → empty page (可能验证码未解/被 ban)")
                continue
            title = _extract_title(html).lower()
            if "not available through sci-hub" in title or "no articles found" in title:
                oa_link = _extract_oa_link(html, page_url) or oa_link
                continue
            return _parse_page_metadata(html, identifier)
        # 所有镜像都失败或全部 not-found
        if oa_link:
            raise LookupError(
                f"SciHub 库无此论文 {identifier}（OA 提示链接：{oa_link}——可能是 publisher 主页而非 PDF）"
            )
        # 走到这里说明全部镜像要么 SSL/超时/空页——raise 结构化异常
        raise SciHubAllMirrorsFailedError(list(self.mirrors), last_errors, doi=identifier)

    # ==================== pull ====================

    def pull(self, meta: PaperMetadata, dest_dir: Path) -> Path:
        """从 SciHub 下载 PDF 到 dest_dir（用 resolve_pdf 拿 URL → 流式下载）"""
        status, url_or_oa = resolve_pdf(meta.doi, cfg=self.cfg)
        if status == STATUS_INVALID_INPUT:
            raise ValueError(f"无效 DOI: {meta.doi}")
        if status == STATUS_NOT_FOUND:
            hint = f"（OA 链接：{url_or_oa}）" if url_or_oa else ""
            raise LookupError(f"SciHub 库无此论文: {meta.doi}{hint}")
        if status == STATUS_MIRROR_ERROR:
            raise SciHubAllMirrorsFailedError(
                list(self.mirrors),
                [f"resolve_pdf 走完所有 {len(self.mirrors)} 镜像都失败"],
                doi=meta.doi,
            )

        dest_dir.mkdir(parents=True, exist_ok=True)
        # 用 doi 做临时文件名（save 阶段会重命名为归档名）
        tmp_name = f"scihub_{meta.doi.replace('/', '_').replace('.', '_')}.pdf"
        pdf_path = dest_dir / tmp_name

        req = Request(url_or_oa, headers=_headers({"Accept": "application/pdf,*/*;q=0.8"}))
        try:
            with build_opener().open(req, timeout=self.pdf_timeout) as resp:
                content_type = (resp.headers.get("Content-Type") or "").lower()
                if "pdf" not in content_type and "octet-stream" not in content_type:
                    raise RuntimeError(
                        f"SciHub 返回非 PDF 内容（Content-Type: {content_type}）"
                    )
                with open(pdf_path, "wb") as f:
                    shutil.copyfileobj(resp, f)
        except (HTTPError, URLError, OSError) as e:
            if pdf_path.exists():
                pdf_path.unlink()
            raise RuntimeError(f"SciHub 下载失败: {e}")

        if pdf_path.stat().st_size < self.min_pdf_size:
            pdf_path.unlink()
            raise RuntimeError(
                f"SciHub 下载文件太小（< {self.min_pdf_size} 字节）: {meta.doi}"
            )

        return pdf_path

    # ==================== save ====================

    def save(self, pdf: Path, meta: PaperMetadata, dest_dir: Path) -> Path:
        """按命名约定归档到 dest_dir（默认 wiki/raw/papers）"""
        target_dir = Path(dest_dir)
        target_dir.mkdir(parents=True, exist_ok=True)
        target_name = meta.archive_filename()
        target_path = target_dir / target_name
        if target_path.exists():
            return target_path
        shutil.move(str(pdf), str(target_path))
        return target_path

    # ==================== fetch（全流水线 override） ====================

    def fetch(
        self,
        identifier: str,
        dest_dir: Path | None = None,
        archive_dir: Path | None = None,
    ) -> Path:
        """完整流水线：find + pull + save（幂等：目标文件已存在直接返回）"""
        meta = self.find(identifier)
        target_dir = Path(archive_dir) if archive_dir else self.archive_dir
        target_path = target_dir / meta.archive_filename()
        if target_path.exists():
            return target_path
        dest = dest_dir or Path("/tmp/scihub_dl")
        pdf = self.pull(meta, dest)
        return self.save(pdf, meta, target_dir)