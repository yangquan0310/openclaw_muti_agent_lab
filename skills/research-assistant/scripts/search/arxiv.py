"""arxiv.py - arXiv 预印本检索器"""

from __future__ import annotations

import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import List

from scripts.search.base import BaseSearcher, Paper


class ArxivSearcher(BaseSearcher):
    """arXiv 检索器（数学/物理预印本）"""

    name = "arxiv"

    API_URL = "http://export.arxiv.org/api/query"
    NS = {"atom": "http://www.w3.org/2005/Atom"}

    def __init__(self, cfg: dict):
        super().__init__(cfg)
        arxiv_cfg = cfg.get("arxiv", {})
        self.request_interval = arxiv_cfg.get("request_interval", 3.0)

    def search(self, **kwargs) -> List[Paper]:
        """检索 arXiv

        kwargs:
            keyword: 检索关键词（必填）
            limit: 最大结果数（默认 20）
            category: arXiv 分类（如 "math.CT"）
            year_min / year_max: 年份范围
        """
        keyword = kwargs.get("keyword", "")
        limit = kwargs.get("limit", 20)
        category = kwargs.get("category")
        year_min = kwargs.get("year_min")
        year_max = kwargs.get("year_max")
        if not keyword:
            return []

        query = f"all:{keyword}"
        if category:
            query = f"({query}) AND cat:{category}"

        params = {
            "search_query": query,
            "start": 0,
            "max_results": min(limit, 50),
            "sortBy": "relevance",
            "sortOrder": "descending",
        }
        url = f"{self.API_URL}?{urllib.parse.urlencode(params)}"
        try:
            resp = urllib.request.urlopen(url, timeout=30)
            xml = resp.read()
        except Exception as e:
            print(f"[arxiv] 请求失败: {e}")
            return []

        time.sleep(self.request_interval)
        papers = []
        try:
            root = ET.fromstring(xml)
        except ET.ParseError as e:
            print(f"[arxiv] XML 解析失败: {e}")
            return []
        for entry in root.findall("atom:entry", self.NS):
            title = entry.findtext("atom:title", "", self.NS).strip()
            title = re.sub(r"\s+", " ", title)
            summary = entry.findtext("atom:summary", "", self.NS).strip()
            id_url = entry.findtext("atom:id", "", self.NS)
            arxiv_id = id_url.split("/")[-1] if id_url else ""
            published = entry.findtext("atom:published", "", self.NS)
            year_m = re.search(r"^(\d{4})", published)
            year = int(year_m.group(1)) if year_m else None
            if year_min and year and year < year_min:
                continue
            if year_max and year and year > year_max:
                continue
            authors = [
                a.findtext("atom:name", "", self.NS)
                for a in entry.findall("atom:author", self.NS)
            ]
            doi = ""
            for link in entry.findall("atom:link", self.NS):
                href = link.get("href", "")
                if "doi.org" in href:
                    doi = href.split("doi.org/")[-1]
                    break
            papers.append(Paper(
                title=title,
                authors=authors,
                year=year,
                venue="arXiv",
                doi=doi,
                url=id_url,
                abstract=summary,
                citation_count=0,
                source=self.name,
                paper_id=arxiv_id,
                external_ids={"ArXiv": arxiv_id},
            ))
        return papers