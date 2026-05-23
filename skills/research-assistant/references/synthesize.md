# 文献综述合成模块 (Synthesizer)

Synthesizer 类提供两个功能：
1. **提取结构化笔记**：从 topic JSON 导出结构化 Markdown 笔记（供代理阅读）
2. **引用检查与修复**：检查 APA 7th 格式、修复 DSAM 引用

## 快速开始

### 我想...

| 需求 | 方法 |
|------|------|
| 从 topic 导出结构化笔记 | [`extract_notes()`](#提取笔记) |
| 检查参考文献格式 | [`check_references()`](#检查引用) |
| 修复 DSAM 引用 | [`fix_references()`](#修复引用) |

## 文件说明

| 文件 | 功能 |
|------|------|
| `Synthesizer.py` | 综述合成主类（提取笔记 + 引用检查） |
| `ReferenceChecker.py` | 参考文献检查与修复类 |

---

## 工作流示例

### 1. 提取结构化笔记

```python
from synthesize.Synthesizer import Synthesizer

synthesizer = Synthesizer()
result = synthesizer.extract_notes("knowledge/topic/治疗期待.json",
                                    "knowledge/note/笔记_治疗期待.md")

# 查看结果
print(f"导出: {result['output_path']}")
print(f"文献数: {result['count']}")
```

输出格式：
```markdown
# 治疗期待 — 文献笔记

> 生成时间: 2026-05-15 18:30
> 总文献: 137 篇

---

## 1. 标题
**作者**: 作者名, et al.  
**年份**: 2019  
**期刊**: 期刊名  
**引用**: 304  
**标签**: 📊实证 🟡重要文献

### 研究问题
...

### 研究方法
...

### 研究结果
...

### 研究结论
...

---
```

### 2. 检查参考文献

```python
from synthesize.Synthesizer import Synthesizer

# 检查综述中的引用格式
results = synthesizer.check_references("knowledge/review/综述.md")

print(f"APA 括号引用: {results['apa_parenthetical']}")
print(f"APA 叙述引用: {results['apa_narrative']}")
print(f"非 APA 可疑: {results['non_apa_suspect']}")
```

### 3. 修复 DSAM 引用

```python
from synthesize.Synthesizer import Synthesizer

# 绑定知识库路径
synthesizer = Synthesizer("knowledge/topic/治疗期待.json")

# 修复引用
fix_result = synthesizer.fix_references("knowledge/review/综述.md",
                                         "knowledge/review/综述_修复后.md")
```

---

## 方法详情

### 提取笔记

```python
extract_notes(topic_path, output_path=None)
```

**参数:**
- `topic_path`: topic JSON 文件路径（如 `knowledge/topic/治疗期待.json`）
- `output_path`: 输出 Markdown 文件路径（默认 `knowledge/note/笔记_{主题}.md`）

**返回:**
```json
{"success": true, "output_path": "...", "count": 137}
```

### 检查参考文献

```python
check_references(doc_path)
```

**参数:**
- `doc_path`: Markdown 文档路径

**返回:**
```json
{
  "success": true,
  "apa_parenthetical": 15,
  "apa_narrative": 8,
  "non_apa_suspect": 2,
  "non_apa_examples": ["DSAM_0015", "[1]"],
  "check_passed": false
}
```

### 修复引用

```python
fix_references(doc_path, output_path=None)
```

> **注意**：需要先绑定知识库路径（初始化时传入），以获取作者和年份信息。

**参数:**
- `doc_path`: 输入文档路径
- `output_path`: 输出文档路径（可选，默认覆盖原文件）

---

## 命令行工具

### 提取笔记
```bash
python3 Synthesizer.py extract --topic knowledge/topic/治疗期待.json --output knowledge/note/笔记_治疗期待.md
```

### 检查引用
```bash
python3 Synthesizer.py check --doc knowledge/review/综述.md
```

### 修复引用
```bash
python3 Synthesizer.py fix --doc knowledge/review/综述.md --kb knowledge/topic/治疗期待.json --output 修复后的.md
```

---

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 2.0.0 | 2026-05-15 | **重构：删除 `write_review`（综述由代理人工撰写），新增 `extract_notes`（从 topic.json 导出结构化 Markdown），保留 `check_references` 和 `fix_references`。** |
| 1.1.0 | 2026-04-22 | 统一风格：初始化时绑定知识库，方法调用时只传文档路径 |
| 1.0.0 | 2026-04-15 | 初始版本，提供文献综述合成功能 |
