
#!/usr/bin/env python3
"""
测试正确的Semantic Scholar API端点
"""

import os
import requests
import json

os.environ['SEMANTIC_SCHOLAR_API_KEY'] = 'KpNolzKwWrMhKMZW0XHq5jBhmBfOfNg3Q0sErPdi'

print("="*80)
print("测试正确的Semantic Scholar API")
print("="*80)

headers = {
    "Accept": "application/json",
    "x-api-key": os.environ['SEMANTIC_SCHOLAR_API_KEY']
}

# 先搜索找一篇肯定存在的文献
print("\n1. 先用搜索找一篇文献...")
search_url = "https://api.semanticscholar.org/graph/v1/paper/search"
search_params = {
    "query": "autobiographical memory",
    "limit": 1,
    "fields": "paperId,title"
}

response = requests.get(search_url, params=search_params, headers=headers, timeout=30)
print(f"   搜索状态码: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    papers = data.get('data', [])
    
    if papers:
        paper = papers[0]
        paper_id = paper.get('paperId')
        print(f"\n2. 找到文献:")
        print(f"   paperId: {paper_id}")
        print(f"   标题: {paper.get('title')}")
        
        # 现在用正确的字段获取这篇文献
        print(f"\n3. 用正确的字段获取详情...")
        detail_url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}"
        
        # 根据老板给的响应示例，请求这些字段
        detail_params = {
            "fields": "paperId,title,abstract,venue,year,journal,publicationVenue,citationCount,authors"
        }
        
        detail_response = requests.get(detail_url, params=detail_params, headers=headers, timeout=30)
        print(f"   详情状态码: {detail_response.status_code}")
        
        if detail_response.status_code == 200:
            detail_data = detail_response.json()
            print(f"\n4. ✅ 成功获取详情！")
            print(f"\n完整响应:")
            print(json.dumps(detail_data, indent=2, ensure_ascii=False))
            
            print(f"\n5. 提取元数据:")
            print(f"   title: {detail_data.get('title')}")
            print(f"   venue: {detail_data.get('venue')}")
            print(f"   year: {detail_data.get('year')}")
            
            if detail_data.get('journal'):
                journal = detail_data['journal']
                print(f"   journal:")
                print(f"     name: {journal.get('name')}")
                print(f"     volume: {journal.get('volume')}")
                print(f"     pages: {journal.get('pages')}")
            
            if detail_data.get('publicationVenue'):
                pub_venue = detail_data['publicationVenue']
                print(f"   publicationVenue: {pub_venue.get('name')}")
        else:
            print(f"   详情失败: {detail_response.text}")

print(f"\n{'='*80}")
