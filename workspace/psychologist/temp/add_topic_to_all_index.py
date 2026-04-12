#!/usr/bin/env python3
"""
为所有知识库index.json添加topic字段（空列表占位）
"""
import json
from datetime import datetime
import os

# 查找所有知识库index.json
base_path = "/root/实验室仓库/项目文件"
projects = []

for item in os.listdir(base_path):
    project_path = os.path.join(base_path, item)
    if os.path.isdir(project_path):
        index_path = os.path.join(project_path, "知识库", "index.json")
        if os.path.exists(index_path):
            projects.append((item, index_path))

print(f"找到 {len(projects)} 个知识库索引文件\n")

# 处理每个知识库
for project_name, index_path in projects:
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        papers = data.get('papers', [])
        modified_count = 0
        
        # 为每篇文献添加topic字段（如果不存在）
        for paper in papers:
            if 'topic' not in paper:
                paper['topic'] = []
                modified_count += 1
            elif isinstance(paper['topic'], str):
                # 如果topic是字符串，改为列表
                paper['topic'] = [paper['topic']]
                modified_count += 1
        
        # 更新版本号和时间戳
        current_version = data.get('version', '1.0.0')
        if isinstance(current_version, str):
            version_parts = current_version.split('.')
            if len(version_parts) >= 2:
                try:
                    version_parts[1] = str(int(version_parts[1]) + 1)
                    data['version'] = '.'.join(version_parts)
                except:
                    data['version'] = '1.1.0'
        else:
            data['version'] = '1.1.0'
        
        data['updated_at'] = datetime.now().isoformat()
        
        # 保存
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ {project_name}: 共 {len(papers)} 篇文献，修改 {modified_count} 篇")
        
    except Exception as e:
        print(f"❌ {project_name}: 错误 - {e}")

print("\n处理完成！")
