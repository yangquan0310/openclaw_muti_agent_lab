---
name: 检索文献
description: >
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
| `检索文献.md` | 检索文献SOP | 完整的文献检索流程文档，包含Step 1-8详细步骤 |
| `检索报告格式.md` | 检索报告模板 | 定义检索报告的标准结构：检索概况、文献统计、高引用文献 |
| `知识库结构.md` | 知识库格式规范 | index.json标准格式，包含字段说明和使用规范 |
| `AcademicSearchSummarizer.py` | 学术文献检索与总结系统 | 整合检索、筛选、LLM分析、导出的一体化脚本 |
| `总结笔记.md` | 文献笔记总结SOP | 手动总结文献笔记的标准操作流程 |
| `README.md` | 文件夹说明 | 检索文献文件夹的整体说明 |

## AcademicSearchSummarizer 完整方法文档

### 类初始化

```python
from AcademicSearchSummarizer import AcademicSearchSummarizer

ass = AcademicSearchSummarizer(
    semantic_scholar_key=None,  # Semantic Scholar API key（可选，默认从环境变量读取）
    llm_key=None,               # LLM API key（可选，默认从环境变量读取）
    llm_base_url="https://api.lkeap.cloud.tencent.com/v1",  # LLM API base URL
    llm_model="deepseek-v3.2"   # LLM 模型名称
)
```

**环境变量配置：**
```bash
export SEMANTIC_SCHOLAR_API_KEY="your-semantic-scholar-api-key"
export LKEAP_API_KEY="your-tencent-api-key"
export LKEAP_BASE_URL="https://api.lkeap.cloud.tencent.com/v1"
export LKEAP_MODEL="deepseek-v3.2"
```

---

### 核心方法一览

| 方法名 | 功能 | 链式调用 | 需要LLM |
|--------|------|----------|---------|
| `search()` | 多主题多轮次检索 | ✅ | ❌ |
| `deduplicate()` | 按标题去重 | ✅ | ❌ |
| `filter_by_year()` | 按年份筛选 | ✅ | ❌ |
| `sort_by_citations()` | 按引用量排序 | ✅ | ❌ |
| `filter_by_criteria()` | 多维度组合筛选文献 | ✅ | ❌ |
| `fetch_full_metadata()` | 批量获取完整元数据（摘要、DOI、期刊信息等） | ✅ | ❌ |
| `summarize()` | 使用LLM分析文献类型和生成笔记 | ✅ | ✅ |
| `load_knowledge_base()` | 从index.json加载文献 | ✅ | ❌ |
| `to_knowledge_base()` | 转换为知识库格式 | ❌ | ❌ |
| `save()` | 保存知识库到文件 | ❌ | ❌ |
| `export_topic_notes()` | 导出特定主题的笔记（JSON格式） | ❌ | ❌ |
| `complete_notes()` | 给知识库补全笔记 | ❌ | ✅ |
| `fill_metadata_from_kb()` | 直接补全已有知识库的完整元数据 | ❌ | ❌ |

---

### 1. search(queries, limit=20)

**功能：** 多主题多轮次检索文献

**参数：**
- `queries`: 检索词字典，格式 `{主题: [关键词列表]}`，列表长度即为轮次
- `limit`: 每轮检索数量，默认20

**返回值：** `self`（支持链式调用）

**示例：**
```python
queries = {
    "负性思维与睡眠质量": [
        "rumination sleep quality",      # 轮次1
        "rumination insomnia",           # 轮次2
        "anxiety sleep quality",         # 轮次3
        "anxious thinking sleep",        # 轮次4
        "repetitive negative thinking sleep"  # 轮次5
    ]
}
```        3: ["repetitive negative thinking sleep"]
    }
}

