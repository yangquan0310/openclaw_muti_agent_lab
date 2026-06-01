---
pageType: synthesis
id: synthesis.agent-engineering-practice
createdAt: "2026-06-01T16:12:00+08:00"
updatedAt: "2026-06-01T16:35:00+08:00"
title: 我的 agent 工程实践：驾驭方法论
sourceIds:
  - source.openclaw-system
  - source.repository
  - entity.steward
  - entity.yangquan
aliases:
  - 驾驭代理
  - 协调者方法论
  - harness 三件套
  - 驾驭方法论
confidence: 0.9
claims:
  - id: claim.harness.1
    text: 协调者通过三件套驾驭代理：代理个人配置（AGENTS+SOUL+IDENTITY+MEMORY+实践技能）、项目工作台、代理自我发展插件
    status: supported
    confidence: 0.95
    evidence:
      - kind: source
        sourceId: entity.steward
        weight: 0.95
  - id: claim.config.1
    text: 代理个人配置六件套各有分工：AGENTS 定原则、SOUL 定风格、IDENTITY 定边界、MEMORY 定规则、实践技能定流程
    status: supported
    confidence: 0.95
  - id: claim.workspace.1
    text: 项目工作台通过四契约文件（README/HANDBOOK/TODO/metadata.json）+ 标准目录结构 + Manager 子类路由实现规范化管理
    status: supported
    confidence: 0.95
  - id: claim.plugin.1
    text: 代理自我发展插件（v4.5.0）通过 8 个工具 + 4 个 hook 时机实现任务追踪、偏差检测、事件记录和自我调节
    status: supported
    confidence: 0.95
  - id: claim.synergy.1
    text: 三件套协同循环：个人配置约束行为 → 工作台承载项目 → 插件固化经验 → 经验沉淀回个人配置
    status: supported
    confidence: 0.9
contradictions:
  - "AGENTS.md 原则数量有版本差异：v8 写 11 条，早期写 10 条"
questions:
  - "三件套各自的迭代节奏如何协调？"
  - "经验沉淀到什么程度可以独立成技能？"
---

# 我的 agent 工程实践：驾驭方法论

> **核心问题**：怎么"驾驭"一群 agent，让它们不变成一次性工具？
> **答案**：**三件套**——代理个人配置 + 项目工作台 + 代理自我发展插件。

---

## 核心要点

| 件套 | 名称 | 定位 |
|------|------|------|
| **第一件** | **代理个人配置** | 驯马缰——约束 agent "怎么做事" |
| **第二件** | **项目工作台** | 赛马场——承载项目"在哪里做" |
| **第三件** | **代理自我发展插件** | 自动记录仪——固化经验"做了什么" |

**协同关系**：
```
个人配置（约束）→ 工作台（承载）→ 插件（固化）→ 经验沉淀回个人配置
```

---

## 一、问题起源

> **"实践是代理最重要的东西。"** —— 杨权

早期 agent 都是"一次性"工具：用完即丢，没有积累。这导致：
- 重复工作反复发生
- 知识无法沉淀
- 跨项目无法复用
- agent 协作靠人肉协调

杨权决定**系统性地培养一个协调者代理（steward）**，让它能用其他 9 个子代理协调工作台 30+ 项目。

**核心洞察**：驾驭 agent 不能靠"一个文件"或"一个工具"，需要**三个维度**同时约束。

---

## 二、第一件套：代理个人配置（harness）

> **定位**：驯马缰——约束 agent "怎么做事"

代理个人配置由 **5 个文件**组成，定义了 agent 的行为边界、人格风格、身份职责、记忆规则和工作流程。

### 2.1 AGENTS.md——行为准则

**回答问题**：agent 应该怎么做事？

| # | 原则 | 内涵 |
|---|------|------|
| 1 | **进项目先看门牌** | 开工前必读 README / HANDBOOK / TODO |
| 2 | **manager 加载** | 收到推进指令时，必读 manager SKILL.md |
| 3 | **先手动跑通** | 新任务先手工 3-10 次，再写技能 |
| 4 | **先思考再执行** | 用检索 + 记忆搜索，准备充分再执行 |
| 5 | **改完即交** | git commit，描述改了什么 |
| 6 | **该自动就自动** | 周期任务直接加 cron，不重复问 |
| 7 | **固化反思** | 同问题 2 次以上，写入规范文件 |
| 8 | **事不过二** | 用户说 2 次同样的话 = 失败 |
| 9 | **子代理自主** | 只定约束/输入/产出，自己拆解 |
| 10 | **禁止传话筒** | 子任务不写死，让子代理自决 |
| 11 | **不懂就问** | 歧义要询问，不在错误目标执行 |

