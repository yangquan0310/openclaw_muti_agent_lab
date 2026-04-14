#!/usr/bin/env python3
"""
直接运行处理脚本 - 确保输出立即显示
"""

import sys
import os
import json

# 立即刷新输出
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

print("开始执行...")
sys.stdout.flush()

# 添加skill目录到路径
sys.path.insert(0, '/root/.openclaw/skills/knowledge-manager')

print("步骤1: 读取配置文件")
sys.stdout.flush()

# 1. 读取config.json
CONFIG_PATH = "/root/.openclaw/skills/knowledge-manager/config.json"
with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    config = json.load(f)

ark_config = config['llm']['providers']['ark']

print("步骤2: 获取API密钥")
sys.stdout.flush()

# 2. 显式获取API密钥
api_key_env = ark_config['api_key_env']
api_key = os.environ.get(api_key_env)

print(f"API密钥长度: {len(api_key) if api_key else 0}")
sys.stdout.flush()

if not api_key:
    print(f"错误: 环境变量 {api_key_env} 未设置!")
    sys.exit(1)

print("="*80)
print("用ark对7个笔记.json文件进行总结")
print("="*80)
print(f"\n使用配置: {ark_config['name']}")
print(f"  base_url: {ark_config['base_url']}")
print(f"  model: {ark_config['default_model']}")
print(f"  API key: {len(api_key)} chars")
sys.stdout.flush()

print("步骤3: 初始化Summarizer")
sys.stdout.flush()

# 3. 手动初始化Summarizer（显式传递参数）
from Summarizer import Summarizer

summarizer = Summarizer(
    api_key=api_key,
    base_url=ark_config['base_url'],
    model=ark_config['default_model']
)

print("Summarizer初始化完成")
sys.stdout.flush()

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

print("步骤4: 开始处理主题")
sys.stdout.flush()

# 逐个处理
total_papers = 0
total_updated = 0

for topic_idx, topic in enumerate(SEVEN_TOPICS, 1):
    safe_topic = topic.replace('/', '_').replace('\\', '_').replace(':', '_')
    input_path = os.path.join(NOTES_DIR, f"{safe_topic}.json")
    
    if not os.path.exists(input_path):
        print(f"\n[{topic_idx}/{len(SEVEN_TOPICS)}] 跳过: {topic}（文件不存在）")
        sys.stdout.flush()
        continue
    
    print(f"\n[{topic_idx}/{len(SEVEN_TOPICS)}] 处理: {topic}")
    sys.stdout.flush()
    
    # 读取主题文件
    with open(input_path, 'r', encoding='utf-8') as f:
        topic_data = json.load(f)
    
    papers = topic_data.get('papers', [])
    print(f"  论文数: {len(papers)}")
    sys.stdout.flush()
    total_papers += len(papers)
    
    # 逐个总结论文
    updated_count = 0
    for i, paper in enumerate(papers, 1):
        title = paper.get('title', '')
        abstract = paper.get('abstract', '')
        
        # 如果已经有notes且不是错误，跳过
        notes = paper.get('notes', {})
        if notes and 'error' not in notes:
            continue
        
        print(f"    处理第{i}/{len(papers)}篇: {title[:50]}...")
        sys.stdout.flush()
        
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
            print(f"      ✓ 成功! 类型: {result['type']}")
            sys.stdout.flush()
        except Exception as e:
            print(f"      ✗ 警告: 总结失败: {e}")
            sys.stdout.flush()
    
    total_updated += updated_count
    
    # 保存更新后的文件
    topic_data['papers'] = papers
    with open(input_path, 'w', encoding='utf-8') as f:
        json.dump(topic_data, f, ensure_ascii=False, indent=2)
    
    print(f"  ✓ 保存完成: {input_path}")
    print(f"  本主题更新: {updated_count}/{len(papers)}篇")
    sys.stdout.flush()

print("\n" + "="*80)
print("所有主题总结完成！")
print(f"总论文数: {total_papers}")
print(f"更新论文数: {total_updated}")
print("="*80)
sys.stdout.flush()
