# 如何合成笔记

> 从 topic JSON 导出结构化 Markdown，并检查/修复 APA 引用格式。

---

## 问题

### Synthesizer 能做什么？

| 功能 | 说明 |
|------|------|
| `extract_notes()` | 从 topic JSON 导出结构化 Markdown |
| `check_references()` | 检查 APA 7th 格式引用 |
| `fix_references()` | 修复 DSAM 等非标准引用 |

### 什么时候需要合成？

| 场景 | 操作 |
|------|------|
| 从 topic 准备笔记供代理阅读 | `extract_notes()` |
| 撰写后检查引用格式 | `check_references()` |
| 修复非标准引用 | `fix_references()` |

---

## 方法论

### 笔记结构设计

导出后的 Markdown 按以下格式组织：
```markdown
# 主题名 — 文献笔记

> 生成时间: 2026-05-15
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
```

### APA 引用格式

| 类型 | 格式 |
|------|------|
| 括号引用 | `(Author, Year)` |
| 叙述引用 | `Author (Year)` |

---

## 工作流

### 提取笔记

```python
from synthesize.Synthesizer import Synthesizer

synthesizer = Synthesizer()
result = synthesizer.extract_notes(
    "knowledge/topic/治疗期待.json",
    "knowledge/note/笔记_治疗期待.md"
)
```

### 检查引用

```python
from synthesize.Synthesizer import Synthesizer

synthesizer = Synthesizer()
results = synthesizer.check_references("knowledge/review/综述.md")

print(f"APA 括号引用: {results['apa_parenthetical']}")
print(f"APA 叙述引用: {results['apa_narrative']}")
print(f"非 APA 可疑: {results['non_apa_suspect']}")
```

### 修复引用

```python
synthesizer = Synthesizer("knowledge/topic/治疗期待.json")
fix_result = synthesizer.fix_references(
    "knowledge/review/综述.md",
    "knowledge/review/综述_修复后.md"
)
```

---

## 执行标准

### 笔记导出检查

| 检查项 | 标准 |
|--------|------|
| 每篇文献都有笔记 | 非空 |
| 结构完整 | 研究问题/方法/结果/结论 |
| Markdown 格式 | 无语法错误 |

### 引用检查标准

| 检查项 | 标准 |
|--------|------|
| APA 括号引用 | `(Author, Year)` |
| APA 叙述引用 | `Author (Year)` |
| 非 APA 可疑 | 需人工确认 |
