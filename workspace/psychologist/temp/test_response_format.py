
#!/usr/bin/env python3
"""
测试API返回的格式
"""

import os
import requests
import json
import time

os.environ['SEMANTIC_SCHOLAR_API_KEY'] = 'KpNolzKwWrMhKMZW0XHq5jBhmBfOfNg3Q0sErPdi'

print("="*80)
print("测试API返回格式（用点号请求子字段）")
print("="*80)

test_paper_id = "13241a844c714549c173e239714ae020386172e3"

headers = {
    "Accept": "application/json",
    "x-api-key": os.environ['SEMANTIC_SCHOLAR_API_KEY']
}

url = f"https://api.semanticscholar.org/graph/v1/paper/{test_paper_id}"
params = {
    "fields": "paperId,title,abstract,venue,year,journal.name,journal.volume,journal.pages,publicationVenue,citationCount,authors,externalIds.DOI"
}

print(f"\n请求URL: {url}")
print(f"请求字段: {params['fields']}")

# 等待避免速率限制
time.sleep(5)

response = requests.get(url, params=params, headers=headers, timeout=30)
print(f"\n状态码: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"\n✅ 响应数据:")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    
    print(f"\n📊 查看字段:")
    for key in sorted(data.keys()):
        print(f"  {key}: {type(data[key])}")
        if isinstance(data[key], dict):
            for subkey in sorted(data[key].keys()):
                print(f"    {subkey}: {data[key][subkey]}")
else:
    print(f"\n❌ 失败: {response.text}")

print(f"\n{'='*80}")
