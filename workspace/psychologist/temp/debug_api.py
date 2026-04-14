
#!/usr/bin/env python3
"""
调试Semantic Scholar API返回数据
"""

import os
import requests
import json

# 设置环境变量
os.environ['SEMANTIC_SCHOLAR_API_KEY'] = 'KpNolzKwWrMhKMZW0XHq5jBhmBfOfNg3Q0sErPdi'

# 测试用的paperId（从数字化存储与自传体记忆知识库取第一篇）
test_paper_id = "03034d731473f19aa2edd8f40d3a979eb3c3082"

print("="*80)
print("调试 Semantic Scholar API")
print("="*80)

# 构建请求
BASE_URL = "https://api.semanticscholar.org/graph/v1/paper"
url = f"{BASE_URL}/{test_paper_id}"
params = {
    "fields": "abstract,venue,year,journal,volume,issue,pages,doi,referenceCount,citationCount,influentialCitationCount,isOpenAccess,openAccessPdf,fieldsOfStudy,authors"
}

headers = {
    "Accept": "application/json",
    "x-api-key": os.environ['SEMANTIC_SCHOLAR_API_KEY']
}

print(f"\n请求URL: {url}")
print(f"请求参数: {params}")

try:
    response = requests.get(url, params=params, headers=headers)
    print(f"\n响应状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n完整响应数据:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        print(f"\n\n字段分析:")
        print(f"  - abstract: {'✓' if 'abstract' in data else '✗'}")
        print(f"  - venue: {'✓' if 'venue' in data else '✗'}")
        print(f"  - year: {'✓' if 'year' in data else '✗'}")
        print(f"  - journal: {'✓' if 'journal' in data else '✗'}")
        if 'journal' in data:
            print(f"    journal字段内容: {data['journal']}")
        print(f"  - volume: {'✓' if 'volume' in data else '✗'}")
        print(f"  - issue: {'✓' if 'issue' in data else '✗'}")
        print(f"  - pages: {'✓' if 'pages' in data else '✗'}")
        print(f"  - doi: {'✓' if 'doi' in data else '✗'}")
    else:
        print(f"\n响应内容: {response.text}")
        
except Exception as e:
    print(f"\n错误: {e}")
    import traceback
    traceback.print_exc()

print(f"\n{'='*80}")
