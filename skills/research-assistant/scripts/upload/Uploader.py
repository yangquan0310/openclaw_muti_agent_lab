"""Uploader.py - 本地 PDF 反向上传工具（v6.0.3+）

download 模块的反向对偶：
- download: 远端 Zotero / WebDAV → 本地 wiki raw（find_paper + download_pdf + archive_to_wiki）
- upload:   本地 PDF → 远端 Zotero / WebDAV + wiki source（add_to_zotero + push_to_webdav + create_wiki_source）

工具边界（v6.0.3 明确）：
- 工具只做数据搬运（本地 → 远端 + wiki 索引）
- 工具不攥写笔记 / 综述（agent 拿到 wiki source 后自己写）
"""

from __future__ import annotations

import os
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional


def _humanize_title_from_filename(pdf_path) -> str:
    """从 PDF 文件名解析人类可读 title（v6.0.5+ 默认 fallback）

    Examples:
        buzsaki-2002-hippocampal-theta.pdf  →  "2002 - Buzsaki - Hippocampal Theta"
        Diehl-et-al_Captured-Memories_JARMAC.pdf → "Diehl Et Al Captured Memories JARMAC"
        2026-06-05_Diehl-et-al_Captured-Memories_JARMAC.pdf → "2026 06 05 - Diehl Et Al Captured Memories JARMAC"

    设计要点（v6.0.5+ 心理学用户痛点 2 修复）：
      - 用 stem 去扩展名
      - 按 _/- 拆段，年份（4 位数字）作前缀，其他段 Title-Case
      - 工具做最小决策（不攥写 narrative），agent 拿到后可自由覆盖
      - 缩写词（≤8 字符全大写）保留（避免把 JARMAC 改成 Jarmac）
    """
    from pathlib import Path as _P
    stem = _P(pdf_path).stem if pdf_path else ""
    if not stem:
        return ""

    import re as _re
    raw_tokens = _re.split(r"[_\-]+", stem)
    raw_tokens = [t.strip() for t in raw_tokens if t.strip()]

    # 检测日期前缀（如 2026-06-05）—— 整体作前缀
    date_prefix = None
    body_tokens = list(raw_tokens)
    if len(body_tokens) >= 3:
        if (_re.match(r"^\d{4}$", body_tokens[0])
                and _re.match(r"^\d{1,2}$", body_tokens[1])
                and _re.match(r"^\d{1,2}$", body_tokens[2])):
            date_prefix = f"{body_tokens[0]} {body_tokens[1].zfill(2)} {body_tokens[2].zfill(2)}"
            body_tokens = body_tokens[3:]

    # 检测年份段（4 位数字）—— 单年份作前缀
    year_prefix = None
    if date_prefix is None:
        for i, tok in enumerate(body_tokens):
            if _re.match(r"^\d{4}[a-z]?$", tok):
                year_prefix = tok
                body_tokens = body_tokens[:i] + body_tokens[i+1:]
                break

    # Title-Case（保留缩写词）
    def _tc(token: str) -> str:
        if not token:
            return token
        if token.isupper() and len(token) <= 8:
            return token
        return token[:1].upper() + token[1:]

    parts = [_tc(t) for t in body_tokens if t]
    if year_prefix:
        parts = [year_prefix] + parts
    if date_prefix:
        parts = [date_prefix] + parts
    if not parts:
        return ""
    return " - ".join(parts)


