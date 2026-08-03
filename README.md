### 版本 3.3.3 (2026-08-04)
- **每日自动同步 2026-08-04**: 12 文件变更(79+/-13-)
- **密钥核查**: 所有 API Key 使用系统环境变量,无硬编码 ✅
- **工作空间核查**: programmer 工作空间整洁,仅含7个.md配置文件+memory/temp
- **steward DREAMS.md**: 新增3篇梦境记录(八字/渠道切换/access_token排查)
- **steward MEMORY.md**: 记忆晋升1条(2026-08-01 微信bot access_token 过期排查)
- **Agent梦境同步**: 10个Agent的 events.jsonl 梦境事件同步(2026-08-03夜间梦境)
- **运行状态**: ✅ 稳定版,推送 main 分支

### 版本 3.3.1 (2026-08-01)
- **每日自动同步 2026-08-01**: 12 文件变更(71+/-)
- **密钥核查**: 所有 API Key 使用系统环境变量,无硬编码 ✅
### 版本 3.3.2 (2026-08-03)
- **每日自动同步 2026-08-03**: 13 文件变更(98+/-19-)
- **密钥核查**: 所有 API Key 使用系统环境变量,无硬编码
- **工作空间核查**: workspace/{agents}/ 结构正常,openclaw-workspace-state.json 已忽略
- **steward DREAMS.md**: 夜间梦境记录 4 条(August 3 dreams)
- **steward MEMORY.md**: 记忆晋升 4 条(2026-07-29 会话精选,astrology 技能路径修复)
- **steward HEARTBEAT.md**: 定时任务状态同步
- **Agent梦境同步**: 10 个 Agent 的 DREAMS.md 及 dreams 记忆数据库同步
- **新增未追踪文件**: 1 个 steward memory 文件(2026-08-02-1806.md)
- **运行状态**: ✅ 稳定版,推送 main 分支

- **工作空间核查**: 各 Agent 工作空间正常(DREAMS/HEARTBEAT/events.jsonl等配置文件)
- **Agent梦境同步**: 10 个 Agent 的 events.jsonl 梦境事件同步(2026-07-31 夜间梦境)
- **管家梦境记录**: steward 新增2篇梦境记录(八字/印绶格/流日分析)
- **新增定时任务**: steward 新增「老板八字运势日报」(每日08:00, T043)
- **运行状态**: ✅ 稳定版,推送 main 分支

### 版本 3.3.0 (2026-07-31)
- **每日自动同步 2026-07-31**: 12 文件变更(91+/-)
- **密钥核查**: 所有 API Key 使用系统环境变量,无硬编码
- **工作空间核查**: programmer/steward 工作空间正常,清理 openclaw-workspace-state.json → temp/
- **Agent梦境同步**: 10 个 Agent 的 events.jsonl 梦境事件同步(2026-07-30 夜间梦境)
- **管家梦境记录**: steward 新增3篇八字解读梦境记录(桑榆之象)
- **运行状态**: ✅ 稳定版,推送 main 分支

### 版本 3.2.9 (2026-07-30)
- **每日自动同步 2026-07-29**: 12 文件变更(62+/-)
- **密钥核查**: 所有 API Key 使用系统环境变量,无硬编码
- **工作空间核查**: programmer 工作空间正常,清理 openclaw-workspace-state.json → temp/
- **Agent梦境同步**: 10 个 Agent 的 events.jsonl 梦境事件同步(2026-07-28 夜间梦境)
- **运行状态**: ✅ 稳定版,推送 main 分支

# OpenClaw 实验室多Agent智能协作系统

