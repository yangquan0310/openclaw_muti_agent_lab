
#!/usr/bin/env python3
"""
简单检查7个主题文件
"""

import json
import os

NOTES_DIR = "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/笔记"

SEVEN_TOPICS = [
    "自传体记忆基础",
    "自传体记忆的自我参照编码",
    "自传体记忆功能",
    "自传体记忆的主动遗忘",
    "自传体记忆的系统性巩固",
    "数字化使用对自传体记忆的影响",
    "自传体记忆的生成性提取"
]

print("="*80)
print("检查7个主题文件")
print("="*80)

total_papers = 0
total_ok = 0
total_err = 0
total_no = 0

for topic in SEVEN_TOPICS:
    safe_topic = topic.replace('/', '_').replace('\\', '_').replace(':', '_')
    input_path = os.path.join(NOTES_DIR, safe_topic + ".json")
    
    if not os.path.exists(input_path):
        print("\n" + topic + ": 文件不存在")
        continue
    
    with open(input_path, 'r', encoding='utf-8') as f:
        topic_data = json.load(f)
    
    papers = topic_data.get('papers', [])
    ok = 0
    err = 0
    no = 0
    
    for p in papers:
        notes = p.get('notes', {})
        if not notes:
            no += 1
        elif 'error' in notes:
            err += 1
        else:
            ok += 1
    
    total_papers += len(papers)
    total_ok += ok
    total_err += err
    total_no += no
    
    print("\n" + topic)
    print("  总论文数: " + str(len(papers)))
    print("  ✅ 已总结: " + str(ok))
    print("  ❌ 有错误: " + str(err))
    print("  ⏳ 未开始: " + str(no))

print("\n" + "="*80)
print("总计")
print("  总论文数: " + str(total_papers))
print("  ✅ 已总结: " + str(total_ok))
print("  ❌ 有错误: " + str(total_err))
print("  ⏳ 未开始: " + str(total_no))
print("="*80)
