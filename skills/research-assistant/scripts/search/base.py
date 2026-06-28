"""base.py - BaseSearcher 抽象基类 + Paper 数据类

类用 ABC 统一接口。
方法统一签名：def search(self, **kwargs) -> list[Paper]
子类从 kwargs 解析自己关心的参数（title / author / year / venue / doi / arxiv_id / keyword / limit）。
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar, List, Dict, Optional, Any


@dataclass
class Paper:
    """标准化文献结构（所有 searcher 通用）"""
    title: str = ""
    authors: List[str] = field(default_factory=list)
    year: Optional[int] = None
    venue: str = ""
    doi: str = ""
    url: str = ""
    abstract: str = ""
    citation_count: int = 0
    source: str = ""
    paper_id: str = ""
    external_ids: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "paperId": self.paper_id,
            "source": self.source,
            "title": self.title,
            "authors": self.authors,
            "year": self.year,
            "venue": self.venue,
            "doi": self.doi,
            "url": self.url,
            "abstract": self.abstract,
            "citationCount": self.citation_count,
            "externalIds": self.external_ids,
        }


class BaseSearcher(ABC):
    """文献检索抽象基类（ABC 统一接口）

    子类必须实现 search(**kwargs) -> list[Paper]
    kwargs 字段（按需解析）：
        - title      标题
        - author     作者
        - year       年份
        - year_min   最早年份
        - year_max   最晚年份
        - venue      期刊/会议
        - doi        DOI
        - arxiv_id   arXiv 编号
        - keyword    关键词（搜标题+摘要）
        - limit      最大结果数
    """

    name: ClassVar[str] = ""

    def __init__(self, cfg: dict):
        self.cfg = cfg

    @abstractmethod
    def search(self, **kwargs) -> List[Paper]:
        """真正的检索文献（基于文献字段）"""
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name!r}>"