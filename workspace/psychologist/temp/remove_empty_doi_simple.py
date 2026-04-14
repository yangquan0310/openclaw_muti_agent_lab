
#!/usr/bin/env python3
"""
删除知识库中空DOI的条目（简化版）
"""

import json
import os
import shutil
from datetime import datetime

KB_PATHS = [
    "/root/实验室仓库/项目文件/学生论文修改/知识库/index.json",
    "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/index.json",
    "/root/实验室仓库/项目文件/跨期选择的年龄差异/知识库/index.json"
]

print("="*80)
print("删除知识库中空DOI的条目")
print("="*80)

for kb_path in KB_PATHS:
    print(f"\n处理: {kb_path}")
    
    # 备份
    if os.path.exists(kb_path):
        backup_path = kb_path + f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(kb_path, backup_path)
        print(f"  已备份到: {backup_path}")
    
    # 加载知识库
    with open(kb_path, 'r', encoding='utf-8') as f:
        kb = json.load(f)
    
    papers = kb['papers']
    print(f"  原论文数: {len(papers)}")
    
    # 过滤掉空DOI的条目
    valid_papers = []
    for p in papers:
        if p.get('doi'):
            valid_papers.append(p)
    
    removed_count = len(papers) - len(valid_papers)
    print(f"  删除空DOI: {removed_count} 篇")
    print(f"  剩余论文: {len(valid_papers)} 篇")
    
    # 更新并保存
    kb['papers'] = valid_papers
    kb['updated_at'] = datetime.now().isoformat()
    
    with open(kb_path, 'w', encoding='utf-8') as f:
        json.dump(kb, f, ensure_ascii=False, indent=2)
    
    print(f"  保存完成: {kb_path}")

print("\n" + "="*80)
print("所有知识库处理完成！")
print("="*80)
