#!/usr/bin/env python3
"""
ScholarSearcher.py - Google Scholar + Semantic Scholar 英文文献检索

继承 BaseSearcher，优先请求 Google Scholar（requests 静态 HTML 解析），
被封禁时自动降级到 Semantic Scholar API，并给出明确提示。

Google Scholar 反爬要点：
  - 正常情况返回静态 HTML，requests 可直接解析
  - 频繁访问触发 CAPTCHA/IP 封禁：返回 200 但 0 结果
  - 被封后自动切换到 Semantic Scholar API 作为备选
"""

from __future__ import annotations

import os
import re
import time
import requests
from typing import List, Optional

from .BaseSearcher import BaseSearcher, Paper


class ScholarSearcher(BaseSearcher):
    """
    Google Scholar 检索器（自动降级到 Semantic Scholar API）

    策略：
      1. 优先 Google Scholar（解析静态 HTML，获取完整 meta 信息）
      2. Google Scholar 被封 → 自动切换 Semantic Scholar API
      3. Semantic Scholar API 也失败 → 抛出明确错误
    """

    source_name = "Google Scholar"
    GS_URL = "https://scholar.google.com/scholar"
    SS_API = "https://api.semanticscholar.org/graph/v1/paper/search"
    SS_BATCH = "https://api.semanticscholar.org/graph/v1/paper/batch"
    SS_FIELDS = (
        "paperId,title,authors,year,venue,abstract,"
        "citationCount,externalIds,url"
    )

    def __init__(
        self,
        kb_path: str = "wiki/sources/cache.json",
        api_key: Optional[str] = None,
        request_interval: float = 3.0,
        hl: str = "zh-CN",
    ):
        super().__init__(kb_path)
        self.request_interval = request_interval
        self.hl = hl
        self._fallback_used = False  # 记录是否使用了备选引擎
        # v5.12.0: SemSch api_key 优先级 key > config > env（注入到 _search_semantic）
        # config 读取（inline；保持与 Searcher.py / SemSchSearcher.py 一致）
        _ss_config: dict = {}
        try:
            import json as _json
            from pathlib import Path as _Path
            _cfg_path = _Path(__file__).parent.parent / "config.json"
            if _cfg_path.exists():
                with open(_cfg_path, "r", encoding="utf-8") as _f:
                    _ss_config = _json.load(_f)
        except Exception:
            pass
        _semantic = _ss_config.get("semantic_scholar", {})
        self._ss_api_key = (
            api_key
            or _semantic.get("api_key", "")
            or os.environ.get(_semantic.get("api_key_env", "SEMANTIC_SCHOLAR_API_KEY"))
        )
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept-Language": f"{hl},en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,"
                      "application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://scholar.google.com/",
        })

    # ── 抽象方法实现 ─────────────────────────────────

    def _do_search(
        self,
        keyword: str,
        limit: int = 20,
        year_min: Optional[int] = None,
        year_max: Optional[int] = None,
        **kwargs,
    ) -> List[Paper]:
        # 先尝试 Google Scholar
        papers, blocked = self._search_google(keyword, limit, year_min, year_max)

        if blocked or not papers:
            # 降级到 Semantic Scholar API
            print(
                "[ScholarSearcher] ⚠️ Google Scholar 不可用，"
                "自动切换到 Semantic Scholar API"
            )
            papers = self._search_semantic(keyword, limit, year_min, year_max)
            self._fallback_used = True

        return papers

    # ── Google Scholar 搜索 ──────────────────────────

    def _search_google(
        self,
        keyword: str,
        limit: int,
        year_min: Optional[int],
        year_max: Optional[int],
    ) -> tuple[List[Paper], bool]:
        """
        返回 (papers, blocked)。
        blocked = True 表示 Google Scholar 触发封禁。
        """
        all_papers: List[Paper] = []
        page = 0

        while len(all_papers) < limit:
            params = {
                "q": keyword,
                "hl": self.hl,
                "start": page * 10,
            }
            if year_min:
                params["as_ylo"] = str(year_min)
            if year_max:
                params["as_yhi"] = str(year_max)

            try:
                resp = self.session.get(
                    self.GS_URL, params=params, timeout=15
                )
                resp.raise_for_status()
            except Exception as e:
                print(f"[ScholarSearcher] Google Scholar 请求失败: {e}")
                return [], True

            papers, blocked = self._parse_html(resp.text)
            if blocked:
                return [], True
            if not papers:
                return all_papers, False

            all_papers.extend(papers)
            page += 1
            if len(papers) < 10:
                break
            if len(all_papers) < limit:
                time.sleep(self.request_interval)

        return all_papers[:limit], False

    # ── Semantic Scholar 备选 ────────────────────────

    def _search_semantic(
        self,
        keyword: str,
        limit: int,
        year_min: Optional[int],
        year_max: Optional[int],
    ) -> List[Paper]:
        """通过 Semantic Scholar API 获取论文（备选引擎）"""
        # v5.12.0: 使用 __init__ 解析的 _ss_api_key（key > config > env）
        api_key = self._ss_api_key or ""
        headers = {"x-api-key": api_key} if api_key else {}
        params = {
            "query": keyword,
            "limit": min(limit, 100),
            "fields": self.SS_FIELDS,
        }
        if year_min:
            params["year"] = f"{year_min}-{year_max or 2026}"
        elif year_max:
            params["year"] = f"1900-{year_max}"

        for attempt in range(3):
            try:
                resp = requests.get(
                    self.SS_API, params=params, headers=headers, timeout=20
                )
                resp.raise_for_status()
                data = resp.json()
                break
            except Exception as e:
                wait = 2 ** attempt
                print(
                    f"[ScholarSearcher] Semantic Scholar API "
                    f"请求失败(尝试 {attempt+1}/3): {e}, "
                    f"{wait}s 后重试..."
                )
                if attempt < 2:
                    time.sleep(wait)
                else:
                    print(f"[ScholarSearcher] Semantic Scholar API 全部重试失败")
                    return []

        papers = []
        for item in data.get("data", []):
            p = Paper()
            p.source = "Semantic Scholar"
            p.paper_id = item.get("paperId", "")
            p.title = item.get("title", "")
            p.year = item.get("year")
            p.venue = item.get("venue", "")
            p.abstract = item.get("abstract", "")
            p.citation_count = item.get("citationCount", 0)
            p.url = item.get("url", "") or (
                f"https://www.semanticscholar.org/paper/{p.paper_id}"
            )

            authors = item.get("authors", [])
            if isinstance(authors, list):
                p.authors = [
                    a.get("name", "") for a in authors if a.get("name")
                ]

            external = item.get("externalIds", {})
            if external.get("DOI"):
                p.doi = external["DOI"]

            if p.title:
                papers.append(p)

        return papers

    # ── HTML 解析 ──────────────────────────────────

    def _parse_html(self, html: str) -> tuple[List[Paper], bool]:
        """
        解析 Google Scholar HTML。
        返回 (papers, blocked)。
        """
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, "html.parser")

        # CAPTCHA 检测
        title = soup.find("title")
        if title and "CAPTCHA" in title.get_text():
            return [], True

        items = soup.select("div.gs_ri")
        if not items:
            # 有搜索框但无结果 = 封禁
            if soup.find("input", {"name": "q"}):
                return [], True
            return [], False

        papers = []
        for item in items:
            p = Paper()
            p.source = "Google Scholar"

            # 标题 + URL
            title_el = item.select_one("h3.gs_rt a")
            if title_el:
                p.title = title_el.get_text(separator=" ", strip=True)
                p.url = title_el.get("href", "")
                m = re.search(r"d=(\d+)", title_el.get("data-clk", ""))
                if m:
                    p.paper_id = f"gs_{m.group(1)}"

            # 作者 + 年份 + 出版物
            meta_el = item.select_one("div.gs_a")
            if meta_el:
                meta_text = meta_el.get_text(separator=" ", strip=True)
                last_dash = meta_text.rfind(" -")
                if last_dash > 0:
                    author_els = meta_el.select("a")
                    if author_els:
                        p.authors = [a.get_text(strip=True) for a in author_els]

                    venue_part = meta_text[last_dash + 2:]
                    year_m = re.search(r"\b(19|20)\d{2}\b", venue_part)
                    if year_m:
                        p.year = int(year_m.group(0))

                    venue_clean = re.sub(
                        r"\b(19|20)\d{2}\b", "", venue_part
                    ).strip(" ,-")
                    if venue_clean:
                        p.venue = venue_clean

            # 摘要
            abs_el = item.select_one("div.gs_rs")
            if abs_el:
                p.abstract = re.sub(
                    r"^[…. \s]+", "",
                    abs_el.get_text(strip=True)
                )

            # 被引用次数
            cited_el = item.select_one('a[href*="/scholar?cites="]')
            if cited_el:
                m = re.search(r"\d+", cited_el.get_text(strip=True))
                if m:
                    p.citation_count = int(m.group(0))

            if p.title:
                papers.append(p)

        return papers, False
