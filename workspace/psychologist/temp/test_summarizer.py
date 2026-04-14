
#!/usr/bin/env python3
"""
测试老板修改后的Summarizer.py
"""

import os
import sys
sys.path.insert(0, '/root/.openclaw/skills/knowledge-manager/knowledge-manager')

# 设置API key
os.environ['ARK_API_KEY'] = '26721730-31fa-4cde-be04-14782c98a485'
os.environ['SEMANTIC_SCHOLAR_API_KEY'] = 'KpNolzKwWrMhKMZW0XHq5jBhmBfOfNg3Q0sErPdi'

print("="*80)
print("测试老板修改后的Summarizer.py")
print("="*80)

# 先用Searcher生成一个测试知识库
from Searcher import Searcher
searcher = Searcher()

queries = {
    "自传体记忆": ["autobiographical memory"]
}
searcher.search(queries, kb_path="test_summarizer_input.json", limit=2)

print("\n" + "="*80)
print("测试Summarizer.summarize()")
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
