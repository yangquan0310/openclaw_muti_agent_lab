"""
scripts/search - 多源文献检索模块
===============================

统一导出所有检索器，支持多态调用：

    from scripts.search import (
        BaseSearcher, Paper,
        CnkiSearcher, SemSchSearcher, ScholarSearcher,
        search_all, create_searcher, load_queries, save_results,
    )

多态用法（无需 if-else 判断子类）：

    # 多源并行检索
    results = search_all(
        [CnkiSearcher(kb_path="kb.json"), SemSchSearcher(kb_path="kb.json")],
        keyword="深度学习",
        limit=10,
        year_min=2020,
    )
    for source, papers in results.items():
        print(f"{source}: {len(papers)} 条")

    # 工厂创建
    searcher = create_searcher("cn")   # → CnkiSearcher
    searcher = create_searcher("en")   # → SemSchSearcher
    searcher = create_searcher("gs")  # → ScholarSearcher (自动降级到 SemSch)

    # 单检索器搜索 + KB 合并
    searcher = SemSchSearcher(kb_path="kb.json")
    kb = searcher.search("deep learning", limit=20, year_min=2020)

备选引擎说明：
    ScholarSearcher 优先使用 Google Scholar；
    Google Scholar 被封时自动降级到 Semantic Scholar API。
    CnkiSearcher 需要通过 browser.snapshot() 传入页面 accessibility tree。
"""

from .BaseSearcher import BaseSearcher, Paper
from .CnkiSearcher import CnkiSearcher
from .SemSchSearcher import SemSchSearcher
from .ScholarSearcher import ScholarSearcher
from .utils import (
    search_all,
    search_by_keyword,
    create_searcher,
    load_queries,
    save_results,
)

__all__ = [
    # ABC 基类
    "BaseSearcher",
    "Paper",
    # 子类（各自实现 _do_search）
    "CnkiSearcher",
    "SemSchSearcher",
    "ScholarSearcher",
    # 多态工具函数
    "search_all",
    "search_by_keyword",
    "create_searcher",
    "load_queries",
    "save_results",
]