ass.search(queries, limit=30)
```

---

### 2. deduplicate()

**功能：** 按标题去重，保留唯一文献

**返回值：** `self`（支持链式调用）

**示例：**
```python
ass.deduplicate()
```

---

### 3. filter_by_year(min_year)

**功能：** 按年份筛选文献

**参数：**
- `min_year`: 最小年份，只保留该年份之后的文献

**返回值：** `self`（支持链式调用）

**示例：**
```python
ass.filter_by_year(2020)  # 只保留2020年及之后的文献
```

---

### 4. sort_by_citations()

**功能：** 按引用量降序排序

**返回值：** `self`（支持链式调用）

**示例：**
```python
ass.sort_by_citations()
```

---

### 5. filter_by_criteria(filters=None, **kwargs)

**功能：** 多维度组合筛选文献

**默认规则（不传参数时自动生效）：**
- 🔴 奠基文献：引用≥500，无时间限制，全部保留
- 🟡 重要文献：引用≥50，近10年，全部保留
- 🔵 新近文献：近3年，实证研究，全部保留

**参数：**
- `filters`: 筛选条件字典，支持多维度组合，多个filter之间取并集
  - 支持维度：
    - `citations`: {"min": int, "max": int} - 引用量范围
    - `years`: {"min": int, "max": int} - 发表年份范围
    - `venue`: list - 期刊/会议名称列表
    - `limit`: int - 本条件最多保留数量
- `**kwargs`: 兼容旧版参数调用方式

**返回值：** `self`（支持链式调用）

**示例1：默认筛选（推荐）**
```python
ass.filter_by_criteria()  # 自动应用默认三级筛选规则
```

**示例2：自定义多维度筛选**
```python
ass.filter_by_criteria({
    "高引顶刊": {
        "citations": {"min": 500, "max": None},
        "years": {"min": 2020, "max": 2026},
        "venue": ["Psychological Review", "Journal of Personality and Social Psychology"],
        "limit": 20
    },
    "近年研究": {
        "citations": {"min": 50, "max": 500},
        "years": {"min": 2022, "max": 2026},
        "limit": 50
    }
})
```

**示例3：旧版参数兼容**
```python
ass.filter_by_criteria(
    foundation_min=500,
    important_min=50,
    foundation_limit=10
)
```

---

### 6. fetch_full_metadata(paper_ids=None)

**功能：** 批量获取文献的完整元数据（摘要、DOI、期刊信息、卷期页码、引用量、PDF链接等）

**说明：** Semantic Scholar搜索接口返回的信息不完整，此方法会调用详情接口获取所有可用元数据

**获取的字段包括：**
- `abstract`: 完整摘要
- `venue`: 会议/期刊名称
- `journal_name`: 期刊全称
- `journal_volume`: 卷号
- `journal_issue`: 期号
- `journal_pages`: 页码范围
- `doi`: 文献DOI
- `citationCount`: 最新引用量
- `isOpenAccess`: 是否开放获取
- `openAccessPdf`: PDF下载链接
- `author_names`: 完整作者列表

**参数：**
- `paper_ids`: 需要补全信息的文献ID列表，None表示补全所有文献

**返回值：** `self`（支持链式调用）

**示例：**
```python
# 检索后自动补全所有元数据
ass.search(queries)\
    .deduplicate()\
    .fetch_full_metadata()  # 补全完整信息
    .summarize()\
    .save("output.json")
```

---

### 7. summarize()

**功能：** 使用LLM分析文献，自动判断类型并生成笔记

**返回值：** `self`（支持链式调用）

**说明：** 需要设置 `LKEAP_API_KEY` 环境变量

**示例：**
```python
ass.summarize()
```

**生成的字段：**
- `labels.type`: 📊实证 / 📖综述 / 💡理论 / 📋待分类
- `labels.importance`: 🔴奠基 / 🟡重要 / 🔵一般
- `labels.confidence`: 分类置信度（0-1）
- `notes`: 根据文献类型生成的不同格式笔记

---

### 7. to_knowledge_base(project_name="")

**功能：** 将文献列表转换为标准知识库格式

**参数：**
- `project_name`: 项目名称

**返回值：** 知识库字典

**示例：**
```python
kb = ass.to_knowledge_base("负性思维与睡眠质量")
```

**返回结构：**
```json
{
  "version": "1.0.0",
  "project": "项目名称",
  "created_at": "2026-04-13T03:33:00",
  "updated_at": "2026-04-13T03:33:00",
  "statistics": {
    "total_count": 38,
    "foundation_count": 2,
    "important_count": 6,
    "general_count": 30,
    "empirical_count": 30,
    "review_count": 4,
    "theory_count": 0
  },
  "papers": [...]
}
```

---

### 8. save(output_path, project_name="")

**功能：** 保存知识库到JSON文件

**参数：**
- `output_path`: 输出文件路径
- `project_name`: 项目名称

**示例：**
```python
ass.save("./知识库/index.json", "负性思维与睡眠质量")
```

---

### 9. export_topic_notes(topic, notes_dir, kb_path=None)

**功能：** 导出特定主题的笔记到笔记文件夹（JSON格式，index.json的子集）

**参数：**
- `topic`: 主题名称
- `notes_dir`: 笔记文件夹路径
- `kb_path`: 知识库文件路径（可选，如果已加载则不需要）

**返回值：** 导出的笔记文件路径

**示例：**
```python
# 从已有知识库导出
ass.export_topic_notes(
    topic="负性思维与睡眠质量",
    notes_dir="./笔记",
    kb_path="./知识库/index.json"
)

