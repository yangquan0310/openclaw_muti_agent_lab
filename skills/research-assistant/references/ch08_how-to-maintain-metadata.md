# 如何维护元数据

> 维护项目元数据（时间戳更新），使用 Git 进行版本控制。

---

## 问题

### 为什么要维护元数据？

元数据记录了知识库的更新历史，帮助：
- 追踪最后修改时间
- 管理多个笔记版本
- 维护项目完整性

### 本项目的版本控制策略

> **Git 进行版本控制**，综述文档的版本历史由 Git 管理，不需要额外的版本归档功能。

---

## 方法论

### 元数据自动更新规则

| 操作 | 触发模块 | 调用方法 | 更新内容 |
|------|----------|----------|----------|
| search 检索后 | `search` | `update_kb_metadata()` | `knowledge_base.updated_at` |
| summarize 总结后 | `summarize` | `update_kb_metadata()` | `knowledge_base.updated_at` |
| manage 导出笔记后 | `manage` | `update_notes_metadata()` | `notes` + `knowledge_base.updated_at` |
| synthesize 提取笔记后 | `synthesize` | `update_kb_metadata()` | `knowledge_base.updated_at` |

---

## 工作流

### 步骤 1：初始化 Maintainer

```python
from maintainer.Maintainer import Maintainer

maintainer = Maintainer("~/项目")
```

### 步骤 2：更新知识库时间戳

```python
maintainer.update_kb_metadata()
```

### 步骤 3：更新笔记元数据

```python
maintainer.update_notes_metadata(
    note_filename="笔记_主题.md",
    local_path="knowledge/note/笔记_主题.md",
    description="主题笔记"
)
```

---

## 执行标准

### 元数据更新检查

| 检查项 | 标准 |
|--------|------|
| `updated_at` | 每次操作后更新 |
| `notes` 列表 | 新增笔记后追加 |
| Git commit | 每次更新后 commit |

### Git 工作流

```bash
# 每次阶段完成后
git add .
git commit -m "feat: 完成检索阶段"
```
