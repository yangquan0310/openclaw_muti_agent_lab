
#!/usr/bin/env python3
"""
检查7个主题文件的总结进度
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
print("检查7个主题文件的总结进度")
print("="*80)

total_papers = 0
total_summarized = 0
total_with_error = 0

for topic in SEVEN_TOPICS:
    safe_topic = topic.replace('/', '_').replace('\\', '_').replace(':', '_')
    input_path = os.path.join(NOTES_DIR, f"{safe_topic}.json")
    
    if not os.path.exists(input_path):
        print(f"\n{topic}: 文件不存在")
        continue
    
    with open(input_path, 'r', encoding='utf-8') as f:
        topic_data = json.load(f)
    
    papers = topic_data.get('papers', [])
    summarized = 0
    with_error = 0
    
    for p in papers:
        notes = p.get('notes', {})
        if notes:
            if 'error' in notes:
                with_error += 1
            else:
                summarized += 1
    
    total_papers += len(papers)
    total_summarized += summarized
    total_with_error += with_error
    
    print(f"\n{topic}")
    print(f"  总论文数: {len(papers)}")
    print(f"  已总结: {summarized}")
    print(f"  有错误: {with_error}")
    print(f"  进度: {summarized/(len(papers) if len(papers) &gt; 0 else 1)*100:.1f}%")

print("\n" + "="*80)
print("总计")
print(f"  总论文数: {total_papers}")
print(f"  已总结: {total_summarized}")
print(f"  有错误: {total_with_error}")
print(f"  总进度: {total_summarized/(total_papers if total_papers &gt; 0 else 1)*100:.1f}%")
print("="*80)
