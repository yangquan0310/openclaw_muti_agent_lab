
#!/usr/bin/env python3
"""
测试不同的API URL格式
"""

import os
import requests
import json

# 设置环境变量
os.environ['SEMANTIC_SCHOLAR_API_KEY'] = 'KpNolzKwWrMhKMZW0XHq5jBhmBfOfNg3Q0sErPdi'

test_paper_id = "03034d731473f19aa2edd8f40d3a979eb3c3082"

print("="*80)
print("测试不同的API URL格式")
print("="*80)

headers = {
    "Accept": "application/json",
    "x-api-key": os.environ['SEMANTIC_SCHOLAR_API_KEY']
}

# 测试几种不同的URL格式
urls_to_test = [
    f"https://api.semanticscholar.org/graph/v1/paper/{test_paper_id}",
    f"https://api.semanticscholar.org/v1/paper/{test_paper_id}",
    f"https://api.semanticscholar.org/graph/v1/paper/{test_paper_id}?fields=abstract,venue,year,journal,doi"
]

for i, url in enumerate(urls_to_test, 1):
    print(f"\n--- 测试 {i} ---")
    print(f"URL: {url}")
    
    try:
        if '?' in url:
            response = requests.get(url, headers=headers)
        else:
            params = {
                "fields": "abstract,venue,year,journal,doi"
            }
            response = requests.get(url, params=params, headers=headers)
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"成功！返回数据:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(f"失败: {response.text}")
            
    except Exception as e:
        print(f"错误: {e}")

print(f"\n{'='*80}")
