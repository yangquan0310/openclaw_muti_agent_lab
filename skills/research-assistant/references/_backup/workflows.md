# research-assistant 核心工作流

> 研究助手的核心工作流：检索 → 整理 → 分析 → 撰写 → 检查

---

## 工作流总览

```
阶段1：理解 → 阶段2：检索 → 阶段3：阅读 → 阶段4：撰写 → 阶段5：检查
```

---

## 阶段 1：理解

**输入**：研究问题
**输出**：明确的研究主题和范围

阅读《文献综述撰写指南》，明确研究问题边界、检索关键词、综述类型

---

## 阶段 2：检索

**输入**：研究主题 + 关键词
**输出**：knowledge/index.json

| 检查项 | 标准 |
|--------|------|
| 论文数量 | ≥ 目标数量的 80% |
| 时间范围 | 覆盖近 5-10 年 |
| 引用格式 | 所有论文有完整 APA 信息 |

CLI：`python3 scripts/search/Searcher.py --queries queries.json --kb-path knowledge/index.json`

---

## 阶段 3：阅读

**输入**：index.json
**输出**：knowledge/note/笔记_{topic}.md

| 检查项 | 标准 |
|--------|------|
| topic 筛选 | Manager.filter() 保存 topic.json |
| AI 总结 | Summarizer 补充 notes/labels |
| 笔记导出 | Synthesizer.extract_notes() 生成 Markdown |
| 补充检索 | Exa/Tavily 补充政策/报告/数据 |

---

## 阶段 4：撰写

**输入**：笔记.md + 写作指南
**输出**：knowledge/review/综述.md

代理阅读笔记，参照写作指南模板撰写

---

## 阶段 5：检查

**输入**：综述.md + topic.json
**输出**：修正后的综述 + 更新的元数据

| 检查项 | 标准 |
|--------|------|
| APA 引用 | Synthesizer.check_references() 无错误 |
| 元数据 | Maintainer 更新时间戳 |

---

## 数据流图

```
queries.json → Searcher → index.json
                            ↓
                    Manager.filter → topic.json
                            ↓
                    Summarizer → notes/labels
                            ↓
                    Synthesizer → 笔记.md
                            ↓
                    jina-ai/Exa/Tavily补充检索 → 代理整合补充结果 → 笔记.md
                            ↓
                    代理撰写 → 综述.md
                            ↓
                    Synthesizer.check → APA 核查
                            ↓
                    Maintainer → 元数据更新
```

*详见 [索引](index.md)*
