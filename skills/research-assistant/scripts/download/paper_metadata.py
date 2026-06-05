"""paper_metadata.py - 文献元数据数据结构 + 文件名生成

定义 PaperMetadata 数据类，承载从 Zotero / Semantic Scholar / CrossRef
等来源抽取的统一元数据，并生成 vault 归档命名（YYYY-MM[-DD]_作者_关键词_期刊.pdf）。
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


# 标题停用词（用于从标题抽取关键词）
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
    # 来源标识
    zotero_item_key: Optional[str] = None
    zotero_attachment_key: Optional[str] = None
    doi: Optional[str] = None
    arxiv_id: Optional[str] = None
    semantic_scholar_id: Optional[str] = None

    # 核心字段
    title: str = ""
    authors: List[str] = field(default_factory=list)  # 仅姓氏 ["Barasch", "Diehl", ...]
    year: Optional[int] = None
    month: Optional[int] = None
    day: Optional[int] = None
    venue: Optional[str] = None  # 期刊/会议名

    # 文件相关
    md5: Optional[str] = None
    source_url: Optional[str] = None
    link_mode: str = "imported_url"  # imported_url / imported_file / linked_url

    def archive_filename(self) -> str:
        """生成 vault 归档文件名：YYYY-MM[-DD]_作者_关键词_期刊.pdf

        命名约定（参考 wiki/raw/README.md）：
        - 日期优先用论文正式发表日；缺日用月初
        - 作者 1-3 位全列，>3 位用前 2 位 + et-al
        - 关键词取标题前 3 个实词
        - 期刊名压缩为 hyphen-case
        """
        # 1. 日期
        if self.year and self.month and self.day:
            date = f"{self.year}-{self.month:02d}-{self.day:02d}"
        elif self.year and self.month:
            date = f"{self.year}-{self.month:02d}"
        elif self.year:
            date = f"{self.year}"
        else:
            date = "unknown"

        # 2. 作者
        if not self.authors:
            authors = "Unknown"
        elif len(self.authors) == 1:
            authors = self.authors[0]
        elif len(self.authors) <= 3:
            authors = "-".join(self.authors)
        else:
            authors = "-".join(self.authors[:2]) + "-et-al"

        # 3. 关键词
        keyword = self._extract_keyword()

        # 4. 期刊
        venue = self._normalize_venue()

        return f"{date}_{authors}_{keyword}_{venue}.pdf"

    def _extract_keyword(self, n: int = 3) -> str:
        """从标题抽取 n 个关键词（驼峰或大写词优先）"""
        if not self.title:
            return "untitled"
        # 取所有"实词"候选
        words = re.findall(r'[A-Z][a-z]+|[A-Z]{2,}|[a-z]{5,}', self.title)
        # 过滤停用词
        meaningful = [w for w in words if w.lower() not in _STOP_WORDS][:n]
        return "-".join(meaningful) if meaningful else "untitled"

    def _normalize_venue(self) -> str:
        """期刊/会议名压缩为 hyphen-case"""
        if not self.venue:
            return "unknown"
        v = self.venue
        # 去掉括号内容
        v = re.sub(r'\([^)]*\)', '', v)
        # 去掉 "The " 开头
        v = re.sub(r'^The\s+', '', v, flags=re.IGNORECASE)
        # 替换空格和点为 hyphen
        v = re.sub(r'[\s\.]+', '-', v.strip())
        # 移除其他非法字符
        v = re.sub(r'[<>:"/\\|?*]', '', v)
        # 合并连续 hyphen
        v = re.sub(r'-+', '-', v).strip('-')
        return v or "unknown"

    def to_dict(self) -> dict:
        """序列化为 dict（用于日志/JSON 输出）"""
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
