# 知识库管理

> 版本: 2.1.0  
> 维护者: Yang Quan  
> 创建时间: 2026-04-08  
> 更新时间: 2026-04-15  
> 更新内容: 面向对象重构知识库管理，拆分为四个独立子模块

## 功能描述

本技能用于进行文献检索、文献总结、知识库管理和文献综述合成。使用 Semantic Scholar 作为学术文献检索来源，支持文献分级、分类和统计分析。

## 核心架构

### 四个独立模块

| 模块 | 目录 | 功能 | 对应类 |
|------|------|------|--------|
| **文献检索** | `search/` | 从 Semantic Scholar 获取数据，支持多主题多轮检索 | Searcher |
| **文献总结** | `summarize/` | 使用 LLM 分析文献，添加 labels 和 notes 字段 | Summarizer |
| **知识库管理** | `manage/` | 合并、筛选、保存知识库，支持链式调用 | Manager |
| **文献综述合成** | `synthesize/` | 基于知识库生成文献综述和研究现状 | Synthesizer |

### 配置文件
- `config.json`：统一配置文件，存放所有 API、模型、存储相关配置
- `SKILL.md`：给 AI 看的技能说明（主入口）

---

## 快速开始

### 我想...

| 需求 | 跳转 |
|------|------|
| 检索文献 | [search/SKILL.md](./search/SKILL.md) |
| 总结文献 | [summarize/SKILL.md](./summarize/SKILL.md) |
| 管理知识库 | [manage/SKILL.md](./manage/SKILL.md) |
| 写文献综述 | [synthesize/SKILL.md](./synthesize/SKILL.md) |

### 完整工作流

```python
# 1. 检索文献
from search.Searcher import Searcher
searcher = Searcher()
queries = {
    "自传体记忆": [
        {"query": "autobiographical memory | personal memory", "limit": 30}
    ]
}
searcher.search(queries, kb_path="my_kb.json")

# 2. 总结文献
from summarize.Summarizer import Summarizer
summarizer = Summarizer()
summarizer.summarize(kb_path="my_kb.json")

# 3. 管理知识库
from manage.Manager import Manager
manager = Manager("my_kb.json")
manager.filter({"citations_min": 50}).save("filtered.json")

# 4. 合成文献综述
from synthesize.Synthesizer import Synthesizer
synthesizer = Synthesizer()
synthesizer.synthesize(kb_path="filtered.json", output_path="review.md")
```

---

## 目录结构

```
knowledge-manager/
├── search/                   # 文献检索模块
│   ├── Searcher.py          # 文献检索类
│   ├── SKILL.md             # 检索模块说明
│   └── 检索报告格式.md      # 检索报告模板
├── summarize/                # 文献总结模块
│   ├── Summarizer.py        # 文献总结类
│   └── SKILL.md             # 总结模块说明
├── manage/                   # 知识库管理模块
│   ├── Manager.py           # 知识库管理类
│   └── SKILL.md             # 管理模块说明
├── synthesize/               # 文献综述合成模块
│   ├── SKILL.md             # 综述合成模块说明
│   ├── 文献综述脚本.md      # 文献综述撰写脚本
│   ├── 文献综述模板         # 文献综述模板
│   └── 研究现状模板.md      # 研究现状模板
├── SKILL.md                  # 主技能说明（AI 入口）
├── README.md                 # 给人类看的说明（本文件）
├── config.json               # 统一配置文件
├── _meta.json                # 技能元数据
└── __pycache__/              # Python 缓存
```

---

## 环境变量配置

### Semantic Scholar API
```bash
export SEMANTIC_SCHOLAR_API_KEY="your-semantic-scholar-api-key"
```

### LLM API（Summarizer）
```bash
# 火山引擎方舟（推荐）
export ARK_API_KEY="your-ark-api-key"

# 腾讯云 LKEAP
export LKEAP_API_KEY="your-tencent-api-key"
```

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 2.1.0 | 2026-04-15 | 面向对象重构知识库管理，拆分为四个独立子模块 |
| 2.0.0 | 2026-04-14 | 重构为三个独立类：Searcher、Summarizer、Manager |
| 1.6.0 | 2026-04-08 | filter_by_criteria 功能升级 |
| 1.3.0 | 2026-04-13 | 重构为 AcademicSearchSummarizer |
| 1.0.0 | 2026-04-08 | 初始版本 |
