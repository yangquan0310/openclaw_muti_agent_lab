
#!/usr/bin/env python3
"""
删除知识库中的id字段
"""

import json
import os
import shutil
from datetime import datetime

KB_PATHS = [
    "/root/实验室仓库/项目文件/学生论文修改/知识库/index.json",
    "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/index.json"
]

print("="*80)
print("删除知识库中的id字段")
print("="*80)

for kb_path in KB_PATHS:
    print(f"\n处理: {kb_path}")
    
    # 备份
    if os.path.exists(kb_path):
        backup_path = kb_path + f".backup_no_id_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(kb_path, backup_path)
        print(f"  已备份到: {backup_path}")
    
    # 加载知识库
    with open(kb_path, 'r', encoding='utf-8') as f:
        kb = json.load(f)
    
    papers = kb['papers']
    print(f"  总论文数: {len(papers)}")
    
    # 删除id字段
    removed_count = 0
    for p in papers:
        if 'id' in p:
            del p['id']
            removed_count += 1
    
    print(f"  删除id字段: {removed_count} 篇")
    
    # 保存
    kb['updated_at'] = datetime.now().isoformat()
    with open(kb_path, 'w', encoding='utf-8') as f:
        json.dump(kb, f, ensure_ascii=False, indent=2)
    
    print(f"  保存完成: {kb_path}")

print("\n" + "="*80)
print("所有知识库处理完成！")
print("="*80)
