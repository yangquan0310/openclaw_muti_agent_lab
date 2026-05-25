---
name: research-assistant
description: >
  科研文献综述全流程助手。支持文献检索、AI总结、知识库管理、笔记导出、文献综述撰写、研究现状撰写。
version: 5.5.0
author: Yang Quan
metadata:
  openclaw:
    emoji: 🔬
    requires:
      bins: [python3]
---

# research-assistant（研究助手）

> 科研文献综述全流程助手

---

## 核心原则

1. **index.json 是核心**：所有知识产出以 index.json 为核心驱动
2. **Git 版本控制**：使用 Git 管理版本，不需要额外归档
3. **阶段化执行**：理解 → 检索 → 阅读 → 撰写 → 检查，五阶段顺序执行
4. **补充检索**：使用 Exa/Tavily 补充政策文件、行业报告等到笔记

---

## 边界条件

| 边界 | 说明 |
|------|------|
| ✅ 能做 | 文献检索（多引擎自动路由）、AI总结、知识库管理、笔记导出、综述撰写 |
| ❌ 不能做 | 直接修改 PDF/PPT 等二进制文件 |

---

## 快速调用

```bash
research-assistant search --keyword "深度学习" --limit 20 --year-min 2020
research-assistant search --keyword "deep learning" --limit 20
research-assistant summarize --kb-path knowledge/index.json
research-assistant manage info --kb-path knowledge/index.json
research-assistant manage merge --inputs a.json,b.json --output merged.json
```

### search 子命令（多态自动路由）

| 参数 | 说明 |
|------|------|
| `--keyword TEXT` | 检索关键词，自动判断语言路由 |
| `--queries FILE` | 高级用法：检索条件 JSON 文件 |
| `--limit N` | 最大结果数（默认 20）|
| `--year-min Y` / `--year-max Y` | 发表年份范围 |
| `--kb-path PATH` | 知识库路径 |

**语言路由**：中文关键词 → CNKI（主）→ SemSch（备）；英文关键词 → SemSch（主）→ Scholar/GS（备）
---

## 书籍目录

| 章节 | 对应的问题 |
|------|------------|
| [ch01_how-to-execute-research-workflow.md](references/ch01_how-to-execute-research-workflow.md) | 如何执行研究工作流？ |
| [ch02_how-to-search-academic-papers.md](references/ch02_how-to-search-academic-papers.md) | 如何检索学术文献？ |
| [ch03_how-to-manage-knowledge-base.md](references/ch03_how-to-manage-knowledge-base.md) | 如何管理知识库？ |
| [ch04_how-to-summarize-papers.md](references/ch04_how-to-summarize-papers.md) | 如何总结文献？ |
| [ch05_how-to-synthesize-notes.md](references/ch05_how-to-synthesize-notes.md) | 如何合成笔记？ |
| [ch06_how-to-write-literature-review.md](references/ch06_how-to-write-literature-review.md) | 如何撰写文献综述？ |
| [ch07_how-to-write-research-status.md](references/ch07_how-to-write-research-status.md) | 如何撰写研究现状？ |
| [ch08_how-to-maintain-metadata.md](references/ch08_how-to-maintain-metadata.md) | 如何维护元数据？ |

---

## 数据流总览

```
阶段1：理解 → 阅读《文献综述撰写指南》，明确研究问题
    ↓
阶段2：检索 → Searcher → index.json
    ↓
阶段3：阅读 → Manager → topic.json → Summarizer → notes/labels → Synthesizer → 笔记.md
    ↓
阶段4：撰写 → 代理阅读笔记，撰写综述/研究现状
    ↓
阶段5：检查 → Synthesizer 检查APA引用 → Maintainer 更新元数据
```

---

## 目录结构

```
项目/
├── knowledge/
│   ├── index.json           ← 核心数据源
│   ├── topic/               ← 主题子集
│   │   └── {topic}.json
│   ├── note/                ← 结构化笔记
│   │   └── 笔记_{topic}.md
│   └── review/              ← 综述文档
│       ├── 综述_{topic}.md
│       └── 研究现状.md
└── metadata.json
```

---

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 5.5.0 | 2026-05-25 | 重构 references：新框架 8 章，how-to 格式命名，问题→方法论→工作流→执行标准结构 |
| 5.4.0 | 2026-05-24 | CLI 重构：统一 search 命令 + 语言自动路由 |
| 5.3.0 | 2026-05-23 | 按 skill-developer 新标准重构 |
