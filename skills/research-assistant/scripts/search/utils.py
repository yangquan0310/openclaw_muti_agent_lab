#!/usr/bin/env python3
"""
utils.py - 检索模块多态工具函数

核心功能：
  - search_all()    → 多态函数，用任意子类实例执行检索
  - create_searcher() → 根据语言创建对应检索器
  - load_queries()  → 从 JSON 文件加载检索条件
"""

from __future__ import annotations

import os
import json
import time as time_module
from typing import List, Dict, Optional, Union
from pathlib import Path

from .BaseSearcher import BaseSearcher, Paper
from .CnkiSearcher import CnkiSearcher
from .SemSchSearcher import SemSchSearcher
from .ScholarSearcher import ScholarSearcher


# ─── 多态检索函数 ───────────────────────────────────

def search_all(
    searchers: List[BaseSearcher],
    keyword: str,
    topic: str = "",
    limit: int = 20,
    interval: float = 3.0,
    **kwargs,
) -> Dict[str, List[Paper]]:
    """
    多态检索：用**任意子类实例**对同一关键词执行检索。

    设计要点：
      - 传入 BaseSearcher 列表（可以是 CnkiSearcher、SemSchSearcher
        或任何继承了 BaseSearcher 的子类）
      - 每个 searcher 独立执行检索，结果不相互覆盖
      - 返回 Dict[source_name, List[Paper]]，方便分类处理

    Args:
        searchers:   BaseSearcher 子类实例列表（如 [CnkiSearcher(), SemSchSearcher()]）
        keyword:     检索关键词
        topic:      主题标签（写入每篇 paper.topic）
        limit:       每个检索器返回的最大结果数
        interval:   两次检索之间的间隔（秒），防止频率限制
        **kwargs:    传给各 searcher._do_search 的额外参数

    Returns:
        {
            "CNKI": [Paper, ...],
            "Semantic Scholar": [Paper, ...],
        }

    Raises:
        TypeError: 如果 searchers 中包含非 BaseSearcher 实例

    Example:
        >>> cnki = CnkiSearcher(kb_path="my_kb.json")
        >>> sem = SemSchSearcher(kb_path="my_kb.json")
        >>> results = search_all(
        ...     [cnki, sem],
        ...     keyword="deep learning",
        ...     topic="深度学习",
        ...     limit=30,
        ... )
        >>> print(f"CNKI: {len(results['CNKI'])} 篇")
        >>> print(f"SS: {len(results['Semantic Scholar'])} 篇")
    """
    # 类型校验
    for s in searchers:
        if not isinstance(s, BaseSearcher):
            raise TypeError(
                f"searchers 中包含非 BaseSearcher 实例: {type(s).__name__}。"
                "请传入 BaseSearcher 的子类实例。"
            )

    combined: Dict[str, List[Paper]] = {}

    for i, searcher in enumerate(searchers):
        src = searcher.source_name
        print(f"\n[{src}] 检索 '{keyword}' ...")

        try:
            # 调用子类的 _do_search（多态）
            papers = searcher._do_search(keyword, limit=limit, **kwargs)
            for p in papers:
                if topic and topic not in p.topic:
                    p.topic.append(topic)

            combined[src] = papers
            print(f"[{src}] → {len(papers)} 篇")

        except Exception as e:
            print(f"[{src}] ❌ 检索失败: {e}")
            combined[src] = []

        # 检索间隔（最后一轮不等待）
        if i < len(searchers) - 1 and interval > 0:
            time_module.sleep(interval)

    return combined


def search_unified(
    searcher: BaseSearcher,
    queries: Dict[str, List[Dict]],
    topic: str = "",
    limit: int = 20,
    interval: float = 3.0,
) -> Dict[str, List[Paper]]:
    """
    统一多态检索：对同一 searcher 实例执行多条件检索。

    与 search_all 的区别：
      - search_all    → 多检索器 + 单关键词
      - search_unified → 单检索器 + 多条件（每个条件独立轮次）

    Args:
        searcher:  BaseSearcher 实例
        queries:  {主题: [条件字典列表]}
                  每条条件字典由子类自行解释
        topic:    外层主题标签
        limit:    每轮最大结果数
        interval: 每轮间隔（秒）

    Returns:
        {source_name: List[Paper]}
    """
    src = searcher.source_name
    results: Dict[str, List[Paper]] = {src: []}

    for main_topic, conditions in queries.items():
        for cond in conditions:
            q = cond.get("query", "")
            if not q:
                continue

            print(f"\n[{src}] 主题: {main_topic} | 检索: '{q}'")

            try:
                papers = searcher._do_search(q, limit=limit, **cond)
                label = main_topic if not topic else topic
                for p in papers:
                    if label and label not in p.topic:
                        p.topic.append(label)

                results[src].extend(papers)
                print(f"[{src}] → {len(papers)} 篇")

            except Exception as e:
                print(f"[{src}] ❌ 失败: {e}")

            time_module.sleep(interval)

    return results