# 或从内存中的文献导出
ass.export_topic_notes(
    topic="负性思维与睡眠质量",
    notes_dir="./笔记"
)
```

**输出文件结构：**
```json
{
  "version": "1.0.0",
  "topic": "负性思维与睡眠质量",
  "source": "./知识库/index.json",
  "created_at": "2026-04-13T03:33:00",
  "statistics": {
    "total_count": 38,
    "empirical_count": 30,
    "review_count": 4,
    "theory_count": 0,
    "foundation_count": 2,
    "important_count": 6,
    "general_count": 30
  },
  "papers": [...]
}
```

---

### 10. complete_notes(kb_path, paper_ids=None)

**功能：** 给知识库补全笔记（对缺少notes或type的文献使用LLM分析）

**参数：**
- `kb_path`: 知识库文件路径
- `paper_ids`: 需要补全的文献ID列表（可选，None表示全部）

**返回值：** `self`（支持链式调用）

**说明：** 需要设置 `LKEAP_API_KEY` 环境变量

**示例：**
```python
# 补全所有缺少笔记的文献
ass.complete_notes("./知识库/index.json")

# 或补全指定文献
ass.complete_notes(
    "./知识库/index.json",
    paper_ids=["paper_001", "paper_002"]
)
```

---

### 11. fill_metadata_from_kb(kb_path, paper_ids=None)

**功能：** 直接补全已有index.json中的完整元数据（摘要、DOI、期刊信息、卷期页码等）

**参数：**
- `kb_path`: 知识库文件路径
- `paper_ids`: 需要补全信息的文献ID列表（可选，None表示补全所有）

**返回值：** 成功补全的文献数量

**示例：**
```python
# 补全所有元数据
count = ass.fill_metadata_from_kb("./知识库/index.json")

# 或补全指定文献
count = ass.fill_metadata_from_kb(
    "./知识库/index.json",
    paper_ids=["paper_001", "paper_002"]
)
```

---

## 完整工作流示例

### 工作流1：完整检索流程（从检索到保存）

```python
from AcademicSearchSummarizer import AcademicSearchSummarizer

ass = AcademicSearchSummarizer()

queries = {
    "负性思维与睡眠质量": [
        "rumination sleep quality",
        "rumination insomnia",
        "anxiety sleep quality",
        "anxious thinking sleep",
        "repetitive negative thinking sleep"
    ]
}

ass \
    .search(queries, limit=30) \
    .deduplicate() \
    .filter_by_year(2020) \
    .sort_by_citations() \
    .filter_by_criteria(
        foundation_min=500,
        important_min=50,
        foundation_limit=999,  # 全部保留
        important_limit=999,   # 全部保留
        general_limit=30
    ) \
    .fetch_full_metadata() \
    .summarize() \
    .save("./知识库/index.json", "负性思维与睡眠质量")
```

### 工作流2：补全已有知识库的元数据

```python
from AcademicSearchSummarizer import AcademicSearchSummarizer

ass = AcademicSearchSummarizer()

