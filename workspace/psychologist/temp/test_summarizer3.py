
#!/usr/bin/env python3
"""
测试老板修改后的Summarizer.py（直接用正确的ARK API key）
"""

import os
import sys
sys.path.insert(0, '/root/.openclaw/skills/knowledge-manager/knowledge-manager')

# 直接设置正确的API key
os.environ['ARK_API_KEY'] = 'abf6fd55-78bf-4f84-b059-28ebbeb4ff63'

print("="*80)
print("测试老板修改后的Summarizer.py（用正确的ARK API key）")
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
