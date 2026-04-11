#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新笔记文件，添加完整的paper字段

功能：读取知识库index.json，为每篇笔记添加完整的参考文献信息
"""

import json
import os
from pathlib import Path
from typing import Dict, Any

def load_json(filepath: str) -> Dict:
    """加载JSON文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data: Dict, filepath: str):
    """保存JSON文件"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def update_notes_with_paper_info(notes_file: str, index_file: str):
    """
    更新笔记文件，添加paper字段
    
    Args:
        notes_file: 笔记文件路径
        index_file: 知识库索引文件路径
    """
    # 加载笔记文件
    notes_data = load_json(notes_file)
    
    # 加载索引文件
    index_data = load_json(index_file)
    
    # 创建ID到文献信息的映射
    paper_info_map = {}
    for paper in index_data.get('papers', []):
        paper_id = paper.get('id', '')
        if paper_id:
            paper_info_map[paper_id] = {
                "authors": paper.get('authors', []),
                "year": paper.get('year', 0),
                "title": paper.get('title', ''),
                "venue": paper.get('venue', ''),
                "volume": paper.get('volume', ''),
                "issue": paper.get('issue', ''),
                "pages": paper.get('pages', ''),
                "doi": paper.get('doi', ''),
                "url": paper.get('url', ''),
                "citation_count": paper.get('citation_count', 0)
            }
    
    # 更新每篇笔记
    updated_count = 0
    for note_id, note_content in notes_data.get('notes', {}).items():
        if note_id in paper_info_map:
            # 添加paper字段
            note_content['paper'] = paper_info_map[note_id]
            updated_count += 1
    
    # 保存更新后的笔记文件
    save_json(notes_data, notes_file)
    
    print(f"✅ 已更新 {updated_count} 篇笔记")
    return updated_count

def main():
    """主函数"""
    notes_dir = "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/笔记"
    index_file = "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/index.json"
    
    # 获取所有笔记文件
    notes_files = [f for f in os.listdir(notes_dir) if f.endswith('.json')]
    
    total_updated = 0
    for notes_file in notes_files:
        filepath = os.path.join(notes_dir, notes_file)
        print(f"\n处理: {notes_file}")
        count = update_notes_with_paper_info(filepath, index_file)
        total_updated += count
    
    print(f"\n✅ 总计更新 {total_updated} 篇笔记")

if __name__ == "__main__":
    main()
