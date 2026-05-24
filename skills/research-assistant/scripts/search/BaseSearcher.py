#!/usr/bin/env python3
"""
BaseSearcher.py - 文献检索抽象基类

定义统一的检索接口，子类只需实现 _do_search() 方法，
公共流程（标准化、合并知识库）由基类统一处理。

子类实现：
  - CnkiSearcher    → 中文检索（search.cnki.com.cn + 浏览器）
  - SemSchSearcher → 英文检索（Semantic Scholar API）
"""

from __future__ import annotations

import os
import json
import re
from abc import ABC, abstractmethod
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any


# ─── 统一的数据模型 ──────────────────────────────────────

@dataclass
class Paper:
    """标准化文献数据结构（所有检索器通用）"""
    title: str = ""
    authors: List[str] = field(default_factory=list)
    year: Optional[int] = None
    venue: str = ""
    volume: str = ""
    issue: str = ""
    pages: str = ""
    doi: str = ""
    url: str = ""
    abstract: str = ""
    citation_count: int = 0
    source: str = ""       # "CNKI" | "Semantic Scholar"
    paper_id: str = ""      # 各平台 ID
    topic: List[str] = field(default_factory=list)   # 所属主题
    keywords: List[str] = field(default_factory=list)  # 关键词（CNKI 特有）

    def to_dict(self) -> Dict[str, Any]:
        return {
            "paperId": self.paper_id,
            "source": self.source,
            "authors": self.authors,
            "year": self.year,
            "title": self.title,
            "venue": self.venue,
            "volume": self.volume,
            "issue": self.issue,
            "pages": self.pages,
            "doi": self.doi,
            "url": self.url,
            "abstract": self.abstract,
            "citationCount": self.citation_count,
            "topic": self.topic,
            "labels": {"type": "", "importance": "", "JCR": ""},
            "_keywords": self.keywords,
        }


# ─── ABC 基类 ───────────────────────────────────────────

