# research-assistant（科研助手）

> **研究工作的全流程数字助手**——让文献检索、知识沉淀、稿件撰写、最终排版形成一条完整链路。

---

## 核心架构

> **wiki ↔ Zotero ↔ WebDAV 三方联动**——三者各司其职，缺一不可。

| 角色 | 载体 | 职责 |
|------|------|------|
| **wiki**（`~/.openclaw/wiki/`） | 知识沉淀层 | 存 source（条目元数据）、synthesis（笔记/综述）、concept（概念卡）|
| **Zotero** | 文献数据库 | 存条目元数据 + 引用关系 + 全库检索 |
| **WebDAV**（坚果云）| 附件存储层 | 存 PDF 原件 + 论文补充材料 |

任何一步操作都必须**三方同步**，不一致 = 数据漂移 = 后续合成会出错。

---

## 七大核心功能

按老板 2026-06-23 拍板的指令顺序：

| # | 功能 | 现状 | 入口命令 | 沉淀位置 |
|---|------|------|---------|---------|
| 1 | **文献检索** | ✅ v5.21.2 已支持多引擎自动路由（CNKI / Semantic Scholar / Google Scholar）| `python3 scripts/main.py search --keyword "..."` | `wiki/sources/<id>.md` |
| 2 | **保存条目到 Zotero** | ✅ v5.13.0+ 已支持自动建条目 + 标签 + 元数据（v6.0.7+ 可选 `--source scihub` 绕过付费墙）| `python3 scripts/main.py download --doi 10.xxxx/xxx [--source {zotero,scihub}]` | Zotero 库 或 `wiki/raw/papers`（v6.0.7+ SciHub 镜像在 `config.json.scibhub.mirrors` 配置）|
| 3 | **管理 WebDAV 附件** | ✅ v5.13.0+ 已支持 rclone 同步到坚果云 | （download `--source zotero` 时内嵌；`--source scihub` 不写 WebDAV）| 坚果云 WebDAV |
| 4 | **管理 OpenClaw wiki 知识库** | ✅ v5.16.0+ 所有模块已迁移 wiki 后端 | `python3 scripts/main.py manage {list,stats,merge,filter,info}` | `~/.openclaw/wiki/` |
| 5 | **对文章进行精读** | ✅ v5.15.0+ 已支持单篇笔记输出（v6.0.2 加本地 PDF 解析：pypdf + pypdfium2 + tesseract）| `python3 scripts/main.py summarize --source-id <slug> [--pdf-path <pdf>] [--ocr]` | `wiki/syntheses/<date>-summarize-<slug>.md` |
| 6 | **攥写学术文章** | ✅ v5.21.0+ 已支持 4 文体模板 | `python3 scripts/main.py synthesize extract --source-id <slug>` | `wiki/syntheses/<date>-extract-<slug>.md` |
| 7 | **文章排版** | ✅ v5.11.0+ 已支持 APA 7 + Quarto + apa.csl | （手工调 `quarto render <file>.md`）| `docs/<title>.pdf` |
| 8 | **本地 PDF 反向上传** | ✅ v6.0.3+ 新增 download 反向对偶（本地 PDF → Zotero + WebDAV + wiki source）| `python3 scripts/main.py upload --pdf-path <pdf> --slug <id>|--doi <doi>` | Zotero 库 + 坚果云 + `wiki/sources/<slug>.md` |

---

## 数据流总览

