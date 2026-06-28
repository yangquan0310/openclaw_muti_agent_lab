"""google_scholar.py - Google Scholar 检索器（自动降级到 SemSch）"""

from __future__ import annotations

import re
import time
from typing import List

import requests

from scripts.search.base import BaseSearcher, Paper
from scripts.search.semantic_scholar import SemanticScholarSearcher


class GoogleScholarSearcher(BaseSearcher):
    """Google Scholar 检索器

    策略：优先 Google Scholar（解析 HTML），0 结果时降级到 SemSch API。
    """

    name = "google_scholar"

    GS_URL = "https://scholar.google.com/scholar"
    HL = "zh-CN"
    USER_AGENT = (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )

    def __init__(self, cfg: dict):
        super().__init__(cfg)
        gs_cfg = cfg.get("google_scholar", {})
        self.request_interval = gs_cfg.get("request_interval", 3.0)
        self.hl = gs_cfg.get("hl", self.HL)
        # 降级到 SemSch
        self._fallback = SemanticScholarSearcher(cfg)
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": self.USER_AGENT,
            "Accept-Language": f"{self.hl},en;q=0.9",
        })

    def search(self, **kwargs) -> List[Paper]:
        keyword = kwargs.get("keyword", "")
        limit = kwargs.get("limit", 20)
        if not keyword:
            return []

        try:
            resp = self.session.get(
                self.GS_URL,
                params={"q": keyword, "hl": self.hl, "num": min(limit, 20)},
                timeout=20,
            )
            html = resp.text
        except Exception as e:
            print(f"[google_scholar] 请求失败，降级到 SemSch: {e}")
            return self._fallback.search(**kwargs)

        time.sleep(self.request_interval)
        papers = self._parse_html(html)
        if not papers:
            # 降级
            print(f"[google_scholar] 0 结果，降级到 SemSch")
            return self._fallback.search(**kwargs)
        return papers[:limit]

    def _parse_html(self, html: str) -> List[Paper]:
        """解析 Google Scholar HTML 提取论文"""
        papers = []
        # 简单正则解析（按需扩展）
        for m in re.finditer(
            r'<h3[^>]*class="gs_rt"[^>]*>(.*?)</h3>',
            html,
            re.DOTALL,
        ):
            title_block = m.group(1)
            title = re.sub(r"<[^>]+>", "", title_block).strip()
            papers.append(Paper(
                title=title,
                authors=[],
                year=None,
                venue="Google Scholar",
                doi="",
                url="",
                abstract="",
                citation_count=0,
                source=self.name,
                paper_id=f"gs_{len(papers)}",
            ))
        return papers