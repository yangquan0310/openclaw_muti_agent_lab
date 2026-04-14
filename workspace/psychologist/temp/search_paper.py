
#!/usr/bin/env python3
"""
用标题搜索文献来验证paperId
"""

import os
import requests
import json

# 设置环境变量
os.environ['SEMANTIC_SCHOLAR_API_KEY'] = 'KpNolzKwWrMhKMZW0XHq5jBhmBfOfNg3Q0sErPdi'

# 测试用的标题
test_title = "Self-concept clarity lays the foundation for self-continuity: The restorative function of autobiographical memory."

print("="*80)
print("通过标题搜索文献")
print("="*80)

# 构建搜索请求
BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
params = {
    "query": test_title[:50],  # 用前50个字符搜索
    "limit": 5,
    "fields": "paperId,title,authors,year,venue,abstract"
}

headers = {
    "Accept": "application/json",
    "x-api-key": os.environ['SEMANTIC_SCHOLAR_API_KEY']
}

print(f"\n搜索标题: {test_title}")
print(f"\n请求URL: {BASE_URL}")

try:
    response = requests.get(BASE_URL, params=params, headers=headers)
    print(f"响应状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        papers = data.get('data', [])
        
        print(f"\n找到 {len(papers)} 篇文献:")
        
        for i, paper in enumerate(papers, 1):
            print(f"\n--- 结果 {i} ---")
            print(f"  paperId: {paper.get('paperId')}")
            print(f"  标题: {paper.get('title')}")
            print(f"  年份: {paper.get('year')}")
            print(f"  期刊: {paper.get('venue')}")
            print(f"  DOI: {paper.get('doi')}")
            print(f"  Journal: {paper.get('journal')}")
            print(f"  Volume: {paper.get('volume')}")
            print(f"  Issue: {paper.get('issue')}")
            print(f"  Pages: {paper.get('pages')}")
    else:
        print(f"\n响应内容: {response.text}")
        
except Exception as e:
    print(f"\n错误: {e}")
    import traceback
    traceback.print_exc()

print(f"\n{'='*80}")
