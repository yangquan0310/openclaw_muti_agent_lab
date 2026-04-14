
#!/usr/bin/env python3
"""
测试老板修改后的Searcher.py
"""

import os
import sys
sys.path.insert(0, '/root/.openclaw/skills/knowledge-manager/knowledge-manager')

os.environ['SEMANTIC_SCHOLAR_API_KEY'] = 'KpNolzKwWrMhKMZW0XHq5jBhmBfOfNg3Q0sErPdi'

print("="*80)
print("测试老板修改后的Searcher.py")
print("="*80)

from Searcher import Searcher

# 1. 初始化
print("\n1. 初始化 Searcher...")
searcher = Searcher()
print("   ✅ 初始化成功！")

# 2. 测试单主题检索
print("\n2. 测试单主题检索...")
queries = {
    "自传体记忆": ["autobiographical memory"]
}

results = searcher.search_relevance(queries, limit=3)

print(f"\n   检索结果:")
for topic, papers in results.items():
    print(f"   主题: {topic}")
    print(f"   文献数: {len(papers)}")
    if papers:
        print(f"\n   第一篇文献:")
        print(f"     paperId: {papers[0].get('paperId')}")
        print(f"     title: {papers[0].get('title')}")
        print(f"     topic: {papers[0].get('topic')}")
        print(f"     labels: {papers[0].get('labels')}")

# 3. 测试get_paper_details
print("\n3. 测试get_paper_details...")
if papers:
    paper_id = papers[0].get('paperId')
    print(f"   paperId: {paper_id}")
    
    details = searcher.get_paper_details(paper_id)
    print(f"   结果: {len(details)} 篇")
    if details:
        print(f"   volume: {details[0].get('volume')}")
        print(f"   pages: {details[0].get('pages')}")
        print(f"   doi: {details[0].get('doi')}")

print("\n" + "="*80)
print("✅ 测试完成！")
print("="*80)