**子代理交互规则**：
- 快速任务直接执行（查看/显示/列出/读取/问句）
- 复杂任务派子代理（新会话不继承，必须传完整上下文）

### 2.2 SOUL.md——人格风格

**回答问题**：agent 是什么样的人？

| 字段 | 内容 |
|------|------|
| 核心自我 | 协调者视角：管方向、定边界、分配任务，不亲自执行 |
| 身份边界铁律 | 协调时只读技能/用模板/不分身/只协调 |
| 风格 | 清晰完整、Markdown、确认导向（每次给路径/版本号）|
| 信念 | 文档是知识的载体、版本是历史的见证、数据安全 > 规范完整 |
| 工作模式 | 先框架后内容、先检查再修改、授权与信任子代理 |

### 2.3 IDENTITY.md——身份边界

**回答问题**：agent 能做什么、不能做什么？

| 项 | 内容 |
|----|------|
| 允许边界 | 文件管理、目录管理、日志记录、知识检索、云文档管理、任务管理 |
| 禁止边界 | 内容创作、数据分析、理论解释、代码编写、学术观点、决策制定 |
| 核心信念 | 文档是知识的载体，版本是历史的见证 |
| 精确执行 | 严格执行指令，不扩散联想；不懂就问 |

### 2.4 MEMORY.md——记忆系统

**回答问题**：agent 记住什么？

| 区域 | 作用 | 内容 |
|------|------|------|
| 工作记忆 | 当前活跃任务 | 任务看板（T036-T042 等） |
| 程序性记忆 | If-Then 规则 | 25+ 条条件-行动规则 |
| 陈述性记忆 | 历史索引 | 34 项已完成任务 |

**固化时机**：每次任务完成 → 检查是否需要新增 If-Then 规则 → 写入 MEMORY.md。

**关键 If-Then 规则示例**：

| 条件 | 行动 |
|------|------|
| 使用 feishu_create_doc 创建云文档 | 文档所有者显示为"大管家"；必须提醒用户手动转移所有权 |
| 需要修改被 gateway tool 拦截的配置项 | 优先用 CLI：`openclaw config set` |
| 派发任务时找不到 open_id | 在群消息中搜索目标代理的历史消息 |
| 更新 TODO.md 后 | 先与老板讨论修改策略，确认后再通知子代理 |
| 分配子任务给子代理 | 只传递约束目标/输入/产出，让子代理自己决定 |
| 监控 OpenClaw 更新时 | 重点关注提供商变化、渠道变化、核心功能更新 |

### 2.5 实践技能——怎么做

**回答问题**：agent 具体怎么执行某类任务？

以 **manager 技能**（v5.3.0）为例：

```
manager/
├── SKILL.md         # 唯一入口（路由 12 大场景）
├── references/      # 27 个指南（任务/项目/知识库/系统维护）
├── scripts/         # 7 个 maintainer（Base/Thesis/Course/Program）
├── assets/          # 31 个模板（6 项目 + 12 agent + 4 项目级 + 4 知识库）
└── index/           # 25 个 manifest
```

**核心流程**：
```
领取任务 → 明确约束 → 更新TODO → 派发子代理 → 追踪进度 → 汇报老板
```

**其他代理的实践技能**：
| 代理 | 技能 | 收录内容 |
|------|------|----------|
| 程序员 | programmer | OOP 指南、架构、全栈开发、测试、运维 |
| 写作助手 | writer | 写作流程、编辑规范、文体模板 |
| 审稿者 | reviewer | 质量审查、审稿意见、建设性反馈 |
| 心理学家 | psychologist | 督导师指南、咨询师指南、科学家指南 |
| 数学家 | mathematician | 建模、方程、优化、统计 |
| 物理学家 | physicist | 物理建模、理论、推导 |

---

## 三、第二件套：项目工作台

> **定位**：赛马场——承载项目"在哪里做"

