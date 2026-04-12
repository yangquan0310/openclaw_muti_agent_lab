#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
标准化知识库index.json格式

功能：
1. 统一字段命名（citationCount -> citation_count）
2. 转换authors为列表格式
3. 添加缺失的字段（volume, issue, pages）
4. 标准化labels格式
5. 添加元数据字段（version, project, created_at等）
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any


def normalize_paper(paper: Dict) -> Dict:
    """标准化单篇文献格式"""
    # 转换authors为列表
    authors = paper.get('authors', '')
    if isinstance(authors, str):
        authors = [a.strip() for a in authors.split(',') if a.strip()]
    
    # 标准化labels
    labels = paper.get('labels', {})
    if isinstance(labels, list):
        # 如果是列表，转换为字典
        labels_dict = {}
        for label in labels:
            if 'importance' in label:
                labels_dict['importance'] = label['importance']
            elif 'type' in label:
                labels_dict['type'] = label['type']
        labels = labels_dict
    
    # 确保labels包含必要字段
    if 'importance' not in labels:
        # 根据引用量判断
        citation_count = paper.get('citationCount', 0) or paper.get('citation_count', 0)
        if citation_count >= 500:
            labels['importance'] = '🔴奠基'
        elif citation_count >= 50:
            labels['importance'] = '🟡重要'
        else:
            labels['importance'] = '🔵一般'
    
    if 'type' not in labels:
        labels['type'] = '📋待分类'
    
    if 'jcr_quartile' not in labels:
        labels['jcr_quartile'] = '待筛选'
    
    return {
        'id': paper.get('id', ''),
        'title': paper.get('title', ''),
        'authors': authors,
        'year': paper.get('year', 0),
        'venue': paper.get('venue', ''),
        'volume': paper.get('volume', ''),
        'issue': paper.get('issue', ''),
        'pages': paper.get('pages', ''),
        'doi': paper.get('doi', ''),
        'url': paper.get('url', ''),
        'citation_count': paper.get('citationCount', 0) or paper.get('citation_count', 0),
        'abstract': paper.get('abstract', ''),
        'topic': paper.get('topic', ''),
        'labels': labels
    }


def normalize_index_json(filepath: str, project_name: str = "") -> Dict:
    """标准化整个index.json文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    papers = data.get('papers', [])
    normalized_papers = [normalize_paper(p) for p in papers]
    
    # 构建标准化的数据结构
    normalized_data = {
        'version': '1.0.0',
        'project': project_name or data.get('project', '未知项目'),
        'created_at': data.get('created_at', datetime.now().isoformat()),
        'updated_at': datetime.now().isoformat(),
        'total_count': len(normalized_papers),
        'statistics': {
            'foundation_count': sum(1 for p in normalized_papers if '🔴' in p['labels'].get('importance', '')),
            'important_count': sum(1 for p in normalized_papers if '🟡' in p['labels'].get('importance', '')),
            'general_count': sum(1 for p in normalized_papers if '🔵' in p['labels'].get('importance', '')),
            'empirical_count': sum(1 for p in normalized_papers if '📊' in p['labels'].get('type', '')),
            'review_count': sum(1 for p in normalized_papers if '📖' in p['labels'].get('type', '')),
            'theory_count': sum(1 for p in normalized_papers if '💡' in p['labels'].get('type', ''))
        },
        'papers': normalized_papers
    }
    
    return normalized_data


def main():
    """主函数"""
    # 处理学生论文修改项目的index.json
    filepath = '/root/实验室仓库/项目文件/学生论文修改/知识库/index.json'
    
    if not os.path.exists(filepath):
        print(f"文件不存在: {filepath}")
        return
    
    print("标准化index.json...")
    normalized = normalize_index_json(filepath, "学生论文修改-课堂拍照行为")
    
    # 保存
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(normalized, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 完成！")
    print(f"  总文献数: {normalized['total_count']}")
    print(f"  奠基文献: {normalized['statistics']['foundation_count']}")
    print(f"  重要文献: {normalized['statistics']['important_count']}")
    print(f"  一般文献: {normalized['statistics']['general_count']}")
    print(f"  实证研究: {normalized['statistics']['empirical_count']}")
    print(f"  综述文献: {normalized['statistics']['review_count']}")
    print(f"  理论文献: {normalized['statistics']['theory_count']}")


if __name__ == "__main__":
    main()
