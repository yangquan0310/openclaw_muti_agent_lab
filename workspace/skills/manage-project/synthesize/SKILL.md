---
name: 文献综述合成
description: 基于知识库生成文献综述和研究现状，提供模板和自动化脚本
version: 1.0.0
author: Yang Quan
dependencies:
  - python>=3.9
  - 知识库文件
tools:
  - python
  - markdown
---

# 文献综述合成模块 (Synthesizer)

Synthesizer 模块基于知识库生成文献综述和研究现状，提供模板和自动化脚本。

## 快速开始

### 我想...

| 需求 | 文件 |
|------|------|
| 写文献综述 | 使用[文献综述模板.md](./文献综述模板.md) |
| 写研究现状 | 使用[研究现状模板.md](./研究现状模板.md) |
| 检查参考文献 | 使用[ReferenceChecker.py](./ReferenceChecker.py) |
| 提取笔记信息 | 使用[NoteExtractor.py](./NoteExtractor.py) |

## 文件说明

| 文件 | 功能 |
|------|------|
| `文献综述模板.md` | 文献综述模板文件 |
| `研究现状模板.md` | 研究现状模板文件 |
| `ReferenceChecker.py` | 参考文献检查与修复类（面向对象） |
| `NoteExtractor.py` | 笔记信息提取类（面向对象） |

---

## 工作流示例

### 1. 准备工作：确保已有笔记文件

```python
from search.Searcher import Searcher
from summarize.Summarizer import Summarizer
from manager.Manager import Manager

# 1. 检索文献
searcher = Searcher(kb_path="my_kb.json")
queries = {"研究主题": [{"query": "keywords", "limit": 30}]}
# 方法调用时不再传知识库路径
searcher.search(queries)

# 2. 筛选并保存笔记
manager = Manager("my_kb.json")
# 筛选后无参保存到绑定的路径
manager.filter({"topic": "主题"}).save()

# 3. 总结文献（基于筛选后的笔记）
summarizer = Summarizer(kb_path="笔记.json")
# 方法调用时不再传知识库路径
summarizer.summarize()
```

### 2. 使用模板

加载模板：[文献综述模板](./文献综述模板) 和 [研究现状模板.md](./研究现状模板.md)

---

### 3. 文本处理

#### 步骤 1：读取笔记文件并提取信息

```python
from synthesize.NoteExtractor import NoteExtractor
from scripts.manage_project import Project

# 初始化项目
project = Project("/path/to/project")

# 提取笔记信息
extractor = NoteExtractor()
info = extractor.extract('/path/to/笔记.json')

# 保存提取的笔记到临时数据/笔记/
note_path = project.save_extracted_note(
    note_title="提取笔记",
    content=str(info),
    source="/path/to/笔记.json"
)

# 查看提取结果
print(f"文献数量: {info['count']}")
print(f"研究问题: {info['research_questions']}")
print(f"研究方法: {info['methods']}")
print(f"研究结果: {info['findings']}")
```

- 打开笔记文件（`~/实验室仓库/项目文件/{项目名}/知识库/笔记/{笔记}.json`）
- 使用NoteExtractor提取所有文献的关键信息
- 解析 JSON 结构，获取文献笔记列表
- 若文献笔记 < 5 篇 → 返回："笔记文献不足，请先补充笔记后再撰写综述"

#### 步骤 2：界定主题与范围
- 明确综述的主题和研究领域
- 基于笔记中的文献确定时间范围和内容范围
- 明确纳入和排除标准

#### 步骤 3：分析笔记
- **不要编造论文**：所有分析必须基于笔记文件中的真实文献，不能编造任何信息
- **围绕笔记综述**：所有内容必须基于笔记中的文献，分类整理文献，逻辑清晰
- **仔细阅读笔记文件中的每一篇文献的笔记**
- **提取笔记字段**
- 汇总文献研究的问题
- 分析研究方法（实证类）
- 汇总发现的效应和解释
- 识别研究空白和方法局限

#### 步骤 4：参照文章
- 参照模板：[文献综述模板](./文献综述模板) 和 [研究现状模板.md](./研究现状模板.md)
- **必须引用论文**：正文中的引用使用 APA 格式（作者, 年份），每个重要观点都必须有文献支持
- 汇总所有引用文献，去重并排序
- 按照 APA 7th 格式生成参考文献列表

#### 步骤 5：核查引用

