#!/usr/bin/env python3
"""
WikiSummesizer.py - summarize 模块接入 wiki 后端（v5.16.0）
- 输入：wiki source 替代 index.json
- 输出：wiki syntheses/<date>-summarize-<id>.md
- 简化：不做 LLM 调用（避免费用/API key 风险），按规则做 type 分类 + notes 提取
"""

import re
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, Any


class Summarizer:
    """从 wiki source 读，summarize 输出到 wiki syntheses/"""

    def __init__(self, wiki_path: str = '~/.openclaw/wiki'):
        self.wiki_path = Path(wiki_path).expanduser()
        self.sources_dir = self.wiki_path / 'sources'
        self.syntheses_dir = self.wiki_path / 'syntheses'
        self.syntheses_dir.mkdir(parents=True, exist_ok=True)

    def _find_source(self, source_id: str) -> Optional[Path]:
        for candidate in self.sources_dir.glob(f"*{source_id}*"):
            if candidate.suffix == '.md' and not candidate.name.startswith('_'):
                return candidate
        for f in self.sources_dir.glob('*.md'):
            if f.name.startswith('_'):
                continue
            content = f.read_text(encoding='utf-8')
            m = re.search(r'^id:\s*(\S+)', content, re.MULTILINE)
            if m and m.group(1) == source_id:
                return f
        return None

    def _classify_type(self, content: str) -> str:
        """根据正文内容规则分类（不调 LLM）"""
        content_lower = content.lower()
        if '综述' in content or 'review' in content_lower or '元分析' in content or 'meta-analysis' in content_lower:
            return 'review'
        if 'preprint' in content or 'arxiv' in content_lower:
            return 'preprint'
        if 'report' in content_lower or '报告' in content:
            return 'report'
        return 'paper'

    def _calc_importance(self, content: str) -> str:
        """根据内容估算重要度（5⭐/4⭐/3⭐/2⭐）"""
        if 'meta-analysis' in content.lower() or '元分析' in content:
            return '5⭐'
        if '5 个研究' in content or 'n=709' in content or '多研究' in content:
            return '4⭐'
        if '预注册' in content or 'preregistered' in content.lower():
            return '4⭐'
        return '3⭐'

    def summarize(self, source_id: str, output_path: Optional[str] = None) -> Dict[str, Any]:
        """从单个 wiki source 读，做 summarize（简化版），输出到 wiki syntheses/"""
        source_file = self._find_source(source_id)
        if not source_file:
            return {"success": False, "error": f"source not found: {source_id}"}

        content = source_file.read_text(encoding='utf-8')

        # 解析 YAML
        yaml_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        yaml_text = yaml_match.group(1) if yaml_match else ''
        body = content[yaml_match.end():] if yaml_match else content

        # 提取字段
        zk_match = re.search(r'^zotero_item_key:\s*(\S+)', yaml_text, re.MULTILINE)
        zotero_key = zk_match.group(1) if zk_match else None
        doi_match = re.search(r'^zotero_doi:\s*(\S+)', yaml_text, re.MULTILINE)
        zotero_doi = doi_match.group(1) if doi_match else None
        title_match = re.search(r'^title:\s*"?([^"\n]+)"?', yaml_text, re.MULTILINE)
        wiki_title = title_match.group(1) if title_match else ''

        # 分类 + 重要度
        paper_type = self._classify_type(body)
        importance = self._calc_importance(body)

        # 提取 notes 段
        notes_match = re.search(r'## 关键内容\s*\n(.*?)(?=\n## |\Z)', body, re.DOTALL)
        notes = notes_match.group(1).strip() if notes_match else ''

        # 输出路径
        if not output_path:
            date = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            slug = source_id.replace('source.', '').replace('.', '-')
            output_path = self.syntheses_dir / f"{date}-summarize-{slug}.md"
        else:
            output_path = Path(output_path)

        summary_md = f"""---
pageType: synthesis
id: synthesis.summarize.{source_id.replace('source.', '')}
title: Summarize — {wiki_title or source_id}
createdAt: "{datetime.now().isoformat(timespec='seconds')}"
zotero_refs:
  - key: {zotero_key or 'PENDING'}
    role: primary
---

# {wiki_title or source_id} — 文献总结

> 来源：[[sources/{source_file.name}]]
> 总结时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}
> 简化模式（不调 LLM，规则分类 + 关键内容提取）

## 分类

| 字段 | 值 |
|---|---|
| 类型 | **{paper_type}** |
| 重要度 | **{importance}** |
| Zotero itemKey | `{zotero_key or '未填'}` |
| Zotero DOI | `{zotero_doi or '未填'}` |

## 关键内容

{notes[:3000] or '（无）'}

## 提取时间

{datetime.now().isoformat(timespec='seconds')}
"""
        output_path.write_text(summary_md, encoding='utf-8')

        return {
            "success": True,
            "output_path": str(output_path),
            "zotero_key": zotero_key,
            "paper_type": paper_type,
            "importance": importance,
            "notes_chars": len(notes),
        }


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('用法: python3 WikiSummesizer.py summarize <wiki-source-id>')
        sys.exit(1)
    s = WikiSummesizer()
    if sys.argv[1] == 'summarize':
        result = s.summarize(sys.argv[2])
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print('未知命令')
