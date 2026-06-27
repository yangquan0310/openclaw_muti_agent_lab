# research-assistant 参考手册

> 科研文献综述全流程助手参考指南。**v5.16.0 起 6 模块走 wiki（v6.0.3+ 扩到 7 模块加 upload，老板 00:08 指令）**。

## 工作流（v5.16.0 统一为 wiki-zotero-webdav 三联动，v6.0.3 加 upload 阶段）

| 阶段 | 操作 | 工具 | 输出位置 |
|------|------|------|----------|
| 1. **检索** | `search` 命中 paper | `scripts/search/Searcher.py` + `ZoteroSearcher.py` | Zotero 库 + cache/index.json |
| 2. **下载** | PDF 拉取（双源）：默认 Zotero→WebDAV→wiki raw（论文须先在 Zotero 库）；可选 SciHub→wiki/raw/papers（绕过付费墙）| `scripts/download/Downloader.py` + `ZoteroJianguoyunDownloader.py` + `SciHubDownloader` | Zotero+WebDAV 或 `wiki/raw/papers` |
| 3. **维护** | wiki source ↔ Zotero 双向建立 | `scripts/maintain/WikiZoteroManager.py` | `wiki/sources/*.md` |
| 4. **总结** | paper 摘要提取 | `scripts/summarize/Summarizer.py` | `wiki/syntheses/<date>-summarize-*.md` |
| 5. **合成** | source extract 笔记 | `scripts/synthesize/Synthesizer.py` | `wiki/syntheses/<date>-extract-*.md` |
| 6. **管理** | merge / filter / stats | `scripts/manage/Manager.py` | `wiki/` 全集 |
| **v6.0.3+ 上传**（下载反向） | 本地 PDF → Zotero + WebDAV + wiki source | `scripts/upload/Uploader.py` | Zotero 库 + nutstore + `wiki/sources/*.md` |

**核心原则**（详见 `wiki/AGENTS.md` v4）：
- zotero 是文献元数据唯一权威
- webdav 是附件存储
- wiki 是笔记/人可读视图
- 一一对应铁律：1 Zotero item = 1 source 页（强制）

## 章节导航（18 文件，v6.0.4 重命名后：1 索引 + 1 工作流 + 1 排版 + 7 模块 + 4 文体 + 1 PRISMA SOP + 3 标准）

| 章节 | 文件 | 内容 |
|------|------|------|
| **工作流** | [research-workflow.md](research-workflow.md) | 五阶段流程原则 |
| **检索模块** | [module-search.md](module-search.md) | Searcher / ZoteroSearcher / ZoteroAdder（v5.15.0+） |
| **管理模块** | [module-manage.md](module-manage.md) | Manager（v5.16.0+ 走 wiki，按 zotero_item_key 去重） |
| **维护模块** | [module-maintain.md](module-maintain.md) | WikiZoteroManager（v6.0.6+ 单一入口，Maintainer.py 已删） |
| **总结模块** | [module-summarize.md](module-summarize.md) | Summarizer（v5.16.0+ 走 wiki，规则分类） |
| **合成模块** | [module-synthesize.md](module-synthesize.md) | Synthesizer（v5.16.0+ 走 wiki，extract notes） |
| **下载模块**（v6.0.7+ 双源）| [module-download.md](module-download.md) | Downloader + ZoteroJianguoyunDownloader + SciHubDownloader |
| **v6.0.3+ 上传模块**（下载反向） | [module-upload.md](module-upload.md) | Uploader（本地 PDF → Zotero + WebDAV + wiki source） |
| **排版（Quarto）** | [apaquarto-manuscript-guide.md](apaquarto-manuscript-guide.md) | 范式 ④ apaquarto 严格 APA 7 |
| **文体指南** | [narrative-review-guide.md](narrative-review-guide.md) | 叙事综述（心理学 APA 7 + JARS-Quant） |
| | [meta-analysis-guide.md](meta-analysis-guide.md) | 元分析 |
| | [observational-study-guide.md](observational-study-guide.md) | 观察性研究 |
| | [experimental-study-guide.md](experimental-study-guide.md) | 实验研究 |
| **v5.21.0 新增：写作严谨** | [prisma-workflow.md](prisma-workflow.md) | PRISMA 系统综述 SOP（ARS Deep Research 思路） |

