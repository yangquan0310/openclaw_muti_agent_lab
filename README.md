# openclaw-agent-self-development

OpenClaw 插件 — Agent 自我发展框架

> **插件定位**：Hook 驱动的认知发展框架。在 Agent 执行任务的特定时机，通过 `skills/` 目录下的 skill 文档注入 Agent 的 system context，作为脚手架指导 Agent 行为。
>
> **核心原则**：插件只负责"提醒"（注入 skill），Agent 负责"执行"（自行决策、读写文件、管理任务空间）。
>
> **v3.0.0 重大变更**：重构为聚合 JSON 文件持久化（JSON），统一目录结构，新增 HookAdapter 生成标准 Hook 声明文件。适配器层保留核心 API 兼容接口（api 参数可为 null），当 OpenClaw 未来暴露对应 API 时可无缝切换。

---

## 认知发展理论基础

本框架的设计根植于三大认知科学理论，将人类认知机制映射为 Agent 的软件架构。

### 皮亚杰认知发展理论（Piaget）

皮亚杰认为认知发展通过 **同化（Assimilation）** 与 **顺应（Accommodation）** 的交替作用实现：

- **同化**：将新经验纳入现有认知图式。Agent 执行日常任务时，新经验被整合到既有技能体系（Skills 对象）和工作信念（Belief 对象）中。
- **顺应**：当新经验无法被现有图式容纳时，修改图式本身。Agent 遇到全新的任务类型或工作方式时，需要更新能力边界（Self 对象）、角色集（Identity 对象）甚至创建新的技能文档。
- **平衡（Equilibration）**：同化与顺应的动态平衡驱动认知发展。每一次 cron 触发的 Personality 模块正是这一机制的实现——通过回顾昨日事件（WorkingMemory.Event）、撰写发展日记（Diary 对象）、对比核心自我文件（SOUL.md / IDENTITY.md / MEMORY.md），判断当日经验属于同化还是顺应，并执行相应更新。

### Baddeley 工作记忆模型

Baddeley 将工作记忆分为 **语音环路**、**视觉空间画板**、**情景缓冲器** 与 **中央执行系统**。在 Agent 语境下映射为：

- **中央执行系统** → `WorkingMemoryModule`：协调任务空间的创建、复用、归档和销毁，管理注意力分配（同任务族复用 idle 空间，不同任务族并行）。
- **情景缓冲器** → `Session`（任务空间）：承载单个任务的完整上下文，是 Agent 执行特定任务时的"内存空间"。
- **长期记忆接口** → 文件系统持久化：completed 任务空间经 Event 聚合到 EventLog 后存入 `memory/` 目录，成为可回顾的长期记忆。

### Flavell 元认知理论

Flavell 将元认知定义为 **"对认知的认知"**，包含三个核心成分：

- **元认知知识** → `Plan` 对象：Agent 对"要做什么、用什么做、做到什么程度"的完整上下文理解，不只是步骤列表。
- **元认知监控** → `Deviation` 对象：每一轮 LLM 输出后，系统注入 monitoring skill，Agent 自行检查当前输出是否与 Plan 偏离。
- **元认知调节** → `Attribution` 对象：当 Deviation 检测到偏差时，Agent 自行生成调节方案（调整 phases、重新汇报、或跳过阶段并说明理由）。

**关键设计**：元认知不是插件替 Agent 做决策，而是插件在正确时机注入 skill 文档，Agent 阅读后自行执行监控与调节。

---

## 四层架构与权力边界

