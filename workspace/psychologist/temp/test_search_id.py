
#!/usr/bin/env python3
"""
先用搜索找到paperId，再试获取详情
"""

import os
import sys
import json
import requests

os.environ['SEMANTIC_SCHOLAR_API_KEY'] = 'KpNolzKwWrMhKMZW0XHq5jBhmBfOfNg3Q0sErPdi'

print("="*80)
print("测试：先搜索，再用搜索返回的paperId获取详情")
print("="*80)

headers = {
    "Accept": "application/json",
    "x-api-key": os.environ['SEMANTIC_SCHOLAR_API_KEY']
}

# 第一步：搜索
title = "Self-concept clarity lays the foundation for self-continuity"
search_url = "https://api.semanticscholar.org/graph/v1/paper/search"
search_params = {
    "query": title[:60],
    "limit": 3,
    "fields": "paperId,title"
}

print(f"\n1. 搜索标题: {title[:60]}")
response = requests.get(search_url, params=search_params, headers=headers, timeout=30)
print(f"   状态码: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    papers = data.get('data', [])
    print(f"   找到 {len(papers)} 篇")
    
    if papers:
        paper = papers[0]
        found_paper_id = paper.get('paperId')
        print(f"\n2. 第一篇paperId: {found_paper_id}")
        print(f"   标题: {paper.get('title')}")
        
        # 第二步：用这个paperId获取详情
        print(f"\n3. 用这个paperId获取详情...")
        detail_url = f"https://api.semanticscholar.org/graph/v1/paper/{found_paper_id}"
        detail_params = {
            "fields": "abstract,venue,year,journal,volume,issue,pages,doi,citationCount"
        }
        
        detail_response = requests.get(detail_url, params=detail_params, headers=headers, timeout=30)
        print(f"   详情状态码: {detail_response.status_code}")
        
        if detail_response.status_code == 200:
            detail_data = detail_response.json()
            print(f"\n   ✅ 成功获取详情！")
            print(f"   DOI: {detail_data.get('doi')}")
            print(f"   Journal: {detail_data.get('journal')}")
            if detail_data.get('journal'):
                j = detail_data['journal']
                print(f"   Volume: {j.get('volume')}")
                print(f"   Issue: {j.get('issue')}")
                print(f"   Pages: {j.get('pages')}")
        else:
            print(f"   详情失败: {detail_response.text}")

print(f"\n{'='*80}")
