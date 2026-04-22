---
name: manage-project
description: 管理项目文件的自动化整理和分类。当需要整理项目目录结构、归档中间文件、移动用户上传文档、管理手稿文件、整理知识库笔记和综述时使用。支持命令行和Python导入调用。
---

# 管理项目数据

自动化整理项目文件，维护标准目录结构，管理元数据。

## 触发条件

- 需要整理项目文件目录结构时
- 需要将中间文件归档到临时数据目录时
- 需要将用户上传文档移动到文档目录时
- 需要将撰写的最新md文档移动到手稿目录时
- 需要将备份版本移动到临时数据/草稿目录时
- 需要整理知识库中的笔记和综述输出时

## 文件说明

| 文件 | 功能 |
|------|------|
| `SKILL.md` | 本技能说明文档 |
| `scripts/manage-project.py` | 核心Python类，支持命令行和导入调用 |
| `references/数据结构.md` | 项目元数据结构说明 |
| `references/知识库管理.md` | 知识库管理技能适配指南 |

## 工作流

### Step 1: 初始化项目对象
```python
from scripts.manage_project import Project

project = Project("/path/to/project")
```

### Step 2: 整理项目的各个环节

1. **把中间文件归档到 `临时数据/` 下**
   ```python
   project.move_file("中间文件.txt", target_dir="临时数据")
   ```

2. **综述输出在 `知识库/综述/`**
   ```python
   project.move_file("综述.md", target_dir="知识库/综述")
   ```

3. **笔记输出在 `知识库/笔记/`**
   ```python
   project.move_file("笔记.md", target_dir="知识库/笔记")
   ```

4. **把用户上传移动到 `文档/`**
   ```python
   project.move_file("用户文档.docx", target_dir="文档")
   ```

5. **把撰写的最新md文档移动到 `手稿/`**
   ```python
   project.move_file("论文.md", target_dir="手稿")
   ```

6. **把备份版本移动到 `临时数据/草稿/`，检索条件.json 移动到 `临时数据/检索条件/`**
   ```python
   project.move_file("论文_backup.md", target_dir="临时数据/草稿")
   project.move_file("检索条件.json", target_dir="临时数据/检索条件")
   ```

7. **把NoteExtractor提取的笔记.md 移动到 `临时数据/笔记/`**
   ```python
   project.move_file("提取笔记.md", target_dir="临时数据/笔记")
   ```

### Step 3: 更新元数据
```python
project.update_metadata()
```

### Step 4: 重命名文件夹（如需调整）
```python
project.rename_folder("旧文件夹名", "新文件夹名")
```

## 命令行使用

```bash
# 整理单个项目
python3 scripts/manage-project.py /path/to/project

# 整理所有项目
python3 scripts/manage-project.py --all

# 预览模式（不实际执行）
python3 scripts/manage-project.py /path/to/project --dry-run
```

## Python导入使用

```python
from scripts.manage_project import Project

# 初始化项目
project = Project("/path/to/project")

# 自动整理
project.organize()

# 预览模式
project.organize(dry_run=True)

# 手动移动文件
project.move_file("文件.txt", target_dir="临时数据")

# 重命名文件夹
project.rename_folder("旧名", "新名")

# 更新元数据
project.update_metadata()
```

## 目录结构

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

## 数据结构

详见 [references/数据结构.md](references/数据结构.md)

## 版本历史

- **v1.0.0** (2026-04-22): 初始版本，基于面向对象设计重构
