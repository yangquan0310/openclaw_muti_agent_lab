#!/usr/bin/env python3
"""
ArxivSearcher.py - arXiv 预印本检索器（v6.0.5+）

继承 BaseSearcher，通过 arXiv API（export.arxiv.org/api/query）检索预印本。
无 API key、无频率限制（arXiv 建议间隔 ≥ 3 秒）。

支持：
  - 全文检索（all fields）
  - 按分类过滤（cat:math.CT / cat:cond-mat / cat:q-bio.NC 等）
  - 年份范围（submittedDate 过滤）

工具边界（v6.0.5 落实）：
  - 只调 arXiv API，不调 LLM，不攥写 narrative
  - 标准化 → Paper → 走 BaseSearcher.merge_to_kb
"""

from __future__ import annotations

import re
import time
import urllib.parse
import urllib.request
from typing import List, Dict, Optional

from .BaseSearcher import BaseSearcher, Paper


class ArxivSearcher(BaseSearcher):
    """arXiv 预印本检索器（v6.0.5+）"""

    source_name = "arXiv"

    API_URL = "http://export.arxiv.org/api/query"

    def __init__(
        self,
        kb_path: str = "wiki/sources/cache.json",
        request_interval: float = 3.0,  # arXiv TOS 建议 ≥3s
    ):
        super().__init__(kb_path)
        self.request_interval = request_interval

    # ── 实现抽象方法 ─────────────────────────────────

    def _do_search(
        self,
        keyword: str,
        limit: int = 20,
        category: Optional[str] = None,    # arXiv 分类（如 "math.CT"）
        year_min: Optional[int] = None,
        year_max: Optional[int] = None,
        **kwargs,
    ) -> List[Paper]:
        """
        通过 arXiv API 检索预印本。

        Args:
            keyword:    检索关键词（全文）
            limit:      最大结果数（arXiv 单页 ≤ 50）
            category:   arXiv 主分类（如 math.CT / cond-mat / q-bio.NC）
            year_min:   起始年份（按 submittedDate 过滤）
            year_max:   截止年份（按 submittedDate 过滤）
        """
        limit = min(limit, 50)

        # 构造查询字符串
        query_parts = [f'all:{self._escape_query(keyword)}']
        if category:
            query_parts.append(f'cat:{category}')
        query = " AND ".join(query_parts)

        params = {
            "search_query": query,
            "start": "0",
            "max_results": str(limit),
            "sortBy": "relevance",
            "sortOrder": "descending",
        }
        url = f"{self.API_URL}?{urllib.parse.urlencode(params)}"

        try:
            with urllib.request.urlopen(url, timeout=30) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
        except Exception as e:
            print(f"[ArxivSearcher] 请求失败: {e}")
            return []

        papers = self._parse_atom_feed(raw)

        # 年份过滤
        if year_min or year_max:
            filtered = []
            for p in papers:
                y = p.year or 0
                if year_min and y < year_min:
                    continue
                if year_max and y > year_max:
                    continue
                filtered.append(p)
            papers = filtered

        return papers

    # ── 工具方法 ─────────────────────────────────────

    @staticmethod
    def _escape_query(q: str) -> str:
        """转义 arXiv 查询特殊字符"""
        # arXiv 查询用双引号包裹短语，但简单场景下不需要
        return q.replace('"', ' ').strip()

    def _parse_atom_feed(self, xml_text: str) -> List[Paper]:
        """解析 arXiv Atom feed（轻量 XML 解析，不依赖 lxml）"""
        papers: List[Paper] = []

        # 按 <entry> 切分
        entries = re.findall(r"<entry>(.*?)</entry>", xml_text, re.DOTALL)
        for entry in entries:
            arxiv_id = self._extract_tag(entry, "id")
            # arXiv id 通常在 <id>http://arxiv.org/abs/2501.12345v1</id>
            arxiv_id_clean = arxiv_id.split("/abs/")[-1].split("v")[0] if "/abs/" in arxiv_id else ""

            title = self._extract_tag(entry, "title")
            summary = self._extract_tag(entry, "summary")
            published = self._extract_tag(entry, "published")  # ISO 8601
            year = None
            if published:
                m = re.match(r"^(\d{4})", published)
                if m:
                    year = int(m.group(1))

            # 作者列表
            authors = []
            for author_match in re.finditer(r"<author>\s*<name>([^<]+)</name>", entry):
                authors.append(author_match.group(1).strip())

            # 分类（可能多个）
            categories = re.findall(r'<category\s+term="([^"]+)"', entry)
            primary_cat = categories[0] if categories else ""

            # DOI（如果有）
            doi_match = re.search(r'<arxiv:doi[^>]*>([^<]+)</arxiv:doi>', entry)
            doi = doi_match.group(1).strip() if doi_match else ""

            url = f"https://arxiv.org/abs/{arxiv_id_clean}" if arxiv_id_clean else ""

            papers.append(Paper(
                paper_id=arxiv_id_clean,
                source="arXiv",
                authors=authors,
                year=year,
                title=title,
                venue=f"arXiv [{primary_cat}]" if primary_cat else "arXiv",
                doi=doi,
                url=url,
                abstract=summary[:2000],  # 截断避免知识库过大
                citation_count=0,  # arXiv API 不提供引用数
            ))

        return papers

    @staticmethod
    def _extract_tag(xml_text: str, tag: str) -> str:
        """提取 XML 标签内容（单行场景）"""
        m = re.search(rf"<{tag}[^>]*>(.*?)</{tag}>", xml_text, re.DOTALL)
        if not m:
            return ""
        return re.sub(r"\s+", " ", m.group(1)).strip()


if __name__ == "__main__":
    # 简单自测
    s = ArxivSearcher()
    papers = s._do_search("topology manifold", limit=3, category="math.AT")
    for p in papers:
        print(f"  [{p.year}] {p.title} ({p.paper_id})")
        print(f"    authors: {', '.join(p.authors[:3])}")
        print(f"    venue: {p.venue}")
        print(f"    url: {p.url}")
        print()