| **v5.21.0 新增：质量核验** | [apa7-standards.md](apa7-standards.md) | APA 7 引用核验 50 项 |
| | [originality-standards.md](originality-standards.md) | 原创性核验 30 项（5 类抄袭） |
| | [manuscript-audit-standards.md](manuscript-audit-standards.md) | 终稿完整性审计 60 项 |

## 按场景查找

### 工作流

| 场景 | 章节 |
|------|------|
| 不知道 5 阶段流程 | [research-workflow.md](research-workflow.md) |
| 想把项目知识迁移到 wiki | [module-manage.md](module-manage.md) + `wiki/AGENTS.md` v4 |
| 想看 skill 整体健康 | `python3 scripts/manage/Manager.py stats` |

### 各模块用法

| 场景 | 章节 |
|------|------|
| 怎么搜 paper 并 add 到 Zotero | [module-search.md](module-search.md) |
| 怎么管理 wiki source/synthesis/concept 列表 | [module-manage.md](module-manage.md) |
| 怎么批量补 wiki source 的 zotero_item_key | [module-maintain.md](module-maintain.md) |
| 怎么对 paper 做总结 | [module-summarize.md](module-summarize.md) |
| 怎么从 source 提取结构化笔记 | [module-synthesize.md](module-synthesize.md) |
| 怎么把 paper PDF 同步到坚果云 | [module-download.md](module-download.md) |
| **怎么把本地 PDF 反向上传到 Zotero + WebDAV + wiki source（v6.0.3+）** | **[module-upload.md](module-upload.md)** |

### 撰写

| 场景 | 章节 |
|------|------|
| 写叙事综述 | [narrative-review-guide.md](narrative-review-guide.md) |
| 写元分析 | [meta-analysis-guide.md](meta-analysis-guide.md) |
| 写观察性研究 | [observational-study-guide.md](observational-study-guide.md) |
| 写实验研究 | [experimental-study-guide.md](experimental-study-guide.md) |
| APA 7 排版（Quarto 范式 ④） | [apaquarto-manuscript-guide.md](apaquarto-manuscript-guide.md) |
| **写 PRISMA 系统综述** | [prisma-workflow.md](prisma-workflow.md) |

| **投稿前核验 APA 7 引用** | [apa7-standards.md](apa7-standards.md) |
| **核验原创性** | [originality-standards.md](originality-standards.md) |
| **终稿完整性审计** | [manuscript-audit-standards.md](manuscript-audit-standards.md) |



> ⚠️ **v5.21.2 已删除 hooks/ 整目录**（老板 14:29 明确不需要 hooks）  
> 原 11 个 markdown SOP 全部删除，相关操作直接走 WikiZoteroManager 类方法

## workboard tracker

`v5-roadmap` 看板：
- v5.14.0 ✅ 完成（删旧类 + 拆 dashboard）
- v5.15.0 ✅ 完成（5/5：main 模块 + Al-Kari + SOP + search 骨架）
- v5.16.0 ✅ 完成（5/5：3 模块接入 wiki + 端到端 demo）
- v5.17.0 ✅ 文档同步
- v5.18.0 ✅ 6 项目 knowledge/ 迁移
- v5.19.0 ✅ WikiSearchReport + _resolve_env bug 修复
- v5.20.0 ✅ SKILL.md 精简 + 版本历史移末尾
- v5.21.0 ✅ 增补 9 项参考文档（SOP 级）
- **v5.21.2 ✅ 删除 hooks/ 整目录 + SKILL.md description 修正（只描述 wiki-zotero-webdav 实际流程）**
- **v6.0.0 ✅ README 重写（老板拍板 7 项功能）+ drift-graph 三方联动可视化**
- **v6.0.1 ✅ drift detection bug 修复（`doi:` → `zotero_doi:` 字段名纠正 + 学术型豁免逻辑）**
- **v6.0.2 ✅ summarize 多模态精读工具能力上线（pypdf + pypdfium2 + tesseract，工具不攥写 narrative）**
- **v6.0.7 ✅ SciHub 整合到 download**（`--source scihub` → SciHubDownloader；零依赖 + ALTCHA 验证码 + 6 镜像 fallback；下载到 `wiki/raw/papers` 不动老板坚果云；原独立技能 `scihub-paper-downloader` 已合并删除）
- **v6.0.3 ✅ upload 模块上线（download 反向对偶：本地 PDF → Zotero + WebDAV + wiki source；slug 必填 agent 传）**
