---
name: 文献总结
description: 使用 LLM 分析文献，自动添加分类标签和结构化笔记
version: 2.0.0
author: Yang Quan
dependencies:
  - python>=3.9
  - openai
tools:
  - python
  - markdown
---

# 文献总结模块 (Summarizer)

Summarizer 类使用 LLM 分析文献内容，自动添加 labels（分类标签）和 notes（结构化笔记）字段。

## 快速开始

### 我想...

| 需求 | 方法 |
|------|------|
| 总结文献 | [`summarize()`](#1-总结文献) |

## 文件说明

| 文件 | 功能 |
|------|------|
| `Summarizer.py` | 文献总结主类 |

---

## 工作流示例

### 1. 总结文献

```python
from Summarizer import Summarizer

summarizer = Summarizer()
kb = summarizer.summarize(kb_path="my_kb.json")
```

---

## 方法详情

### `summarize(kb_path="index.json", progress_interval=10)`

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `kb_path` | str | "index.json" | 知识库文件路径 |
| `progress_interval` | int | 10 | 进度打印间隔 |

---

## 输出字段结构

### labels 字段
```python
{
    "type": "📊实证",  # 或 "📖综述" / "💡理论" / "📋待分类"
    "importance": "🔴奠基文献",  # 或 "🟡重要文献" / "🔵一般文献"
    "JCR": ""
}
```

### notes 字段

#### 实证文献
```python
{
    "研究问题": "...",
    "研究方法": "...",
    "研究结果": "...",
    "研究结论": "..."
}
```

#### 综述文献
```python
{
    "研究问题": "...",
    "研究结果": "...",
    "研究展望": "..."
}
```

#### 理论文献
```python
{
    "研究问题": "...",
    "理论观点": "..."
}
```

#### 待分类
```python
{
    "说明": "..."
}
```

---

## 命令行工具

### 总结文献
```bash
python3 Summarizer.py \
    --kb-path my_kb.json \
    --progress-interval 10
```

### 命令参数
| 参数 | 说明 |
|------|------|
| `--kb-path` | 知识库文件路径（默认: index.json） |
| `--progress-interval` | 进度打印间隔（默认: 10） |
| `--use-conversation` | 使用会话模式（默认不使用） |

### 输出示例
```bash
正在总结文献...
完成! 知识库: my_kb.json
  论文总数: 30
  实证文献: 20
  综述文献: 8
  理论文献: 2
```

---

## 配置说明

### LLM 配置
```python
{
    "base_url": "https://ark.cn-beijing.volces.com/api/v3",
    "default_model": "deepseek-v3-2-251201",
    "api_key_env": "ARK_API_KEY"
}
```

### 环境变量
```bash
# 火山引擎方舟
export ARK_API_KEY="your-ark-api-key"

# 腾讯云 tokenhub
export TOKENHUB_API_KEY="your-tencent-api-key"
```

---

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 2.0.0 | 2026-04-14 | 重构为独立 Summarizer 类 |