```
┌─────────────────────────────────────────────┐
│             用户层（User）                   │
│  · 下达任务需求（自然语言）                   │
│  · 审核代理制定的 Plan                        │
│  · 确认/修改/取消 Plan                        │
│  · 判断任务是否完成                           │
└─────────────────────────────────────────────┘
  ↑ 自然语言汇报          ↓ 自然语言指令
  ↑ Plan 状态/执行结果     ↓ 任务需求/确认反馈
  ↑ 任务完成报告           ↓ 审核意见
┌─────────────────────────────────────────────┐
│            代理层（Agent）                   │
│  · 接收用户任务，制定 Plan（含子任务分解、工具/技能、成功标准）
│  · 向用户汇报 Plan，等待审核                  │
│  · 审核通过后，在 Session（任务族）中推进执行 │
│  · 管理多个 Session，复用上下文               │
│  · 向插件层上报：Plan 状态、Session 状态      │
└─────────────────────────────────────────────┘
  ↑ skill 注入            ↓ 状态上报
  ↑ planning skill         ↓ Plan 状态
  ↑ monitoring skill        ↓ Session 状态
  ↑ 执行上下文提示          ↓ 执行结果
┌─────────────────────────────────────────┐
│              插件层（Plugin）            │
│  · 注册 Hook 事件处理器                   │
│  · 在事件触发时调用系统底层 API           │
│  · 接收代理层状态，写入系统底层            │
│  · 注入无可争议的流程/参数 skill           │
│                                          │
│  before_prompt_build → 注入 planning     │
│  llm_output          → 注入 monitoring   │
│  before_tool_call    → 记录 Session 创建 │
│  after_tool_call     → 记录事件/更新状态  │
│  agent_end           → 注入 working_memory│
└─────────────────────────────────────────┘
  ↑ Hook 事件触发         ↓ API 调用
  ↑ before_prompt_build   ↓ State.savePlan
  ↑ llm_output            ↓ State.saveDeviation
  ↑ agent_end             ↓ Memory.archiveSession
  ↑ cron 触发             ↓ Log.write
┌─────────────────────────────────────────┐
│           系统底层（文件系统）              │
│  · 提供 Hook 事件总线（Plugin api.on）    │
│  · 插件专属 聚合 JSON 文件持久化               │
│                                          │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐   │
│  │  Hook   │ │  Flow   │ │  State  │   │
│  │ (hooks/)│ │(flows/) │ │(state/) │   │
│  │ ├─────────┤ ├─────────┤ ├─────────┤ │
│  │ │before_  │ │ JSON   │ │ JSON   │ │
│  │ │prompt_  │ │ files  │ │ files  │ │
│  │ │build    │ │        │ │        │ │
│  │ │llm_     │ │        │ │        │ │
│  │ │output   │ │        │ │        │ │
│  │ │agent_   │ │        │ │        │ │
│  │ │end      │ │        │ │        │ │
│  │ └─────────┘ └─────────┘ └─────────┘ │
│  │ ┌─────────┐ ┌─────────┐            │
│  │ │ Memory  │ │  Log    │            │
│  │ │(memory/)│ │(logs/)  │            │
│  │ │ JSON    │ │ 文本/   │            │
│  │ │ files   │ │ JSONL   │            │
│  │ └─────────┘ └─────────┘            │
│  └───────────────────────────────────────┘
```

| 层级 | 权力边界 | 左侧输入 | 右侧输出 |
|------|---------|---------|---------|
| **用户层** | 任务所有者，拥有最终审核权和完成判定权 | 代理层的自然语言汇报、Plan 状态、执行结果 | 自然语言指令、确认反馈、审核意见 |
| **代理层** | 任务执行者，自行决策、制定 Plan、管理 Session | 插件层的 skill 注入、执行上下文 | Plan 状态、Session 状态、执行结果 |
| **插件层** | 工具层，只负责记录和注入无可争议的流程/参数 | 系统底层的 Hook 事件 | skill 文档、状态记录、API 调用 |
| **系统底层** | 基础设施，提供持久化、任务流、状态、记忆、日志 | 插件层的 API 调用 | Hook 事件、数据持久化 |

### 权力边界详解

**用户层（User）**
- ✅ 下达任务需求
- ✅ 审核代理制定的 Plan
- ✅ 确认/修改/取消 Plan
- ✅ 判断任务是否完成
- ❌ 不直接操作系统底层
- ❌ 不直接管理 Session

**代理层（Agent）**
- ✅ 接收用户任务，制定 Plan（含子任务分解、工具/技能、成功标准）
- ✅ 向用户汇报 Plan，等待审核
- ✅ 审核通过后，在 Session（任务族）中推进执行
- ✅ 管理多个 Session，复用上下文
- ✅ 向插件层上报状态
- ❌ 不直接读写系统底层（通过插件层）
- ❌ 不替用户做最终决策

**插件层（Plugin）**
- ✅ 注册 Plugin 生命周期事件处理器（api.on）
- ✅ 在事件触发时读写插件专属 聚合 JSON 文件
- ✅ 接收代理层状态，持久化到文件系统
- ✅ 注入无可争议的流程/参数 skill
- ❌ 不做业务决策
- ❌ 不替代理制定 Plan
- ❌ 只记录和传递，不判断

**系统底层（文件系统）**
- ✅ 提供 Plugin 事件总线（api.on）
- ✅ 插件专属目录结构（state/ flows/ memory/ logs/ hooks/）
- ✅ JSON / 文本 / JSONL 文件持久化
- ❌ 不做业务逻辑
- ❌ 不替代理或插件决策

### 数据流向

**双向流向（各层之间）**

| 方向 | 左侧输入（下层→上层） | 右侧输出（上层→下层） |
|------|----------------------|----------------------|
| 用户层 ↔ 代理层 | ↑ 自然语言汇报（Plan状态/执行结果） | ↓ 自然语言指令（任务需求/确认反馈） |
| 代理层 ↔ 插件层 | ↑ 状态上报（Deviation/Attribution/Event） | ↓ Skill注入（planning/monitoring/regulation/personality） |
| 插件层 ↔ 系统层 | ↑ 文件读写（State.save/Memory.query） | ↓ Plugin 事件触发（before_prompt_build/llm_output/agent_end） |

### 文件系统映射

