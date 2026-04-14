
---
name: 检索文献
description: &gt;
  进行文献检索，建立项目知识库并生成检索报告。
  使用Semantic Scholar进行学术文献检索，支持文献分级、分类和统计。
metadata:
  openclaw:
    emoji: "📚"
    requires:
      bins: []
---

## 文件说明

| 文件 | 功能 | 说明 |
|------|------|------|
| `Searcher.py` | 文献检索 | 从Semantic Scholar获取数据，支持检索和更新两种模式 |
| `Summarizer.py` | 文献总结 | 使用LLM分析文献，添加labels和notes字段 |
| `Manager.py` | 知识库管理 | 合并、筛选、保存知识库，支持链式调用 |

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
kb = searcher.search(queries, kb_path="my_kb.json","limit": 30)
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

## 完整方法文档

### 核心配置
**LLM配置 (Summarizer)**
```python
{
    "base_url": "https://ark.cn-beijing.volces.com/api/v3",
    "default_model": "deepseek-v3-2-251201",
    "api_key_env": "ARK_API_KEY"
}
```

**Semantic Scholar配置 (Searcher)**
```python
{
    "api_key_env": "SEMANTIC_SCHOLAR_API_KEY",
    "default_fields": "paperId,authors,year,title,venue,citationCount,journal,externalIds,url,abstract",
    "default_publication_types": "Review,MetaAnalysis,JournalArticle,Study"
}
```

### Searcher 检索规则建立指南

#### 第一步：确定研究主题和关键词

**核心概念与同义词**
- 先列出你的核心研究概念
- 然后列出该概念的同义词、近义词、相关术语

**示例：研究"自传体记忆"**
- 核心概念：autobiographical memory
- 同义词：personal memory, life narrative, episodic memory
- 相关术语：self-memory system, life story, reminiscence

---

#### 第二步：构建检索关键词组合

**方法1：基础检索（AND关系）**
- 多个关键词用空格分隔，表示必须同时出现
- 示例：`autobiographical memory self`
  → 匹配同时包含 "autobiographical"、"memory"、"self" 的文献

**方法2：扩展检索（OR关系）**
- 用 `|` 分隔同义词，表示任一即可
- 示例：`autobiographical memory | personal memory`
  → 匹配包含 "autobiographical memory" 或 "personal memory" 的文献

**方法3：精确短语检索**
- 用双引号 `""` 包裹短语，必须精确匹配
- 示例：`"self-memory system"`
  → 匹配精确短语 "self-memory system"，而不是分散的 "self" 和 "memory"

**方法4：排除检索（NOT关系）**
- 用 `-` 前缀排除不需要的术语
- 示例：`autobiographical memory -childhood`
  → 匹配包含 "autobiographical memory" 但不包含 "childhood" 的文献

**方法5：组合使用（优先级括号）**
- 用 `()` 组合复杂查询
- 示例：`(autobiographical memory | personal memory) (self | identity)`
  → 匹配 (自传体记忆 或 个人记忆) 且 (自我 或 身份) 的文献

---

#### 第三步：多主题多轮检索策略（每轮单独设置条件）

**推荐做法**
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

#### 第四步：条件字典支持的所有字段

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

## 核心方法

### Searcher 类

#### `search(queries, kb_path="index.json", fields=None, deduplicate=True, **global_params)`
**功能**: 多主题多轮检索（每轮可单独设置条件），合并到现有知识库，保存

**参数**:
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `queries` | Dict[str, List[Dict]] | 必填 | 多主题字典，格式 `{主题名: [条件字典列表]}`，每个条件字典必须包含 `query` 键 |
| `kb_path` | str | "index.json" | 知识库文件路径 |
| `fields` | str | None | 返回字段，默认使用类属性FIELDS |
| `deduplicate` | bool | True | 是否对结果去重（基于paperId） |
| `**global_params` | - | - | 全局默认参数（会被条件字典中的同名字段覆盖） |

**条件字典支持的字段**:
| 字段 | 类型 | 说明 |
|------|------|------|
| `query` | str | **必填**，检索关键词 |
| `limit` | int | 本次检索数量（默认20，最大100） |
| `year` | str | 年份范围，如 `"2020-2023"` |
| `minCitationCount` | int | **客户端过滤**，最小引用量 |
| `venue` | str | 期刊/会议名称 |
| `fields_of_study` | str | 研究领域 |
| `publication_types` | str | 文献类型 |

**返回**: 知识库字典（包含papers列表）

---

#### `update(kb_path="index.json", fields=None)`
**功能**: 加载知识库，批量补全元数据（volume、pages、doi等），保存

**参数**:
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `kb_path` | str | "index.json" | 知识库文件路径 |
| `fields` | str | None | 请求字段，默认使用类属性FIELDS |

**返回**: 更新后的知识库字典

---

### Summarizer 类

#### `summarize(kb_path="index.json", progress_interval=10)`
**功能**: 分析知识库中所有论文，添加labels和notes字段，保存并返回知识库

**参数**:
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `kb_path` | str | "index.json" | 知识库文件路径 |
| `progress_interval` | int | 10 | 进度打印间隔 |

**返回**: 更新后的知识库字典

