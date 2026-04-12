# 文献主题分类任务

> 技能版本: 1.0.0
> 创建时间: 2026-04-11
> 作者: 心理学家

---

## 功能描述

根据研究问题自动判断文献是否适合当前主题分类，如不适合则记录建议移动到的主题。

---

## 脚本结构

### 核心类

#### 1. TopicConfig
主题配置类，存储主题名称和关键词列表。

```python
@dataclass
class TopicConfig:
    name: str           # 主题名称
    keywords: List[str] # 关键词列表
    
    def matches(self, text: str) -> int:
        """计算文本与主题的匹配度得分"""
```

#### 2. TopicClassifier
主题分类器，基于关键词匹配判断文献主题归属。

```python
class TopicClassifier:
    TOPICS: List[TopicConfig]  # 7个预定义主题
    
    def classify(self, paper_id: str, paper_data: Dict, current_topic: str) 
                 -> Tuple[bool, str, str]:
        """
        返回: (是否适合当前主题, 建议主题, 判断理由)
        """
```

#### 3. NotesLoader
笔记加载器，负责读取JSON格式的笔记文件。

```python
class NotesLoader:
    def __init__(self, notes_dir: str)
    def load(self, filename: str) -> Dict
    def get_topic_from_filename(self, filename: str) -> str
```

#### 4. ClassificationResult
分类结果类，存储和处理分类结果。

```python
class ClassificationResult:
    def add_modification(self, ...)
    def to_dict(self) -> Dict
    def save(self, output_file: str)
```

#### 5. BatchClassifier
批量分类器，整合上述组件执行批量分类任务。

```python
class BatchClassifier:
    def classify_batch(self, notes_file: str, start_idx: int, 
                      end_idx: int, output_file: str) -> ClassificationResult
```

---

## 7个主题定义

| 主题 | 关键词 |
|------|--------|
| 自传体记忆的概念 | 定义、结构、模型、理论、概念、分类、系统、框架 |
| 自传体记忆的功能 | 功能、作用、应用、叙事身份、回忆疗法、自我连续 |
| 自传体记忆的编码 | 编码、自我参照、注意、加工、形成、获得 |
| 自传体记忆的存储 | 存储、巩固、保持、海马、皮层、睡眠 |
| 自传体记忆的遗忘 | 遗忘、衰退、抑制、定向遗忘、过度概括 |
| 自传体记忆的提取 | 提取、检索、回忆、搜索、访问 |
| 数字化使用对自传体记忆的影响 | 数字、拍照、谷歌效应、认知卸载、社交媒体 |

---

## 使用方法

### 命令行

```bash
python3 classify_papers.py <主题文件> <起始索引> <结束索引> <输出文件>
```

### 示例

```bash
python3 classify_papers.py "自传体记忆的概念.json" 0 30 "/tmp/调整_概念_1-30.json"
```

### Python API

```python
from classify_papers import BatchClassifier

classifier = BatchClassifier("/path/to/notes/dir")
result = classifier.classify_batch(
    notes_file="自传体记忆的概念.json",
    start_idx=0,
    end_idx=30,
    output_file="/tmp/调整_概念_1-30.json"
)

print(f"检查文献: {result.total_checked}篇")
print(f"建议修改: {len(result.modifications)}篇")
```

---

## 输出格式

```json
{
  "source_file": "自传体记忆的概念.json",
  "current_topic": "自传体记忆的概念",
  "range": "1-30",
  "total_checked": 30,
  "modifications_count": 10,
  "modifications": [
    {
      "id": "DSAM_0005",
      "title": "文献标题",
      "current_topic": "自传体记忆的概念",
      "suggested_topic": "自传体记忆的功能",
      "research_question": "研究问题",
      "reason": "判断理由"
    }
  ]
}
```

---

## 扩展方法

### 添加新主题

```python
# 在 TopicClassifier.TOPICS 中添加
TopicConfig("新主题名称", ["关键词1", "关键词2", ...])
```

### 修改匹配算法

重写 `TopicConfig.matches()` 方法或 `TopicClassifier.classify()` 方法。

---

## 文件位置

- 脚本: `~/.openclaw/workspace/psychologist/scripts/文献分类任务/classify_papers.py`
- 技能文档: `~/.openclaw/workspace/psychologist/scripts/文献分类任务/SKILL.md`

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 1.0.0 | 2026-04-11 | 初始版本，面向对象设计 |
