#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
笔记生成器 - 按照S2脚本要求生成文献笔记

类结构说明：
- NoteExtractor: 笔记提取器，负责从文献中提取结构化笔记内容
- NoteMerger: 笔记合并器，负责合并多个笔记文件
- NoteGenerator: 笔记生成器主类，协调提取和合并流程

使用示例：
    generator = NoteGenerator(project_dir="/path/to/project")
    generator.generate_all_notes()
    
    merger = NoteMerger(notes_dir="/path/to/notes")
    merger.merge_by_topic(topic_mapping)
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Paper:
    """文献数据类"""
    id: str
    title: str
    authors: str = ""
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
    
    @property
    def doc_type(self) -> str:
        """获取文献类型"""
        return self.labels.get('type', '📋待分类')
    
    @property
    def importance(self) -> str:
        """获取重要性等级"""
        return self.labels.get('importance', '🔵一般')


@dataclass
class NoteContent:
    """笔记内容数据类"""
    title: str
    doc_type: str
    paper: Dict[str, Any]  # 完整的参考文献信息
    content: Dict[str, str]
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "title": self.title,
            "type": self.doc_type,
            "paper": self.paper,
            "content": self.content
        }


@dataclass
class NoteStatistics:
    """笔记统计数据类"""
    total_count: int = 0
    empirical_count: int = 0
    review_count: int = 0
    theory_count: int = 0
    
    def add(self, doc_type: str) -> None:
        """添加一篇文献的统计"""
        self.total_count += 1
        if "📊" in doc_type:
            self.empirical_count += 1
        elif "📖" in doc_type:
            self.review_count += 1
        elif "💡" in doc_type:
            self.theory_count += 1
    
    def to_dict(self) -> Dict[str, int]:
        """转换为字典格式"""
        return {
            "total_count": self.total_count,
            "empirical_count": self.empirical_count,
            "review_count": self.review_count,
            "theory_count": self.theory_count
        }


class NoteExtractor:
    """
    笔记提取器
    
    负责从单篇文献中提取结构化笔记内容
    严格按照S2脚本要求处理不同类型的文献
    """
    
    def __init__(self):
        self.processed_count = 0
    
    def extract(self, paper: Paper) -> Optional[NoteContent]:
        """
        从文献中提取笔记内容
        
        Args:
            paper: 文献数据对象
            
        Returns:
            NoteContent对象，如果提取失败则返回None
        """
        if not paper.title:
            return None
        
        doc_type = paper.doc_type
        content = self._extract_by_type(paper, doc_type)
        
        # 构建完整的参考文献信息
        paper_info = {
            "authors": paper.authors.split(', ') if paper.authors else [],
            "year": paper.year,
            "title": paper.title,
            "venue": paper.venue,
            "volume": paper.volume,
            "issue": paper.issue,
            "pages": paper.pages,
            "doi": paper.doi,
            "url": paper.url,
            "citation_count": paper.citation_count
        }
        
        self.processed_count += 1
        return NoteContent(
            title=paper.title,
            doc_type=doc_type,
            paper=paper_info,
            content=content
        )
    
    def _extract_by_type(self, paper: Paper, doc_type: str) -> Dict[str, str]:
        """
        根据文献类型提取不同结构的内容
        
        📊实证文献：研究问题、研究方法、研究结果、研究结论
        📖综述文献：问题、结果、展望
        💡理论文献：问题、观点
        """
        abstract = paper.abstract or ''
        
        if "📊" in doc_type:
            return self._extract_empirical(abstract)
        elif "📖" in doc_type:
            return self._extract_review(abstract)
        elif "💡" in doc_type:
            return self._extract_theory(abstract)
        else:
            return {}
    
    def _extract_empirical(self, abstract: str) -> Dict[str, str]:
        """提取实证文献内容（待子代理填充）"""
        return {
            "research_question": "",
            "method": "",
            "results": "",
            "conclusion": ""
        }
    
    def _extract_review(self, abstract: str) -> Dict[str, str]:
        """提取综述文献内容（待子代理填充）"""
        return {
            "question": "",
            "results": "",
            "outlook": ""
        }
    
    def _extract_theory(self, abstract: str) -> Dict[str, str]:
        """提取理论文献内容（待子代理填充）"""
        return {
            "question": "",
            "viewpoint": ""
        }
    
    def get_stats(self) -> int:
        """获取已处理的文献数量"""
        return self.processed_count
    
    def reset_stats(self) -> None:
        """重置统计"""
        self.processed_count = 0


