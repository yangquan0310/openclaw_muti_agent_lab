
#!/usr/bin/env python3
"""
直接用Searcher.update()更新
"""

import sys
sys.path.insert(0, '/root/.openclaw/skills/knowledge-manager')

from Searcher import Searcher

KB_PATH = "/root/实验室仓库/项目文件/学生论文修改/知识库/index.json"

print("="*80)
print("用Searcher.update()更新元数据")
print("="*80)

searcher = Searcher()
kb = searcher.update(kb_path=KB_PATH)

print("\n" + "="*80)
print("完成！")
print("="*80)
print(f"论文总数: {len(kb['papers'])}")
print(f"DOI非空: {sum(1 for p in kb['papers'] if p.get('doi'))}")
print("="*80)
