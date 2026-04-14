
# 检索文献

&gt; 版本: 2.1.0  
&gt; 维护者: 大管家  
&gt; 创建时间: 2026-04-08  
&gt; 更新时间: 2026-04-14  
&gt; 更新内容: Searcher.search()支持字典格式条件列表，每轮可单独设置query、limit、year、minCitationCount等

## 功能描述

本技能用于进行文献检索，建立项目知识库并生成检索报告。使用Semantic Scholar作为唯一允许的学术文献检索来源，支持文献分级、分类和统计分析。

## 核心架构

### 三个独立类

| 类 | 文件 | 功能 |
|----|------|------|
| **Searcher** | `Searcher.py` | 从Semantic Scholar获取数据，支持检索和更新两种模式 |
| **Summarizer** | `Summarizer.py` | 使用LLM分析文献，添加labels和notes字段 |
| **Manager** | `Manager.py` | 合并、筛选、保存知识库，支持链式调用 |

### 配置文件
- `config.json`：统一配置文件，存放所有API、模型、存储相关配置
- `SKILL.md`：给AI看的技能说明（完整方法文档）

---

## 快速开始

### 1. 检索文献并保存
```python
from Searcher import Searcher

searcher = Searcher()
queries = {
    "自传体记忆": [
        {"query": "autobiographical memory | personal memory", "limit": 30},
        {"query": "\"self-memory system\" Conway", "year": "2010-2025"},
        {"query": "autobiographical memory -childhood", "minCitationCount": 50}
    ],
    "数字记忆": [
        {"query": "digital memory | Google effect", "limit": 20},
        {"query": "photo taking memory", "year": "2020-2025", "minCitationCount": 20}
    ]
}
kb = searcher.search(queries, kb_path="my_kb.json")
```

### 2. 更新知识库元数据
```python
from Searcher import Searcher

searcher = Searcher()
kb = searcher.update(kb_path="my_kb.json")
```

### 3. 总结文献
```python
from Summarizer import Summarizer

summarizer = Summarizer()
kb = summarizer.summarize(kb_path="my_kb.json")
```

### 4. 合并知识库
```python
from Manager import Manager

manager = Manager()
manager.merge("kb1.json", "kb2.json", "kb3.json").save("merged.json", "合并项目")
```

### 5. 筛选文献
```python
from Manager import Manager

manager = Manager("my_kb.json")
manager.filter({
    "citations_min": 50,
    "types": ["📊实证", "📖综述"],
    "sort_by": "citationCount",
    "limit": 10
}).save("filtered.json")
```

---

## 完整示例

### 从零开始检索并总结
```python
from Searcher import Searcher
from Summarizer import Summarizer

# 1. 检索
searcher = Searcher()
queries = {
    "自传体记忆": [
        {"query": "autobiographical memory | personal memory", "limit": 30},
        {"query": "\"self-memory system\" Conway", "year": "2010-2025"},
        {"query": "autobiographical memory -childhood", "minCitationCount": 50}
    ]
}
searcher.search(queries, kb_path="my_project.json")

# 2. 更新元数据
searcher.update(kb_path="my_project.json")

# 3. 总结文献
summarizer = Summarizer()
summarizer.summarize(kb_path="my_project.json")
```

### 合并多个知识库并筛选
```python
from Manager import Manager

manager = Manager()
manager.merge("kb1.json", "kb2.json", "kb3.json")
manager.filter({
    "citations_min": 50,
    "types": ["📊实证", "📖综述"],
    "sort_by": "citationCount",
    "limit": 20
})
manager.save("final_kb.json", "最终项目")
```

---

## 检索规则建立指南

### 第一步：确定研究主题和关键词

**核心概念与同义词**
- 先列出你的核心研究概念
- 然后列出该概念的同义词、近义词、相关术语

**示例：研究"自传体记忆"**
- 核心概念：autobiographical memory
- 同义词：personal memory, life narrative, episodic memory
- 相关术语：self-memory system, life story, reminiscence

---

### 第二步：构建检索关键词组合

| 语法 | 说明 | 示例 |
|------|------|------|
| **空格** | AND关系（必须同时出现） | `autobiographical memory self` |
| `\|` | OR关系（任一即可） | `autobiographical memory \| personal memory` |
| `\"\"` | 精确短语匹配 | `\"self-memory system\"` |
| `-` | NOT关系（排除） | `autobiographical memory -childhood` |
| `()` | 优先级组合 | `(autobiographical \| personal) memory (self \| identity)` |

