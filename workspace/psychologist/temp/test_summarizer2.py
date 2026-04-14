
#!/usr/bin/env python3
"""
测试老板修改后的Summarizer.py（用正确的API key）
"""

import os
import sys
sys.path.insert(0, '/root/.openclaw/skills/knowledge-manager/knowledge-manager')

# 直接从.env文件读取API key
with open('/root/.openclaw/.env', 'r') as f:
    for line in f:
        if line.strip() and not line.startswith('#'):
            key, value = line.strip().split('=', 1)
            os.environ[key] = value

print("="*80)
print("测试老板修改后的Summarizer.py（用正确的API key）")
print("="*80)

from Summarizer import Summarizer
summarizer = Summarizer()

kb = summarizer.summarize(kb_path="test_summarizer_input.json")

print(f"\n✅ summarize() 完成！")
print(f"   论文数: {len(kb['papers'])}")

for i, paper in enumerate(kb['papers']):
    print(f"\n   论文 {i+1}:")
    print(f"     title: {paper.get('title')}")
    print(f"     labels: {paper.get('labels')}")
    print(f"     notes: {paper.get('notes')}")

print("\n" + "="*80)
print("🎉 Summarizer测试成功！")
print("="*80)
