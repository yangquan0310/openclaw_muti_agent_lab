# OpenClaw 实验室多Agent智能协作系统

![OpenClaw](https://img.shields.io/badge/OpenClaw-2026.5.20-blue.svg)
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
| **大管家** | `ou_b341ae5dfcb556fe77beb1508f6d6ad5` | 文档管理、系统维护、任务调度 | 管理、维护、备份、同步、调度 |
| **程序员** | — | 代码开发、工具开发、系统优化、架构设计 | 开发、代码、脚本、工具、优化 |
| **数学家** | — | 统计分析、数学建模、算法实现 | 统计、建模、数据分析、计算、算法 |
| **物理学家** | — | 物理建模、理论推导、量化研究 | 建模、模拟、物理分析、理论推导 |
| **心理学家** | `ou_a0a0e824aa1959a64231872dce5cc775` | 理论审核、实验设计、结果解释 | 心理学、实验设计、理论分析、问卷设计 |
| **写作助手** | `ou_6286830776f65067c096418e0c42bc57` | 论文撰写、内容创作、文档编辑 | 写作、编辑、翻译、润色、文档生成 |
| **审稿助手** | `ou_1fe1fb30adbe8c90838ba3b8dbaee7f9` | 质量审查、格式规范、投稿建议 | 审稿、检查、格式、投稿、审查 |
| **审计员** | — | 教学质量审核、课件一致性检查 | 审计、检查、一致性、审核 |
| **讲师** | — | 教学辅助、课程材料整理 | 教学、课件、整理 |
| **呈现师** | `ou_990a093e6dc0a444c328747bcae11a77` | PPT设计与视觉呈现 | PPT、设计、呈现、视觉 |

> 注："—" 表示尚未在飞书群中配置 open_id

---

## 📁 仓库文件结构

### OpenClaw系统目录
```
.openclaw/                          # OpenClaw 根目录（Git仓库根目录）
├── README.md                          # 本说明文件（需同步更新）
├── .gitignore                         # Git忽略规则
├── .gitallowed                        # Git允许规则（secrets豁免）
├── requirements.txt                   # Python依赖文件
├── openclaw.json                      # OpenClaw主配置文件
├── cron/                              # 定时任务
│   ├── jobs.json                      # 任务列表
│   └── jobs-state.json                # 运行状态
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
├── wiki/                              # 知识库（全局共享）
│   ├── concepts/                      # 概念页面
│   ├── entities/                      # 实体页面
│   ├── sources/                       # 来源页面
│   ├── syntheses/                    # 综合分析页面
│   └── reports/                       # 报告页面
└── plugins/                           # 插件目录
```
## 📄 论文项目管理

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
    ├── agents/         # 决策存档
    ├── skills/         # 决策存档
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
7. 大管家归档版本 → temp/draft/ + 更新 metadata.json
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
| 备份文件 | 含 backup/备份/old/旧 | temp/draft/ |
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
python3 scripts/main.py search --queries queries.json --kb-path index.json
python3 scripts/main.py summarize --kb-path index.json
python3 scripts/main.py manage filter --kb-path index.json --output filtered.json
python3 scripts/main.py synthesize extract --notes notes.json

# 元数据维护
python3 scripts/maintainer/Maintainer.py ~/项目 update-kb
python3 scripts/maintainer/Maintainer.py ~/项目 save-version knowledge/review/综述.md
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
## 🤖 Agent自我发展插件(agent-self-development v4.2.0)

> 插件位置:`extensions/agent-self-development/`

> 源码仓库:`https://github.com/yangquan0310/agent-self-development`

> **核心原则**：用户领航 → Agent 执行 → 插件史官只记录（Plugin asks, Agent decides, Plugin records）

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
│           外部记忆（.agent/events/）      │
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
| **计划** | 任务启动前制定执行方案 | `.agent/tasks/{runId}.json` | 明确目标、约束、验收标准 |
| **偏差** | 实际执行与预期的差异 | `.agent/tasks/{runId}.json` | 记录执行中的偏离 |
| **归因** | 对偏差的分析与策略调整 | `.agent/tasks/{runId}.json` | 分析原因，更新 If-Then 规则 |

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
- **Git自动推送**: 每日凌晨 04:00 自动同步本地更改到 development 分支

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
- **Git自动推送**: 每日凌晨 04:00 自动同步本地更改到 development 分支

### 版本 4.2.2 (2026-05-16)
- **MiniMax 模型集成**: Steward 配置新增 minimax / minimax-cn / minimax-portal / minimax-portal-cn 四个 provider，支持 MiniMax-M2.7 及 MiniMax-M2.7-highspeed 模型（204.8K 上下文 / 131.072K 最大输出）
- **README更新**: 同步版本号、Agent 数量(7→10)、运行状态标签(运行中→稳定版)
- **Git自动推送**: 每日凌晨 04:00 自动同步本地更改到 development 分支

### 版本 4.2.1 (2026-05-16)
- **安全审计**: 扫描并确认当前待提交文件中无硬编码 API Key，所有密钥均使用系统变量引用
- **README更新**: 同步版本号、时间戳、运行状态
- **Git自动推送**: 每日凌晨 04:00 自动同步本地更改到 development 分支

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
- **Git自动推送**: 每日凌晨 04:00 自动同步本地更改到 development 分支

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
- **Git自动推送**：每日凌晨 04:00 自动同步本地更改到 development 分支

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
- **Git自动推送**：每日凌晨 04:00 自动同步本地更改到 development 分支

### 版本 4.1.3 (2026-05-13)
- **Cron任务通知调整**：Git自动推送任务的通知目标从实验室群(`oc_cd80162eb81e39f77160a0daab2a6ab8`)改为当前私聊(`ou_a4bc01a3736e458817235a94124d340c`)，便于个人接收任务执行状态
- **安全审计**：扫描并确认当前待提交文件中无硬编码 API Key，所有密钥均使用系统变量引用
- **README更新**：同步版本号、时间戳、运行状态
- **Git自动推送**：每日凌晨 04:00 自动同步本地更改到 development 分支

### 版本 4.1.2 (2026-05-13)
- **安全审计**：扫描并确认当前待提交文件中无硬编码 API Key，所有密钥均使用系统变量引用
- **README更新**：同步版本号、时间戳、运行状态
- **Git自动推送**：每日凌晨 04:00 自动同步本地更改到 development 分支

### 版本 4.1.2 (2026-05-13)
- **安全审计**：修复 `agents/programmer/agent/models.json`、`agents/main/agent/models.json`、`agents/instructor/agent/models.json` 中 6 处硬编码 API Key（3 处 Tencent Token Plan + 3 处 Kimi Code），分别替换为 `${TENCENTTOKENPLAN_API_KEY}` 和 `${KIMICODE_API_KEY}` 系统变量引用
- **README更新**：同步版本号、时间戳、运行状态
- **Git自动推送**：每日凌晨 04:00 自动同步本地更改到 development 分支

### 版本 4.1.1 (2026-05-12)
- **安全审计**：扫描并确认当前待提交文件中无硬编码 API Key，所有密钥均使用系统变量引用
- **README更新**：同步版本号、时间戳、运行状态
- **Git自动推送**：每日凌晨 04:00 自动同步本地更改到 development 分支

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
- **Git自动推送**:每日凌晨 04:00 自动同步本地更改到 development 分支

### 版本 3.4.1 (2026-05-10)
- **安全审计**:扫描并确认当前待提交文件中无硬编码 API Key,所有密钥均使用系统变量引用
- **Gitignore 加固**:显式添加 `credentials/`、`qqbot/data/credential-backup-*.json` 至 `.gitignore`
- **README更新**:同步版本号、时间戳、运行状态
- **Git自动推送**:每日凌晨 04:00 自动同步本地更改到 development 分支

### 版本 3.4.0 (2026-05-09)
- **agent-self-development 插件重构**:目录结构重组,新增 `agents/`、`docs/`、`skills/`、`test/reports/` 目录
- **安全审计**:扫描并修复 `workspace/skills/research-assistant/scripts/config.json` 中 3 处硬编码 API Key
- **各代理记忆日常更新**:所有 10 个代理的 `.dreams/` 记忆文件、events.jsonl、phase-signals.json 日常同步
- **README更新**:同步版本号、时间戳、运行状态
- **Git自动推送**:每日凌晨 04:00 自动同步本地更改到 development 分支

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
- **Git自动推送**:每日凌晨 04:00 自动同步本地更改到 development 分支

### 版本 3.3.0 (2026-05-06)
- **技能全局共享重构**:所有技能从 `workspace/skills/` 迁移至 `~/.openclaw/skills/`
- **Skill-developer v3.1.0**:升级为元技能混合结构
- **research-assistant v4.0.0**:重构为 Skill-developer v3.1.0 规范
- **cron 任务更新**:steward 每日仓库检查任务更新 CLI 入口
- **安全清理**:从所有代理 `tools.alsoAllow` 中移除误配的技能名称

### 版本 3.2.9 (2026-05-06)
- **安全审计**:扫描并替换 10 个 agents 的 models.json 中硬编码 API Key
- **README更新**:同步版本号、时间戳、运行状态
- **Git自动推送**:每日凌晨 04:00 自动同步本地更改到 development 分支

### 版本 3.2.8 (2026-05-05)
- **安全审计**:扫描并确认无硬编码 API Key
- **README更新**:同步版本号、时间戳、运行状态
- **Git自动推送**:每日凌晨 04:00 自动同步本地更改到 development 分支

### 版本 3.2.7 (2026-05-04)
### 版本 3.2.8 (2026-05-18)
- **模型配置升级**: 新增 Kimi Code 系列模型(kimi-for-coding, kimi-code, k2p5)
- **上下文窗口扩展**: DeepSeek V4 Flash 从 256K 扩展至 1M
- **MiniMax 更新**: M2.5 → M2.7, 新增 VL-01 视觉模型, maxTokens 扩展至 25600
- **工作空间清理**: steward/ 目录 LaTeX 中间文件移至 temp/
- **pixel-office 优化**: EditorToolbar 组件、layoutSerializer、spriteCache 精简
- **Git自动推送**: 每日 04:00 自动同步 development 分支
- **安全审计**:扫描并确认无硬编码 API Key
- **README更新**:同步版本号、时间戳、运行状态
- **Git自动推送**:每日凌晨 04:00 自动同步本地更改到 development 分支

### 版本 3.2.6 (2026-05-03)
- **安全审计**:扫描并确认无硬编码 API Key
- **README更新**:同步版本号、时间戳、运行状态
- **Git自动推送**:每日凌晨 04:00 自动同步本地更改到 development 分支

### 版本 3.2.4 (2026-04-28)
- **安全审计**:扫描并确认无硬编码 API Key
- **README更新**:同步版本号、时间戳、运行状态
- **Git自动推送**:每日凌晨 04:00 自动同步本地更改到 development 分支

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

**最后更新: 2026-05-25 04:00:00**
**系统版本**: OpenClaw 2026.5.22
**插件版本**: agent-self-development v4.3.1
**运行状态**: ✅ 稳定版
**备份状态**: ✅ 自动执行中
