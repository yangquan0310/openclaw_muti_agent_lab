# manage-project

项目文件自动化整理工具。

## 功能

- 自动化整理项目目录结构
- 归档中间文件到临时数据目录
- 管理手稿文件（写作助手撰写的最新md文档）
- 整理知识库中的笔记和综述
- 维护项目元数据

## 目录结构

```
project/
├── 文档/              # 用户上传的文档
├── 手稿/              # 写作助手、审稿助手等撰写的最新md文档
├── 知识库/
│   ├── 笔记/          # 笔记输出
│   └── 综述/          # 综述输出
└── 临时数据/
    └── 草稿/          # 备份版本、中间文件
```

## 使用方法

### 命令行

```bash
# 整理单个项目
python3 scripts/manage-project.py /path/to/project

# 整理所有项目
python3 scripts/manage-project.py --all
```

### Python导入

```python
from scripts.manage_project import Project

# 初始化项目
project = Project("/path/to/project")

# 移动文件
project.move_file("文件.txt", target_dir="临时数据")

# 重命名文件夹
project.rename_folder("旧名", "新名")

# 更新元数据
project.update_metadata()
```

## 文件说明

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 技能说明文档 |
| `scripts/manage-project.py` | 核心Python脚本 |
| `references/数据结构.md` | 元数据结构说明 |