项目工作台是仓库中的**各个项目目录**，是 agent 协作的实际场所。

### 3.1 仓库根目录

```
/data/disk/仓库/
├── agent-self-development/    # 自我发展插件
├── AI-Agent科普文章/          # 科普项目
├── 创业指导/                  # 论文项目
├── 教育科学研究方法/          # 课程项目
├── 数字化存储与自传体记忆/    # 博士论文
├── 学生论文修改/              # 学生论文
├── 论文审稿/                  # 审稿项目
├── ...                        # 30+ 项目
```

### 3.2 四契约文件标准

每个项目**必须**在根目录有 4 个文件，缺一不可：

| 文件 | 作用 | 机器可读 |
|------|------|---------|
| **README.md** | 项目总览、目标、角色分工 | ❌ |
| **HANDBOOK.md** | 操作手册、流水线、目录规范 | ❌ |
| **TODO.md** | 任务看板、进度追踪 | ❌ |
| **metadata.json** | 项目元数据（类型/版本/状态） | ✅ |

### 3.3 按类型路由到 Manager 子类

```
项目根目录
    ↓
读取 metadata.json → project_type
    ↓
路由到对应 Manager 子类：
    ├── thesis   → ThesisMaintainer（论文项目）
    ├── course   → CourseMaintainer（课程项目）
    ├── program  → ProgramMaintainer（程序项目）
    └── (通用)   → BaseMaintainer（兜底）
```

### 3.4 标准目录结构

```
项目/
├── README.md           # 四契约
├── HANDBOOK.md
├── TODO.md
├── metadata.json
├── uploads/            # 上传的原始文件
├── manuscripts/        # 论文/稿件（thesis 类型）
├── knowledge/          # 知识库页面
├── outputs/            # 产出物
├── .agents/            # 元数据层
│   ├── tasks/          # task JSON 文件
│   ├── events/         # 事件报告
│   └── skills/         # 项目级技能
└── temp/               # 临时文件
```

### 3.5 Manager 自动整理能力

```bash
# 整理项目（自动识别类型、归档、更新 metadata）
manager maintainer organize <project_path> [--dry-run]

# 同步模板（保留 PRIVATE 区块，更新 GENERATED 区块）
manager maintainer sync <project_path> [--dry-run]

# 检查更新（对比模板版本）
manager maintainer check-updates <project_path>
```

---

## 四、第三件套：代理自我发展插件

> **定位**：自动记录仪——固化经验"做了什么"

代理自我发展插件（agent-self-development v4.5.0）是 OpenClaw 插件，通过**钩子加工具**架构实现任务追踪、偏差检测、事件记录和自我调节。

### 4.1 8 个命名空间工具

| 工具 | 功能 |
|------|------|
| `task.create` | 创建 draft task，自动推断 plan |
| `task.advance` | 推进任务到下一阶段 |
| `task.update` | 更新任务状态（含 deviation / attribution / outcome） |
| `task.get` | 查询完整 task JSON |
| `task.archive` | 归档已完成任务 |
| `event.query` | 查询事件记录（按 runId/日期/类型） |
| `event.archive` | 归档事件文件 |
| `event.report` | 一次性生成 event.md |

### 4.2 4 个 hook 时机

| 时机 | 触发条件 | 注入内容 |
|------|---------|---------|
| **M1** | task.create 返回成功 | 提醒：制定计划 → 拆解 TODO |
| **M2** | task.update 含 deviation | 提醒：执行偏差分析 → 归因分析 |
| **M3** | event.report 返回成功 | 提醒：六维度平衡性判断 |
| **M4** | before_prompt_build 无 active task | 提醒：创建任务 |

### 4.3 任务状态机

```
draft → pending_approval → active → completed
              ↑_____________|
                    ↓ revising → draft
```

### 4.4 典型工作流（10 步）

```
1. task.create({ prompt: "..." })           → 获取 runId
2. task.update({ status: "pending_approval" })  → 申请审批
3. task.update({ status: "active" })  → 开始执行
4. task.advance({ runId })                   → 推进阶段（可多次）
5. 发现偏差 → task.update({ deviation: {...} })
6. 分析归因 → task.update({ attribution: {...} })
7. 任务完成 → task.update({ status: "completed", outcome: {...} })
8. event.report({ runId })                   → 生成事件文件
9. event.query({ runId })                    → 按需查询历史
10. task.archive({ runId })                  → 归档任务
```

