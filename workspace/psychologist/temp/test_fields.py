
#!/usr/bin/env python3
"""
测试Semantic Scholar API支持哪些字段
"""

import os
import requests
import json

os.environ['SEMANTIC_SCHOLAR_API_KEY'] = 'KpNolzKwWrMhKMZW0XHq5jBhmBfOfNg3Q0sErPdi'

print("="*80)
print("测试Semantic Scholar API支持的字段")
print("="*80)

headers = {
    "Accept": "application/json",
    "x-api-key": os.environ['SEMANTIC_SCHOLAR_API_KEY']
}

paper_id = "03034d731473f19aa2edd8f40d3a979eb3c3082"
base_url = "https://api.semanticscholar.org/graph/v1/paper"

# 试试不同的字段组合
field_combinations = [
    "paperId,title,abstract,venue,year",
    "paperId,title,abstract,venue,year,journal",
    "paperId,title,abstract,venue,year,journal,authors",
    "paperId,title,abstract,venue,year,citationCount",
    "paperId,title,abstract,venue,year,referenceCount",
]

for i, fields in enumerate(field_combinations, 1):
    print(f"\n--- 测试{i} ---")
    print(f"字段: {fields}")
    
    url = f"{base_url}/{paper_id}"
    params = {"fields": fields}
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 成功！返回字段: {list(data.keys())}")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            break  # 找到一个可用的就停
        else:
            print(f"❌ 失败: {response.text}")
            
    except Exception as e:
        print(f"错误: {e}")

print(f"\n{'='*80}")
