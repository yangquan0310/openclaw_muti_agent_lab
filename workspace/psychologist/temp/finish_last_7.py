
#!/usr/bin/env python3
"""
重新总结最后7篇有错误的论文
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

NOTES_DIR = "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/笔记/"

# 需要重新总结的文件和错误论文
files_with_errors = [
    ("自传体记忆基础.json", 4),
    ("自传体记忆功能.json", 2),
    ("自传体记忆的生成性提取.json", 1),
]

print("="*80)
print("重新总结最后7篇有错误的论文")
print("="*80)

total_fixed = 0

for topic_file, _ in files_with_errors:
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
        errors = len(papers) - success
        total_fixed += (errors == 0)
        print(f"   总计: {len(papers)} 篇, 成功: {success} 篇, 错误: {errors} 篇")
        
    except Exception as e:
        print(f"❌ 失败: {topic_file}")
        print(f"   错误: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "="*80)
print("全部完成")
print("="*80)
