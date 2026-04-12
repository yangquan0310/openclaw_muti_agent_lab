#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文献处理工具 - 面向对象版本

功能：
1. 文献去重（基于DOI和标题相似度）
2. 文献分类（基于关键词匹配）
3. 文献筛选（按引用量、年份等）
4. 文献合并（多个来源合并）

使用示例：
    processor = LiteratureProcessor()
    
    # 去重
    unique_papers = processor.deduplicate(papers_list)
    
    # 分类
    classified = processor.classify_by_topic(papers, topic_keywords)
    
    # 筛选
    filtered = processor.filter_by_citation(papers, min_citations=50)
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict
import difflib


@dataclass
class Paper:
    """文献数据类"""
    id: str = ""
    title: str = ""
    authors: List[str] = field(default_factory=list)
    year: int = 0
    venue: str = ""
    volume: str = ""
    issue: str = ""
    pages: str = ""
    doi: str = ""
    url: str = ""
    citation_count: int = 0
    abstract: str = ""
    topic: str = ""
    labels: Dict[str, str] = field(default_factory=dict)
    source: str = ""  # 来源标识
    
    @property
    def doc_type(self) -> str:
        """获取文献类型"""
        return self.labels.get('type', '📋待分类')
    
    @property
    def importance(self) -> str:
        """获取重要性等级"""
        return self.labels.get('importance', '🔵一般')
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'id': self.id,
            'title': self.title,
            'authors': self.authors,
            'year': self.year,
            'venue': self.venue,
            'volume': self.volume,
            'issue': self.issue,
            'pages': self.pages,
            'doi': self.doi,
            'url': self.url,
            'citation_count': self.citation_count,
            'abstract': self.abstract,
            'topic': self.topic,
            'labels': self.labels,
            'source': self.source
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Paper':
        """从字典创建"""
        return cls(
            id=data.get('id', ''),
            title=data.get('title', ''),
            authors=data.get('authors', []),
            year=data.get('year', 0),
            venue=data.get('venue', ''),
            volume=data.get('volume', ''),
            issue=data.get('issue', ''),
            pages=data.get('pages', ''),
            doi=data.get('doi', ''),
            url=data.get('url', ''),
            citation_count=data.get('citation_count', 0),
            abstract=data.get('abstract', ''),
            topic=data.get('topic', ''),
            labels=data.get('labels', {}),
            source=data.get('source', '')
        )


class Deduplicator:
    """文献去重器"""
    
    def __init__(self, similarity_threshold: float = 0.85):
        self.similarity_threshold = similarity_threshold
        self.seen_dois: Set[str] = set()
        self.seen_titles: List[Tuple[str, Paper]] = []
    
    def deduplicate(self, papers: List[Paper]) -> List[Paper]:
        """
        去重文献列表
        
        策略：
        1. 首先基于DOI去重
        2. 然后基于标题相似度去重
        3. 保留信息更完整的版本
        """
        unique_papers = []
        
        for paper in papers:
            # 检查DOI
            if paper.doi and paper.doi in self.seen_dois:
                continue
            
            # 检查标题相似度
            if self._is_similar_title(paper.title):
                continue
            
            # 添加到已见列表
            if paper.doi:
                self.seen_dois.add(paper.doi)
            self.seen_titles.append((paper.title.lower(), paper))
            unique_papers.append(paper)
        
        return unique_papers
    
    def _is_similar_title(self, title: str) -> bool:
        """检查标题是否相似"""
        title_lower = title.lower()
        for seen_title, _ in self.seen_titles:
            similarity = difflib.SequenceMatcher(None, title_lower, seen_title).ratio()
            if similarity >= self.similarity_threshold:
                return True
        return False


class TopicClassifier:
    """主题分类器"""
    
    def __init__(self, topic_keywords: Dict[str, List[str]]):
        self.topic_keywords = topic_keywords
    
    def classify(self, paper: Paper) -> str:
        """
        根据关键词匹配判断文献主题
        
        Returns:
            最匹配的主题名称
        """
        text = f"{paper.title} {paper.abstract}".lower()
        
        best_topic = "未分类"
        best_score = 0
        
        for topic, keywords in self.topic_keywords.items():
            score = sum(1 for kw in keywords if kw.lower() in text)
            if score > best_score:
                best_score = score
                best_topic = topic
        
        return best_topic
    
    def classify_batch(self, papers: List[Paper]) -> Dict[str, List[Paper]]:
        """批量分类"""
        result = defaultdict(list)
        for paper in papers:
            topic = self.classify(paper)
            paper.topic = topic
            result[topic].append(paper)
        return dict(result)


