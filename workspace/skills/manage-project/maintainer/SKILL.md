---
name: 项目文件整理
description: 自动化整理项目目录结构、归档中间文件、管理手稿和元数据
version: 2.0.0
author: Yang Quan
dependencies:
  - python>=3.9
tools:
  - python
  - markdown
---

# 项目文件整理模块 (Maintainer)

Maintainer 类负责自动化整理项目目录结构、归档中间文件、管理手稿文件和维护项目元数据。

## 快速开始

### 我想...

| 需求 | 方法 |
|------|------|
| 自动整理项目文件 | [`organize()`](#1-自动整理项目文件) |
| 移动单个文件 | [`move_file()`](#2-移动文件) |
| 重命名文件夹 | [`rename_folder()`](#3-重命名文件夹) |
| 更新项目元数据 | [`update_metadata()`](#4-更新元数据) |

## 文件说明

| 文件 | 功能 |
|------|------|
| `Maintainer.py` | 项目文件整理主类 |
| `数据结构.md` | 项目元数据结构说明 |

---

## 工作流示例

### 1. 自动整理项目文件

```python
from maintainer.Maintainer import Maintainer

maintainer = Maintainer("/path/to/project")

# 实际执行整理
maintainer.organize()

# 预览模式（不实际执行）
maintainer.organize(dry_run=True)
```

自动整理规则：
- `.md` 文件含 "backup"/"备份" → `临时数据/草稿/`
- `.md` 文件含 "综述"/"review" → `知识库/综述/`
- `.md` 文件含 "笔记" + "提取" → `临时数据/笔记/`
- `.md` 文件含 "笔记" → `知识库/笔记/`
- 其他 `.md` 文件 → `手稿/`
- `.json` 文件 → `临时数据/检索条件/`
- `.tmp`/`.temp`/`.log`/`.bak` → `临时数据/`
- `.docx`/`.pdf`/`.txt` 不自动移动（仅用户命令可加入/移出）

### 2. 移动文件

```python
from maintainer.Maintainer import Maintainer

maintainer = Maintainer("/path/to/project")

# 基本移动
maintainer.move_file("论文.md", target_dir="手稿")

# 移动并重命名
maintainer.move_file("旧文件.txt", target_dir="临时数据", new_name="新文件.txt")

# 强制覆盖
maintainer.move_file("文件.md", target_dir="知识库/笔记", overwrite=True)
```

### 3. 重命名文件夹

```python
from maintainer.Maintainer import Maintainer

maintainer = Maintainer("/path/to/project")

# 基本重命名
maintainer.rename_folder("旧名称", "新名称")

# 合并重命名（目标存在时合并内容）
maintainer.rename_folder("旧目录", "现有目录", merge=True)
```

### 4. 更新元数据

```python
from maintainer.Maintainer import Maintainer

maintainer = Maintainer("/path/to/project")

# 更新并保存元数据
maintainer.update_metadata()

# 带额外信息更新
maintainer.update_metadata(
    description="这是一个示例项目",
    tags=["学术写作", "文献综述"],
    status="active"
)
```

---

## 方法详情

### `__init__(project_path)`

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `project_path` | str | 必填 | 项目文件夹路径 |

### `organize(dry_run=False)`

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `dry_run` | bool | False | 是否只预览不执行 |

自动扫描项目根目录文件，按规则移动到对应目录，并更新元数据。

### `move_file(file_path, target_dir, **kwargs)`

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `file_path` | str | 必填 | 源文件路径（相对项目根目录或绝对路径） |
| `target_dir` | str | 必填 | 目标目录（相对项目根目录） |
| `new_name` | str | 原文件名 | 新文件名（可选） |
| `overwrite` | bool | False | 是否覆盖已存在文件 |

**返回**: `bool` 是否成功

### `rename_folder(old_name, new_name, **kwargs)`

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `old_name` | str | 必填 | 原文件夹名（相对项目根目录） |
| `new_name` | str | 必填 | 新文件夹名 |
| `merge` | bool | False | 目标存在时是否合并内容 |

**返回**: `bool` 是否成功

### `update_metadata(**kwargs)`

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `description` | str | 现有值 | 项目描述 |
| `tags` | list | 现有值 | 标签列表 |
| `status` | str | "active" | 项目状态 |

扫描 `文档/` 目录更新文档列表，构建目录结构，保存到 `元数据.json`。

**返回**: `bool` 是否成功

### `get_documents()` / `get_manuscripts()`

分别获取 `文档/` 目录下的用户上传文档列表和 `手稿/` 目录下的代理撰写文档列表。

**返回**: `list` 文档/手稿信息列表

---

## 标准目录结构

```
project/
├── 文档/              # 用户上传的文档（仅用户命令可加入/移出）
├── 手稿/              # 写作助手、审稿助手等撰写的最新md文档
├── 知识库/
│   ├── 笔记/          # 笔记输出
│   └── 综述/          # 综述输出
└── 临时数据/
    ├── 草稿/          # 备份版本、中间文件
    ├── 检索条件/       # 知识库管理检索脚本的检索条件 {检索条件}.json
    └── 笔记/          # NoteExtractor提取出来的笔记文件.md
```

---

## 命令行工具

### 整理单个项目
```bash
python3 maintainer/Maintainer.py /path/to/project
```

### 整理所有项目
```bash
python3 maintainer/Maintainer.py --all
```

### 预览模式
```bash
python3 maintainer/Maintainer.py /path/to/project --dry-run
```

### 指定项目根目录
```bash
python3 maintainer/Maintainer.py --all --projects-dir /custom/projects/dir
```

### 命令参数
| 参数 | 说明 |
|------|------|
| `project_path` | 项目文件夹路径 |
| `--all` | 整理所有项目 |
| `--dry-run` | 预览模式，不实际执行 |
| `--projects-dir` | 项目根目录（默认: /root/实验室仓库/项目文件） |

---

## 配置说明

Maintainer 类会自动读取 `config.json` 中的 `storage` 配置，用于确定标准目录结构和默认项目根路径：

```json
{
  "storage": {
    "root_path": "/root/实验室仓库/项目文件/",
    "knowledge_base_dir": "知识库/",
    "knowledge_base_file": "index.json",
    "notes_dir": "知识库/笔记/",
    "reviews_dir": "知识库/综述/",
    "search_queries_dir": "临时数据/检索条件/",
    "extracted_notes_dir": "临时数据/笔记/"
  }
}
```

| 配置项 | 说明 |
|--------|------|
| `root_path` | 默认项目根目录（命令行 `--projects-dir` 的默认值） |
| `knowledge_base_dir` | 知识库根目录 |
| `notes_dir` | 笔记存放目录 |
| `reviews_dir` | 综述存放目录 |
| `search_queries_dir` | 检索条件存放目录 |
| `extracted_notes_dir` | NoteExtractor 提取笔记存放目录 |

## 元数据结构

元数据保存在项目根目录的 `元数据.json` 中，结构详见 [数据结构.md](数据结构.md)。

---

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 2.0.0 | 2026-04-22 | 重构为独立 maintainer 模块，增加检索条件管理和笔记保存功能 |
| 1.0.0 | 2026-04-22 | 初始版本，基于面向对象设计重构 |