| 存储类型 | 数据库路径 | 格式 | 插件层调用 | 用途 |
|----------|-----------|------|-----------|------|
| **Task** | `.openclaw/tasks/agent-self-development.json` | JSON | TaskAdapter | 任务创建、查询、管理 |
| **Flow** | `.openclaw/flows/agent-self-development.json` | JSON | FlowAdapter | 计划工作流、阶段推进、等待用户确认 |
| **State** | `.openclaw/state/agent-self-development.json` | JSON | StateAdapter | Plan/Session/Deviation/Attribution 状态 |
| **Memory** | `.openclaw/memory/agent-self-development.json` | JSON | MemoryAdapter | 归档、事件记录、历史查询 |
| **Log** | `.openclaw/logs/agent-self-development/` | 文本/JSONL | LogAdapter | 日志写入、读取、查询 |
| **Hook** | `.openclaw/hooks/agent-self-development/` | MD/TS | HookAdapter | Hook 声明文件（备案与 CLI 发现） |
| **Cron** | `.openclaw/cron/jobs.json` | JSON | CronAdapter | 定时任务注册 |

> **兼容性设计**：适配器构造函数接收 `(api, options)`，当 `api` 为 null 时回退到 JSON 文件。若未来 OpenClaw 暴露对应核心 API，传入真实 API 对象即可无缝切换，无需修改业务代码。

---

## v3.0.0 系统层重大变更

### 变更概览

| 组件 | v2.0.2（旧） | v3.0.0（新） | 变更原因 |
|------|-------------|-------------|---------|
| **Hook 机制** | 基础 Hook 支持 | 标准 Plugin 生命周期事件（api.on） | 规范事件注册、备案文件生成 |
| **Plan 存储** | 自研 聚合 JSON 文件 (`state/`) | 结构化 聚合 JSON 文件 (`state/agent-self-development/`) | 目录隔离、避免冲突 |
| **Session 追踪** | 内存 + JSON | 结构化 聚合 JSON 文件 (`state/agent-self-development/`) | 持久化、跨会话恢复 |
| **归档系统** | 自研 `memory_table:{日期}` | 结构化 聚合 JSON 文件 (`memory/agent-self-development/`) | 统一目录结构 |
| **状态管理** | `PluginState` 类（文件锁） | `StateAdapter`（文件系统 + 兼容接口） | 原子操作（单进程）、兼容未来核心 API |
| **应用Flow** | 自研 Plan 状态机 | `FlowAdapter`（文件系统 + 兼容接口） | 标准化 Flow 数据结构 |
| **日志系统** | 控制台输出 | `LogAdapter`（文本/JSONL 文件） | 结构化日志、查询、审计 |

### 新增组件

| 组件 | 职责 | 底层存储 | 兼容性 |
|------|------|---------|--------|
| `StateAdapter` | 状态存储适配器 | `state/agent-self-development/` (JSON文件) | 接口兼容核心 State API |
| `TaskAdapter` | 任务适配器 | `tasks/agent-self-development/` (JSON文件) | 接口兼容核心 Task API |
| `FlowAdapter` | 应用Flow适配器 | `flows/agent-self-development/` (JSON文件) | 接口兼容核心 Flow API |
| `MemoryAdapter` | 记忆存储适配器 | `memory/agent-self-development/` (JSON文件) | 接口兼容核心 Memory API |
| `LogAdapter` | 日志适配器 | `logs/agent-self-development/` (文本/JSONL) | 接口兼容核心 Log API |
| `HookAdapter` | Hook 文件生成器 | `hooks/agent-self-development/` (MD/TS) | 生成标准 Hook 声明文件 |
| `PlanManager` | Plan 业务逻辑 | State + Flow | `state/agent-self-development/` + `flows/agent-self-development/` |
| `SessionManager` | Session 业务逻辑 | State + Flow | `state/agent-self-development/` + `flows/agent-self-development/` |
| `ArchiveManager` | 归档业务逻辑 | Memory | `memory/{agentId}.json` |

### 系统层架构变化

**v2.0.2（旧架构）**：
```
OpenClaw 核心
    ├── Hook API（基础事件通知）
    ├── Flow（未使用）
    ├── State（未使用）
    ├── Memory（未使用）
    └── Log（未使用）

Plugin (Hook Handler)
    ├── MetacognitionModule
    │   └── 自研 Plan 状态机（JSON文件）
    ├── WorkingMemoryModule
    │   └── 自研 Session 管理（内存+JSON）
    └── PersonalityModule
        └── 自研 Archive 系统（memory_table）
```

**v3.0.0（新架构）**：
```
OpenClaw 核心
    ├── Plugin 事件总线（api.on）
    └── 适配器层（聚合 JSON 文件）

Plugin
    ├── MetacognitionModule
    │   └── PlanManager
    │       ├── StateAdapter → state/ (JSON)
    │       └── FlowAdapter → flows/ (JSON)
    ├── WorkingMemoryModule
    │   └── SessionManager
    │       ├── StateAdapter → state/ (JSON)
    │       └── FlowAdapter → flows/ (JSON)
    └── PersonalityModule
        └── EventManager / DiaryManager
            ├── MemoryAdapter → memory/ (JSON)
            └── LogAdapter → logs/ (文本/JSONL)
```

---

## 面向对象模型

框架由三个模块（Module）、一组适配器（Adapter）、一组管理器（Manager）和一组对象（Object）构成。