# 直接补全已有知识库的完整元数据
count = ass.fill_metadata_from_kb("./知识库/index.json")
print(f"成功补全{count}篇文献的完整信息")
```

### 工作流3：导出主题笔记

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

### 工作流3：补全已有知识库的笔记

```python
from AcademicSearchSummarizer import AcademicSearchSummarizer

ass = AcademicSearchSummarizer()

# 需要LLM API key
ass.complete_notes("./知识库/index.json")
```

### 工作流4：仅检索不分析（节省API费用）

```python
from AcademicSearchSummarizer import AcademicSearchSummarizer

ass = AcademicSearchSummarizer()

queries = {
    "负性思维与睡眠质量": {
        1: ["rumination sleep quality", "rumination insomnia"]
    }
}

ass \
    .search(queries, limit=20) \
    .deduplicate() \
    .filter_by_year(2020) \
    .filter_by_criteria() \
    .save("./知识库/index.json")
```

---

## 文献分级标准

| 级别 | 引用量 | 标记 | 处理方式 |
|------|--------|------|----------|
| 奠基 | >=500 | 🔴 | 全部保留（最多5篇） |
| 重要 | 50-500 | 🟡 | 保留10篇 |
| 一般 | <50 | 🔵 | 保留30篇（近3年） |

## 文献类型分类

文献类型经过两轮分类：

### 初分类（基于规则）

根据标题和摘要关键词进行初步判断：

| 类型 | 标记 | 判断标准 |
|------|------|----------|
| 实证 | 📊 | 摘要含 participant / sample / method / result |
| 综述 | 📖 | 标题含 review / meta-analysis / systematic review |
| 理论 | 💡 | 标题含 theoretical / theory / perspective / commentary |
| 待分类 | 📋 | 无法明确归类的文献 |

### 修订（再分类，基于LLM）

使用大语言模型对初分类结果进行验证和修正：

| 初分类 | LLM判断 | 最终类型 | notes字段 |
|--------|---------|----------|-----------|
| 📊实证 | ✅确认 | 📊实证 | 研究问题、研究方法、研究结果、研究结论 |
| 📊实证 | ❌修正 | 📖综述 / 💡理论 / 📋待分类 | 对应类型的notes字段 |
| 📖综述 | ✅确认 | 📖综述 | 研究问题、研究结果、研究展望 |
| 📖综述 | ❌修正 | 📊实证 / 💡理论 / 📋待分类 | 对应类型的notes字段 |
| 💡理论 | ✅确认 | 💡理论 | 研究问题、理论观点 |
| 💡理论 | ❌修正 | 📊实证 / 📖综述 / 📋待分类 | 对应类型的notes字段 |
| 📋待分类 | LLM判断 | 📊实证 / 📖综述 / 💡理论 / 📋待分类 | 对应类型的notes字段 |

### 分类流程

```
┌─────────────────┐
│  初分类（规则）  │
│  基于标题/摘要   │
└────────┬────────┘
         ▼
┌─────────────────┐
│  修订（LLM）    │
│  验证和修正     │
└────────┬────────┘
         ▼
