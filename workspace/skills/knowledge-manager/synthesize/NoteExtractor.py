#!/usr/bin/env python3
"""
NoteExtractor.py - 笔记信息提取类

面向对象设计的笔记信息提取器，用于从知识库笔记文件中提取关键信息。
支持提取：研究问题、研究方法、研究结果、研究结论、理论观点等。

作者: Yang Quan
版本: 1.0.0
日期: 2026-04-20
"""

import json
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class PaperInfo:
    """单篇文献信息的数据类"""
    paper_id: str = ""
    title: str = ""
    authors: List[str] = field(default_factory=list)
    year: int = 0
    venue: str = ""
    doi: str = ""
    citation_count: int = 0
    paper_type: str = ""  # 实证/综述/理论
    research_question: str = ""
    method: str = ""
    findings: str = ""
    conclusion: str = ""
    theoretical_points: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'paper_id': self.paper_id,
            'title': self.title,
            'authors': self.authors,
            'year': self.year,
            'venue': self.venue,
            'doi': self.doi,
            'citation_count': self.citation_count,
            'type': self.paper_type,
            'research_question': self.research_question,
            'method': self.method,
            'findings': self.findings,
            'conclusion': self.conclusion,
            'theoretical_points': self.theoretical_points
        }


class NoteExtractor:
    """
    笔记信息提取类
    
    从知识库笔记文件中提取结构化信息，支持：
    - 提取所有文献的基本信息
    - 提取研究问题、方法、结果、结论
    - 按主题分类文献
    - 生成统计信息
    """
    
    def __init__(self):
        """初始化提取器"""
        self.papers: List[PaperInfo] = []
        self.stats: Dict[str, Any] = {}
        
    def extract(self, notes_path: str) -> Dict[str, Any]:
        """
        从笔记文件中提取所有信息
        
        参数:
            notes_path: 笔记JSON文件路径
            
        返回:
            包含提取信息的字典
        """
        # 加载JSON文件
        with open(notes_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 提取每篇文献的信息
        papers_data = data.get('papers', [])
        self.papers = []
        
        for paper_data in papers_data:
            paper_info = self._extract_paper_info(paper_data)
            self.papers.append(paper_info)
        
        # 生成统计信息
        self._generate_stats()
        
        # 返回提取结果
        return {
            'count': len(self.papers),
            'stats': self.stats,
            'papers': [p.to_dict() for p in self.papers],
            'research_questions': self._extract_all_research_questions(),
            'methods': self._extract_all_methods(),
            'findings': self._extract_all_findings(),
            'conclusions': self._extract_all_conclusions(),
            'theoretical_points': self._extract_all_theoretical_points(),
            'by_type': self._group_by_type(),
            'by_year': self._group_by_year()
        }
    
    def _extract_paper_info(self, paper_data: Dict) -> PaperInfo:
        """提取单篇文献的信息"""
        info = PaperInfo()
        
        # 基本信息
        info.paper_id = paper_data.get('paperId', '')
        info.title = paper_data.get('title', '')
        info.authors = paper_data.get('authors', [])
        info.year = paper_data.get('year', 0)
        info.venue = paper_data.get('venue', '')
        info.doi = paper_data.get('doi', '')
        info.citation_count = paper_data.get('citationCount', 0)
        
        # 类型标签
        labels = paper_data.get('labels', {})
        info.paper_type = labels.get('type', '')
        
        # 笔记信息
        notes = paper_data.get('notes', {})
        info.research_question = notes.get('研究问题', '')
        info.method = notes.get('研究方法', '')
        info.findings = notes.get('研究结果', '')
        info.conclusion = notes.get('研究结论', '')
        info.theoretical_points = notes.get('理论观点', '')
        
        return info
    
    def _generate_stats(self):
        """生成统计信息"""
        type_counts = defaultdict(int)
        year_counts = defaultdict(int)
        total_citations = 0
        
        for paper in self.papers:
            # 统计类型
            if paper.paper_type:
                type_counts[paper.paper_type] += 1
            
            # 统计年份
            if paper.year:
                year_counts[paper.year] += 1
            
            # 统计引用
            total_citations += paper.citation_count
        
        self.stats = {
            'total_count': len(self.papers),
            'type_distribution': dict(type_counts),
            'year_distribution': dict(year_counts),
            'total_citations': total_citations,
            'avg_citations': total_citations / len(self.papers) if self.papers else 0,
            'year_range': {
                'min': min(year_counts.keys()) if year_counts else 0,
                'max': max(year_counts.keys()) if year_counts else 0
            }
        }
    
    def _extract_all_research_questions(self) -> List[str]:
        """提取所有研究问题"""
        questions = []
        for paper in self.papers:
            if paper.research_question:
                questions.append({
                    'paper_id': paper.paper_id,
                    'title': paper.title,
                    'question': paper.research_question
                })
        return questions
    
    def _extract_all_methods(self) -> List[Dict]:
        """提取所有研究方法"""
        methods = []
        for paper in self.papers:
            if paper.method:
                methods.append({
                    'paper_id': paper.paper_id,
                    'title': paper.title,
                    'method': paper.method
                })
        return methods
    
    def _extract_all_findings(self) -> List[Dict]:
        """提取所有研究结果"""
        findings = []
        for paper in self.papers:
            if paper.findings:
                findings.append({
                    'paper_id': paper.paper_id,
                    'title': paper.title,
                    'findings': paper.findings
                })
        return findings
    
    def _extract_all_conclusions(self) -> List[Dict]:
        """提取所有研究结论"""
        conclusions = []
        for paper in self.papers:
            if paper.conclusion:
                conclusions.append({
                    'paper_id': paper.paper_id,
                    'title': paper.title,
                    'conclusion': paper.conclusion
                })
        return conclusions
    
    def _extract_all_theoretical_points(self) -> List[Dict]:
        """提取所有理论观点"""
        points = []
        for paper in self.papers:
            if paper.theoretical_points:
                points.append({
                    'paper_id': paper.paper_id,
                    'title': paper.title,
                    'points': paper.theoretical_points
                })
        return points
    
    def _group_by_type(self) -> Dict[str, List[Dict]]:
        """按类型分组"""
        groups = defaultdict(list)
        for paper in self.papers:
            paper_type = paper.paper_type or '未分类'
            groups[paper_type].append(paper.to_dict())
        return dict(groups)
    
    def _group_by_year(self) -> Dict[str, List[Dict]]:
        """按年份分组"""
        groups = defaultdict(list)
        for paper in self.papers:
            year = str(paper.year) if paper.year else '未知'
            groups[year].append(paper.to_dict())
        return dict(groups)
    
    def get_paper_by_id(self, paper_id: str) -> Optional[PaperInfo]:
        """根据ID获取单篇文献信息"""
        for paper in self.papers:
            if paper.paper_id == paper_id:
                return paper
        return None
    
    def filter_by_type(self, paper_type: str) -> List[PaperInfo]:
        """按类型筛选文献"""
        return [p for p in self.papers if p.paper_type == paper_type]
    
    def filter_by_year(self, year: int) -> List[PaperInfo]:
        """按年份筛选文献"""
        return [p for p in self.papers if p.year == year]
    
    def export_to_json(self, output_path: str):
        """导出提取结果到JSON文件"""
        result = {
            'count': len(self.papers),
            'stats': self.stats,
            'papers': [p.to_dict() for p in self.papers]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"提取结果已保存到: {output_path}")


# 命令行接口
if __name__ == '__main__':
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='笔记信息提取工具')
    parser.add_argument('--input', '-i', required=True, help='输入笔记JSON文件路径')
    parser.add_argument('--output', '-o', help='输出提取结果JSON文件路径（可选）')
    parser.add_argument('--format', '-f', choices=['json', 'markdown'], default='json',
                       help='输出格式')
    
    args = parser.parse_args()
    
    # 执行提取
    extractor = NoteExtractor()
    result = extractor.extract(args.input)
    
    # 输出结果
    if args.output:
        if args.format == 'json':
            extractor.export_to_json(args.output)
        else:
            # Markdown格式输出
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(f"# 笔记提取结果\n\n")
                f.write(f"## 统计信息\n\n")
                f.write(f"- 文献总数: {result['count']}\n")
                f.write(f"- 总引用数: {result['stats']['total_citations']}\n")
                f.write(f"- 平均引用: {result['stats']['avg_citations']:.2f}\n")
                f.write(f"- 年份范围: {result['stats']['year_range']['min']}-{result['stats']['year_range']['max']}\n\n")
                
                f.write(f"## 文献列表\n\n")
                for paper in result['papers']:
                    f.write(f"### {paper['title']}\n\n")
                    f.write(f"- **作者**: {', '.join(paper['authors'])}\n")
                    f.write(f"- **年份**: {paper['year']}\n")
                    f.write(f"- **类型**: {paper['type']}\n")
                    if paper['research_question']:
                        f.write(f"- **研究问题**: {paper['research_question']}\n")
                    if paper['findings']:
                        f.write(f"- **研究结果**: {paper['findings']}\n")
                    f.write(f"\n")
            
            print(f"提取结果已保存到: {args.output}")
    else:
        # 打印到控制台
        print(json.dumps(result, ensure_ascii=False, indent=2))
