# 元数据维护模块 (Maintainer)

Maintainer 负责维护项目元数据（时间戳更新）。

> 注意：本项目使用 **Git 进行版本控制**，综述文档的版本历史由 Git 管理，不需要额外的版本归档功能。

## 快速开始

| 需求 | 方法 |
|------|------|
| 更新知识库时间戳 | [`update_kb_metadata()`](#更新知识库时间戳) |
| 更新笔记元数据 | [`update_notes_metadata()`](#更新笔记元数据) |

## 核心类

### `Maintainer(project_path)`

元数据维护协调器。

```python
from maintain.Maintainer import Maintainer

maintainer = Maintainer("~/项目")

# 更新知识库时间戳
maintainer.update_kb_metadata()

# 更新笔记元数据
maintainer.update_notes_metadata("笔记_主题.md", "knowledge/note/笔记_主题.md", "主题笔记")
```

### `MetadataManager(project_path)`

元数据管理器，提供链式调用修改元数据。

```python
from maintain.Maintainer import MetadataManager

mm = MetadataManager("~/项目")

# 链式调用
mm.set_title("新项目").add_tag("AI").update_knowledge_base_timestamp().save()
```

---

## 方法详情

### 更新知识库时间戳

```python
maintainer.update_kb_metadata()
```

由 search/summarize/manage/synthesize 模块在操作完成后调用，自动更新 `metadata.json` 中 `knowledge_base.updated_at` 字段。

### 更新笔记元数据

```python
maintainer.update_notes_metadata(note_filename, local_path, description="")
```

由 manage 模块在导出笔记后调用，自动更新 `metadata.json` 中 `notes` 字段。

---

## CLI 入口

```bash
# 更新知识库时间戳
python3 maintain/Maintainer.py ~/项目 update-kb

# 更新笔记元数据
python3 maintain/Maintainer.py ~/项目 update-notes 笔记_主题.md knowledge/note/笔记_主题.md "描述"
```

---

## 元数据自动更新规则

| 操作 | 触发模块 | 调用方法 | 更新内容 |
|------|----------|----------|----------|
| search 检索后 | `search` | `update_kb_metadata()` | `knowledge_base.updated_at` |
| summarize 总结后 | `summarize` | `update_kb_metadata()` | `knowledge_base.updated_at` |
| manage 导出笔记后 | `manage` | `update_notes_metadata()` | `notes` + `knowledge_base.updated_at` |
| synthesize 提取笔记后 | `synthesize` | `update_kb_metadata()` | `knowledge_base.updated_at` |

---

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 3.0.0 | 2026-05-15 | **简化：移除版本归档功能（temp/draft/），因为项目使用 Git 进行版本控制。保留元数据维护功能。** |
| 2.0.0 | 2026-05-09 | 重构：从项目文件整理转为元数据维护+版本控制 |
| 1.0.0 | 2026-04-22 | 初始版本，基于面向对象设计重构 |
