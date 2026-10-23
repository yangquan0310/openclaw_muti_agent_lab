# OpenClaw 实验室多Agent智能协作系统

![OpenClaw](https://img.shields.io/badge/OpenClaw-2026.7.20-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Agents](https://img.shields.io/badge/Agents-8%20个-orange.svg)
![Skills](https://img.shields.io/badge/Skills-20%2B-yellow.svg)
![Status](https://img.shields.io/badge/Status-稳定版-success.svg)

---

## 👥 实验室成员(研究团队)

整个系统围绕**实验室科研**展开,由 **8 个 Agent** 组成:

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
| 呈现师Agent | 科研可视化 | 科研图表、论文 figure、poster、报告 pptx |

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
| **审计员** | ~~已删除（2026-08-04 v8.52.0）~~ | ~~审计、检查、一致性、审核~~ |
| **讲师** | ~~已删除（2026-08-04 v8.52.0）~~ | ~~教学、课件、整理~~ |
| **呈现师** | 科研图表、论文 figure、poster、报告 pptx | 可视化、图表、figure、poster |

---

## 📁 仓库文件结构

### OpenClaw系统目录
```
.openclaw/                          # OpenClaw 根目录（Git仓库根目录）
├── README.md                          # 本说明文件（需同步更新）
├── .gitignore                         # Git忽略规则
├── requirements.txt                   # Python依赖文件
├── openclaw.json                      # OpenClaw主配置文件
├── workspace/                         # Agent工作空间（8个）
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
│   └── presenter/                     # 呈现师（科研可视化师）
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

> 仅保留最近 5 次变更；完整历史见 git log --oneline -- README.md。

### 版本 3.7.34 (2026-10-24)
- **每日自动同步 2026-10-24**: 1 文件变更(35+/-1335-)，README 结构重组（正文前置，变更日志移至文末并收敛为最近 5 版）
- **密钥核查**: 精确扫描待推送内容(diff,35 新增行)及全部已跟踪文件,匹配 sk-/ghp_/github_pat_/AKIA/xox/AIza/PRIVATE KEY/api_key/secret/token 等模式,未发现任何硬编码 API Key/密钥 ✅;.env 与 gateway.systemd.env 已被 .gitignore 排除,未跟踪
- **工作空间核查**: 9 个 agent 顶层仅含核心 .md 配置(AGENTS/DREAMS/IDENTITY/MEMORY/SOUL/USER,除 main 外均含 HEARTBEAT)+标准目录(temp/memory/.agents;steward 另含 .clawhub/ideas/scripts/skills,psychologist/writer/steward 含 media);无杂散中间/解析/一次性文件,无未跟踪文件,无需移入 temp
- **运行状态**: ✅ 稳定版,推送 main 分支(development 分支已于 2026-06-12 删除)

### 版本 3.7.33 (2026-10-22)
- **每日自动同步 2026-10-22**: 1 文件变更(11+/-0-)
- **密钥核查**: 精确扫描待推送内容(diff origin/main..工作区,11 新增行)及全部已跟踪文件,匹配 sk-/ghp_/github_pat_/AKIA/xox/AIza/PRIVATE KEY/api_key/secret/token 等模式,未发现任何硬编码 API Key/密钥 ✅;.env 与 gateway.systemd.env 已被 .gitignore 排除,未跟踪
- **工作空间核查**: 9 个 agent 顶层仅含核心 .md 配置(AGENTS/DREAMS/IDENTITY/MEMORY/SOUL/USER,除 main 外均含 HEARTBEAT)+标准目录(temp/memory/.agents;main 无 HEARTBEAT/.agents 系 2026-10-01 系统迁移遗留;steward 另含 .clawhub/ideas/scripts/skills,psychologist/writer/steward 含 media);无杂散中间/解析/一次性文件,无未跟踪文件,无需移入 temp
- **Agent梦境同步**: steward 的 DREAMS.md 更新(2026-10-22 凌晨梦境记录)
- **运行状态**: ✅ 稳定版,推送 main 分支(development 分支已于 2026-06-12 删除)

### 版本 3.7.32 (2026-10-21)
- **每日自动同步 2026-10-21**: 1 文件变更(7+/-0-)
- **密钥核查**: 精确扫描待推送内容(diff origin/main..工作区,7 新增行)及全部已跟踪文件,匹配 sk-/ghp_/github_pat_/AKIA/xox/AIza/PRIVATE KEY/api_key/secret/token 等模式,未发现任何硬编码 API Key/密钥 ✅;.env 与 gateway.systemd.env 已被 .gitignore 排除,未跟踪
- **工作空间核查**: 9 个 agent 顶层仅含核心 .md 配置(AGENTS/DREAMS/IDENTITY/MEMORY/SOUL/USER,除 main 外均含 HEARTBEAT)+标准目录(temp/memory/.agents;main 无 HEARTBEAT/.agents 系 2026-10-01 系统迁移遗留;steward 另含 .clawhub/ideas/scripts/skills,psychologist/writer/steward 含 media);无杂散中间/解析/一次性文件,无未跟踪文件,无需移入 temp
- **Agent梦境同步**: steward 的 DREAMS.md 更新(2026-10-21 凌晨梦境记录)
- **运行状态**: ✅ 稳定版,推送 main 分支(development 分支已于 2026-06-12 删除)

### 版本 3.7.31 (2026-10-20)
- **每日自动同步 2026-10-20**: 1 文件变更(14+/-0-)
- **密钥核查**: 精确扫描待推送内容(diff origin/main..工作区,14 新增行)及全部已跟踪文件,匹配 sk-/ghp_/github_pat_/AKIA/xox/AIza/PRIVATE KEY/api_key/secret/token 等模式,未发现任何硬编码 API Key/密钥 ✅;.env 与 gateway.systemd.env 已被 .gitignore 排除,未跟踪
- **工作空间核查**: 9 个 agent 顶层仅含核心 .md 配置(AGENTS/DREAMS/IDENTITY/MEMORY/SOUL/USER,除 main 外均含 HEARTBEAT)+标准目录(temp/memory/.agents;main 无 HEARTBEAT/.agents 系 2026-10-01 系统迁移遗留;steward 另含 .clawhub/ideas/scripts/skills,psychologist/writer/steward 含 media);无杂散中间/解析/一次性文件,无未跟踪文件,无需移入 temp
- **Agent梦境同步**: steward 的 DREAMS.md 更新(2026-10-20 凌晨梦境记录)
- **运行状态**: ✅ 稳定版,推送 main 分支(development 分支已于 2026-06-12 删除)

### 版本 3.7.30 (2026-10-19)
- **每日自动同步 2026-10-19**: 3 文件变更(15+/-0-)
- **密钥核查**: 精确扫描待推送内容(diff origin/main..工作区,15 新增行)及全部已跟踪文件,匹配 sk-/ghp_/github_pat_/AKIA/xox/AIza/PRIVATE KEY/api_key/secret/token 等模式,未发现任何硬编码 API Key/密钥 ✅;.env 与 gateway.systemd.env 已被 .gitignore 排除,未跟踪
- **工作空间核查**: 9 个 agent 顶层仅含核心 .md 配置(AGENTS/DREAMS/IDENTITY/MEMORY/SOUL/USER,除 main 外均含 HEARTBEAT)+标准目录(temp/memory/.agents;main 无 HEARTBEAT/.agents 系 2026-10-01 系统迁移遗留;steward 另含 .clawhub/ideas/scripts/skills,psychologist/writer/steward 含 media);无杂散中间/解析/一次性文件,无未跟踪文件,无需移入 temp
- **Agent梦境同步**: physicist/reviewer 的 DREAMS.md 深睡记录更新(recall 存储修复);steward 的 DREAMS.md 更新(2026-10-19 凌晨梦境记录)
- **运行状态**: ✅ 稳定版,推送 main 分支(development 分支已于 2026-06-12 删除)

## 📄 许可证

本项目遵循 MIT 许可证,详见 LICENSE 文件。

---

## 👨‍💻 维护者

- **杨权** - 系统架构、实验室负责人
- **大管家Agent** - 自动维护、系统监控

---

**最后更新: October 24, 2026 05:00 (GMT+8)**
**系统版本**: OpenClaw 2026.7.1-2
**Git 分支**: main（development 分支已于 2026-06-12 删除）
**运行状态**: ✅ 稳定版
**备份状态**: ✅ 自动执行中
