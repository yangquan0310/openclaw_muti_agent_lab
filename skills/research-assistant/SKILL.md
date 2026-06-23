---
name: research-assistant
description: >
  老板研究工作的全流程数字助手——wiki ↔ Zotero ↔ WebDAV 三联动场景下激活。提供文献检索、PDF 同步、本地 PDF 反向上传、源笔记 / 综述产出、三方一致性检查、APA 7 排版指南。详见下方“触发场景”与 README。
version: 6.0.6
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

## 触发场景

需要在以下场景下激活本技能（**wiki ↔ Zotero ↔ WebDAV 三联动**是核心识别信号）：

1. 检索论文（Semantic Scholar / CNKI / Google Scholar）
2. 拉 PDF 到 WebDAV（坚果云）
3. 本地 PDF 反向上传到 Zotero + WebDAV + wiki source（v6.0.3+ upload）
4. 在 Zotero 库建条目 + wiki/sources/ 写 source YAML
5. 单篇笔记写到 wiki/syntheses/
6. 多篇综述写到 wiki/syntheses/
7. 管理 wiki source 列表（merge / filter / stats）
8. 跑 wiki source ↔ Zotero 条目 ↔ WebDAV 附件三方一致性检查（含 drift-graph）
9. 用 apaquarto 排版终稿（APA 7 + Quarto + apa.csl）
10. 批量迁移项目 knowledge/ 到 wiki
11. 跑 search 报告到 wiki

---

## 核心原则

1. **wiki ↔ Zotero ↔ WebDAV 三联动是核心**：所有知识产出以 wiki（人可读视图 + 笔记）+ Zotero（文献元数据唯一权威）+ WebDAV（PDF 附件）为三方联动驱动（v5.20.0 起取代 index.json / knowledge/）
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

## 快速调用（v5.20.0+ 实际命令，wiki 后端）

```bash
# 7 个模块 CLI 入口（v6.0.3+）：python3 scripts/main.py <module> [args]

# 1. 检索（自动路由中文/英文）
python3 scripts/main.py search --keyword "深度学习" --limit 20 --topic general
python3 scripts/main.py search --keyword "working memory cognitive" --limit 5 --dry-run

# 2. 下载（Zotero → 坚果云 WebDAV → wiki raw）
python3 scripts/main.py download --zotero-key BNA4WATT

# 2b. 反向上传（v6.0.3+ 本地 PDF → Zotero + WebDAV + wiki source）
python3 scripts/main.py upload --pdf-path /data/local-pdfs/smith-2025.pdf --slug smith-2025-memory --doi "10.1234/example.2025.001"

# 3. 单篇笔记（→ wiki/syntheses/<date>-summarize-<slug>.md）
python3 scripts/main.py summarize --source-id buzsaki-2002-hippocampal-theta

# 4. 多篇综述（→ wiki/syntheses/<date>-extract-<slug>.md）
python3 scripts/main.py synthesize extract --source-id buzsaki-2002-hippocampal-theta
# 注：synthesize check/fix 已在 v5.16.0 范围外移除（未迁移到 wiki），如需 APA 7 引用核验请走 references/apa7-standards.md

# 5. wiki source 列表管理
python3 scripts/main.py manage list
python3 scripts/main.py manage stats
python3 scripts/main.py manage merge --inputs source.a,source.b
python3 scripts/main.py manage filter --has-zotero-key true

# 6. 一致性检查（wiki ↔ Zotero ↔ WebDAV）
python3 scripts/main.py maintain check-drift
python3 scripts/main.py maintain list-missing
python3 scripts/main.py maintain report
```

### 7 模块核心参数

| 子命令 | 核心参数 | 说明 |
|--------|---------|------|
| `search` | `--keyword` 或 `--queries` + `--limit` + `--topic` + `--dry-run` | 检索关键词（必填二选一）|
| `download` | `--zotero-key` 或 `--doi` | 二选一，8 字符 Zotero item key |
| `summarize` | `--source-id`（必填，wiki source slug）| + 可选 `--output` |
| `synthesize` | `extract`（仅 extract 已实现；check/fix v5.16.0 范围外未迁移）| `--source-id` |
| `manage` | `list` / `stats` / `merge` / `filter` / `info` 五 sub-action | 各自参数不同 |
| `maintain` | `check-drift` / `list-missing` / `report` 三 sub-action（v5.20.0 新增）| 一致性检查 |

**v5.20.0+ 关键变化**：
- 所有模块**走 wiki 后端**（`~/.openclaw/wiki/`），不再用 `index.json` / `knowledge/`
- `--source-id` 是 wiki source 裸名（不带 `.md` / 不带路径），如 `buzsaki-2002-hippocampal-theta`
- Zotero / WebDAV 通过 rclone + Zotero API 自动同步
---

## 指南导航（v6.0.4：18 个 references——1 索引 + 1 工作流 + 1 排版 + 7 模块 + 4 文体 + 1 PRISMA SOP + 3 标准）

