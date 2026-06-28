"""synthesizer.py - Synthesizer 类（综述素材抽取）"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

from scripts.utils import config, frontmatter, WIKI_SOURCES, WIKI_SYNTHESES


class Synthesizer:
    """从 wiki source 抽两段（summary + key_content）→ 写 syntheses/"""

    def __init__(self, cfg: dict | None = None):
        self.cfg = cfg or config()
        self.sources_dir = WIKI_SOURCES
        self.syntheses_dir = WIKI_SYNTHESES
        self.syntheses_dir.mkdir(parents=True, exist_ok=True)

    def _find_source(self, source_id: str) -> Path | None:
        if not self.sources_dir.exists():
            return None
        for f in self.sources_dir.glob("*.md"):
            if f.name.startswith("_"):
                continue
            content = f.read_text(encoding="utf-8")
            meta, _ = frontmatter(content)
            if meta.get("id") == source_id:
                return f
        return None

    def extract(self, source_id: str, output_path: str | None = None) -> dict:
        """主入口：从 source body 抽两段 → 写 syntheses/

        Args:
            source_id: wiki source id（如 source.diehl-2026-captured-memories）
            output_path: 自定义输出路径（可选）

        Returns:
            {success, output_path, zotero_key, summary_chars, key_content_chars}
        """
        source_file = self._find_source(source_id)
        if not source_file:
            return {"success": False, "error": f"source not found: {source_id}"}

        content = source_file.read_text(encoding="utf-8")
        meta, body = frontmatter(content)

        zk = meta.get("zotero_item_key") or ""
        zd = meta.get("zotero_doi") or ""
        title = meta.get("title", "") or source_id

        # 抽 "## 一句话总结" 段
        summary_match = re.search(r"## 一句话总结\s*\n\s*(.+?)(?=\n## |\Z)", body, re.DOTALL)
        summary = summary_match.group(1).strip() if summary_match else ""

        # 抽 "## 关键内容" 段
        key_match = re.search(r"## 关键内容\s*\n(.*?)(?=\n## |\Z)", body, re.DOTALL)
        key_content = key_match.group(1).strip() if key_match else ""

        if not output_path:
            date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            slug = source_id.replace("source.", "").replace(".", "-")
            output_path = self.syntheses_dir / f"{date}-extract-{slug}.md"
        else:
            output_path = Path(output_path)

        md = f"""---
pageType: synthesis
id: synthesis.extract.{source_id.replace('source.', '')}
title: Extract Notes — {title}
createdAt: "{datetime.now().isoformat(timespec='seconds')}"
zotero_refs:
  - key: {zk or 'PENDING'}
    role: primary
---

# {title} — 笔记提取

> 来源：[[sources/{source_file.name}]]
> 提取时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}
> Zotero itemKey: `{zk or '未填'}`

## 一句话总结

{summary or '（无）'}

## 关键内容

{key_content[:3000] or '（无）'}

## 来源信息

| 字段 | 值 |
|---|---|
| wiki source | `sources/{source_file.name}` |
| Zotero itemKey | `{zk or '未填'}` |
| Zotero DOI | `{zd or '未填'}` |
| 提取时间 | `{datetime.now().isoformat(timespec='seconds')}` |
"""

        output_path.write_text(md, encoding="utf-8")

        return {
            "success": True,
            "output_path": str(output_path),
            "zotero_key": zk,
            "zotero_doi": zd,
            "summary_chars": len(summary),
            "key_content_chars": len(key_content),
        }
