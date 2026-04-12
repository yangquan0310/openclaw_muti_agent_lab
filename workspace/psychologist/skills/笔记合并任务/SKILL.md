# 笔记合并任务

> 技能ID: psychologist-notes-merge
> 版本: 1.1.0
> 创建时间: 2026-04-11
> 维护者: 心理学家 (psychologist)

---

## 描述

将多个分散的文献笔记JSON文件按主题合并为统一的笔记文件，便于后续分析和综述撰写。

---

## 触发条件

当需要合并文献笔记文件时触发：
- 完成多个批次的文献笔记生成后需要合并
- 需要按主题重新组织笔记文件
- 需要清理中间文件，保留最终合并版本

---

## 输入

- 多个JSON格式的笔记文件（符合S2脚本输出格式）
- 主题分类映射关系

## 输出

- 按主题合并的JSON笔记文件
- 合并统计报告

---

## 使用步骤

### 步骤1: 准备文件映射

定义主题与文件的对应关系：

```python
topic_files = {
    '主题名称1': ['文件1.json', '文件2.json'],
    '主题名称2': ['文件3.json', '文件4.json'],
}
```

### 步骤2: 执行合并脚本

使用 `generate_notes_s2.py` 脚本执行合并：

```bash
cd /root/实验室仓库/项目文件/{项目名}/知识库/笔记
python3 generate_notes_s2.py
```

### 步骤3: 验证合并结果

检查合并后的文件：
- JSON格式正确性
- 文献数量统计
- 去重验证

### 步骤4: 清理中间文件

删除已合并的中间文件：

```bash
rm -v *_第*.json *_全部.json 第*批_*.json
```

---

## 文件格式规范

### 输入文件格式

每个笔记文件必须符合以下JSON结构：

```json
{
  "version": "1.0.0",
  "project": "项目名称",
  "note_name": "笔记名称",
  "created_at": "2026-04-11T00:00:00",
  "updated_at": "2026-04-11T00:00:00",
  "statistics": {
    "total_count": 30,
    "empirical_count": 22,
    "review_count": 5,
    "theory_count": 3
  },
  "notes": {
    "DSAM_0001": {
      "title": "文献标题",
      "type": "📊实证",
      "content": {
        "research_question": "...",
        "method": "...",
        "results": "...",
        "conclusion": "..."
      }
    }
  }
}
```

### 输出文件格式

合并后的文件保持相同结构，统计信息累加，notes合并。

---

## 脚本位置

`/root/.openclaw/workspace/psychologist/scripts/笔记合并任务/generate_notes_s2.py`

---

## 脚本结构

脚本采用面向对象设计，包含以下核心类：

### 数据类
- **`Paper`** - 文献数据类，封装文献ID、标题、作者、摘要等属性
- **`NoteContent`** - 笔记内容数据类
- **`NoteStatistics`** - 笔记统计数据类

### 处理类
- **`NoteExtractor`** - 笔记提取器，负责从文献中提取结构化笔记内容
  - `extract(paper)` - 从单篇文献提取笔记
  - `_extract_by_type()` - 根据文献类型提取不同结构
  
- **`NoteMerger`** - 笔记合并器，负责合并多个笔记文件
  - `load_note_file()` - 加载单个笔记文件
  - `merge_notes()` - 合并多个笔记文件
  - `merge_by_topic()` - 按主题合并笔记
  
- **`NoteGenerator`** - 笔记生成器主类，协调提取和合并流程
  - `load_index()` - 加载知识库索引
  - `generate_topic_notes()` - 为单个主题生成笔记
  - `generate_all_notes()` - 为所有主题生成笔记

### 便捷函数
- `generate_notes()` - 快速生成笔记
- `merge_notes()` - 快速合并笔记

---

## 使用示例

### 示例1: 使用NoteGenerator类生成笔记

```python
from generate_notes_s2 import NoteGenerator

generator = NoteGenerator(project_dir="/path/to/project")
results = generator.generate_all_notes()

for topic, count, filepath in results:
    print(f"{topic}: {count}篇 -> {filepath}")
```

### 示例2: 使用NoteMerger类合并笔记

```python
from generate_notes_s2 import NoteMerger, DEFAULT_TOPIC_MAPPING

merger = NoteMerger(notes_dir="/path/to/notes")
results = merger.merge_by_topic(DEFAULT_TOPIC_MAPPING)
```

### 示例3: 使用便捷函数

```python
from generate_notes_s2 import generate_notes, merge_notes

# 生成笔记
results = generate_notes(project_dir="/path/to/project")

# 合并笔记
topic_mapping = {
    '主题1': ['file1.json', 'file2.json'],
    '主题2': ['file3.json', 'file4.json'],
}
results = merge_notes(notes_dir="/path/to/notes", topic_mapping=topic_mapping)
```

---

## 注意事项

1. **去重检查**: 合并前检查是否有重复文献ID
2. **统计准确性**: 确保统计信息正确累加
3. **格式验证**: 合并后验证JSON格式正确性
4. **备份**: 合并前备份原始文件

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 1.0.0 | 2026-04-11 | 初始版本，支持按主题合并笔记文件 |
| 1.1.0 | 2026-04-11 | 重构为面向对象结构，增加NoteExtractor、NoteMerger、NoteGenerator类 |

---

*最后更新: 2026-04-11*