```
┌──────────────────────────────────────────────────────────────────────┐
│                       老板研究意图（自然语言）                        │
└──────────────────────────────────────────────────────────────────────┘
                                  ↓
┌──────────────────────────────────────────────────────────────────────┐
│  阶段1 检索（search 模块）                                            │
│    多引擎自动路由（中文→CNKI / 英文→Semantic Scholar / Scholar）        │
│    自动去重 + 自动判定中英文 + dry-run 预览                            │
└──────────────────────────────────────────────────────────────────────┘
                                  ↓
┌──────────────────────────────────────────────────────────────────────┐
│  阶段2 收录（download 模块）                                           │
│    DOI/Zotero key → 两个下载源（v6.0.7+ 双源）                          │
│      --source zotero（默认）→ Zotero 建条目 + WebDAV 拉 PDF + wiki raw │
│      --source scihub        → SciHub 绕过付费墙 → wiki/raw/papers     │
│    三方同时落库 + 元数据一致性保证                                    │
└──────────────────────────────────────────────────────────────────────┘
                                  ↓
┌──────────────────────────────────────────────────────────────────────┐
│  阶段3 精读（summarize 模块）                                         │
│    单篇 PDF → LLM 提取结构化笔记                                     │
│    写入 wiki/syntheses/<date>-summarize-<slug>.md                   │
│    支持 jina-ai / Exa / Tavily 补充政策文件/行业报告                  │
└──────────────────────────────────────────────────────────────────────┘
                                  ↓
┌──────────────────────────────────────────────────────────────────────┐
│  阶段4 撰写（synthesize 模块）                                        │
│    多篇笔记 → 文献综述/研究现状                                      │
│    4 文体模板：叙述性综述 / 元分析 / 观察研究 / 实验研究               │
│    可选 5 文体润色与质量核验（见 references/）         │
└──────────────────────────────────────────────────────────────────────┘
                                  ↓
┌──────────────────────────────────────────────────────────────────────┐
│  阶段5 检查（maintain 模块）                                          │
│    wiki ↔ Zotero ↔ WebDAV 三方一致性检查                              │
│    check-drift / list-missing / report 三 sub-action                 │
│    APA 7 引用核验（50 项）+ 原创性核验（30 项）+ 终稿审计（60 项）      │
└──────────────────────────────────────────────────────────────────────┘
                                  ↓
┌──────────────────────────────────────────────────────────────────────┐
│  阶段6 排版（apaquarto）                                              │
│    APA 7 manuscript + Quarto + apa.csl + references.bib              │
│    templates: apaquarto-manuscript-guide.md                         │
│    输出：docs/<title>.pdf                                            │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 目录结构（v5.20.0+ wiki 后端）

```
research-assistant/
├── SKILL.md                          ← 给 LLM 看的入口（含 YAML frontmatter + 触发场景）
├── README.md                         ← 给人类看的纲领（本文档）
├── scripts/
│   ├── main.py                       ← CLI 统一入口（7 模块分发：search / download / upload / summarize / synthesize / manage / maintain）
│   ├── config.json                   ← 统一配置（LLM provider / API key / 路径）
│   ├── search/                       ← 文献检索（多引擎路由）
│   ├── summarize/                    ← 精读笔记（LLM 提取）
│   ├── synthesize/                   ← 多篇合成（4 文体模板）
│   ├── download/                     ← Zotero+WebDAV（默认）/ SciHub（v6.0.7+ 绕过付费墙）拉 PDF
│   ├── manage/                       ← wiki source 列表管理（merge/filter/stats）
│   └── maintain/                     ← 三方一致性检查（check-drift 等）
├── references/                       ← 18 份 SOP 文档
│   ├── index.md                      ← references 目录索引
│   ├── research-workflow.md          ← 5 阶段流程原则
│   ├── apaquarto-manuscript-guide.md ← 严格 APA 7 manuscript 完整配置
│   ├── module-{search,manage,summarize,synthesize,download,maintain,upload}.md
│   ├── narrative-review-guide.md     ← 叙述性综述撰写指南（APA 7 + SANRA）
│   ├── meta-analysis-guide.md        ← 元分析撰写指南（JARS-Quant Table 9）
│   ├── observational-study-guide.md  ← 观察研究报告撰写指南
│   ├── experimental-study-guide.md   ← 实验研究报告撰写指南
│   ├── prisma-workflow.md            ← PRISMA 系统综述 SOP（9 阶段）

