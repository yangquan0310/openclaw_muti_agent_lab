---
name: 知识库管理
description: 提供知识库的合并、筛选、保存功能，支持链式调用
version: 2.0.0
author: Yang Quan
dependencies:
  - python>=3.9
tools:
  - python
  - markdown
---

# 知识库管理模块 (Manager)

Manager 类提供知识库的合并、筛选、保存功能，支持链式调用，方便进行多步操作。

## 快速开始

### 我想...

| 需求 | 方法 |
|------|------|
| 合并知识库 | [`merge()`](#1-合并知识库) |
| 筛选知识库 | [`filter()`](#2-筛选知识库) |
| 保存知识库 | [`save()`](#3-保存知识库) |

## 文件说明

| 文件 | 功能 |
|------|------|
| `Manager.py` | 知识库管理主类 |

---

## 工作流示例

### 1. 合并知识库

```python
from Manager import Manager

manager = Manager()
manager.merge("kb1.json", "kb2.json", "kb3.json").save("merged.json", "合并项目")
```

### 2. 筛选知识库

```python
from Manager import Manager

manager = Manager("my_kb.json")
manager.filter({
    "citations_min": 50,
    "types": ["📊实证", "📖综述"],
    "sort_by": "citationCount",
    "limit": 10
}).save("filtered.json")
```

### 3. 链式调用：合并 → 筛选 → 保存

```python
from Manager import Manager

manager = Manager()
manager.merge("kb1.json", "kb2.json") \
       .filter({
           "citations_min": 50,
           "types": ["📊实证", "📖综述"],
           "sort_by": "citationCount",
           "limit": 20
       }) \
       .save("final_kb.json", "最终项目")
```

---

## 方法详情

### `merge(*kb_paths, deduplicate=True)`

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `*kb_paths` | str | 必填 | 知识库文件路径（可传入多个） |
| `deduplicate` | bool | True | 是否全局去重（基于 paperId） |

### `filter(conditions)`

| 参数 | 类型 | 说明 |
|------|------|------|
| `conditions` | Dict | 筛选条件字典 |

#### 支持的筛选条件
| 键 | 类型 | 说明 |
|----|------|------|
| `year_min` | int | 最小年份 |
| `year_max` | int | 最大年份 |
| `citations_min` | int | 最小引用量 |
| `citations_max` | int | 最大引用量 |
| `topics` | List[str] | 主题列表（任意匹配） |
| `types` | List[str] | 文献类型列表（如 `["📊实证", "📖综述"]`） |
| `importance` | List[str] | 重要性列表（如 `["🔴奠基", "🟡重要"]`） |
| `venue` | str | 期刊/会议名称（模糊匹配） |
| `limit` | int | 返回前 N 篇（需与排序配合） |
| `sort_by` | str | 排序字段（如 `"citationCount"`, `"year"`） |
| `sort_desc` | bool | 是否降序（默认 True） |

### `save(output_path, project_name="")`

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `output_path` | str | 必填 | 输出文件路径 |
| `project_name` | str | "" | 项目名称（会更新到知识库中） |

### `get_kb()`
返回当前知识库字典

### `get_papers()`
返回当前论文列表

---

## 知识库 JSON 结构

```json
{
  "version": "1.0.0",
  "project": "项目名称",
  "created_at": "2026-04-13T03:33:00",
  "updated_at": "2026-04-13T03:33:00",
  "statistics": {
    "total_count": 38,
    "total_citations": 12345,
    "foundation_count": 2,
    "important_count": 6,
    "general_count": 30,
    "empirical_count": 30,
    "review_count": 4,
    "theory_count": 0
  },
  "papers": [
    {
      "paperId": "ff9c8a3d364d027da407dd772be53cb237a349f2",
      "authors": ["张敏", "李华", "王伟"],
      "year": 2022,
      "title": "怀旧技术在降低老年人压力水平中的应用效果：系统综述",
      "venue": "中国老年学杂志",
      "volume": "42",
      "issue": "5",
      "pages": "1123-1128",
      "doi": "10.3969/j.issn.1005-9202.2022.05.032",
      "url": "https://example.com/paper_001",
      "abstract": "目的：系统评价怀旧技术对降低老年人压力水平的效果。...",
      "topic": ["怀旧技术", "老年人", "压力缓解"],
      "citationCount": 45,
      "labels": {
        "type": "📖综述",
        "importance": "🔴奠基文献",
        "JCR": ""
      },
      "notes": {
        "研究问题": "...",
        "研究结果": "...",
        "研究展望": "..."
      }
    }
  ]
}
```

---

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 2.0.0 | 2026-04-14 | 重构为独立 Manager 类 |
