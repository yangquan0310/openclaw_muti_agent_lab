---
name: research-assistant
description: >
  科研文献综述全流程助手。支持文献检索、AI总结、知识库管理、笔记导出、文献综述撰写、研究现状撰写。
  **v5.9.0 重点**：默认所有学术论文走 APA 7 manuscript mode（apaquarto 范式 ④）。
version: 5.9.0
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
4. **补充检索**：使用 jina-ai/Exa/Tavily 补充政策文件、行业报告等到笔记

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
research-assistant summarize --kb-path knowledge/index.json --update-jcr
research-assistant summarize --kb-path knowledge/index.json --update-jcr --dry-run
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

## 指南导航

| 章节 | 文件 | 内容 |
|------|------|------|
| 研究工作流 | [research-workflow.md](references/research-workflow.md) | 五阶段流程原则 |
| 文献检索 | [paper-search.md](references/paper-search.md) | 检索策略与引擎选择 |
| 知识库管理 | [knowledge-management.md](references/knowledge-management.md) | index.json 管理原则 |
| 文献总结 | [paper-summary.md](references/paper-summary.md) | Summarizer 使用原则 |
| 笔记合成 | [note-synthesis.md](references/note-synthesis.md) | Synthesizer 使用原则 |
| 文献综述撰写 | [literature-review.md](references/literature-review.md) | 综述撰写原则 |
| 研究现状撰写 | [research-status.md](references/research-status.md) | 现状报告撰写原则 |
| 元数据维护 | [metadata-maintenance.md](references/metadata-maintenance.md) | Maintainer 使用原则 |
| 🆕 排版原则 | [typesetting.md](references/typesetting.md) | Quarto 四范式（书 / 基础 / 一般 / **apaquarto 严格 APA 7**）|
| 🆕 APA 7 manuscript 详细配置 | [apaquarto-manuscript.md](references/apaquarto-manuscript.md) | 范式 ④ 完整环境/扩展/YAML/排错指南 |
| 排版标准 | [formatting-standards.md](references/formatting-standards.md) | 写作内容规范 + 范式决策 |
| 期刊等级查询 | [easyScholar API](references/easyscholar-api.md) | EasyScholarRanker 使用原则 |

## 模板资源

| 模板 | 文件 |
|------|------|
| 文献综述模板 | [assets/文献综述模板.md](assets/文献综述模板.md) |
| 研究现状模板 | [assets/研究现状模板.md](assets/研究现状模板.md) |
| 检索报告模板 | [assets/检索报告模板.md](assets/检索报告模板.md) |

---

## 数据流总览

```
阶段1：理解 → 阅读《文献综述撰写指南》（literature-review.md），明确研究问题
    ↓
阶段2：检索 → Searcher → index.json（数据库检索）
    ↓
阶段3：阅读 → Manager → topic.json → Summarizer → notes/labels → Synthesizer.extract_notes() → 笔记.md → jina-ai/Tavily补充检索 → 代理整合补充结果写入笔记
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
│   │   └── 研究笔记_{topic}.md
│   ├── review/              ← 综述文档
│   │   ├── 文献综述_{topic}.md
│   │   └── 研究现状_{topic}.md
│   ├── retrieval_report/     ← 检索报告
│   │   └── 检索报告_{topic}.md
│   └── search_query/        ← 检索条件
│       └── 检索条件_{topic}.json
│ 
└── metadata.json
```

---

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 5.9.0 | 2026-06-04 | **铁律：所有学术论文默认 APA 7 manuscript mode（apaquarto 范式 ④）**。新增 `apaquarto-manuscript.md` 详细配置指南；`typesetting.md` 升级到四范式；`formatting-standards.md` 新增范式决策提示。源自记忆机制认知推断论文实战。 |
| 5.8.0 | 2026-05-30 | 新增 easyScholar API 支持：获取期刊 JCR/SCI 分区 |
| 5.7.0 | 2026-05-30 | 目录结构重构：研究现状_{topic}.md、检索报告、检索条件独立目录 |
| 5.6.0 | 2026-05-26 | 重构 references 为原则性章节；新增文献综述模板、研究现状模板 |
| 5.5.0 | 2026-05-25 | 重构 references：新框架 8 章，how-to 格式命名，问题→方法论→工作流→执行标准结构 |
| 5.4.0 | 2026-05-24 | CLI 重构：统一 search 命令 + 语言自动路由 |
| 5.3.0 | 2026-05-23 | 按 skill-developer 新标准重构 |
