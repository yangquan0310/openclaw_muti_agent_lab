---
name: 腾讯文档分段上传
description: 长文档分段上传到腾讯文档，将长文档切分成多个段落，逐段上传到腾讯文档智能文档
version: 2.2.0
author: 大管家
dependencies:
  - python>=3.9
  - mcporter
tools:
  - python
  - mcporter
---

# 腾讯文档分段上传技能

将长文档切分成多个段落，逐段上传到腾讯文档智能文档。

## 快速开始

### 使用场景
文档超过 5000 字时，使用分段上传功能。

## 文件说明

| 文件 | 功能 |
|------|------|
| `upload_by_sections.py` | 分段上传主类（面向对象） |
| `SKILL.md` | 本技能说明文档 |

## 使用方法

### 面向对象使用

```python
from upload_by_sections import TencentDocUploader

uploader = TencentDocUploader(file_id="WRqFxRGmnIkj")
result = uploader.upload("文档.md")

# 查看结果
if result["success"]:
    print(f"上传成功: {result['uploaded_count']} 个段落")
else:
    print(f"上传失败: {result.get('error']}")
```

### 命令行使用

```bash
python3 upload_by_sections.py \
    --file-id WRqFxRGmnIkj \
    --file 文档.md
```

### 参数说明

| 参数 | 说明 | 必需 |
|------|------|------|
| `--file-id` | 腾讯文档 file_id | ✅ |
| `--file` | 要上传的文档路径 | ✅ |

## 类结构

### TencentDocUploader 类

**核心方法:**

| 方法 | 功能 |
|------|------|
| `__init__(file_id) | 初始化上传器，必需提供 file_id |
| `upload(file)` | 执行上传，返回结果字典 |
| `split_into_sections(file_path) | 将文档切分成段落（按 ## 标题） |
| `run_mcporter(action, content) | 调用 mcporter 执行操作 |

**返回结果字典结构:**

```python
{
    "success": bool,           # 是否成功
    "file_id": str,            # 文件 ID
    "file": str,               # 文档路径
    "sections_count": int,     # 总段落数
    "uploaded_count": int,        # 已上传段落数
    "start_time": str,         # 开始时间（ISO格式）
    "end_time": str,           # 结束时间（ISO格式）
    "error": str               # 错误信息（如果有）
}
```

## 工作原理

1. **初始化**
   - 必需提供 `file_id`

2. **切分段落**
   - 按 `## ` 开头的行检测新章节
   - 每个章节作为一个独立段落

3. **上传内容**
   - 跳过第一个标题（因为文档已创建）
   - 逐段使用 `smartcanvas.edit` 上传
   - 使用 `INSERT_AFTER` 操作追加内容

## 切分规则

- 按 `## ` 开头的行检测新章节
- 每个章节作为一个独立段落上传
- 保持原文的 Markdown 格式

## 命令行输出示例

```
============================================================
腾讯文档分段上传工具 v2.2.0
============================================================
文件 ID: WRqFxRGmnIkj
文档: 文档.md
============================================================
正在切分段落...
共切分成 8 个段落
正在上传第 2/8 段...
✓ 第 2 段上传成功
正在上传第 3/8 段...
✓ 第 3 段上传成功
...

============================================================
上传完成
============================================================
✓ 成功: 上传了 7/8 个段落
```

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 2.2.0 | 2026-04-15 | 参数重命名：--source-file 改为 --file |
| 2.1.0 | 2026-04-15 | 取消 --cloud-url 参数，简化接口，只保留 --file-id |
| 2.0.0 | 2026-04-15 | 面向对象重构，支持 cloud_url 参数，改进命令行接口 |
| 1.0.0 | 2026-04-15 | 初始版本 |
