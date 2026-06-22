#!/usr/bin/env python3
"""
WikiSynthesizer.py - synthesize 模块接入 wiki 后端（v5.16.0）
- 输入：wiki source 替代 topic.json
- 输出：wiki syntheses/<date>-xxx.md
"""

import re
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any


class Synthesizer:
    """从 wiki source 读 abstract，extract_notes 输出到 wiki syntheses/"""

    def __init__(self, wiki_path: str = '~/.openclaw/wiki'):
        self.wiki_path = Path(wiki_path).expanduser()
        self.sources_dir = self.wiki_path / 'sources'
        self.syntheses_dir = self.wiki_path / 'syntheses'
        self.syntheses_dir.mkdir(parents=True, exist_ok=True)

    def _find_source(self, source_id: str) -> Optional[Path]:
        """根据 id 找 source 文件（支持带或不带 .md 后缀）"""
        for candidate in self.sources_dir.glob(f"*{source_id}*"):
            if candidate.suffix == '.md' and not candidate.name.startswith('_'):
                return candidate
        # 也试按 id 字段搜
        for f in self.sources_dir.glob('*.md'):
            if f.name.startswith('_'):
                continue
            content = f.read_text(encoding='utf-8')
            m = re.search(r'^id:\s*(\S+)', content, re.MULTILINE)
            if m and m.group(1) == source_id:
                return f
        return None

    def extract_notes(self, source_id: str, output_path: Optional[str] = None) -> Dict[str, Any]:
        """从单个 wiki source 读，extract 结构化笔记，输出到 wiki syntheses/

        Args:
            source_id: wiki source id（如 source.diehl-2026-captured-memories）
            output_path: 输出路径（可选，默认 wiki syntheses/<date>-extract-<slug>.md）
        Returns:
            dict: {success, output_path, zotero_key, summary_chars, key_content_chars, ...}
        """
        source_file = self._find_source(source_id)
        if not source_file:
            return {"success": False, "error": f"source not found: {source_id}"}

        content = source_file.read_text(encoding='utf-8')

        # 解析 YAML frontmatter
        yaml_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        yaml_text = yaml_match.group(1) if yaml_match else ''

        # 提取字段
        zk_match = re.search(r'^zotero_item_key:\s*(\S+)', yaml_text, re.MULTILINE)
        zotero_key = zk_match.group(1) if zk_match else None
        doi_match = re.search(r'^zotero_doi:\s*(\S+)', yaml_text, re.MULTILINE)
        zotero_doi = doi_match.group(1) if doi_match else None
        title_match = re.search(r'^title:\s*"?([^"\n]+)"?', yaml_text, re.MULTILINE)
        wiki_title = title_match.group(1) if title_match else ''

        # 提取 markdown 内容段
        body = content[yaml_match.end():] if yaml_match else content

        # 一句话总结
        summary_match = re.search(r'## 一句话总结\s*\n\s*(.+?)(?=\n## |\Z)', body, re.DOTALL)
        summary = summary_match.group(1).strip() if summary_match else ''

        # 关键内容
        key_match = re.search(r'## 关键内容\s*\n(.*?)(?=\n## |\Z)', body, re.DOTALL)
        key_content = key_match.group(1).strip() if key_match else ''

        # 构造 synthesis 输出
        if not output_path:
            date = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            slug = source_id.replace('source.', '').replace('.', '-')
            output_path = self.syntheses_dir / f"{date}-extract-{slug}.md"
        else:
            output_path = Path(output_path)

        synthesis = f"""---
pageType: synthesis
id: synthesis.extract.{source_id.replace('source.', '')}
title: Extract Notes — {wiki_title or source_id}
createdAt: "{datetime.now().isoformat(timespec='seconds')}"
zotero_refs:
  - key: {zotero_key or 'PENDING'}
    role: primary
---

# {wiki_title or source_id} — 笔记提取

> 来源：[[sources/{source_file.name}]]
> 提取时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}
> Zotero itemKey: `{zotero_key or '未填'}`

## 一句话总结

{summary or '（无）'}

## 关键内容

{key_content[:3000] or '（无）'}

## 来源信息

| 字段 | 值 |
|---|---|
| wiki source | `sources/{source_file.name}` |
| Zotero itemKey | `{zotero_key or '未填'}` |
| Zotero DOI | `{zotero_doi or '未填'}` |
| 提取时间 | `{datetime.now().isoformat(timespec='seconds')}` |
"""

        output_path.write_text(synthesis, encoding='utf-8')

        return {
            "success": True,
            "output_path": str(output_path),
            "zotero_key": zotero_key,
            "zotero_doi": zotero_doi,
            "summary_chars": len(summary),
            "key_content_chars": len(key_content),
        }


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('用法: python3 WikiSynthesizer.py extract <wiki-source-id>')
        sys.exit(1)
    s = WikiSynthesizer()
    if sys.argv[1] == 'extract':
        result = s.extract_notes(sys.argv[2])
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print('未知命令')