class LiteratureFilter:
    """文献筛选器"""
    
    @staticmethod
    def by_citation_count(papers: List[Paper], min_count: int = 0, max_count: int = float('inf')) -> List[Paper]:
        """按引用量筛选"""
        return [p for p in papers if min_count <= p.citation_count <= max_count]
    
    @staticmethod
    def by_year(papers: List[Paper], min_year: int = 0, max_year: int = float('inf')) -> List[Paper]:
        """按年份筛选"""
        return [p for p in papers if min_year <= p.year <= max_year]
    
    @staticmethod
    def by_venue_type(papers: List[Paper], exclude_types: List[str] = None) -> List[Paper]:
        """按期刊类型筛选（排除预印本等）"""
        if exclude_types is None:
            exclude_types = ['preprint', 'manuscript', 'working paper']
        
        filtered = []
        for paper in papers:
            venue_lower = paper.venue.lower()
            if not any(excl in venue_lower for excl in exclude_types):
                filtered.append(paper)
        return filtered
    
    @staticmethod
    def by_importance(papers: List[Paper], levels: List[str]) -> List[Paper]:
        """按重要性等级筛选"""
        return [p for p in papers if p.importance in levels]


class LiteratureMerger:
    """文献合并器"""
    
    def __init__(self):
        self.deduplicator = Deduplicator()
    
    def merge(self, *paper_lists: List[Paper]) -> List[Paper]:
        """
        合并多个文献列表并去重
        
        Args:
            *paper_lists: 多个文献列表
            
        Returns:
            合并去重后的文献列表
        """
        all_papers = []
        for i, papers in enumerate(paper_lists):
            for paper in papers:
                paper.source = f"source_{i+1}"
            all_papers.extend(papers)
        
        return self.deduplicator.deduplicate(all_papers)


class LiteratureProcessor:
    """文献处理主类"""
    
    def __init__(self, topic_keywords: Dict[str, List[str]] = None):
        self.deduplicator = Deduplicator()
        self.classifier = TopicClassifier(topic_keywords or {})
        self.filter = LiteratureFilter()
        self.merger = LiteratureMerger()
    
    def process_pipeline(self, 
                        papers: List[Paper],
                        min_citations: int = 0,
                        min_year: int = 0,
                        exclude_preprints: bool = True) -> Dict[str, Any]:
        """
        完整处理流程
        
        Args:
            papers: 原始文献列表
            min_citations: 最小引用量
            min_year: 最小年份
            exclude_preprints: 是否排除预印本
            
        Returns:
            处理结果统计
        """
        result = {
            'original_count': len(papers),
            'after_deduplication': 0,
            'after_filter': 0,
            'by_topic': {},
            'by_importance': {}
        }
        
        # 1. 去重
        papers = self.deduplicator.deduplicate(papers)
        result['after_deduplication'] = len(papers)
        
        # 2. 筛选
        papers = self.filter.by_citation_count(papers, min_count=min_citations)
        papers = self.filter.by_year(papers, min_year=min_year)
        if exclude_preprints:
            papers = self.filter.by_venue_type(papers)
        result['after_filter'] = len(papers)
        
        # 3. 分类
        by_topic = self.classifier.classify_batch(papers)
        result['by_topic'] = {k: len(v) for k, v in by_topic.items()}
        
        # 4. 重要性统计
        importance_count = defaultdict(int)
        for paper in papers:
            importance_count[paper.importance] += 1
        result['by_importance'] = dict(importance_count)
        
        return result
    
    def save_to_json(self, papers: List[Paper], filepath: str):
        """保存文献到JSON文件"""
        data = {
            'version': '1.0.0',
            'total_count': len(papers),
            'papers': [p.to_dict() for p in papers]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_from_json(self, filepath: str) -> List[Paper]:
        """从JSON文件加载文献"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return [Paper.from_dict(p) for p in data.get('papers', [])]


# 预定义的主题关键词（用于课堂拍照行为研究）
CLASSROOM_PHOTOGRAPHY_TOPICS = {
    "课堂拍照行为": ["photo-taking", "photography", "camera", "phone use", "mobile device"],
    "行为动机": ["motivation", "reason", "purpose", "why students"],
    "情境因素": ["context", "situation", "classroom environment", "setting"],
    "教师态度": ["teacher attitude", "instructor perception", "faculty view"],
    "课堂管理": ["classroom management", "policy", "regulation", "ban", "prohibit"],
    "学习效果": ["learning outcome", "academic performance", "comprehension", "retention"],
    "认知负荷": ["cognitive load", "cognitive offload", "mental effort"],
    "注意力": ["attention", "distraction", "focus", "engagement"]
}


def main():
    """示例用法"""
    # 创建处理器
    processor = LiteratureProcessor(CLASSROOM_PHOTOGRAPHY_TOPICS)
    
    # 示例：处理文献列表
    # papers = processor.load_from_json('input.json')
    # result = processor.process_pipeline(papers, min_citations=10, min_year=2015)
    # processor.save_to_json(papers, 'output.json')
    
    print("文献处理工具已加载")
    print("功能：去重、分类、筛选、合并")
    print("预定义主题：", list(CLASSROOM_PHOTOGRAPHY_TOPICS.keys()))


if __name__ == "__main__":
    main()