│   ├── apa7-standards.md             ← 50 项 APA 7 引用核验
│   ├── originality-standards.md      ← 30 项原创性核验
│   └── manuscript-audit-standards.md ← 60 项终稿完整性审计
├── assets/                           ← 11 个模板
│   ├── apa.csl                       ← APA 7 引用样式（CSL）
│   ├── reference.bib                 ← 引用库（自动从 Zotero 导出）
│   ├── 检索报告模板.md
│   ├── narrative-review-template.md
│   ├── meta-analysis-template.md
│   ├── observational-study-template.md
│   ├── experimental-study-template.md
│   ├── motivation-thread-template.md ← 章节主线 + 段落蓝图 + rewrite_matrix
│   ├── polish-nature-style.md        ← Nature 风格润色 prompt
│   └── data-availability-template.md ← Nature/Cell/Science 4 模板
└── _meta.json                        ← 技能元数据
```

---

## 快速开始（老板最常用的 8 条命令）

```bash
# 1. 检索文献（自动路由中英文）
python3 scripts/main.py search --keyword "深度学习" --limit 20 --topic general
python3 scripts/main.py search --keyword "working memory cognitive" --limit 5 --dry-run

# 2. 收录到 Zotero + 拉 PDF 到 WebDAV + 写 wiki source
python3 scripts/main.py download --zotero-key BNA4WATT
python3 scripts/main.py download --doi 10.1234/example.2024.001
python3 scripts/main.py download --doi 10.1234/example.2024.001 --source scihub   # 绕过付费墙（v6.0.7+）

# 3. 精读（单篇 PDF → 笔记）
python3 scripts/main.py summarize --source-id buzsaki-2002-hippocampal-theta

# 4. 攥写（多篇笔记 → 综述/研究现状）
python3 scripts/main.py synthesize extract --source-id buzsaki-2002-hippocampal-theta
# 注：synthesize check/fix 已在 v5.16.0 范围外移除（未迁移到 wiki），如需 APA 7 引用核验请走 references/apa7-standards.md

# 5. wiki source 列表管理
python3 scripts/main.py manage list
python3 scripts/main.py manage stats
python3 scripts/main.py manage merge --inputs source.a,source.b
python3 scripts/main.py manage filter --has-zotero-key true

