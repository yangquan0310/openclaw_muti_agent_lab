
#!/usr/bin/env python3
"""
更新数字化存储与自传体记忆知识库（带重试和延迟）
"""

import sys
sys.path.insert(0, '/root/.openclaw/skills/knowledge-manager')

import json
import os
import requests
import time
from datetime import datetime
from typing import List, Dict

KB_PATH = "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/index.json"
BATCH_URL = "https://api.semanticscholar.org/graph/v1/paper/batch"
FIELDS = "paperId,authors,year,title,venue,citationCount,journal,externalIds,url,abstract"

print("="*80)
print("更新数字化存储与自传体记忆知识库（带重试和延迟）")
print("="*80)

# 1. 备份
import shutil
if os.path.exists(KB_PATH):
    backup_path = KB_PATH + ".backup_20260414_full"
    shutil.copy2(KB_PATH, backup_path)
    print(f"已备份现有知识库到: {backup_path}")

# 2. 加载知识库
with open(KB_PATH, 'r', encoding='utf-8') as f:
    kb = json.load(f)

papers = kb['papers']
print(f"总论文: {len(papers)}")

# 3. 准备API
api_key = os.environ.get('SEMANTIC_SCHOLAR_API_KEY')
session = requests.Session()
session.headers.update({"Accept": "application/json"})
if api_key:
    session.headers.update({"x-api-key": api_key})

# 4. 批量获取（带延迟和重试）
paper_ids = [p['paperId'] for p in papers if 'paperId' in p and p['paperId']]
print(f"有paperId的: {len(paper_ids)}")

detail_map = {}

for i in range(0, len(paper_ids), 50):  # 用更小的批次
    batch = paper_ids[i:i+50]
    print(f"  处理 {i+1}-{min(i+50, len(paper_ids))} / {len(paper_ids)}")
    
    success = False
    retry_count = 0
    max_retries = 5
    
    while not success and retry_count &lt; max_retries:
        try:
            resp = session.post(
                BATCH_URL, 
                json={"ids": batch}, 
                params={"fields": FIELDS}, 
                timeout=60
            )
            resp.raise_for_status()
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
                        'citationCount': raw.get('citationCount', 0),
                        'authors': raw.get('authors'),
                        'year': raw.get('year'),
                        'title': raw.get('title'),
                        'venue': raw.get('venue'),
                        'abstract': raw.get('abstract'),
                        'url': raw.get('url')
                    }
            
            success = True
            print(f"    成功获取 {len([r for r in raw_list if r])} 篇")
            
        except Exception as e:
            retry_count += 1
            wait_time = 2 ** retry_count  # 指数退避
            print(f"    错误 (尝试 {retry_count}/{max_retries}): {e}")
            if retry_count &lt; max_retries:
                print(f"    等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)
    
    # 批次间延迟
    time.sleep(2)

print(f"\n成功获取详情: {len(detail_map)} 篇")

# 5. 更新论文
updated = 0
doi_added = 0
for p in papers:
    pid = p.get('paperId')
    if pid and pid in detail_map:
        d = detail_map[pid]
        if d.get('doi') and not p.get('doi'):
            p['doi'] = d['doi']
            doi_added += 1
        for key in ['volume', 'issue', 'pages', 'citationCount', 'authors', 'year', 'title', 'venue', 'abstract', 'url']:
            if d.get(key) is not None:
                p[key] = d[key]
        updated += 1

print(f"更新论文: {updated}")
print(f"新增DOI: {doi_added}")

# 6. 保存
kb['updated_at'] = datetime.now().isoformat()
kb['statistics']['total_citations'] = sum(p.get('citationCount', 0) for p in papers)
kb['statistics']['foundation_count'] = sum(1 for p in papers if p.get('citationCount', 0) &gt;= 500)
kb['statistics']['important_count'] = sum(1 for p in papers if 50 &lt;= p.get('citationCount', 0) &lt; 500)
kb['statistics']['general_count'] = len(papers) - kb['statistics']['foundation_count'] - kb['statistics']['important_count']

with open(KB_PATH, 'w', encoding='utf-8') as f:
    json.dump(kb, f, ensure_ascii=False, indent=2)

print("\n" + "="*80)
print("知识库元数据更新完成！")
print("="*80)
print(f"论文总数: {len(papers)}")
print(f"DOI非空: {sum(1 for p in papers if p.get('doi'))}")
print(f"总引用量: {kb['statistics']['total_citations']}")
print(f"奠基文献: {kb['statistics']['foundation_count']}")
print(f"重要文献: {kb['statistics']['important_count']}")
print(f"一般文献: {kb['statistics']['general_count']}")
print("="*80)
