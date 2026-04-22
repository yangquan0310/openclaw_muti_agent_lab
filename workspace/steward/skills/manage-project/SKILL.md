---
name: manage-project
description: 管理实验室项目文件结构，维护项目元数据，自动整理项目文件到标准目录。用于：(1) 创建或更新项目元数据，(2) 自动整理项目文件到文档/手稿/知识库/临时数据目录，(3) 移动或重命名项目内文件，(4) 扫描项目生成文件清单，(5) 维护本地文档与云文档映射关系。触发词：整理项目、项目整理、更新元数据、项目元数据、扫描项目、移动文件、重命名文件夹。
---

# 项目管理

管理实验室项目文件结构，维护项目元数据，自动整理项目文件到标准目录。

## 触发条件

- 需要整理项目文件时
- 需要创建或更新项目元数据时
- 需要移动/重命名项目内文件时
- 需要扫描项目生成文件清单时
- 需要维护本地文档与云文档映射关系时

## 项目标准目录结构

```
project/
├── 文档/              # 用户上传文档（docx/pdf/txt等）
├── 手稿/              # 写作助手、审稿助手等撰写的最新md文档
├── 知识库/
│   ├── 笔记/          # 笔记输出
│   └── 综述/          # 综述输出
└── 临时数据/
    └── 草稿/          # 备份版本、中间文件
```

## 工作流

### 整理项目文件

1. 确保标准目录存在（`ensure_directories`）
2. 扫描项目根目录，按文件类型自动分类：
   - 用户上传文档（docx/pdf等）→ `文档/`
   - 代理撰写的md文件 → `手稿/`
   - 综述文件（文件名含"综述"）→ `知识库/综述/`
   - 笔记文件 → `知识库/笔记/`
   - 备份/中间文件 → `临时数据/草稿/`
   - 其他文件 → `临时数据/`
3. 处理旧目录迁移：
   - 旧"草稿"目录内容 → `临时数据/草稿/`
   - 旧"终稿"目录中的md → `手稿/`
   - 旧"终稿"目录中的其他文件 → `文档/`
4. 更新元数据（`update_metadata`）

### 更新元数据

- 调用 `update_metadata()` 方法
- 自动扫描并更新 directories、documents、manuscripts、notes、reviews
- 支持传入额外字段覆盖（title、description、status、version、tags等）

### 移动文件

- 调用 `move_file(file_path, target_dir)`
- 自动处理文件名冲突（添加序号后缀）

### 重命名文件夹

- 调用 `rename_folder(old_name, new_name)`
- 检查目标是否已存在

## 使用方法

### 命令行

```bash
# 列出所有项目
python3 scripts/manage-project.py --action list

# 扫描项目（更新元数据）
python3 scripts/manage-project.py <项目名> --action scan

# 整理项目文件
python3 scripts/manage-project.py <项目名> --action organize

# 移动文件
python3 scripts/manage-project.py <项目名> --action move --file <源文件> --target <目标目录>

# 重命名文件夹
python3 scripts/manage-project.py <项目名> --action rename --old-name <旧名> --new-name <新名>

# 更新元数据
python3 scripts/manage-project.py <项目名> --action update --title <标题> --description <描述>
```

### Python 导入

```python
from scripts.manage-project import Project, list_projects

# 初始化项目
project = Project("项目名称")

# 整理文件
project.organize()

# 移动文件
project.move_file("旧路径/文件.md", "手稿/")

# 更新元数据
project.update_metadata(title="新标题", status="active")

# 列出所有项目
projects = list_projects()
```

## 数据结构

详细数据结构说明参见 [references/数据结构.md](references/数据结构.md)。

## MCP 工具

本技能提供 MCP 服务器，暴露以下工具：

- `organize_project` - 整理项目文件
- `move_file` - 移动文件
- `rename_folder` - 重命名文件夹
- `update_metadata` - 更新元数据
- `list_projects` - 列出所有项目

MCP 服务器入口：`mcp/server.py`
