#!/usr/bin/env python3
"""
为学生论文修改项目的20篇文献添加主题：课堂拍照行为
"""
import json
from datetime import datetime

index_path = "/root/实验室仓库/项目文件/学生论文修改/知识库/index.json"

# 读取index.json
with open(index_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

papers = data.get('papers', [])
modified_count = 0

# 为每篇文献添加topic字段
for paper in papers:
    paper['topic'] = ["课堂拍照行为"]
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

print(f"修改完成：共修改 {modified_count} 篇文献的topic字段")
print(f"主题：课堂拍照行为")
print(f"版本号：{data['version']}")
print(f"更新时间：{data['updated_at']}")