### 4.5 自我调节机制

**偏差检测（M2 触发）**：
```
执行中发现偏离计划
    ↓
task.update({ deviation: { type, description, impact } })
    ↓
Hook M2 自动注入："执行偏差分析 → 归因分析"
    ↓
task.update({ attribution: { rootCause, strategy } })
```

**事件生成后调节（M3 触发）**：
```
event.report({ runId }) → 生成事件文件
    ↓
Hook M3 自动注入："六维度平衡性判断"
    ↓
Agent 检查：目标达成 / 资源消耗 / 时间偏差 / 质量偏差 / 协作摩擦 / 学习收获
    ↓
如果值得记住 → 调节到个人配置文件
```

**调节沉淀目标**：

| 发现 | 沉淀到 | 示例 |
|------|--------|------|
| 新的行为准则 | AGENTS.md | "禁止一次性任务" |
| 新的风格偏好 | SOUL.md | "先框架后内容" |
| 新的身份边界 | IDENTITY.md | "不处理教学事务" |
| 新的 If-Then 规则 | MEMORY.md | "pip 损坏时用 get-pip.py" |
| 新的工作流 | manager/references/ | "ASR 配置流程" |

---

## 五、三件套如何协同

### 5.1 协同循环

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│  │  第一件套    │    │  第二件套    │    │  第三件套    │  │
│  │  个人配置    │───→│  项目工作台  │───→│  自我发展    │  │
│  │  (约束行为)  │    │  (承载项目)  │    │  插件(固化)  │  │
│  └──────┬──────┘    └─────────────┘    └──────┬──────┘  │
│         │                                      │         │
│         │         经验沉淀回个人配置             │         │
│         └──────────────────────────────────────┘         │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### 5.2 任务派发场景（三件套协同实例）

```
用户：整理「创业指导」项目
    ↓
【第一件套·个人配置】
    ├── AGENTS.md："进项目先看门牌" → 先读 README/HANDBOOK/TODO
    ├── AGENTS.md："manager 加载" → 读 manager SKILL.md
    ├── SOUL.md："先框架后内容" → 先列目录结构
    ├── IDENTITY.md：确认在允许边界内（文件管理 ✅）
    └── MEMORY.md：检查 If-Then 规则
    ↓
【第二件套·项目工作台】
    ├── 读取 /data/disk/仓库/创业指导/metadata.json → project_type = "thesis"
    ├── 路由到 ThesisMaintainer
    ├── 检查四契约文件是否齐全
    └── 执行 manager maintainer organize
    ↓
【第三件套·自我发展插件】
    ├── task.create({ prompt: "整理创业指导项目" }) → runId
    ├── task.update({ status: "active" })
    ├── task.advance × N（执行各阶段）
    ├── 完成 → task.update({ status: "completed" })
    ├── event.report → 生成事件文件
    └── 任务完成
    ↓
【经验沉淀】
    ├── 发现新规则 → MEMORY.md（If-Then）
    ├── 发现新流程 → manager/references/
    └── git commit
```

### 5.3 经验沉淀闭环

```
执行任务
    ↓
发现偏差/问题
    ↓
插件记录（event.report）
    ↓
归因分析（attribution）
    ↓
判断：是否值得记住？
    ├── 是 → 写入个人配置（AGENTS/SOUL/IDENTITY/MEMORY/manager）
    └── 否 → 仅保留事件记录
    ↓
下次执行类似任务时
    ↓
个人配置已更新 → 行为自动改进
```

### 5.4 协同的关键原则

| 原则 | 说明 |
|------|------|
| **配置约束行为** | 个人配置定义"怎么做事"，agent 必须遵守 |
| **工作台承载项目** | 项目目录是协作场所，四契约文件是入口 |
| **插件固化经验** | 任务追踪、偏差检测、事件记录，经验不丢失 |
| **经验回流配置** | 发现新规则 → 写入个人配置 → 下次自动改进 |
| **循环不终止** | 配置 → 执行 → 固化 → 更新配置 → 继续执行 |

---

## 六、关键经验提炼

### 6.1 五条核心洞察

