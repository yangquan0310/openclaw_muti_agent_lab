# -*- coding: utf-8 -*-
import re

# 读取修改后的文件
with open('/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/综述/数字化使用对自传体记忆的影响.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 查找所有APA格式的引用（作者, 年份）
# 匹配模式：中文或英文作者名 + 年份
pattern = r'[\u4e00-\u9fa5A-Za-z][\u4e00-\u9fa5A-Za-z\s\.&]+,\s*20[0-9]{2}'
citations = re.findall(pattern, content)

# 清理并统计
clean_citations = []
for c in citations:
    # 去除多余空格
    c = c.strip()
    if c and len(c) > 5:  # 过滤掉太短的匹配
        clean_citations.append(c)

# 去重统计
unique_citations = sorted(set(clean_citations))

print(f"共找到 {len(clean_citations)} 处引用")
print(f"去重后共有 {len(unique_citations)} 个不同引用")
print("\n所有引用列表：")
for i, c in enumerate(unique_citations, 1):
    count = clean_citations.count(c)
    print(f"{i}. {c} (出现{count}次)")