```python
from synthesize.ReferenceChecker import ReferenceChecker

# 初始化时绑定一个或多个知识库
checker = ReferenceChecker("kb1.json", "kb2.json")

# 检查参考文献（方法调用时只传文档路径）
results = checker.check_references("综述文档.md")

# 查看结果
print(f"DSAM引用: {results['stats']['dsam_total']}")
print(f"缺失引用: {results['missing_references']}")

# 修复引用（可选）
fix_result = checker.fix_references("综述文档.md", "修复后的文档.md")
```

#### 步骤 6：保存文档
- 草稿：`~/实验室仓库/项目文件/{项目名}/临时数据/草稿/{标题}/{标题}_v{version}.md`
- 终稿：`~/实验室仓库/项目文件/{项目名}/知识库/综述/{标题}.md`
- 修改：先移动`~/实验室仓库/项目文件/{项目名}/知识库/综述/{标题}.md`至 `临时数据/草稿/{标题}` 并命名{标题}_v{version}.md，然后再创建新的{标题}.md

#### 步骤 7：管理元数据
- 在项目元数据.json中file中记录文献综述信息:
```json
{标题、路径、文献数量、创建时间}
```

---
## 方法详情

### ReferenceChecker 类

文献检查与修复的核心类，采用面向对象设计。

#### 核心方法

```python
check_references(doc_path)
```

**参数:**
- `doc_path`: 待检查的Markdown文档路径

**返回:**
检查结果字典，包含：
- `success`: 检查是否成功
- `stats`: 统计信息（DSAM引用数、APA引用数、缺失引用数等）
- `missing_references`: 缺失的引用列表
- `recommendations`: 修复建议列表

> **注意**：知识库路径在初始化 `ReferenceChecker(kb1, kb2, ...)` 时绑定，不在 `check_references()` 方法中传入。

#### 私有辅助方法

| 方法 | 功能 |
|------|------|
| `_load_documents()` | 加载文档和笔记文件 |
| `_build_citation_maps()` | 从笔记构建引用映射 |
| `_find_dsam_references()` | 查找DSAM格式引用 |
| `_find_apa_references()` | 查找APA格式引用 |
| `_validate_references()` | 验证引用完整性 |
| `_collect_stats()` | 收集统计信息 |
| `_generate_recommendations()` | 生成修复建议 |
| `_parse_authors()` | 解析作者字符串 |
| `_format_apa_citation()` | 格式化APA引用 |
| `_format_apa_citation_text()` | 格式化文本型APA引用 |

#### 可选修复方法

```python
fix_references(doc_path, output_path=None)
```

将文档中的DSAM引用替换为APA格式引用。

**参数:**
- `doc_path`: 输入文档路径
- `output_path`: 输出文档路径（可选，默认覆盖原文件）

**返回:**
修复结果字典，包含替换统计信息。

> **注意**：`fix_references` 使用初始化时绑定的知识库映射，无需额外传入。

---

## 命令行工具

### 检查参考文献（绑定一个知识库）
```bash
# 初始化时绑定知识库，方法调用时只传文档路径
python3 ReferenceChecker.py \
    --doc 综述文档.md \
    --kb 知识库1.json
```

### 检查参考文献（绑定多个知识库）
```bash
# 初始化时绑定多个知识库
python3 ReferenceChecker.py \
    --doc 综述文档.md \
    --kb 知识库1.json \
    --kb 知识库2.json \
    --kb 知识库3.json
```

### 检查并修复参考文献
```bash
# 绑定知识库并修复
python3 ReferenceChecker.py \
    --doc 综述文档.md \
    --kb 知识库1.json \
    --kb 知识库2.json \
    --fix \
    --output 修复后的文档.md
```

### 命令参数
| 参数 | 说明 |
|------|------|
| `--doc` | 待检查的Markdown文档路径（必填） |
| `--kb` | 知识库JSON文件路径（可多次使用以加载多个知识库） |
| `--fix` | 修复引用（将DSAM引用替换为APA格式） |
| `--output` | 修复后输出路径（仅在--fix时使用） |

### 输出示例
```bash
正在检查参考文献...

检查完成!
DSAM引用总数: 15
唯一DSAM引用: 10
缺失引用: 2

缺失的引用: ['DSAM_0015', 'DSAM_0020']

建议:
  - 补充缺失引用的文献信息
  - 确保所有DSAM引用都有对应的文献记录
```

---
## 输出

- 结构化文献综述文档（APA 7th 格式）
- 参考文献列表
- 文件保存路径

---

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.1.0 | 2026-04-22 | 统一风格：初始化时绑定知识库，方法调用时只传文档路径 |
| 1.0.0 | 2026-04-15 | 初始版本，提供文献综述合成功能 |
