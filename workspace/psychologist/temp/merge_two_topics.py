
#!/usr/bin/env python3
"""
合并两个主题JSON文件
"""

import json
import os
from collections import OrderedDict

NOTES_DIR = "/root/实验室仓库/项目文件/学生论文修改/知识库/笔记"
FILE1 = os.path.join(NOTES_DIR, "负性思维与睡眠质量.json")
FILE2 = os.path.join(NOTES_DIR, "反刍思维与睡眠质量.json")
OUTPUT = os.path.join(NOTES_DIR, "负性思维与反刍思维_睡眠质量.json")

print("="*80)
print("合并两个主题JSON文件")
print("="*80)

# 1. 加载两个文件
with open(FILE1, 'r', encoding='utf-8') as f:
    data1 = json.load(f)

with open(FILE2, 'r', encoding='utf-8') as f:
    data2 = json.load(f)

print(f"文件1: {data1['topic']} - {data1['total_count']} 篇")
print(f"文件2: {data2['topic']} - {data2['total_count']} 篇")

# 2. 合并论文（去重）
paper_map = OrderedDict()
for p in data1['papers']:
    pid = p['paperId']
    if pid not in paper_map:
        paper_map[pid] = p

for p in data2['papers']:
    pid = p['paperId']
    if pid not in paper_map:
        paper_map[pid] = p

merged_papers = list(paper_map.values())
print(f"\n合并后: {len(merged_papers)} 篇 (去重 {len(data1['papers'])+len(data2['papers'])-len(merged_papers)} 篇)")

# 3. 构建合并后的数据
total_citations = sum(p.get('citationCount', 0) for p in merged_papers)
merged_data = {
    "topic": "负性思维与反刍思维_睡眠质量",
    "total_count": len(merged_papers),
    "total_citations": total_citations,
    "papers": merged_papers
}

# 4. 保存
with open(OUTPUT, 'w', encoding='utf-8') as f:
    json.dump(merged_data, f, ensure_ascii=False, indent=2)

print(f"\n保存完成: {OUTPUT}")
print("="*80)
