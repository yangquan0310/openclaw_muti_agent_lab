"""统一导出所有类，供 main.py 和 MCP server 导入。"""

from .search.Searcher import Searcher
from .search.CnkiSearcher import CnkiSearcher
from .search.SemSchSearcher import SemSchSearcher
from .search.ScholarSearcher import ScholarSearcher
from .search.BaseSearcher import BaseSearcher, Paper
from .summarize.Summarizer import Summarizer
from .manage.Manager import Manager
from .synthesize.Synthesizer import Synthesizer
from .maintainer.Maintainer import Maintainer

# ── 向后兼容别名 ────────────────────────────────────
CNKISearcher = CnkiSearcher        # 旧名
SemanticSearcher = SemSchSearcher   # 旧名
BrowserCNKISearcher = CnkiSearcher # 旧名

__all__ = [
    "Searcher",
    "CnkiSearcher",
    "SemSchSearcher",
    "ScholarSearcher",
    "BaseSearcher",
    "Paper",
    # 向后兼容
    "CNKISearcher",
    "SemanticSearcher",
    "BrowserCNKISearcher",
    "Summarizer",
    "Manager",
    "Synthesizer",
    "Maintainer",
]