# ─── 工厂函数 ───────────────────────────────────────

_LANG_MAP = {
    # 中文
    "cn": CnkiSearcher,
    "chi": CnkiSearcher,
    "chinese": CnkiSearcher,
    "zh": CnkiSearcher,
    # 英文（Semantic Scholar）
    "en": SemSchSearcher,
    "eng": SemSchSearcher,
    "english": SemSchSearcher,
    "semantic": SemSchSearcher,
    "ss": SemSchSearcher,
    # 英文（Google Scholar）
    "gs": ScholarSearcher,
    "scholar": ScholarSearcher,
    "google": ScholarSearcher,
    "google_scholar": ScholarSearcher,
}


def create_searcher(
    lang: str,
    kb_path: str = "knowledge/index.json",
    **kwargs,
) -> BaseSearcher:
    """
    工厂函数：根据语言标识字符串创建对应的检索器实例。

    Args:
        lang:   语言标识（不区分大小写）
                  - "cn" / "chi" / "chinese" / "zh" → CnkiSearcher
                  - "en" / "eng" / "english"         → SemSchSearcher
                  - "ss" / "semantic"                → SemSchSearcher
        kb_path: 知识库文件路径
        **kwargs: 传给检索器构造函数的额外参数

    Returns:
        BaseSearcher 子类实例

    Raises:
        ValueError: 不支持的 lang 参数

    Example:
        >>> searcher = create_searcher("cn", kb_path="my_kb.json")
        >>> searcher = create_searcher("en", api_key="xxx")
    """
    lang_lower = lang.lower().strip()
    cls = _LANG_MAP.get(lang_lower)

    if cls is None:
        supported = ", ".join(sorted(_LANG_MAP.keys()))
        raise ValueError(
            f"不支持的语言 '{lang}'，可选值: {supported}"
        )

    return cls(kb_path=kb_path, **kwargs)


# ─── 查询文件加载 ───────────────────────────────────

