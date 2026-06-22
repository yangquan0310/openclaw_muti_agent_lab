#!/usr/bin/env python3
"""
ZoteroAdder.py - 把 search 命中的 papers 直接 add 到 Zotero 库
v5.15.0：search 接入 Zotero 的最小实现（不动 Searcher.py，向后兼容）
"""

import os
import subprocess
import json
from pathlib import Path


class ZoteroAdder:
    """将 paper 列表 add 到 Zotero 库（v5.15.0）"""

    def __init__(self, zotero_script='~/.openclaw/skills/zotero/scripts/zotero.py'):
        self.zotero_script = Path(os.path.expanduser(zotero_script))

    def add_paper(self, paper):
        """添加单篇 paper 到 Zotero

        Args:
            paper: dict with 'doi' or 'title' field
        Returns:
            dict: {'added': bool, 'itemKey': str|None, 'title': str, 'error': str|None}
        """
        doi = self._extract_doi(paper)
        title = paper.get('title', '?')

        if not doi:
            return {'added': False, 'itemKey': None, 'title': title, 'error': 'no_doi'}

        result = subprocess.run(
            ['python3', str(self.zotero_script), 'add-doi', doi],
            capture_output=True, text=True, timeout=30
        )
        out = result.stdout

        # 解析结果
        if 'Added:' in out:
            # 提取 itemKey
            m = out.split('[')
            if len(m) > 1:
                key = m[1].split(']')[0]
            else:
                key = None
            return {'added': True, 'itemKey': key, 'title': title, 'error': None}
        elif 'already' in out.lower() or 'duplicate' in out.lower():
            return {'added': False, 'itemKey': None, 'title': title, 'error': 'duplicate'}
        else:
            return {'added': False, 'itemKey': None, 'title': title, 'error': out[:200]}

    def add_papers(self, papers, dry_run=False):
        """批量添加 papers

        Args:
            papers: list of paper dicts
            dry_run: True 则不实际 add，只返回预览
        Returns:
            list of result dicts
        """
        results = []
        for p in papers:
            if dry_run:
                results.append({
                    'dry_run': True,
                    'title': p.get('title', '?'),
                    'doi': self._extract_doi(p),
                })
            else:
                results.append(self.add_paper(p))
        return results

    def _extract_doi(self, paper):
        """从 paper 字典提 DOI（兼容多种格式）"""
        if 'doi' in paper and paper['doi']:
            return paper['doi']
        # SemSch 格式
        ext = paper.get('externalIds', {})
        if isinstance(ext, dict) and 'DOI' in ext:
            return ext['DOI']
        return None
