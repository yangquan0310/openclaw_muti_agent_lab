#!/usr/bin/env python3
"""
ZoteroSearcher.py - 继承 Searcher，加 Zotero 自动入库能力
v5.15.0：search 接入 Zotero（最小骨架，向后兼容）

用法：
    from search.ZoteroSearcher import ZoteroSearcher
    s = ZoteroSearcher(add_to_zotero=True)
    result = s.search(queries)  # 同时写 index.json + add 到 Zotero
"""

import os
import sys
from pathlib import Path
from typing import Dict, Optional

# 兼容包内 import 和直接脚本运行
try:
    from .Searcher import Searcher
    from .ZoteroAdder import ZoteroAdder
except (ImportError, ValueError):
    sys.path.insert(0, str(Path(__file__).parent))
    from Searcher import Searcher
    from ZoteroAdder import ZoteroAdder


class ZoteroSearcher(Searcher):
    """Searcher 扩展：search 命中后自动 add 到 Zotero 库"""

    def __init__(self, kb_path: str = "cache/index.json",
                 api_key: Optional[str] = None,
                 add_to_zotero: bool = False,
                 dry_run: bool = False,
                 **kwargs):
        """初始化
        Args:
            kb_path: index.json cache 路径（默认 cache/，不再用 knowledge/）
            add_to_zotero: search 命中后是否自动 add 到 Zotero
            dry_run: True 则只预览，不实际 add
        """
        super().__init__(kb_path=kb_path, api_key=api_key, **kwargs)
        self.add_to_zotero = add_to_zotero
        self.dry_run = dry_run
        if add_to_zotero:
            self.adder = ZoteroAdder()

    def search(self, queries, **kwargs):
        """执行检索 + 可选 add 到 Zotero

        Returns:
            dict: 原 Searcher 返回 + 字段 'zotero_results'（如果 add_to_zotero=True）
        """
        result = super().search(queries, **kwargs)

        if self.add_to_zotero:
            papers = result.get('papers', [])
            zotero_results = self.adder.add_papers(papers, dry_run=self.dry_run)
            result['zotero_results'] = zotero_results
            result['zotero_summary'] = {
                'total': len(zotero_results),
                'added': sum(1 for r in zotero_results if r.get('added')),
                'duplicate': sum(1 for r in zotero_results if r.get('error') == 'duplicate'),
                'failed': sum(1 for r in zotero_results if not r.get('added') and r.get('error') not in ('duplicate', None)),
            }

        return result


# === CLI ===
if __name__ == '__main__':
    import sys
    import json

    if len(sys.argv) < 2:
        print('用法: python3 ZoteroSearcher.py --query "<keyword>" [--add-to-zotero] [--dry-run] [--limit N]')
        sys.exit(1)

    args = sys.argv[1:]
    query = None
    add_to_zotero = '--add-to-zotero' in args
    dry_run = '--dry-run' in args
    limit = 20
    for i, a in enumerate(args):
        if a == '--query' and i+1 < len(args):
            query = args[i+1]
        if a == '--limit' and i+1 < len(args):
            limit = int(args[i+1])

    if not query:
        # 用 search --keyword 模式
        if '--keyword' in args:
            query = args[args.index('--keyword') + 1]

    if not query:
        print('错误: 必须提供 --query 或 --keyword')
        sys.exit(1)

    # 构造 queries dict
    queries = {'queries': [{'q': query, 'limit': limit}]}

    s = ZoteroSearcher(add_to_zotero=add_to_zotero, dry_run=dry_run)
    result = s.search(queries)

    if add_to_zotero:
        print(f'\n=== Zotero 同步结果 ===')
        print(json.dumps(result.get('zotero_summary', {}), indent=2, ensure_ascii=False))
    else:
        # 默认只显示前 5 篇
        papers = result.get('papers', [])[:5]
        print(f'\n=== 命中 {len(result.get("papers", []))} 篇（前 5） ===')
        for p in papers:
            print(f'- {p.get("title", "?")[:80]}')
            print(f'  DOI: {p.get("doi", "无")}')