### 1. 适配器层（Adapter Layer）

隔离核心系统变化，提供统一接口。

| 适配器 | 核心方法 | 职责 | 底层存储 | 兼容性 |
|--------|---------|------|----------|--------|
| **StateAdapter** | `transaction()`, `savePlan()`, `getPlan()`, `saveSession()`, `getSession()`, `saveDeviation()`, `getDeviation()`, `saveAttribution()`, `getAttribution()` | Plan/Session/Deviation/Attribution 存储 | `state/agent-self-development/` (JSON文件) | 接口兼容核心 State API |
| **TaskAdapter** | `createTask()`, `getTask()`, `updateTask()`, `deleteTask()` | 任务创建、查询、更新、删除 | `tasks/agent-self-development/` (JSON文件) | 接口兼容核心 Task API |
| **FlowAdapter** | `createPlanFlow()`, `advancePhase()`, `waitForApproval()`, `getByRunId()` | 计划工作流、阶段推进、等待确认 | `flows/agent-self-development/` (JSON文件) | 接口兼容核心 Flow API |
| **MemoryAdapter** | `archiveSession()`, `logEvent()`, `queryHistory()` | 归档、事件记录、历史查询 | `memory/agent-self-development/` (JSON文件) | 接口兼容核心 Memory API |
| **LogAdapter** | `write()`, `read()`, `query()` | 日志写入、读取、查询 | `logs/agent-self-development/` (文本/JSONL) | 接口兼容核心 Log API |
| **HookAdapter** | `init()`, `updateEvents()`, `readMetadata()` | 生成标准 Hook 声明文件 | `hooks/agent-self-development/` (MD/TS) | 备案与 CLI 发现 |

### 2. 管理器层（Manager Layer）

实现业务逻辑，组合适配器。

| 管理器 | 核心方法 | 职责 |
|--------|---------|------|
| **PlanManager** | `createPlan()`, `approvePlan()`, `completePhase()` | 计划创建、用户确认、阶段推进 |
| **SessionManager** | `createSession()`, `releaseSession()`, `destroySession()` | 会话创建/复用、释放、销毁 |
| **DeviationManager** | `createDeviation()`, `acknowledgeDeviation()`, `resolveDeviation()` | 偏差检测、确认、解决 |
| **AttributionManager** | `createAttribution()`, `analyzeAttribution()`, `executeAttribution()` | 归因分析、调节方案生成与执行 |

### 3. 元认知模块（MetacognitionModule）

管理 **Plan / Deviation / Attribution** 的闭环。复杂任务时注入 planning skill，active 状态时注入 monitoring skill。

| 对象 | 职责 | 状态机 | 关联 |
|------|------|--------|------|
| **Plan** | 完整的任务上下文语境（目标/约束/工作空间/阶段化执行） | `draft → pending_approval → active → completed → destroyed` | 驱动 Session 创建，为 Deviation 提供参照 |
| **Deviation** | 记录代理对偏差的认知（预期 vs 实际 vs 差距） | `detected → acknowledged → resolved` | 引用 Plan.successCriteria，触发 Attribution |
| **Attribution** | 记录代理对偏差的归因（根因 + 调节方案） | `analyzing → completed → executed` | 引用 Deviation，修改 Plan 或 Session |

> **工作流详情**：见 `metacognition/planning/SKILL.md`（制定并汇报、处理确认、阶段化执行、任务空间管理）
> **工作流详情**：见 `metacognition/monitoring/SKILL.md`（偏差检测与认知）
> **工作流详情**：见 `metacognition/regulation/SKILL.md`（归因分析与调节）

#### **Plan 对象**

```json
{
  "runId": "uuid",
  "prompt": "用户原始输入",
  "status": "draft",
  "context": {
    "goal": "任务目标",
    "constraints": ["约束条件"],
    "successCriteria": ["成功标准：创建/修改哪些文档"]
  },
  "workspace": {
    "sessions": [],
    "artifacts": ["预期产出文档"],
    "tools": ["所用工具"],
    "skills": ["所用技能"]
  },
  "execution": {
    "phases": [
      {
        "id": "phase1",
        "name": "子任务名称",
        "goal": "子任务目标",
        "sessionId": "session:CODE:task-family",
        "taskFamily": "CODE",
        "tools": ["所需工具"],
        "skills": ["所需技能"],
        "outputs": ["产出文档"],
        "status": "pending"
      }
    ],
    "currentPhase": 0
  }
}
```

**Plan 状态转换规则**：

| 当前状态 | 触发条件 | 新状态 |
|----------|----------|--------|
| 不存在 | 收到复杂任务 | `draft` |
| `draft` | Agent 制定完成并汇报 | `pending_approval` |
| `pending_approval` | 用户确认 | `active` |
| `pending_approval` | 用户要求修改 | `pending_approval`（重新汇报） |
| `pending_approval` | 用户取消 | `completed` |
| `active` | 阶段正常推进 | `active`（currentPhase++） |
| `active` | 所有 phases 完成 | `completed` |
| `active` | 重大偏差需重规划 | `draft`（重新汇报） |
| `completed` | `agent_end` | `destroyed` |