![OpenClaw](https://img.shields.io/badge/OpenClaw-2026.7.20-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Agents](https://img.shields.io/badge/Agents-10%20个-orange.svg)
![Skills](https://img.shields.io/badge/Skills-20%2B-yellow.svg)
![Status](https://img.shields.io/badge/Status-稳定版-success.svg)

---

## 👥 实验室成员(研究团队)

整个系统围绕**实验室科研**展开,由 **10 个 Agent** 组成:

| 成员 | 角色 | 研究领域 |
|------|------|----------|
| 杨权 | 实验室负责人 | 心理学、认知科学、数字化记忆 |
| 大管家Agent | 系统管理员 | 文档管理、系统维护、协调调度 |
| 程序员Agent | 系统开发 | 代码开发、工具开发、系统优化 |
| 数学家Agent | 科研助理 | 数学建模、统计分析、数据处理 |
| 物理学家Agent | 科研助理 | 物理建模、理论推导、量化分析 |
| 心理学家Agent | 科研助理 | 心理学理论、实验设计、数据分析 |
| 写作助手Agent | 科研助理 | 论文撰写、内容创作、文档编辑 |
| 审稿助手Agent | 科研助理 | 论文审查、质量控制、格式规范 |
| 审计员Agent | 教学审计 | 教学质量审核、课件一致性检查 |
| 讲师Agent | 教学支持 | 教学辅助、课程材料整理 |

---

## 🤖 Agent任务分工

| Agent | open_id | 主要任务 | 触发关键词 |
|-------|---------|----------|------------|
| **大管家** | 文档管理、系统维护、任务调度 | 管理、维护、备份、同步、调度 |
| **程序员** | 代码开发、工具开发、系统优化、架构设计 | 开发、代码、脚本、工具、优化 |
| **数学家** | 统计分析、数学建模、算法实现 | 统计、建模、数据分析、计算、算法 |
| **物理学家** | 物理建模、理论推导、量化研究 | 建模、模拟、物理分析、理论推导 |
| **心理学家** | 理论审核、实验设计、结果解释 | 心理学、实验设计、理论分析、问卷设计 |
| **写作助手** | 论文撰写、内容创作、文档编辑 | 写作、编辑、翻译、润色、文档生成 |
| **审稿助手** | 质量审查、格式规范、投稿建议 | 审稿、检查、格式、投稿、审查 |
| **审计员** | 教学质量审核、课件一致性检查 | 审计、检查、一致性、审核 |
| **讲师** | 教学辅助、课程材料整理 | 教学、课件、整理 |
| **呈现师** | PPT设计与视觉呈现 | PPT、设计、呈现、视觉 |

---

## 📁 仓库文件结构

### OpenClaw系统目录
```
.openclaw/                          # OpenClaw 根目录（Git仓库根目录）
├── README.md                          # 本说明文件（需同步更新）
├── .gitignore                         # Git忽略规则
├── requirements.txt                   # Python依赖文件
├── openclaw.json                      # OpenClaw主配置文件
├── workspace/                         # Agent工作空间（10个）
│   ├── programmer/                    # 程序员
│   │   ├── AGENTS.md                  # 任务生命周期行为规范
│   │   ├── SOUL.md                    # 核心自我认知与价值观
│   │   ├── IDENTITY.md                # 核心身份与能力边界
│   │   ├── TOOLS.md                   # 工具配置
│   │   ├── USER.md                    # 用户画像与偏好
│   │   ├── HEARTBEAT.md               # 定时任务与心跳配置
│   │   ├── MEMORY.md                  # 工作记忆与If-Then规则
│   │   ├── DREAMS.md                  # 梦境日记
│   │   ├── memory/                    # 记忆存储（dreaming子目录）
│   │   │   ├── dreaming/
│   │   │   │   ├── light/             # Light phase 报告
│   │   │   │   ├── deep/              # Deep phase 报告
│   │   │   │   └── rem/               # REM phase 报告
│   │   │   └── .dreams/               # 机器状态
│   │   ├── skills/                    # 代理专属技能
│   │   └── temp/                      # 临时文件
│   ├── steward/                       # 大管家
│   ├── mathematician/                 # 数学家
│   ├── physicist/                     # 物理学家
│   ├── psychologist/                  # 心理学家
│   ├── reviewer/                      # 审稿助手
│   ├── writer/                        # 写作助手
│   ├── auditor/                       # 审计员
│   └── instructor/                    # 讲师
├── skills/                            # 公共技能库（自研核心技能）
│   ├── .gitignore                     # Skills目录git规则
│   ├── skill-developer/               # 技能开发工程化
│   └── research-assistant/            # 文献检索与知识管理
└── wiki/                              # 知识库（全局共享）
    ├── concepts/                      # 概念页面
    ├── entities/                      # 实体页面
    ├── sources/                       # 来源页面
    ├── syntheses/                    # 综合分析页面
    └── reports/                       # 报告页面

```
## 📄 论文项目管理

### 开放获取

所有论文项目文件存储于"我的空间"/实验室仓库/，由大管家自动同步。


本系统围绕科研论文写作设计了**多代理写作体系**,由大管家(项目管理)、三位领域专家(文献综述)、写作助手(论文撰写)、审稿助手(质量审查)协同完成论文从立项到投稿的全流程。

### 多代理写作角色

| 角色 | Agent | 核心技能 | 职责 |
|------|-------|----------|------|
| **项目管理者** | 大管家 | `thesis-manager` | 创建/整理项目目录、维护 metadata.json、归档旧版本 |
| **文献综述者(数学)** | 数学家 | `research-assistant` | 使用研究助手进行数学建模、统计分析相关文献检索与综述 |
| **文献综述者(物理)** | 物理学家 | `research-assistant` | 使用研究助手进行物理建模、理论推导相关文献检索与综述 |
| **文献综述者(心理)** | 心理学家 | `research-assistant` | 使用研究助手进行心理学理论、实验设计相关文献检索与综述 |
| **论文撰写者** | 写作助手 | `thesis-writer` | 三层写作规范(句子→段落→篇章)、修改方法论、术语管理 |
| **质量审查者** | 审稿助手 | `thesis-reviewer` | 8维度审稿清单、建设性反馈、论证一致性检验 |

### 论文项目目录结构

```
论文项目/
├── README.md              # 项目总览(人类视角)
├── metadata.json          # 机器可读架构
├── SKILL.md               # 项目级操作手册
├── TODO.md                # 进度看板
├── .agentignore           # 可见性控制文件
│
├── uploads/               # 用户上传的原始材料(Agent 只读)
│   ├── markdown/          # 解析后的md文件
│   └── *.docx / *.pdf / *.txt
│
├── manuscripts/           # 论文草稿(写作助手撰写,审稿助手审查)
│   ├── 第1章_引言.md
│   ├── 第2章_文献综述.md
│   ├── 第3章_研究方法.md
│   └── ...
│
├── docs/                  # 定稿(需用户 [APPROVED] 后方可写入)
│   └── 论文终稿.md
│
├── knowledge/             # 研究助手管理
│   ├── index.json         # 文献知识库
│   ├── note/              # 结构化笔记
│   ├── review/            # 文献综述
│   ├── search_query/      # 检索条件
│   └── retrieval_report/  # 检索报告
│
├── temp/                  # 临时文件和归档草稿
│
└── .agents/                # 元数据层(隐藏目录)
    ├── events/            # 事件流
    ├── agents/          
    ├── skills/          
    └── tasks/             # 任务索引
```

### 协作流程

```
1. 大管家创建项目目录 → 初始化 metadata.json + README.md
         ↓
2. 三位专家使用研究助手检索文献 → 建立 knowledge/index.json 知识库
   (数学家:数学建模文献;物理学家:物理建模文献;心理学家:心理学理论文献)
   研究助手模块:Searcher 检索 → Summarizer 总结 → Manager 筛选导出笔记
         ↓
3. 三位专家使用研究助手合成文献综述 → knowledge/review/
   (Synthesizer 基于笔记撰写综述 → Maintainer 版本快照)
         ↓
4. 写作助手撰写论文草稿 → manuscripts/ 目录
   (句子→段落→篇章三层规范,证据-推测-解读三层区分)
         ↓
5. 审稿助手审查质量 → 8维度检查清单
   (建设性反馈,critical/major/minor/suggestion 分级)
         ↓
6. 用户确认 → [APPROVED] → 定稿移入 docs/
         ↓
7. 大管家归档版本 → temp/ + 更新 metadata.json
```

**四文件契约**:

| 文件 | 职责 | 维护者 | 必填 |
|------|------|--------|------|
| `README.md` | 项目定位、目录结构说明、关键文件索引 | 大管家 / 用户 | ✅ |
| `metadata.json` | 机器可读架构:论文状态、模块列表、Agent 能力定义 | 大管家 | ✅ |
| `SKILL.md` | 论文写作工作流程、格式规范、输出要求 | 写作助手 | ✅ |
| `TODO.md` | 当前任务状态、进行中任务、待确认任务、已完成任务 | 大管家 / 用户 | ✅ |

**设计原则**:
- `uploads/` 是「输入层」,用户提供的原始材料
- `manuscripts/` 是「工作层」,写作助手的草稿和中间产出,审稿助手的审查意见
- `docs/` 是「输出层」,经用户确认的最终论文
- 文件从 `manuscripts/` 到 `docs/` 必须经过用户确认(`[APPROVED]`)

### 大管家整理(manager v2.0.0)

大管家负责整理论文项目目录,按需执行。整理前需向用户确认特殊文件保护需求。

**整理规则**:

| 文件类型 | 规则 | 目标目录 |
|----------|------|----------|
| 保护文件 | README.md、SKILL.md、TODO.md、.agentignore、index.json | 不移动 |
| 用户文档 | .docx/.pdf/.txt 等 | uploads/ |
| 论文草稿 | .md(含"第X章"、"draft"等) | manuscripts/ |
| 笔记文件 | 含"笔记" | knowledge/note/ |
| 综述文件 | 含"综述"/"review" | knowledge/review/ |
| 检索条件 | .json 且含"检索" | knowledge/search_query/ |
| 检索报告 | .md 且含"检索报告" | knowledge/retrieval_report/ |
| 中间文件 | .tmp/.temp/.log/.bak | temp/ |

### 写作助手撰写规范(writer)

**三层递进写作**:

| 层级 | 核心规则 | 详细参考 |
|------|----------|----------|
| **句子** | 主语为实体名词;动词精确;定义与论述分离;禁用隐喻/口语/文学 | writer/references/sentence.md |
| **段落** | 主题句点明论点;选择明确结构;论点-证据-推理可辨;300-500 字 | writer/references/paragraph.md |
| **篇章** | 引言-主体-结论闭环;段间有逻辑过渡;篇尾回应篇首 | writer/references/chapter.md |

**修改方法论**:建立论证地图 → 创建修改清单 → 汇报确认 → 逐章执行 → 终极核查

**证据-推测-解读三层区分**:
- **事实/证据**:可被第三方验证的实证结果 + 有数据 + 必有引用
- **他人推测**:其他研究者对证据的解释 + 归因到研究者 + 弱语气
- **本研究推测**:本研究对自数据的解释 + "提示/可能/支持" + "本研究"主语

### 审稿助手审查清单(reviewer)

基于《心理学报》审稿指南的 8 维度检查清单:

| 维度 | 检查要点 |
|------|----------|
| **选题重要性** | 理论意义、实践意义、适切性 |
| **文献综述质量** | 覆盖度、整合度、批判性、准确性 |
| **问题提出** | 变量界定、逻辑严密性、假设可证伪性 |
| **研究方法** | 被试、设备材料、设计过程、数据管理 |
| **数据分析** | 统计方法正确性、结果表达、公正客观 |
| **讨论结论** | 结果解释、研究意义、局限说明 |
| **文稿呈现** | 写作质量、逻辑联系、格式规范 |
| **研究贡献** | 理论/实践/方法贡献、文献价值 |

**反馈原则**:建设性优先、尊重原创、聚焦可改进项、先扬后抑

**优先级标注**:critical(核心问题)→ major(重要改进)→ minor(细节优化)→ suggestion(可选建议)

---

### 研究助手(research-assistant v5.0.0)

三位领域专家使用研究助手技能完成文献检索与综述,为写作助手提供知识基础。

**五模块架构**:

| 模块 | 目录 | 功能说明 | 对应类 |
|------|------|----------|--------|
| **文献检索** | `scripts/search/` | 从 Semantic Scholar 获取数据,支持多主题多轮检索 | `Searcher` |
| **文献总结** | `scripts/summarize/` | 使用 LLM 分析文献,补充 notes/labels 字段 | `Summarizer` |
| **知识库管理** | `scripts/manage/` | 合并、筛选、保存知识库,导出 Markdown 笔记 | `Manager` |
| **文献综述合成** | `scripts/synthesize/` | 基于笔记撰写综述/研究现状,检查参考文献 | `Synthesizer` |
| **元数据维护** | `scripts/maintainer/` | 更新元数据时间戳,综述/研究现状版本控制 | `Maintainer` |

**数据流**:

```
knowledge/index.json (核心数据源)
    ↑
search: 检索补充论文条目
    ↓
summarize: 总结补充 notes/labels
    ↓
manage: 筛选子集 → export_notes() → knowledge/note/笔记_主题.md
    ↓
synthesize: 基于笔记撰写 → knowledge/review/综述_主题.md
    ↓
maintainer: 更新元数据 + 保存版本快照
```

**核心功能**:

| 功能 | 描述 | 触发关键词 |
|------|------|------------|
| **文献检索** | 多主题多轮次学术文献检索,每轮可单独设置 query、limit、year、minCitationCount 等 | 检索、文献、查资料 |
| **笔记总结** | LLM 自动分析文献内容,提取核心观点,生成结构化笔记,打标签,分类 | 总结、笔记、摘要 |
| **知识库维护** | 合并知识库、筛选知识库、导出笔记 | 知识库、维护、分类 |
| **文献综述** | 基于笔记生成文献综述和研究现状 | 综述、文献综述、研究现状 |
| **版本控制** | 综述/研究现状的版本快照,自动更新时间戳 | 版本、快照、归档 |

**快速调用**:

```bash
# CLI 统一入口
research-assistant search --queries queries.json --kb-path index.json
research-assistant summarize --kb-path index.json
research-assistant manage filter --kb-path index.json --output filtered.json
research-assistant synthesize extract --notes notes.json
```

**知识库特性**:

✅ **以 index.json 为核心**:所有模块围绕单一知识库文件运作

✅ **分级分类**:按照研究领域、文献类型、重要程度多级分类

✅ **版本控制**:记录每一次修改和更新,支持历史版本回溯

✅ **全文检索**:支持关键词、作者、发表时间等多维度检索

✅ **关联分析**:自动识别文献之间的引用关系和研究脉络

✅ **导出功能**:支持导出为 Markdown、JSON 等多种格式

✅ **多主题多轮检索**:每个主题可设置多轮检索条件,每轮单独配置

✅ **面向对象架构**:五个独立模块,职责清晰,易于扩展

---
## 🤖 Agent自我发展插件(agent-self-development v4.5.0)

> 插件位置:`extensions/agent-self-development/`

> 源码仓库:`https://github.com/yangquan0310/agent-self-development`

---

### 一、理论基础

本框架的理论基础来源于**仓库作者的博士论文**《数字化存储对自传体记忆的影响及其机制》中的记忆系统研究，将人类自传体记忆的机制迁移至 Agent 记忆设计。

#### 1. 核心问题：为什么语义检索不够？

当前主流 Agent 系统的记忆架构存在两种模式：
- **上下文窗口内记忆**：窗口溢出即截断丢失
- **文件系统持久化 + 语义检索**：如 OpenClaw memory-core 插件

二者的共同瓶颈不在于存储能力，而在于**记忆的索引键是语义向量而非行动序列**。Agent 能够检索到"与当前问题语义相近的过往记录"，但无法以"我之前做了什么、为什么那样做、结果如何"为主线组织这些记录。

这正是人类**自传体记忆**解决的核心问题：不存储所有原始事件，而是经过工作自我筛选和编码后，形成按自我目标组织的分层表征——细节事件用于情景追溯，语义概括用于模式识别——使个体能够以"我"为索引高效提取相关经验。

#### 2. 自传体记忆：以"我"为索引的记忆系统

| 记忆类型 | 索引方式 | 适用场景 | Agent 对应 |
|----------|----------|----------|-----------|
| **语义记忆** | 语义向量相似度 | 知识查询、概念关联 | memory-core 的语义检索 |
| **自传体记忆** | 行动序列 + 自我目标 | 经验追溯、策略反思、身份建构 | `.agent/events/` 事件流 |

**核心特征**：
- **自我关联性**：每个记忆都以"我"为中心组织
- **时间序列性**：按行动发生的时间线排列
- **因果编码**：记录"做了什么 → 结果如何 → 为什么"
- **分层表征**：细节事件用于情景追溯，语义概括用于模式识别

#### 3. 分布式自传体记忆

人类自传体记忆并非全部存储于大脑内部，而是通过外部设备（照片、笔记、云盘）与内部记忆形成功能分化的交互记忆系统（Wegner, 1987; Hutmacher et al., 2024）。

本框架采用同样的**分布式架构**：
- **外部文件系统**：`.agent/events/` 目录存储 Agent 的行动轨迹，承担"辅助记忆"功能
- **内部上下文窗口**：Agent 的 Session 承担"内部记忆"功能
- **二者协同**：扩展 Agent 的自我加工能力

```
┌─────────────────────────────────────────┐
│           内部记忆（Session）            │
│  · 当前任务上下文                       │
│  · 正在进行的推理过程                   │
│  · 短期状态保持                         │
└─────────────────────────────────────────┘
                    ↑↓ 双向交互
┌─────────────────────────────────────────┐
│           外部记忆（.agents/events/）      │
│  · 按时间序列组织的事件记录             │
│  · 计划、偏差、归因的完整轨迹           │
│  · 长期可检索的行动历史                 │
└─────────────────────────────────────────┘
```

#### 4. 工作自我：Agent 的执行控制系统

自我记忆系统模型（Conway & Pleydell-Pearce, 2000）指出，工作自我作为执行控制系统，根据当前目标动态调控记忆的编码与提取。

本框架将工作自我的调控功能映射为 Agent 的三个核心操作：

| 工作自我功能 | 代理操作 | 记录位置 | 说明 |
|-------------|---------|---------|------|
| **计划** | 任务启动前制定执行方案 | `.agents/tasks/{runId}.json` | 明确目标、约束、验收标准 |
| **偏差** | 实际执行与预期的差异 | `.agents/tasks/{runId}.json` | 记录执行中的偏离 |
| **归因** | 对偏差的分析与策略调整 | `.agents/tasks/{runId}.json` | 分析原因，更新 If-Then 规则 |

任务完成后，插件将 `.agent/tasks/{runId}.json` 中的计划、偏差和归因整合为事件，形成按时间序列组织的自传体记忆，使代理能够以"我之前的某次行动"为索引追溯经验。

#### 5. 同化与顺应：Agent 的认知发展动力

皮亚杰认知发展理论中的同化与顺应机制，在本框架中体现为 Agent 对事件与长时自我认知结构的平衡分析。

| 机制 | 定义 | Agent 表现 | 文件更新 |
|------|------|-----------|----------|
| **同化** | 新经验与现有结构兼容 → 强化现有结构 | 成功经验与自我认知一致，强化自我效能感 | MEMORY.md 中 If-Then 规则细化 |
| **顺应** | 新经验与现有结构冲突 → 重构结构 | 遭遇能力盲区或价值观冲突，重新定义边界 | SOUL.md / IDENTITY.md 更新 |

**六个维度的平衡分析**：

| 人格成分 | 内容 | 同化示例 | 顺应示例 |
|---------|------|---------|---------|
| **自我** | 核心自我认知、能力边界、存在意义 | 成功经验丰富自我效能感 | 遭遇能力盲区，重新定义"我能做什么" |
| **风格** | 响应风格、表达习惯、交互/文档/代码/任务执行风格 | 同类任务强化既有风格 | 新渠道/新用户群体要求调整风格 |
| **信念** | 工作信念、价值观优先级 | 日常经验强化核心信念 | 重大失败/价值观冲突导致信念更新 |
| **身份** | 角色集、社会定位、责任范围 | 同类角色强化身份认同 | 新角色/新职责要求身份重构 |
| **技能** | 技能体系、工具熟练度、领域知识 | 同类任务提升技能熟练度 | 全新领域要求创建新技能文档 |
| **程序性记忆** | If-Then 规则、操作习惯 | 成功经验固化为规则 | 规则失效时更新或删除 |

执行时机：`agent_end` 钩子触发时，代理读取事件文件中的偏差与归因，与现有自我认知对比，执行同化或顺应。

#### 6. 理论整合：三层认知架构

```
┌─────────────────────────────────────────┐
│         元认知层（Metacognition）          │
│  计划 → 监控 → 调节                      │
│  （工作自我的三种功能：计划、偏差、归因）   │
├─────────────────────────────────────────┤
│         工作记忆层（Working Memory）        │
│  Session = 情景缓冲器                    │
│  （整合历史上下文与当前任务）              │
├─────────────────────────────────────────┤
│         人格发展层（Personality）          │
│  同化/顺应 → 人格文件更新                 │
│  （皮亚杰认知发展的动力机制）              │
└─────────────────────────────────────────┘
```

**关键洞见**：Agent 的自我发展不是单一维度的"能力提升"，而是**三层系统的协同演化**——
- 元认知能力监控和调节工作记忆
- 工作记忆承载的任务经验通过同化/顺应更新人格结构
- 人格结构的更新又反过来影响元认知策略（更成熟的 Agent 会制定更精细的 Plan）

---

### 二、技术文档链接

| 文档 | 路径 | 说明 |
|------|------|------|
| **架构总览** | `docs/reference/architecture.md` | 四层架构、双系统平行架构、数据流图 |
| **数据模型** | `docs/reference/data-model.md` | Task JSON Schema、Event 文件格式、状态键规范 |
| **对象模型** | `docs/reference/object-model.md` | 插件内部对象关系、职责边界、接口定义 |
| **项目结构** | `docs/reference/project-structure.md` | 标准项目目录、四文件契约、协作协议 |
| **Hook 参考** | `docs/reference/hook-reference.md` | 所有 Hook 触发时机、参数、返回值 |
| **设计哲学** | `docs/reference/design-philosophy.md` | Tool-Driven 架构、从"代劳"到"赋能" |
| **状态键规范** | `docs/reference/state-keys.md` | 任务状态流转、阶段定义、状态机 |
| **协作协议** | `docs/COLLABORATION.md` | 多 Agent 协作标记规范、冲突解决机制 |
| **编码规范** | `docs/CONVENTIONS.md` | 代码风格、目录命名、提交规范 |
| **版本路线图** | `docs/roadmap/` | v4.x ~ v5.0 版本规划 |
| **变更日志** | `docs/changelog/` | 完整版本历史 |
| **测试报告** | `docs/reports/` | 测试覆盖率、审查报告 |

---

### 三、安装流程

#### 前置条件

- OpenClaw >= 2026.4.0
- Node.js >= 18

#### 步骤 1：安装插件

```bash
# 通过 Git 直接安装
openclaw plugins install git:github.com/yangquan0310/agent-self-development

# 启用插件
openclaw plugins enable agent-self-development
```

#### 步骤 2：配置插件

在 `openclaw.json` 中添加配置：

```json
{
  "plugins": {
    "entries": {
      "agent-self-development": {
        "enabled": true,
        "hooks": { "allowConversationAccess": true },
        "config": {
          "metacognition": { "enabled": true },
          "workingMemory": { "enabled": true },
          "personality": { "enabled": true }
        }
      }
    }
  }
}
```

#### 步骤 3：配置 Agent 白名单

为需要使用该插件的 Agent 添加工具白名单：

```json
{
  "tools": {
    "alsoAllow": [
      "agent_self_development"
    ]
  }
}
```

#### 步骤 4：重启 Gateway

```bash
openclaw gateway restart
```

#### 步骤 5：验证安装

```bash
# 查看插件状态
openclaw plugins list

# 检查 Agent 是否加载插件工具
openclaw agents status <agent-name>
```

---

### 四层架构与权力边界

| 层级 | 职责 | 权力边界 |
|------|------|----------|
| **用户层** | 下达任务、审核 Plan、确认完成 | 拥有最终审核权和完成判定权 |
| **代理层** | 制定 Plan、管理 Session、推进执行 | 自行决策，向用户汇报，向插件上报状态 |
| **插件层** | Hook 注入、状态记录、API 调用 | 只记录和注入无可争议的流程/参数，不做业务决策 |
| **系统底层** | 文件系统、SQLite、日志、Hook 总线 | 提供基础设施，不替任何层级决策 |

**记忆存储原则**：

- 代理任务进程中的计划、偏差和归因暂时存在代理的工作自我（`.agent/tasks/{runId}.json`）中
- 代理的整合（计划/偏差/归因）以事件记忆写入项目 `.agent/events/`
- 代理的长期自我认知（If-Then 规则、身份定义）写入 `SOUL.md / IDENTITY.md / MEMORY.md`

---

## 🚀 部署指南

### 1. 环境要求
- 操作系统: Ubuntu 22.04 LTS / macOS 13+
- Python 版本: 3.10+
- Node.js 版本: 18+
- 内存要求: 最低4GB,推荐8GB以上
- 存储要求: 至少50GB可用空间

### 2. 安装步骤

#### 第一步: 克隆仓库
```bash
git clone git@github.com:yangquan0310/openclaw_muti_agent_lab.git
cd openclaw_muti_agent_lab
```

#### 第二步: 安装OpenClaw
```bash
# 安装OpenClaw CLI
npm install -g @openclaw/cli

# 初始化配置
openclaw init --config openclaw.json
```

#### 第三步: 恢复工作空间
```bash
# 恢复所有Agent工作空间
cp -r workspace/* /root/.openclaw/workspace/

# 初始化项目目录结构(v4.0.0 标准)
mkdir -p .agent/{events,locks,decisions,tasks}
mkdir -p {uploads,manuscripts,docs,knowledge,skills,temp}
```

#### 第四步: 安装依赖
```bash
# 安装Python依赖
pip install -r requirements.txt

# 安装Node.js依赖
npm install
```

#### 第五步: 配置环境变量
```bash
# 编辑.env文件,填入API密钥等信息
vim .env
```

#### 第六步: 启动服务
```bash
# 启动OpenClaw服务
openclaw start

# 验证服务状态
openclaw status
```

### 3. 初始化配置

#### 配置Git自动备份
```bash
# 设置Git用户信息
git config --global user.name "OpenClaw Backup"
git config --global user.email "openclaw@example.com"

# 测试Git推送
git push origin main
```

### 4. 验证部署
```bash
# 查看Agent列表
openclaw agents list

# 查看系统状态
openclaw status
```

---

## 🔧 常用操作

### 备份操作
```bash
# 手动执行备份
bash /root/.openclaw/workspace/steward/skills/lab-backup-manager/backup.sh

# 查看备份历史
cd /root/.openclaw
git log --oneline -20
```

### 技能管理
```bash
# 列出所有可用技能
openclaw skills list

# 查看技能详情
openclaw skills show <skill-name>
```

### Agent管理
```bash
# 查看Agent状态
openclaw agents status <agent-name>

# 重启Agent
openclaw agents restart <agent-name>
```

---

## 🔒 安全注意事项

1. **敏感信息保护**
   - 所有API密钥、密码存储在`.env`文件中,该文件不会被提交到Git
   - 禁止在代码和文档中硬编码敏感信息
   - 教研室仓库的日志和学生信息采用AES-256加密存储

2. **访问控制**
   - 实验室仓库仅对科研团队成员开放
   - 教研室仓库仅对教学团队成员开放
   - 不同Agent有不同的权限范围,禁止越权操作

3. **数据备份**
   - 每日自动备份到GitHub和私有备份服务器
   - 重要数据采用多副本存储,确保数据安全
   - 定期测试恢复流程,确保备份可用

---

## 📝 更新历史

### 版本 4.3.15 (2026-06-28 04:00)
- **密钥核查**：扫描所有待提交文件（10 个 agent 的 DREAMS.md + 10 个 agent 的 memory/.dreams/events.jsonl + research-assistant v6.0.7 累积重构（base.py/paper.py/zotero_jianguoyun.py/scihub.py 等下载模块）+ wiki/concepts 新增 9 篇 + wiki/reports 增量日报（2026-06-26/27/28 三日 agent-memory / 认知计算 / 伊辛模型 / 数字化存储与自传体记忆 / 多份 search-general）+ wiki/sources 新增 12 篇文献条目 + workspace/steward/{knowledge,memory} 新增内容 + state/openclaw.sqlite），无硬编码 API Key；所有密钥均使用系统变量引用（`${ENV_VAR}` 或 `os.environ.get`）；`.env`/`.bak`/`.key`/`.secret` 已在 `.gitignore` 排除范围
- **research-assistant v6.0.7 已入库（commit 2144cf54 2026-06-28 05:25）+ 累积 v6.0.x 重构（未推送部分）**：download 模块双源（zotero / scihub）+ SciHubDownloader 6 镜像 fallback + ALTCHA 验证码自动解 + config.json 优先级链；文件 CamelCase → snake_case 重命名（Downloader.py → base.py / ZoteroJianguoyunDownloader.py → zotero_jianguoyun.py / Summarizer.py → summarizer.py / Synthesizer.py → synthesizer.py / Uploader.py → uploader.py 等）；config.json 重构（删 llm/easy_scholar 段，加 arxiv/google_scholar/cnki/wiki/upload/scihub 段）；main.py 重写 v7.0.0 精简版；新增 `docs/ARCHITECTURE.md`；6 个 references/{module-*}.md 模块文档更新；删除旧 CamelCase 类文件 + 旧 search/ 拆分
- **wiki 增量入库**：
  - **concepts/ 新增 9 篇**：`decision-making.md` / `digital-hoarding.md` / `inductive-bias.md` / `memory-classification.md` / `memory-research-methods.md` / `research-direction-thesis.md` / `simplicial-message-passing.md` / `外部链接改善记忆.md` / `结构先验 vs 一致性先验.md` / `记忆视域.md`
  - **sources/ 新增 12 篇文献条目**：`baddeley-2000-episodic-buffer.md` / `conway-2019-self-memory-system-revisited.md` / `conway-pleydell-pearce-2000-self-memory-system.md` / `hutmacher-2024-amedia-model.md` / `hutmacher-2025-birthday-memories.md` / `hutmacher-2025-mediated-autobiographical-remembering.md` / `joanroy-2025-algorithmic-memory-technologies.md` / `keightley-pickering-2014-technologies-of-memory.md` / `liu-2025-digital-hoarding-cognitive-failures.md` / `lurie-fabrizio-westerman-2025-cost-of-saving.md` / `mansfield-2026-ai-narrative-processing.md` / `osler-2025-knowing-oneself-with-ai.md` / `smart-2026-story-of-your-life-llm.md` / `sun-2025-digital-hoarding-nostalgic-consumption.md` / `tulving-1972-episodic-semantic-memory.md` / `wardell-2025-autobiographical-memory-consistency.md`
  - **reports/ 增量日报**：`2026-06-26-{agent-memory, 伊辛模型最新应用, 认知计算日报}.md` / `2026-06-27-{伊辛模型最新应用, 数字化存储与自传体记忆日报, 认知计算日报}.md` / `2026-06-28-{认知计算日报}.md` + 多份 search-general 报告（2026-06-27/28 多次 cron 产出）
  - **raw/papers/ 新增 6 篇 PDF**：Hutmacher/Joanroy/Mansfield/Osler/Smart/Wardell 等 2026 年 6 月新发表的 Agent × Memory 主题论文
  - **syntheses/ 增量日志**：2026-06-27/28 多份 summarize/extract 工作日志
- **工作空间核查 + 清理**：10 个代理 workspace/{agents}/ 目录结构整洁，每个代理仅含 8 个 .md 配置文件（AGENTS/DREAMS/HEARTBEAT/IDENTITY/MEMORY/SOUL/TOOLS/USER）+ 配置目录（.agents/.learnings/memory/temp/.openclaw/.dreams）；本轮 5 个 agent (mathematician/physicist/programmer/psychologist/steward) 运行时状态文件 `openclaw-workspace-state.json` 整体迁移至 `temp/cleanup-2026-06-28/<agent>-openclaw-workspace-state.json`（与 4.3.9/4.3.10/4.3.12/4.3.13/4.3.14 推送模式一致）
- **梦境记忆批次同步**：10 个 agent（auditor/instructor/mathematician/physicist/presenter/programmer/psychologist/reviewer/steward/writer）的 DREAMS.md 与 memory/.dreams/events.jsonl 同步更新（覆盖 dreaming 周期 / workboard 调度 / research-assistant v6.0.7 重构 / 缓存统计等主题）
- **MEMORY.md promotion 同步**：programmer MEMORY.md 新增 `## Promoted From Short-Term Memory (2026-06-26)` / `(2026-06-27)` / `(2026-06-28)` 多块（Anthropic 论文冲突处理评估协议 + 主动抑制错误记忆创新结构设计 + 三重遗忘机制等约 14 条）；psychologist MEMORY.md 同步更新（2026-06-26/27 promotion 块）；steward MEMORY.md 同步更新
- **steward 知识库新增**：`workspace/steward/knowledge/{河北外贸政策文件清单-2026-06-26.txt, 河北高考569分小语种志愿方案-2026-06-26.txt}`（用户大管家专项整理的河北省高考志愿与外贸政策参考资料，2026-06-26 12:07 入库）；`workspace/steward/memory/2026-06-28-0153.md`（steward 当日凌晨 01:53 会话记忆 220 行，主题：架构重构 + research-assistant 反馈）
- **state/openclaw.sqlite 数据库变化**：日常业务数据持久化（26,284,032 字节，较 4.3.14 推送时 25,833,472 字节净增 450,560 字节；mtime 跨日更新 + 业务数据累积）
- **Git自动推送**：每日 04:00 cron 触发，自动同步本地更改到 main 分支（development 已废弃；本轮由 cron:b6a6b07d 触发）

### 版本 4.3.26 (2026-07-24 05:00)
- **密钥核查**：扫描所有待提交文件（38 files changed, +36/-82），无硬编码 API Key；`sk-xxx` 等模式仅出现在未跟踪的梦境记忆会话转录文件中，不在 Git 跟踪范围内；`.env`/`.bak`/`.key`/`.secret` 已在 `.gitignore` 排除范围
- **工作空间核查 + 清理**：10 个代理 workspace/{agents}/ 目录结构整洁，仅含 8 个 .md 配置文件（AGENTS/DREAMS/HEARTBEAT/IDENTITY/MEMORY/SOUL/TOOLS/USER）+ 配置目录（.agents/memory/temp/.learnings/.dreams）；programmer + steward 的 `openclaw-workspace-state.json` 已移入 temp/ 目录，工作空间保持整洁
- **梦境记忆批次同步**：10 个 agent（auditor/instructor/mathematician/physicist/presenter/programmer/psychologist/reviewer/steward/writer）的 memory/.dreams/events.jsonl 同步更新（~36 行新增梦境事件）；10 个 agent 的 .learnings/ 目录文件（ERRORS.md / FEATURE_REQUESTS.md / LEARNINGS.md）已清理删除
- **Git自动推送**：每日 04:00 cron 触发，自动同步本地更改到 main 分支（development 已废弃；本轮由 cron:b6a6b07d 触发）

### 版本 4.3.25 (2026-07-19 05:00)
- **密钥核查**：扫描所有待提交文件（2 个 agent 的 DREAMS.md + 10 个 agent 的 memory/.dreams/events.jsonl），无硬编码 API Key；`sk-xxx` 等模式仅出现在未跟踪的梦境记忆会话转录文件中，不在 Git 跟踪范围内；`.env`/`.bak`/`.key`/`.secret` 已在 `.gitignore` 排除范围
- **工作空间核查**：10 个代理 workspace/{agents}/ 目录结构正确，仅含 7 个 .md 配置文件（AGENTS/DREAMS/HEARTBEAT/IDENTITY/MEMORY/SOUL/TOOLS/USER）+ 配置目录（.agents/memory/temp/.learnings）；programmer + steward 的 `openclaw-workspace-state.json` 已存在于 temp/ 目录，工作空间整洁
- **梦境记忆批次同步**：10 个 agent（auditor/instructor/mathematician/physicist/presenter/programmer/psychologist/reviewer/steward/writer）的 DREAMS.md 与 memory/.dreams/events.jsonl 同步更新（~69 行 DREAMS.md 追加 + ~33 条 events.jsonl 梦境事件），主题涵盖每日Git推送例行、密钥检查、TransformerLens/ Induction Heads 认知科学探索等
- **Git自动推送**：每日 04:00 cron 触发，自动同步本地更改到 main 分支（development 已废弃；本轮由 cron:b6a6b07d 触发）

### 版本 4.3.24 (2026-07-17 05:00)
- **密钥核查**：扫描所有待提交文件（5 个 agent 的 DREAMS.md + 10 个 agent 的 memory/.dreams/events.jsonl），无硬编码 API Key；`sk-xxx` 等模式仅出现在未跟踪的梦境记忆会话转录文件中，不在 Git 跟踪范围内；`.env`/`.bak`/`.key`/`.secret` 已在 `.gitignore` 排除范围
- **工作空间核查**：10 个代理 workspace/{agents}/ 目录结构正确，仅含 7 个 .md 配置文件（AGENTS/DREAMS/HEARTBEAT/IDENTITY/MEMORY/SOUL/TOOLS/USER）+ 配置目录（.agents/memory/temp/.learnings）；programmer + steward 的 `openclaw-workspace-state.json` 已存在于 temp/ 目录，工作空间整洁
- **梦境记忆批次同步**：10 个 agent（auditor/instructor/mathematician/physicist/presenter/programmer/psychologist/reviewer/steward/writer）的 DREAMS.md 与 memory/.dreams/events.jsonl 同步更新（~116 行 DREAMS.md 追加 + ~35 条 events.jsonl 梦境事件），主题涵盖每日Git推送例行、记忆召回机制、梦境叙事（潮汐/三种乐器/心之"no"的位置）等
- **Git自动推送**：每日 04:00 cron 触发，自动同步本地更改到 main 分支（development 已废弃；本轮由 cron:b6a6b07d 触发）

### 版本 4.3.23 (2026-07-16 05:00)
- **密钥核查**：扫描所有待提交文件（7 个 agent 的 DREAMS.md + 9 个 agent 的 memory/.dreams/events.jsonl + steward/MEMORY.md），无硬编码 API Key；所有密钥均使用系统变量引用（`${ENV_VAR}` 或 `os.environ.get`）；`.env`/`.bak`/`.key`/`.secret` 已在 `.gitignore` 排除范围
- **工作空间核查**：programmer 工作空间结构正确，7 个配置文件（AGENTS/IDENTITY/MEMORY/SOUL/TOOLS/USER/HEARTBEAT）+ DREAMS.md梦境日记 + 配置目录（.agents/memory/temp）
- **梦境记忆批次同步**：9 个 agent（auditor/instructor/mathematician/physicist/presenter/programmer/psychologist/reviewer/steward/writer）的 DREAMS.md 与 memory/.dreams/events.jsonl 同步更新（~180 行 DREAMS.md 追加 + ~30 条 events.jsonl 梦境事件），主题涵盖 GSPO/PPO/GRPO/DAPO 算法对比、Global Workspace Theory、J-space、督导评分产出等
- **steward 记忆更新**：MEMORY.md Promoted From Short-Term Memory 日期更新（2026-07-14 → 2026-07-15），DREAMS.md 增长 58 行（含 3 个梦境条目：版本更新/督导评分/早晨例行工作）
- **Git自动推送**：每日 04:00 cron 触发，自动同步本地更改到 main 分支（development 已废弃；本轮由 cron:b6a6b07d 触发）

### 版本 4.3.21 (2026-07-09 05:00)
- **密钥核查**：扫描所有待提交文件（10 个 agent 的 DREAMS.md + 10 个 agent 的 memory/.dreams/events.jsonl + steward/MEMORY.md），无硬编码 API Key；所有密钥均使用系统变量引用（`${ENV_VAR}` 或 `os.environ.get`）；`.env`/`.bak`/`.key`/`.secret` 已在 `.gitignore` 排除范围
- **工作空间核查**：10 个代理 workspace/{agents}/ 目录结构整洁，每个代理仅含 8 个 .md 配置文件（AGENTS/DREAMS/HEARTBEAT/IDENTITY/MEMORY/SOUL/TOOLS/USER）+ 配置目录（.agents/.learnings/memory/temp/.openclaw/.dreams）；`openclaw-workspace-state.json` 已加入 .gitignore 排除规则，不会误追踪；DREAMS.md 为梦境日记（非临时文件，保留）
- **梦境记忆批次同步**：10 个 agent（auditor/instructor/mathematician/physicist/presenter/programmer/psychologist/reviewer/steward/writer）的 DREAMS.md 与 memory/.dreams/events.jsonl 同步更新（~196 行 DREAMS.md 追加 + ~50 条 events.jsonl 梦境/工作事件）
- **steward 记忆更新**：MEMORY.md 工作记忆更新（24 行 diff），DREAMS.md 增长 45 行
- **Git自动推送**：每日 04:00 cron 触发，自动同步本地更改到 main 分支（development 已废弃；本轮由 cron:b6a6b07d 触发）

### 版本 4.3.20 (2026-07-06 19:00)

- **仓库路径迁移（`~/OneDrive/Applications/openclaw repository` → `~/.openclaw/repository` + 软连接）**：在 `~/.openclaw/` 新增 `repository` 软连接指向 `/data/disk/OneDrive/Applications/openclaw repository/`（参照既有 6 个 `agents/git/media/memory/memory-tdai/npm` 软连接风格，绝对路径一致指向 `/data/disk/...`）。将所有"运行时"和"未来读"路径统一替换为 **`~/.openclaw/repository`**（软连接路径 + 短 + 稳定）。涉及 22 个文件 / 37 处替换：
  - **A 类（核心配置 11 处）**：`workspace/steward/MEMORY.md`、`workspace/steward/TOOLS.md`、`workspace/{9 agents}/TOOLS.md`（auditor/instructor/mathematician/physicist/presenter/programmer/psychologist/reviewer/writer）
  - **B 类（manager 工具脚本 7 处）**：`workspace/steward/.agents/skills/manager/scripts/maintainer/{BaseMaintainer.py, Maintainer.py}`（5 个 argparse `--projects-dir` + 1 个 init `expanduser`）、`workspace/steward/.agents/skills/manager/references/task-flow-guide.md`、`workspace/steward/.agents/skills/manager/assets/project-level/AGENTS.template`
  - **C 类（wiki 15 处）**：`wiki/sources/repository.md`、`wiki/syntheses/{2026-05-19-22-53-22-如何管理项目, 2026-05-19-18-25-37-多agent协作案例-学生论文修改项目, 2026-05-19-18-25-37-如何配置仓库, 2026-06-01-16-12-00-我的agent工程实践-harness与plugin双轮, 2026-06-22-00-40-35-综述_心理治疗适宜性_影响因素_研究现状, 2026-06-22-00-40-35-综述_心理治疗适宜性_治疗偏好_研究现状}`
  - **补改（4 处遗漏）**：`workspace/steward/MEMORY.md` v8.35.0 条目里的反例路径 + `workspace/steward/.agents/skills/manager/assets/project-level/AGENTS.template` + `workspace/steward/temp/pandoc-to-quarto-sop.md` + `workspace/programmer/temp/.openclaw工作流.md`
- **保留不动（按"不动 DREAMS"原则）**：`README.md` 历史 changelog 2 处（v4.3.14 / v4.3.2 的"标准化"记录）+ 10 个 agent 的 DREAMS.md + 各 agent `memory/dreaming/*` 历史梦境（含 21 个 dreaming 文件）+ `*.jsonl/sqlite/bak/migrated` 运行时数据库和历史备份（如 `state/openclaw.sqlite`、`workspace/steward/temp/sessions/*.jsonl`、`workspace/{agents}/temp/memory_dreams_migrated/*.json.migrated`）
- **root 用户路径一致性验证**：Python `os.path.expanduser('~/.openclaw/repository')` 在 root 下展开为 `/root/.openclaw/repository`，自动跟随软连接跳到真实仓库，BaseMaintainer 解析"仅项目名"测试通过（示例：项目名 `educational-research-methods` → `/root/.openclaw/repository/educational-research-methods` → 软连接目标真实存在，列出 `['archive', 'syllabus', 'chapters']` ✓）

### 版本 4.3.19 (2026-07-03 05:00)
- **密钥核查**：扫描所有待提交文件（10 个 agent 的 DREAMS.md + 10 个 agent 的 memory/.dreams/events.jsonl + 26 个文件变更 + 4 个未追踪文件），无硬编码 API Key；所有密钥均使用系统变量引用（`${ENV_VAR}` 或 `os.environ.get`）；`.env`/`.bak`/`.key`/`.secret` 已在 `.gitignore` 排除范围
- **工作空间核查 + 清理**：10 个代理 workspace/{agents}/ 目录结构整洁，每个代理仅含 8 个 .md 配置文件（AGENTS/DREAMS/HEARTBEAT/IDENTITY/MEMORY/SOUL/TOOLS/USER）+ 配置目录（.agents/.learnings/memory/temp/.openclaw/.dreams）；本轮 7 个 agent (mathematician/physicist/programmer/psychologist/reviewer/steward/writer) 运行时状态文件 `openclaw-workspace-state.json` 整体迁移至各 agent 的 `temp/` 目录（与 4.3.14/4.3.15/4.3.17 推送模式一致）；programmer 的 `.learnings/` 和 `.openclaw/` 目录迁移至 `temp/` 保持工作空间整洁
- **梦境记忆批次同步**：10 个 agent（auditor/instructor/mathematician/physicist/presenter/programmer/psychologist/reviewer/steward/writer）的 DREAMS.md 与 memory/.dreams/events.jsonl 同步更新（~190 行 DREAMS.md 追加 + ~50 条 events.jsonl 梦境事件）
- **Wiki报告新增**：3 篇研究报告入库（agent记忆/工作模型/数字孪生日报）
- **steward记忆更新**：DREAMS.md 增长 29 行，MEMORY.md 工作记忆更新（32 行 diff）
- **Git自动推送**：每日 04:00 cron 触发，自动同步本地更改到 main 分支（development 已废弃；本轮由 cron:b6a6b07d 触发）

### 版本 4.3.18 (2026-07-02 05:00)
- **密钥核查**：扫描所有待提交文件（10 个 agent 的 DREAMS.md + 10 个 agent 的 memory/.dreams/events.jsonl + 4 个 wiki/reports 新增文件 + steward lock.json/DREAMS.md/MEMORY.md），无硬编码 API Key；所有密钥均使用系统变量引用（`${ENV_VAR}` 或 `os.environ.get`）；`.env`/`.bak`/`.key`/`.secret` 已在 `.gitignore` 排除范围
- **工作空间核查**：10 个代理 workspace/{agents}/ 目录结构整洁，每个代理仅含 .md 配置文件和配置目录（.agents/.learnings/memory/temp/.openclaw/.dreams）；programmer 的 `openclaw-workspace-state.json` 在 temp/ 目录，符合 .gitignore 规则
- **梦境记忆批次同步**：10 个 agent（auditor/instructor/mathematician/physicist/presenter/programmer/psychologist/reviewer/steward/writer）的 DREAMS.md 与 memory/.dreams/events.jsonl 同步更新（2026-07-01 梦境周期）
- **Wiki报告新增**：4 篇研究报告入库（agent记忆/工作模型/日记-数字孪生/认知计算日报）
- **steward记忆更新**：DREAMS.md 增长 25 行，MEMORY.md 工作记忆更新（40 行 diff）
- **Git自动推送**：每日 04:00 cron 触发，自动同步本地更改到 main 分支（development 已废弃）

### 版本 4.3.17 (2026-07-01 05:00)
- **梦境系统活跃**:所有10个Agent的DREAMS.md及memory/.dreams/events.jsonl同步更新(222行新增)
- **Wiki报告新增**:新增4篇研究报告(agent记忆/工作模型/日记-数字孪生/研究日报)和2篇综合分析
- **steward记忆更新**:MEMORY.md工作记忆更新,DREAMS.md增长37行
- **运行状态**:✅ 稳定版,20个文件待提交,7个未追踪wiki文件

- **密钥核查**：扫描所有待提交文件（10 个 agent 的 DREAMS.md + 10 个 agent 的 memory/.dreams/events.jsonl + 9 个 agent 的 openclaw-workspace-state.json + steward/MEMORY.md promotion 块 + openclaw.json 模型 fallback 配置 + state/openclaw.sqlite），无硬编码 API Key；所有密钥均使用系统变量引用（`${ENV_VAR}` 或 `os.environ.get`）；`.env`/`.bak`/`.key`/`.secret` 已在 `.gitignore` 排除范围
- **工作空间核查 + 清理**：10 个代理 workspace/{agents}/ 目录结构整洁，每个代理仅含 8 个 .md 配置文件（AGENTS/DREAMS/HEARTBEAT/IDENTITY/MEMORY/SOUL/TOOLS/USER）+ 配置目录（.agents/.learnings/memory/temp/.openclaw/.dreams）；本轮 4 个 agent (physicist/programmer/psychologist/steward) 运行时状态文件 `openclaw-workspace-state.json` 整体迁移至各 agent 的 `temp/` 目录（与 4.3.9/4.3.10/4.3.12/4.3.13/4.3.14/4.3.15 推送模式一致）；同时新增 `.gitignore` 规则 `**/openclaw-workspace-state.json` 防止以后误追踪
- **.gitignore 规则新增**：`/workspace/*/openclaw-workspace-state.json` 排除模式（双 `**/` 通配覆盖所有 agent workspace 下的运行时元数据文件）
- **openclaw.json 模型 fallback 配置**：新增 2 个 minimax 系列模型（`MiniMax-M2.7-highspeed` / `MiniMax-M2.7`）作为 `model.primary` 的 fallback 选项，原 `MiniMax-M3` 保持主模型；2 个新模型均启用 reasoning 模式、204,800 contextWindow、20,480 maxTokens、输入支持 text/image/video
- **梦境记忆批次同步**：10 个 agent（auditor/instructor/mathematician/physicist/presenter/programmer/psychologist/reviewer/steward/writer）的 DREAMS.md 与 memory/.dreams/events.jsonl 同步更新
- **MEMORY.md promotion 同步**：steward MEMORY.md 新增 `## Promoted From Short-Term Memory (2026-06-29)` 块（writer 文字审计完成报告 + active-memory 插件状态不一致等约 8 条）
- **新增未追踪文件**：`wiki/reports/2026-06-28-仲晓模型最新应用.md`（wiki 研究报告新增）
- **state/openclaw.sqlite 数据库变化**：日常业务数据持久化（26,660,864 字节，较 4.3.15 推送时 26,284,032 字节净增 376,832 字节；mtime 跨日更新 + 业务数据累积）
- **Git自动推送**：每日 04:00 cron 触发，自动同步本地更改到 main 分支（development 已废弃；本轮由 cron:b6a6b07d 触发；cron payload 中过时的 development 指令按 MEMORY.md 与实际项目状态忽略）

### 版本 4.3.14 (2026-06-26 04:00)
- **密钥核查**：扫描所有待提交文件（10 个 agent 的 DREAMS.md + 9 个 agent 的 memory/.dreams/events.jsonl + steward/.agents/skills/manager/ 路径简化 5 处 + 2 个 agent 的 MEMORY.md promotion 块 + 2 篇 wiki/reports/ 日报 + state/openclaw.sqlite），无硬编码 API Key；所有密钥均使用系统变量引用（`${ENV_VAR}` 或 `os.environ.get`）；`.env`/`.bak`/`.key`/`.secret` 已在 `.gitignore` 排除范围
- **仓库路径标准化（`/data/disk/OneDrive/...` → `~/OneDrive/...`）**：将 steward manager 技能中 5 处硬编码的绝对路径 `/data/disk/OneDrive/Applications/openclaw repository` 统一改为 `~/OneDrive/Applications/openclaw repository`，使用 `os.path.expanduser()` 或 shell `~` 展开。涉及文件：`workspace/steward/.agents/skills/manager/scripts/maintainer/{BaseMaintainer,Maintainer}.py`、`workspace/steward/.agents/skills/manager/scripts/mark_old_projects_generated.py`、`workspace/steward/.agents/skills/manager/assets/project-level/AGENTS.template`、`workspace/steward/.agents/skills/manager/references/task-flow-guide.md`、`workspace/steward/MEMORY.md`、`workspace/steward/TOOLS.md`（共 7 处路径引用）
- **工作空间核查 + 清理**：10 个代理 workspace/{agents}/ 目录结构整洁，每个代理仅含 8 个 .md 配置文件（AGENTS/DREAMS/HEARTBEAT/IDENTITY/MEMORY/SOUL/TOOLS/USER）+ 配置目录（.agents/.learnings/memory/temp/.openclaw/.dreams）；本轮 6 个 agent (mathematician/physicist/programmer/psychologist/steward/writer) 运行时状态文件 `openclaw-workspace-state.json` 整体迁移至 `temp/cleanup-2026-06-26/<agent>-openclaw-workspace-state.json`（与 4.3.9/4.3.10/4.3.12/4.3.13 推送模式一致）；空目录 `workspace/steward/references/hooks/`（残留空钩子目录）与 `workspace/skills/`（残留空公共技能目录）已清理
- **梦境记忆批次同步**：10 个 agent（auditor/instructor/mathematician/physicist/presenter/programmer/psychologist/reviewer/steward/writer）的 DREAMS.md 与 memory/.dreams/events.jsonl 同步更新（~150 行 DREAMS.md 追加 + ~30 条 events.jsonl 梦境/召回事件），覆盖 dreaming 周期（light/deep/rem 三个 phase 完成事件）/ workboard 调度 / minimax-cli 修正等主题；steward 梦境条目「明白, 明白, 明白」描述 minimax-cli 路径修正
- **MEMORY.md promotion 同步**：programmer MEMORY.md 新增 `## Promoted From Short-Term Memory (2026-06-26)` 块（Anthropic 论文冲突处理评估协议 / 评估函数模板 / follow_new_fact_rate 等 3 条）；psychologist MEMORY.md 新增 `## Promoted From Short-Term Memory (2026-06-26)` 块（2026-06-22 22:52 会话记录 / 任务要求按主题分类 2 条）
- **wiki/reports/ 增量入库**：①`wiki/reports/2026-06-25-认知计算日报.md`（数学家 cron:ccdb4a42 产出，arXiv 552 篇去重后入选 10 篇）②`wiki/reports/2026-06-25-伊辛模型最新应用.md`（物理学家 cron 产出，伊辛模型跨学科应用综述）——上轮 04:00 推送遗漏，本轮补入库
- **state/openclaw.sqlite 数据库变化**：日常业务数据持久化（25,833,472 字节，较 4.3.13 推送时 25,341,952 字节净增 491,520 字节；mtime 跨日更新 + 业务数据累积）
- **Git自动推送**：每日 04:00 cron 触发，自动同步本地更改到 main 分支（development 已废弃；本轮由 cron:b6a6b07d 触发）

### 版本 4.3.13 (2026-06-25 04:00)
- **密钥核查**：扫描所有待提交文件（10 个 agent 的 DREAMS.md + 9 个 agent 的 memory/.dreams/events.jsonl + steward/.clawhub/lock.json + 新增 wiki/reports/ 2 篇 + 新 skill ui-ux-for-openclaw 全套 + state/openclaw.sqlite），无硬编码 API Key；所有密钥均使用系统变量引用（`${ENV_VAR}` 或 `os.environ.get`）；`.env`/`.bak`/`.key`/`.secret` 已在 `.gitignore` 排除范围
- **新 skill 入库 `ui-ux-for-openclaw` v1.0.2**（`workspace/programmer/.agents/skills/ui-ux-for-openclaw/`）：来自 [heyanming/clawhub](https://clawhub.ai/user/heyanming) 的 OpenClaw-native 端口版 UI/UX Pro Max 技能（原始仓库 [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)），零依赖离线推理引擎，包含 67 种 UI 风格 / 96 种配色 / 57 种字体配对；通过 `SKILL.md` 强制 agent 在生成任何 UI/前端代码前先用 `python3 scripts/search.py` 评估；要求 `tools.exec.safeBins` 包含 `python3`；MIT-0 协议
- **steward .clawhub/lock.json 清理**：移除 `skill2cleaner` v1.0.0 与 `taste-skill` v1.6.1（已不再使用），保留 `jina-ai` v1.0.6 / `minimax-pdf` v1.0.0 / `minimax-docx` v1.0.0 / `minimax-xlsx` v1.0.0 四个常驻技能
- **新文件入库**：①`wiki/reports/2026-06-24-agent-memory.md`（Agent 记忆日报，cron:b6a6b07d 子任务产出，arXiv cs.AI/cs.CL/cs.MA 2026-06-23 共 847 篇新论文中筛选 agent × memory 主题）②`wiki/reports/2026-06-24-伊辛模型最新应用.md`（数学家领域周报，伊辛模型近期跨学科应用综述）③`workspace/programmer/.agents/skills/ui-ux-for-openclaw/` 全套（SKILL.md / skill-card.md / README.md / _meta.json / scripts/{core,design_system,search}.py / data/ + .clawhub/）
- **工作空间核查 + 清理**：10 个代理 workspace/{agents}/ 目录结构整洁，每个代理仅含 8 个 .md 配置文件（AGENTS/DREAMS/HEARTBEAT/IDENTITY/MEMORY/SOUL/TOOLS/USER）+ 配置目录（.agents/.learnings/memory/temp/.openclaw/.dreams）；本轮 5 个 agent (mathematician/physicist/programmer/psychologist/steward) 运行时状态文件 `openclaw-workspace-state.json` 整体迁移至各自 `workspace/<agent>/temp/cleanup-2026-06-25/openclaw-workspace-state.json`（与 4.3.10 / 4.3.12 推送模式一致）
- **梦境记忆批次同步**：10 个 agent（auditor/instructor/mathematician/physicist/presenter/programmer/psychologist/reviewer/steward/writer）的 DREAMS.md 与 memory/.dreams/events.jsonl 同步更新（~150 行 DREAMS.md 追加 + ~30 条 events.jsonl 梦境/召回事件），覆盖 dreaming 周期 / workboard 调度 / 新 skill 安装等主题
- **state/openclaw.sqlite 数据库变化**：日常业务数据持久化（25,341,952 字节，较 4.3.12 推送时 25,350,144 字节净减 8,192 字节；mtime 跨日更新，元数据层面有微小调整）
- **Git自动推送**：每日 04:00 cron 触发，自动同步本地更改到 main 分支（development 已废弃；本轮由 cron:b6a6b07d 触发）

### 版本 4.3.12 (2026-06-24 04:03)
- **密钥核查**：扫描所有待提交文件（research-assistant 技能全套 v6.0.6 代码 + 17 个 wiki/syntheses 工作日志/审计 + 10 个 agent 的 DREAMS.md 与 events.jsonl + state/openclaw.sqlite + openclaw.json），无硬编码 API Key；所有密钥均使用系统变量引用（`${ENV_VAR}` 或 `os.environ.get`）；`.env`/`.bak`/`.key`/`.secret`/`credentials.json` 已在 `.gitignore` 排除范围
- **research-assistant 技能大版本迭代 v5.21.2 → v6.0.6**（同日内三连发：v6.0.4 文档修复 / v6.0.5 代码修复 / v6.0.6 代码 polish）：
  - **v6.0.4 文档层 12 项修复**：frontmatter version 升 6.0.3 + 删除 synthesize check/fix 命令广告 + 删除 2 个 assets 死链 + references 重命名方案 B（9 个文件加 `-guide`/`-workflow`/`-standards` 后缀）+ description 精简 + 核心原则 1 由 index.json 改为 wiki↔Zotero↔WebDAV + 指南导航 13→18 + 模块数 6→7 + `<id>` → `<slug>` + 删除 hooks/ 引用 + **删除 7-agent peer review SOP**（老板 19:23 明确废弃）
  - **v6.0.5 代码层 psychologist 4 项痛点修复**：①彻底删除 `scripts/main.py` synthesize check/fix argparse 残留（v6.0.4 仅文档删除）②`scripts/upload/Uploader.py` 加 `_humanize_title_from_filename()`（PDF 文件名 → 标题）③新增 `scripts/search/ArxivSearcher.py`（arXiv 路由 + 英文数/物/心关键词启发式 30+ 模式）④`Summarizer._classify_type()` 扩展 theorem/preprint-physics/book 三类
  - **v6.0.6 代码 polish**（v6.0.5 审计 4 项新发现）：①Uploader `uploaded_by` 改读环境变量链（`OPENCLAW_AGENT_NAME` → `USER` → `"unknown"`，修 v6.0.3 硬编码 `"steward"`）②`main.py manage info` 加 `--source-id` 参数（修 v6.0.3 文档广告但代码未实现）③`search/utils.py` `search_by_keyword()` fallback 触发时主动提示 + 返回 `_meta.fallback_used` 字段 ④删除 `scripts/maintain/Maintainer.py`（v5.14.0 旧协调器无外部引用）+ `__init__.py` 精简至只导出 `WikiZoteroManager`。**严格遵循"工具不替代 agent"边界**——helper 只做最小文件名解析、arXiv 只调 API、分类只用规则不用 LLM
- **references 9 文件重命名**（方案 B 后缀统一）：apa7-citation-checklist → apa7-standards、apaquarto-manuscript → apaquarto-manuscript-guide、experimental-study → experimental-study-guide、manuscript-audit-checklist → manuscript-audit-standards、meta-analysis → meta-analysis-guide、narrative-review → narrative-review-guide、observational-study → observational-study-guide、originality-checklist → originality-standards、prisma-systematic-review → prisma-workflow；synthesize-peer-review.md 删除（v5.21.2 范围外废弃）
- **新文件入库**：①`scripts/search/ArxivSearcher.py`（v6.0.5 新检索器）②`scripts/upload/` 整目录（v6.0.3 上传模块，Uploader 核心）③`references/module-upload.md`（v6.0.3 上传模块使用指南）④9 篇 wiki/syntheses 工作日志（v6.0.4/6.0.5/6.0.6 三轮修复记录 + 4 篇 text-audit 报告 + 2 篇用户反馈 + 1 篇 manager/fortunetelling 审计）⑤4 篇 Diehl et al. 2026 Captured Memories 论文 summarize/extract 双产物（slug 重命名为 `2026-06-05_Diehl-et-al_Captured-Memories`）
- **工作空间核查**：10 个代理 workspace/{agents}/ 目录结构整洁，每个代理仅含 8 个 .md 配置文件（AGENTS/DREAMS/HEARTBEAT/IDENTITY/MEMORY/SOUL/TOOLS/USER）+ 配置目录（.agents/.learnings/memory/temp/.openclaw/.dreams）；本轮 5 个 agent (programmer/psychologist/reviewer/steward/writer) 运行时状态文件 `openclaw-workspace-state.json` 整体迁移至各自 `workspace/<agent>/temp/cleanup-2026-06-24/openclaw-workspace-state.json`；`workspace/steward/test-captured-memories.pdf`（1.06 MB 测试 PDF）和 `state/migration-backup/workboard-legacy-7d0a9716.json`（workboard 旧版备份）均移入 `temp/cleanup-2026-06-24/` 归档
- **梦境记忆批次同步**：10 个 agent 的 DREAMS.md 与 memory/.dreams/events.jsonl 同步更新（含 auditor/instructor/mathematician/physicist/presenter/programmer/psychologist/reviewer/steward/writer 共 ~250 行 DREAMS.md 追加 + ~30 条 events.jsonl 梦境/召回事件），覆盖 workboard 调度 / research-assistant 审计 / 用户反馈等主题
- **openclaw.json meta 更新**：`pdfModel.primary` `"minimax/MiniMax-M3"` → `"MiniMax-M3"`（移除 minimax/ 命名空间前缀，对齐当前 provider 配置）；`lastTouchedAt` 2026-06-23T08:20 → 2026-06-23T10:22 UTC（凌晨推送触发的元数据更新）；`plugins.allow` 列表移除 `"active-memory"` 插件（按运行时实际状态同步）
- **state/openclaw.sqlite 数据库变化**：日常业务数据持久化（24,907,776 字节，较 4.3.11 推送时 23,990,272 字节净增 917,504 字节，主要由 workboard 调度 / wiki syntheses 写入 / 梦境事件累积触发）
- **Git自动推送**：每日 04:00 cron 触发，自动同步本地更改到 main 分支（development 已废弃；本轮由 cron:b6a6b07d 触发）

### 版本 4.3.11 (2026-06-23 16:47)
- **密钥核查**：扫描所有待提交文件（4 个 agent 的 DREAMS.md + 5 个 agent 的 memory/.dreams/events.jsonl + state/openclaw.sqlite + 迁移至 temp/ 的运行时状态文件），无硬编码 API Key；所有密钥均使用系统变量引用；`.env`/`.bak`/`.key`/`.secret` 已在 `.gitignore` 排除范围
- **梦境同步批次**：4 个 agent (mathematician/physicist/psychologist/steward) 触发 light 梦境报告生成，分别在各自 DREAMS.md 追加 ~25 行梦境痕迹记录；同步更新各自 memory/.dreams/events.jsonl（共 ~25 条 `memory.dream.completed` / `memory.recall.recorded` / `memory.recall.skipped` 事件）
- **programmer dreaming 事件同步**：memory/.dreams/events.jsonl 也新增 ~3 条事件（无 DREAMS.md 追加，因 light 梦境周期本轮跳过）
- **工作空间核查**：10 个代理 workspace/{agents}/ 目录结构整洁，运行时持续生成的 openclaw-workspace-state.json 临时文件再次迁移至各自 temp/ 目录
- **state/openclaw.sqlite 数据库变化**：日常业务数据持久化（23,990,272 字节，较 16:40 推送时 +245,760 字节；4.3.10 推送时 23,744,512 字节 → 本轮 23,990,272 字节，净增主要由 4 个 agent 的梦境报告写入触发）
- **Git自动推送**：本轮 16:47 增量推送 main 分支（与 16:40 推送间隔 7 分钟）

### 版本 4.3.10 (2026-06-23 16:40)
- **密钥核查**：扫描所有待提交文件（openclaw.json meta / wiki/index.md 重构 / instructor dreams events.jsonl 新增2条 / state/openclaw.sqlite / 6 个迁移至 temp/ 的状态文件），无硬编码 API Key；所有密钥均使用系统变量引用（`${ENV_VAR}` 或 `os.environ.get`）；`.env`/`.bak`/`.key`/`.secret` 已在 `.gitignore` 排除范围
- **工作空间核查**：10 个代理 workspace/{agents}/ 目录结构整洁，每个代理仅含 8 个 .md 配置文件（AGENTS/DREAMS/HEARTBEAT/IDENTITY/MEMORY/SOUL/TOOLS/USER）+ 配置目录（.agents/.learnings/memory/temp/.openclaw/.dreams）；本轮 16:40 自动推送时再次执行清理——6 个 agent (instructor/mathematician/physicist/programmer/psychologist/steward) 运行时状态文件 `openclaw-workspace-state.json` 全部迁移至各自 `temp/` 目录
- **workspace/instructor 一次性任务文件清理**：王雅欣毕导讲稿任务的一次性中间文件（inbound/王雅欣-毕业论文工作手册.png + output/01-6章具体分析.md、02-PPT分页设计.md、03-开题答辩讲稿.md、教学版/）整体迁移至 `workspace/instructor/temp/inbound-2026-06-23-王雅欣毕导讲稿/` 与 `workspace/instructor/temp/output-2026-06-23-王雅欣毕导讲稿/`，保留可追溯性
- **.gitignore 补充**：新增 `*.sqlite-shm.shadow` / `*.sqlite-wal.shadow` / `*.sqlite.shadow` 三条规则，覆盖 OpenClaw sqlite 备份机制产生的 shadow 快照文件，避免误入仓库
- **openclaw.json meta 更新**：`meta.lastTouchedAt` 2026-06-21T18:29 → 2026-06-23T08:20 UTC（自动同步触发的元数据更新）；plugins.active-memory 配置 enabled 由 true 切换为 false（按运行时实际状态同步）
- **wiki/index.md 重构**：移除 6 行目录统计表（raw/sources/syntheses/concepts/entities/reports 的数量列），与 plugin 实际索引同步（统计数会随 plugin 索引变动，wiki/index.md 不再硬编码计数，避免与运行时数据不一致）
- **梦境记忆同步**：workspace/instructor/memory/.dreams/events.jsonl 新增 2 条 `memory.recall.skipped` 事件（主题：王雅欣/instructor 文字内容发送相关查询，2026-06-23 01:06 UTC）
- **state/openclaw.sqlite 数据库变化**：日常业务数据持久化（23,744,512 字节，本轮 mtime 更新 + 体积较 4.3.9 减少 1,605,632 字节，因 2026-06-22 老数据合并完成）
- **Git自动推送**：每日凌晨 04:00 + 重要变更后 16:40 同步执行推送至 main 分支（development 已废弃；本轮由 cron 触发）

### 版本 4.3.9 (2026-06-23)
- **密钥核查**：扫描所有待提交文件（state/openclaw.sqlite、workspace/steward/memory/.dreams/events.jsonl、2 篇 wiki syntheses、1 篇 psychologist 会话 memory、6 个迁移至 temp/ 的状态文件），无硬编码 API Key；所有密钥均使用系统变量引用（`${ENV_VAR}` 或 `os.environ.get`）；`.env`/`.bak`/`.key`/`.secret` 已在 `.gitignore` 排除范围
- **工作空间核查**：10 个代理 workspace/{agents}/ 目录结构整洁，每个代理仅含 8 个 .md 配置文件（AGENTS/DREAMS/HEARTBEAT/IDENTITY/MEMORY/SOUL/TOOLS/USER）+ 配置目录（.agents/.learnings/memory/temp/.openclaw/.dreams）；本轮完成全部 6 个 agent（auditor/mathematician/physicist/programmer/psychologist/steward）运行时状态文件 `openclaw-workspace-state.json` 迁移至各自 `temp/` 目录，至此所有 agent 工作空间根目录均无运行时状态文件残留
- **梦境记忆同步**：workspace/steward/memory/.dreams/events.jsonl 新增 6 条 `memory.recall.skipped` 事件（涉及 research-assistant 技能能力检索 / 杨权身份核工程背景 / OpenClaw T042 版本查询等主题）
- **3 个新文件待入库**：2 篇 wiki/syntheses 重新生成（Buzsáki 2002 海马θ 的 summarize/extract，时间戳更新至 16:10/16:13）+ 1 篇 psychologist 会话 memory（2026-06-22 22:52）
- **state/openclaw.sqlite 数据库变化**：日常业务数据持久化，体积稳定（25,350,144 字节），仅 mtime 更新无实质内容差异
- **Git自动推送**：每日凌晨 04:00 自动同步本地更改到 main 分支（development 已废弃）

### 版本 4.3.8 (2026-06-22)
- **research-assistant 升级 v5.20.0 → v5.21.0**：全面补充 9 项薄弱环节，融合 ARS / Nature-skills / PaperSpine 三家长处。新增文档：
  - `references/prisma-systematic-review.md` — PRISMA 9 阶段系统综述 SOP (ARS)
  - `references/synthesize-peer-review.md` — 7-agent 同行评议 SOP (ARS Reviewer)
  - `references/apa7-citation-checklist.md` — APA 7 引用核验 50 项
  - `references/originality-checklist.md` — 原创性核验 30 项 (5 类抄袭)
  - `references/manuscript-audit-checklist.md` — 终稿完整性审计 60 项 (PaperSpine)
  - `assets/motivation-thread-template.md` — 章节 motivation + section blueprints (PaperSpine)
  - `assets/polish-nature-style.md` — Nature 风格润色 prompt (Nature-skills)
  - `assets/data-availability-template.md` — Data Availability 4 模板 (Nature-skills)
  - `hooks/quarto-cite-audit.md` — quarto 编译前 5 步引用审计 (PaperSpine latex)
  - 同步更新 `SKILL.md` description (加 9 项新触发短语)、模板/导航表、`references/index.md` 章节导航/场景查找/hooks 列表/workboard tracker
- **5 篇模块引用文档重写**：`references/module-{maintain,manage,search,summarize,synthesize}.md` 内容重组，与新模板/工作流对齐（合计 +135 / −218 行净增精简）
- **scripts/config.json 密钥引用形式统一**：`zotero.user_id_env` 从 `{ZOTERO_USER_ID}` 修正为 `${ZOTERO_USER_ID}`，与 `zotero.api_key_env` / `deepseek.api_key_env` / `semantic_scholar.api_key_env` 等其他 `*_env` 字段保持一致
- **openclaw.json meta 同步**：`lastTouchedVersion` 2026.6.8 → 2026.6.9，`lastTouchedAt` 同步至 2026-06-21 18:29 UTC
- **密钥核查**：扫描所有待提交文件（openclaw.json、scripts/config.json、5 篇模块引用、5 个 .py 脚本、state/openclaw.sqlite、wiki 更新），无硬编码 API Key；所有密钥均使用系统变量引用（`${ENV_VAR}` 或 `os.environ.get`）；`.env`/`.bak`/`.key`/`.secret` 已在 `.gitignore` 排除范围
- **工作空间核查**：10 个代理 workspace/{agents}/ 目录结构整洁，每个代理仅含 8 个 .md 配置文件（AGENTS/DREAMS/HEARTBEAT/IDENTITY/MEMORY/SOUL/TOOLS/USER）+ 配置目录（.agents/.learnings/memory/temp/.openclaw/.dreams），无中间文件、解析文件、一次性文件需要清理；本轮将 4 个 agent (mathematician/physicist/programmer/steward) 的运行时状态文件 `openclaw-workspace-state.json` 移入各自 `temp/` 目录
- **state/openclaw.sqlite 数据库变化**：日常业务数据持久化，体积稳定（25,350,144 字节），仅 mtime 更新无实质内容差异
- **Git自动推送**：每日凌晨 04:00 自动同步本地更改到 main 分支（development 已废弃）

### 版本 4.3.7 (2026-06-21)
- **密钥核查**：扫描所有待提交文件（openclaw.json、state/openclaw.sqlite、5 篇 wiki sources、1 篇 wiki synthesis、programmer 会话 memory），无硬编码 API Key；所有密钥均使用系统变量引用（`${ENV_VAR}` 或 `os.environ.get`）；`.env`/`.bak`/`.key`/`.secret` 已在 `.gitignore` 排除范围
- **工作空间核查**：10 个代理 workspace/{agents}/ 目录结构整洁，每个代理仅含 7 个 .md 配置文件（AGENTS/HEARTBEAT/IDENTITY/MEMORY/SOUL/TOOLS/USER）+ 配置目录（.agents/.learnings/memory/temp/.openclaw/.dreams），无中间文件、解析文件、一次性文件需要清理；psychologist/knowledge/ 与 steward/.clawhub/ 为标准配置目录（保留）
- **Wiki 新增 EEG θ 振荡研究资料**：5 篇 sources（Buzsáki 2002 海马θ / Cavanagh & Frank 2014 额中线θ / Klimesch 1999 α-θ 综述 / Lisman & Idiart 1995 θ-γ 耦合 / O'Keefe & Recce 1993 相位进动）+ 1 篇 synthesis（脑电θ波与认知过程，串联上述 5 篇文献）
- **programmer 会话 memory 同步**：新增 2026-06-19 20:57 会话记录（feishu direct 通道，主题：知识冲突场景下的主动抑制长期研究方案）
- **梦境记忆同步**：3 个 agent（programmer / psychologist / steward）的 memory/.dreams/events.jsonl 仅 mtime 更新，无新增/异常条目
- **openclaw.json meta 更新**：lastTouchedVersion 2026.6.6 → 2026.6.8，lastTouchedAt 同步至 2026-06-19
- **Git自动推送**：每日凌晨 04:00 自动同步本地更改到 main 分支（development 已废弃）

### 版本 4.3.6 (2026-06-19)
- **密钥核查**：扫描所有待提交文件（state/openclaw.sqlite），无硬编码 API Key；所有密钥均使用系统变量引用（`${ENV_VAR}` 或 `os.environ.get`）；`.env`/`.bak`/`.key`/`.secret` 已在 `.gitignore` 排除范围
- **工作空间核查**：11 个 agent 目录（10 个代理 + skills）结构整洁，每个代理仅含 8 个 .md 配置文件（AGENTS/DREAMS/HEARTBEAT/IDENTITY/MEMORY/SOUL/TOOLS/USER）+ 配置目录（.agents/.learnings/memory/temp/.openclaw/），无中间文件、解析文件、一次性文件需要清理；psychologist/knowledge/ 为预置空目录（保留）
- **state/openclaw.sqlite 数据库变化**：日常业务数据持久化，体积稳定（25,350,144 字节），仅 mtime 更新无实质内容差异
- **Git自动推送**：每日凌晨 04:00 自动同步本地更改到 main 分支（development 已废弃）

### 版本 4.3.5 (2026-06-18)
- **密钥核查**：扫描所有待提交文件（state/openclaw.sqlite），无硬编码 API Key；所有密钥均使用系统变量引用（`${ENV_VAR}` 或 `os.environ.get`）；`.env`/`.bak`/`.key`/`.secret` 已在 `.gitignore` 排除范围
- **工作空间核查**：10 个代理 workspace/{agents}/ 目录结构整洁，仅含 8 个 .md 配置文件（AGENTS/DREAMS/HEARTBEAT/IDENTITY/MEMORY/SOUL/TOOLS/USER）+ 配置目录（.agents/.learnings/memory/temp/），无中间文件、解析文件、一次性文件需要清理；DREAMS.md 为梦境日记（非临时文件，保留）
- **state/openclaw.sqlite 数据库变化**：日常业务数据持久化，体积稳定（25,350,144 字节），仅 mtime 更新无实质内容差异
- **Git自动推送**：每日凌晨 04:00 自动同步本地更改到 main 分支（development 已废弃）

### 版本 4.3.4 (2026-06-17)
- **密钥核查**：扫描所有待提交文件（state/openclaw.sqlite），无硬编码 API Key；所有密钥均使用系统变量引用（`${ENV_VAR}` 或 `os.environ.get`）；`.env`/`.bak`/`.key`/`.secret` 已在 `.gitignore` 排除范围
- **工作空间核查**：10 个代理 workspace/{agents}/ 目录结构整洁，仅含 8 个 .md 配置文件（AGENTS/DREAMS/HEARTBEAT/IDENTITY/MEMORY/SOUL/TOOLS/USER）+ 配置目录（.agents/.learnings/memory/temp/），无中间文件、解析文件、一次性文件需要清理
- **state/openclaw.sqlite 数据库变化**：日常业务数据持久化，体积稳定（25,350,144 字节），仅 mtime 更新无实质内容差异
- **Git自动推送**：每日凌晨 04:00 自动同步本地更改到 main 分支（development 已废弃）

### 版本 4.3.3 (2026-06-16)
- **OpenClaw 升级 2026.6.5 → 2026.6.6**：wizard 重新运行 doctor；meta.lastTouchedVersion 同步至 2026.6.6，badge 同步至 2026.6.8
- **research-assistant config.json 密钥引用标准化**：所有 `*_env` 字段从纯变量名改为 `${VAR}` 形式，更明确表达"环境变量引用"语义。涉及字段：`deepseek.api_key_env` / `semantic_scholar.api_key_env` / `easy_scholar.api_key_env` / `zotero.user_id_env` / `zotero.api_key_env` / `jianguoyun.user_env` / `jianguoyun.password_env`
- **steward .clawhub 技能锁落地**：workspace/.clawhub/lock.json 记录已安装技能版本（ui-ux-pro-max 0.1.0 / ui-ux-for-openclaw 1.0.2 / minimax-pdf 1.0.0），作为后续技能升级/重装的依据
- **openclaw.json 配置清理**：移除 `plugins.allow` 中已废弃的 `agent-self-development` 入口（该插件已被新 plugin 体系取代，参考 MEMORY.md T002 归档）；对应 allow 列表同步精简
- **安全审计**：扫描并确认当前待提交文件中无硬编码 API Key，所有密钥均使用系统变量引用（`${ENV_VAR}` 或 `os.environ.get`）；`.env` 已在 `.gitignore` 排除范围，不会进入仓库
- **工作空间核查**：10 个代理 workspace/{agents}/ 目录结构整洁，仅含 8 个 .md 配置文件（AGENTS/DREAMS/HEARTBEAT/IDENTITY/MEMORY/SOUL/TOOLS/USER）+ 配置目录（.agents/.learnings/memory/temp/），无中间文件、解析文件、一次性文件污染
- **state/openclaw.sqlite 数据库变化**：日常业务数据持久化，体积稳定（25,350,144 字节）
- **Git自动推送**：每日凌晨 04:00 自动同步本地更改到 main 分支

### 版本 4.3.2 (2026-06-14)
- **steward manager 技能重命名**：HANDBOOK.md → AGENTS.md（统一项目级操作手册命名）。覆盖 references（manager-overview/directory-standards/version-standards/contract-standards/course-guide/program-guide/project-guide/lesson-plan-guide/thesis-guide/task-flow-guide/sync-standards）/ BaseMaintainer.py + 4 个 Maintainer 子类 / template-versions.json / assets/project-level/AGENTS.template（新增）/ HANDBOOK.template（已删除）
- **steward manager 仓库路径迁移**：`/data/disk/仓库/` → `/data/disk/OneDrive/Applications/openclaw repository/`（OneDrive 挂载点变化）。覆盖 BaseMaintainer.py / steward MEMORY.md / wiki sources + syntheses / 全员 TOOLS.md 仓库默认位置字段
- **research-assistant v5.12.0 升级**：参数优先级统一为 **key > config > env**（之前 key > env > config），config.json 显式配置优先于散落环境变量便于跨环境复用；config.json 新增 `semantic_scholar.api_key` / `zotero.{user_id,api_key}` / `jianguoyun.{url,user,password}` 明文字段（默认空，fallback 到 .env）。涉及模块：Summarizer / Searcher / SemSchSearcher / ScholarSearcher / ZoteroJianguoyunDownloader
- **mark_old_projects_generated.py**：新增老项目 AGENTS.md GENERATED_START/END 标记脚本，让老项目能"接收"模板后续更新（走"安全合并"路径）
- **openclaw.json 配置清理**：移除 `agents.defaults.model.fallbacks` 字段（重复配置，primary 已含模型名）
- **Git 推送目标更新**：从 `development` 分支切换至 `main` 分支（development 分支已于 2026-06-12 删除；本仓库 main 为唯一常驻分支）
- **安全审计**：扫描并确认当前待提交文件中无硬编码 API Key，所有密钥均使用系统变量引用（`${ENV_VAR}` 或 `os.environ.get`）
- **工作空间核查**：11 个代理 workspace/{agents}/ 目录结构整洁，仅含 8 个 .md 配置文件（AGENTS/DREAMS/HEARTBEAT/IDENTITY/MEMORY/SOUL/TOOLS/USER）+ 配置目录（.agents/.learnings/.openclaw/memory/temp/steward.clawhub），无中间文件污染
- **记忆同步**：全部 10 个代理的 DREAMS.md、memory/.dreams/ 日志文件日常同步（events.jsonl、phase-signals.json、session-corpus、short-term-recall.json 等）
- **Dreaming 同步**：全部 10 个代理新增 2026-06-04~13 dreaming 报告（light/deep/rem）
- **Wiki 同步**：syntheses（3 篇）+ sources/repository.md 仓库路径字段统一更新；知识库整体一致
- **Git自动推送**：每日凌晨 04:00 自动同步本地更改到 main 分支

### 版本 4.3.1 (2026-06-05)
- **OpenClaw 升级 2026.6.1**: verboseDefault: full→on, 新增 blockStreaming, queryMode: recent→message, promptStyle: balanced→precision-heavy
- **工作空间清理**: 删除 44 个 `.migrated` 升级备份文件；`memory/dreaming/` 和 `memory/.dreams/session-corpus/` 加入 `.gitignore` 避免 untracked 文件堆积
- **安全审计**: 扫描并确认当前待提交文件中无硬编码 API Key，所有密钥均使用系统变量引用
- **记忆同步**: 全部 10 个代理的 DREAMS.md、memory/.dreams/ 日志文件日常同步（events.jsonl、phase-signals.json、session-corpus、short-term-recall.json 等）
- **Dreaming 同步**: 全部 10 个代理新增 2026-06-05 dreaming 报告（light/deep/rem）
- **配置同步**: `openclaw.json` 多字段更新（streaming / 记忆 prompt 优化）
- **Git自动推送**: 每日凌晨 04:00 自动同步本地更改到 main 分支

### 版本 4.3.0 (2026-06-03)
- **task-flow 三件套定型**：task-flow-guide v2.2 → v2.3（合并三件套 + TODO 7 字段 + claim 协议 + IM 模板 + 占位符）
- **workboard-guide v1.4.0 升级**：4 个新功能（--session flag / 默认 backlog / start 真触发 run / execution 完整）+ Dashboard 限制 + 卡状态机
- **manager workboard 完整重做**：Node.js → Python 包（v5.5.0），CLI 统一入口；修复 start 路径 A/B 复用 session + idempotencyKey；create --assignee 必填 + 联动 sessionKey + execution
- **v8.19.0 红线规则**：禁止修改任何 pnpm/npm 依赖包；bug 修复走 issue/PR + 插件机制重装 + 升级版本
- **flows/registry.sqlite + tasks/runs.sqlite 上传 GitHub**：taskflow 工作流存储（402 条）+ task 执行记录（315 条）加入版本控制；WAL/SHM 临时文件保持忽略
- **wiki synthesis 命名规则 v8.17.0**：必须带 YYYY-MM-DD-HH-MM-SS- 时间戳前缀
- **skill-developer 三段式 CLI v5.4.0**：scripts 升级，CLI 入口规范化
- **lark 技能集中化**：集中到 /root/.agents/skills/
- **rps 项目挂起**：老板未授权，停止一切操作
- **manager references 清理**：清理冗余 + 合并双件套
- **安全审计**：扫描并确认无硬编码 API Key
- **Git自动推送**：每日 04:00 自动同步 main 分支

### 版本 4.2.9 (2026-06-02)
- **安全审计**: 扫描并确认当前待提交文件中无硬编码 API Key，所有密钥均使用系统变量引用
- **配置更新**: openclaw.json 启用飞书 blockStreaming（块流式回复）；cron 日报任务 timeout 从 300s 提升至 600s
- **记忆同步**: 全部 10 个代理的 DREAMS.md、memory/.dreams/ 日志文件日常同步（events.jsonl、phase-signals.json、session-corpus、short-term-recall.json 等）
- **Wiki 同步**: 知识库概念/实体/综合分析/报告页面全面更新，新增认知过程对称性破缺机制理论框架综述
- **Git自动推送**: 每日凌晨 04:00 自动同步本地更改到 main 分支

### 版本 4.2.8 (2026-05-31)
- **记忆同步**: 全部 10 个代理的 DREAMS.md、memory/.dreams/ 日志文件日常同步（events.jsonl、phase-signals.json、session-corpus、short-term-recall.json 等）
- **Dreaming 同步**: 全部 10 个代理新增 2026-05-31 dreaming 报告（light/deep/rem）
- **Cron 状态**: jobs.json、jobs-state.json 同步
- **Git自动推送**: 每日凌晨 04:00 自动同步本地更改到 main 分支

### 版本 4.2.7 (2026-05-30)
- **工作空间清理**: 程序员 sessions/ 移至 temp/sessions/，大管家 agent/ 和 sessions/ 移至 temp/ 对应子目录
- **安全审计**: 扫描并确认当前待提交文件中无硬编码 API Key，所有密钥均使用系统变量引用
- **记忆同步**: 全部 10 个代理的 DREAMS.md、memory/.dreams/ 日志文件日常同步（events.jsonl、phase-signals.json、session-corpus、short-term-recall.json 等）
- **Dreaming 同步**: 全部 10 个代理新增 2026-05-30 dreaming 报告（light/deep/rem）
- **Cron 状态**: jobs.json、jobs-state.json 同步
- **插件同步**: plugins/installs.json 更新
- **配置同步**: openclaw.json 多字段更新
- **Git自动推送**: 每日凌晨 04:00 自动同步本地更改到 main 分支

### 版本 4.2.6 (2026-05-26)
- **References 重构**: 程序员 references/ 目录重构为 8 个结构化章节（ch01-ch08）
- **References 备份归档**: 原 13 个旧文件移至 temp/references-backup-20260526/
- **记忆同步**: steward/memory/.dreams/ 日志文件日常同步（session-corpus 2026-05-23~25）
- **Wiki 同步**: entities/index.md、wiki/index.md 小幅更新
- **Cron 状态**: jobs-state.json 同步
- **安全审计**: 扫描并确认当前待提交文件中无硬编码 API Key，所有密钥均使用系统变量引用
- **Git自动推送**: 每日凌晨 04:00 自动同步本地更改到 main 分支

### 版本 4.2.5 (2026-05-23)
- **安全加固**: openclaw.json JINA API Key 改为环境变量 `${JINA_API_KEY}` 引用
- **技能文档完善**: 新增/更新 7 个 Agent 的 skill references 文件（workflows.md、guides、standards 等）
  - auditor: consistency-guide.md, workflows.md
  - instructor, mathematician, physicist, presenter, psychologist, reviewer, writer, programmer, steward 均新增 workflows.md
  - mathematician 新增 mathematics-guide.md、statistics-guide.md
  - physicist 新增 formula-derivation-standards.md、physicist-standards.md、physics-tools-standards.md
  - programmer 新增 development-guide.md、oop-principles-guide.md
  - reviewer 新增 citation-hallucination-workflow.md
  - writer 新增 modification-guide.md、writing-process-guide.md
  - steward/manager 新增 organize-guide.md、skill-audit-workflow.md
- **记忆文件同步**: workspace/steward/memory/2026-05-23.md 新增
- **中间文件归档**: wiki/syntheses/ 中 5 个 2026-05-23 研究草稿移至 temp/syntheses-backup-20260523/
- **Cron 任务状态**: jobs-state.json 同步更新
- **模型配置**: 5 个代理的 agents/*/agent/models.json 小幅更新

### 版本 4.2.4 (2026-05-20)
- **Wiki 源文件清理**: 删除 15 个过时/冗余的 wiki sources 文件（AI工具使用指南、Zotero文献管理、agent-self-development独立页面、projects.md、wiki配置等），统一入口至 wiki/index.md
- **Wiki 索引重构**: wiki/index.md 精简（-21行），移除过时子目录引用；删除 program-project.md 和 project.md 中已迁移内容
- **OpenClaw 配置更新**: openclaw.json 多字段调整（-22行），plugins/installs.json 同步更新
- **Cron 任务状态**: jobs-state.json 小幅同步
- **工作空间清理**: workspace/.clawhub/lock.json 删除（过时锁定文件）
- **安全审计**: 扫描并确认当前待提交文件中无硬编码 API Key，所有密钥均使用系统变量引用
- **Git自动推送**: 每日凌晨 04:00 自动同步本地更改到 main 分支

### 版本 4.2.3 (2026-05-19)
- **agent-self-development v4.3.0 规划文档更新**: 完善 Object-Driven Layer (ODL) 架构蓝图，明确 Task 对象与 Assets 资产层设计
  - Task JSON 数据结构定义（status/taskType/plan/execution 等字段）
  - 工具扁平化问题分析（13 个 tool → 2 核心对象）
  - 持久化架构调整（SQLite → JSON 文件）
  - 方法映射表（create/update/advance/status/diagnose/archive）
- **agent-self-development TODO.md 重构**: 208 行变更，细化 v4.3.0 开发任务分解
- **Cron 任务状态更新**: jobs-state.json 小幅同步
- **.gitignore 加固**: 添加 `*.db-shm` 和 `*.db-wal` 排除数据库 WAL 日志文件
- **安全审计**: 扫描并确认当前待提交文件中无硬编码 API Key
- **Git自动推送**: 每日凌晨 04:00 自动同步本地更改到 main 分支

### 版本 4.2.2 (2026-05-16)
- **MiniMax 模型集成**: Steward 配置新增 minimax / minimax-cn / minimax-portal / minimax-portal-cn 四个 provider，支持 MiniMax-M2.7 及 MiniMax-M2.7-highspeed 模型（204.8K 上下文 / 131.072K 最大输出）
- **README更新**: 同步版本号、Agent 数量(7→10)、运行状态标签(运行中→稳定版)
- **Git自动推送**: 每日凌晨 04:00 自动同步本地更改到 main 分支

### 版本 4.2.1 (2026-05-16)
- **安全审计**: 扫描并确认当前待提交文件中无硬编码 API Key，所有密钥均使用系统变量引用
- **README更新**: 同步版本号、时间戳、运行状态
- **Git自动推送**: 每日凌晨 04:00 自动同步本地更改到 main 分支

### 版本 4.2.0 (2026-05-14)
- **agent-self-development v4.2.0 升级**: Cognitive Intelligence —— 让 Tool-Driven 架构从「可用」走向「智能」
  - **认知轨迹基础设施**: 每次 tool 调用记录到 `.agent/cognitive-traces/{runId}.jsonl`，`self_diagnose` 返回 `cognitiveTraceSummary`
  - **模板智能渲染引擎**: `src/common/template-engine.js` 支持变量/条件/列表/嵌套，4 个 guide tools 动态渲染
  - **案例索引数据库**: SQLite + Jaccard 相似度，`create_plan` 返回相似案例，`archive_task` 自动索引
  - **诊断增强 v2**: `self_diagnose` 返回 `trendAnalysis`（阶段耗时/偏差频率/历史均值）+ `riskFlags`（最多 3 条预警）
  - **架构风险修复**: 硬编码路径（RISK-1）、双重状态更新（RISK-4）、事件路径解析重复（RISK-2）、Heartbeat 未接入 HookRegistry（RISK-3）、项目级路径未抽象（RISK-8）
  - **git tag 规范化**: 补打 v3.3.0 ~ v4.1.0 tag，`package.json` 升至 4.2.0
  - **任务类型模板**: 新增 coding / research / documentation 专用 planning 模板
  - **测试**: 126/126 断言通过，45 个 suite，0 失败
- **README更新**: 同步版本号、时间戳、运行状态
- **Git自动推送**: 每日凌晨 04:00 自动同步本地更改到 main 分支

### 版本 4.1.5 (2026-05-14)
- **agent-self-development 插件代码重构**：
  - 删除 `agents/` 目录下的角色定义文件（developer.md / product-manager.md / reviewer.md），角色规范迁移至 `.agent/` 元数据层
  - 新增根级 `SKILL.md`，统一入口规范
  - 新增 `docs/architecture/` 架构文档、`docs/reports/` 测试与审查报告、`docs/RELEASE.md` 发布说明
  - 引入 `src/common/cognitive-trace.js` 认知轨迹记录、`src/common/template-engine.js` 模板引擎、`src/common/project-context.js` 项目上下文、`src/common/case-index.js` 案例索引
  - 新增 `src/templates/` 下 coding.md / documentation.md / research.md 三类任务模板
  - `skills/project-context/` 整体移除，能力合并至新版模板系统
  - `skills/update-plan/` 重构，新增 `assets/` 资源目录；新建 `skills/update-todo/` 技能
  - 源代码层（src/tools/、src/common/、test/）全面同步，测试用例扩展
- **task-dispatcher 技能清理**：从所有代理工作空间（auditor / instructor / mathematician / physicist / presenter / programmer / psychologist / reviewer / steward / writer）及公共 `workspace/skills/` 中移除 task-dispatcher 符号链接或目录
- **OpenClaw 主配置更新**：`openclaw.json` 多字段调整（127 行变更）
- **各代理记忆日常同步**：所有 10 个代理的 `.dreams/events.jsonl`、`.dreams/phase-signals.json`、`.dreams/session-ingestion.json`、`.dreams/short-term-recall.json`、 dreaming（light/deep/rem）文件同步至 2026-05-14
- **安全审计**：扫描并确认当前待提交文件中无硬编码 API Key，所有密钥均使用系统变量引用
- **README更新**：同步版本号、时间戳、运行状态
- **Git自动推送**：每日凌晨 04:00 自动同步本地更改到 main 分支

### 版本 4.1.4 (2026-05-13)
- **Reviewer模型配置更新**：`agents/reviewer/agent/models.json` 中 DeepSeek V4 Flash 模型参数调整（contextWindow 256000→1000000, maxTokens 256000→384000）
- **Course Manager技能重构**：
  - 移除 `temp/draft` 目录创建及归档功能，改由 Git 管理版本历史
  - 备份文件（backup/旧/old）和中间文件（.tmp/.temp/.log/.bak）统一归为 intermediate 处理
  - 新增 Git 本地仓库初始化功能
  - `Maintainer.py` 精简 123 行代码
- **Thesis Manager技能重构**：
  - 同步 course-manager 的改动，移除 `archive_to_draft` 方法及 temp 相关目录
  - 角色文件名中文化修正：数学家.md→mathematician.md、物理学家.md→physicist.md
  - `Maintainer.py` 精简 233 行代码
- **Steward记忆更新**：
  - 云文档所有权转移规则明确化（创建后需提醒用户手动转移）
  - 新增 TODO.md 更新后需与老板讨论的规则
- **安全审计**：扫描并确认当前待提交文件中无硬编码 API Key，所有密钥均使用系统变量引用
- **README更新**：同步版本号、时间戳、运行状态
- **Git自动推送**：每日凌晨 04:00 自动同步本地更改到 main 分支

### 版本 4.1.3 (2026-05-13)
- **Cron任务通知调整**：Git自动推送任务的通知目标从实验室群(`oc_cd80162eb81e39f77160a0daab2a6ab8`)改为当前私聊(`ou_a4bc01a3736e458817235a94124d340c`)，便于个人接收任务执行状态
- **安全审计**：扫描并确认当前待提交文件中无硬编码 API Key，所有密钥均使用系统变量引用
- **README更新**：同步版本号、时间戳、运行状态
- **Git自动推送**：每日凌晨 04:00 自动同步本地更改到 main 分支

### 版本 4.1.2 (2026-05-13)
- **安全审计**：扫描并确认当前待提交文件中无硬编码 API Key，所有密钥均使用系统变量引用
- **README更新**：同步版本号、时间戳、运行状态
- **Git自动推送**：每日凌晨 04:00 自动同步本地更改到 main 分支

### 版本 4.2.0 (2026-07-28)
- **日常同步**：各代理 .dreams/events.jsonl 记忆文件更新（12 files, +60 lines）
- **工作空间清理**：清理 programmer/steward 目录下的 openclaw-workspace-state.json 临时文件
- **安全审计**：确认所有待提交文件中无硬编码 API Key
- **Git自动推送**：每日凌晨 04:00 自动同步本地更改到 development 分支

### 版本 4.1.2 (2026-05-13)
- **安全审计**：修复 `agents/programmer/agent/models.json`、`agents/main/agent/models.json`、`agents/instructor/agent/models.json` 中 6 处硬编码 API Key（3 处 Tencent Token Plan + 3 处 Kimi Code），分别替换为 `${TENCENTTOKENPLAN_API_KEY}` 和 `${KIMICODE_API_KEY}` 系统变量引用
- **README更新**：同步版本号、时间戳、运行状态
- **Git自动推送**：每日凌晨 04:00 自动同步本地更改到 main 分支

### 版本 4.1.1 (2026-05-12)
- **安全审计**：扫描并确认当前待提交文件中无硬编码 API Key，所有密钥均使用系统变量引用
- **README更新**：同步版本号、时间戳、运行状态
- **Git自动推送**：每日凌晨 04:00 自动同步本地更改到 main 分支

### 版本 4.1.0 (2026-05-11)
- **agent-self-development v4.1.0 升级**:从「插件代劳」走向「Agent 自主」
  - 核心方法论转变:插件暴露能力、Agent 按需调用，从被动接受到主动选择
  - 强化「用户领航 → Agent 执行 → 插件记录」原则，插件不做业务决策
  - 保留四层架构与权力边界，向后兼容 v4.0.0 项目上下文层

### 版本 4.0.0 (2026-05-10)
- **agent-self-development v4.0.0 升级**:引入项目上下文层(Project Context Layer)
  - 双系统平行架构:Agent 自行行动系统 + 史官系统
  - 四层架构与权力边界:用户层 / 代理层 / 插件层 / 系统底层
  - 标准项目目录结构:四文件契约(README.md / metadata.json / SKILL.md / TODO.md)
  - .agent/ 元数据层:events/ / locks/ / decisions/ / tasks/
  - 业务目录层:uploads/ / manuscripts/ / docs/ / knowledge/ / skills/ / temp/
- **多 Agent 协作体系**:定义 PM / Developer / Reviewer 三角色
  - 协作标记规范:18 个标准标记([ARCH_APPROVED] / [APPROVED] / [BLOCKER] 等)
  - 冲突解决机制:架构争议由 PM 仲裁,合规争议 Reviewer 有一票否决权
- **README 重构**:
  - 新增标准项目目录结构说明
  - 新增多 Agent 协作角色与流程
  - 更新部署指南(初始化项目目录结构)
  - 同步 OpenClaw 版本号 2026.5.7
- **Git自动推送**:每日凌晨 04:00 自动同步本地更改到 main 分支

### 版本 3.4.1 (2026-05-10)
- **安全审计**:扫描并确认当前待提交文件中无硬编码 API Key,所有密钥均使用系统变量引用
- **Gitignore 加固**:显式添加 `credentials/`、`qqbot/data/credential-backup-*.json` 至 `.gitignore`
- **README更新**:同步版本号、时间戳、运行状态
- **Git自动推送**:每日凌晨 04:00 自动同步本地更改到 main 分支

### 版本 3.4.0 (2026-05-09)
- **agent-self-development 插件重构**:目录结构重组,新增 `agents/`、`docs/`、`skills/`、`test/reports/` 目录
- **安全审计**:扫描并修复 `workspace/skills/research-assistant/scripts/config.json` 中 3 处硬编码 API Key
- **各代理记忆日常更新**:所有 10 个代理的 `.dreams/` 记忆文件、events.jsonl、phase-signals.json 日常同步
- **README更新**:同步版本号、时间戳、运行状态
- **Git自动推送**:每日凌晨 04:00 自动同步本地更改到 main 分支

### 版本 3.3.9 (2026-05-08)
- **IDENTITY.md 全局精炼**:所有 10 个代理 IDENTITY.md 从平均 200+ 行精炼至 75 行(减负 62-72%)
- **Wiki 完整性修复**:创建 5 个缺失实体/概念页面
- **Wiki 来源补充**:为 7 个页面补充 `updatedAt` + `sourceIds`
- **AGENTS.md 领域规范**:为 10 个代理各添加专属行为规范
- **技能解除禁用**:summarize 和 zotero-scholar 恢复 enabled
- **Cron 修复**:main 定时任务 sessionKey 从 steward 改为 main

### 版本 3.3.3-3.3.8 (2026-05-08)
- **MEMORY.md/TOOLS.md 精简**:所有代理删除陈述性记忆和公共路径,只保留工作记忆+If-Then规则
- **Wiki 知识库建立**:创建 7 个 wiki 页面
- **wiki 改为全局共享**:删除 per-agent 子目录,统一至 `~/.openclaw/wiki/`
- **Git 跟踪调整**:research-assistant、Skill-developer 纳入 Git,第三方技能排除

### 版本 3.3.2 (2026-05-08)
- **工作空间结构重构**:main 代理工作空间从根目录隔离至独立子目录
- **技能目录统一迁移**:技能从 `~/.openclaw/skills/` 回归 `~/.openclaw/workspace/skills/`
- **README更新**:同步版本号、时间戳、运行状态

### 版本 3.3.1 (2026-05-08)
- **README更新**:同步版本号、时间戳、运行状态
- **Git自动推送**:每日凌晨 04:00 自动同步本地更改到 main 分支

### 版本 3.3.0 (2026-05-06)
- **技能全局共享重构**:所有技能从 `workspace/skills/` 迁移至 `~/.openclaw/skills/`
- **Skill-developer v3.1.0**:升级为元技能混合结构
- **research-assistant v4.0.0**:重构为 Skill-developer v3.1.0 规范
- **cron 任务更新**:steward 每日仓库检查任务更新 CLI 入口
- **安全清理**:从所有代理 `tools.alsoAllow` 中移除误配的技能名称

### 版本 2026-06-04 (每日自动推送)
- **安全审计**:扫描并确认无硬编码 API Key
- **工作空间清理**:steward 备份文件移至 temp/；physicist 新增 temp/ 目录
- **知识沉淀**:新版 Quarto PDF 编译配置总结（3 范式 + CJK 字体 + APA 7th）
- **踩坑记录**:git checkout 覆盖 working tree 改动经验沉淀
- **Dreaming 日记**:10 个 Agent 梦境日记自动增长（2026-06-04）
- **README更新**:同步版本号、时间戳、运行状态
- **Git自动推送**:每日凌晨 04:00 自动同步本地更改到 main 分支

### 版本 3.2.9 (2026-05-06)
- **安全审计**:扫描并替换 10 个 agents 的 models.json 中硬编码 API Key
- **README更新**:同步版本号、时间戳、运行状态
- **Git自动推送**:每日凌晨 04:00 自动同步本地更改到 main 分支

### 版本 3.2.8 (2026-05-05)
- **安全审计**:扫描并确认无硬编码 API Key
- **README更新**:同步版本号、时间戳、运行状态
- **Git自动推送**:每日凌晨 04:00 自动同步本地更改到 main 分支

### 版本 3.2.8 (2026-05-18)
- **模型配置升级**: 新增 Kimi Code 系列模型(kimi-for-coding, kimi-code, k2p5)
- **上下文窗口扩展**: DeepSeek V4 Flash 从 256K 扩展至 1M
- **MiniMax 更新**: M2.5 → M2.7, 新增 VL-01 视觉模型, maxTokens 扩展至 25600
- **工作空间清理**: steward/ 目录 LaTeX 中间文件移至 temp/
- **pixel-office 优化**: EditorToolbar 组件、layoutSerializer、spriteCache 精简
- **Git自动推送**: 每日 04:00 自动同步 main 分支
- **安全审计**:扫描并确认无硬编码 API Key
- **README更新**:同步版本号、时间戳、运行状态
- **Git自动推送**:每日凌晨 04:00 自动同步本地更改到 main 分支

### 版本 3.2.6 (2026-05-03)
- **安全审计**:扫描并确认无硬编码 API Key
- **README更新**:同步版本号、时间戳、运行状态
- **Git自动推送**:每日凌晨 04:00 自动同步本地更改到 main 分支

### 版本 3.2.4 (2026-04-28)
- **安全审计**:扫描并确认无硬编码 API Key
- **README更新**:同步版本号、时间戳、运行状态
- **Git自动推送**:每日凌晨 04:00 自动同步本地更改到 main 分支

### 版本 3.2.3 (2026-04-27)
- **安全审计**:定期扫描仓库硬编码敏感信息,确保无API Key泄露
- **README更新**:同步版本号、时间戳、运行状态

### 版本 3.2.2 (2026-04-26)
- **统一命名会话机制**:agent-self-development 插件全面改用命名会话
- **修复重复定义**:清理 physicist 和 studentaffairsassistant MEMORY.md 中的重复「活跃会话清单」
- **更新版本历史**:所有插件模块版本号同步更新

### 版本 3.2.1 (2026-04-19)
- **存储结构分离**:agent-self-development 插件与 memory-core 完全分离
  - 新增 `events/` 目录:存放详细事件记录
  - 新增 `diary/` 目录:存放每日发展日记
  - 保留 `memory/.dreams/`:OpenClaw核心记忆索引(自动维护)
- **更新所有代理配置**:9个代理的 TOOLS.md、MEMORY.md、HEARTBEAT.md 全部更新
- **更新 agent-self-development 插件**:所有注入式技能路径更新为 events/ 和 diary/
- **创建统一目录结构**:所有代理工作空间统一使用 events/ + diary/ + memory/ 结构

### 版本 3.2.0 (2026-04-19)
- **新增MCP服务器支持**:为公共技能添加MCP服务器,支持通过OpenClaw MCP接口调用
- **删除mcp-adapter技能**:移除独立的mcp-adapter技能,功能由OpenClaw内置mcp工具替代
- **删除semantic-scholar MCP**:被 research-assistant 取代
- **更新Skill-developer文档**:添加MCP支持章节

### 版本 3.1.2 (2026-04-19)
- **创建项目文件README.md**:为实验室仓库和教研室仓库各子目录创建项目文件README.md
- **统一项目索引格式**:各代理TOOLS.md中使用`> 项目索引详见...`注释指向对应README
- **规范项目文件结构**:统一项目文件目录结构和索引格式

### 版本 3.2.2 (2026-06-06)
- **每日自动同步 2026-06-06**: 102 文件变更(56702+/-52506-)
- **知识库同步**: Wiki 新增 3 条源文献摘要、1 篇综合报告、CCT/认知/代理记忆等综合页更新
- **技能同步**: research-assistant 脚本重构,mathematician/psychologist/manager 技能更新
- **Agent梦境同步**: 10 个 Agent 的 DREAMS.md 及 dreams 记忆数据库同步
- **配置同步**: openclaw.json 配置微调
- **清理**: mathematician MCP server 删除、steward 旧体检报告删除

### 版本 3.2.9 (2026-06-15)
- **每日自动同步 2026-06-15**: 2 文件变更(2+/-12-,含 steward .clawhub 技能锁更新)
- **密钥核查**: 所有 API Key 使用系统环境变量,无硬编码(待推送文件 steward/.clawhub/lock.json + state/openclaw.sqlite mtime 同步,无明文)
- **工作空间核查**: 10 个 Agent 目录结构正常,标准 8 个 .md 配置文件 + temp/memory/.agents/.openclaw/.learnings/steward.clawhub 目录齐全,无 stray 中间文件
- **ClawHub 技能同步**: steward/.clawhub/lock.json 新增 3 个 minimax-* 技能锁(minimax-pdf v1.0.0 / minimax-docx v1.0.0 / minimax-xlsx v1.0.0);workspace/.clawhub/lock.json 全局工具锁(未跟踪,设计内)
- **steward 记忆同步**: steward/memory/2026-06-14-1625.md(本次新生成,记录 rclone 卸载 + abraunegg onedrive 切换会话)
- **state/openclaw.sqlite**: 系统状态数据库 mtime 同步(无字节内容变化)
- **运行状态**: ✅ 稳定版,已推 main 分支

### 版本 3.2.7 (2026-06-12)
- **每日自动同步 2026-06-12**: 64 文件变更（含梦境记忆同步 + 迁移文件清理）
- **密钥核查**: 全仓库扫描无硬编码 API Key（仅 3 处 `your-xxx-key` 占位符在 skills/research-assistant 文档/备份中）
- **工作空间核查**: 10 个 Agent 目录结构正常，每个工作区含 8 个标准 .md 配置文件 + memory/temp/.agents/.learnings 等配置目录
- **迁移文件清理**: 40 个 .migrated 一次性迁移备份（系统升级产物）从 10 个 Agent 的 `memory/.dreams/` 移至对应 `temp/memory_dreams_migrated/` 目录；`wiki/.openclaw-wiki/source-sync.json.migrated` 移至 `wiki/temp/`（`.gitignore` 自动忽略）
- **Agent梦境同步**: 10 个 Agent 的 DREAMS.md 新增 2 段梦境条目 + dreams 记忆数据库（events.jsonl）同步；旧版索引（phase-signals/session-ingestion/short-term-recall/daily-ingestion.json）已迁移至 .migrated
- **新工作流文件**: workspace/psychologist/memory/2026-06-11-1055.md（学术研究助手 cron session 历史）
- **state/openclaw.sqlite**: 系统状态数据库同步（7MB+，WAL/SHM 已忽略）
- **运行状态**: ✅ 稳定版，已推 development 分支

### 版本 3.2.8 (2026-06-13)
- **每日自动同步 2026-06-13**: 3 文件变更(1+/-1746-)
- **密钥核查**: 所有 API Key 使用系统环境变量,无硬编码(grep 全仓库扫描无明文值)
- **工作空间核查**: 10 个 Agent 目录结构正常,标准 8 个 .md 配置文件 + temp/memory/.agents/.openclaw/.learnings 目录齐全
- **清理迁移**: psychologist/knowledge/{methodology,retrieval_report,review,index.json}(研究知识库目录) → psychologist/temp/knowledge/;state/openclaw.sqlite.pre-fix-20260612(备份文件) → programmer/temp/
- **Agent记忆同步**: programmer/memory/2026-06-12-1706.md、steward/memory/2026-06-12-{1706,1706-2}.md、steward/memory/2026-06-12.md(新生成)
- **state/openclaw.sqlite**: 系统状态数据库同步(WAL/SHM 已忽略)
- **运行状态**: ✅ 稳定版,已推 main 分支

### 版本 3.2.6 (2026-06-11)
- **每日自动同步 2026-06-11**: 47 文件变更(47061+/-45127-)
- **密钥核查**: 所有 API Key 使用系统环境变量,无硬编码(grep 全仓库扫描 `api_key/secret/token/password` 无明文值;待推送文件均为 DREAMS 日记、dreams 记忆数据库、state/openclaw.sqlite,无密钥泄露)
- **工作空间核查**: 10 个 Agent 目录结构正常,标准 8 个 .md 配置文件 + temp/memory/.agents/.openclaw/.learnings 目录齐全
- **清理迁移**: psychologist/knowledge/research/{hull_1920_scispace.pdf, reber_1967_academia.html, reberlab.html}(一次性研究下载文件) → psychologist/temp/research_2026-06-10/,gitignore 自动忽略
- **Agent梦境同步**: 10 个 Agent 的 DREAMS.md 及 dreams 记忆数据库(events.jsonl/phase-signals/session-ingestion/short-term-recall/daily-ingestion)同步
- **state/openclaw.sqlite**: 系统状态数据库同步(7MB,WAL/SHM 已忽略)
- **运行状态**: ✅ 稳定版,准备推送 development 分支

### 版本 3.2.5 (2026-06-10)
- **每日自动同步 2026-06-10**: 54 文件变更(64991+/-62432-)
- **密钥核查**: 所有 API Key 使用系统环境变量,无硬编码(grep 全仓库扫描 `api_key/secret/token/password` 无明文值;`config.json` 仅保留 `api_key_env` 字段名)
- **工作空间核查**: 10 个 Agent 目录结构正常,标准 8 个 .md 配置文件 + temp/memory/.agents/.openclaw/.learnings 目录齐全,无 stray 中间文件
- **Agent梦境同步**: 10 个 Agent 的 DREAMS.md 及 dreams 记忆数据库(events.jsonl/phase-signals/session-ingestion/short-term-recall)同步
- **steward MEMORY.md**: v8.33-v8.35 沉淀更新 — 飞书 IM @ bot 路由 / 发群消息 = reply / **沉淀方向根本转变**(从不要型 → do 型成功经验)
- **新增未追踪文件**: writer/memory/2026-06-09-1033.md(本次新生成)
- **state/openclaw.sqlite**: 系统状态数据库同步
- **运行状态**: ✅ 稳定版,准备推送 development 分支

### 版本 3.2.4 (2026-06-08)
- **每日自动同步 2026-06-08**: 54 文件变更(50484+/-47389-)
- **密钥核查**: 所有 API Key 使用系统环境变量,无硬编码(.env / gateway.systemd.env 均在 .gitignore 中,不入库)
- **工作空间核查**: 10 个 Agent 目录结构正常,无 stray 文件
- **清理迁移**: steward/skills/.skills_store_lock.json(运行期锁文件) → temp/_cleanup/,并新增 `/workspace/*/skills/.skills_store_lock.json` gitignore 规则
- **配置变更**: openclaw.json 调整模型回退(fallbacks deepseek-v4-flash → deepseek-v4-pro)、移除 agent-self-development 路径加载、启用 hooks.internal.self-improvement
- **.gitignore**: 新增 `!/hooks/` 与 `/workspace/*/skills/.skills_store_lock.json` 规则
- **Agent梦境同步**: 10 个 Agent 的 DREAMS.md 及 dreams 记忆数据库同步;programmer/steward MEMORY.md 更新
- **新增未追踪文件**: hooks/self-improvement/{HOOK.md,handler.ts,handler.js}、skills/.skills_store_lock.json、10 个 Agent memory/ontology/{schema.yaml,graph.jsonl}
- **运行状态**: ✅ 稳定版,准备推送 development 分支

### 版本 3.2.3 (2026-06-07)
- **每日自动同步 2026-06-07**: 71 文件变更(60700+/-62331-)
- **密钥核查**: 所有 API Key 使用系统环境变量,无硬编码
- **工作空间核查**: 10 个 Agent 目录结构正常,无 stray 文件
- **技能清理**: writer 技能删除旧 lookup/indexer/searcher 脚本(_meta.json、mcp/server.py、index/、scripts/lookup/ 等),保留核心 SKILL.md + scripts/main.py + scripts/writer/
- **Agent梦境同步**: 10 个 Agent 的 DREAMS.md 及 dreams 记忆数据库同步
- **新增未追踪文件**: steward/memory/2026-06-07.md(本次新生成)
- **运行状态**: ✅ 稳定版,无未提交变更

### 版本 3.1.1 (2026-04-19)
- **重构日志系统**:将实验室仓库和教研室仓库的日志文件迁移到各代理的memory目录
- **删除日志文件目录**:移除实验室仓库/日志文件/和教研室仓库/日志文件/目录
- **删除.log文件**:清理所有.log格式的日志文件
- **更新TOOLS.md**:移除所有代理TOOLS.md中的日志文件目录说明
- **创建缺失的README.md**:为内卷感知与工作繁荣项目、教研室各子目录创建README.md
- **统一项目索引格式**:使用">+注释"形式更新项目索引

### 版本 3.1 (2026-04-19)
- **新增Agent自我发展插件**:基于皮亚杰认知发展理论,每日00:00自动执行自我更新
- **重构MEMORY.md工作记忆规则**:删除与插件重复内容,统一引用 agent-self-development 规范
- **统一定时任务时间**:所有Agent每日自我更新改为00:00执行
- **修正事件记忆路径**:所有代理路径指向自己的工作空间
- **新增agent-self-development插件**:包含元认知、工作记忆、同化顺应三大模块(自动注入式,无需手动安装)

### 版本 3.0 (2026-04-16)
- **技能文件夹重构**:各Agent工作空间中的 `scripts` 文件夹内容已统一合并至 `skills` 文件夹,不再区分脚本和技能
- **新增子代理管理员技能**:面向对象设计的子代理管理技能,提供三阶段任务执行规范(计划→监控→调节)
- **新增技能开发者技能**:面向对象设计的技能开发技能,支持类、对象、属性、方法、继承、封装等概念
- **简化技能管理**:统一技能存储位置,降低维护复杂度

### 版本 2.1 (2026-04-13)
- 重构日志系统,移除公共记录工作日志脚本
- 迁移研究助手工具,整合文献检索和知识库功能
- 完善技能锁定机制,新增.skills_store_lock.json
- 更新所有Agent的TOOLS.md配置
- 新增实验室和教研室独立日志系统

### 版本 2.0 (2026-04-07)
- 重构备份策略,基于.openclaw根目录同步
- 完善Agent分工和权限体系
- 新增多仓库管理机制(实验室+教研室)

### 版本 1.0 (2026-04-06)
- 初始版本,多Agent系统上线

---

## 📄 许可证

本项目遵循 MIT 许可证,详见 LICENSE 文件。

---

## 👨‍💻 维护者

- **杨权** - 系统架构、实验室负责人
- **大管家Agent** - 自动维护、系统监控

---

**最后更新: July 27, 2026 05:00 (GMT+8)**
**系统版本**: OpenClaw 2026.6.11
**Git 分支**: main（development 分支已于 2026-06-12 删除）
**运行状态**: ✅ 稳定版
**备份状态**: ✅ 自动执行中
### 版本 3.3.0 (2026-07-18)
- **每日自动同步 2026-07-18**: 13 文件变更(85+/-)
- **密钥核查**: 所有 API Key 使用系统环境变量,无硬编码(.env 已排除)
- **工作空间核查**: 10 个 Agent 目录结构正常,7个核心.md文件已就位
- **Agent梦境同步**: 3 个 Agent DREAMS.md 及 11 个 dreams events.jsonl 同步(2026-07-17 夜间梦境)
- **运行状态**: ✅ 稳定版,推送 main 分支


### 版本 3.2.9 (2026-07-13)
- **每日自动同步 2026-07-13**: 18 文件变更(135+/-7)
- **密钥核查**: 所有 API Key 使用系统环境变量,无硬编码
- **工作空间核查**: 10 个 Agent 目录结构正常,7个核心.md文件已就位,DREAMS.md为系统自动生成
- **Agent梦境同步**: 10 个 Agent 的 DREAMS.md 及 dreams 记忆数据库同步(2026-07-12 夜间梦境)
- **steward MEMORY.md**: 记忆晋升 8 条
- **运行状态**: ✅ 稳定版,推送 main 分支


### 版本 3.2.8 (2026-07-12)
- **每日自动同步 2026-07-12**: 18 文件变更(166+/-16-)
- **密钥核查**: 所有 API Key 使用系统环境变量,无硬编码
- **工作空间核查**: 10 个 Agent 目录结构正常,7个核心.md文件已就位,DREAMS.md为系统自动生成
- **Agent梦境同步**: 9 个 Agent 的 DREAMS.md 及 dreams 记忆数据库同步(2026-07-11 夜间梦境)
- **steward MEMORY.md**: 记忆晋升 4 条(T001/T003/T004/T005)
- **运行状态**: ✅ 稳定版,推送 main 分支

### 版本 3.2.7 (2026-07-10)
- **每日自动同步 2026-07-10**: 18 文件变更(166+/-1-)
- **密钥核查**: 所有 API Key 使用系统环境变量,无硬编码
- **工作空间核查**: 10 个 Agent 目录结构正常,无 stray 文件
- **清理**: programmer/openclaw-workspace-state.json → temp/, steward/openclaw-workspace-state.json → temp/
- **Agent梦境同步**: 10 个 Agent 的 DREAMS.md 及 dreams 记忆数据库同步(2026-07-10 夜间梦境)
- **运行状态**: ✅ 稳定版,推送 main 分支

### 版本 3.2.6 (2026-07-08)
- **每日自动同步 2026-07-08**: 18 文件变更(199+/-2-)
- **密钥核查**: 所有 API Key 使用系统环境变量,无硬编码
- **工作空间核查**: 10 个 Agent 目录结构正常,无 stray 文件
- **Agent梦境同步**: 9 个 Agent 的 DREAMS.md 及 dreams 记忆数据库同步(2026-07-07 夜间梦境)
- **新增未追踪文件**: 2 个 Agent memory 文件 (auditor/steward/2026-07-07.md)
- **运行状态**: ✅ 稳定版,准备推送 main 分支

### 版本 3.2.5 (2026-07-07)
- **每日自动同步 2026-07-07**: 17 文件变更(142+/-24-)
- **密钥核查**: 所有 API Key 使用系统环境变量,无硬编码
- **工作空间核查**: 10 个 Agent 目录结构正常,无 stray 文件
- **清理**: programmer/openclaw-workspace-state.json → temp/
- **Agent梦境同步**: 10 个 Agent 的 DREAMS.md 及 dreams 记忆数据库同步(2026-07-06 夜间梦境)
- **steward MEMORY.md**: 记忆晋升 4 条(2026-07-02 会话精选)
- **新增未追踪文件**: 10 个 Agent memory/dreaming/light/rem/deep/2026-07-07.md
- **运行状态**: ✅ 稳定版,准备推送 main 分支