class Uploader:
    """本地 PDF 反向上传工具（v6.0.3+）"""

    ZOTERO_SCRIPT = Path.home() / ".openclaw/skills/zotero/scripts/zotero.py"
    DEFAULT_WEBDAV_REMOTE = "nutstore:quanquanzi/zotero/"
    DEFAULT_WIKI_SOURCES_DIR = "~/.openclaw/wiki/sources"
    DEFAULT_RCLONE_CONF = "~/.config/rclone/rclone.conf"

    def __init__(
        self,
        webdav_remote: Optional[str] = None,
        wiki_sources_dir: Optional[str] = None,
        rclone_conf: Optional[str] = None,
    ):
        self.webdav_remote = webdav_remote or self.DEFAULT_WEBDAV_REMOTE
        self.wiki_sources_dir = Path(os.path.expanduser(wiki_sources_dir or self.DEFAULT_WIKI_SOURCES_DIR))
        self.rclone_conf = os.path.expanduser(rclone_conf or self.DEFAULT_RCLONE_CONF)
        self.wiki_sources_dir.mkdir(parents=True, exist_ok=True)

    # ── Step 1: Zotero 建条目（如有 DOI） ──

    def add_to_zotero(self, doi: str, tags: Optional[list] = None) -> Dict:
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
        # 解析输出找 8 字符 item key
        match = re.search(r"\b([A-Z0-9]{8})\b", r.stdout)
        return {
            "success": r.returncode == 0,
            "item_key": match.group(1) if match else None,
            "stdout": r.stdout.strip()[-500:] if r.stdout else "",
            "stderr": r.stderr.strip()[-500:] if r.stderr else "",
        }

    # ── Step 2: WebDAV 推 PDF ──

    def push_to_webdav(self, pdf_path: Path) -> Dict:
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

    # ── Step 3: 创建 wiki source YAML ──

    def create_wiki_source(
        self,
        slug: str,
        pdf_path: Path,
        zotero_meta: Optional[Dict] = None,
        title: Optional[str] = None,
    ) -> Dict:
        """在 wiki/sources/ 写 source YAML（最小可用，agent 自己补充）

        slug 必填且由 agent 传（避免工具替 agent 决策命名）
        """
        wiki_path = self.wiki_sources_dir / f"{slug}.md"
        if wiki_path.exists():
            return {"success": False, "error": f"wiki source 已存在: {wiki_path}", "wiki_source_path": str(wiki_path)}

        zk = (zotero_meta or {}).get("item_key", "PENDING")
        zd = (zotero_meta or {}).get("doi", "")
        now = datetime.now().isoformat(timespec="seconds")
        # v6.0.5+: title 默认从 PDF 文件名解析（替代 v6.0.4 的 slug 兜底）
        # 优先级：agent 显式传 title > PDF 文件名解析 > slug 兜底
        effective_title = title or _humanize_title_from_filename(pdf_path) or slug
        # v6.0.6+：多 agent 协作追溯——按 OPENCLAW_AGENT_ID → OPENCLAW_AGENT_NAME → USER → "unknown" 兜底
        # 修复 v6.0.3 硬编码 "steward"（audit 报告 #1：多 agent 场景下审计追溯不准确）
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

> **来源**：本地 PDF 上传（v6.0.3+ upload 工具）
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

    def run(
        self,
        pdf_path: str,
        doi: Optional[str] = None,
        slug: Optional[str] = None,
        title: Optional[str] = None,
        tags: Optional[list] = None,
        no_zotero: bool = False,
        no_webdav: bool = False,
        no_wiki: bool = False,
    ) -> Dict:
        """完整流水线：add_to_zotero → push_to_webdav → create_wiki_source

        参数：
          pdf_path: 本地 PDF 路径
          doi: 可选，DOI（如有则建 Zotero 条目）
          slug: 必填或与 doi 二选一，wiki source 唯一标识（agent 自決）
          title: 可选，wiki source title
          tags: 可选，Zotero tags
          no_zotero / no_webdav / no_wiki: 跳过对应步骤
        """
        pdf = Path(os.path.expanduser(pdf_path))
        if not pdf.exists():
            return {"success": False, "error": f"PDF not found: {pdf}"}
        if not doi and not slug:
            return {"success": False, "error": "需要 --doi 或 --slug 其中之一（agent 自決唯一标识）"}
        # 默认 slug 用 pdf stem（仅当 doi 已传但 slug 没传时）
        effective_slug = slug or (doi.replace("/", "-").replace(".", "-") if doi else None)
        result = {"success": True, "pdf_path": str(pdf), "slug": effective_slug, "steps": {}}

        # Step 1: Zotero 建条目
        zotero_meta = {}
        if doi and not no_zotero:
            zr = self.add_to_zotero(doi, tags=tags)
            result["steps"]["zotero"] = zr
            if zr.get("success") and zr.get("item_key"):
                zotero_meta = {"item_key": zr["item_key"], "doi": doi}

        # Step 2: WebDAV 推
        if not no_webdav:
            wr = self.push_to_webdav(pdf)
            result["steps"]["webdav"] = wr

        # Step 3: wiki source
        if not no_wiki:
            wr_src = self.create_wiki_source(effective_slug, pdf, zotero_meta=zotero_meta, title=title)
            result["steps"]["wiki_source"] = wr_src

        # 整体 success：所有跑的步骤都成功
        result["success"] = all(
            s.get("success", True) for s in result["steps"].values()
        )
        return result