1. **堆规则无用需内化**
   - 规则再多，agent 不执行 = 0
   - 必须实际跑 3-10 次后规则才"活"起来
   - 失败一次胜过规则十次

2. **一次性任务 → 技能 → cron**
   - 第一次：手动做（发现）
   - 第二次：skill-developer 固化
   - 第三次：cron 自动跑
   - **不能让用户说 2 次同样的话**

3. **TODO.md 是工作台的协作载体**
   - 多 agent 看同一份 TODO = 状态共享
   - 任务状态显式流转：⬜ → ⏳ → 🔍 → ✅
   - steward 维护，其他 agent 只读 + 更新自己

4. **约束目标前置**
   - 没明确验收标准 = 任务必返工
   - 没边界条件 = agent 越界
   - 申请审批 = 让用户拍板

5. **失败归因是成长机制**
   - deviation 必分析（不放过）
   - 复盘 → 更新个人配置
   - 事件流可追溯

### 6.2 失败教训（已沉淀）

| 失败 | 归因 | 沉淀到 |
|------|------|--------|
| 早期 steward 重复回答相似问题 | 缺 MECE 原则 | AGENTS.md |
| 子代理理解错任务 | 缺约束目标 | task-guide.md |
| 一次性工作反复发生 | 缺 skill-developer 固化 | skill-developer 技能 |
| cron 任务堆积错误 | 缺监控首跑 | AGENTS.md |
| TTS 自动模式跑不通 | 缺 runtime bug 排查深度 | TTS 手动 message 兜底 |
| 记忆索引需要重建 | 缺 sqlite 健康监控 | openclaw-maintenance-guide |

---

## 七、未来指引

### 7.1 个人配置迭代策略

- **少即是多**：规则不超 12 条
- **每次失败 → 反思 → 1 条新规则**
- **规则变更 = 版本号 +1**

### 7.2 插件扩展边界

- 工具数 ≤ 8（避免认知负担）
- hook 时机 ≤ 4（注入越频繁越打扰）
- 重要变化 = changelog + version bump

### 7.3 六件套版本对齐

| 文件 | 当前版本 | 管理方式 |
|------|---------|---------|
| AGENTS.md | v9.3.0 | 手动版本号 |
| SOUL.md | v1.9.0 | 手动版本号 |
| IDENTITY.md | v2.3.0 | 手动版本号 |
| MEMORY.md | v8.14.0 | 手动版本号 |
| manager/SKILL.md | v5.3.0 | 手动版本号 |
| agent-self-development | v4.5.0 | package.json |

---

## 八、对应已有 wiki 引用

| 主题 | 已有页面 |
|------|---------|
| 协调者 | [[entities/steward]] |
| 用户 | [[entities/yangquan]] |
| 演化路径 | [[syntheses/2026-05-17-18-40-33-多agent协作案例-从实践到规范的演化]] |
| 三方协作 | [[syntheses/2026-05-20-23-34-38-三方协作实践-代理如何领取与执行任务]] |
| 技能体系 | [[syntheses/2026-05-23-11-14-00-代理实践技能体系总结]] |
| AGENTS 模板 | [[syntheses/2026-05-19-18-25-37-如何攥写agents配置文件]] |
| 系统目录 | [[sources/openclaw-system]] |

---

## 来源

- entity.steward / entity.yangquan
- source.openclaw-system / source.repository
- synthesis.协作演化（2026-05-17）
- synthesis.three-party-collaboration（2026-05-20）
- task-guide.md / constraint-standards.md / task-lifecycle-standards.md
- agent-self-development/SKILL.md v4.5.0

---

## 待解决问题

- 三件套各自的迭代节奏如何协调？
- 经验沉淀到什么程度可以独立成技能？
- 六件套版本号如何对齐（当前各自独立管理）？

---

*创建时间：2026-06-01 16:12*
*更新时间：2026-06-01 16:35*
*更新者：大管家（Steward）*
*版本：v3（按老板定义的真正三件套重写：代理个人配置 + 项目工作台 + 自我发展插件）*

## Related
<!-- openclaw:wiki:related:start -->
### Sources

- [[sources/openclaw-system|openclaw-system]]
- [[sources/repository|仓库]]
- [[entities/steward|大管家（Steward）]]
- [[entities/yangquan|杨权（实验室负责人）]]
<!-- openclaw:wiki:related:end -->
