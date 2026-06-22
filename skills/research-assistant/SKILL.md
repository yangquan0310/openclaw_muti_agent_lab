---
name: research-assistant
description: >
  当需要：检索论文（Semantic Scholar / CNKI / Scholar）、管理文献知识库（按 zotero_item_key / 主题筛选）、AI 总结论文、生成文献综述/研究现状、维护 wiki source ↔ Zotero 条目 ↔ WebDAV 附件一致性、批量迁移项目 knowledge/ 到 wiki、跑 search 报告到 wiki、PRISMA 系统综述、章节 motivation 蓝图、quarto APA 引用审计、synthesize 7-agent 同行评议、Nature 风格润色、APA 7 引用核验、原创性核验、Data Availability 声明生成、终稿完整性审计 时激活。
version: 5.21.0
author: Yang Quan
metadata:
  openclaw:
    emoji: 🔬
    requires:
      bins: [python3]
---
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
| 14 | PRISMA 系统综述 SOP（v5.21.0 新增）| [prisma-systematic-review.md](references/prisma-systematic-review.md) | 9 阶段流程：PICO → 多源检索 → 筛选 → 数据抽取 → 偏倚评估 → PRISMA 流程图 → 证据综合 → GRADE 评级 |
| 15 | Synthesize 7-agent 同行评议（v5.21.0 新增）| [synthesize-peer-review.md](references/synthesize-peer-review.md) | EIC + 3 dynamic + Devil's Advocate + 0-100 rubric + R&R Traceability Matrix |
| 16 | APA 7 引用核验（v5.21.0 新增）| [apa7-citation-checklist.md](references/apa7-citation-checklist.md) | 50 项 in-text + reference list + DOI 核验 |
| 17 | 原创性核验（v5.21.0 新增）| [originality-checklist.md](references/originality-checklist.md) | 30 项：直接抄袭 + 自我抄袭 + 翻译抄袭 + 观点 + LLM 痕迹 |
| 18 | 终稿完整性审计（v5.21.0 新增）| [manuscript-audit-checklist.md](references/manuscript-audit-checklist.md) | 60 项终稿审计：完整性 + rationale + 引用库 + 翻译覆盖 + artifact 健康 |

## 模板资源

| 模板 | 文件 |
|------|------|
| 文献综述模板 | [assets/文献综述模板.md](assets/文献综述模板.md) |
| 研究现状模板 | [assets/研究现状模板.md](assets/研究现状模板.md) |
| 检索报告模板 | [assets/检索报告模板.md](assets/检索报告模板.md) |
| Motivation Thread + Section Blueprints 模板（v5.21.0 新增）| [assets/motivation-thread-template.md](assets/motivation-thread-template.md) | 章节主线动机 + 段落蓝图 + rewrite_matrix |
| Nature 风格润色 Prompt（v5.21.0 新增）| [assets/polish-nature-style.md](assets/polish-nature-style.md) | 中文笔记 → Nature 风格学术中文 + Style Calibration checklist |
| Data Availability Statement 模板（v5.21.0 新增）| [assets/data-availability-template.md](assets/data-availability-template.md) | Nature/Cell/Science 4 模板（完全公开/部分公开/第三方/理论）|

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

## 版本历史

> 完整版本演进记录。**description 字段保持简洁**，仅包含触发短语 + 最近 1-2 个版本重点。

| 版本 | 日期 | 主要变更 |
|------|------|----------|
| v5.21.0 | 2026-06-22 | **全面补充薄弱环节**：吸收三家之长（ARS / Nature-skills / PaperSpine）补强 9 项——①PRISMA 系统综述 SOP ②章节 motivation 蓝图 ③quarto 引用审计 hook ④synthesize 7-agent 同行评议 ⑤Nature 风格润色 ⑥APA 7 引用核验 ⑦原创性核验 ⑧Data Availability 模板 ⑨终稿完整性审计 |
| v5.20.0 | 2026-06-22 | SKILL.md description 精简 + 版本历史移至末尾（老板纠错） |
| v5.19.0 | 2026-06-22 | 新建 WikiSearchReport.py（search 命中写 wiki report） + 修 _resolve_env() 解析 ${VAR} bug |
| v5.18.0 | 2026-06-22 | 6 个项目 knowledge/ 按 B 方案改写为 wiki/reports/<date>-all-papers.md（1764 papers / 866KB） |
| v5.17.0 | 2026-06-22 | SKILL.md + references 文档同步（13 文件全反映 v5.15.0 / v5.16.0 改动） |
| v5.16.0 | 2026-06-22 | 6 模块全部走 wiki（删 3 旧主类，WikiXxx.py 重命名为默认名），老板 00:08 指令"不需要向后兼容" |
| v5.15.0 | 2026-06-22 | WikiZoteroManager Python 类（5 方法 + CLI，check-drift 跑通）+ Al-Kari title PATCH 修复 + concept/synthesis 联动 SOP + ZoteroSearcher/ZoteroAdder 骨架 |
| v5.14.0 | 2026-06-22 | 删 MetadataManager / VersionController 类（老板 19:39 指令"全部转移到 wiki"），Maintainer.py 376→46 行精简 |
| v5.13.4 | 2026-06-22 | 新增 zotero-patch-with-version.md + arxiv-title-parse.md hooks（实战发现 Zotero API 用 If-Unmodified-Since-Version 头） |
| v5.13.3 | 2026-06-22 | 新增 wiki-source-missing-in-zotero.md hook（4 路径：add-doi / CrossRef / arXiv / 标红） |
| v5.13.2 | 2026-06-22 | 新增 manual-add-item / cleanup-wrong-entry hooks + add-zotero-source 失败处理附录 |
| v5.13.1 | 2026-06-22 | 新增 dashboard.md（**v5.21.2 已删除 hooks/ 整目录**，按老板 14:29 明确不需要 hooks）|
| v5.13.0 | 2026-06-22 | Maintain 模块工作平台迁移到 wiki-zotero-webdav 三联动 |
| v5.12.0 | 2026-06-22 | 参数优先级统一为 key > config > env（涉及 Summarizer / Searcher / SemSchSearcher / ScholarSearcher / ZoteroJianguoyunDownloader） |
| v5.11.0 | 2026-06-21 | references 重构为 13 个文件（1 索引 + 1 工作流 + 1 排版 + 6 模块 + 4 文体），4 文体指南（narrative-review / meta-analysis / observational / experimental） |

> **注意**：v5.11.0 之前的历史在 `git log` 里。
