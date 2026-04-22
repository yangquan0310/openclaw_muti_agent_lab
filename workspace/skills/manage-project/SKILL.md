---
name: manage-project
description: 管理项目文件的自动化整理和分类，以及文献检索、笔记提取与总结、综述撰写等学术事务。包含五个子模块：文献检索(search)、文献总结(summarize)、知识库管理(manage)、文献综述合成(synthesize)、项目文件整理(maintainer)。当用户需要搜索论文、总结文献、生成综述、整理项目目录结构或归档文件时，使用此技能。
version: 3.0.0
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

# 项目管理技能包

本技能模拟一个"项目管理经理"，协调五个子技能共同完成学术事务处理和项目文件管理。

## 五个独立模块

| 模块 | 目录 | 功能 | 对应类 |
|------|------|------|--------|
| **文献检索** | `search/` | 从 Semantic Scholar 获取数据，支持多主题多轮检索 | Searcher |
| **文献总结** | `summarize/` | 使用 LLM 分析文献，添加 labels 和 notes 字段 | Summarizer |
| **知识库管理** | `manage/` | 合并、筛选、保存知识库，支持链式调用 | Manager |
| **文献综述合成** | `synthesize/` | 基于知识库生成文献综述和研究现状，检查参考文献 | Synthesizer |
| **项目文件整理** | `maintainer/` | 自动化整理项目目录结构、归档文件、管理元数据 | Maintainer |

---

## 快速开始

### 我想...

| 需求 | 跳转 |
|------|------|
| 检索文献 | [search/SKILL.md](./search/SKILL.md) |
| 总结文献 | [summarize/SKILL.md](./summarize/SKILL.md) |
| 管理知识库 | [manage/SKILL.md](./manage/SKILL.md) |
| 写文献综述 | [synthesize/SKILL.md](./synthesize/SKILL.md) |
| 整理项目文件 | [maintainer/SKILL.md](./maintainer/SKILL.md) |

---

## 工作流

### 1. 初始化项目对象
```python
from maintainer.Maintainer import Maintainer

maintainer = Maintainer("/path/to/project")
```

### 2. 检索文献
- 确定检索范围
```json
{
    "自传体记忆": [
        {"query": "autobiographical memory | personal memory", "limit": 30}
    ]
}
- 将{检索条件}.json 存储于 `临时数据/检索条件/`
```
- 检索
```python
from search.Searcher import Searcher
# 初始化时绑定知识库路径
searcher = Searcher(kb_path="my_kb.json")
queries = {
    "自传体记忆": [
        {"query": "autobiographical memory | personal memory", "limit": 30}
    ]
}
# 方法调用时不再传知识库路径
searcher.search(queries)
searcher.update()
```

### 3. 管理知识库（筛选并保存笔记）
```python
from manage.Manager import Manager
# 初始化时绑定知识库路径
manager = Manager("my_kb.json")
# 筛选后无参保存到绑定的路径
manager.filter({"citations_min": 50}).save()
```

### 4. 总结文献（基于筛选后的笔记）
```python
from summarize.Summarizer import Summarizer
# 初始化时绑定知识库路径
summarizer = Summarizer(kb_path="笔记.json")
# 方法调用时不再传知识库路径
kb = summarizer.summarize()
```

### 5. 检查参考文献
```python
from synthesize.Synthesizer import Synthesizer
# 初始化时绑定一个或多个知识库
synthesizer = Synthesizer("kb1.json", "kb2.json")
# 方法调用时只传文档路径
synthesizer.check_references("综述文档.md")
```

### 6. 整理项目文件

1. **把中间文件归档到 `临时数据/` 下**
   ```python
   maintainer.move_file("中间文件.txt", target_dir="临时数据")
   ```

2. **综述输出在 `知识库/综述/`**
   ```python
   maintainer.move_file("综述.md", target_dir="知识库/综述")
   ```

3. **笔记输出在 `知识库/笔记/`**
   ```python
   maintainer.move_file("笔记.md", target_dir="知识库/笔记")
   ```

4. **把用户上传移动到 `文档/`**
   ```python
   maintainer.move_file("用户文档.docx", target_dir="文档")
   ```

5. **把撰写的最新md文档移动到 `手稿/`**
   ```python
   maintainer.move_file("论文.md", target_dir="手稿")
   ```

6. **把备份版本移动到 `临时数据/草稿/`，检索条件.json 移动到 `临时数据/检索条件/`**
   ```python
   maintainer.move_file("论文_backup.md", target_dir="临时数据/草稿")
   maintainer.move_file("检索条件.json", target_dir="临时数据/检索条件")
   ```

7. **把NoteExtractor提取的笔记.md 移动到 `临时数据/笔记/`**
   ```python
   maintainer.move_file("提取笔记.md", target_dir="临时数据/笔记")
   ```

### 7. 更新元数据
```python
maintainer.update_metadata()
```

### 8. 重命名文件夹（如需调整）
```python
maintainer.rename_folder("旧文件夹名", "新文件夹名")
```

### 命令行使用
```bash
# 整理单个项目
python3 maintainer/Maintainer.py /path/to/project

# 整理所有项目
python3 maintainer/Maintainer.py --all

# 预览模式（不实际执行）
python3 maintainer/Maintainer.py /path/to/project --dry-run
```

---

## 配置介绍

- `config.json`：统一配置文件，存放所有 API、模型、存储相关配置
- `README.md`：给人类看的说明文档
- `search/`：负责检索并获取论文列表或加载已有知识库并更新
- `summarize/`：负责解析摘要并提取结构化笔记
- `manage/`：负责知识库合并、筛选、提取
- `synthesize/`：负责将所有提取的笔记组织成一篇完整的综述，检查参考文献
  - `Synthesizer.py`：综述合成主类，协调笔记提取与引用检查
  - `ReferenceChecker.py`：参考文献检查与修复类
  - `NoteExtractor.py`：笔记信息提取类
- `maintainer/`：负责自动化整理项目目录结构、归档文件、管理元数据

---

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 3.0.0 | 2026-04-22 | 重构为统一项目管理技能，整合知识库管理与项目文件整理为五大模块 |
| 2.1.0 | 2026-04-22 | 统一风格：初始化时绑定知识库/笔记，方法调用时不再传知识库或笔记 |
| 2.0.0 | 2026-04-15 | 按面向对象思路重构，拆分为四个独立子模块 |
