#!/usr/bin/env python3
"""
WikiManager.py - manage 模块接入 wiki 后端（v5.16.0）
- merge: 按 zotero_item_key 去重
- filter: 按 wiki YAML 字段筛选
- statistics: 统计 wiki 现状
"""

import re
import json
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any


class Manager:
    """以 wiki 为存储后端的 manage 模块"""

    def __init__(self, wiki_path: str = '~/.openclaw/wiki'):
        self.wiki_path = Path(wiki_path).expanduser()
        self.sources_dir = self.wiki_path / 'sources'
        self.concepts_dir = self.wiki_path / 'concepts'
        self.syntheses_dir = self.wiki_path / 'syntheses'
        self.reports_dir = self.wiki_path / 'reports'

    def list_sources(self) -> List[Dict[str, Any]]:
        """列出所有 wiki source"""
        result = []
        for f in self.sources_dir.glob('*.md'):
            if f.name.startswith('_'):
                continue
            content = f.read_text(encoding='utf-8')
            yaml_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
            if not yaml_match:
                continue
            yaml_text = yaml_match.group(1)
            m = re.search(r'^id:\s*(\S+)', yaml_text, re.MULTILINE)
            if not m:
                continue
            zk = re.search(r'^zotero_item_key:\s*(\S+)', yaml_text, re.MULTILINE)
            doi = re.search(r'^zotero_doi:\s*(\S+)', yaml_text, re.MULTILINE)
            title = re.search(r'^title:\s*"?([^"\n]+)"?', yaml_text, re.MULTILINE)
            page_type = re.search(r'^pageType:\s*(\S+)', yaml_text, re.MULTILINE)
            result.append({
                'id': m.group(1),
                'file': str(f.relative_to(self.wiki_path)),
                'title': title.group(1) if title else '',
                'zotero_item_key': zk.group(1) if zk else None,
                'zotero_doi': doi.group(1) if doi else None,
                'pageType': page_type.group(1) if page_type else 'source',
            })
        return result

    def merge(self, *source_ids: str) -> List[Dict[str, Any]]:
        """合并多个 wiki source，按 zotero_item_key 去重"""
        all_sources = self.list_sources()
        by_zk = {}
        by_id = {}
        for s in all_sources:
            zk = s.get('zotero_item_key')
            if zk:
                by_zk.setdefault(zk, s)
            by_id[s['id']] = s

        result = []
        seen = set()
        for sid in source_ids:
            s = by_id.get(sid)
            if not s:
                continue
            zk = s.get('zotero_item_key')
            if zk and zk in seen:
                continue
            if zk:
                seen.add(zk)
            result.append(s)
        return result

    def filter(self, conditions: Dict[str, Any]) -> List[Dict[str, Any]]:
        """按 wiki YAML 字段筛选 source"""
        sources = self.list_sources()
        result = []
        for s in sources:
            ok = True
            if 'has_zotero_key' in conditions:
                if conditions['has_zotero_key'] and not s.get('zotero_item_key'):
                    ok = False
                if not conditions['has_zotero_key'] and s.get('zotero_item_key'):
                    ok = False
            if 'has_doi' in conditions:
                if conditions['has_doi'] and not s.get('zotero_doi'):
                    ok = False
                if not conditions['has_doi'] and s.get('zotero_doi'):
                    ok = False
            if 'pageType' in conditions:
                if s.get('pageType') != conditions['pageType']:
                    ok = False
            if ok:
                result.append(s)
        return result

    def statistics(self) -> Dict[str, Any]:
        """统计 wiki 现状"""
        all_sources = self.list_sources()
        all_concepts = list(self.concepts_dir.glob('*.md')) if self.concepts_dir.exists() else []
        all_syntheses = list(self.syntheses_dir.glob('*.md')) if self.syntheses_dir.exists() else []
        all_reports = list(self.reports_dir.glob('*.md')) if self.reports_dir.exists() else []

        with_zk = sum(1 for s in all_sources if s.get('zotero_item_key'))
        with_doi = sum(1 for s in all_sources if s.get('zotero_doi'))
        page_types = {}
        for s in all_sources:
            pt = s.get('pageType', 'unknown')
            page_types[pt] = page_types.get(pt, 0) + 1

        return {
            'total_sources': len(all_sources),
            'sources_with_zotero_key': with_zk,
            'sources_with_doi': with_doi,
            'sources_by_pageType': page_types,
            'total_concepts': len(all_concepts),
            'total_syntheses': len(all_syntheses),
            'total_reports': len(all_reports),
            'computed_at': datetime.now().isoformat(timespec='seconds'),
        }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['list', 'filter', 'merge', 'stats'])
    parser.add_argument('--ids', nargs='*', help='source ids')
    parser.add_argument('--has-zotero-key', type=lambda v: v.lower() == 'true')
    parser.add_argument('--has-doi', type=lambda v: v.lower() == 'true')
    parser.add_argument('--page-type')
    args = parser.parse_args()

    m = WikiManager()
    if args.command == 'list':
        for s in m.list_sources():
            print(f"{s['id'][:50]:50s} zk={s.get('zotero_item_key') or 'N/A':10s} type={s.get('pageType', '?')}")
    elif args.command == 'filter':
        cond = {}
        if args.has_zotero_key is not None:
            cond['has_zotero_key'] = args.has_zotero_key
        if args.has_doi is not None:
            cond['has_doi'] = args.has_doi
        if args.page_type:
            cond['pageType'] = args.page_type
        for s in m.filter(cond):
            print(f"{s['id'][:50]:50s} zk={s.get('zotero_item_key') or 'N/A'}")
    elif args.command == 'merge':
        result = m.merge(*(args.ids or []))
        print(json.dumps({'merged_count': len(result), 'merged': [s['id'] for s in result]}, indent=2, ensure_ascii=False))
    elif args.command == 'stats':
        print(json.dumps(m.statistics(), indent=2, ensure_ascii=False))