| # | 章节 | 文件 | 内容 |
|---|------|------|------|
| 1 | references 索引 | [index.md](references/index.md) | references 目录索引 |
| 2 | 研究助手工作流 | [research-workflow.md](references/research-workflow.md) | 5 阶段流程原则 |
| 3 | apaquarto 排版指南 | [apaquarto-manuscript-guide.md](references/apaquarto-manuscript-guide.md) | 严格 APA 7 manuscript 完整配置 |
| 4 | search 模块使用指南 | [module-search.md](references/module-search.md) | 检索（学术数据库：CNKI / SemSch / Google Scholar）|
| 5 | manage 模块使用指南 | [module-manage.md](references/module-manage.md) | 知识库管理（merge / filter / info）|
| 6 | maintain 模块使用指南 | [module-maintain.md](references/module-maintain.md) | 元数据维护（MetadataManager）|
| 7 | summarize 模块使用指南 | [module-summarize.md](references/module-summarize.md) | 总结（v6.0.2+ 多模态：pypdf + pypdfium2 + tesseract；工具不攥写 narrative）|
| 8 | synthesize 模块使用指南 | [module-synthesize.md](references/module-synthesize.md) | 合成（extract_notes / check_references / fix_references）|
| 9 | download 模块使用指南 | [module-download.md](references/module-download.md) | PDF 下载（DOI / Zotero key → 坚果云 → wiki raw）|
| 10 | 叙述性综述撰写指南 | [narrative-review-guide.md](references/narrative-review-guide.md) | APA 7 + Baumeister & Leary 1997 + SANRA |
| 11 | 元分析撰写指南 | [meta-analysis-guide.md](references/meta-analysis-guide.md) | APA 7 + JARS-Quant Table 9 (MARS) |
| 12 | 观察研究报告撰写指南 | [observational-study-guide.md](references/observational-study-guide.md) | APA 7 + JARS-Quant Tables 1, 5, 6 |
| 13 | 实验研究报告撰写指南 | [experimental-study-guide.md](references/experimental-study-guide.md) | APA 7 + JARS-Quant Table 2 |
| 14 | PRISMA 系统综述 SOP（v5.21.0 新增）| [prisma-workflow.md](references/prisma-workflow.md) | 9 阶段流程：PICO → 多源检索 → 筛选 → 数据抽取 → 偏倚评估 → PRISMA 流程图 → 证据综合 → GRADE 评级 |

| 16 | APA 7 引用核验（v5.21.0 新增）| [apa7-standards.md](references/apa7-standards.md) | 50 项 in-text + reference list + DOI 核验 |
| 17 | 原创性核验（v5.21.0 新增）| [originality-standards.md](references/originality-standards.md) | 30 项：直接抄袭 + 自我抄袭 + 翻译抄袭 + 观点 + LLM 痕迹 |
| 18 | 终稿完整性审计（v5.21.0 新增）| [manuscript-audit-standards.md](references/manuscript-audit-standards.md) | 60 项终稿审计：完整性 + rationale + 引用库 + 翻译覆盖 + artifact 健康 |

## 模板资源

> v5.11.0 重构后，原"文献综述模板.md""研究现状模板.md"已被英文版文体模板取代（`narrative-review-template.md` / `meta-analysis-template.md` / `observational-study-template.md` / `experimental-study-template.md`），不再保留中文版。

| 模板 | 文件 |
|------|------|
| 检索报告模板 | [assets/检索报告模板.md](assets/检索报告模板.md) |
| Motivation Thread + Section Blueprints 模板（v5.21.0 新增）| [assets/motivation-thread-template.md](assets/motivation-thread-template.md) | 章节主线动机 + 段落蓝图 + rewrite_matrix |
| Nature 风格润色 Prompt（v5.21.0 新增）| [assets/polish-nature-style.md](assets/polish-nature-style.md) | 中文笔记 → Nature 风格学术中文 + Style Calibration checklist |
| Data Availability Statement 模板（v5.21.0 新增）| [assets/data-availability-template.md](assets/data-availability-template.md) | Nature/Cell/Science 4 模板（完全公开/部分公开/第三方/理论）|

---

## 数据流总览（v5.20.0+ wiki 后端）

```
阶段1：理解 → 阅读《研究助手工作流》（research-workflow.md），明确研究问题
    ↓
阶段2：检索 → Searcher / ZoteroSearcher → Zotero 库（wiki source 写入 wiki/sources/）
    ↓
阶段3：阅读 → Summarizer 调 LLM 提取结构化笔记 → 写入 wiki/syntheses/<date>-summarize-<slug>.md → jina-ai/Tavily 补充检索 → agent 拿到笔记后自己攥写 narrative（工具不攥写）
    ↓
阶段4：撰写 → Synthesizer.extract_notes() 抽字段 → agent 阅读笔记后攥写综述 → 写入 wiki/syntheses/<date>-extract-<slug>.md
    ↓
阶段5：检查 → WikiZoteroManager.check_drift() 跑三方一致性 + 6 项 references 核验清单（APA 7 / 原创性 / 终稿审计）
```

---

## 目录结构（wiki 后端）