class BaseSearcher(ABC):
    """
    文献检索抽象基类。

    子类只需实现：
      - _do_search()    → 执行检索，返回 List[Paper]
      - source_name     → 标识来源（如 "CNKI"）

    基类提供公共流程：
      - search()       → 检索 → 标准化 → 合并知识库
      - normalize()    → Paper → index.json dict
      - merge_to_kb()  → 合并到知识库文件
    """

    source_name: str = ""

    def __init__(self, kb_path: str = "knowledge/index.json"):
        self.kb_path = kb_path

    # ── 抽象接口 ─────────────────────────────────────

    @abstractmethod
    def _do_search(
        self,
        keyword: str,
        limit: int = 20,
        **kwargs,
    ) -> List[Paper]:
        """
        子类实现具体的检索逻辑。

        Args:
            keyword: 检索关键词
            limit:   最大结果数
            **kwargs: 子类自定义参数（如 year, order, page 等）

        Returns:
            Paper 列表
        """
        ...

    # ── 公共检索流程 ────────────────────────────────

    def search(
        self,
        keyword: str,
        topic: str = "",
        limit: int = 20,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        检索 → 标准化 → 合并知识库。

        Args:
            keyword: 检索关键词
            topic:   主题名称（写入 paper.topic）
            limit:   最大结果数
            **kwargs: 传给 _do_search 的额外参数

        Returns:
            知识库完整 dict
        """
        papers = self._do_search(keyword, limit=limit, **kwargs)

        # 设置主题
        for p in papers:
            if topic and topic not in p.topic:
                p.topic.append(topic)

        # 标准化
        normalized = self.normalize_batch(papers)

        # 合并写入知识库
        kb = self.merge_to_kb(normalized)

        print(f"[{self.source_name}] 检索 '{keyword}' → {len(papers)} 篇"
              f"，已写入 {self.kb_path}（共 {kb['statistics']['total_count']} 篇）")
        return kb

    # ── 标准化 ──────────────────────────────────────

    def normalize_batch(self, papers: List[Paper]) -> List[Dict]:
        """将 Paper 列表转为 index.json 标准格式"""
        return [p.to_dict() for p in papers]

    # ── 知识库操作 ──────────────────────────────────

    def merge_to_kb(
        self,
        new_papers: List[Dict],
        kb_path: Optional[str] = None,
    ) -> Dict:
        """
        将新论文合并到知识库文件（原地更新）。

        合并逻辑：
          - 已有文献（相同 paperId）：合并 topic 列表
          - 新文献：追加到 papers 列表
          - 全局去重（基于 paperId + title）
          - 更新统计信息
        """
        kb_path = kb_path or self.kb_path
        kb_data = self._load_kb(kb_path)

        existing: List[Dict] = kb_data.get("papers", [])
        existing_ids = {p.get("paperId") for p in existing if p.get("paperId")}
        existing_titles = {p.get("title", "").lower() for p in existing}

        for paper in new_papers:
            pid = paper.get("paperId")
            title = paper.get("title", "").lower()

            if pid and pid in existing_ids:
                # 已有文献 → 合并 topic
                for ep in existing:
                    if ep.get("paperId") == pid:
                        topics = set(ep.get("topic", []))
                        for t in paper.get("topic", []):
                            topics.add(t)
                        ep["topic"] = sorted(topics)
                        break

            elif title and title in existing_titles:
                # 同标题 → 合并 topic
                for ep in existing:
                    if ep.get("title", "").lower() == title:
                        topics = set(ep.get("topic", []))
                        for t in paper.get("topic", []):
                            topics.add(t)
                        ep["topic"] = sorted(topics)
                        break

            else:
                existing.append(paper)
                if pid:
                    existing_ids.add(pid)
                if title:
                    existing_titles.add(title)

        kb_data["papers"] = self._deduplicate(existing)
        kb_data = self._update_statistics(kb_data)
        self._save_kb(kb_data, kb_path)
        return kb_data

    # ── 知识库工具方法 ──────────────────────────────

    def _load_kb(self, kb_path: str) -> Dict:
        if os.path.exists(kb_path):
            with open(kb_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return self._new_kb()

    def _new_kb(self) -> Dict:
        return {
            "version": "1.0.0",
            "project": "",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "statistics": {
                "total_count": 0,
                "total_citations": 0,
                "foundation_count": 0,
                "important_count": 0,
                "general_count": 0,
                "empirical_count": 0,
                "review_count": 0,
                "theory_count": 0,
                "cnki_count": 0,
                "semantic_count": 0,
            },
            "papers": [],
        }

    def _save_kb(self, kb_data: Dict, kb_path: str):
        os.makedirs(os.path.dirname(os.path.abspath(kb_path)) or ".", exist_ok=True)
        with open(kb_path, "w", encoding="utf-8") as f:
            json.dump(kb_data, f, ensure_ascii=False, indent=2)

    def _deduplicate(self, papers: List[Dict]) -> List[Dict]:
        seen_ids = set()
        seen_titles = set()
        unique = []
        for p in papers:
            pid = p.get("paperId", "")
            title = p.get("title", "").strip().lower()
            if pid and pid in seen_ids:
                continue
            if title and title in seen_titles:
                continue
            seen_ids.add(pid)
            seen_titles.add(title)
            unique.append(p)
        return unique

    def _update_statistics(self, kb_data: Dict) -> Dict:
        papers = kb_data.get("papers", [])
        total = len(papers)
        total_cites = sum(p.get("citationCount", 0) for p in papers)
        foundation = sum(1 for p in papers if p.get("citationCount", 0) >= 500)
        important = sum(1 for p in papers
                        if 50 <= p.get("citationCount", 0) < 500)
        general = max(0, total - foundation - important)
        cnki_count = sum(1 for p in papers if p.get("source") == "CNKI")
        sem_count = sum(1 for p in papers
                        if p.get("source") in ("Semantic Scholar", "semantic-scholar"))
        kb_data["statistics"].update({
            "total_count": total,
            "total_citations": total_cites,
            "foundation_count": foundation,
            "important_count": important,
            "general_count": general,
            "cnki_count": cnki_count,
            "semantic_count": sem_count,
        })
        kb_data["updated_at"] = datetime.now().isoformat()
        if not kb_data.get("created_at"):
            kb_data["created_at"] = datetime.now().isoformat()
        return kb_data
