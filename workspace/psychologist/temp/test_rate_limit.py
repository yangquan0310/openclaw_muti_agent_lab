
#!/usr/bin/env python3
"""
测试速率限制，用更长的延迟
"""

import os
import sys
import json
import time
import requests

# 设置环境变量
os.environ['SEMANTIC_SCHOLAR_API_KEY'] = 'KpNolzKwWrMhKMZW0XHq5jBhmBfOfNg3Q0sErPdi'

print("="*80)
print("测试：用更长的延迟")
print("="*80)

paper_id = "03034d731473f19aa2edd8f40d3a979eb3c3082"
headers = {
    "Accept": "application/json",
    "x-api-key": os.environ['SEMANTIC_SCHOLAR_API_KEY']
}

print(f"\n等待2秒...")
time.sleep(2)

print(f"现在请求...")
url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}"
params = {
    "fields": "abstract,venue,year,journal,volume,issue,pages,doi,citationCount"
}

response = requests.get(url, params=params, headers=headers, timeout=30)
print(f"状态码: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"\n成功！数据:")
    print(json.dumps(data, indent=2, ensure_ascii=False))
else:
    print(f"\n失败: {response.text}")

print(f"\n{'='*80}")