# 6. 三方一致性检查
python3 scripts/main.py maintain check-drift
python3 scripts/main.py maintain list-missing
python3 scripts/main.py maintain report
python3 scripts/main.py maintain drift-graph           # ASCII 状态图（light 模式，秒级）
python3 scripts/main.py maintain drift-graph --full    # 完整三方（1-5 分钟）
```

---

## 边界条件

| 边界 | 说明 |
|------|------|
| ✅ 能做 | 文献检索（多引擎自动路由）、AI 总结、wiki 知识库管理、笔记导出、综述攥写、APA 7 排版 |
| ❌ 不能做 | 直接修改 PDF/PPT 等二进制文件（只能读 + 提取文字 + 用 LLM 重写） |
| ❌ 不负责 | 学术观点的最终判断（由作者本人定稿，技能只做证据汇总和格式规范） |
| ⚠️ 边界条件 | Zotero / WebDAV / wiki 三方任一缺失 = 数据漂移 = 后续合成会出错，必须 maintain.check-drift 兜底 |

---

## 环境变量

| 变量 | 用途 | 必填 |
|------|------|------|
| `SEMANTIC_SCHOLAR_API_KEY` | Semantic Scholar 学术检索 | ✅ |
| `DEEPSEEK_API_KEY` / `KIMI_API_KEY` / `TOKENHUB_API_KEY` | Summarizer / Synthesizer 用的 LLM API key（按 config.json 中 `llm.default_provider` 选择）| ✅ |
| `ZOTERO_API_KEY` | Zotero REST API v3 | ✅ |
| `ZOTERO_USER_ID` | Zotero user ID（数字）| ✅ |
| `ZOTERO_GROUP_ID` | Zotero 群组库 ID（仅当用群组库时）| ❌ |
| `CROSSREF_EMAIL` | CrossRef/Unpaywall polite pool（提高 DOI 查找成功率）| ❌ |

---

## 进一步开发方向（v6.0.0+）

| 缺口 | 现状 | 目标 |
|------|------|------|
| **个人研究主页自动生成** | wiki 沉淀足够多后无出口 | 扫描 wiki/sources + syntheses 自动生成个人主页 / ORCID 同步 |
| **引用网络分析** | 基于 Zotero 条目之间的共引网络 | 自动发现研究空白 + 推荐潜在合作方向 |
| **跨项目知识图谱** | 当前 wiki 按 source/synthesis/concept 三类页组织，无跨项目关联 | 加 `concept` 索引层，支持跨项目查询"心理学+AI 交叉"等主题 |

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| **v6.0.6** | **2026-06-23** | **代码 polish（清 v6.0.5 专项审计报告末尾 4 项新发现）**（不动 v6.0.5 代码修复成果）：**(1)🟡 `uploaded_by` 读环境变量**——`scripts/upload/Uploader.py` `create_wiki_source` 不再硬编码 `"steward"`，改读 `OPENCLAW_AGENT_ID` → `OPENCLAW_AGENT_NAME` → `AGENT_NAME` → `USER` → `"unknown"` 兑底链（多 agent 协作场景下审计追溯准确）；**(2)🟡 `manage info --source-id`**——`scripts/main.py` `info` subparser 加 `--source-id` 参数，返回单篇 wiki source 详情（id + 完整 frontmatter_raw + file_path），不传则退化为 stats 总统计（修复 v6.0.3 文档广告但代码未实现）；**(3)🟡 search fallback 主动提示**——`scripts/search/utils.py` `search_by_keyword()` fallback 触发时 print `⚠️ fallback 已触发 → <engine>（主引擎 X 返回 0 篇）` + 返回 `_meta.fallback_used` / `_meta.fallback_reason` 字段；`scripts/main.py` `_run_search` 改走 `search_by_keyword()`（不再只走 WikiSearchReport），CLI JSON 输出带 `fallback_used` 字段（修复 primary 0 命中时默默退化）；**(4)🟢 删 `Maintainer.py`**——`scripts/maintain/Maintainer.py` 删除（v5.14.0 旧协调器、无外部引用验证通过）+ `__init__.py` 精简到只导出 `WikiZoteroManager`；`references/index.md` / `research-workflow.md` 同步更新。**严格遵循"工具不替代 agent"边界**——读环境变量不攒策略、`info --source-id` 只读 frontmatter 不攒 narrative、fallback 提示只打印不改路由。详见 `wiki/syntheses/2026-06-23-v6-0-6-polish-log.md`。|
| **v6.0.5** | **2026-06-23** | **代码修复（按 psychologist 用户意见 4 项痛点）**（不动文档/不动 v6.0.4 文档修复成果）：**(1)🔴 synthesize check/fix argparse 残留彻底清理**——`scripts/main.py` `_run_synthesize` 删 `check` / `fix` 两个 subparser 及其 handler，现在调 `python3 main.py synthesize check` 会直接 argparse `unrecognized arguments: invalid choice 'check' (choose from extract)`（v6.0.4 文档删除但 CLI 仍接受参数的问题彻底解决）；**(2)🔴 upload title 默认解析 PDF 文件名**——`scripts/upload/Uploader.py` 新增 `_humanize_title_from_filename()` helper，`create_wiki_source` 优先级：agent 显式传 title > PDF 文件名解析 > slug 兜底（如 `buzsaki-2002-hippocampal-theta.pdf` → `2002 - Buzsaki - Hippocampal - Theta`）；**(3)🟡 search 加 arXiv 路由**——新增 `scripts/search/ArxivSearcher.py`（继承 BaseSearcher，调 export.arxiv.org/api/query 无 key 无 rate limit）+ `utils.py` `_LANG_MAP` 加 `arxiv` / `ax` / `preprint` 三个 lang 标识 + 英文数学/物理关键词启发式（`topology` / `manifold` / `quantum` / `cond-mat` 等 30+ 模式）→ 主引擎改走 arXiv，SemSch 备用；MathSciNet 需订阅暂列 TODO；**(4)🟡 paper_type 加 theorem / preprint-physics / book**——`scripts/summarize/Summarizer.py` `_classify_type()` 加 3 类（数学定理 / 物理预印本 / 书籍章节），9 测试用例全过。**严格遵循"工具 = 工具说明书，不替代 agent"边界**——helper 只做最小文件名解析、arXiv 只调 API 不攥写 narrative、分类只用规则不用 LLM。详见 `wiki/syntheses/2026-06-23-v6-0-5-improves-log.md`。|
| **v6.0.4** | **2026-06-23** | **文档修复（审计报告 12 项可执行修复）**（不动代码）：**(1)** SKILL.md frontmatter version 5.21.2 → 6.0.3；**(2)** SKILL.md / README.md "快速调用" 删除 synthesize check/fix 命令（未迁移到 wiki）；**(3)** SKILL.md / README.md 删除 assets/文献综述模板.md / 研究现状模板.md 死链；**(4)** references 重命名（方案 B：8 个文件）——文体指南 + 排版加 `-guide` 后缀（apaquarto/narrative-review/meta-analysis/observational-study/experimental-study），PRISMA 改名 `prisma-workflow.md`，3 个 checklist 改 `-standards.md`；**(5)** SKILL.md description 精简（13 行 → 3 行）+ 触发场景独立章节；**(6)** 核心原则 1 由废弃的 `index.json` 改为 `wiki↔Zotero↔WebDAV 三联动`；**(7)** 指南导航表头 13 → 18、模块数 6 → 7 统一；**(8)** synthesize / summarize 输出命名 `<id>` → `<slug>`；**(9)** module-maintain.md + manuscript-audit-standards.md 删 hooks/ SOP 引用（改为直接调 WikiZoteroManager 类方法）；**(10)** SKILL.md 数据流图删 `index.json` 残留。**7-agent peer review SOP 删除**（老板 2026-06-23 19:23 明确废弃）已在 v5.21.2 完成后处理。|
| **v6.0.3** | **2026-06-23** | **upload 模块上线**（download 反向对偶）：本地 PDF → Zotero 建条目 + WebDAV 推 + wiki source 创建；3 步流水线（`add_to_zotero` / `push_to_webdav` / `create_wiki_source`）；CLI `upload --pdf-path/--slug/--doi`；**严格遵循"工具不替代 agent"原则**：slug / title / tags 全部由 agent 传，工具只做幂等检查 + 最小可用 wiki source YAML（标注 PENDING + agent 待办清单）；**v6.0.3 教训沉淀**：第一版替 agent 派生 slug 导致重复 wiki source，删错文件后改为 slug 必填 agent 传；新增 `references/module-upload.md`；README 工具清单 6→7 |
| **v6.0.7** | **2026-06-28** | **SciHub 整合到 download**（老板 04:08 指令）：原独立技能 `scihub-paper-downloader`（v1.0.3）合并到 `scripts/download/scihub.py` 的 `SciHubDownloader` 类，独立技能目录删除；CLI 新增 `--source {zotero,scihub}` 选项（默认 `zotero`）；`SciHubDownloader` 零外部依赖（纯 Python stdlib）+ ALTCHA 验证码自动解 + 6 镜像 fallback（`sci-hub.st/se/ru/ren/box/workflow`，**v6.0.7 后老板 05:16 指令配置写到 `config.json.scibhub.mirrors` 持久化**）+ 4 状态语义（FOUND / NOT_FOUND+OA_LINK / MIRROR_ERROR / INVALID_INPUT）；`wiki/raw/papers` 默认归档目录不变；`--source zotero` 行为完全不变（老板坚果云保护逻辑保留）；3 个 reference 文档（`SKILL.md` / `references/module-download.md` / `README.md` / `docs/ARCHITECTURE.md`）+ `psychologist/references/guides/paper-reading.md` 同步更新；**v6.0.7 末老板 05:16 指令**：`SCIHUB_MIRRORS` 写入 `config.json`（优先级链：config → env → hardcoded 兑底）；全失败时 `SciHubAllMirrorsFailedError` 异常携带 `mirrors_tried` + `last_errors` + `doi` 字段；CLI `cmd_download` 用 `isinstance` 捕获后返 `error_type: scihub_all_mirrors_failed` + 4 步 `suggestion` 结构化反馈 |
| **v6.0.2** | **2026-06-23** | **多模态精读工具能力上线**（重新定位：工具不攥写，只提供数据）：summarize 工具加 `--pdf-path` / `--ocr` 标志；内部集成 `pypdf`（文本提取）+ `pypdfium2`（渲染）+ `tesseract`（OCR）；返回结构化数据（页数 / 文件大小 / 每页文本 / 图片 OCR）；**明确边界：工具不调 LLM、不攥写笔记**——agent 拿数据后自己写 narrative；删 v6.0.2 越界的"agent 流程"章节（之前错把 agent 流程塞进工具文档，违反"工具不替代 agent"原则）|
| **v6.0.1** | **2026-06-23** | **Bug 修复**：drift detection 字段名纠正（`doi:` → `zotero_doi:`）+ 学术型判定加 `zotero_item_key` 兜底（兼容 arXiv 论文）；加 **非学术型豁免逻辑**（系统笔记 / 工具笔记 / 网页分享不再误报为"缺 zotero_item_key"）；`generate_drift_graph` / `check_drift` / `find_missing_zotero_keys` / `generate_drift_report` 全加 `non_academic` 类别；**修复后老板 wiki 后端真实健康度**：🟢 7/7 学术型三方同步 + 📂 7/14 非学术型豁免 |
| **v6.0.0** | **2026-06-23** | **(1)** 重写 README：以老板拍板的 7 项功能为骨架，跟 v5.21.2 SKILL.md 对齐（wiki-zotero-webdav 三方联动）；**(2)** **drift-graph 三方联动可视化**上线（`python3 scripts/main.py maintain drift-graph [--full]`），light 模式秒级 / full 模式 1-5 分钟；输出 ASCII 状态图 + 漂移统计 + 修复建议；首次跑发现老板 wiki 后端 14 source 中 7 个缺 zotero_item_key（50% 漂移，后证实是误报）；**(3)** SKILL.md description 补齐 2 项：apaquarto 排版 + drift-graph 状态图；**(4)** 教学课件生成缺口移除（老板明确"不管"）|
| v5.21.2 | 2026-06-22 | （仅 SKILL.md）：删除 hooks/ 整目录，description 重写为只描述 wiki-zotero-webdav 实际运作流程 |
| v5.21.0 | 2026-06-22 | （仅 SKILL.md）：增补 9 项参考文档（PRISMA / 同行评议 / 引用核验 / 原创性核验 / 终稿审计等）|
| v5.20.0 | 2026-06-22 | 所有模块走 wiki 后端（不再用 index.json / knowledge/）|
| v5.11.0 | 2026-06-21 | references 重构为 13 个文件（1 索引 + 1 工作流 + 1 排版 + 6 模块 + 4 文体）|
| v5.0.0 | 2026-05-09 | 重构为研究助手，聚焦知识库管理，拆分项目整理为 lab-organizer |
| 4.0.0 | 2026-05-06 | 重构为 v3.1.0 混合结构 |
| 3.0.0 | 2026-04-22 | 重构为统一项目管理技能，整合五大模块 |
| 2.1.0 | 2026-04-15 | 面向对象重构知识库管理，拆分为四个独立子模块 |
| 2.0.0 | 2026-04-14 | 重构为三个独立类：Searcher、Summarizer、Manager |
| 1.0.0 | 2026-04-08 | 初始版本 |

---

*最后更新：2026-06-23*
*作者：杨权*
*维护者：research-assistant 技能组*