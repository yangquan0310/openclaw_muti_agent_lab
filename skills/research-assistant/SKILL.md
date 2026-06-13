---
name: research-assistant
description: >
  科研文献综述全流程助手。支持文献检索、AI总结、知识库管理、笔记导出、文献综述撰写、研究现状撰写。
  **v5.12.0 重点**：参数优先级统一为 **key > config > env**（之前是 key > env > config）。
  让 config.json 显式配置优先于散落的环境变量，便于跨环境/跨项目复用。涉及模块：Summarizer / Searcher / SemSchSearcher / ScholarSearcher / ZoteroJianguoyunDownloader。config.json 新增 `semantic_scholar.api_key` / `zotero.{user_id,api_key}` / `jianguoyun.{url,user,password}` 明文字段（默认空，自动 fallback 到 .env）。
  **v5.11.0 重点**：references 重构为 13 个文件（1 索引 + 1 工作流 + 1 排版 + 6 模块 + 4 文体）。4 个文体撰写指南（narrative-review / meta-analysis / observational-study / experimental-study）基于心理学 APA 7 + JARS-Quant 规范，**不**用医学 PRISMA / STROBE / CONSORT。
version: 5.12.0
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

## 指南导航（v5.11.0 重构：13 个 references）

| # | 章节 | 文件 | 内容 |
|---|------|------|------|
| 1 | references 索引 | [index.md](references/index.md) | references 目录索引 |
| 2 | 研究助手工作流 | [research-workflow.md](references/research-workflow.md) | 5 阶段流程原则 |
| 3 | apaquarto 排版指南 | [apaquarto-manuscript.md](references/apaquarto-manuscript.md) | 严格 APA 7 manuscript 完整配置 |
| 4 | search 模块使用指南 | [module-search.md](references/module-search.md) | 检索（学术数据库：CNKI / SemSch / Google Scholar）|
| 5 | manage 模块使用指南 | [module-manage.md](references/module-manage.md) | 知识库管理（merge / filter / info）|
| 6 | maintain 模块使用指南 | [module-maintain.md](references/module-maintain.md) | 元数据维护（MetadataManager）|
| 7 | summarize 模块使用指南 | [module-summarize.md](references/module-summarize.md) | 总结（+ JCR / SCI 分区更新）|
| 8 | synthesize 模块使用指南 | [module-synthesize.md](references/module-synthesize.md) | 合成（extract_notes / check_references / fix_references）|
| 9 | download 模块使用指南 | [module-download.md](references/module-download.md) | PDF 下载（DOI / Zotero key → 坚果云 → wiki raw）|
| 10 | 叙述性综述撰写指南 | [narrative-review.md](references/narrative-review.md) | APA 7 + Baumeister & Leary 1997 + SANRA |
| 11 | 元分析撰写指南 | [meta-analysis.md](references/meta-analysis.md) | APA 7 + JARS-Quant Table 9 (MARS) |
| 12 | 观察研究报告撰写指南 | [observational-study.md](references/observational-study.md) | APA 7 + JARS-Quant Tables 1, 5, 6 |
| 13 | 实验研究报告撰写指南 | [experimental-study.md](references/experimental-study.md) | APA 7 + JARS-Quant Table 2 |

## 模板资源

| 模板 | 文件 |
|------|------|
| 文献综述模板 | [assets/文献综述模板.md](assets/文献综述模板.md) |
| 研究现状模板 | [assets/研究现状模板.md](assets/研究现状模板.md) |
| 检索报告模板 | [assets/检索报告模板.md](assets/检索报告模板.md) |

---

## 数据流总览

```
阶段1：理解 → 阅读《研究助手工作流》（research-workflow.md），明确研究问题
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
| 5.11.0 | 2026-06-12 | **references 重构为 13 个文件**：删 12 个旧文件（typesetting, formatting-standards, research-status, literature-review, easyscholar-api, paper-search, knowledge-management, paper-summary, note-synthesis, metadata-maintenance, narrative-synthesis, systematic-review），重组为 1 索引 + 1 工作流 + 1 排版 + 6 模块 + 4 文体。4 个文体撰写指南（narrative-review / meta-analysis / observational-study / experimental-study）基于心理学 APA 7 + JARS-Quant 规范，**不**用医学 PRISMA / STROBE / CONSORT。 |
| 5.10.0 | 2026-06-12 | **apaquarto 排版指南重大修正**（基于跨期选择年龄差异论文实战）：① `_quarto.yml`/`_extensions`/`references.bib` 全在 `manuscripts/` 下；② 不需要 `header.tex`；③ 引用必须用 `[@key]` 语法（参考 Quarto Citations 文档）；④ 图表直接放正文（apaquarto 自动处理 `floatsintext`）；⑤ 安装命令 `cd manuscripts` 不复制；⑥ 渲染命令加 `--resource-path .`。 |
| 5.9.0 | 2026-06-04 | **铁律：所有学术论文默认 APA 7 manuscript mode（apaquarto 范式 ④）**。新增 `apaquarto-manuscript.md` 详细配置指南；`typesetting.md` 升级到四范式；`formatting-standards.md` 新增范式决策提示。源自记忆机制认知推断论文实战。 |
| 5.8.0 | 2026-05-30 | 新增 easyScholar API 支持：获取期刊 JCR/SCI 分区 |
| 5.7.0 | 2026-05-30 | 目录结构重构：研究现状_{topic}.md、检索报告、检索条件独立目录 |
| 5.6.0 | 2026-05-26 | 重构 references 为原则性章节；新增文献综述模板、研究现状模板 |
| 5.5.0 | 2026-05-25 | 重构 references：新框架 8 章，how-to 格式命名，问题→方法论→工作流→执行标准结构 |
| 5.4.0 | 2026-05-24 | CLI 重构：统一 search 命令 + 语言自动路由 |
| 5.3.0 | 2026-05-23 | 按 skill-developer 新标准重构 |
