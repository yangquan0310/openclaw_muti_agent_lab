#!/usr/bin/env python3
"""
处理单个主题文件
"""

import sys
import os
import json

# 添加skill目录到路径
sys.path.insert(0, '/root/.openclaw/skills/knowledge-manager')

# 1. 读取config.json
CONFIG_PATH = "/root/.openclaw/skills/knowledge-manager/config.json"
with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    config = json.load(f)

ark_config = config['llm']['providers']['ark']

# 2. 显式获取API密钥
api_key_env = ark_config['api_key_env']
api_key = os.environ.get(api_key_env)

if not api_key:
    print(f"错误: 环境变量 {api_key_env} 未设置!")
    sys.exit(1)

# 3. 手动初始化Summarizer
from Summarizer import Summarizer

summarizer = Summarizer(
    api_key=api_key,
    base_url=ark_config['base_url'],
    model=ark_config['default_model']
)

# 4. 处理单个主题
if len(sys.argv) < 2:
    print("用法: python process_single_topic.py <主题文件名>")
    sys.exit(1)

topic_file = sys.argv[1]
NOTES_DIR = "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/笔记"
input_path = os.path.join(NOTES_DIR, topic_file)

if not os.path.exists(input_path):
    print(f"错误: 文件不存在: {input_path}")
    sys.exit(1)

print(f"处理文件: {topic_file}")

# 读取主题文件
with open(input_path, 'r', encoding='utf-8') as f:
    topic_data = json.load(f)

papers = topic_data.get('papers', [])
print(f"论文数: {len(papers)}")

# 逐个总结论文
updated_count = 0
for i, paper in enumerate(papers, 1):
    title = paper.get('title', '')
    abstract = paper.get('abstract', '')
    
    # 如果已经有notes且不是错误，跳过
    notes = paper.get('notes', {})
    if notes and 'error' not in notes:
        continue
    
    print(f"[{i}/{len(papers)}] 处理: {title[:60]}...")
    
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
        print(f"  ✓ 成功: {result['type']}")
    except Exception as e:
        print(f"  ✗ 失败: {e}")

# 保存更新后的文件
topic_data['papers'] = papers
with open(input_path, 'w', encoding='utf-8') as f:
    json.dump(topic_data, f, ensure_ascii=False, indent=2)

print(f"\n完成! 更新了 {updated_count}/{len(papers)} 篇论文")
print(f"保存到: {input_path}")
