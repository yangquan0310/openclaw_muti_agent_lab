
#!/usr/bin/env python3
"""
测试 Manager 类刷新元数据（只试一篇）
"""

import os
import sys
import json
import time
sys.path.insert(0, '/root/.openclaw/skills/knowledge-manager')

os.environ['SEMANTIC_SCHOLAR_API_KEY'] = 'KpNolzKwWrMhKMZW0XHq5jBhmBfOfNg3Q0sErPdi'

print("="*80)
print("测试 Manager 刷新元数据（只试一篇）")
print("="*80)

from Searcher import Searcher
from Manager import Manager

kb_path = "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/index.json"

# 1. 先读取知识库，看看第一篇文献
print(f"\n1. 读取知识库: {kb_path}")
with open(kb_path, 'r', encoding='utf-8') as f:
    kb = json.load(f)

paper = kb['papers'][0]
paper_id = paper.get('paperId')
print(f"   第一篇文献:")
print(f"     paperId: {paper_id}")
print(f"     标题: {paper.get('title')}")
print(f"     当前volume: '{paper.get('volume')}'")
print(f"     当前pages: '{paper.get('pages')}'")
print(f"     当前doi: '{paper.get('doi')}'")

# 2. 用Searcher获取详情
print(f"\n2. 用Searcher获取详情...")
searcher = Searcher()

time.sleep(3)  # 等待避免速率限制
details = searcher.get_paper_details(paper_id)

if details:
    print(f"   ✅ 获取成功！")
    print(f"\n   详情内容:")
    print(json.dumps(details, indent=2, ensure_ascii=False))
    
    # 3. 测试Manager的格式化逻辑
    print(f"\n3. 测试元数据提取...")
    if details.get('journal'):
        journal = details['journal']
        print(f"   journal:")
        print(f"     name: {journal.get('name')}")
        
        if journal.get('volume'):
            vol = journal['volume'].strip()
            if ' ' in vol:
                vol = vol.split()[0]
            print(f"     volume: {vol}")
        
        if journal.get('pages'):
            pages = journal['pages'].strip()
            pages = ' '.join(pages.split())
            print(f"     pages: {pages}")
    
    if details.get('externalIds') and details['externalIds'].get('DOI'):
        print(f"   doi: {details['externalIds']['DOI']}")

print("\n" + "="*80)
print("✅ 测试完成！")
print("="*80)
