
#!/usr/bin/env python3
"""
更新数字化存储与自传体记忆知识库（只更新元数据，不添加新文献）
"""

import sys
sys.path.insert(0, '/root/.openclaw/skills/knowledge-manager')

from Searcher import Searcher

KB_PATH = "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/index.json"

print("="*80)
print("更新数字化存储与自传体记忆知识库（只更新元数据）")
print("="*80)

# 备份
import shutil
import os
if os.path.exists(KB_PATH):
    backup_path = KB_PATH + ".backup_20260414"
    shutil.copy2(KB_PATH, backup_path)
    print(f"已备份现有知识库到: {backup_path}")

# 更新元数据
searcher = Searcher()
kb = searcher.update(kb_path=KB_PATH)

print("\n" + "="*80)
print("知识库元数据更新完成！")
print("="*80)
print(f"论文总数: {len(kb['papers'])}")
print(f"DOI非空: {sum(1 for p in kb['papers'] if p.get('doi'))}")
print(f"总引用量: {kb['statistics']['total_citations']}")
print(f"奠基文献: {kb['statistics']['foundation_count']}")
print(f"重要文献: {kb['statistics']['important_count']}")
print(f"一般文献: {kb['statistics']['general_count']}")
print("="*80)
