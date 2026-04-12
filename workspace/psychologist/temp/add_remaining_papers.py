#!/usr/bin/env python3
"""
将剩余的32篇关于"多元负性思维与睡眠质量"的文献添加到学生论文修改项目知识库
"""
import json
from datetime import datetime

index_path = "/root/实验室仓库/项目文件/学生论文修改/知识库/index.json"

# 读取现有知识库
with open(index_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 获取当前最大ID
current_ids = [int(p['id']) for p in data.get('papers', []) if p['id'].isdigit()]
max_id = max(current_ids) if current_ids else 0

print(f"当前最大ID: {max_id}")
print(f"现有文献数量: {len(data.get('papers', []))}")

# 剩余32篇文献数据（从Semantic Scholar检索结果整理）
# 这里需要根据实际检索结果填写
new_papers = []

# TODO: 添加剩余的32篇文献

print(f"\n准备添加 {len(new_papers)} 篇新文献...")

# 添加到知识库
data['papers'].extend(new_papers)

# 更新统计信息
stats = data.get('statistics', {})
stats['total_count'] = len(data['papers'])
# 其他统计字段也需要更新...

# 更新版本号和时间戳
data['version'] = '1.4.0'
data['updated_at'] = datetime.now().isoformat()

# 保存
with open(index_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n更新完成：")
print(f"  - 新增文献: {len(new_papers)}篇")
print(f"  - 总计: {len(data['papers'])}篇")
print(f"  - 版本号: {data['version']}")
print(f"  - 更新时间: {data['updated_at']}")
