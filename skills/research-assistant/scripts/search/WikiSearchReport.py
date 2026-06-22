#!/usr/bin/env python3
"""
WikiSearchReport.py - search 模块接入 wiki report（v5.19.0）
- search 命中后**直接**写入 wiki report（不再写 cache/index.json）
- 按 query/topic 拆分（类似 index.json B 方案）
- 老板 00:45 指令："以后把搜索到内容，像这样，写入report"

不向后兼容（v5.16.0 老板指令"不需要向后兼容，全部改为 wiki"）：
- 旧 search → cache/index.json 路径**已废弃**
- 新 WikiSearchReport.search() 默认写 wiki/reports/<date>-search-<topic>.md
"""

import json
import re
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

# 兼容包内/直接脚本运行
try:
    from .Searcher import Searcher
except (ImportError, ValueError):
    sys.path.insert(0, str(Path(__file__).parent))
    from Searcher import Searcher


class WikiSearchReport(Searcher):
    """Searcher 扩展：search 命中后**直接**写 wiki report"""

    def __init__(self,
                 wiki_path: str = '~/.openclaw/wiki',
                 kb_path: str = 'cache/report.json',  # 临时缓存（不持久化）
                 topic: Optional[str] = None,  # query 对应的 topic（用于分类）
                 api_key: Optional[str] = None,
                 **kwargs):
        """初始化
        Args:
            wiki_path: wiki 根目录
            kb_path: 临时缓存路径（默认 cache/report.json，**不**作为权威存储）
            topic: query 对应的 topic（用于 report 文件命名）
        """
        super().__init__(kb_path=kb_path, api_key=api_key, **kwargs)
        self.wiki_path = Path(wiki_path).expanduser()
        self.reports_dir = self.wiki_path / 'reports'
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.topic = topic or 'general'
        self.cache_dir = Path(kb_path).parent
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def search(self, queries, write_report: bool = True, **kwargs) -> Dict[str, Any]:
        """执行检索 + 写 wiki report

        Args:
            queries: 查询 dict
            write_report: 是否写 wiki report（默认 True）
        Returns:
            dict: 原 Searcher 返回 + 字段 'wiki_report_path'
        """
        # 1. 调父类 search（用临时 cache）
        result = super().search(queries, **kwargs)
        papers = result.get('papers', [])

        if not write_report or not papers:
            return result

        # 2. 写 wiki report
        report_path = self._write_report(papers, queries)
        result['wiki_report_path'] = str(report_path)
        result['wiki_topic'] = self.topic
        result['wiki_report_paper_count'] = len(papers)

        return result

    def _write_report(self, papers: List[Dict], queries: Any) -> Path:
        """把 search 命中的 papers 写到 wiki reports/<date>-search-<topic>.md"""
        # 提取 query 关键词（用于报告标题）
        query_kw = []
        if isinstance(queries, dict):
            for q in queries.get('queries', []):
                if isinstance(q, dict) and 'q' in q:
                    query_kw.append(q['q'])
        query_str = ' / '.join(query_kw[:3]) if query_kw else self.topic

        date_str = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        slug = re.sub(r'[^\w\-]', '_', self.topic)[:50]
        report_path = self.reports_dir / f"{date_str}-search-{slug}.md"

        md_lines = [
            '---',
            f'pageType: report',
            f'id: report.search-{slug}-{date_str}',
            f'title: "Search Report — {query_str}"',
            f'createdAt: "{datetime.now().isoformat(timespec="seconds")}"',
            f'sources:',
            f'  - search query: {query_str}',
            '---',
            '',
            f'# Search Report — {query_str}',
            '',
            f'> Topic: {self.topic}',
            f'> Papers: **{len(papers)}**',
            f'> 生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M")}',
            '',
            '## Papers',
            '',
        ]

        for i, p in enumerate(papers, 1):
            title = p.get('title', '?')
            authors = p.get('authors', [])
            if isinstance(authors, list) and authors:
                if isinstance(authors[0], dict):
                    author_str = ', '.join([a.get('name', '?') for a in authors[:3]])
                else:
                    author_str = ', '.join([str(a) for a in authors[:3]])
            else:
                author_str = '?'
            year = p.get('year', '?')
            venue = p.get('venue', '?')
            doi = p.get('doi', '') or p.get('externalIds', {}).get('DOI', '')
            cite = p.get('citationCount', 0)

            md_lines.append(f'### {i}. {title}')
            md_lines.append('')
            md_lines.append(f'- **作者**: {author_str}')
            md_lines.append(f'- **年份**: {year} | **期刊**: {venue}')
            if doi:
                md_lines.append(f'- **DOI**: [{doi}](https://doi.org/{doi})')
            md_lines.append(f'- **引用**: {cite}')
            md_lines.append('')

        report_path.write_text('\n'.join(md_lines), encoding='utf-8')
        return report_path


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('用法: python3 WikiSearchReport.py --keyword "<query>" [--topic <topic>] [--limit N]')
        print('  默认: search 命中后直接写 wiki reports/<date>-search-<topic>.md')
        sys.exit(1)

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--keyword', required=True)
    parser.add_argument('--topic', default='general')
    parser.add_argument('--limit', type=int, default=20)
    parser.add_argument('--dry-run', action='store_true', help='不写 wiki report')
    args = parser.parse_args()

    queries = {'queries': [{'query': args.keyword, 'limit': args.limit}]}
    s = WikiSearchReport(topic=args.topic)
    result = s.search(queries, write_report=not args.dry_run)

    print(f'✅ Papers: {len(result.get("papers", []))}')
    print(f'✅ Wiki report: {result.get("wiki_report_path", "N/A (dry-run)")}')
