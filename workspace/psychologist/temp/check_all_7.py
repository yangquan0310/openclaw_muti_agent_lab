
#!/usr/bin/env python3
"""
检查所有7个主题文件的错误情况
"""

import json
import os

NOTES_DIR = "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/笔记/"

topic_files = [
    "自传体记忆基础.json",
    "自传体记忆的自我参照编码.json",
    "自传体记忆功能.json",
    "自传体记忆的主动遗忘.json",
    "自传体记忆的系统性巩固.json",
    "数字化使用对自传体记忆的影响.json",
    "自传体记忆的生成性提取.json",
]

print("="*80)
print("检查所有7个主题文件")
print("="*80)

total_papers = 0
total_success = 0
total_errors = 0

for topic_file in topic_files:
    kb_path = os.path.join(NOTES_DIR, topic_file)
    if not os.path.exists(kb_path):
        print(f"\n⚠️ 文件不存在: {kb_path}")
        continue
    
    with open(kb_path, 'r', encoding='utf-8') as f:
        kb = json.load(f)
    
    papers = kb.get('papers', [])
    
    error_count = 0
    success_count = 0
    
    for p in papers:
        notes = p.get('notes', {})
        if 'error' in notes:
            error_count += 1
        else:
            success_count += 1
    
    total_papers += len(papers)
    total_success += success_count
    total_errors += error_count
    
    print(f"\n{topic_file}")
    print(f"  总计: {len(papers)} 篇")
    print(f"  ✅ 成功: {success_count} 篇")
    print(f"  ❌ 错误: {error_count} 篇")

print("\n" + "="*80)
print("总计")
print("="*80)
print(f"  总计: {total_papers} 篇")
print(f"  ✅ 成功: {total_success} 篇")
print(f"  ❌ 错误: {total_errors} 篇")
print("="*80)
