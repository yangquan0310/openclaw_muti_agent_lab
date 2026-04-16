#!/usr/bin/env python3
"""
Searcher.py - 从 Semantic Scholar 获取原始数据并标准化

使用方式：
    searcher = Searcher()
    # 检索并保存到知识库
    kb = searcher.search(queries, kb_path="my_kb.json")
    # 更新知识库中的元数据（DOI、卷期页码等）
    kb = searcher.update(kb_path="my_kb.json")
"""

import os
import time
import json
import requests
from datetime import datetime
from typing import List, Dict, Optional, Union, Any
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class Searcher:
    """文献检索与知识库管理（路径作为方法参数）"""

    # API 端点
    SEARCH_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
    BATCH_URL = "https://api.semanticscholar.org/graph/v1/paper/batch"

    # 默认字段
    FIELDS = "paperId,authors,year,title,venue,citationCount,journal,externalIds,url,abstract"
    PUBLICATION_TYPES = "Review,MetaAnalysis,JournalArticle,Study"

    def __init__(self, api_key: Optional[str] = None):
        """初始化检索器（不绑定知识库路径）"""
        self.api_key = api_key or os.environ.get('SEMANTIC_SCHOLAR_API_KEY')
        if not self.api_key:
            print("警告: 未设置 Semantic Scholar API key，可能受到速率限制")

        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})
        if self.api_key:
            self.session.headers.update({"x-api-key": self.api_key})

        # 重试策略
        retry = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('https://', adapter)

    # ==================== 公共方法 ====================

    def search(self, queries: Dict[str, List[Dict]],
               kb_path: str = "index.json",
               fields: Optional[str] = None,
               deduplicate: bool = True,
               **global_params) -> Dict:
        """
        检索文献并更新知识库（每个条件必须为字典，且包含 'query' 键）
        Args:
            queries: {主题: [条件字典列表]}，每个条件字典必须包含：
                - query (必需): 检索关键词
                - limit (可选): 本次检索数量
                - year (可选): 年份范围，如 "2020-2023"
                - minCitationCount (可选): 最小引用量（客户端过滤）
                - venue (可选): 期刊/会议名称
                - fields_of_study (可选): 研究领域
                - publication_types (可选): 文献类型，默认使用类属性 PUBLICATION_TYPES
            kb_path: 知识库文件路径
            fields: 请求字段，默认 FIELDS
            deduplicate: 是否去重
            **global_params: 全局默认参数（会被条件字典中的同名字段覆盖）
        Returns:
            知识库字典（包含 papers 列表）
        """
        kb_data = self._load_kb(kb_path)
        existing_papers = kb_data.get('papers', [])
        fields = fields or self.FIELDS
        all_new_papers = []

        for topic, conditions in queries.items():
            print(f"\n【主题: {topic}】")
            for idx, cond in enumerate(conditions, 1):
                query = cond.get('query')
                if not query:
                    print(f"  错误: 第{idx}个条件缺少 'query' 字段，跳过")
                    continue

                # 合并参数：全局参数 + 条件字典（条件覆盖全局）
                params = {**global_params, **cond}
                params.pop('query', None)  # 移除 query，已单独提取
                limit = params.pop('limit', 20)
                pub_types = params.pop('publication_types', self.PUBLICATION_TYPES)

                print(f"  轮次 {idx}: 检索 '{query}'")
                if params.get('year'):
                    print(f"    年份: {params['year']}")
                if params.get('minCitationCount'):
                    print(f"    最小引用: {params['minCitationCount']}")

                papers = self._search_single_query(
                    query, limit, fields, pub_types, **params
                )
                for p in papers:
                    p['topic'] = [topic]
                    p['labels'] = {"type": "", "importance": "", "JCR": ""}
                all_new_papers.extend(papers)
                print(f"    获取 {len(papers)} 篇")
                time.sleep(0.5)

        if deduplicate:
            before = len(all_new_papers)
            all_new_papers = self._deduplicate(all_new_papers)
            print(f"新检索去重: {before} -> {len(all_new_papers)} 篇")

        combined = existing_papers + all_new_papers
        combined = self._deduplicate(combined)
        kb_data['papers'] = combined
        kb_data = self._update_statistics(kb_data)
        self._save_kb(kb_data, kb_path)
        return kb_data

    def update(self, kb_path: str = "index.json", fields: Optional[str] = None) -> Dict:
        """
        更新知识库中所有论文的元数据（批量获取详情）
        Args:
            kb_path: 知识库文件路径
            fields: 请求字段，默认 FIELDS
        Returns:
            知识库字典
        """
        kb_data = self._load_kb(kb_path)
        papers = kb_data.get('papers', [])
        if not papers:
            print("知识库为空，无需更新")
            return kb_data

        paper_ids = [p.get('paperId') for p in papers if p.get('paperId')]
        if not paper_ids:
            print("没有有效的 paperId，无法更新")
            return kb_data

        fields = fields or self.FIELDS
        details = self._fetch_batch(paper_ids, fields)
        detail_map = {d['paperId']: d for d in details if d.get('paperId')}

        for paper in papers:
            pid = paper.get('paperId')
            if pid and pid in detail_map:
                detail = detail_map[pid]
                # 更新标准化字段（保留 topic, labels 等）
                for key in ['authors', 'year', 'title', 'venue', 'volume', 'issue', 'pages', 'doi', 'url', 'abstract', 'citationCount']:
                    if detail.get(key) is not None:
                        paper[key] = detail[key]

        kb_data['papers'] = papers
        kb_data = self._update_statistics(kb_data)
        self._save_kb(kb_data, kb_path)
        return kb_data

    # ==================== 私有辅助方法 ====================

    def _load_kb(self, kb_path: str) -> Dict:
        """加载知识库 JSON 文件，若不存在则返回新结构"""
        if os.path.exists(kb_path):
            with open(kb_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"已加载知识库: {kb_path}, 共 {len(data.get('papers', []))} 篇论文")
            return data
        else:
            print(f"知识库 {kb_path} 不存在，创建新知识库")
            return {
                "version": "1.0.0",
                "project": "",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "statistics": {
                    "total_count": 0, "total_citations": 0,
                    "foundation_count": 0, "important_count": 0, "general_count": 0,
                    "empirical_count": 0, "review_count": 0, "theory_count": 0
                },
                "papers": []
            }

    def _save_kb(self, kb_data: Dict, kb_path: str):
        """保存知识库到文件"""
        os.makedirs(os.path.dirname(os.path.abspath(kb_path)), exist_ok=True)
        with open(kb_path, 'w', encoding='utf-8') as f:
            json.dump(kb_data, f, ensure_ascii=False, indent=2)
        print(f"知识库已保存: {kb_path}")

    def _update_statistics(self, kb_data: Dict) -> Dict:
        """重新计算统计信息并更新时间戳"""
        papers = kb_data.get('papers', [])
        total = len(papers)
        total_cites = sum(p.get('citationCount', 0) for p in papers)
        foundation = sum(1 for p in papers if p.get('citationCount', 0) >= 500)
        important = sum(1 for p in papers if 50 <= p.get('citationCount', 0) < 500)
        general = total - foundation - important
        empirical = sum(1 for p in papers if p.get('labels', {}).get('type') == '📊实证')
        review = sum(1 for p in papers if p.get('labels', {}).get('type') == '📖综述')
        theory = sum(1 for p in papers if p.get('labels', {}).get('type') == '💡理论')
        kb_data['statistics'] = {
            "total_count": total,
            "total_citations": total_cites,
            "foundation_count": foundation,
            "important_count": important,
            "general_count": general,
            "empirical_count": empirical,
            "review_count": review,
            "theory_count": theory
        }
        kb_data['updated_at'] = datetime.now().isoformat()
        if not kb_data.get('created_at'):
            kb_data['created_at'] = datetime.now().isoformat()
        return kb_data

    def _search_single_query(self, query: str, limit: int, fields: str,
                             publication_types: str, **kwargs) -> List[Dict]:
        """单次检索，支持 minCitationCount 客户端过滤"""
        params = {
            "query": query,
            "limit": min(limit, 100),
            "fields": fields,
            "publicationTypes": publication_types
        }
        if 'year' in kwargs:
            params["year"] = kwargs['year']
        if 'venue' in kwargs:
            params["venue"] = kwargs['venue']
        if 'fields_of_study' in kwargs:
            params["fieldsOfStudy"] = kwargs['fields_of_study']

        try:
            resp = self.session.get(self.SEARCH_URL, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            raw_papers = data.get('data', [])
            papers = [self._normalize(p) for p in raw_papers]
            # 客户端过滤最小引用量
            min_cite = kwargs.get('minCitationCount')
            if min_cite is not None:
                papers = [p for p in papers if p.get('citationCount', 0) >= min_cite]
            return papers
        except Exception as e:
            print(f"检索失败: {e}")
            return []

    def _fetch_batch(self, paper_ids: List[str], fields: str) -> List[Dict]:
        """批量获取论文详情（自动分批）"""
        all_papers = []
        for i in range(0, len(paper_ids), 100):
            batch = paper_ids[i:i+100]
            payload = {"ids": batch}
            try:
                resp = self.session.post(self.BATCH_URL, json=payload, params={"fields": fields}, timeout=30)
                resp.raise_for_status()
                data = resp.json()
                raw_papers = data if isinstance(data, list) else data.get('data', [])
                # 过滤None值
                valid_papers = [p for p in raw_papers if p is not None]
                all_papers.extend([self._normalize(p) for p in valid_papers])
                time.sleep(0.5)
            except Exception as e:
                print(f"批量获取失败: {e}")
        return all_papers

    def _normalize(self, raw: Dict) -> Dict:
        """标准化单篇论文（基础字段）"""
        authors = []
        for author in raw.get('authors', []):
            if isinstance(author, dict):
                name = author.get('name')
                if name:
                    authors.append(name)
            elif isinstance(author, str):
                authors.append(author)

        journal = raw.get('journal', {})
        volume = journal.get('volume') if isinstance(journal, dict) else None
        issue = journal.get('issue') if isinstance(journal, dict) else None
        pages = journal.get('pages') if isinstance(journal, dict) else None

        external = raw.get('externalIds', {})
        doi = external.get('DOI') if isinstance(external, dict) else None

        url = raw.get('url')
        if not url and raw.get('paperId'):
            url = f"https://www.semanticscholar.org/paper/{raw['paperId']}"

        return {
            "paperId": raw.get('paperId'),
            "authors": authors,
            "year": raw.get('year'),
            "title": raw.get('title'),
            "venue": raw.get('venue'),
            "volume": volume,
            "issue": issue,
            "pages": pages,
            "doi": doi,
            "url": url,
            "abstract": raw.get('abstract'),
            "citationCount": raw.get('citationCount', 0)
        }

    def _deduplicate(self, papers: List[Dict]) -> List[Dict]:
        """基于 paperId 去重"""
        seen = set()
        unique = []
        for p in papers:
            pid = p.get('paperId')
            if pid and pid not in seen:
                seen.add(pid)
                unique.append(p)
            elif not pid:
                title = p.get('title')
                if title and title not in seen:
                    seen.add(title)
                    unique.append(p)
        return unique


# ==================== 命令行入口 ====================
if __name__ == "__main__":
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(
        description="Searcher - 文献检索工具"
    )
    subparsers = parser.add_subparsers(title="命令", dest="command")
    
    # search 命令
    search_parser = subparsers.add_parser("search", help="检索文献")
    search_parser.add_argument("--queries", required=True, help="检索条件JSON文件路径")
    search_parser.add_argument("--kb-path", default="index.json", help="知识库文件路径 (默认: index.json)")
    search_parser.add_argument("--fields", help="请求字段 (可选)")
    search_parser.add_argument("--no-deduplicate", action="store_true", help="不去重")
    
    # update 命令
    update_parser = subparsers.add_parser("update", help="更新知识库元数据")
    update_parser.add_argument("--kb-path", default="index.json", help="知识库文件路径 (默认: index.json)")
    update_parser.add_argument("--fields", help="请求字段 (可选)")
    
    args = parser.parse_args()
    
    searcher = Searcher()
    
    if args.command == "search":
        # 加载检索条件
        if not os.path.exists(args.queries):
            print(f"错误: 检索条件文件不存在: {args.queries}")
            sys.exit(1)
        
        with open(args.queries, 'r', encoding='utf-8') as f:
            queries = json.load(f)
        
        print(f"正在检索...")
        kb = searcher.search(
            queries, 
            kb_path=args.kb_path,
            fields=args.fields,
            deduplicate=not args.no_deduplicate
        )
        print(f"完成! 知识库: {args.kb_path}, 论文数: {len(kb['papers'])}")
    
    elif args.command == "update":
        print(f"正在更新元数据...")
        kb = searcher.update(
            kb_path=args.kb_path,
            fields=args.fields
        )
        print(f"完成! 知识库: {args.kb_path}, DOI非空: {sum(1 for p in kb['papers'] if p.get('doi'))}")
    
    else:
        parser.print_help()