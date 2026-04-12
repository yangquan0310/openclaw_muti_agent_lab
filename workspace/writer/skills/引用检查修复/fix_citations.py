#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修改综述中的引用格式：将DSAM_XXXX替换为APA 7th格式
"""

import json
import re

def parse_authors(author_str):
    """解析作者字符串，返回姓氏列表"""
    # 移除可能的 "and" 和 "&"
    author_str = author_str.replace(' and ', ', ').replace(' & ', ', ')
    # 按逗号分割
    authors = [a.strip() for a in author_str.split(',') if a.strip()]
    
    # 提取姓氏（假设格式是 "名 姓" 或 "姓, 名"）
    surnames = []
    for author in authors:
        # 处理 "Kymberly D. Young" 这种格式 -> 取最后一个词作为姓
        parts = author.split()
        if len(parts) > 0:
            # 取最后一个部分作为姓氏
            surname = parts[-1]
            surnames.append(surname)
    
    return surnames

def format_apa_citation(authors, year):
    """格式化APA引用"""
    surnames = parse_authors(authors)
    
    if len(surnames) == 1:
        return f"({surnames[0]}, {year})"
    elif len(surnames) == 2:
        return f"({surnames[0]} & {surnames[1]}, {year})"
    else:
        # 3个或更多作者
        return f"({surnames[0]} et al., {year})"

def format_apa_citation_text(authors, year):
    """格式化APA引用（文本内格式：作者等（年份））"""
    surnames = parse_authors(authors)
    
    if len(surnames) == 1:
        return f"{surnames[0]}（{year}）"
    elif len(surnames) == 2:
        return f"{surnames[0]}和{surnames[1]}（{year}）"
    else:
        # 3个或更多作者
        return f"{surnames[0]}等（{year}）"

def main():
    # 读取笔记文件
    with open('/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/笔记/自传体记忆的提取.json', 'r', encoding='utf-8') as f:
        notes = json.load(f)
    
    # 建立文献ID到APA引用的映射
    citation_map = {}
    citation_text_map = {}
    
    for note_id, note_data in notes.get('notes', {}).items():
        if note_id.startswith('DSAM_'):
            paper = note_data.get('paper', {})
            authors = paper.get('authors', '')
            year = paper.get('year', '')
            
            if authors and year:
                citation_map[note_id] = format_apa_citation(authors, year)
                citation_text_map[note_id] = format_apa_citation_text(authors, year)
                print(f"{note_id} -> {citation_map[note_id]} (文本: {citation_text_map[note_id]})")
    
    # 读取综述文件
    with open('/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/综述/自传体记忆的提取.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 替换模式1: "DSAM_XXXX研究" -> "作者等（年份）的研究"
    for dsam_id, citation_text in citation_text_map.items():
        pattern = rf'{dsam_id}研究'
        replacement = f'{citation_text}的研究'
        content = re.sub(pattern, replacement, content)
    
    # 替换模式2: "（DSAM_XXXX）" -> "（作者, 年份）"
    for dsam_id, citation in citation_map.items():
        pattern = rf'（{dsam_id}）'
        content = re.sub(pattern, citation.replace('(', '（').replace(')', '）'), content)
        
        # 也处理英文括号
        pattern = rf'\({dsam_id}\)'
        content = re.sub(pattern, citation, content)
    
    # 替换模式3: "DSAM_XXXX研究发现" -> "作者等（年份）的研究发现"
    for dsam_id, citation_text in citation_text_map.items():
        pattern = rf'{dsam_id}研究发现'
        replacement = f'{citation_text}的研究发现'
        content = re.sub(pattern, replacement, content)
    
    # 替换模式4: 单独出现的 "DSAM_XXXX"（作为名词使用）
    for dsam_id, citation_text in citation_text_map.items():
        # 确保是独立的词，不是其他词的一部分
        pattern = rf'(?<![A-Za-z0-9_]){dsam_id}(?![A-Za-z0-9_])'
        # 检查是否已经被替换过（通过检查是否还包含DSAM_）
        if dsam_id in content:
            content = re.sub(pattern, citation_text, content)
    
    # 写入修改后的文件
    with open('/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/综述/自传体记忆的提取.md', 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 统计替换情况
    replaced_count = 0
    for dsam_id in citation_map.keys():
        if dsam_id not in content:
            replaced_count += 1
            print(f"✓ 已替换: {dsam_id}")
        else:
            print(f"✗ 未替换: {dsam_id}")
    
    print(f"\n总计: {replaced_count}/{len(citation_map)} 个引用已替换")

if __name__ == '__main__':
    main()
