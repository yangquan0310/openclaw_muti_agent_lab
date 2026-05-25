# 如何管理知识库

> 知识库的合并、筛选、保存功能，支持链式调用。

---

## 问题

### 知识库是什么？

`knowledge/index.json` 是研究助手的核心数据源，包含：
- 所有检索到的论文元数据
- 标签（labels）和笔记（notes）
- 统计信息（statistics）

### 什么时候需要管理知识库？

| 场景 | 操作 |
|------|------|
| 合并多个检索结果 | `merge()` |
| 按条件筛选文献 | `filter()` |
| 保存到文件 | `save()` |

### 为什么要链式调用？

减少中间变量，一步到位：
```python
# ❌ 分离调用
manager = Manager()
manager.merge("kb1.json", "kb2.json")
manager.filter({"citations_min": 50})
manager.save("result.json")

# ✅ 链式调用
Manager().merge("kb1.json", "kb2.json").filter({"citations_min": 50}).save("result.json")
```

---

## 方法论

### 判断：绑定路径还是空初始化？

| 场景 | 初始化方式 |
|------|------------|
| 合并多个知识库 | `Manager()` 空初始化 |
| 操作已有知识库 | `Manager(kb_path="...")` 绑定路径 |

### 判断：筛选条件怎么选？

| 筛选目标 | 推荐条件 |
|----------|----------|
| 高影响力文献 | `citations_min`, `sort_by: citationCount` |
| 最新文献 | `year_min`, `sort_by: year` |
| 特定类型 | `types: ["📊实证", "📖综述"]` |
| 特定主题 | `topics` |

---

## 工作流

### 步骤 1：初始化

**空初始化（用于合并）**：
```python
from manage.Manager import Manager

manager = Manager()
```

**绑定路径（用于操作已有知识库）**：
```python
manager = Manager("knowledge/index.json")
```

### 步骤 2：执行操作

**合并**：
```python
manager.merge("kb1.json", "kb2.json", "kb3.json")
```

**筛选**：
```python
manager.filter({
    "citations_min": 50,
    "types": ["📊实证", "📖综述"],
    "sort_by": "citationCount",
    "limit": 10
})
```

### 步骤 3：保存

**有绑定路径**：
```python
manager.save()  # 无参保存到绑定路径
```

**无绑定路径**：
```python
manager.save("output.json", "项目名称")
```

---

## 执行标准

### 知识库 JSON 结构

```json
{
  "version": "1.0.0",
  "project": "项目名称",
  "statistics": {
    "total_count": 38,
    "total_citations": 12345
  },
  "papers": [
    {
      "paperId": "...",
      "title": "...",
      "authors": ["..."],
      "year": 2022,
      "citationCount": 45,
      "labels": {...},
      "notes": {...}
    }
  ]
}
```

### 保存检查清单

- [ ] 绑定路径时，`save()` 无参调用
- [ ] 空初始化时，`save()` 必须指定 `output_path`
- [ ] 保存后验证文件存在
