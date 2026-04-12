#!/usr/bin/env python3
"""
将知识库index.json中的topic字段从字符串改为列表格式
"""
import json
from datetime import datetime

# 项目路径
project_path = "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/index.json"

# 读取index.json
with open(project_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 统计修改数量
modified_count = 0

# 遍历所有papers，将topic从字符串改为列表
for paper in data.get('papers', []):
    if 'topic' in paper:
        topic = paper['topic']
        # 如果topic是字符串，改为列表
        if isinstance(topic, str):
            paper['topic'] = [topic]
            modified_count += 1
        # 如果topic已经是列表，保持不变
        elif isinstance(topic, list):
            pass

# 更新版本号和时间戳
data['version'] = '6.1.0'
data['updated_at'] = datetime.now().isoformat()

# 保存更新后的index.json
with open(project_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"修改完成：共修改 {modified_count} 篇文献的topic字段")
print(f"版本号：{data['version']}")
print(f"更新时间：{data['updated_at']}")