#### **Deviation 对象**

```json
{
  "deviationId": "uuid",
  "runId": "uuid",
  "phaseId": "phase1",
  "status": "detected",
  "detectedAt": "ISO-8601 timestamp",
  "type": "scope_creep|tool_failure|logic_error|user_intervention|other",
  "expected": {
    "description": "预期行为/输出",
    "criteria": "引用的 Plan.successCriteria"
  },
  "actual": {
    "description": "实际行为/输出",
    "evidence": "截图/日志/输出片段"
  },
  "gap": {
    "description": "差距描述",
    "severity": "low|medium|high|critical"
  },
  "acknowledgedAt": "ISO-8601 timestamp|null",
  "resolvedAt": "ISO-8601 timestamp|null",
  "resolution": "解决方式描述|null"
}
```

**Deviation 状态转换规则**：

| 当前状态 | 触发条件 | 新状态 |
|----------|----------|--------|
| 不存在 | LLM 输出与 Plan 偏离 | `detected` |
| `detected` | Agent 确认偏差 | `acknowledged` |
| `acknowledged` | 执行 Attribution 调节方案 | `resolved` |

#### **Attribution 对象**

```json
{
  "attributionId": "uuid",
  "runId": "uuid",
  "deviationId": "uuid",
  "status": "analyzing",
  "createdAt": "ISO-8601 timestamp",
  "rootCause": {
    "category": "planning|execution|tool|skill|knowledge|other",
    "description": "根因分析",
    "evidence": "支持证据"
  },
  "adjustment": {
    "type": "modify_plan|skip_phase|create_session|update_criteria|other",
    "description": "调节方案描述",
    "targetId": "Plan.runId 或 Session.sessionId",
    "changes": {
      "phases": [],
      "artifacts": [],
      "tools": [],
      "skills": []
    }
  },
  "executedAt": "ISO-8601 timestamp|null",
  "result": "执行结果描述|null"
}
```

**Attribution 状态转换规则**：

| 当前状态 | 触发条件 | 新状态 |
|----------|----------|--------|
| 不存在 | Deviation 已确认 | `analyzing` |
| `analyzing` | 根因分析和调节方案完成 | `completed` |
| `completed` | 调节方案已执行 | `executed` |

### 4. 工作记忆模块（WorkingMemoryModule）

管理 **Session** 的全生命周期。任务空间跨 runId 复用，completed 归档，killed 销毁。

**Session 状态转换**：
```
不存在 → before_tool_call → pending → 开始执行 → active
  ├─ 正常完成 → completed → agent_end → 归档
  ├─ 工具报错 → killed → agent_end → 销毁
  └─ 主动暂停 → paused → 恢复 → active
```

**任务空间复用规则**：同一 `taskFamily`（CODE/RESEARCH/ANALYSIS/WRITING/TEST/DESIGN/TASK）的后续任务复用 idle 空间，标识格式 `session:{TYPE}:{任务族}`。

| 对象 | 职责 | 生命周期 | 持久化 |
|------|------|----------|--------|
| **Session** | 执行特定任务的内存空间 | `pending → active → completed/killed/paused`；completed 后 `idle`（可复用）；killed 后销毁 | `state:session:{sessionId}` |

> **工作流详情**：见 `working_memory/session/SKILL.md`（创建/监控/完成/终止）

#### **Session 对象**

```json
{
  "sessionId": "session:CODE:task-family",
  "taskFamily": "CODE",
  "status": "pending",
  "createdAt": "ISO-8601 timestamp",
  "activatedAt": "ISO-8601 timestamp|null",
  "completedAt": "ISO-8601 timestamp|null",
  "runIds": ["uuid"],
  "artifacts": ["产出文档路径"],
  "tools": ["使用过的工具"],
  "context": {
    "lastGoal": "最后执行的目标",
    "lastOutputs": ["最后产出"]
  }
}
```

**Session 状态转换规则**：

| 当前状态 | 触发条件 | 新状态 |
|----------|----------|--------|
| 不存在 | 需要新任务空间 | `pending` |
| `pending` | 开始执行 | `active` |
| `active` | 阶段完成 | `completed` |
| `completed` | agent_end | `idle`（可复用） |
| `active` | 工具报错 | `killed`（销毁） |
| `active` | 主动暂停 | `paused` |
| `paused` | 恢复执行 | `active` |

### 5. 人格模块（PersonalityModule）

基于皮亚杰同化/顺应理论，每日 cron 触发时驱动 Agent 回顾昨日事件、撰写发展日记、更新核心自我文件。

| 对象 | 职责 | 生命周期 | 持久化 |
|------|------|--------|--------|
| **Event** | 任务执行事件记录（计划/偏差/归因/工具/阶段/会话） | 单次事件，agent_end 时聚合到 EventLog | `state:event:{eventId}`（临时）→ 追加到 `memory:eventlog:{date}` |
| **Diary** | 撰写日记、提取更新触发信号 | `draft → reviewing → completed` | `memory:diary:{date}` |

