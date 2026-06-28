"""cnki.py - CNKI 检索器（依赖 browser snapshot 注入）"""

from __future__ import annotations

import re
import urllib.parse
from typing import List

from scripts.search.base import BaseSearcher, Paper


class CnkiSearcher(BaseSearcher):
    """CNKI 检索器（中文）

    注意：CNKI 不提供公开 API，需要通过 browser.snapshot 注入 HTML 文本解析。
    - search(**kwargs) 返回 []（需 agent 注入 snapshot）
    - parse_snapshot(keyword, snapshot_text) 解析 HTML 文本
    """

    name = "cnki"

    SEARCH_URL_TPL = (
        "https://search.cnki.com.cn/Search/Result"
        "?SearchWord={keyword}&Match={match}&Order={order}&Page={page}"
    )

    def __init__(self, cfg: dict):
        super().__init__(cfg)
        cnki_cfg = cfg.get("cnki", {})
        self.request_interval = cnki_cfg.get("request_interval", 3.0)

    def search(self, **kwargs) -> List[Paper]:
        """CNKI 检索需要 agent 调 browser.snapshot 后注入 HTML

        用法：
            searcher = CnkiSearcher(cfg)
            papers = searcher.parse_snapshot(keyword, html_text)
        """
        keyword = kwargs.pop("keyword", "") if "keyword" in kwargs else ""
        if not keyword:
            return []
        # 返回空，提示 agent 注入 snapshot
        url = self._build_url(keyword, **kwargs)
        print(f"[cnki] 请在浏览器中打开: {url}")
        print(f"[cnki] 打开后调 parse_snapshot(keyword, html_text) 解析")
        return []

    def _build_url(self, keyword: str, **kwargs) -> str:
        match = kwargs.get("match", "Contains")
        order = kwargs.get("order", 0)
        page = kwargs.get("page", 1)
        return self.SEARCH_URL_TPL.format(
            keyword=urllib.parse.quote(keyword),
            match=match, order=order, page=page,
        )


    def parse_snapshot(self, keyword: str, snapshot_text: str) -> List[Paper]:
        """解析 CNKI 搜索结果页 HTML 文本

        Args:
            keyword: 检索关键词（用于构造 paper_id / 标识）
            snapshot_text: browser.snapshot() 返的 HTML 文本

        Returns:
            Paper 列表
        """
        papers = []
        # CNKI 搜索结果条目（典型 class）
        # 这里只做最小可用解析（agent 可按需扩展）
        for m in re.finditer(
            r'<div class="list-item"[^>]*>(.*?)</div>\s*</div>',
            snapshot_text,
            re.DOTALL,
        ):
            block = m.group(1)
            title_m = re.search(r'<a[^>]*>(.*?)</a>', block, re.DOTALL)
            author_m = re.search(r'作者[：:]\s*<[^>]*>(.*?)</a>', block, re.DOTALL)
            venue_m = re.search(r'来源[：:]\s*([^<\n]+)', block)
            year_m = re.search(r'(\d{4})', block)
            if title_m:
                papers.append(Paper(
                    title=re.sub(r'<[^>]+>', '', title_m.group(1)).strip(),
                    authors=(
                        [a.strip() for a in re.split(r'[,，;；\s]+', author_m.group(1)) if a.strip()]
                        if author_m else []
                    ),
                    year=int(year_m.group(1)) if year_m else None,
                    venue=venue_m.group(1).strip() if venue_m else "",
                    source=self.name,
                    paper_id=f"cnki_{len(papers)}",
                ))
        return papers