```
~/.openclaw/wiki/
├── sources/                 ← 文献条目元数据（每篇 1 个 source YAML）
│   └── source.<slug>.md
├── syntheses/               ← 笔记 / 综述（summarize / extract 输出）
│   ├── <date>-summarize-<slug>.md
│   └── <date>-extract-<slug>.md
├── concepts/                ← 概念卡（跨项目主题索引）
└── reports/                 ← search 报告 + drift 报告
```

## 版本历史

> 完整版本演进记录。**description 字段保持简洁**，仅包含触发短语 + 最近 1-2 个版本重点。

| 版本 | 日期 | 主要变更 |
|------|------|----------|
| **v6.0.6** | **2026-06-23** | **代码 polish（清 v6.0.5 专项审计报告末尾 4 项新发现）**：**(1)🟡** `scripts/upload/Uploader.py` `uploaded_by` 改读 `OPENCLAW_AGENT_ID` → `OPENCLAW_AGENT_NAME` → `AGENT_NAME` → `USER` → `"unknown"` 兑底链（修复 v6.0.3 硬编码 `"steward"`，多 agent 场景下审计追溯准确）；**(2)🟡** `scripts/main.py` `manage info` 加 `--source-id` 参数——返回单篇 wiki source 详情（id + frontmatter_raw + file_path），不传退化为 stats（修复 v6.0.3 文档广告但代码未实现）；**(3)🟡** `scripts/search/utils.py` `search_by_keyword()` fallback 触发时主动提示用户（`⚠️ fallback 已触发 → <engine>`）+ 返回 `_meta.fallback_used` / `_meta.fallback_reason` 字段——CLI JSON 输出也带上 fallback 信息（修复 primary 0 命中时默默退化）；**(4)🟢** `scripts/maintain/Maintainer.py` 删除（v5.14.0 旧协调器无外部引用）+ `__init__.py` 精简到只导出 `WikiZoteroManager`——references/index.md + research-workflow.md 同步更新。**严格遵循"工具不替代 agent"边界**——读环境变量不攒策略、`info --source-id` 只读 frontmatter 不攒 narrative、fallback 提示只打印不改路由。详见 `wiki/syntheses/2026-06-23-v6-0-6-polish-log.md`。|
| **v6.0.5** | **2026-06-23** | **代码修复（psychologist 用户意见 4 项痛点）**：**(1)🔴** `scripts/main.py` 彻底删 synthesize check/fix argparse 残留（v6.0.4 文档层删除但 CLI 仍接受参数 → 现在 argparse 层拒绝）；**(2)🔴** `scripts/upload/Uploader.py` 加 `_humanize_title_from_filename()`，upload title 默认解析 PDF 文件名（`buzsaki-2002-hippocampal-theta.pdf` → `2002 - Buzsaki - Hippocampal - Theta`）替代 slug 兜底；**(3)🟡** search 加 arXiv 路由：`scripts/search/ArxivSearcher.py`（新文件）+ `utils._LANG_MAP` 加 `arxiv`/`ax`/`preprint` + 英文数学/物理关键词启发式（30+ 模式）→ 主引擎改走 arXiv；**(4)🟡** `scripts/summarize/Summarizer.py` `_classify_type()` 加 `theorem` / `preprint-physics` / `book` 三类（支撑老板数/物/心交叉研究）。**严格遵循"工具不替代 agent"边界**——helper 只做最小文件名解析、arXiv 只调 API、分类只用规则不用 LLM。详见 `wiki/syntheses/2026-06-23-v6-0-5-improves-log.md`。|
| **v6.0.4** | **2026-06-23** | **文档修复（审计报告 12 项可执行修复，不动代码）**：frontmatter version 升 6.0.3 + 删 synthesize check/fix 命令广告 + 删 2 个 assets 死链 + references 重命名（方案 B：8 个文件加 `-guide`/`-workflow`/`-standards` 后缀）+ description 精简 + 核心原则 1 由 index.json 改为 wiki↔Zotero↔WebDAV + 指南导航 13→18 + 模块数 6→7 + `<id>` → `<slug>` + 删 hooks/ 引用。**7-agent peer review SOP 删除**（老板 19:23 明确废弃）已在 v5.21.2 后处理。详见 `wiki/syntheses/2026-06-23-v6.0.4-fixes-log.md`。|
| v5.21.0 | 2026-06-22 | **增补 9 项参考文档**
| v5.21.2 | 2026-06-22 | **删除 hooks/ 整目录**（11 个 markdown SOP，老板 14:29 明确不需要 hooks）；SKILL.md description 重写为只描述 wiki-zotero-webdav 实际运作流程，删除与功能不对应的描述 |（SOP 级，非功能）：①PRISMA 系统综述 SOP ②章节 motivation 蓝图 ③Nature 风格润色 ④APA 7 引用核验 ⑤原创性核验 ⑥Data Availability 模板 ⑦终稿完整性审计（注：原含 ⑧quarto 引用审计 hook，v5.21.2 已删除；v6.0.4 删除 7-agent 同行评议 SOP） |
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
