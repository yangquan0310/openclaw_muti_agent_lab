#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
核查并修复综述参考文献格式
只使用笔记文件中实际存在的字段（authors, year, title, venue, url）
不编造volume、issue、pages、doi等信息
"""

import json
import re
import os

# 文件路径映射
file_mapping = {
    "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/综述/自传体记忆的概念.md": "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/笔记/自传体记忆的概念.json",
    "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/综述/自传体记忆的功能.md": "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/笔记/自传体记忆的功能.json",
    "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/综述/自传体记忆的存储.md": "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/笔记/自传体记忆的存储.json",
    "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/综述/自传体记忆的遗忘.md": "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/笔记/自传体记忆的遗忘.json",
    "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/综述/自传体记忆的提取.md": "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/笔记/自传体记忆的提取.json",
    "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/综述/数字化使用对自传体记忆的影响.md": "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/笔记/数字化使用对自传体记忆的影响.json",
}

def load_json_notes(json_path):
    """加载笔记JSON文件，返回文献信息列表"""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    papers = []
    for note_id, note_data in data.get('notes', {}).items():
        paper = note_data.get('paper', {})
        if paper:
            papers.append(paper)
    return papers

def format_apa_reference(paper):
    """
    根据APA格式生成参考文献，只使用实际存在的字段
    格式：作者. (年份). 标题. *期刊名*. URL
    """
    authors = paper.get('authors', '').strip()
    year = paper.get('year', '')
    title = paper.get('title', '').strip()
    venue = paper.get('venue', '').strip()
    url = paper.get('url', '').strip()
    
    # 构建APA格式引用
    parts = []
    
    # 作者
    if authors:
        parts.append(authors)
    
    # 年份
    if year:
        parts.append(f"({year})")
    
    # 标题
    if title:
        # 标题末尾添加句点
        if not title.endswith('.'):
            title += '.'
        parts.append(title)
    
    # 期刊名（斜体）
    if venue:
        # 期刊名末尾添加句点
        if not venue.endswith('.'):
            venue += '.'
        parts.append(f"*{venue}*")
    
    # URL
    if url:
        parts.append(url)
    
    return ' '.join(parts)

def parse_reference_line(line):
    """
    解析参考文献行，提取作者和年份
    返回 (作者, 年份, 原始行)
    """
    # 匹配格式：Author, A. A. (Year). Title. *Venue*, ...
    # 或 Author et al. (Year)
    match = re.match(r'^([^(]+)\((\d{4})\)[.,]?\s*(.*)', line.strip())
    if match:
        authors = match.group(1).strip()
        year = match.group(2)
        rest = match.group(3)
        return authors, year, rest
    return None, None, None

def match_paper_to_reference(authors, year, papers):
    """
    根据作者和年份匹配文献
    """
    if not authors or not year:
        return None
    
    authors_lower = authors.lower()
    
    for paper in papers:
        paper_authors = paper.get('authors', '').lower()
        paper_year = str(paper.get('year', ''))
        
        # 年份必须匹配
        if paper_year != year:
            continue
        
        # 检查作者是否匹配
        # 提取第一作者姓氏
        ref_first_author = authors_lower.split(',')[0].strip()
        paper_first_author = paper_authors.split(',')[0].strip() if ',' in paper_authors else paper_authors.split()[-1].strip()
        
        # 检查是否包含
        if ref_first_author in paper_first_author or paper_first_author in ref_first_author:
            return paper
        
        # 检查et al.情况
        if 'et al' in authors_lower:
            ref_first = authors_lower.split('et al')[0].strip()
            if ref_first in paper_authors or paper_authors.startswith(ref_first):
                return paper
    
    return None

def fix_references_section(md_path, json_path):
    """修复markdown文件中的参考文献部分"""
    # 加载笔记数据
    papers = load_json_notes(json_path)
    
    # 读取markdown内容
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找参考文献部分
    ref_section_match = re.search(r'## 参考文献\s*\n', content)
    if not ref_section_match:
        print(f"   ⚠️ 未找到参考文献部分")
        return {'fixed': 0, 'total': 0}
    
    ref_start = ref_section_match.end()
    ref_content = content[ref_start:]
    
    # 分割参考文献行
    lines = ref_content.split('\n')
    
    fixed_count = 0
    total_count = 0
    new_lines = []
    
    for line in lines:
        # 跳过空行和标题
        if not line.strip() or line.strip().startswith('#') or line.strip().startswith('*'):
            new_lines.append(line)
            continue
        
        # 检查是否是参考文献行（以作者开头，包含年份）
        authors, year, rest = parse_reference_line(line)
        if authors and year:
            total_count += 1
            paper = match_paper_to_reference(authors, year, papers)
            if paper:
                new_ref = format_apa_reference(paper)
                new_lines.append(new_ref)
                fixed_count += 1
            else:
                # 无法匹配，保留原行
                new_lines.append(line)
        else:
            new_lines.append(line)
    
    # 重建内容
    new_ref_content = '\n'.join(new_lines)
    new_content = content[:ref_start] + new_ref_content
    
    # 写回文件
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return {'fixed': fixed_count, 'total': total_count}

def main():
    """主函数"""
    print("=" * 60)
    print("开始核查并修复参考文献格式")
    print("=" * 60)
    
    total_fixed = 0
    total_refs = 0
    
    for md_path, json_path in file_mapping.items():
        if not os.path.exists(md_path):
            print(f"\n❌ 文件不存在: {md_path}")
            continue
        if not os.path.exists(json_path):
            print(f"\n❌ 文件不存在: {json_path}")
            continue
        
        print(f"\n📄 处理: {os.path.basename(md_path)}")
        
        try:
            stats = fix_references_section(md_path, json_path)
            print(f"   总参考文献: {stats['total']}")
            print(f"   成功修复: {stats['fixed']}")
            total_fixed += stats['fixed']
            total_refs += stats['total']
        except Exception as e:
            print(f"   ❌ 错误: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print(f"参考文献格式修复完成")
    print(f"总计: {total_fixed}/{total_refs} 条参考文献已修复")
    print("=" * 60)

if __name__ == "__main__":
    main()
