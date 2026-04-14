
#!/usr/bin/env python3
"""
详细调试脚本：一步步测试每个环节
"""

import os
import sys
import json
import time
import requests

# 设置环境变量
os.environ['SEMANTIC_SCHOLAR_API_KEY'] = 'KpNolzKwWrMhKMZW0XHq5jBhmBfOfNg3Q0sErPdi'

print("="*80)
print("调试脚本：逐步测试每个环节")
print("="*80)

# 测试1：读取一篇文献看看
print("\n--- 测试1：读取知识库中的一篇文献 ---")
kb_path = "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/index.json"
with open(kb_path, 'r', encoding='utf-8') as f:
    kb = json.load(f)
paper = kb['papers'][0]
print(f"标题: {paper.get('title')}")
print(f"paperId: {paper.get('paperId')}")
print(f"现有DOI: '{paper.get('doi', '')}'")
print(f"现有volume: '{paper.get('volume', '')}'")
print(f"现有issue: '{paper.get('issue', '')}'")
print(f"现有pages: '{paper.get('pages', '')}'")

# 测试2：搜索这个标题
print("\n--- 测试2：用标题搜索 ---")
title = paper.get('title', '')
search_query = title[:60] if len(title) > 60 else title
print(f"搜索查询: {search_query}")

BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
headers = {
    "Accept": "application/json",
    "x-api-key": os.environ['SEMANTIC_SCHOLAR_API_KEY']
}

params = {
    "query": search_query,
    "limit": 3,
    "fields": "paperId,title,authors,year,venue,abstract"
}

print(f"\n请求: {BASE_URL}")
response = requests.get(BASE_URL, params=params, headers=headers, timeout=30)
print(f"状态码: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    papers_found = data.get('data', [])
    print(f"找到 {len(papers_found)} 篇文献")
    
    for i, p in enumerate(papers_found, 1):
        print(f"\n  结果{i}:")
        print(f"    paperId: {p.get('paperId')}")
        print(f"    标题: {p.get('title')}")
        
        # 测试3：尝试获取这篇文献的详情
        if i == 1:
            print(f"\n--- 测试3：获取这篇文献的详情 ---")
            paper_id = p.get('paperId')
            detail_url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}"
            detail_params = {
                "fields": "abstract,venue,year,journal,volume,issue,pages,doi,citationCount"
            }
            print(f"详情URL: {detail_url}")
            
            detail_response = requests.get(detail_url, params=detail_params, headers=headers, timeout=30)
            print(f"详情状态码: {detail_response.status_code}")
            
            if detail_response.status_code == 200:
                detail_data = detail_response.json()
                print(f"\n详情数据:")
                print(json.dumps(detail_data, indent=2, ensure_ascii=False))
                
                # 测试4：看看能不能提取到需要的字段
                print(f"\n--- 测试4：提取字段 ---")
                print(f"  DOI: {detail_data.get('doi')}")
                print(f"  journal: {detail_data.get('journal')}")
                if detail_data.get('journal'):
                    journal = detail_data['journal']
                    print(f"    volume: {journal.get('volume')}")
                    print(f"    issue: {journal.get('issue')}")
                    print(f"    pages: {journal.get('pages')}")
            else:
                print(f"详情失败: {detail_response.text}")
else:
    print(f"搜索失败: {response.text}")

print(f"\n{'='*80}")
