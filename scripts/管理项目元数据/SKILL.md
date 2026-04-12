---
name: 管理项目元数据
description: >
  创建新项目元数据，维护本地文档，维护本地文档与云文档（飞书/腾讯文档）的映射关系。
metadata:
  openclaw:
    emoji: "📋"
    requires:
      bins: []
---

# 管理项目元数据

创建新项目元数据，维护本地文档，维护本地文档与云文档（飞书/腾讯文档）的映射关系。

## 触发条件

- 需要创建新项目元数据时
- 需要维护本地文档与云文档映射关系时

## 执行方式

主代理执行

## 依赖

- 目标项目已创建（对于映射云文档）

## 输入

### 创建元数据时：
- 项目ID：项目名称
- 项目标题：项目标题
- 创建日期：创建日期（YYYY-MM-DD）
- 项目描述：项目描述
- 状态：active / completed

### 元数据结构
```json
{
  "project_id": "项目名称",
  "title": "项目标题",
  "created_date": "创建日期",
  "status": "active",
  "version": "v1",
  "description": "项目描述",
  "directories": {},
  "files": [],
  "tags": [],
  "tasks": [],
  "cloud_doc_mappings": {}
}
```

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

## 步骤

### Step 1: 确定项目路径
- 项目路径：`~/实验室仓库/项目文件/项目名/`
- 检查路径是否存在，如果不存在则提示错误

### Step 2: 写入元数据.json
- 确认项目名称
- 确认本地文件路径
- 确认云文档URL和平台
- 写入到项目根目录
- 设置正确文件权限：644

### Step 3: 验证
- 验证JSON格式是否正确

## 输出

- 创建完成的 `元数据.json` 文件路径（创建时）
- 更新后的项目元数据.json（修改时）
