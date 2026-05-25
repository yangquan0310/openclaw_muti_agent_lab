# 如何执行研究工作流

> 科研文献综述全流程：检索 → 整理 → 分析 → 撰写 → 检查

---

## 问题

### 为什么要了解工作流？

研究文献综述是一个多阶段任务，不了解全流程容易：
- 遗漏关键步骤
- 顺序混乱导致返工
- 不知道每个阶段的目标

### 工作流的五个阶段

```
阶段1：理解 → 阶段2：检索 → 阶段3：阅读 → 阶段4：撰写 → 阶段5：检查
```

| 阶段 | 输入 | 输出 | 负责模块 |
|------|------|------|----------|
| 理解 | 研究问题 | 明确的研究主题和范围 | 代理 |
| 检索 | 研究主题 + 关键词 | knowledge/index.json | Searcher |
| 阅读 | index.json | topic.json + 笔记.md | Manager + Summarizer |
| 撰写 | 笔记.md + 写作指南 | 综述.md | 代理 |
| 检查 | 综述.md + topic.json | 修正后的综述 + 更新的元数据 | Synthesizer + Maintainer |

---

## 方法论

### 核心原则

1. **阶段顺序执行**：不要跳跃阶段
2. **每个阶段有明确输出**：没有输出 = 阶段未完成
3. **Git 版本控制**：每个阶段完成后 commit

### 判断：何时进入下一阶段？

| 当前阶段 | 下一阶段入口条件 |
|----------|------------------|
| 理解 | 明确研究主题和检索关键词 |
| 检索 | index.json 包含 ≥ 目标数量的 80% 文献 |
| 阅读 | 笔记.md 生成完毕 |
| 撰写 | 综述.md 完成初稿 |
| 检查 | APA 引用无错误，元数据已更新 |

---

## 工作流

### 步骤 1：理解

**目标**：明确研究主题和范围

**操作**：
1. 阅读《文献综述撰写指南》或《研究现状撰写指南》
2. 确定研究问题边界
3. 列出检索关键词（中英文）

**输出**：研究主题 + 关键词列表

---

### 步骤 2：检索

**目标**：获取文献数据

**操作**：
```bash
research-assistant search --queries queries.json --kb-path knowledge/index.json
```

详见 [ch02_how-to-search-academic-papers.md](ch02_how-to-search-academic-papers.md)

**输出**：knowledge/index.json

---

### 步骤 3：阅读

**目标**：从文献中提取结构化笔记

**操作**：
1. 使用 Manager 筛选 topic
2. 使用 Summarizer 生成 notes
3. 使用 Synthesizer 导出 Markdown

详见：
- [ch03_how-to-manage-knowledge-base.md](ch03_how-to-manage-knowledge-base.md)
- [ch04_how-to-summarize-papers.md](ch04_how-to-summarize-papers.md)

**输出**：knowledge/note/笔记_{topic}.md

---

### 步骤 4：撰写

**目标**：撰写综述或研究现状

**操作**：代理阅读笔记，参照写作指南模板撰写

详见：
- [ch06_how-to-write-literature-review.md](ch06_how-to-write-literature-review.md)
- [ch07_how-to-write-research-status.md](ch07_how-to-write-research-status.md)

**输出**：knowledge/review/综述_{topic}.md

---

### 步骤 5：检查

**目标**：确保综述质量

**操作**：
1. 使用 Synthesizer 检查 APA 引用
2. 使用 Maintainer 更新元数据

详见：
- [ch05_how-to-synthesize-notes.md](ch05_how-to-synthesize-notes.md)
- [ch08_how-to-maintain-metadata.md](ch08_how-to-maintain-metadata.md)

---

## 执行标准

### 数据流验证

```
queries.json → Searcher → index.json
                            ↓
                    Manager.filter → topic.json
                            ↓
                    Summarizer → notes/labels
                            ↓
                    Synthesizer → 笔记.md
                            ↓
                    补充检索 → Exa/Tavily → 笔记.md
                            ↓
                    代理撰写 → 综述.md
                            ↓
                    Synthesizer.check → APA 核查
                            ↓
                    Maintainer → 元数据更新
```

### 阶段检查清单

| 阶段 | 检查项 | 通过标准 |
|------|--------|----------|
| 检索 | 论文数量 | ≥ 目标数量的 80% |
| 检索 | 时间范围 | 覆盖近 5-10 年 |
| 阅读 | topic 筛选 | Manager.filter() 保存 topic.json |
| 阅读 | 笔记导出 | Synthesizer.extract_notes() 生成 Markdown |
| 检查 | APA 引用 | Synthesizer.check_references() 无错误 |
| 检查 | 元数据 | Maintainer 更新时间戳 |
