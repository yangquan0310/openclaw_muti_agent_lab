
#!/usr/bin/env python3
"""
测试请求journal.volume等字段，看返回的JSON是不是平的
"""

import os
import requests
import json
import time

os.environ['SEMANTIC_SCHOLAR_API_KEY'] = 'KpNolzKwWrMhKMZW0XHq5jBhmBfOfNg3Q0sErPdi'

print("="*80)
print("测试：请求journal.volume等字段，看返回JSON结构")
print("="*80)

test_paper_id = "13241a844c714549c173e239714ae020386172e3"

headers = {
    "Accept": "application/json",
    "x-api-key": os.environ['SEMANTIC_SCHOLAR_API_KEY']
}

url = f"https://api.semanticscholar.org/graph/v1/paper/{test_paper_id}"

# 试几种不同的字段组合
test_cases = [
    "paperId,title,journal,externalIds",
    "paperId,title,journal.volume,journal.pages,externalIds.DOI",
    "paperId,title,journal.name,journal.volume,journal.pages,externalIds.DOI",
]

for i, fields in enumerate(test_cases, 1):
    print(f"\n--- 测试 {i} ---")
    print(f"字段: {fields}")
    
    params = {"fields": fields}
    
    time.sleep(3)
    
    response = requests.get(url, params=params, headers=headers, timeout=30)
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n返回的字段: {sorted(data.keys())}")
        print(f"\n完整JSON:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(f"失败: {response.text}")

print(f"\n{'='*80}")