---

### 第三步：多主题多轮检索策略（每轮单独设置条件）

```python
queries = {
    "自传体记忆基础": [
        {
            "query": "autobiographical memory | personal memory",
            "limit": 30,
            "year": "2015-2025"
        },
        {
            "query": "\"self-memory system\" Conway",
            "limit": 20,
            "minCitationCount": 100
        },
        {
            "query": "autobiographical memory -childhood",
            "year": "2020-2025",
            "minCitationCount": 50
        }
    ],
    "自传体记忆功能": [
        {
            "query": "autobiographical memory function social | directive",
            "limit": 25,
            "venue": "Memory"
        },
        {
            "query": "autobiographical memory (self-continuity | identity)",
            "year": "2018-2025",
            "minCitationCount": 30
        }
    ]
}
```

**条件字典说明**
- 每个条件字典必须包含 `query` 字段（检索关键词）
- 其他字段可选：`limit`、`year`、`minCitationCount`、`venue`、`fields_of_study`、`publication_types`
- 支持全局默认参数（会被条件字典中的同名字段覆盖）

---

### 第四步：条件字典支持的所有字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `query` | str | **必填**，检索关键词 |
| `limit` | int | 本次检索数量（默认20，最大100） |
| `year` | str | 年份范围，如 `"2020-2023"` |
| `minCitationCount` | int | **客户端过滤**，最小引用量 |
| `venue` | str | 期刊/会议名称 |
| `fields_of_study` | str | 研究领域 |
| `publication_types` | str | 文献类型 |

---

## 可用选项

### 可用文献类型
- `Review` - 综述
- `JournalArticle` - 期刊论文
- `MetaAnalysis` - 元分析
- `Study` - 研究报告
- `Conference` - 会议论文
- `Book` - 书籍
- `BookSection` - 书籍章节

### 可用研究领域
- `Computer Science` - 计算机科学
- `Medicine` - 医学
- `Chemistry` - 化学
- `Biology` - 生物学
- `Materials Science` - 材料科学
- `Physics` - 物理学
- `Geology` - 地质学
- `Psychology` - 心理学
- `Art` - 艺术
- `History` - 历史学
- `Geography` - 地理学
- `Sociology` - 社会学
- `Business` - 商学
- `Political Science` - 政治学
- `Economics` - 经济学
- `Philosophy` - 哲学
- `Mathematics` - 数学
- `Engineering` - 工程学
- `Environmental Science` - 环境科学
- `Agricultural and Food Sciences` - 农业与食品科学
- `Education` - 教育学
- `Law` - 法学
- `Linguistics` - 语言学

---

## Manager筛选条件

| 键 | 类型 | 说明 |
|----|------|------|
| `year_min` | int | 最小年份 |
| `year_max` | int | 最大年份 |
| `citations_min` | int | 最小引用量 |
| `citations_max` | int | 最大引用量 |
| `topics` | List[str] | 主题列表（任意匹配） |
| `types` | List[str] | 文献类型列表（如 `["📊实证", "📖综述"]`） |
| `importance` | List[str] | 重要性列表（如 `["🔴奠基", "🟡重要"]`） |
| `venue` | str | 期刊/会议名称（模糊匹配） |
| `limit` | int | 返回前N篇（需与排序配合） |
| `sort_by` | str | 排序字段（如 `"citationCount"`, `"year"`） |
| `sort_desc` | bool | 是否降序（默认True） |

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

## 文件结构

```
检索文献/
├── Searcher.py              # 文献检索类
├── Summarizer.py            # 文献总结类
├── Manager.py               # 知识库管理类
├── SKILL.md                 # 给AI看的技能说明（完整方法文档）
├── README.md                # 给人类看的说明（本文件）
├── config.json              # 统一配置文件
├── _meta.json               # 技能元数据
└── __pycache__/             # Python缓存
```

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 2.1.0 | 2026-04-14 | Searcher.search()支持字典格式条件列表，每轮可单独设置query、limit、year、minCitationCount等 |
| 2.0.0 | 2026-04-14 | 重构为三个独立类：Searcher、Summarizer、Manager |
| 1.6.0 | 2026-04-08 | filter_by_criteria功能升级 |
| 1.3.0 | 2026-04-13 | 重构为AcademicSearchSummarizer |
| 1.0.0 | 2026-04-08 | 初始版本 |

