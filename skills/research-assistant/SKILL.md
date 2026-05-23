---
name: research-assistant
description: >
  科研文献综述全流程助手。支持文献检索、文献AI总结、知识库管理、主题筛选、笔记导出、文献综述撰写、研究现状撰写。
version: 5.3.0
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
3. **阶段化执行**：检索→整理→分析→撰写→检查，五阶段顺序执行
4. **补充检索**：使用 Exa/Tavily 补充政策文件、行业报告等到笔记

---

## 边界条件

| 边界 | 说明 |
|------|------|
| ✅ 能做 | 文献检索、AI总结、知识库管理、笔记导出、综述撰写 |
| ❌ 不能做 | 直接修改 PDF/PPT 等二进制文件 |

---

## 快速调用

```bash
# 检索文献 → index.json
python3 scripts/search/Searcher.py --queries queries.json --kb-path knowledge/index.json

# 筛选 topic
python3 scripts/manage/Manager.py filter --kb-path knowledge/index.json \
    --output knowledge/topic/xxx.json --conditions conditions.json

# AI 总结
python3 scripts/summarize/Summarizer.py --kb-path knowledge/topic/xxx.json --provider deepseek

# 导出笔记
python3 scripts/synthesize/Synthesizer.py extract --topic knowledge/topic/xxx.json \
    --output knowledge/note/笔记_xxx.md

# 检查引用
python3 scripts/synthesize/Synthesizer.py check --doc knowledge/review/综述.md
```

---

## 快速导航

| 指南 | 位置 |
|------|------|
| 核心工作流 | [references/workflows.md](references/workflows.md) |
| 文献综述撰写指南 | [references/Guide_to_Writing_a_Literature_Review.md](references/Guide_to_Writing_a_Literature_Review.md) |
| 研究现状撰写指南 | [references/Guide_to_Writing_a_Research_Status_Review.md](references/Guide_to_Writing_a_Research_Status_Review.md) |

---

## 数据流总览

```
阶段1：理解篇 → 阅读《文献综述撰写指南》，明确研究问题
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
| 5.3.0 | 2026-05-23 | 按 skill-developer 新标准重构：核心原则、边界条件、快速调用、指南导航 |
| 5.2.0 | 2026-05-18 | 阶段3新增补充检索步骤 |
| 5.1.0 | 2026-05-15 | 整合写作指南 |
| 5.0.0 | 2026-05-09 | 从 manage-project 拆分，聚焦知识库管理 |
