# SKILL.md - search-photo-effect

## 技能信息

| 属性 | 值 |
|------|-----|
| 技能名称 | search-photo-effect |
| 技能类型 | 文献检索 |
| 触发条件 | 需要搜索照片效应相关文献 |
| 作者 | 心理学家 |

## 功能描述

本技能用于自动化检索照片效应（photo-taking impairment effect）相关学术文献。

## 输入

- 检索关键词：photo-taking impairment, camera, memory, etc.
- 引用量阈值：奠基(>500), 重要(50-500), 一般(<50)

## 输出

- 结构化文献列表（JSON格式）
- 文献分类标签（重要性、类型）

## 使用示例

```python
from search_photo_effect import search_papers

results = search_papers(query="photo-taking impairment", limit=100)
```

## 注意事项

- 必须使用Semantic Scholar API
- 严禁编造文献信息
- 检索过程需留痕记录
