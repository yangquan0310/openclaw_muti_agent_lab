#!/usr/bin/env python3
"""
CnkiSearcher.py - 中国知网中文文献检索

继承 BaseSearcher，通过浏览器访问 search.cnki.com.cn 抓取渲染后的页面，
解析为标准化 Paper 数据。

无需登录，不依赖知网 API。
"""

from __future__ import annotations

import re
import os
import json
import time
from typing import List, Dict, Optional, Any

from .BaseSearcher import BaseSearcher, Paper


class CnkiSearcher(BaseSearcher):
    """中文文献检索器（CNKI / 知网空间）"""

    source_name = "CNKI"

    SEARCH_URL_TPL = (
        "https://search.cnki.com.cn/Search/Result"
        "?SearchWord={keyword}&Match={match}&Order={order}&Page={page}"
    )

    def __init__(
        self,
        kb_path: str = "knowledge/index.json",
        request_interval: float = 3.0,
    ):
        """
        Args:
            kb_path:           知识库文件路径
            request_interval:  每次页面访问之间的间隔（秒），避免触发风控
        """
        super().__init__(kb_path)
        self.request_interval = request_interval

    # ── 实现抽象方法 ─────────────────────────────────

    def _do_search(
        self,
        keyword: str,
        limit: int = 20,
        match: str = "Contains",
        order: int = 0,
        page: int = 1,
        **kwargs,
    ) -> List[Paper]:
        """
        通过浏览器抓取 CNKI 搜索结果。

        Args:
            keyword: 检索关键词
            limit:   最大结果数（CNKI 每页约 20 条）
            match:   匹配方式，Contains=模糊，Exact=精确
            order:   排序，0=相关度  1=发表时间  2=被引量
            page:    起始页码（从 1 开始）

        Returns:
            Paper 列表
        Note:
            此方法需要在 OpenClaw 浏览器中配合使用：
              1. browser.navigate(url)  → 打开搜索结果页
              2. browser.snapshot()    → 获取渲染后文本
              3. 调用 parse_snapshot(text) 解析
        """
        url = self.build_search_url(keyword, match=match, order=order, page=page)
        print(f"[CNKI] 搜索 URL: {url}")
        print(f"[CNKI] 请在浏览器中打开上述 URL，然后调用 parse_snapshot() 传入快照文本")
        return []

    # ── 快照解析 ──────────────────────────────────────

    def parse_snapshot(self, snapshot_text: str, topic: str = "") -> List[Paper]:
        """
        解析浏览器快照文本，提取 Paper 列表。

        在 _do_search 之后调用：
            url = searcher.build_search_url("深度学习")
            browser.navigate(url)
            snapshot_text = browser.snapshot(...)
            papers = searcher.parse_snapshot(snapshot_text, topic="深度学习")
            searcher.merge_to_kb([p.to_dict() for p in papers])
        """
        results = self._parse_tree(snapshot_text)
        for p in results:
            if topic and topic not in p.topic:
                p.topic.append(topic)
        return results

    # ── URL 构造 ─────────────────────────────────────

    def build_search_url(
        self,
        keyword: str,
        match: str = "Contains",
        order: int = 0,
        page: int = 1,
    ) -> str:
        """构造知网空间搜索 URL"""
        from urllib.parse import quote
        kw = quote(keyword.encode("utf-8"))
        return self.SEARCH_URL_TPL.format(
            keyword=kw, match=match, order=order, page=page
        )

    # ── 快照解析核心 ─────────────────────────────────

    def _parse_tree(self, text: str) -> List[Paper]:
        """
        解析 accessibility tree 格式快照（search.cnki.com.cn）。

        已知快照格式（每条结果的结构）：
          - link "标题  CNKI文献" [ref=xx]     ← depth=2，标题行
            - statictext "标题  CNKI文献"      ← depth=4，子节点副本
          - statictext "一、摘要..."             ← depth=2，摘要行
          - link "作者名" [ref=xx]              ← depth=2，作者
          - link "《期刊名》" [ref=xx]           ← depth=2，期刊
          - link "202X年XX期" [ref=xx]          ← depth=2，年份
          - statictext "关键词："                 ← depth=2，关键词标签
          - statictext "关键词1" / statictext "/" ← depth=2，关键词词条
          - statictext "下载（123）"              ← depth=2
          - statictext "被引（4）"               ← depth=2

        处理策略：**同级连续块**。
        - 找到标题行（depth=2，含 "CNKI文献"）后，收集该结果所有同级（depth>=2）行，
          直到遇到下一个同级标题行。
        - 通过内容特征识别各字段。
        """
        papers: List[Paper] = []
        lines = text.split("\n")

        def get_depth(raw: str) -> int:
            return len(raw) - len(raw.lstrip(" "))

        def extract_text(raw: str) -> str:
            """从 accessibility tree 行提取纯文本"""
            line = raw.strip()
            # 匹配: '  - link "文本" [ref=11_29]' → "文本"
            m = re.match(r"^[^\"']*\"(.+?)\"(?:\s+\[ref=[^\]]+\])?\s*$", line)
            if m:
                return m.group(1).strip()
            # 回退：去掉已知前缀
            s = re.sub(
                r"^\s*-?\s*(?:link|statictext|heading|textbox)\s+",
                "", line,
            )
            s = re.sub(r"\s*\[ref=[^\]]+\]\s*$", "", s)
            return s.strip('" \'-').strip()

        # ── 第一步：定位所有标题行（depth=2）────────────
        title_indices: List[tuple] = []  # (line_index, title_text, depth)
        for i, raw in enumerate(lines):
            if "CNKI文献" not in raw:
                continue
            txt = extract_text(raw)
            d = get_depth(raw)
            # 只取 depth=2 的 link 行（去掉 statictext 重复）
            if d == 2 and len(txt) >= 5:
                title_indices.append((i, txt, d))

        if not title_indices:
            return []

        # ── 第二步：每个标题块 → 收集字段 ───────────
        for ti, (title_idx, title_txt, td) in enumerate(title_indices):
            next_title_idx = (
                title_indices[ti + 1][0]
                if ti + 1 < len(title_indices)
                else len(lines)
            )

            paper = Paper()
            paper.title = re.sub(r"\s+CNKI文献\s*$", "", title_txt).strip()
            paper.source = "CNKI"

            # 关键词缓冲区
            kw_buffer: List[str] = []
            in_kw_zone = False

            # 已知非作者词（用于排除）
            NON_AUTHOR = {
                "下载", "被引", "期刊", "关键词", "关键词：",
                "CNKI", "研究", "涉及", "分析", "方法", "技术", "系统",
            }

            for j in range(title_idx + 1, next_title_idx):
                raw = lines[j]
                d = get_depth(raw)
                if d < td:  # 跳过浅于标题的行
                    continue

                txt = extract_text(raw)
                if not txt:
                    continue

                # ── ① 关键词区域开始 ────────────────
                if txt in ("关键词：", "关键词"):
                    in_kw_zone = True
                    kw_buffer = []
                    continue

                # ── ② 下载数 ───────────────────────
                dl_m = re.search(r"下载[（(](\d+)[)）]", txt)
                if dl_m:
                    # 注意：下载数存在 Paper.keywords 的特殊字段
                    continue

                # ── ③ 被引数 ───────────────────────
                cite_m = re.search(r"被引[（(](\d+)[)）]", txt)
                if cite_m:
                    paper.citation_count = int(cite_m.group(1))
                    continue

                # ── ④ 年份（在期刊之前检测）──────────
                if paper.year is None:
                    ym = re.search(r"(\d{4})年", txt)
                    if ym:
                        paper.year = int(ym.group(1))

                # ── ⑤ 期刊（在年份之后才匹配）────────
                # 标题含《》时会误匹配 → 限定 r.year is None（journal 在 year 之前）
                # 摘要中的《》→ 限定行长度 ≤30
                if (paper.venue == ""
                    and paper.year is None
                    and not in_kw_zone
                    and "CNKI文献" not in txt):
                    vm = re.search(r"《([^》]+)》", txt)
                    if vm and len(vm.group(1)) <= 25 and len(txt) <= 30:
                        paper.venue = vm.group(1)

                # ── ⑥ 作者（2-5个汉字，排除词）──────
                if not paper.authors:
                    if (re.match(r"^[\u4e00-\u9fa5]{2,5}$", txt)
                       and txt not in NON_AUTHOR):
                        paper.authors = [txt]

                # ── ⑦ 关键词区域 ───────────────────
                if in_kw_zone and not paper.keywords:
                    # "/" 分隔的多词行
                    if "/" in txt:
                        parts = [p.strip() for p in txt.split("/")]
                        kw_buffer.extend([p for p in parts if p and 2 <= len(p) <= 15])
                    # 独立词条（纯中文/英文/数字，2-15字）
                    elif re.match(r"^[\u4e00-\u9fa5a-zA-Z0-9]{2,15}$", txt):
                        if txt not in ("期刊", "关键词", "下载", "被引", "CNKI"):
                            kw_buffer.append(txt)
                    # 遇到非关键词行，停止收集
                    if kw_buffer and (
                        re.search(r"下载|被引|《|\d{4}年", txt)
                        or (
                            txt not in ("/", "关键词：", "关键词")
                            and not re.match(r"^[\u4e00-\u9fa5a-zA-Z0-9]{2,15}$", txt)
                            and "/" not in txt
                        )
                    ):
                        in_kw_zone = False
                        paper.keywords = kw_buffer
                        kw_buffer = []

                # ── ⑧ 摘要（长段落）────────────────
                if (not paper.abstract
                    and len(txt) > 30
                    and txt not in ("期刊", "关键词", "关键词：",
                                    "下载", "被引", "CNKI")
                    and not re.match(r"^[\u4e00-\u9fa5]{2,5}$", txt)):
                    paper.abstract = txt

            # 退出时还有剩余关键词
            if not paper.keywords and kw_buffer:
                paper.keywords = kw_buffer

            if paper.title:
                papers.append(paper)

        return papers
