
#!/usr/bin/env python3
"""
更新学生论文修改项目知识库
"""

import sys
import os

# 添加skill目录到路径
sys.path.insert(0, '/root/.openclaw/skills/knowledge-manager')

from Searcher import Searcher
from Summarizer import Summarizer

# 知识库路径
KB_PATH = "/root/实验室仓库/项目文件/学生论文修改/知识库/index.json"

print("="*80)
print("更新学生论文修改项目知识库")
print("="*80)

# 1. 先备份现有知识库
import shutil
if os.path.exists(KB_PATH):
    backup_path = KB_PATH + ".backup_20260414"
    shutil.copy2(KB_PATH, backup_path)
    print(f"已备份现有知识库到: {backup_path}")

# 2. 确定研究主题和检索条件
queries = {
    "错失焦虑与学业拖延": [
        {
            "query": "fear of missing out academic procrastination",
            "limit": 30,
            "minCitationCount": 10
        },
        {
            "query": "rumination academic procrastination mediation",
            "limit": 25,
            "year": "2018-2025"
        }
    ],
    "课堂拍照行为": [
        {
            "query": "photo taking in class learning cognitive load",
            "limit": 30,
            "minCitationCount": 5
        },
        {
            "query": "photographing learning effect memory",
            "limit": 25,
            "year": "2015-2025"
        }
    ],
    "反刍思维与睡眠质量": [
        {
            "query": "rumination sleep quality anxiety",
            "limit": 30,
            "minCitationCount": 20
        },
        {
            "query": "repetitive negative thinking sleep",
            "limit": 25,
            "year": "2018-2025"
        }
    ],
    "消费频率与主观幸福感": [
        {
            "query": "consumption frequency subjective well-being",
            "limit": 25,
            "minCitationCount": 10
        },
        {
            "query": "experience sampling well-being college students",
            "limit": 20,
            "year": "2015-2025"
        }
    ]
}

# 3. 执行检索
searcher = Searcher()
kb = searcher.search(
    queries,
    kb_path=KB_PATH,
    fields_of_study="Psychology"
)

print(f"\n检索完成！知识库现在有 {len(kb['papers'])} 篇论文")

# 4. 更新元数据
print("\n" + "="*80)
print("更新知识库元数据")
print("="*80)
kb = searcher.update(kb_path=KB_PATH)
print("元数据更新完成！")

print("\n" + "="*80)
print("知识库更新完成！")
print("="*80)
print(f"论文总数: {len(kb['papers'])}")
print(f"总引用量: {kb['statistics']['total_citations']}")
print(f"奠基文献: {kb['statistics']['foundation_count']}")
print(f"重要文献: {kb['statistics']['important_count']}")
print(f"一般文献: {kb['statistics']['general_count']}")
print("="*80)
