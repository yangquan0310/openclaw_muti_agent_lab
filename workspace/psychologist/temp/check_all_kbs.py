
#!/usr/bin/env python3
"""
检查所有项目知识库状态
"""

import json
import os

PROJECTS_DIR = "/root/实验室仓库/项目文件"

print("="*80)
print("检查所有项目知识库状态")
print("="*80)

projects = [d for d in os.listdir(PROJECTS_DIR) 
            if os.path.isdir(os.path.join(PROJECTS_DIR, d)) 
            and not d.startswith('.')]

for project in sorted(projects):
    project_path = os.path.join(PROJECTS_DIR, project)
    kb_path = os.path.join(project_path, "知识库", "index.json")
    
    if os.path.exists(kb_path):
        try:
            with open(kb_path, 'r', encoding='utf-8') as f:
                kb = json.load(f)
            
            papers = kb.get('papers', [])
            total = len(papers)
            doi_count = sum(1 for p in papers if p.get('doi'))
            has_id = any('id' in p for p in papers)
            
            status = []
            if has_id:
                status.append("有id字段")
            if doi_count &lt; total:
                status.append(f"DOI不全 ({doi_count}/{total})")
            
            status_str = ", ".join(status) if status else "✅ 正常"
            
            print(f"\n{project}")
            print(f"  论文数: {total}")
            print(f"  DOI非空: {doi_count}")
            print(f"  状态: {status_str}")
            
        except Exception as e:
            print(f"\n{project}")
            print(f"  错误: {e}")

print("\n" + "="*80)
print("检查完成")
print("="*80)