┌─────────────────┐
│  最终类型 +     │
│  notes字段      │
└─────────────────┘
```

### 各类型最终notes字段

| 最终类型 | notes字段 |
|----------|-----------|
| 📊实证 | 研究问题、研究方法、研究结果、研究结论 |
| 📖综述 | 研究问题、研究结果、研究展望 |
| 💡理论 | 研究问题、理论观点 |
| 📋待分类 | 说明 |

---

## Notes字段详细说明

根据文献最终类型，系统会自动生成不同结构的notes字段：

### 📊 实证文献 Notes

实证研究包含完整的科学研究要素：

| 字段名 | 内容说明 | 示例 |
|--------|----------|------|
| `研究问题` | 文献试图解决的科学问题 | 探讨反刍思维对睡眠质量的影响机制 |
| `研究方法` | 采用的方法、被试/样本、实验设计 | 采用问卷调查法，以500名大学生为被试，使用匹兹堡睡眠质量指数和反刍思维量表 |
| `研究结果` | 主要发现和效应大小 | 反刍思维与睡眠质量呈显著负相关(r=-0.45, p<0.001) |
| `研究结论` | 结论和理论贡献 | 反刍思维是预测睡眠质量的重要认知因素，干预应针对认知模式 |

**完整示例：**
```json
{
  "研究问题": "探讨反刍思维对大学生睡眠质量的影响",
  "研究方法": "采用横断面设计，以800名大学生为被试，使用PSQI和RRS量表进行测量",
  "研究结果": "反刍思维与睡眠质量显著负相关(r=-0.52)，中介分析显示认知情绪调节起部分中介作用",
  "研究结论": "反刍思维通过影响认知情绪调节进而影响睡眠质量，为干预提供了靶点"
}
```

---

### 📖 综述文献 Notes

综述文献总结和整合已有研究：

| 字段名 | 内容说明 | 示例 |
|--------|----------|------|
| `研究问题` | 综述试图解决的科学问题 | 系统综述反刍思维与睡眠关系的实证研究进展 |
| `研究结果` | 主要发现和效应量 | 纳入45项研究，元分析显示中等效应量(d=0.58)，异质性较高(I²=75%) |
| `研究展望` | 未来研究方向 | 需要更多纵向研究确定因果关系；探索文化差异和调节变量 |

**完整示例：**
```json
{
  "研究问题": "系统综述反刍思维与睡眠质量关系的实证研究",
  "研究结果": "纳入32项研究，元分析显示显著正相关(r=0.42)，调节分析发现年龄和文化背景是重要调节变量",
  "研究展望": "未来研究应采用纵向设计，探索神经机制和干预效果，关注不同人群的差异"
}
```

---

### 💡 理论文献 Notes

理论文章提出新理论或概念框架：

| 字段名 | 内容说明 | 示例 |
|--------|----------|------|
| `研究问题` | 理论试图解释的科学问题 | 如何解释反刍思维影响睡眠的心理机制 |
| `理论观点` | 核心概念和逻辑 | 提出认知-情绪级联模型：反刍思维→认知唤醒→情绪失调→睡眠障碍 |

**完整示例：**
```json
{
  "研究问题": "解释反刍思维影响睡眠质量的认知机制",
  "理论观点": "提出认知激活模型：反刍思维导致睡前认知激活增加，抑制睡眠启动；同时通过情绪调节影响睡眠维持"
}
```

---

### 📋 待分类文献 Notes

无法明确归类的文献：

| 字段名 | 内容说明 | 示例 |
|--------|----------|------|
| `说明` | 无法分类的简要说明 | 文献为会议摘要，信息不完整，无法判断类型 |

**完整示例：**
```json
{
  "说明": "文献为会议海报摘要，缺少完整摘要和方法描述，无法准确判断类型"
}
```

---

### Notes生成流程

```
┌─────────────────┐
│  读取文献信息    │
│  title/abstract │
└────────┬────────┘
         ▼
┌─────────────────┐
│  LLM分析判断    │
│  文献类型       │
└────────┬────────┘
         ▼
┌─────────────────┐     ┌─────────────────┐
│  根据类型选择   │────▶│  📊实证：4个字段 │
│  notes模板      │     ├─────────────────┤
└─────────────────┘     │  📖综述：3个字段 │
                        ├─────────────────┤
                        │  💡理论：2个字段 │
                        ├─────────────────┤
                        │  📋待分类：1个字段│
                        └─────────────────┘
```

### 字段填写要求

- **研究问题**：1-2句话概括，使用中文
- **研究方法**：简述设计、样本、工具，1-2句话
- **研究结果**：核心发现+效应量/统计值，1-2句话
- **研究结论**：理论贡献和实践意义，1-2句话
- **研究展望**：未来研究方向，1-2句话
- **理论观点**：核心概念和逻辑链条，1-2句话
- **说明**：无法分类的原因，1句话

所有字段必须基于文献实际内容，禁止编造。

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 1.3.0 | 2026-04-13 | 添加完整方法文档，整理所有API |
| 1.2.0 | 2026-04-13 | 添加academic_search.py重构版，整合检索和LLM总结 |
| 1.1.0 | 2026-04-12 | 添加topic字段为列表格式 |
| 1.0.0 | 2026-04-08 | 初始版本 |
