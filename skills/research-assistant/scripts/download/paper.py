"""paper.py - PaperMetadata 数据类（文献元数据 + 归档文件名生成）"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Optional


_STOP_WORDS = {
    "the", "a", "an", "and", "or", "for", "with", "from", "of", "to", "in", "on",
    "at", "by", "is", "are", "was", "were", "be", "been", "being", "as", "that",
    "this", "these", "those", "it", "its", "which", "who", "whom", "whose",
    "effect", "effects", "study", "studies", "research", "analysis", "review",
    "new", "old", "first", "second", "third", "one", "two", "three",
    "we", "our", "they", "their", "his", "her", "he", "she",
}


@dataclass
class PaperMetadata:
    """文献元数据（跨数据源统一）"""
    zotero_item_key: Optional[str] = None
    zotero_attachment_key: Optional[str] = None
    doi: Optional[str] = None
    arxiv_id: Optional[str] = None
    semantic_scholar_id: Optional[str] = None

    title: str = ""
    authors: List[str] = field(default_factory=list)
    year: Optional[int] = None
    month: Optional[int] = None
    day: Optional[int] = None
    venue: Optional[str] = None

    md5: Optional[str] = None
    source_url: Optional[str] = None
    link_mode: str = "imported_url"

    def archive_filename(self) -> str:
        """生成 vault 归档文件名：YYYY-MM[-DD]_作者_关键词_期刊.pdf"""
        if self.year and self.month and self.day:
            date = f"{self.year}-{self.month:02d}-{self.day:02d}"
        elif self.year and self.month:
            date = f"{self.year}-{self.month:02d}"
        elif self.year:
            date = f"{self.year}"
        else:
            date = "unknown"

        if not self.authors:
            authors = "Unknown"
        elif len(self.authors) == 1:
            authors = self.authors[0]
        elif len(self.authors) <= 3:
            authors = "-".join(self.authors)
        else:
            authors = "-".join(self.authors[:2]) + "-et-al"

        keyword = self._extract_keyword()
        venue = self._normalize_venue()

        return f"{date}_{authors}_{keyword}_{venue}.pdf"

    def _extract_keyword(self, n: int = 3) -> str:
        if not self.title:
            return "untitled"
        words = re.findall(r'[A-Z][a-z]+|[A-Z]{2,}|[a-z]{5,}', self.title)
        meaningful = [w for w in words if w.lower() not in _STOP_WORDS][:n]
        return "-".join(meaningful) if meaningful else "untitled"

    def _normalize_venue(self) -> str:
        if not self.venue:
            return "unknown"
        v = self.venue
        v = re.sub(r'\([^)]*\)', '', v)
        v = re.sub(r'^The\s+', '', v, flags=re.IGNORECASE)
        v = re.sub(r'[\s\.]+', '-', v.strip())
        v = re.sub(r'[<>:"/\\|?*]', '', v)
        v = re.sub(r'-+', '-', v).strip('-')
        return v or "unknown"

    def to_dict(self) -> dict:
        return {
            "zotero_item_key": self.zotero_item_key,
            "zotero_attachment_key": self.zotero_attachment_key,
            "doi": self.doi,
            "title": self.title,
            "authors": self.authors,
            "year": self.year,
            "month": self.month,
            "venue": self.venue,
            "md5": self.md5,
            "archive_filename": self.archive_filename(),
        }