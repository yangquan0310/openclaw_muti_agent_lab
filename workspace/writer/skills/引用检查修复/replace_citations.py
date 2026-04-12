#!/usr/bin/env python3
"""
将综述中的DSAM_XXXX引用替换为APA 7th格式（作者, 年份）
"""

import json
import re

# 读取笔记文件
with open('/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/笔记/自传体记忆的功能.json', 'r', encoding='utf-8') as f:
    notes = json.load(f)

# 读取综述文件
with open('/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/综述/自传体记忆的功能.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 提取所有文献的作者和年份信息，构建映射字典
citation_map = {}
for key, value in notes['notes'].items():
    if 'paper' in value:
        authors = value['paper'].get('authors', '')
        year = value['paper'].get('year', '')
        
        # 处理作者格式：提取姓氏
        if authors and year:
            # 分割多个作者
            author_list = [a.strip() for a in authors.split(',')]
            
            # 提取姓氏（假设格式为 "名 姓" 或 "名 姓"）
            surnames = []
            for author in author_list:
                if author:
                    # 处理可能的格式：First Last 或 Last, First
                    parts = author.split()
                    if len(parts) >= 2:
                        # 取最后一个部分作为姓氏
                        surnames.append(parts[-1])
                    else:
                        surnames.append(author)
            
            # 构建APA格式引用
            if len(surnames) == 1:
                apa_citation = f"({surnames[0]}, {year})"
            elif len(surnames) == 2:
                apa_citation = f"({surnames[0]} & {surnames[1]}, {year})"
            elif len(surnames) >= 3:
                apa_citation = f"({surnames[0]} et al., {year})"
            else:
                apa_citation = f"({authors}, {year})"
            
            citation_map[key] = apa_citation

print(f"提取到 {len(citation_map)} 条文献引用映射")

# 查找综述中所有的DSAM_XXXX引用
pattern = r'DSAM_\d+'
found_citations = set(re.findall(pattern, content))
print(f"\n综述中找到 {len(found_citations)} 个DSAM引用:")
for c in sorted(found_citations):
    if c in citation_map:
        print(f"  {c} -> {citation_map[c]}")
    else:
        print(f"  {c} -> [未找到对应文献]")

# 执行替换
for dsam_id, apa_citation in citation_map.items():
    content = content.replace(dsam_id, apa_citation)

# 检查是否还有未替换的DSAM引用
remaining = re.findall(pattern, content)
if remaining:
    print(f"\n警告：还有 {len(set(remaining))} 个DSAM引用未替换:")
    for c in set(remaining):
        print(f"  {c}")
else:
    print("\n✓ 所有DSAM引用已成功替换")

# 保存修改后的文件
with open('/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/综述/自传体记忆的功能.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n文件已保存")
