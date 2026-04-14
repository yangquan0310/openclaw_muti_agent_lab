
#!/usr/bin/env python3
"""
按主题提取知识库论文到笔记文件夹
"""

import json
import os
from collections import defaultdict

KB_PATH = "/root/实验室仓库/项目文件/学生论文修改/知识库/index.json"
NOTES_DIR = "/root/实验室仓库/项目文件/学生论文修改/知识库/笔记"

print("="*80)
print("按主题提取知识库论文")
print("="*80)

# 1. 确保笔记目录存在
os.makedirs(NOTES_DIR, exist_ok=True)

# 2. 加载知识库
with open(KB_PATH, 'r', encoding='utf-8') as f:
    kb = json.load(f)

papers = kb['papers']
print(f"总论文数: {len(papers)}")

# 3. 按主题分组
topic_map = defaultdict(list)

for p in papers:
    topics = p.get('topic', [])
    if not topics:
        continue
    for topic in topics:
        topic_map[topic].append(p)

print(f"主题数: {len(topic_map)}")

# 4. 为每个主题创建文件
for topic, topic_papers in topic_map.items():
    # 清理文件名中的特殊字符
    safe_topic = topic.replace('/', '_').replace('\\', '_').replace(':', '_')
    output_path = os.path.join(NOTES_DIR, f"{safe_topic}.json")
    
    topic_data = {
        "topic": topic,
        "total_count": len(topic_papers),
        "total_citations": sum(p.get('citationCount', 0) for p in topic_papers),
        "papers": topic_papers
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(topic_data, f, ensure_ascii=False, indent=2)
    
    print(f"  {topic}: {len(topic_papers)} 篇 -&gt; {safe_topic}.json")

print("\n" + "="*80)
print("提取完成！")
print("="*80)
print(f"输出目录: {NOTES_DIR}")
print("="*80)