class NoteMerger:
    """
    笔记合并器
    
    负责将多个笔记文件按主题合并为统一的笔记文件
    """
    
    def __init__(self, notes_dir: str):
        self.notes_dir = Path(notes_dir)
        self.merged_count = 0
        self.duplicate_count = 0
    
    def load_note_file(self, filepath: Path) -> Optional[Dict[str, Any]]:
        """
        加载单个笔记文件
        
        Args:
            filepath: 文件路径
            
        Returns:
            笔记数据字典，加载失败返回None
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError, UnicodeDecodeError) as e:
            print(f"❌ 加载失败 {filepath}: {str(e)[:50]}")
            return None
    
    def merge_notes(self, file_list: List[str]) -> Tuple[Dict[str, Any], set]:
        """
        合并多个笔记文件
        
        Args:
            file_list: 要合并的文件列表
            
        Returns:
            (合并后的数据字典, 所有文献ID集合)
        """
        merged_data = {
            "version": "1.0.0",
            "project": "",
            "note_name": "",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "statistics": {
                "total_count": 0,
                "empirical_count": 0,
                "review_count": 0,
                "theory_count": 0
            },
            "notes": {}
        }
        
        all_paper_ids = set()
        
        for filename in file_list:
            filepath = self.notes_dir / filename
            data = self.load_note_file(filepath)
            
            if not data:
                continue
            
            # 合并统计信息
            stats = data.get('statistics', {})
            merged_data['statistics']['total_count'] += stats.get('total_count', 0)
            merged_data['statistics']['empirical_count'] += stats.get('empirical_count', 0)
            merged_data['statistics']['review_count'] += stats.get('review_count', 0)
            merged_data['statistics']['theory_count'] += stats.get('theory_count', 0)
            
            # 合并笔记（检查重复）
            notes = data.get('notes', {})
            for paper_id, note_content in notes.items():
                if paper_id in all_paper_ids:
                    self.duplicate_count += 1
                    continue
                merged_data['notes'][paper_id] = note_content
                all_paper_ids.add(paper_id)
            
            self.merged_count += 1
        
        return merged_data, all_paper_ids
    
    def save_merged_notes(self, data: Dict[str, Any], output_filename: str) -> Path:
        """
        保存合并后的笔记文件
        
        Args:
            data: 合并后的数据
            output_filename: 输出文件名
            
        Returns:
            输出文件路径
        """
        output_path = self.notes_dir / output_filename
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return output_path
    
    def merge_by_topic(self, topic_mapping: Dict[str, List[str]], 
                       project_name: str = "数字化存储与自传体记忆") -> List[Tuple[str, int, Path]]:
        """
        按主题合并笔记文件
        
        Args:
            topic_mapping: 主题到文件列表的映射
            project_name: 项目名称
            
        Returns:
            合并结果列表 [(主题, 文献数, 文件路径), ...]
        """
        results = []
        all_papers = set()
        
        for topic, file_list in topic_mapping.items():
            print(f"\n合并主题: {topic}")
            
            # 合并笔记
            merged_data, paper_ids = self.merge_notes(file_list)
            merged_data['project'] = project_name
            merged_data['note_name'] = topic
            
            # 更新统计（基于实际合并后的数量）
            actual_count = len(merged_data['notes'])
            merged_data['statistics']['total_count'] = actual_count
            
            # 保存文件
            output_filename = f"{topic}.json"
            output_path = self.save_merged_notes(merged_data, output_filename)
            
            results.append((topic, actual_count, output_path))
            all_papers.update(paper_ids)
            
            print(f"  ✅ {output_filename}: {actual_count}篇")
        
        print(f"\n{'='*60}")
        print(f"合并完成: 共{len(results)}个主题, {len(all_papers)}篇文献")
        if self.duplicate_count > 0:
            print(f"发现重复: {self.duplicate_count}篇")
        
        return results
    
    def get_stats(self) -> Dict[str, int]:
        """获取合并统计"""
        return {
            "merged_files": self.merged_count,
            "duplicates": self.duplicate_count
        }
    
    def reset_stats(self) -> None:
        """重置统计"""
        self.merged_count = 0
        self.duplicate_count = 0


class NoteGenerator:
    """
    笔记生成器主类
    
    协调笔记提取和合并流程，提供统一的生成接口
    """
    
    def __init__(self, project_dir: str):
        self.project_dir = Path(project_dir)
        self.index_file = self.project_dir / "知识库" / "index.json"
        self.notes_dir = self.project_dir / "知识库" / "笔记"
        
        self.extractor = NoteExtractor()
        self.merger = NoteMerger(str(self.notes_dir))
        
        self.index_data = None
        self.papers = []
    
    def load_index(self) -> bool:
        """加载知识库索引"""
        try:
            with open(self.index_file, 'r', encoding='utf-8') as f:
                self.index_data = json.load(f)
            self.papers = self._parse_papers()
            return True
        except Exception as e:
            print(f"❌ 加载索引失败: {str(e)}")
            return False
    
    def _parse_papers(self) -> List[Paper]:
        """解析索引数据为Paper对象列表"""
        papers = []
        for p in self.index_data.get('papers', []):
            paper = Paper(
                id=p.get('id', ''),
                title=p.get('title', ''),
                authors=p.get('authors', ''),
                year=p.get('year', 0),
                venue=p.get('venue', ''),
                abstract=p.get('abstract', ''),
                topic=p.get('topic', ''),
                labels=p.get('labels', {})
            )
            papers.append(paper)
        return papers
    
    def get_papers_by_topic(self, topic: str) -> List[Paper]:
        """获取指定主题的文献"""
        return [p for p in self.papers if p.topic == topic]
    
    def generate_topic_notes(self, topic: str, output_filename: Optional[str] = None) -> Optional[Path]:
        """
        为单个主题生成笔记文件
        
        Args:
            topic: 主题名称
            output_filename: 输出文件名（默认为主题名.json）
            
        Returns:
            输出文件路径，失败返回None
        """
        papers = self.get_papers_by_topic(topic)
        if not papers:
            print(f"⚠ {topic}: 无文献")
            return None
        
        notes = {}
        stats = NoteStatistics()
        
        # 逐篇提取笔记
        for paper in papers:
            note = self.extractor.extract(paper)
            if note:
                notes[paper.id] = note.to_dict()
                stats.add(paper.doc_type)
        
        # 构建笔记文件数据
        note_data = {
            "version": "1.0.0",
            "project": self.index_data.get('project', ''),
            "note_name": topic,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "statistics": stats.to_dict(),
            "notes": notes
        }
        
        # 保存文件
        if not output_filename:
            output_filename = f"{topic}.json"
        output_path = self.notes_dir / output_filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(note_data, f, ensure_ascii=False, indent=2)
        
        return output_path
    
    def generate_all_notes(self, topics: Optional[List[str]] = None) -> List[Tuple[str, int, Path]]:
        """
        为所有主题生成笔记
        
        Args:
            topics: 主题列表（默认从索引中获取所有主题）
            
        Returns:
            生成结果列表 [(主题, 文献数, 文件路径), ...]
        """
        if not self.load_index():
            return []
        
        if not topics:
            # 从索引中获取所有主题
            topics = list(set(p.topic for p in self.papers if p.topic))
        
        results = []
        print(f"\n{'='*60}")
        print(f"开始生成笔记: 共{len(topics)}个主题")
        print(f"{'='*60}\n")
        
        for topic in sorted(topics):
            output_path = self.generate_topic_notes(topic)
            if output_path:
                count = len(self.get_papers_by_topic(topic))
                results.append((topic, count, output_path))
                print(f"✓ {topic}: {count}篇")
        
        print(f"\n{'='*60}")
        print(f"生成完成: 共{len(results)}个主题")
        print(f"{'='*60}")
        
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取生成统计"""
        return {
            "extractor": self.extractor.get_stats(),
            "merger": self.merger.get_stats(),
            "total_papers": len(self.papers),
            "topics": len(set(p.topic for p in self.papers if p.topic))
        }


