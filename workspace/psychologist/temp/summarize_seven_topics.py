
#!/usr/bin/env python3
"""
用ark对7个笔记.json文件进行总结
"""

import sys
import os
import json

# 添加skill目录到路径
sys.path.insert(0, '/root/.openclaw/skills/knowledge-manager')

from Summarizer import Summarizer

NOTES_DIR = "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/笔记"

print("="*80)
print("用ark对7个笔记.json文件进行总结")
print("="*80)

# 定义7个主题
SEVEN_TOPICS = [
    "自传体记忆基础",
    "自传体记忆的自我参照编码",
    "自传体记忆功能",
    "自传体记忆的主动遗忘",
    "自传体记忆的系统性巩固",
    "数字化使用对自传体记忆的影响",
    "自传体记忆的生成性提取"
]

# 初始化Summarizer（用ark）
print("\n初始化Summarizer（ark）...")
summarizer = Summarizer()

# 逐个处理
for topic in SEVEN_TOPICS:
    safe_topic = topic.replace('/', '_').replace('\\', '_').replace(':', '_')
    input_path = os.path.join(NOTES_DIR, f"{safe_topic}.json")
    
    if not os.path.exists(input_path):
        print(f"\n跳过: {topic}（文件不存在）")
        continue
    
    print(f"\n处理: {topic}")
    
    # 读取主题文件
    with open(input_path, 'r', encoding='utf-8') as f:
        topic_data = json.load(f)
    
    papers = topic_data.get('papers', [])
    print(f"  论文数: {len(papers)}")
    
    # 逐个总结论文
    updated_count = 0
    for i, paper in enumerate(papers, 1):
        title = paper.get('title', '')
        abstract = paper.get('abstract', '')
        
        # 如果已经有notes，跳过
        if paper.get('notes'):
            continue
        
        # 调用Summarizer总结单个论文
        try:
            result = summarizer._summarize_single(title, abstract)
            paper['labels'] = {
                "type": result['type'],
                "importance": paper.get('labels', {}).get('importance', summarizer._calc_importance(paper.get('citationCount', 0))),
                "JCR": paper.get('labels', {}).get('JCR', '')
            }
            paper['notes'] = result['notes']
            updated_count += 1
        except Exception as e:
            print(f"    警告: 第{i}篇总结失败: {e}")
        
        if i % 5 == 0 or i == len(papers):
            print(f"    进度: {i}/{len(papers)} ({i/len(papers)*100:.1f}%), 已更新: {updated_count}")
    
    # 保存更新后的文件
    topic_data['papers'] = papers
    with open(input_path, 'w', encoding='utf-8') as f:
        json.dump(topic_data, f, ensure_ascii=False, indent=2)
    
    print(f"  保存完成: {input_path}")

print("\n" + "="*80)
print("所有主题总结完成！")
print("="*80)
