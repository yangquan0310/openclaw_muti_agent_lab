"""uploader.py - Uploader 类（本地 PDF → Zotero + WebDAV + wiki source）"""

from __future__ import annotations

import os
import re
import subprocess
from datetime import datetime
from pathlib import Path

from scripts.utils import config, WIKI_SOURCES


def _humanize_title_from_filename(pdf_path):
    """从 PDF 文件名解析人类可读 title

    Examples:
        buzsaki-2002-hippocampal-theta.pdf → "2002 - Buzsaki - Hippocampal Theta"
        2026-06-05_Diehl-et-al_Captured-Memories_JARMAC.pdf → "2026 06 05 - Diehl Et Al Captured Memories JARMAC"
    """
    stem = Path(pdf_path).stem if pdf_path else ""
    if not stem:
        return ""
    raw = re.split(r"[_\-]+", stem)
    raw = [t.strip() for t in raw if t.strip()]

    date_prefix = None
    body = list(raw)
    if len(body) >= 3 and re.match(r"^\d{4}$", body[0]) and re.match(r"^\d{1,2}$", body[1]) and re.match(r"^\d{1,2}$", body[2]):
        date_prefix = f"{body[0]} {body[1].zfill(2)} {body[2].zfill(2)}"
        body = body[3:]

    year_prefix = None
    if date_prefix is None:
        for i, tok in enumerate(body):
            if re.match(r"^\d{4}[a-z]?$", tok):
                year_prefix = tok
                body = body[:i] + body[i+1:]
                break

    def _tc(token):
        if not token:
            return token
        if token.isupper() and len(token) <= 8:
            return token
        return token[:1].upper() + token[1:]

    parts = [_tc(t) for t in body if t]
    if year_prefix:
        parts = [year_prefix] + parts
    if date_prefix:
        parts = [date_prefix] + parts
    return " - ".join(parts) if parts else ""


