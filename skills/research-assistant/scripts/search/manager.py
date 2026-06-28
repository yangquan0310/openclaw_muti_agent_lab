"""manager.py - SearchManager（编排器：选 source + 调 searcher 检索）"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import List

from scripts.utils import WIKI_REPORTS
from scripts.search.base import BaseSearcher, Paper
from scripts.search.semantic_scholar import SemanticScholarSearcher
from scripts.search.google_scholar import GoogleScholarSearcher
from scripts.search.cnki import CnkiSearcher
from scripts.search.arxiv import ArxivSearcher


class SearchManager:
    """搜索 source 编排器：选 source，不调 API

    真正的检索文献由 BaseSearcher 子类的 search(**kwargs) 完成。
    """

    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.sources: dict[str, BaseSearcher] = {
            "semantic_scholar": SemanticScholarSearcher(cfg),
            "google_scholar": GoogleScholarSearcher(cfg),
            "cnki": CnkiSearcher(cfg),
            "arxiv": ArxivSearcher(cfg),
        }
        self.reports_dir = WIKI_REPORTS
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def pick(self, source: str | None = None, **kwargs) -> BaseSearcher:
        """选 source

        Args:
            source: 指定 source 名（如 "cnki"）；None 则自动路由
            **kwargs: 用于自动路由的辅助参数（keyword）

        Returns:
            BaseSearcher 实例
        """
        if source:
            if source not in self.sources:
                raise ValueError(f"未知 source: {source}（可选: {list(self.sources.keys())}）")
            return self.sources[source]
        primary, _ = self._route(kwargs.get("keyword", ""))
        return primary

    def search(self, **kwargs) -> dict:
        """统一入口：自动路由 + fallback + 写 wiki report

        kwargs:
            keyword: 检索关键词
            source: 指定 source（可选，覆盖自动路由）
            sources: 多源列表（可选）
            limit: 最大结果数
            year_min / year_max: 年份范围
            topic: 报告分类（默认 "general"）
            write_report: 是否写 wiki report（默认 True）
        """
        if "source" in kwargs:
            # 单源
            source = kwargs.pop("source")
            return {
                "success": True,
                "primary_engine": source,
                "fallback_used": None,
                "papers": [p.to_dict() for p in self.sources[source].search(**kwargs)],
            }

        if "sources" in kwargs:
            # 多源并行
            sources = kwargs.pop("sources")
            all_papers = []
            for s in sources:
                papers = self.sources[s].search(**kwargs)
                all_papers.extend(p.to_dict() for p in papers)
            return {
                "success": True,
                "primary_engine": "multi",
                "fallback_used": None,
                "papers": all_papers,
            }

        # 自动路由 + fallback
        keyword = kwargs.get("keyword", "")
        primary, fallback = self._route(keyword)
        limit = kwargs.get("limit", 20)
        papers = primary.search(**kwargs)
        fallback_used = None
        if fallback and len(papers) < limit:
            extra = fallback.search(**{**kwargs, "limit": limit - len(papers)})
            papers.extend(extra)
            fallback_used = fallback.name

        # 写 wiki report
        report_path = None
        if kwargs.get("write_report", True):
            report_path = self._report(
                papers,
                keyword,
                kwargs.get("topic", "general"),
            )

        return {
            "success": True,
            "primary_engine": primary.name,
            "fallback_used": fallback_used,
            "papers_count": len(papers),
            "report_path": str(report_path) if report_path else None,
            "papers": [p.to_dict() for p in papers],
        }

    # === 内部方法 ===

    def _route(self, keyword: str) -> tuple[BaseSearcher, BaseSearcher | None]:
        """自动路由决策

        - 中文 → CNKI（primary）+ SemSch（fallback）
        - 英文 + 数/物关键词 → arXiv（primary）+ SemSch（fallback）
        - 英文 → SemSch（primary）+ Google Scholar（fallback）
        """
        if not keyword:
            return self.sources["semantic_scholar"], self.sources["google_scholar"]
        if self._chinese(keyword):
            return self.sources["cnki"], self.sources["semantic_scholar"]
        if self._arxiv(keyword):
            return self.sources["arxiv"], self.sources["semantic_scholar"]
        return self.sources["semantic_scholar"], self.sources["google_scholar"]

    def _chinese(self, text: str) -> bool:
        return bool(re.search(r"[\u4e00-\u9fff]", text))

    _ARXIV_PATTERNS = [
        r"\btheorem\b", r"\bconjecture\b", r"\bmanifold\b", r"\btopology\b",
        r"\bhomotopy\b", r"\bgroup\s+theory\b", r"\bquantum\b",
        r"\bhamiltonian\b", r"\bschroedinger\b", r"\bschrödinger\b",
        r"\barxiv\b", r"\bpreprint\b", r"\bcosmology\b", r"\bmanifold\s+learning\b",
        r"\bgeometric\s+deep\s+learning\b", r"\btopological\s+data\s+analysis\b",
    ]

    def _arxiv(self, keyword: str) -> bool:
        if self._chinese(keyword):
            return False
        kw = keyword.lower()
        return any(re.search(p, kw) for p in self._ARXIV_PATTERNS)

    def _report(self, papers: List[Paper], keyword: str, topic: str) -> Path | None:
        """写 wiki report"""
        if not papers:
            return None
        date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        slug = re.sub(r"[^\w\-]", "_", topic)[:50]
        path = self.reports_dir / f"{date}-search-{slug}.md"
        lines = [
            "---",
            "pageType: report",
            f'id: report.search-{slug}-{date}',
            f'title: "Search Report — {keyword}"',
            f'createdAt: "{datetime.now().isoformat(timespec="seconds")}"',
            "---",
            "",
            f"# Search Report — {keyword}",
            "",
            f"> Topic: {topic}",
            f"> Papers: **{len(papers)}**",
            f'> 生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M")}',
            "",
            "## Papers",
            "",
        ]
        for i, p in enumerate(papers, 1):
            authors = ", ".join(p.authors[:3]) if p.authors else "?"
            year = p.year if p.year else "?"
            venue = p.venue or "?"
            doi = p.doi
            cite = p.citation_count
            lines.append(f"### {i}. {p.title}")
            lines.append("")
            lines.append(f"- **作者**: {authors}")
            lines.append(f"- **年份**: {year} | **期刊**: {venue}")
            if doi:
                lines.append(f"- **DOI**: [{doi}](https://doi.org/{doi})")
            lines.append(f"- **引用**: {cite}")
            lines.append("")
        path.write_text("\n".join(lines), encoding="utf-8")
        return path