| 子对象 | 职责 | 对应文件 |
|--------|------|----------|
| **Belief** | 工作信念与风格 | `SOUL.md` |
| **Self** | 能力边界与责任边界 | `MEMORY.md` |
| **Identity** | 角色集与社会身份 | `IDENTITY.md` |
| **Skills** | 个人技能体系 | `skills/README.md` |

#### **Event 对象**

```json
{
  "eventId": "uuid",
  "runId": "uuid",
  "type": "plan_created|phase_completed|deviation_detected|attribution_completed|tool_called|session_created|session_completed|other",
  "timestamp": "ISO-8601 timestamp",
  "actor": "Plan|Deviation|Attribution|Session|Tool",
  "action": "create|advance|detect|acknowledge|resolve|analyze|execute|complete|fail",
  "targetId": "受影响的对象ID",
  "details": {
    "description": "事件描述",
    "metadata": {}
  }
}
```

**Event 生命周期**：单次事件，agent_end 时聚合到 EventLog。

#### **Diary 对象**

```json
{
  "diaryId": "uuid",
  "date": "YYYY-MM-DD",
  "status": "draft",
  "createdAt": "ISO-8601 timestamp",
  "completedAt": "ISO-8601 timestamp|null",
  "reflection": {
    "events": ["昨日事件摘要"],
    "assimilation": ["同化内容：既有认知的细化"],
    "accommodation": ["顺应内容：新结构的发现"]
  },
  "signals": [
    {
      "type": "belief|self|identity|skills",
      "description": "变化信号描述",
      "confidence": "high|medium|low",
      "suggestedAction": "update|create|none"
    }
  ],
  "updates": {
    "belief": ["SOUL.md 更新内容"],
    "self": ["MEMORY.md 更新内容"],
    "identity": ["IDENTITY.md 更新内容"],
    "skills": ["skills/README.md 更新内容"]
  }
}
```

**Diary 状态转换规则**：

| 当前状态 | 触发条件 | 新状态 |
|----------|----------|--------|
| 不存在 | cron 触发每日回顾 | `draft` |
| `draft` | 撰写完成 | `reviewing` |
| `reviewing` | 信号提取和更新方案完成 | `completed` |

```
idle → cron 触发 → reflecting（Diary 撰写）
  → updating（对比核心自我，检测变化信号）
    ├── 自我认知变化 → Self 更新
    ├── 角色变化 → Identity 更新
    ├── 信念调整 → Belief 更新
    └── 技能变化 → Skills 更新
  → syncing → idle
```

**同化 vs 顺应判定**：
- **同化**：原有内容的细化 → 调用子对象的 update 方法
- **顺应**：新结构的出现 → 调用子对象的 create 方法

> **工作流详情**：见 `skills/personality/SKILL.md`（任务工作流六阶段闭环、每日同化与顺应）

### 6. 模块协作关系

```
Metacognition.Plan ──→ WorkingMemory.Session 创建/复用
Metacognition.Deviation ──→ WorkingMemory.Session 状态同步
Metacognition.Attribution ──→ WorkingMemory.Session 暂停/恢复

WorkingMemory.Session.completed ──→ 归档到 `memory/`（聚合 JSON 文件）
Personality.Event（任务执行事件）──→ EventLog（按日聚合）──→ Personality.Diary（每日回顾原料）
核心 `memory:eventlog:{date}`（已完成任务事件）──→ Personality（反思已完成任务）
```

---

## 系统层：Hook 注入映射

| Hook | 条件 | 注入 skill | 操作对象 | 文件系统交互 |
|------|------|------------|----------|-------------|
| `before_prompt_build` | 复杂任务 + Plan 不存在/draft | `planning` | Plan | State.savePlan() |
| `before_prompt_build` | Plan pending_approval | `planning` | Plan | Flow.waitForApproval() |
| `before_prompt_build` | Plan active | 执行上下文（当前阶段提醒） | Plan | State.getPlan() |
| `llm_output` | Plan active | `monitoring` | Deviation | State.saveDeviation() |
| `before_tool_call` | 会话工具调用 | —（仅记录） | Session | State.saveSession() |
| `after_tool_call` | 任意 | —（仅记录事件/状态） | Event | State.saveEvent() |
| `agent_end` | 任意 | `personality` | Event | State.events → Memory.eventlog |
| `before_prompt_build` | cron 消息 | `personality` | Diary | Memory.queryEventLog() |

---

## 技术实现

### 源码结构（按模块组织）

