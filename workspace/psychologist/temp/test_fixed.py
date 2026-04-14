
#!/usr/bin/env python3
"""
测试修复后的AcademicSearchSummarizer
"""

import os
import sys
sys.path.insert(0, '/root/.openclaw/skills/knowledge-manager')

from AcademicSearchSummarizer import AcademicSearchSummarizer

# 设置环境变量
os.environ['SEMANTIC_SCHOLAR_API_KEY'] = 'KpNolzKwWrMhKMZW0XHq5jBhmBfOfNg3Q0sErPdi'

print("="*80)
print("测试修复后的AcademicSearchSummarizer")
print("="*80)

# 初始化
ass = AcademicSearchSummarizer()

# 测试用的知识库
kb_path = "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/index.json"

# 先加载知识库看看
print("\n--- 加载知识库 ---")
ass.load_knowledge_base(kb_path)
print(f"  加载了 {len(ass.all_papers)} 篇文献")

# 测试第一篇文献
paper = ass.all_papers[0]
print(f"\n--- 测试第一篇文献 ---")
print(f"  标题: {paper.get('title')}")
print(f"  paperId: {paper.get('paperId')}")

# 测试修复后的fetch_full_metadata
print(f"\n--- 测试修复后的fetch_full_metadata (只试1篇) ---")

# 只测试第一篇
import time
import requests

paper_id = paper.get('paperId')
searcher = ass.searcher

# 调用修复后的_fetch_paper_details
print(f"  调用_fetch_paper_details({paper_id})...")
result = searcher._fetch_paper_details(paper_id)

if result:
    print(f"  ✅ 成功获取数据！")
    print(f"  DOI: {result.get('doi')}")
    print(f"  Volume: {result.get('volume')}")
    print(f"  Issue: {result.get('issue')}")
    print(f"  Pages: {result.get('pages')}")
else:
    print(f"  ❌ 获取失败")

print(f"\n{'='*80}")
