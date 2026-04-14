
#!/usr/bin/env python3
"""
更新跨期选择的年龄差异知识库
"""

import sys
sys.path.insert(0, '/root/.openclaw/skills/knowledge-manager')

import json
import os
import shutil
from datetime import datetime

from Searcher import Searcher

KB_PATH = "/root/实验室仓库/项目文件/跨期选择的年龄差异/知识库/index.json"

print("="*80)
print("更新跨期选择的年龄差异知识库")
print("="*80)

# 1. 备份
if os.path.exists(KB_PATH):
    backup_path = KB_PATH + f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(KB_PATH, backup_path)
    print(f"已备份到: {backup_path}")

# 2. 更新元数据
print("\n正在更新元数据...")
searcher = Searcher()
kb = searcher.update(kb_path=KB_PATH)
print("元数据更新完成！")

# 3. 删除id字段
print("\n正在删除id字段...")
removed_id_count = 0
for p in kb['papers']:
    if 'id' in p:
        del p['id']
        removed_id_count += 1
print(f"删除id字段: {removed_id_count} 篇")

# 4. 保存
kb['updated_at'] = datetime.now().isoformat()
with open(KB_PATH, 'w', encoding='utf-8') as f:
    json.dump(kb, f, ensure_ascii=False, indent=2)

print("\n" + "="*80)
print("知识库更新完成！")
print("="*80)
print(f"论文总数: {len(kb['papers'])}")
print(f"DOI非空: {sum(1 for p in kb['papers'] if p.get('doi'))}")
print(f"总引用量: {kb['statistics']['total_citations']}")
print("="*80)