```
openclaw-agent-self-development/
├── openclaw.plugin.json          # 插件 manifest
├── package.json                  # npm 包配置（ESM）
├── HOOK.md                       # Hook 事件声明
├── README.md                     # 本文档
├── src/
│   ├── index.js                  # 插件入口：依赖注入，创建并注册三大模块 + 适配器 + 管理器
│   ├── metacognition/            # 元认知模块
│   │   ├── module.js             # MetacognitionModule（Plan/Deviation/Attribution 调度）
│   │   ├── plan-manager.js       # PlanManager（计划业务逻辑）
│   │   ├── deviation-manager.js  # DeviationManager（偏差认知业务逻辑）
│   │   ├── attribution-manager.js # AttributionManager（归因调节业务逻辑）
│   │   ├── planning/             # 计划 skill（文档+代码一体）
│   │   │   ├── SKILL.md          # Plan 对象操作指南
│   │   │   ├── plan-template.js  # Plan 模板与验证
│   │   │   └── plan-examples.js  # 示例 Plan（含子任务分解、工具、技能）
│   │   ├── monitoring/           # 偏差认知 skill
│   │   │   ├── SKILL.md          # Deviation 对象操作指南
│   │   │   └── deviation.js      # Deviation 对象实现
│   │   └── regulation/           # 归因调节 skill
│   │       ├── SKILL.md          # Attribution 对象操作指南
│   │       └── attribution.js    # Attribution 对象实现
│   ├── working-memory/           # 工作记忆模块
│   │   ├── module.js             # WorkingMemoryModule（Session 生命周期）
│   │   ├── session-manager.js    # SessionManager（会话业务逻辑）
│   │   ├── session/              # Session skill（文档+代码一体）
│   │   │   ├── SKILL.md          # Session 对象操作指南
│   │   │   ├── session-utils.js  # Session 工具函数
│   │   │   └── session-examples.js # 示例 Session 配置
│   ├── personality/              # 人格模块
│   │   ├── module.js             # PersonalityModule（Event/Diary 管理）
│   │   ├── event-manager.js      # EventManager（事件业务逻辑）
│   │   ├── diary-manager.js      # DiaryManager（日记业务逻辑）
│   │   ├── event/                # Event skill
│   │   │   ├── SKILL.md          # Event 对象操作指南
│   │   │   └── event-template.js # 事件模板
│   │   ├── diary/                # Diary skill
│   │   │   ├── SKILL.md          # Diary 对象操作指南
│   │   │   └── diary-template.js # 日记模板
│   │   ├── belief/               # Belief skill
│   │   │   ├── SKILL.md          # Belief 对象操作指南
│   │   │   └── belief-utils.js   # 信念更新工具
│   │   ├── self/                 # Self skill
│   │   │   ├── SKILL.md          # Self 对象操作指南
│   │   │   └── self-utils.js     # 自我认知工具
│   │   ├── identity/             # Identity skill
│   │   │   ├── SKILL.md          # Identity 对象操作指南
│   │   │   └── identity-utils.js # 身份更新工具
│   │   └── skills/               # Skills skill
│   │       ├── SKILL.md          # Skills 对象操作指南
│   │       └── skills-registry.js # 技能注册表
│   ├── common/                   # 公共组件
│   │   ├── adapters/             # JSON 适配器（兼容核心 API 接口）
│   │   │   ├── state-adapter.js  # StateAdapter
│   │   │   ├── task-adapter.js   # TaskAdapter
│   │   │   ├── flow-adapter.js   # FlowAdapter
│   │   │   ├── memory-adapter.js # MemoryAdapter
│   │   │   ├── log-adapter.js    # LogAdapter
│   │   │   └── hook-adapter.js   # HookAdapter（生成标准 Hook 声明文件）
│   │   │   └── cron-adapter.js   # CronAdapter（读写 jobs.json）
│   │   ├── skills-loader.js      # SkillLoader（带缓存）
│   │   ├── state.js              # PluginState（向后兼容，v2.x 迁移用）
│   │   └── utils.js              # 工具函数（日期、任务族推断）
│   └── _meta.json                # Skill 元数据索引
```

### 面向对象类设计

| 类 | 职责 | 方法 |
|---|------|------|
| `PluginState` | 聚合 JSON 文件状态管理（并发安全，向后兼容） | `get()`, `set()`, `append()`, `_persist()` |
| `SkillLoader` | Skill 文件加载与缓存 | `load()`, `clearCache()`, `getAvailableSkills()` |
| `StateAdapter` | 状态存储适配器（文件系统 + 兼容接口） | `transaction()`, `savePlan()`, `getPlan()`, `saveSession()`, `getSession()`, `saveDeviation()`, `getDeviation()`, `saveAttribution()`, `getAttribution()` |
| `TaskAdapter` | 任务适配器（文件系统 + 兼容接口） | `createTask()`, `getTask()`, `updateTask()`, `deleteTask()` |
| `FlowAdapter` | 应用Flow适配器（文件系统 + 兼容接口） | `createPlanFlow()`, `advancePhase()`, `waitForApproval()`, `getByRunId()` |
| `MemoryAdapter` | 记忆存储适配器（文件系统 + 兼容接口） | `archiveSession()`, `logEvent()`, `queryHistory()` |
| `LogAdapter` | 日志适配器（文件系统 + 兼容接口） | `write()`, `read()`, `query()` |
| `HookAdapter` | Hook 文件生成器 | `init()`, `updateEvents()`, `readMetadata()` |
| `PlanManager` | 计划业务逻辑 | `createPlan()`, `approvePlan()`, `completePhase()` |
| `DeviationManager` | 偏差认知业务逻辑 | `detectDeviation()`, `acknowledgeDeviation()`, `resolveDeviation()` |
| `AttributionManager` | 归因调节业务逻辑 | `analyzeAttribution()`, `applyAdjustment()`, `executePlan()` |
| `SessionManager` | 会话业务逻辑 | `createSession()`, `releaseSession()`, `destroySession()` |
| `EventManager` | 事件业务逻辑 | `recordEvent()`, `aggregateEvents()`, `queryEventLog()` |
| `DiaryManager` | 日记业务逻辑 | `createDiary()`, `reviewDiary()`, `extractSignals()` |
| `MetacognitionModule` | 元认知闭环调度 | `onBeforePromptBuild()`, `onLlmOutput()`, `onAgentEnd()` |
| `WorkingMemoryModule` | 任务空间生命周期管理 | `onBeforeToolCall()`, `onAfterToolCall()`, `onAgentEnd()` |
| `PersonalityModule` | 每日自我更新触发 | `onBeforePromptBuild()` |

