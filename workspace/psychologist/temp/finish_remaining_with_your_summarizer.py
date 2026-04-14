
#!/usr/bin/env python3
"""
用老板修改后的Summarizer.py重新总结剩余论文
"""

import sys
import os
import json

# 直接读取.env文件
dotenv_path = "/root/.openclaw/.env"
if os.path.exists(dotenv_path):
    with open(dotenv_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value

# 添加skill目录到路径
sys.path.insert(0, '/root/.openclaw/skills/knowledge-manager')

from Summarizer import Summarizer

# 7个主题文件路径
NOTES_DIR = "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/笔记/"

# 需要重新总结的主题文件（之前失败的）
topic_files = [
    "自传体记忆的系统性巩固.json",
    "数字化使用对自传体记忆的影响.json",
]

print("="*80)
print("重新总结剩余论文")
print("="*80)

for topic_file in topic_files:
    kb_path = os.path.join(NOTES_DIR, topic_file)
    if not os.path.exists(kb_path):
        print(f"\n⚠️ 文件不存在: {kb_path}")
        continue
    
    print(f"\n处理: {topic_file}")
    print("-"*80)
    
    try:
        summarizer = Summarizer()
        kb = summarizer.summarize(kb_path=kb_path, progress_interval=5)
        print(f"✅ 完成: {topic_file}")
        
        # 统计结果
        papers = kb.get('papers', [])
        success = sum(1 for p in papers if p.get('notes') and 'error' not in p.get('notes', {}))
        print(f"   总计: {len(papers)} 篇, 成功: {success} 篇")
        
    except Exception as e:
        print(f"❌ 失败: {topic_file}")
        print(f"   错误: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "="*80)
print("全部完成")
print("="*80)
