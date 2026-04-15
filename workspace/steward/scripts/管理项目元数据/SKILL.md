---
name: 管理项目元数据
description: 创建新项目元数据，维护本地元数据，维护本地文档与云文档（飞书/腾讯文档）的映射关系。
version: 1.0.0
author: 大管家
dependencies:
  - python3
tools:
  - markdown
---

# 管理项目元数据

创建新项目元数据，维护本地元数据，维护本地文档与云文档（飞书/腾讯文档）的映射关系。

## 触发条件

- 需要创建新项目元数据时
- 需要维护本地文档与云文档映射关系时


## 工作流

### Step 1: 确定项目路径
- 项目路径：`~/实验室仓库/项目文件/项目名/`
- 检查路径是否存在，如果不存在则提示错误

### Step 2: 维护元数据.json
- 确认项目名称
- 确认本地文件路径
- 确认云文档URL和平台
- 确认元数据内容是否符合`元数据结构`小节
- 设置正确文件权限：644

### Step 3: 验证
- 验证JSON格式是否正确

## 文件说明

| 文件 | 功能 |
|------|------|
| `SKILL.md` | 本技能说明文档 |
| `维护所有项目元数据.py` | 批量维护所有项目元数据的Python脚本 |

## 使用方法

### 批量维护所有项目元数据
```bash
cd /root/实验室仓库/项目文件/
python3 维护所有项目元数据.py
```

**功能说明**：
- 自动检测所有项目
- 确保标准目录存在（文档/草稿/终稿/知识库）
- 自动更新 directories 结构（根据实际文件夹）
- 自动扫描 documents（文档和终稿目录）
- 保存元数据并设置权限 644

## 元数据结构
```json
{
  "project_id": "项目名称",
  "title": "项目标题",
  "created_date": "创建日期",
  "status": "active",
  "version": "v1",
  "description": "项目描述",
  "directories": {},
  "documents": [],
  "tags": [],
  "cloud_doc_mappings": {}
}
```

### directories结构
根据目前的文件夹目录更新directories结构
```json
{
  "文档": "文档/",
  "草稿": "草稿/",
  "终稿": "终稿/",
  "知识库": "知识库/"
}
```

字段表
| 字段 | 值类型 | 说明 |
|------|--------|------|
| 文档 | str | 用户上传文档的目录路径 |
| 草稿 | str | 论文草稿的目录路径 |
| 终稿 | str | 最终版本的目录路径 |
| 知识库 | str | 项目专属知识库的目录路径 |

### documents结构
只记录代理撰写的非草稿文档和用户上传的文档。
```json
[
  {
    "title": "文档标题",
    "version": "v1",
    "path": "文档/文档标题.md",
    "type": "user_uploaded"
  }
]
```

字段表
| 字段 | 值类型 | 说明 |
|------|--------|------|
| title | str | 文档标题 |
| version | str | 文档版本号（如 v1、v2） |
| path | str | 文档相对路径 |
| type | str | 文档类型：user_uploaded（用户上传）或 agent_written（代理撰写） |

### tags结构
```json
[
  "AI降重",
  "提示工程",
  "学术写作"
]
```

字段表
| 字段 | 值类型 | 说明 |
|------|--------|------|
| - | str | 标签字符串，用于项目分类和检索 |

### cloud_doc_mappings 结构
```json
{
  "文档标题": {
    "local_path": "文档标题.md",
    "cloud": [
      {
        "platform": "feishu",
        "cloud_url": "https://...",
        "cloud_id": "doc-xxx",
        "created_at": "ISO时间戳",
        "updated_at": "ISO时间戳"
      }
    ]
  }
}
```

字段表
| 字段 | 值类型 | 说明 |
|------|--------|------|
| local_path | str | 本地文档路径 |
| platform | str | 云文档平台：feishu（飞书）或 tencent（腾讯文档） |
| cloud_url | str | 云文档URL |
| cloud_id | str | 云文档ID |
| created_at | str | 云文档创建时间（ISO格式） |
| updated_at | str | 云文档更新时间（ISO格式） |

