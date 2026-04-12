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
    """加载笔记JSON文件，返回文献ID到文献信息的映射"""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    papers = {}
    for note_id, note_data in data.get('notes', {}).items():
        paper = note_data.get('paper', {})
        if paper:
            papers[note_id] = paper
    return papers

def format_apa_reference(paper):
    """
    根据APA格式生成参考文献，只使用实际存在的字段
    格式：作者. (年份). 标题. 期刊名. URL
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
    
    # 期刊名
    if venue:
        # 期刊名末尾添加句点
        if not venue.endswith('.'):
            venue += '.'
        parts.append(f"*{venue}*")
    
    # URL
    if url:
        parts.append(url)
    
    return ' '.join(parts)

def extract_citations_from_md(md_content):
    """从markdown内容中提取引用标记"""
    # 匹配 ((作者, 年份)) 或 ((作者年份)) 格式的引用
    pattern = r'\(\(([^)]+)\)\)'
    citations = re.findall(pattern, md_content)
    return citations

def find_paper_by_citation(citation_text, papers):
    """
    根据引用文本找到对应的文献
    支持多种匹配方式
    """
    citation_lower = citation_text.lower().strip()
    
    for note_id, paper in papers.items():
        authors = paper.get('authors', '').lower()
        year = str(paper.get('year', ''))
        title = paper.get('title', '').lower()
        
        # 尝试匹配作者+年份
        if year and year in citation_text:
            # 检查作者是否匹配
            author_parts = citation_lower.split(',')
            if author_parts:
                first_author = author_parts[0].strip()
                # 移除年份部分
                first_author = re.sub(r'\d{4}', '', first_author).strip()
                if first_author and (first_author in authors or authors.startswith(first_author)):
                    return paper
        
        # 尝试直接匹配标题
        if title and citation_lower in title:
            return paper
        
        # 尝试匹配作者
        if authors and citation_lower in authors:
            return paper
    
    return None

def fix_references_in_md(md_path, json_path):
    """修复markdown文件中的参考文献"""
    # 加载笔记数据
    papers = load_json_notes(json_path)
    
    # 读取markdown内容
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取引用
    citations = extract_citations_from_md(content)
    
    # 统计信息
    stats = {
        'total_citations': len(citations),
        'matched': 0,
        'unmatched': []
    }
    
    # 替换引用为正确的APA格式
    for citation in citations:
        paper = find_paper_by_citation(citation, papers)
        if paper:
            stats['matched'] += 1
            apa_ref = format_apa_reference(paper)
            old_citation = f"(({citation}))"
            content = content.replace(old_citation, apa_ref)
        else:
            stats['unmatched'].append(citation)
    
    # 写回文件
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return stats

def main():
    """主函数"""
    print("=" * 60)
    print("开始核查并修复参考文献格式")
    print("=" * 60)
    
    for md_path, json_path in file_mapping.items():
        if not os.path.exists(md_path):
            print(f"❌ 文件不存在: {md_path}")
            continue
        if not os.path.exists(json_path):
            print(f"❌ 文件不存在: {json_path}")
            continue
        
        print(f"\n📄 处理: {os.path.basename(md_path)}")
        
        try:
            stats = fix_references_in_md(md_path, json_path)
            print(f"   总引用数: {stats['total_citations']}")
            print(f"   成功匹配: {stats['matched']}")
            if stats['unmatched']:
                print(f"   未匹配: {len(stats['unmatched'])}")
                for u in stats['unmatched'][:5]:  # 只显示前5个
                    print(f"      - {u}")
        except Exception as e:
            print(f"   ❌ 错误: {e}")
    
    print("\n" + "=" * 60)
    print("参考文献格式修复完成")
    print("=" * 60)

if __name__ == "__main__":
    main()