def load_queries(
    path: str,
    default_topic: str = "",
) -> Dict[str, List[Dict]]:
    """
    加载检索条件 JSON 文件。

    JSON 格式：
        {
            "自传体记忆": [
                {"query": "autobiographical memory", "limit": 30, "year": "2020-2025"},
                {"query": "\"self-memory system\"", "limit": 20}
            ],
            "深度学习": [
                {"query": "深度学习", "limit": 30, "source": "cn"}
            ]
        }

    Args:
        path:           JSON 文件路径
        default_topic:  没有主题时的默认 topic 名称

    Returns:
        Dict[str, List[Dict]]
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"检索条件文件不存在: {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if default_topic and isinstance(data, list):
        # 简单格式：纯列表（每项是条件 dict，需要指定 topic）
        return {default_topic: data}

    return dict(data)


def save_results(
    results: Dict[str, List[Paper]],
    kb_path: str,
    mode: str = "merge",
) -> Dict:
    """
    将多态检索结果保存到知识库。

    Args:
        results: search_all() 返回的 {source_name: [Paper]}
        kb_path: 知识库文件路径
        mode:    "merge"=合并到现有知识库  "replace"=覆盖现有知识库

    Returns:
        知识库完整 dict
    """
    all_papers: List[Dict] = []
    for src, papers in results.items():
        for p in papers:
            d = p.to_dict()
            d["source"] = src
            all_papers.append(d)

    if not all_papers:
        print("没有结果可保存")
        return {}

    if mode == "replace":
        # 直接覆盖：只保留新检索结果
        kb_data = {
            "version": "1.0.0",
            "project": "",
            "papers": all_papers,
        }
        # 写入
        os.makedirs(os.path.dirname(os.path.abspath(kb_path)) or ".", exist_ok=True)
        with open(kb_path, "w", encoding="utf-8") as f:
            json.dump(kb_data, f, ensure_ascii=False, indent=2)
        print(f"已覆盖写入 {kb_path}，共 {len(all_papers)} 篇")
        return kb_data

    # mode == "merge"：合并到现有知识库
    searcher = CnkiSearcher(kb_path=kb_path)
    return searcher.merge_to_kb(all_papers, kb_path=kb_path)


# ─── 语言自动路由检索 ─────────────────────────────────

def _is_chinese(text: str) -> bool:
    """
    简单判断文本是否包含中文。
    只要有 1 个中文字符就视为中文关键词。
    """
    return bool(_CHINESE_RE.search(text))


_CHINESE_RE = __import__("re").compile(r"[\u4e00-\u9fff]")


def search_by_keyword(
    keyword: str,
    kb_path: str = "knowledge/index.json",
    limit: int = 20,
    year_min: Optional[int] = None,
    year_max: Optional[int] = None,
    include_fallback: bool = True,
) -> Dict[str, List[Paper]]:
    """
    根据关键词语言自动路由到对应检索器。

    路由规则：
      - 关键词含中文  → CnkiSearcher（主）+ SemSchSearcher（备）
      - 关键词纯英文  → SemSchSearcher（主）+ ScholarSearcher（备）

    Args:
        keyword:        检索关键词
        kb_path:       知识库文件路径
        limit:         最大结果数
        year_min/year_max: 发表年份范围
        include_fallback: 是否同时请求备选检索器（返回合并结果）

    Returns:
        Dict[str, List[Paper]]，键为来源名，如 {"CNKI": [...], "Semantic Scholar": [...]}。

    Example:
        >>> results = search_by_keyword("深度学习", limit=10, year_min=2020)
        >>> for src, papers in results.items():
        ...     print(f"{src}: {len(papers)} 条")

        >>> results = search_by_keyword("deep learning", limit=10)
        >>> results = search_by_keyword(
        ...     "machine learning",
        ...     include_fallback=False,  # 只用主引擎
        ... )
    """
    is_chinese = _is_chinese(keyword)
    results: Dict[str, List[Paper]] = {}

    if is_chinese:
        # ── 中文关键词：主 CNKI，备 Semantic Scholar ──
        primary = CnkiSearcher(kb_path=kb_path)
        fallback = SemSchSearcher(kb_path=kb_path)
        primary_name = "CNKI"
        fallback_name = "Semantic Scholar"
        print(f"[search_by_keyword] 检测到中文关键词 → 主引擎: CNKI")
    else:
        # ── 英文关键词：主 Semantic Scholar，备 ScholarSearcher ──
        primary = SemSchSearcher(kb_path=kb_path)
        fallback = ScholarSearcher(kb_path=kb_path)
        primary_name = "Semantic Scholar"
        fallback_name = "Google Scholar"
        print(f"[search_by_keyword] 检测到英文关键词 → 主引擎: Semantic Scholar")

    # 主引擎
    try:
        papers = primary._do_search(
            keyword, limit=limit, year_min=year_min, year_max=year_max
        )
        if papers:
            primary.merge_to_kb(primary.normalize_batch(papers))
            results[primary_name] = papers
            print(f"[search_by_keyword] {primary_name} → {len(papers)} 篇")
        else:
            print(f"[search_by_keyword] {primary_name} 返回 0 篇")
    except Exception as e:
        print(f"[search_by_keyword] {primary_name} 失败: {e}")
        papers = []

    # 备选引擎
    if include_fallback and (not papers or len(papers) < limit):
        remaining = limit - len(results.get(primary_name, []))
        try:
            fb_papers = fallback._do_search(
                keyword,
                limit=remaining,
                year_min=year_min,
                year_max=year_max,
            )
            if fb_papers:
                fallback.merge_to_kb(fallback.normalize_batch(fb_papers))
                results[fallback_name] = fb_papers
                print(f"[search_by_keyword] {fallback_name}（备选）→ {len(fb_papers)} 篇")
        except Exception as e:
            print(f"[search_by_keyword] {fallback_name}（备选）失败: {e}")

    return results