**labels字段结构**:
```python
{
    "type": "📊实证",  # 或 "📖综述" / "💡理论" / "📋待分类"
    "importance": "🔴奠基文献",  # 或 "🟡重要文献" / "🔵一般文献"
    "JCR": ""
}
```

**notes字段结构**:
- 实证文献: `{"研究问题": "...", "研究方法": "...", "研究结果": "...", "研究结论": "..."}`
- 综述文献: `{"研究问题": "...", "研究结果": "...", "研究展望": "..."}`
- 理论文献: `{"研究问题": "...", "理论观点": "..."}`
- 待分类: `{"说明": "..."}`

---

### Manager 类

#### `merge(*kb_paths, deduplicate=True)`
**功能**: 合并一个或多个知识库文件（去重），支持链式调用

**参数**:
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `*kb_paths` | str | 必填 | 知识库文件路径（可传入多个） |
| `deduplicate` | bool | True | 是否全局去重（基于paperId） |

**返回**: self（支持链式调用）

---

#### `filter(conditions)`
**功能**: 按条件筛选当前知识库，支持链式调用

**参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| `conditions` | Dict | 筛选条件字典 |

**支持的筛选条件**:
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

**返回**: self（支持链式调用）

---

#### `save(output_path, project_name="")`
**功能**: 保存当前知识库数据到文件，支持链式调用

**参数**:
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `output_path` | str | 必填 | 输出文件路径 |
| `project_name` | str | "" | 项目名称（会更新到知识库中） |

**返回**: 保存的文件路径

---

#### `get_kb()`
**功能**: 返回当前知识库字典

**返回**: 知识库字典

---

#### `get_papers()`
**功能**: 返回当前论文列表

**返回**: 论文列表

---

## 工作流

### 完整检索流程（从检索到保存）

1. **确定检索内容**：包括检索关键词、研究类型、时间、期刊和学科
2. **调用Searcher.search()**：多主题多轮检索（每轮可单独设置条件）
3. **调用Searcher.update()**：批量补全元数据（可选）
4. **调用Summarizer.summarize()**：分析文献，添加labels和notes
5. **调用Manager.merge()/filter()**：合并或筛选知识库（可选）
6. **调用Manager.save()**：保存最终结果

## 输出格式

### 知识库JSON结构
```json
{
  "version": "1.0.0",
  "project": "项目名称",
  "created_at": "2026-04-13T03:33:00",
  "updated_at": "2026-04-13T03:33:00",
  "statistics": {
    "total_count": 38,
    "total_citations": 12345,
    "foundation_count": 2,
    "important_count": 6,
    "general_count": 30,
    "empirical_count": 30,
    "review_count": 4,
    "theory_count": 0
  },
  "papers": [
    {
      "paperId": "ff9c8a3d364d027da407dd772be53cb237a349f2",
      "authors": ["张敏", "李华", "王伟"],
      "year": 2022,
      "title": "怀旧技术在降低老年人压力水平中的应用效果：系统综述",
      "venue": "中国老年学杂志",
      "volume": "42",
      "issue": "5",
      "pages": "1123-1128",
      "doi": "10.3969/j.issn.1005-9202.2022.05.032",
      "url": "https://example.com/paper_001",
      "abstract": "目的：系统评价怀旧技术对降低老年人压力水平的效果。方法：检索PubMed、Google Scholar等数据库，筛选5篇2013-2023年发表的符合纳入标准的期刊。结果：怀旧技术可有效降低老年人压力，是一种安全的非药物干预方法。结论：建议在社区养老机构推广应用。",
      "topic": ["怀旧技术", "老年人", "压力缓解"],
      "citationCount": 45,
      "labels": {
        "type": "📖综述",
        "importance": "🔴奠基文献",
        "JCR": ""
      },
      "notes": {
        "研究问题": "...",
        "研究结果": "...",
        "研究展望": "..."
      }
    }
  ]
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `version` | str | 知识库版本号 |
| `project` | str | 项目名称 |
| `created_at` | str | 创建时间（ISO格式） |
| `updated_at` | str | 更新时间（ISO格式） |
| `statistics` | Dict | 统计信息 |
| `papers` | List[Dict] | 论文列表 |
| `paperId` | str | Semantic Scholar论文ID |
| `authors` | List[str] | 作者列表 |
| `year` | int | 发表年份 |
| `title` | str | 论文标题 |
| `venue` | str | 期刊/会议名称 |
| `volume` | str | 卷号 |
| `issue` | str | 期号 |
| `pages` | str | 页码 |
| `doi` | str | DOI号 |
| `url` | str | 论文URL |
| `abstract` | str | 摘要 |
| `topic` | List[str] | 主题列表 |
| `citationCount` | int | 引用量 |
| `labels` | Dict | 标签（type、importance、JCR） |
| `notes` | Dict | 笔记（根据文献类型不同结构不同） |

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| v2.1.0 | 2026-04-14 | Searcher.search()支持字典格式条件列表，每轮可单独设置query、limit、year、minCitationCount等 |
| v2.0.0 | 2026-04-14 | 重构为三个独立类：Searcher、Summarizer、Manager |
| v1.0.0 | 2026-04-13 | 初始版本 |

