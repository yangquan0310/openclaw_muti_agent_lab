
#!/usr/bin/env python3
"""
简单更新知识库元数据
"""

import json
import os
import requests
import time
from datetime import datetime

KB_PATH = "/root/实验室仓库/项目文件/学生论文修改/知识库/index.json"
BATCH_URL = "https://api.semanticscholar.org/graph/v1/paper/batch"
FIELDS = "paperId,authors,year,title,venue,citationCount,journal,externalIds,url,abstract"

# 1. 加载知识库
with open(KB_PATH, 'r', encoding='utf-8') as f:
    kb = json.load(f)

papers = kb['papers']
print(f"总论文: {len(papers)}")

# 2. 准备API
api_key = os.environ.get('SEMANTIC_SCHOLAR_API_KEY')
session = requests.Session()
session.headers.update({"Accept": "application/json"})
if api_key:
    session.headers.update({"x-api-key": api_key})

# 3. 批量获取
paper_ids = [p['paperId'] for p in papers if 'paperId' in p and p['paperId']]
print(f"有paperId的: {len(paper_ids)}")

detail_map = {}
for i in range(0, len(paper_ids), 100):
    batch = paper_ids[i:i+100]
    print(f"  处理 {i+1}-{min(i+100, len(paper_ids))}")
    try:
        resp = session.post(BATCH_URL, json={"ids": batch}, params={"fields": FIELDS}, timeout=30)
        data = resp.json()
        raw_list = data if isinstance(data, list) else data.get('data', [])
        for raw in raw_list:
            if raw and raw.get('paperId'):
                pid = raw['paperId']
                
                # 提取DOI
                doi = None
                ext = raw.get('externalIds')
                if isinstance(ext, dict):
                    doi = ext.get('DOI')
                
                # 提取期刊信息
                volume = None
                issue = None
                pages = None
                journal = raw.get('journal')
                if isinstance(journal, dict):
                    volume = journal.get('volume')
                    issue = journal.get('issue')
                    pages = journal.get('pages')
                
                detail_map[pid] = {
                    'doi': doi,
                    'volume': volume,
                    'issue': issue,
                    'pages': pages,
                    'citationCount': raw.get('citationCount', 0)
                }
        time.sleep(0.5)
    except Exception as e:
        print(f"    错误: {e}")

print(f"获取到详情: {len(detail_map)}")

# 4. 更新论文
updated = 0
doi_added = 0
for p in papers:
    pid = p.get('paperId')
    if pid and pid in detail_map:
        d = detail_map[pid]
        if d.get('doi') and not p.get('doi'):
            p['doi'] = d['doi']
            doi_added += 1
        if d.get('volume'):
            p['volume'] = d['volume']
        if d.get('issue'):
            p['issue'] = d['issue']
        if d.get('pages'):
            p['pages'] = d['pages']
        p['citationCount'] = d.get('citationCount', 0)
        updated += 1

print(f"更新论文: {updated}")
print(f"新增DOI: {doi_added}")

# 5. 保存
kb['updated_at'] = datetime.now().isoformat()
kb['statistics']['total_citations'] = sum(p.get('citationCount', 0) for p in papers)
kb['statistics']['foundation_count'] = sum(1 for p in papers if p.get('citationCount', 0) >= 500)
kb['statistics']['important_count'] = sum(1 for p in papers if 50 &lt;= p.get('citationCount', 0) &lt; 500)

with open(KB_PATH, 'w', encoding='utf-8') as f:
    json.dump(kb, f, ensure_ascii=False, indent=2)

print(f"\n完成！DOI非空: {sum(1 for p in papers if p.get('doi'))}")
