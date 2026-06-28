"""semantic_scholar.py - Semantic Scholar 检索器"""

from __future__ import annotations

import os
import time
from typing import List

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from scripts.search.base import BaseSearcher, Paper


class SemanticScholarSearcher(BaseSearcher):
    """英文文献检索器（Semantic Scholar API）"""

    name = "semantic_scholar"

    SEARCH_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
    BATCH_URL = "https://api.semanticscholar.org/graph/v1/paper/batch"
    FIELDS = (
        "paperId,authors,year,title,venue,citationCount,"
        "journal,externalIds,url,abstract"
    )

    def __init__(self, cfg: dict):
        super().__init__(cfg)
        sem_cfg = cfg.get("semantic_scholar", {})
        self.request_interval = sem_cfg.get("request_interval", 0.5)
        self.api_key = sem_cfg.get("api_key", "")

        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})
        if self.api_key:
            self.session.headers.update({"x-api-key": self.api_key})
        retry = Retry(
            total=3, backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retry))

    def search(self, **kwargs) -> List[Paper]:
        """检索 Semantic Scholar

        kwargs:
            keyword: 关键词
            limit: 最大结果数（默认 20）
            year_min / year_max: 年份范围
            title / author / venue / doi: 暂未直接用（SemSch API 主要支持 keyword + year）
        """
        keyword = kwargs.get("keyword", "")
        limit = kwargs.get("limit", 20)
        year_min = kwargs.get("year_min")
        year_max = kwargs.get("year_max")
        if not keyword:
            return []

        params = {
            "query": keyword,
            "limit": min(limit, 100),
            "fields": self.FIELDS,
        }
        if year_min or year_max:
            y_low = year_min or ""
            y_high = year_max or ""
            params["year"] = f"{y_low}-{y_high}"

        try:
            resp = self.session.get(self.SEARCH_URL, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"[semantic_scholar] 请求失败: {e}")
            return []

        time.sleep(self.request_interval)
        papers = []
        for item in data.get("data", []):
            authors = [a.get("name", "") for a in item.get("authors", []) if a.get("name")]
            ext = item.get("externalIds") or {}
            papers.append(Paper(
                title=item.get("title", ""),
                authors=authors,
                year=item.get("year"),
                venue=item.get("venue") or item.get("journal", ""),
                doi=ext.get("DOI", ""),
                url=item.get("url", ""),
                abstract=item.get("abstract", "") or "",
                citation_count=item.get("citationCount", 0) or 0,
                source=self.name,
                paper_id=item.get("paperId", ""),
                external_ids=ext,
            ))
        return papers