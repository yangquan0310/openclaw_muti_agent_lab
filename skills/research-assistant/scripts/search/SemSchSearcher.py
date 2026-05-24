#!/usr/bin/env python3
"""
SemSchSearcher.py - Semantic Scholar 英文文献检索

继承 BaseSearcher，通过 Semantic Scholar API 获取英文文献数据。
支持 API Key（环境变量 SEMANTIC_SCHOLAR_API_KEY）。
"""

from __future__ import annotations

import os
import time
import json
import requests
from typing import List, Dict, Optional, Any
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .BaseSearcher import BaseSearcher, Paper


class SemSchSearcher(BaseSearcher):
    """英文文献检索器（Semantic Scholar）"""

    source_name = "Semantic Scholar"

    SEARCH_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
    BATCH_URL = "https://api.semanticscholar.org/graph/v1/paper/batch"

    # 默认请求字段
    FIELDS = (
        "paperId,authors,year,title,venue,citationCount,"
        "journal,externalIds,url,abstract"
    )
    PUBLICATION_TYPES = "Review,MetaAnalysis,JournalArticle,Study"

    def __init__(
        self,
        kb_path: str = "knowledge/index.json",
        api_key: Optional[str] = None,
        request_interval: float = 0.5,
    ):
        """
        Args:
            kb_path:          知识库文件路径
            api_key:          API Key（默认从环境变量 SEMANTIC_SCHOLAR_API_KEY 读取）
            request_interval: 每次 API 请求之间的间隔（秒），避免触发频率限制
        """
        super().__init__(kb_path)
        self.request_interval = request_interval
        self.api_key = api_key or os.environ.get("SEMANTIC_SCHOLAR_API_KEY")

        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})
        if self.api_key:
            self.session.headers.update({"x-api-key": self.api_key})

        retry = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("https://", adapter)

        if not self.api_key:
            print("警告: 未设置 SEMANTIC_SCHOLAR_API_KEY，可能受速率限制")

    # ── 实现抽象方法 ─────────────────────────────────

    def _do_search(
        self,
        keyword: str,
        limit: int = 20,
        year: Optional[str] = None,
        min_citation: Optional[int] = None,
        venue: Optional[str] = None,
        fields_of_study: Optional[str] = None,
        publication_types: Optional[str] = None,
        **kwargs,
    ) -> List[Paper]:
        """
        通过 Semantic Scholar API 检索英文文献。

        Args:
            keyword:          检索关键词（英文）
            limit:            最大结果数（上限 100）
            year:             年份范围，如 "2020-2023"
            min_citation:     最小引用量（客户端过滤）
            venue:            期刊/会议名称过滤
            fields_of_study: 研究领域列表
            publication_types: 文献类型过滤
        """
        params = {
            "query": keyword,
            "limit": min(limit, 100),
            "fields": self.FIELDS,
            "publicationTypes": publication_types or self.PUBLICATION_TYPES,
        }
        if year:
            params["year"] = year
        if venue:
            params["venue"] = venue
        if fields_of_study:
            params["fieldsOfStudy"] = fields_of_study

        try:
            resp = self.session.get(self.SEARCH_URL, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"[SemSchSearcher] 检索失败: {e}")
            return []

        raw_papers = data.get("data", [])
        papers = [self._normalize(raw) for raw in raw_papers]

        # 客户端过滤：最小引用量
        if min_citation is not None:
            papers = [p for p in papers if p.citation_count >= min_citation]

        return papers

    # ── 私有方法 ──────────────────────────────────────

    def _normalize(self, raw: Dict) -> Paper:
        """将 Semantic Scholar API 返回的原始 dict 转为 Paper"""
        authors = []
        for author in raw.get("authors", []):
            name = author.get("name") if isinstance(author, dict) else author
            if name:
                authors.append(name)

        journal = raw.get("journal", {})
        volume = journal.get("volume") if isinstance(journal, dict) else None
        issue = journal.get("issue") if isinstance(journal, dict) else None
        pages = journal.get("pages") if isinstance(journal, dict) else None

        external = raw.get("externalIds", {})
        doi = external.get("DOI") if isinstance(external, dict) else None

        url = raw.get("url")
        paper_id = raw.get("paperId", "")
        if not url and paper_id:
            url = f"https://www.semanticscholar.org/paper/{paper_id}"

        return Paper(
            paper_id=paper_id,
            source="Semantic Scholar",
            authors=authors,
            year=raw.get("year"),
            title=raw.get("title", ""),
            venue=raw.get("venue", ""),
            volume=volume or "",
            issue=issue or "",
            pages=pages or "",
            doi=doi or "",
            url=url or "",
            abstract=raw.get("abstract", ""),
            citation_count=raw.get("citationCount", 0),
        )

    # ── 批量更新（扩展方法）───────────────────────────

    def update_metadata(self, kb_path: Optional[str] = None) -> Dict:
        """
        批量更新知识库中所有论文的元数据（通过 DOI 补全卷期页码等）。
        当前会话绑定的 kb_path 会被覆盖。
        """
        kb_path = kb_path or self.kb_path
        kb_data = self._load_kb(kb_path)
        papers = kb_data.get("papers", [])
        if not papers:
            print("[SemSchSearcher] 知识库为空，无需更新")
            return kb_data

        # 只更新 Semantic Scholar 来源的论文
        ss_papers = [p for p in papers if p.get("source") == "Semantic Scholar"]
        paper_ids = [p.get("paperId") for p in ss_papers if p.get("paperId")]
        if not paper_ids:
            print("[SemSchSearcher] 没有可更新的 paperId")
            return kb_data

        # 批量获取
        all_details = []
        for i in range(0, len(paper_ids), 100):
            batch = paper_ids[i:i + 100]
            try:
                resp = self.session.post(
                    self.BATCH_URL,
                    json={"ids": batch},
                    params={"fields": self.FIELDS},
                    timeout=30,
                )
                resp.raise_for_status()
                details = resp.json() or []
                valid = [d for d in details if d is not None]
                all_details.extend(valid)
            except Exception as e:
                print(f"[SemSchSearcher] 批量获取失败: {e}")
            time.sleep(self.request_interval)

        detail_map = {d.get("paperId"): d for d in all_details}

        for paper in papers:
            pid = paper.get("paperId")
            if pid in detail_map:
                d = detail_map[pid]
                for key in ["authors", "year", "title", "venue",
                             "volume", "issue", "pages", "doi",
                             "url", "abstract", "citationCount"]:
                    val = d.get(key)
                    if val is not None:
                        paper[key] = val

        kb_data["papers"] = papers
        kb_data = self._update_statistics(kb_data)
        self._save_kb(kb_data, kb_path)
        return kb_data
