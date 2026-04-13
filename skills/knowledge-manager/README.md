# 检索文献

> 版本: 1.6.0  
> 维护者: 大管家  
> 创建时间: 2026-04-08  
> 更新内容: filter_by_criteria功能升级，支持多维度组合筛选，默认启用三级文献筛选规则

## 功能描述

本脚本用于进行文献检索，建立项目知识库并生成检索报告。使用Semantic Scholar作为唯一允许的学术文献检索来源，支持文献分级、分类和统计分析。

## 核心脚本
### 配置文件
- `config.json`：统一配置文件，包含LLM供应商、API地址、模型、存储路径、筛选规则等所有参数
- 支持多LLM供应商切换：火山引擎方舟、腾讯云LKE、腾讯云LKE规划版、OpenAI
- 所有配置修改无需改动代码，直接编辑config.json即可全局生效


### AcademicSearchSummarizer.py（推荐）

**一体化检索+LLM总结系统**，包含三个核心类：
- **Searcher**: 从Semantic Scholar检索文献，支持完整元数据补全
- **Summarizer**: 使用LLM判断文献类型和总结
- **AcademicSearchSummarizer**: 总类，协调检索和总结流程

**Python代码调用：**

```python
from AcademicSearchSummarizer import AcademicSearchSummarizer

# 初始化
ass = AcademicSearchSummarizer()

# 配置检索词（新格式：列表长度=轮次）
queries = {
    "负性思维与睡眠质量": [
        "rumination sleep quality",      # 轮次1
        "rumination insomnia",           # 轮次2
        "anxiety sleep quality",         # 轮次3
        "anxious thinking sleep",        # 轮次4
        "repetitive negative thinking sleep"  # 轮次5
    ]
}

# 执行完整流程（链式调用，支持自动补全完整元数据）
ass \
    .search(queries, limit=30) \
    .deduplicate() \
    .filter_by_year(2020) \
    .fetch_full_metadata() \
    .filter_by_criteria() \
    .summarize() \
    .save("output.json", "项目名称")
```

**命令行调用：**

```bash
# 检索并生成知识库
python3 AcademicSearchSummarizer.py search \
  --queries queries.json \
  --output result.json \
  --project "负性思维与睡眠质量" \
  --fetch-abstracts

# 补全已有知识库的完整元数据（摘要、DOI、期刊信息等）
python3 AcademicSearchSummarizer.py fill-metadata \
  --kb-path "./知识库/index.json"
```

## 快速开始示例

### 示例2：使用默认筛选规则（推荐）
```python
from AcademicSearchSummarizer import AcademicSearchSummarizer

ass = AcademicSearchSummarizer()

# 默认筛选规则自动生效：
# - 奠基文献：引用≥500，无时间限制，全部保留
# - 重要文献：引用≥50，近10年，全部保留  
# - 新近文献：近3年，实证研究，全部保留
ass \
    .search(queries, limit=30) \
    .deduplicate() \
    .fetch_full_metadata() \
    .filter_by_criteria()  # 不传参数自动使用默认规则
    .summarize() \
    .save("./知识库/")  # 自动保存为 知识库/index.json
```

### 示例3：自定义多维度筛选

### 示例2：导出主题笔记

```python
from AcademicSearchSummarizer import AcademicSearchSummarizer

ass = AcademicSearchSummarizer()

# 不需要LLM，直接导出
ass.export_topic_notes(
    topic="负性思维与睡眠质量",
    notes_dir="./笔记",
    kb_path="./知识库/index.json"
)
```

### 示例3：补全已有知识库的笔记

```python
from AcademicSearchSummarizer import AcademicSearchSummarizer

ass = AcademicSearchSummarizer()

# 需要LLM API key
ass.complete_notes("./知识库/index.json")
```

## 文件结构

```
检索文献/
├── AcademicSearchSummarizer.py      # 学术文献检索与总结系统（主脚本）
├── 总结笔记.md                       # 文献笔记总结SOP
├── SKILL.md                         # 给AI看的技能说明（完整方法文档）
├── README.md                        # 给人类看的说明（本文件）
├── 检索文献.md                       # 核心脚本（五要素SOP）
├── 检索报告格式.md                   # 检索报告模板
├── 知识库结构.md                     # 知识库JSON格式规范
└── __pycache__/                     # Python缓存
```

### 各文件详细说明

| 文件 | 功能 | 说明 |
|------|------|------|
| `AcademicSearchSummarizer.py` | 学术文献检索与总结系统 | 主脚本，整合检索、筛选、LLM分析、导出功能 |
| `总结笔记.md` | 文献笔记总结SOP | 手动总结文献笔记的标准操作流程 |
| `SKILL.md` | 技能文档 | 给AI看的完整技能说明，包含10个方法的详细文档 |
| `README.md` | 文件夹说明 | 本文件，给人类看的整体说明 |
| `检索文献.md` | 检索文献SOP | 完整的文献检索流程文档，包含Step 1-8详细步骤 |
| `检索报告格式.md` | 检索报告模板 | 定义检索报告的标准结构 |
| `知识库结构.md` | 知识库格式规范 | index.json标准格式，包含字段说明 |

## 环境变量配置

### Semantic Scholar API
```bash
export SEMANTIC_SCHOLAR_API_KEY="your-semantic-scholar-api-key"
```

### 腾讯云 LKEAP API（推荐）
```bash
export LKEAP_API_KEY="your-tencent-api-key"
export LKEAP_BASE_URL="https://api.lkeap.cloud.tencent.com/v1"
export LKEAP_MODEL="deepseek-v3.2"
```

### OpenAI API（可选）
```bash
export OPENAI_API_KEY="your-openai-api-key"
export OPENAI_MODEL="gpt-4o-mini"
```

## 默认筛选规则

无需任何参数，调用 `filter_by_criteria()` 自动启用：

| 类别 | 规则 | 处理方式 |
|------|------|----------|
| 🔴 奠基文献 | 引用量≥500，无时间限制 | 全部保留 |
| 🟡 重要文献 | 引用量50-500，近10年发表 | 全部保留 |
| 🔵 新近文献 | 近3年发表，类型为实证研究 | 全部保留 |

## 自定义筛选器示例

```python
# 多维度组合筛选，多个条件取并集
ass.filter_by_criteria({
    "高引顶刊": {
        "citations": {"min": 500, "max": None},
        "venue": ["Psychological Review", "JPSP"],
        "limit": 20
    },
    "近年研究": {
        "citations": {"min": 50, "max": 500},
        "years": {"min": 2022, "max": 2026},
        "limit": 50
    }
})
```

## 文献类型分类

### 初分类（基于规则）

| 类型 | 标记 | 判断标准 |
|------|------|----------|
| 实证 | 📊 | 摘要含 participant / sample / method / result |
| 综述 | 📖 | 标题含 review / meta-analysis / systematic review |
| 理论 | 💡 | 标题含 theoretical / theory / perspective / commentary |
| 待分类 | 📋 | 无法明确归类的文献 |

### 修订（再分类，基于LLM）

使用大语言模型对初分类结果进行验证和修正，生成对应的notes字段。

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 1.3.0 | 2026-04-13 | 重构为AcademicSearchSummarizer，整合检索和LLM总结 |
| 1.2.0 | 2026-04-13 | 添加academic_search.py重构版 |
| 1.1.0 | 2026-04-12 | 添加topic字段为列表格式 |
| 1.0.0 | 2026-04-08 | 初始版本 |
