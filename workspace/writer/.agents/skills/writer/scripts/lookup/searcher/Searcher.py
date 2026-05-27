#!/usr/bin/env python3
"""
References 搜索引擎核心类
基于关键词匹配 + 语义相似度排序
"""

import json
import re
from pathlib import Path
from typing import Any


class ReferencesSearcher:
    def __init__(self, skill_dir: Path):
        self.skill_dir = skill_dir
        self.index_dir = skill_dir / "scripts" / "lookup" / "index"
        self._load_index()

    def _load_index(self):
        """加载索引"""
        manifest_path = self.index_dir / "manifest.json"
        chunks_path = self.index_dir / "chunks.json"

        if not manifest_path.exists():
            raise FileNotFoundError(f"Index not found. Run: python3 -m scripts.lookup.indexer")

        with open(manifest_path, 'r', encoding='utf-8') as f:
            self.manifest = json.load(f)

        if chunks_path.exists():
            with open(chunks_path, 'r', encoding='utf-8') as f:
                self.chunks = json.load(f)
        else:
            self.chunks = []

    # 停用词（查询时过滤）
    STOPWORDS = {'是', '的', '了', '在', '和', '与', '或', '不', '一个', '什么', '怎么', '如何', '为什么', '哪些', '哪个', '有', '没有', '这', '那', '我', '你', '他', '她', '它', '们'}

    def _tokenize(self, text: str, filter_stopwords: bool = False) -> set[str]:
        """分词"""
        # 转小写，提取中英文词
        text = text.lower()
        # 英文词
        words = re.findall(r'[a-z]+', text)
        # 中文单字
        chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
        # 中文2-gram（提高匹配精度）
        chinese_2gram = [text[i:i+2] for i in range(len(text)-1)
                         if re.match(r'[\u4e00-\u9fff]{2}', text[i:i+2])]
        tokens = set(words + chinese_chars + chinese_2gram)

        # 过滤停用词
        if filter_stopwords:
            tokens = tokens - self.STOPWORDS

        return tokens

    def _calculate_score(self, query_tokens: set[str], text: str, keywords: list[str] = None) -> float:
        """计算匹配分数"""
        text_tokens = self._tokenize(text)

        # 交集
        common = query_tokens & text_tokens

        if not common:
            return 0.0

        # 基础分数：交集/查询词数
        score = len(common) / len(query_tokens)

        # 关键词加权
        if keywords:
            keyword_tokens = self._tokenize(' '.join(keywords))
            keyword_match = common & keyword_tokens
            if keyword_match:
                score += 0.5 * len(keyword_match) / len(keyword_tokens)

        return min(score, 1.0)

    def search_files(self, query: str) -> list[tuple[str, float]]:
        """搜索文件级别匹配"""
        query_tokens = self._tokenize(query, filter_stopwords=True)  # 过滤停用词
        results = []

        for filename, data in self.manifest.items():
            # 检查标题匹配
            title_score = self._calculate_score(query_tokens, data['title'], data.get('keywords', []))

            # 检查描述匹配
            desc_score = self._calculate_score(query_tokens, data['description'])

            # 检查关键词匹配
            kw_score = 0.0
            if 'keywords' in data:
                kw_score = self._calculate_score(query_tokens, ' '.join(data['keywords']))

            # 检查章节标题匹配
            section_score = 0.0
            for section in data.get('sections', []):
                section_score = max(section_score, self._calculate_score(query_tokens, section['heading']))

            # 综合分数
            total_score = max(title_score, desc_score, kw_score, section_score)

            if total_score > 0:
                results.append((filename, total_score))

        # 排序
        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def search_chunks(self, query: str, file_filter: str = None) -> list[dict[str, Any]]:
        """搜索章节块级别匹配"""
        query_tokens = self._tokenize(query)
        results = []

        for chunk in self.chunks:
            # 文件过滤
            if file_filter and chunk['file'].startswith(file_filter):
                continue

            # 计算分数
            heading_score = self._calculate_score(query_tokens, chunk['heading'])
            content_score = self._calculate_score(query_tokens, chunk.get('content_preview', ''))

            total_score = max(heading_score, content_score * 0.7)  # 标题权重更高

            if total_score > 0:
                results.append({
                    **chunk,
                    'score': total_score
                })

        # 排序
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:10]  # 返回前10个

    def search(self, query: str, show_chunks: bool = True) -> dict[str, Any]:
        """综合搜索"""
        # 文件级别搜索
        file_results = self.search_files(query)

        if not file_results:
            return {"files": [], "chunks": [], "query": query}

        # 获取前3个匹配文件
        top_files = file_results[:3]

        # 章节块搜索（限制前2个文件）
        chunks_results = []
        if show_chunks:
            for filename, _ in top_files[:2]:
                file_chunks = self.search_chunks(query, file_filter=filename)
                chunks_results.extend(file_chunks[:3])

        # 去重并排序
        seen = set()
        unique_chunks = []
        for chunk in chunks_results:
            if chunk['id'] not in seen:
                seen.add(chunk['id'])
                unique_chunks.append(chunk)
        unique_chunks.sort(key=lambda x: x['score'], reverse=True)

        return {
            "query": query,
            "files": [{"file": f, "score": s, **self.manifest[f]} for f, s in top_files],
            "chunks": unique_chunks[:5]
        }