### 状态存储键空间

| 键 | 类型 | 生命周期 | 说明 |
|----|------|----------|------|
| `plan:{runId}` | Plan | runId | 当前运行的 Plan（`state/`） |
| `deviation:{runId}:{phaseId}` | Deviation | runId | 当前运行的偏差记录（`state/`） |
| `attribution:{runId}:{deviationId}` | Attribution | runId | 当前运行的归因记录（`state/`） |
| `session:{TYPE}:{任务族}` | Session | 长期 | 任务族会话（`state/`） |
| `event:{eventId}` | Event | 临时 | 单次任务执行事件（`state/`）→ agent_end 聚合到 EventLog |
| `diary:{YYYY-MM-DD}` | Diary | 日期 | 每日发展日记（`memory/`） |
| `output:{runId}` | string | runId | Monitor 引用的最新 LLM 输出（`state/`） |
| `session_list:{runId}` | Session[] | runId | 本次运行的任务空间快照（`state/`） |
| `wm:{runId}:tools` | ToolRecord[] | runId | 本次运行的工具记录（`state/`） |
| `events:{YYYY-MM-DD}` | Event[] | 日期 | 按日累积的错误事件（`memory/`） |
| `memory_table:{YYYY-MM-DD}` | Archive[] | 日期 | 按日累积的 completed 归档（`memory/`，向后兼容） |
| `working_memory:active_sessions` | Session[] | 全局 | 全局活跃任务空间索引（`state/`） |
| `taskflow:{flowId}` | Flow | 长期 | Flow 实例（`flows/`） |
| `logs:{YYYY-MM-DD}` | LogEntry[] | 日期 | 按日累积的日志（`logs/`） |

---

## 安装

### 前置条件

- OpenClaw >= 2026.4.0
- Node.js >= 18
- `plugins.entries.agent-self-development.hooks.allowConversationAccess = true`

### 步骤

```bash
# 1. 安装插件
openclaw plugins install https://github.com/yangquan0310/openclaw_muti_agent_lab/releases/download/v3.0.0/openclaw-agent-self-development-3.0.0.tgz --force

# 2. 启用
openclaw plugins enable agent-self-development

# 3. 配置 cron（必需）
mkdir -p ~/.openclaw/cron
cat > ~/.openclaw/cron/jobs.json << 'EOF'
{
  "jobs": [
    {
      "id": "daily-self-update",
      "name": "每日自我更新",
      "schedule": "0 0 * * *",
      "timezone": "Asia/Shanghai",
      "message": "[cron:每日自我更新]",
      "enabled": true
    }
  ]
}
EOF

# 4. 编辑 ~/.openclaw/openclaw.json 配置 Agent 白名单与 hooks 权限

# 5. 重启 Gateway
openclaw gateway restart
```

### 配置示例

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "tools": { "alsoAllow": ["agent-self-development"] }
      }
    ]
  },
  "plugins": {
    "entries": {
      "agent-self-development": {
        "enabled": true,
        "hooks": { "allowConversationAccess": true },
        "config": {
          "metacognition": { "enabled": true, "planning": true, "monitoring": true },
          "workingMemory": { "enabled": true, "trackSubagents": true, "autoArchive": true },
          "personality": { "enabled": true }
        }
      }
    }
  }
}
```

### 配置项

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `metacognition.enabled` | boolean | `true` | 元认知模块总开关 |
| `metacognition.planning` | boolean | `true` | 计划阶段（draft → pending_approval → active） |
| `metacognition.monitoring` | boolean | `true` | 偏差认知阶段（仅 active 状态注入 monitoring） |
| `workingMemory.enabled` | boolean | `true` | 工作记忆模块总开关 |
| `workingMemory.trackSubagents` | boolean | `true` | 追踪任务空间创建/完成 |
| `workingMemory.autoArchive` | boolean | `true` | 任务结束后 Archive → Memory 归档 |
| `personality.enabled` | boolean | `true` | 人格模块总开关（cron 检测） |

> **向后兼容**：`config.assimilation` 仍可工作，内部映射到 `personality`