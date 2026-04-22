# Session: 2026-04-22 09:15:37 UTC

- **Session Key**: agent:steward:subagent:3be599d3-b7d5-48ea-95d2-7bd3959fb0d9
- **Session ID**: 5e6c71c9-412c-4536-bb4b-077a18afd79b
- **Source**: webchat

## Conversation Summary

user: [Wed 2026-04-22 17:14 GMT+8] [Subagent Context] You are running as a subagent (depth 1/1). Results auto-announce to your requester; do not busy-poll for status.

[Subagent Task]: 重构"管理项目元数据"技能，合并知识库管理功能，创建为manage-project技能，并添加MCP服务器支持。

## 当前技能状态
原技能位置：`/root/.openclaw/workspace/steward/skills/管理项目元数据/`
包含文件：
- SKILL.md - 技能说明文档
- 维护所有项目元数据.py - 批量维护脚本（过程式函数）
- README.md - 人类可读说明
- _meta.json - 技能元数据

## 重构需求

### 1. 技能重命名和迁移
- 新名称：manage-project
- 新位置：`/root/.openclaw/workspace/steward/skills/manage-project/`
- 删除旧目录

### 2. 目录结构变更
原结构：
```
project/
├── 文档/          # 用户上传文档
├── 草稿/          # 论文草稿
├── 终稿/          # 最终版本
└── 知识库/
    ├── 笔记/      # 笔记文件
    └── ...
```

新结构：
```
project/
├── 文档/              # 用户上传文档（保持不变）
├── 手稿/              # 写作助手、审稿助手等撰写的最新md文档（原"终稿"改名）
├── 知识库/
│   ├── 笔记/          # 笔记输出
│   └── 综述/          # 综述输出
└── 临时数据/
    └── 草稿/          # 备份版本、中间文件（原"草稿"移动到这里）
```

### 3. 文件重构

#### manage-project.py（原"维护所有项目元数据.py"重命名）
- 修改为面向对象：一个 `Project` 类，多个方法
- 核心参数为 project 文件夹路径
- 方法签名主要为 `(文件路径, **kwargs)` 形式
- 支持命令行和Python导入调用
- 同时支持命令行使用和.py文件调用

核心方法：
- `move_file(file_path, target_dir, **kwargs)` - 移动文件
- `rename_folder(old_name, new_name, **kwargs)` - 重命名文件夹
- `update_metadata(**kwargs)` - 更新元数据
- `organize(**kwargs)` - 自动整理项目文件
- `ensure_directories()` - 确保标准目录存在
- `get_documents()` - 获取用户上传文档列表
- `get_manuscripts()` - 获取手稿列表

#### SKILL.md
- 将数据结构部分另存为 `references/数据结构.md`
- 工作流改为"整理项目的各个环节"：
  1. 把中间文件归档到 `临时数据/` 下
  2. 综述输出在 `知识库/综述/`
  3. 笔记输出在 `知识库/笔记/`
  4. 把用户上传移动到 `文档/`
  5. 把撰写的最新md文档移动到 `手稿/`
  6. 把备份版本移动到 `临时数据/草稿/`

#### references/数据结构.md
- 包含完整的元数据结构说明
- 更新 directories 结构以匹配新布局

### 4. MCP服务器支持
按照 Skill-developer 技能的工作流5，添加MCP服务器支持：

#### 4.1 创建 mcp/server.py
- 使用 Python MCP SDK 创建 stdio 服务器
- 暴露以下工具：
  - `organize_project` - 整理项目文件
  - `move_file` - 移动文件
  - `rename_folder` - 重命名文件夹
  - `update_metadata` - 更新元数据
  - `list_projects` - 列出所有项目

#### 4.2 注册到 OpenClaw MCP
使用 gateway config.patch 注册到 openclaw.json 的 mcp.servers 中

### 5. 开发规范
严格按照 Skill-developer 技能的工作流执行：
1. 初始化项目结构（SKILL.md、README.md、_meta.json、references/、scripts/、mcp/）
2. 创建 Python 脚本（面向对象、类封装）
3. 撰写 SKILL.md
4. 创建 references/数据结构.md
5. 添加 mcp/server.py MCP服务器
6. 注册MCP服务器

### 6. 输出要求
创建 `/root/.openclaw/workspace/steward/skills/manage-project/` 目录，包含：
- `SKILL.md` - 技能说明文档
- `README.md` - 给人类看的说明
- `_meta.json` - 技能元数据
- `references/数据结构.md` - 数据结构说明
- `scripts/manage-project.py` - 核心Python类
- `mcp/server.py` - MCP服务器入口

然后注册MCP服务器到OpenClaw配置。

请严格按照 Skill-developer 技能的工作流1-5执行。
assistant:  
assistant:   
