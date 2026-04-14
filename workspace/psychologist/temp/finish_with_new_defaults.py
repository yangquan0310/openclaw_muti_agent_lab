#!/usr/bin/env python3
"""
用新的默认配置（tencent LKE + 会话模式）完成剩下的55篇论文
"""

import sys
import os
import json

# 添加skill目录到路径
sys.path.insert(0, '/root/.openclaw/skills/knowledge-manager')

print("="*80)
print("用新的默认配置（tencent LKE + 会话模式）完成剩下的55篇论文")
print("="*80)

# 1. 初始化Summarizer（使用新的默认配置）
from Summarizer import Summarizer

summarizer = Summarizer()  # 使用默认配置：tencent LKE + 会话模式

print(f"\n使用配置:")
print(f"  base_url: {summarizer.base_url}")
print(f"  model: {summarizer.model}")
print(f"  会话模式: {'开启' if summarizer.use_conversation else '关闭'}")

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

NOTES_DIR = "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/笔记"

# 逐个处理
total_updated = 0

for topic_idx, topic in enumerate(SEVEN_TOPICS, 1):
    safe_topic = topic.replace('/', '_').replace('\\', '_').replace(':', '_')
    input_path = os.path.join(NOTES_DIR, f"{safe_topic}.json")
    
    if not os.path.exists(input_path):
        print(f"\n[{topic_idx}/{len(SEVEN_TOPICS)}] 跳过: {topic}（文件不存在）")
        continue
    
    print(f"\n[{topic_idx}/{len(SEVEN_TOPICS)}] 处理: {topic}")
    
    # 读取主题文件
    with open(input_path, 'r', encoding='utf-8') as f:
        topic_data = json.load(f)
    
    papers = topic_data.get('papers', [])
    print(f"  论文数: {len(papers)}")
    
    # 只处理有错误或待分类的论文
    updated_count = 0
    for i, paper in enumerate(papers, 1):
        title = paper.get('title', '')
        abstract = paper.get('abstract', '')
        
        # 只处理有错误或待分类的论文
        notes = paper.get('notes', {})
        labels = paper.get('labels', {})
        if notes and 'error' not in notes and labels.get('type') != '📋待分类':
            continue
        
        print(f"    重新总结第{i}/{len(papers)}篇: {title[:50]}...")
        
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
            total_updated += 1
            print(f"      ✓ 成功! 类型: {result['type']}")
        except Exception as e:
            print(f"      ✗ 警告: 总结失败: {e}")
    
    # 保存更新后的文件
    if updated_count > 0:
        topic_data['papers'] = papers
        with open(input_path, 'w', encoding='utf-8') as f:
            json.dump(topic_data, f, ensure_ascii=False, indent=2)
        
        print(f"  ✓ 保存完成: {input_path}")
        print(f"  本主题更新: {updated_count}篇")

print("\n" + "="*80)
print("所有主题完成！")
print(f"总共更新: {total_updated}篇")
print("="*80)
