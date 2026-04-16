---
name: 知识库管理
description: 知识库管理技能。包含：文献检索，文献总结，知识库合并、筛选、提取，综述撰写技能。当用户需要搜索某一主题的论文、阅读并总结文献、或生成一篇结构化的文献综述时，使用此技能。
version: 2.0.0
author: Yang Quan
dependencies:
  - python>=3.9
  - openai
  - requests
  - pypdf2
  - tiktoken
tools:
  - python
  - markdown
---

# 知识库管理技能包
本技能模拟一个“知识库管理经理”，协调四个子技能共同知识库管理。
你将严格按照“面向对象”的调度方式，实例化并调用以下三个类：

- **`Searcher`** (位于 `search/SKILL.md`)：负责检索并获取论文列表或加载已有知识库并更新。
- **`Summarizer`** (位于 `Summarize/SKILL.md`)：负责解析摘要并提取结构化笔记。
- **`Manager`**(位于 `Manage/SKILL.md`):负责知识库合并、筛选、提取。
- **`Synthesizer`** (位于 `synthesize/SKILL.md`)：负责将所有提取的笔记组织成一篇完整的综述、检查参考文献引用是否正确。
---
## 快速开始

我想...

| 需求 | 跳转 |
|------|------|
| 检索文献 | [search/SKILL.md](./search/SKILL.md) |
| 总结文献 | [summarize/SKILL.md](./summarize/SKILL.md) |
| 管理知识库 | [manage/SKILL.md](./manage/SKILL.md) |
| 写文献综述 | [synthesize/SKILL.md](./synthesize/SKILL.md) |
---
## 工作流示例

### 1. 检索文献
- 确定检索范围
```json
{
    "自传体记忆": [
        {"query": "autobiographical memory | personal memory", "limit": 30}
    ]
}
```
- 检索
```python
from search.Searcher import Searcher
searcher = Searcher()
queries = {
    "自传体记忆": [
        {"query": "autobiographical memory | personal memory", "limit": 30}
    ]
}
searcher.search(queries, kb_path="my_kb.json")
```

### 2. 总结文献
```python
from summarize.Summarizer import Summarizer
summarizer = Summarizer()
summarizer.summarize(kb_path="my_kb.json")
```

### 3. 导出笔记
```python
from manage.Manager import Manager
manager = Manager("my_kb.json")
manager.filter({"citations_min": 50}).save("笔记.json")
```
### 4. 撰写文献综述
- 读取`笔记.json`每篇notes
- 按照模板进行攥写
```
---

## 配置介绍
- `config.json`：统一配置文件，存放所有 API、模型、存储相关配置
- `README.md`：给人类看的说明文档
- `search/`：负责检索并获取论文列表或加载已有知识库并更新。
- `summarize/`：负责解析摘要并提取结构化笔记。
- `manage/`:负责知识库合并、筛选、提取。
- `synthesize/`：负责将所有提取的笔记组织成一篇完整的综述。
  - `reference_checker.py`：参考文献检查与修复类
---

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 3.0.0 | 2026-04-15 | 按面向对象思路重构，拆分为四个独立子模块 |
