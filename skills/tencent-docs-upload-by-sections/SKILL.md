---
name: tencent-docs-upload-by-sections
description: >
  腾讯云文档分段上传工具。当需要上传长文档到腾讯云文档时，将文档切分成多个段落逐段上传，
  避免内容截断问题。支持按二级标题、段落或固定行数切分，支持断点续传。
homepage: https://docs.qq.com/
metadata: { "openclaw": { "emoji": "📄", "requires": { "bins": ["mcporter", "python3"] } } }
---

# 腾讯云文档分段上传工具

将长Markdown文档切分成多个段落逐段上传到腾讯云文档，避免内容截断问题。

## 功能特性

- ✅ 智能切分：支持按二级标题、段落、固定行数切分
- ✅ 断点续传：支持从指定段落重新上传
- ✅ 状态报告：实时显示上传进度
- ✅ 错误处理：记录失败段落，支持重试
- ✅ 结果保存：生成JSON结果文件

## 前置条件

1. **mcporter已安装**：用于调用腾讯云文档API
2. **腾讯云文档已创建**：需要先创建一个空的腾讯云文档获取file_id
3. **Python 3**：用于运行上传脚本

## 使用方式

### 基本用法

```bash
python3 upload_by_sections.py \
  --file-id <腾讯云文档file_id> \
  --source-file <源Markdown文件路径>
```

### 完整参数

```bash
python3 upload_by_sections.py \
  --file-id <file_id> \
  --source-file <source_file> \
  --split-strategy <headers|paragraphs|lines> \
  --skip-first \
  --start-index <起始索引>
```

## 参数说明

| 参数 | 必填 | 说明 | 默认值 |
|------|------|------|--------|
| `--file-id` | ✅ | 腾讯云文档的file_id | - |
| `--source-file` | ✅ | 源Markdown文件路径 | - |
| `--split-strategy` | ❌ | 切分策略 | `headers` |
| `--skip-first` | ❌ | 跳过第一个段落 | `false` |
| `--start-index` | ❌ | 起始段落索引（断点续传） | `1` |

## 切分策略

### 1. 按二级标题切分（`headers`，默认）

按Markdown二级标题（`## ` 开头）切分，适合有章节结构的长文档。

**示例**：
```markdown
## 第一章
内容...

## 第二章
内容...

## 第三章
内容...
```

会切分成3个段落上传。

### 2. 按段落切分（`paragraphs`）

按空行切分，适合段落分明的文档。

### 3. 按固定行数切分（`lines`）

每50行切分一次，适合无结构的长文本。

## 使用流程

### 完整上传流程

1. **先创建空文档**
   ```bash
   mcporter call tencent-docs.create_smartcanvas_by_mdx \
     --args '{"title": "文档标题", "content_format": "markdown"}'
   ```
   保存返回的 `file_id`。

2. **分段上传内容**
   ```bash
   python3 upload_by_sections.py \
     --file-id <file_id> \
     --source-file document.md \
     --skip-first
   ```
   使用 `--skip-first` 跳过标题（空文档可能已有标题）。

### 断点续传

如果上传过程中部分段落失败，可以从失败的段落重新上传：

```bash
python3 upload_by_sections.py \
  --file-id <file_id> \
  --source-file document.md \
  --start-index 5
```

从第5个段落开始重新上传。

## 输出示例

```
正在切分段落...
共切分成 6 个段落
正在上传第 2/6 段...
✓ 第 2 段上传成功
正在上传第 3/6 段...
✓ 第 3 段上传成功
正在上传第 4/6 段...
✓ 第 4 段上传成功
正在上传第 5/6 段...
✓ 第 5 段上传成功
正在上传第 6/6 段...
✓ 第 6 段上传成功

==================================================
上传完成！
成功: 5/5
失败: 0/5
==================================================

结果已保存到: /tmp/tencent_upload_result_<file_id>.json
```

## 结果文件

上传完成后会在 `/tmp/` 目录生成JSON结果文件：

```json
{
  "file_id": "文档file_id",
  "source_file": "源文件路径",
  "total_sections": 6,
  "uploaded_sections": 5,
  "failed_sections": 0,
  "failed_indices": []
}
```

## 常见问题

### Q: 上传后发现内容重复怎么办？

A: 使用 `--skip-first` 参数跳过第一个段落。

### Q: 部分段落上传失败怎么办？

A: 查看结果文件中的 `failed_indices`，然后使用 `--start-index` 从失败的段落重新上传。

### Q: 如何获取腾讯云文档的file_id？

A: 创建文档时返回的结果中包含file_id，或者从文档URL中提取（如 `https://docs.qq.com/aio/<file_id>`）。

### Q: 支持哪些切分策略？

A: 三种：
- `headers`：按二级标题（## 开头）切分
- `paragraphs`：按空行切分
- `lines`：每50行切分

## 依赖

- Python 3
- mcporter（腾讯云文档MCP工具）
- json模块（Python标准库）
- argparse模块（Python标准库）
- subprocess模块（Python标准库）

## 技术实现

### 核心函数

- `split_into_sections()`: 文档切分函数
- `run_mcporter()`: 调用mcporter上传单段
- `upload_sections()`: 分段上传主函数

### 错误处理

- 实时显示上传成功/失败状态
- 记录失败的段落索引
- 生成结果JSON文件用于重试
