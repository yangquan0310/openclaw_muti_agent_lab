# 文献处理工具

> 版本: 1.0.0
> 创建时间: 2026-04-12
> 作者: 心理学家

---

## 功能概述

提供文献处理的完整工具链，包括去重、分类、筛选、合并等功能。

---

## 核心类

### 1. Paper
文献数据类，包含完整的参考文献信息。

```python
@dataclass
class Paper:
    id: str
    title: str
    authors: List[str]  # 作者列表
    year: int
    venue: str
    volume: str
    issue: str
    pages: str
    doi: str
    url: str
    citation_count: int
    abstract: str
    topic: str
    labels: Dict[str, str]
    source: str
```

### 2. Deduplicator
文献去重器，基于DOI和标题相似度去重。

```python
deduplicator = Deduplicator(similarity_threshold=0.85)
unique_papers = deduplicator.deduplicate(papers)
```

### 3. TopicClassifier
主题分类器，基于关键词匹配自动分类。

```python
classifier = TopicClassifier(topic_keywords)
by_topic = classifier.classify_batch(papers)
```

### 4. LiteratureFilter
文献筛选器，支持多种筛选条件。

```python
filter = LiteratureFilter()
filtered = filter.by_citation_count(papers, min_count=50)
filtered = filter.by_year(papers, min_year=2015)
filtered = filter.by_venue_type(papers)  # 排除预印本
```

### 5. LiteratureMerger
文献合并器，合并多个来源并去重。

```python
merger = LiteratureMerger()
merged = merger.merge(papers1, papers2, papers3)
```

### 6. LiteratureProcessor
主处理器，整合所有功能。

```python
processor = LiteratureProcessor(topic_keywords)
result = processor.process_pipeline(
    papers,
    min_citations=10,
    min_year=2015,
    exclude_preprints=True
)
```

---

## 预定义主题

### 课堂拍照行为研究主题

```python
CLASSROOM_PHOTOGRAPHY_TOPICS = {
    "课堂拍照行为": ["photo-taking", "photography", "camera", "phone use"],
    "行为动机": ["motivation", "reason", "purpose", "why students"],
    "情境因素": ["context", "situation", "classroom environment"],
    "教师态度": ["teacher attitude", "instructor perception"],
    "课堂管理": ["classroom management", "policy", "regulation"],
    "学习效果": ["learning outcome", "academic performance"],
    "认知负荷": ["cognitive load", "cognitive offload"],
    "注意力": ["attention", "distraction", "focus"]
}
```

---

## 使用示例

### 基本用法

```python
from literature_processor import LiteratureProcessor, CLASSROOM_PHOTOGRAPHY_TOPICS

# 创建处理器
processor = LiteratureProcessor(CLASSROOM_PHOTOGRAPHY_TOPICS)

# 加载文献
papers = processor.load_from_json('input.json')

# 处理流程
result = processor.process_pipeline(
    papers,
    min_citations=50,
    min_year=2015,
    exclude_preprints=True
)

# 保存结果
processor.save_to_json(papers, 'output.json')
```

### 单独使用功能

```python
# 仅去重
from literature_processor import Deduplicator
deduplicator = Deduplicator()
unique = deduplicator.deduplicate(papers)

# 仅分类
from literature_processor import TopicClassifier
classifier = TopicClassifier(keywords)
by_topic = classifier.classify_batch(papers)

# 仅筛选
from literature_processor import LiteratureFilter
filter = LiteratureFilter()
recent = filter.by_year(papers, min_year=2020)
```

---

## 文件清单

| 文件 | 功能 |
|------|------|
| `literature_processor.py` | 主处理工具（面向对象） |
| `normalize_index.py` | 标准化index.json格式 |
| `SKILL.md` | 本文档 |

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 1.0.0 | 2026-04-12 | 初始版本，整合去重、分类、筛选、合并功能 |