class Uploader:
    """本地 PDF 反向上传工具"""

    ZOTERO_SCRIPT = Path.home() / ".openclaw/skills/zotero/scripts/zotero.py"
    DEFAULT_WEBDAV_REMOTE = "nutstore:quanquanzi/zotero/"
    DEFAULT_WIKI_SOURCES_DIR = WIKI_SOURCES
    DEFAULT_RCLONE_CONF = "~/.config/rclone/rclone.conf"

    def __init__(self, cfg: dict | None = None):
        self.cfg = cfg or config()
        self.webdav_remote = self.cfg.get("jianguoyun", {}).get(
            "remote_root", self.DEFAULT_WEBDAV_REMOTE
        )
        self.wiki_sources_dir = WIKI_SOURCES
        self.wiki_sources_dir.mkdir(parents=True, exist_ok=True)
        self.rclone_conf = os.path.expanduser(
            self.cfg.get("upload", {}).get("rclone_config", self.DEFAULT_RCLONE_CONF)
        )

    # ── Step 1: Zotero ──

    def _add_to_zotero(self, doi: str, tags: list[str] | None = None) -> dict:
        """基于 DOI 在 Zotero 库建条目（包装 zotero.py add-doi）"""
        if not self.ZOTERO_SCRIPT.exists():
            return {"success": False, "error": f"zotero.py not found: {self.ZOTERO_SCRIPT}"}
        cmd = ["python3", str(self.ZOTERO_SCRIPT), "add-doi", doi]
        if tags:
            cmd.extend(["--tags", ",".join(tags)])
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "zotero.py add-doi timeout"}
        match = re.search(r"\b([A-Z0-9]{8})\b", r.stdout)
        return {
            "success": r.returncode == 0,
            "item_key": match.group(1) if match else None,
            "stdout": r.stdout.strip()[-500:] if r.stdout else "",
            "stderr": r.stderr.strip()[-500:] if r.stderr else "",
        }

    # ── Step 2: WebDAV ──

    def _push_webdav(self, pdf_path: Path) -> dict:
        """rclone copyto 推 PDF 到坚果云 WebDAV"""
        if not pdf_path.exists():
            return {"success": False, "error": f"PDF not found: {pdf_path}"}
        remote = f"{self.webdav_remote}{pdf_path.name}"
        try:
            r = subprocess.run(
                ["rclone", "copyto", str(pdf_path), remote, "--config", self.rclone_conf],
                capture_output=True, text=True, timeout=120,
            )
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "rclone copyto timeout"}
        return {
            "success": r.returncode == 0,
            "remote_path": remote,
            "stdout": r.stdout.strip()[-300:] if r.stdout else "",
            "stderr": r.stderr.strip()[-300:] if r.stderr else "",
        }

    # ── Step 3: wiki source ──

    def _create_wiki_source(
        self,
        slug: str,
        pdf_path: Path,
        zotero_meta: dict | None = None,
        title: str | None = None,
    ) -> dict:
        """在 wiki/sources/ 写 source YAML（最小可用，agent 自己补充）"""
        wiki_path = self.wiki_sources_dir / f"{slug}.md"
        if wiki_path.exists():
            return {
                "success": False,
                "error": f"wiki source 已存在: {wiki_path}",
                "wiki_source_path": str(wiki_path),
            }

        zk = (zotero_meta or {}).get("item_key", "PENDING")
        zd = (zotero_meta or {}).get("doi", "")
        now = datetime.now().isoformat(timespec="seconds")

        effective_title = title or _humanize_title_from_filename(pdf_path) or slug

        uploaded_by = (
            os.environ.get("OPENCLAW_AGENT_ID")
            or os.environ.get("OPENCLAW_AGENT_NAME")
            or os.environ.get("AGENT_NAME")
            or os.environ.get("USER")
            or "unknown"
        )

        content = f"""---
pageType: source
id: source.{slug}
createdAt: "{now}"
updatedAt: "{now}"
title: "{effective_title}"
zotero_item_key: {zk}
zotero_doi: "{zd}"
sourceIds: []
aliases: []
provenance:
  type: local_upload
  pdf_path: "{pdf_path}"
  uploaded_by: {uploaded_by}
  uploadedAt: "{now}"
---

# {effective_title}

> **来源**：本地 PDF 上传（v7.0.0 upload 工具）
> **PDF 路径**：`{pdf_path}`
> **状态**：PENDING — 等待 agent 攥写笔记

## agent 待办

- [ ] 跑 `python3 main.py summarize --source-id source.{slug} --pdf-path {pdf_path}` 提数据
- [ ] 攥写笔记 / 综述（**agent 能力**，本工具不攥写）
- [ ] 加 zotero tags / 改 source YAML
"""
        wiki_path.write_text(content, encoding="utf-8")
        return {
            "success": True,
            "wiki_source_path": str(wiki_path),
            "wiki_source_id": f"source.{slug}",
        }

    # ── 流水线 ──

    def upload(
        self,
        pdf_path: str,
        doi: str | None = None,
        slug: str | None = None,
        title: str | None = None,
        tags: list[str] | None = None,
        skip_zotero: bool = False,
        skip_webdav: bool = False,
        skip_wiki: bool = False,
    ) -> dict:
        """完整流水线：add_to_zotero → push_webdav → create_wiki_source

        Args:
            pdf_path: 本地 PDF 路径
            doi: 可选，DOI（如有则建 Zotero 条目）
            slug: 必填或与 doi 二选一（agent 自決唯一标识）
            title: 可选，wiki source title
            tags: 可选，Zotero tags
            skip_zotero / skip_webdav / skip_wiki: 跳过对应步骤
        """
        pdf = Path(os.path.expanduser(pdf_path))
        if not pdf.exists():
            return {"success": False, "error": f"PDF not found: {pdf}"}
        if not doi and not slug:
            return {"success": False, "error": "需要 --doi 或 --slug 其中之一"}

        effective_slug = slug or (doi.replace("/", "-").replace(".", "-") if doi else None)
        result = {
            "success": True,
            "pdf_path": str(pdf),
            "slug": effective_slug,
            "steps": {},
        }

        zotero_meta: dict = {}
        if doi and not skip_zotero:
            zr = self._add_to_zotero(doi, tags=tags)
            result["steps"]["zotero"] = zr
            if zr.get("success") and zr.get("item_key"):
                zotero_meta = {"item_key": zr["item_key"], "doi": doi}

        if not skip_webdav:
            wr = self._push_webdav(pdf)
            result["steps"]["webdav"] = wr

        if not skip_wiki:
            wr_src = self._create_wiki_source(effective_slug, pdf, zotero_meta=zotero_meta, title=title)
            result["steps"]["wiki_source"] = wr_src

        result["success"] = all(s.get("success", True) for s in result["steps"].values())
        return result
