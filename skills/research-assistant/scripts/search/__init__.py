"""search/ - 文献检索（ABC 统一接口 + kwargs 多态）

- BaseSearcher: 抽象基类（4 个 searcher 子类继承）
- SearchManager: 编排器（选 source + 调 searcher 检索）
- 4 个 searcher: semantic_scholar / google_scholar / cnki / arxiv

类用 ABC，方法统一签名为 `def search(**kwargs) -> list[Paper]`。
"""

from scripts.search.base import BaseSearcher, Paper
from scripts.search.semantic_scholar import SemanticScholarSearcher
from scripts.search.google_scholar import GoogleScholarSearcher
from scripts.search.cnki import CnkiSearcher
from scripts.search.arxiv import ArxivSearcher
from scripts.search.manager import SearchManager

__all__ = [
    "BaseSearcher",
    "Paper",
    "SemanticScholarSearcher",
    "GoogleScholarSearcher",
    "CnkiSearcher",
    "ArxivSearcher",
    "SearchManager",
]