# 便捷函数接口
def generate_notes(project_dir: str, topics: Optional[List[str]] = None) -> List[Tuple[str, int, Path]]:
    """
    便捷函数：生成笔记
    
    Args:
        project_dir: 项目目录路径
        topics: 主题列表（可选）
        
    Returns:
        生成结果列表
    """
    generator = NoteGenerator(project_dir)
    return generator.generate_all_notes(topics)


def merge_notes(notes_dir: str, topic_mapping: Dict[str, List[str]], 
                project_name: str = "数字化存储与自传体记忆") -> List[Tuple[str, int, Path]]:
    """
    便捷函数：合并笔记
    
    Args:
        notes_dir: 笔记目录路径
        topic_mapping: 主题到文件列表的映射
        project_name: 项目名称
        
    Returns:
        合并结果列表
    """
    merger = NoteMerger(notes_dir)
    return merger.merge_by_topic(topic_mapping, project_name)


# 默认主题映射（用于数字化存储与自传体记忆项目）
DEFAULT_TOPIC_MAPPING = {
    '自传体记忆的概念': [
        '自传体记忆基础_第1-10篇.json',
        '自传体记忆基础_第11-20篇.json',
        '自传体记忆基础_第21-30篇.json',
        '第4批_DSAM_0079-0114.json',
        '第5批_DSAM_0115-0136.json',
        '自传体记忆基础_第41-50篇.json',
        '自传体记忆基础_第51-67篇.json',
        '自传体记忆基础_第68-84篇.json'
    ],
    '自传体记忆的功能': [
        '自传体记忆功能_第1-30篇.json',
        '自传体记忆功能_第31-60篇.json',
        '自传体记忆功能_第61-85篇.json'
    ],
    '自传体记忆的编码': [
        '自传体记忆的自我参照编码_第1-27篇.json',
        '自传体记忆的自我参照编码_第28-54篇.json'
    ],
    '自传体记忆的存储': [
        '自传体记忆的系统性巩固_第1-22篇.json',
        '自传体记忆的系统性巩固_第23-44篇.json'
    ],
    '自传体记忆的遗忘': [
        '自传体记忆的主动遗忘_全部.json'
    ],
    '自传体记忆的提取': [
        '自传体记忆的生成性提取_全部.json'
    ],
    '数字化使用对自传体记忆的影响': [
        '数字化使用对自传体记忆的影响_全部.json'
    ]
}


if __name__ == "__main__":
    # 示例用法
    PROJECT_DIR = "/root/实验室仓库/项目文件/数字化存储与自传体记忆"
    
    # 方式1: 使用NoteGenerator生成笔记
    # generator = NoteGenerator(PROJECT_DIR)
    # results = generator.generate_all_notes()
    
    # 方式2: 使用便捷函数
    # results = generate_notes(PROJECT_DIR)
    
    # 方式3: 合并已有笔记文件
    NOTES_DIR = f"{PROJECT_DIR}/知识库/笔记"
    merger = NoteMerger(NOTES_DIR)
    results = merger.merge_by_topic(DEFAULT_TOPIC_MAPPING)
    
    print("\n生成结果:")
    for topic, count, filepath in results:
        print(f"  - {topic}: {count}篇 -> {filepath}")
