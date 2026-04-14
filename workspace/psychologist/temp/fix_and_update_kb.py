
#!/usr/bin/env python3
"""
修复Searcher.update()问题并更新知识库元数据
"""

import sys
import os

# 添加skill目录到路径
sys.path.insert(0, '/root/.openclaw/skills/knowledge-manager')

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import List, Dict, Optional
import json
import time
from datetime import datetime

# 知识库路径
KB_PATH = "/root/实验室仓库/项目文件/学生论文修改/知识库/index.json"

print("="*80)
print("修复并更新知识库元数据")
print("="*80)

# 1. 加载知识库
with open(KB_PATH, 'r', encoding='utf-8') as f:
    kb_data = json.load(f)

papers = kb_data.get('papers', [])
print(f"已加载知识库: {len(papers)} 篇论文")

# 2. 获取API key
api_key = os.environ.get('SEMANTIC_SCHOLAR_API_KEY')
if not api_key:
    print("警告: 未设置 Semantic Scholar API key")

# 3. 准备会话
session = requests.Session()
session.headers.update({"Accept": "application/json"})
if api_key:
    session.headers.update({"x-api-key": api_key})

retry = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry)
session.mount('https://', adapter)

# 4. 批量获取详情
BATCH_URL = "https://api.semanticscholar.org/graph/v1/paper/batch"
FIELDS = "paperId,authors,year,title,venue,citationCount,journal,externalIds,url,abstract"

paper_ids = [p.get('paperId') for p in papers if p.get('paperId')]
print(f"有效的 paperId: {len(paper_ids)} 个")

detail_map = {}
for i in range(0, len(paper_ids), 100):
    batch = paper_ids[i:i+100]
    print(f"  批量获取: {i+1}-{min(i+100, len(paper_ids))} / {len(paper_ids)}")
    payload = {"ids": batch}
    try:
        resp = session.post(BATCH_URL, json=payload, params={"fields": FIELDS}, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        raw_papers = data if isinstance(data, list) else data.get('data', [])
        
        # 处理每篇论文
        for raw in raw_papers:
            if raw is None:
                continue
            pid = raw.get('paperId')
            if not pid:
                continue
                
            # 标准化
            authors = []
            for author in raw.get('authors', []):
                if isinstance(author, dict):
                    name = author.get('name')
                    if name:
                        authors.append(name)
                elif isinstance(author, str):
                    authors.append(author)
            
            journal = raw.get('journal', {})
            volume = journal.get('volume') if isinstance(journal, dict) else None
            issue = journal.get('issue') if isinstance(journal, dict) else None
            pages = journal.get('pages') if isinstance(journal, dict) else None
            
            external = raw.get('externalIds', {})
            doi = external.get('DOI') if isinstance(external, dict) else None
            
            url = raw.get('url')
            if not url and raw.get('paperId'):
                url = f"https://www.semanticscholar.org/paper/{raw['paperId']}"
            
            detail_map[pid] = {
                "paperId": raw.get('paperId'),
                "authors": authors,
                "year": raw.get('year'),
                "title": raw.get('title'),
                "venue": raw.get('venue'),
                "volume": volume,
                "issue": issue,
                "pages": pages,
                "doi": doi,
                "url": url,
                "abstract": raw.get('abstract'),
                "citationCount": raw.get('citationCount', 0)
            }
        time.sleep(0.5)
    except Exception as e:
        print(f"批量获取失败: {e}")

print(f"成功获取详情: {len(detail_map)} 篇")

# 5. 更新论文
updated_count = 0
for paper in papers:
    pid = paper.get('paperId')
    if pid and pid in detail_map:
        detail = detail_map[pid]
        for key in ['authors', 'year', 'title', 'venue', 'volume', 'issue', 'pages', 'doi', 'url', 'abstract', 'citationCount']:
            if detail.get(key) is not None:
                paper[key] = detail[key]
        updated_count += 1

print(f"已更新论文: {updated_count} 篇")

# 6. 重新计算统计
total = len(papers)
total_cites = sum(p.get('citationCount', 0) for p in papers)
foundation = sum(1 for p in papers if p.get('citationCount', 0) &gt;= 500)
important = sum(1 for p in papers if 50 &lt;= p.get('citationCount', 0) &lt; 500)
general = total - foundation - important
empirical = sum(1 for p in papers if p.get('labels', {}).get('type') == '📊实证')
review = sum(1 for p in papers if p.get('labels', {}).get('type') == '📖综述')
theory = sum(1 for p in papers if p.get('labels', {}).get('type') == '💡理论')

kb_data['statistics'] = {
    "total_count": total,
    "total_citations": total_cites,
    "foundation_count": foundation,
    "important_count": important,
    "general_count": general,
    "empirical_count": empirical,
    "review_count": review,
    "theory_count": theory
}
kb_data['updated_at'] = datetime.now().isoformat()

# 7. 保存
os.makedirs(os.path.dirname(os.path.abspath(KB_PATH)), exist_ok=True)
with open(KB_PATH, 'w', encoding='utf-8') as f:
    json.dump(kb_data, f, ensure_ascii=False, indent=2)

print("\n" + "="*80)
print("知识库元数据更新完成！")
print("="*80)
print(f"论文总数: {total}")
print(f"总引用量: {total_cites}")
print(f"DOI非空: {sum(1 for p in papers if p.get('doi'))}")
print(f"奠基文献: {foundation}")
print(f"重要文献: {important}")
print(f"一般文献: {general}")
print("="*80)
