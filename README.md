# openclaw-agent-self-development

OpenClaw 插件 — Agent 自我发展框架（深度集成版）

> **插件定位**：Hook 驱动的认知发展框架。在 Agent 执行任务的特定时机，通过 `skills/` 目录下的 skill 文档注入 Agent 的 system context，作为脚手架指导 Agent 行为。
>
> **核心原则**：插件只负责"提醒"（注入 skill），Agent 负责"执行"（自行决策、读写文件、管理任务空间）。
>
> **v3.0.0 重大变更**：深度集成 OpenClaw 核心系统（TaskFlow、Memory、State），从自研 JSON 文件迁移到核心 SQLite 持久化，实现跨会话恢复、并发安全和系统级状态管理。

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
- **长期记忆接口** → `Memory` 对象：completed 任务空间经归档（Archive）后存入核心 Memory 系统，成为可回顾的长期记忆。

### Flavell 元认知理论

Flavell 将元认知定义为 **"对认知的认知"**，包含三个核心成分：

- **元认知知识** → `Plan` 对象：Agent 对"要做什么、用什么做、做到什么程度"的完整上下文理解，不只是步骤列表。
- **元认知监控** → `Monitor` 对象：每一轮 LLM 输出后，系统注入 monitoring skill，Agent 自行检查当前输出是否与 Plan 偏离。
- **元认知调节** → `Regulator` 对象：当 Monitor 检测到偏差时，Agent 自行生成调节方案（调整 phases、重新汇报、或跳过阶段并说明理由）。

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
  ↑ before_prompt_build   ↓ TaskFlow.create
  ↑ llm_output            ↓ State.set
  ↑ agent_end             ↓ Memory.archive
  ↑ cron 触发             ↓ Log.write
┌─────────────────────────────────────────┐
│           系统底层（Core System）         │
│  · 提供 Hook 事件总线                     │
│  · 提供 TaskFlow / State / Memory / Log   │
│                                          │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐   │
│  │  Hook   │ │TaskFlow │ │  State  │   │
│  │ (hooks/)│ │(tasks/) │ │(state/) │   │
│  │ ├─────────┤ ├─────────┤ ├─────────┤ │
│  │ │before_  │ │ create  │ │ get/set │ │
│  │ │prompt_  │ │ advance │ │ trans-  │ │
│  │ │build    │ │ phase   │ │ action  │ │
│  │ │llm_     │ │ setWait │ │         │ │
│  │ │output   │ │         │ │         │ │
│  │ │agent_   │ │         │ │         │ │
│  │ │end      │ │         │ │         │ │
│  │ └─────────┘ └─────────┘ └─────────┘ │
│  │ ┌─────────┐ ┌─────────┐            │
│  │ │ Memory  │ │  Log    │            │
│  │ │(memory/)│ │(logs/)  │            │
│  │ │ archive │ │ write   │            │
│  │ │ query   │ │ read    │            │
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
- ✅ 注册 Hook 事件处理器
- ✅ 在事件触发时调用系统底层 API
- ✅ 接收代理层状态，写入系统底层
- ✅ 注入无可争议的流程/参数 skill
- ❌ 不做业务决策
- ❌ 不替代理制定 Plan
- ❌ 只记录和传递，不判断

**系统底层（Core System）**
- ✅ 提供 Hook 事件总线
- ✅ 提供 TaskFlow / State / Memory / Log API
- ✅ 数据持久化、事务支持、并发安全
- ❌ 不做业务逻辑
- ❌ 不替代理或插件决策

### 数据流向

**下行流向（用户 → 代理 → 插件 → 系统）**
1. 用户下达任务需求 → 代理接收
2. 代理制定 Plan → 向用户汇报
3. 用户审核通过 → 代理开始执行
4. 代理上报状态 → 插件接收
5. 插件调用 API → 系统底层记录

**上行流向（系统 → 插件 → 代理 → 用户）**
1. 系统触发 Hook 事件 → 插件接收
2. 插件注入 skill → 代理接收
3. 代理执行后汇报 → 用户查看
4. 系统返回状态 → 插件读取 → 代理使用

### 核心系统 API 映射

| 核心系统 | API 路径 | 插件层调用 | 用途 |
|----------|---------|-----------|------|
| **TaskFlow** | `api.runtime.tasks.flow` | TaskFlowAdapter | 计划工作流、阶段推进、等待用户确认 |
| **State** | `api.runtime.state` | StateAdapter | 原子存储、事务、Plan/Session 状态 |
| **Memory** | `api.runtime.memory` | MemoryAdapter | 归档、事件记录、历史查询 |
| **Log** | `api.runtime.log` | LogAdapter | 日志写入、读取、查询 |
| **Hook** | `api.runtime.hooks` | HookManager | 事件注册、触发、路由 |
| **Session** | `api.runtime.sessions` | SessionManager | 会话创建、复用、销毁（按任务族） |

---

## v3.0.0 系统层重大变更

### 变更概览

| 组件 | v2.0.2（旧） | v3.0.0（新） | 变更原因 |
|------|-------------|-------------|---------|
| **Hook 机制** | 基础 Hook 支持 | 核心系统 Hook API (`hooks/`) | 标准化事件系统、插件可注册自定义 Hook |
| **Plan 存储** | 自研 JSON 文件 (`state/`) | 核心 TaskFlow (`tasks/`) | 持久化、跨会话恢复 |
| **Session 追踪** | 内存 + JSON | 核心 State API (`state/`) | 并发安全、事务支持 |
| **归档系统** | 自研 `memory_table:{日期}` | 核心 Memory API (`memory/`) | 统一记忆管理、跨插件共享 |
| **状态管理** | `PluginState` 类（文件锁） | 核心 State 事务 | 原子操作、版本控制 |
| **任务流** | 自研 Plan 状态机 | 核心 TaskFlow | 标准持久化、断点续传 |
| **日志系统** | 控制台输出 | 核心 Log API (`logs/`) | 结构化日志、查询、审计 |

### 新增组件

| 组件 | 职责 | 依赖核心系统 |
|------|------|-------------|
| `StateAdapter` | 状态存储适配器 | `api.runtime.state` |
| `TaskFlowAdapter` | 任务流适配器 | `api.runtime.tasks.flow` |
| `MemoryAdapter` | 记忆存储适配器 | `api.runtime.memory` |
| `LogAdapter` | 日志适配器 | `api.runtime.log` |
| `PlanManager` | Plan 业务逻辑 | State + TaskFlow |
| `SessionManager` | Session 业务逻辑 | State + TaskFlow |
| `ArchiveManager` | 归档业务逻辑 | Memory |

### 系统层架构变化

**v2.0.2（旧架构）**：
```
核心系统层
    ├── Hook API（基础事件通知）
    ├── TaskFlow（未使用）
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
核心系统层
    ├── Hook API（事件路由）← 插件注册 Handler
    ├── TaskFlow（计划工作流）← PlanManager 调用
    ├── State（原子存储）← StateAdapter 封装
    ├── Memory（长期记忆）← MemoryAdapter 封装
    ├── Log（结构化日志）← LogAdapter 封装
    └── Session（会话管理）← SessionManager 调用

Plugin (Hook Handler)
    ├── MetacognitionModule
    │   └── PlanManager
    │       ├── StateAdapter → 核心 State API
    │       └── TaskFlowAdapter → 核心 TaskFlow
    ├── WorkingMemoryModule
    │   └── SessionManager
    │       ├── StateAdapter → 核心 State API
    │       ├── TaskFlowAdapter → 核心 TaskFlow
    │       └── SessionManager → 核心 Session API
    └── PersonalityModule
        └── ArchiveManager
            ├── MemoryAdapter → 核心 Memory API
            └── LogAdapter → 核心 Log API
```

---

## 面向对象模型

框架由三个模块（Module）、一组适配器（Adapter）、一组管理器（Manager）和一组对象（Object）构成。

### 适配器层（Adapter Layer）

隔离核心系统变化，提供统一接口。

#### StateAdapter（状态适配器）

```typescript
class StateAdapter {
  private state: CoreStateAPI;
  
  constructor(stateAPI: CoreStateAPI) {
    this.state = stateAPI;
  }
  
  // 原子操作
  async transaction<T>(operations: (tx: StateTransaction) => Promise<T>): Promise<T> {
    return this.state.transaction(operations);
  }
  
  // Plan 存储
  async savePlan(runId: string, plan: Plan): Promise<void> {
    await this.state.set(`plan:${runId}`, plan);
  }
  
  async getPlan(runId: string): Promise<Plan | null> {
    return this.state.get(`plan:${runId}`);
  }
  
  // Session 存储
  async saveSession(sessionId: string, session: Session): Promise<void> {
    await this.state.set(`session:${sessionId}`, session);
  }
  
  async getSession(sessionId: string): Promise<Session | null> {
    return this.state.get(`session:${sessionId}`);
  }
}
```

#### TaskFlowAdapter（任务流适配器）

```typescript
class TaskFlowAdapter {
  private taskFlow: CoreTaskFlowAPI;
  
  constructor(taskFlowAPI: CoreTaskFlowAPI) {
    this.taskFlow = taskFlowAPI;
  }
  
  // 创建计划工作流
  async createPlanFlow(plan: Plan): Promise<Flow> {
    return this.taskFlow.createManaged({
      controllerId: "agent-self-development/planning",
      goal: plan.context.goal,
      currentStep: "draft",
      stateJson: {
        plan: plan,
        phases: plan.execution.phases,
        currentPhase: 0,
        status: "draft"
      }
    });
  }
  
  // 推进阶段
  async advancePhase(flowId: string, phase: Phase): Promise<void> {
    const flow = await this.taskFlow.get(flowId);
    await this.taskFlow.update({
      flowId,
      expectedRevision: flow.revision,
      currentStep: phase.id,
      stateJson: {
        ...flow.stateJson,
        currentPhase: flow.stateJson.currentPhase + 1
      }
    });
  }
  
  // 等待用户确认
  async waitForApproval(flowId: string): Promise<void> {
    const flow = await this.taskFlow.get(flowId);
    await this.taskFlow.setWaiting({
      flowId,
      expectedRevision: flow.revision,
      currentStep: "pending_approval",
      waitJson: { kind: "user_confirm", reason: "Plan pending approval" }
    });
  }
}
```

#### MemoryAdapter（记忆适配器）

```typescript
class MemoryAdapter {
  private memory: CoreMemoryAPI;
  
  constructor(memoryAPI: CoreMemoryAPI) {
    this.memory = memoryAPI;
  }
  
  // 归档 Session
  async archiveSession(session: Session): Promise<void> {
    await this.memory.archive({
      type: "session",
      data: session,
      tags: [session.status, session.taskFamily],
      date: new Date()
    });
  }
  
  // 记录事件
  async logEvent(event: Event): Promise<void> {
    await this.memory.archive({
      type: "event",
      data: event,
      tags: [event.type, event.severity],
      date: new Date()
    });
  }
  
  // 查询历史
  async queryHistory(options: QueryOptions): Promise<Archive[]> {
    return this.memory.query({
      type: options.type,
      tags: options.tags,
      dateRange: options.dateRange
    });
  }
}
```

### 管理器层（Manager Layer）

实现业务逻辑，组合适配器。

#### PlanManager（计划管理器）

```typescript
class PlanManager {
  private state: StateAdapter;
  private taskFlow: TaskFlowAdapter;
  
  constructor(state: StateAdapter, taskFlow: TaskFlowAdapter) {
    this.state = state;
    this.taskFlow = taskFlow;
  }
  
  // 创建计划（双写：State + TaskFlow）
  async createPlan(prompt: string): Promise<Plan> {
    const plan = new Plan({
      runId: generateUUID(),
      prompt,
      status: "draft",
      context: { goal: "", constraints: [], successCriteria: [] },
      execution: { phases: [], currentPhase: 0 }
    });
    
    await this.state.savePlan(plan.runId, plan);
    await this.taskFlow.createPlanFlow(plan);
    
    return plan;
  }
  
  // 用户确认
  async approvePlan(runId: string): Promise<void> {
    const plan = await this.state.getPlan(runId);
    if (!plan) throw new Error("Plan not found");
    
    plan.status = "active";
    await this.state.savePlan(runId, plan);
    
    const flow = await this.taskFlow.getByRunId(runId);
    await this.taskFlow.advancePhase(flow.flowId, plan.execution.phases[0]);
  }
  
  // 阶段完成
  async completePhase(runId: string, phaseIndex: number): Promise<void> {
    const plan = await this.state.getPlan(runId);
    if (!plan) throw new Error("Plan not found");
    
    plan.execution.phases[phaseIndex].status = "completed";
    plan.execution.currentPhase = phaseIndex + 1;
    
    await this.state.savePlan(runId, plan);
    
    if (plan.execution.currentPhase >= plan.execution.phases.length) {
      plan.status = "completed";
      await this.state.savePlan(runId, plan);
    } else {
      const nextPhase = plan.execution.phases[plan.execution.currentPhase];
      const flow = await this.taskFlow.getByRunId(runId);
      await this.taskFlow.advancePhase(flow.flowId, nextPhase);
    }
  }
}
```

#### SessionManager（会话管理器）

```typescript
class SessionManager {
  private state: StateAdapter;
  private taskFlow: TaskFlowAdapter;
  private sessionAPI: CoreSessionAPI;
  
  constructor(state: StateAdapter, taskFlow: TaskFlowAdapter, sessionAPI: CoreSessionAPI) {
    this.state = state;
    this.taskFlow = taskFlow;
    this.sessionAPI = sessionAPI;
  }
  
  // 创建/复用任务空间（按任务族）
  async createSession(phase: Phase, taskFamily: string): Promise<Session> {
    const sessionId = `session:${taskFamily}:${taskFamily}`;
    
    // 1. 检查核心系统 Session API
    const existingSession = await this.sessionAPI.get(sessionId);
    if (existingSession && existingSession.status === "idle") {
      existingSession.status = "active";
      await this.sessionAPI.update(sessionId, existingSession);
      return existingSession;
    }
    
    // 2. 检查 State 中的记录
    const existing = await this.state.getSession(sessionId);
    if (existing && existing.status === "idle") {
      existing.status = "active";
      await this.state.saveSession(sessionId, existing);
      return existing;
    }
    
    // 3. 创建新 Session
    const session = new Session({
      id: sessionId,
      taskFamily,
      status: "active",
      createdAt: Date.now()
    });
    
    // 4. 双写：State + Session API
    await this.state.saveSession(sessionId, session);
    await this.sessionAPI.create(sessionId, session);
    
    // 5. 关联 TaskFlow
    const flow = await this.taskFlow.getByPhase(phase.id);
    await this.taskFlow.runSubtask(flow.flowId, phase);
    
    return session;
  }
  
  // 释放 Session（标记为 idle，可复用）
  async releaseSession(sessionId: string): Promise<void> {
    const session = await this.state.getSession(sessionId);
    if (session) {
      session.status = "idle";
      await this.state.saveSession(sessionId, session);
      await this.sessionAPI.update(sessionId, { status: "idle" });
    }
  }
  
  // 销毁 Session（killed 后清理）
  async destroySession(sessionId: string): Promise<void> {
    await this.state.saveSession(sessionId, null);
    await this.sessionAPI.destroy(sessionId);
  }
}
```

#### ArchiveManager（归档管理器）

```typescript
class ArchiveManager {
  private memory: MemoryAdapter;
  
  constructor(memory: MemoryAdapter) {
    this.memory = memory;
  }
  
  async archivePlan(plan: Plan): Promise<void> {
    await this.memory.archiveSession({
      type: "plan",
      data: plan,
      tags: [plan.status, "plan"],
      date: new Date()
    });
  }
  
  async dailySummary(date: Date): Promise<DailySummary> {
    const archives = await this.memory.queryHistory({
      type: "session",
      dateRange: [startOfDay(date), endOfDay(date)]
    });
    
    return {
      date,
      totalSessions: archives.length,
      completedSessions: archives.filter(a => a.data.status === "completed").length,
      failedSessions: archives.filter(a => a.data.status === "killed").length,
      items: archives
    };
  }
}
```

### 元认知模块（MetacognitionModule）

管理 **Plan / Monitor / Regulator** 的闭环。复杂任务时注入 planning skill，active 状态时注入 monitoring skill。

**Plan 对象**（Agent 通过 skill 了解完整属性，见 `metacognition/planning/SKILL.md`）：

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

**核心原则**：`draft` 必须汇报，`pending_approval` 必须等待用户确认，只有 `active` 才能执行。

| 对象 | 职责 | 状态机 | 关联 |
|------|------|--------|------|
| **Plan** | 完整的任务上下文语境（目标/约束/工作空间/阶段化执行） | `draft → pending_approval → active → completed → destroyed` | 驱动 Session 创建，为 Monitor 提供参照 |
| **Monitor** | 跟踪 LLM 输出与 Plan 的偏离程度 | `idle → tracking → alert → destroyed` | 引用 Plan，触发 Regulator |
| **Regulator** | 接收偏差报告，生成并执行调节方案 | `idle → analyzing → executing → completed → destroyed` | 修改 Plan 或回到 draft 重新汇报 |

> **工作流详情**：见 `metacognition/planning/SKILL.md`（制定并汇报、处理确认、阶段化执行、任务空间管理）

### 工作记忆模块（WorkingMemoryModule）

管理 **Session / Event / Archive / Memory** 的全生命周期。任务空间跨 runId 复用，completed 归档，killed 销毁。

**Session 状态转换**：
```
不存在 → before_tool_call → pending → 开始执行 → active
  ├─ 正常完成 → completed → agent_end → Archive → Memory + idle
  ├─ 工具报错 → killed → agent_end → 销毁
  └─ 主动暂停 → paused → 恢复 → active
```

**任务空间复用规则**：同一 `taskFamily`（CODE/RESEARCH/ANALYSIS/WRITING/TEST/DESIGN/TASK）的后续任务复用 idle 空间，标识格式 `session:{TYPE}:{任务族}`。

| 对象 | 职责 | 生命周期 | 持久化 |
|------|------|----------|--------|
| **Session** | 执行特定任务的内存空间 | `pending → active → completed/killed/paused`；completed 后 `idle`（可复用）；killed 后销毁 | `session_list:{runId}`（运行级） `working_memory:active_sessions`（全局索引） |
| **Event** | 工具调用错误记录 | 按日累积 | 核心 Memory API (`memory/`) |
| **ToolRecord** | 工具调用创建/完成记录 | runId 级 | `wm:{runId}:tools` |
| **Archive** | completed Session 的归档记录 | 日期级 | 核心 Memory API (`memory/`) |
| **Memory** | 按日聚合的归档记录集合 | 长期保留 | 核心 Memory API (`memory/`) |

> **工作流详情**：见 `working_memory/session/SKILL.md`（创建/监控/完成/终止）和 `working_memory/memory/SKILL.md`（归档/清理）

### 人格模块（PersonalityModule）

基于皮亚杰同化/顺应理论，每日 cron 触发时驱动 Agent 回顾昨日事件、撰写发展日记、更新核心自我文件。

| 对象 | 职责 | 对应文件 |
|------|------|----------|
| **Personality** | 容器，驱动每日更新流程 | — |
| **Diary** | 撰写日记、提取更新触发信号 | `diary/YYYY-MM-DD.md` |
| **Belief** | 工作信念与风格 | `SOUL.md` |
| **Self** | 能力边界与责任边界 | `MEMORY.md` |
| **Identity** | 角色集与社会身份 | `IDENTITY.md` |
| **Skills** | 个人技能体系 | `skills/README.md` |

**Personality 生命周期**：
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

### 模块协作关系

```
Metacognition.Plan ──→ WorkingMemory.Session 创建/复用
Metacognition.Monitor ──→ WorkingMemory.Session 状态同步
Metacognition.Regulator ──→ WorkingMemory.Session 暂停/恢复

WorkingMemory.Session.completed ──→ ArchiveManager.archiveSession() ──→ 核心 Memory API
WorkingMemory.Event ──→ Personality.Diary（每日回顾）
核心 Memory.archives ──→ Personality（反思已完成任务）
```

---

## 系统层：Hook 注入映射

| Hook | 条件 | 注入 skill | 操作对象 | 核心系统交互 |
|------|------|------------|----------|-------------|
| `before_prompt_build` | 复杂任务 + Plan 不存在/draft | `planning` | Plan | TaskFlow.createManaged() |
| `before_prompt_build` | Plan pending_approval | `planning` | Plan | TaskFlow.setWaiting() |
| `before_prompt_build` | Plan active | 执行上下文（当前阶段提醒） | Plan | TaskFlow.get() |
| `llm_output` | Plan active | `monitoring` | Monitor | State.getPlan() |
| `before_tool_call` | 会话工具调用 | —（仅记录） | Session | State.saveSession() |
| `after_tool_call` | 任意 | —（仅记录错误/状态） | Event / Session | Memory.logEvent() |
| `agent_end` | 任意 | `working_memory` | Memory | ArchiveManager.archivePlan() |
| `before_prompt_build` | cron 消息 | `personality` | Personality | Memory.queryHistory() |

---

## 职责边界

| 职责 | 用户层 | 代理层 | 插件层 | 系统底层 |
|------|--------|--------|--------|----------|
| 下达任务 | ✅ | — | — | — |
| 审核 Plan | ✅ | — | — | — |
| 确认/修改 Plan | ✅ | — | — | — |
| 判断任务完成 | ✅ | — | — | — |
| 制定 Plan（含子任务分解、工具/技能、成功标准） | — | ✅ 阅读 skill 自行制定 | ✅ 注入 planning skill | ✅ 提供 TaskFlow API |
| 汇报 Plan | — | ✅ | — | — |
| 执行监控 | — | ✅ 阅读 skill 自行检查 | ✅ 注入 monitoring skill | ✅ 提供 State API |
| 管理 Session（任务族） | — | ✅ 自行决定复用/创建 | ✅ 记录状态变更 | ✅ 提供 State API |
| 每日自我更新 | — | ✅ 阅读 skill 自行写日记 | ✅ 注入 personality skill | ✅ 提供 Memory API |
| 核心文件读写 | — | ✅ 自行读写 | ✅ 不碰 | ✅ 不碰 |
| 定时任务 | — | — | ✅ 不内置定时器（用户配置 OpenClaw cron） | ✅ 提供 cron 基础设施 |
| 状态记录 | — | ✅ 上报状态 | ✅ 接收并写入系统 | ✅ 提供持久化 |
| 流程注入 | — | ✅ 接收并执行 | ✅ 注入无可争议的流程 | ✅ 提供 Hook 机制 |

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
│   │   ├── module.js             # MetacognitionModule（Plan/Monitor/Regulator 调度）
│   │   ├── plan-manager.js       # PlanManager（计划业务逻辑）
│   │   ├── state-adapter.js      # StateAdapter（状态存储适配）
│   │   ├── taskflow-adapter.js   # TaskFlowAdapter（任务流适配）
│   │   └── planning/             # 计划 skill（文档+代码一体）
│   │       ├── SKILL.md          # Plan 对象操作指南
│   │       ├── plan-template.js  # Plan 模板与验证
│   │       └── plan-examples.js  # 示例 Plan（含子任务分解、工具、技能）
│   ├── working-memory/           # 工作记忆模块
│   │   ├── module.js             # WorkingMemoryModule（Session 生命周期）
│   │   ├── session-manager.js    # SessionManager（会话业务逻辑）
│   │   ├── memory-adapter.js   # MemoryAdapter（记忆存储适配）
│   │   ├── session/              # Session skill（文档+代码一体）
│   │   │   ├── SKILL.md          # Session 对象操作指南
│   │   │   ├── session-utils.js  # Session 工具函数
│   │   │   └── session-examples.js # 示例 Session 配置
│   │   └── memory/               # Memory skill
│   │       ├── SKILL.md          # Memory 对象操作指南
│   │       └── archive-utils.js  # 归档工具函数
│   ├── personality/              # 人格模块
│   │   ├── module.js             # PersonalityModule（cron 检测 / skill 注入）
│   │   ├── archive-manager.js    # ArchiveManager（归档业务逻辑）
│   │   ├── log-adapter.js        # LogAdapter（日志适配）
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
│   │   ├── skills-loader.js      # SkillLoader（带缓存）
│   │   ├── state.js              # PluginState（向后兼容，v2.x 迁移用）
│   │   └── utils.js              # 工具函数（日期、任务族推断）
│   └── _meta.json                # Skill 元数据索引
```

### 面向对象类设计

| 类 | 职责 | 方法 |
|---|------|------|
| `PluginState` | JSON 文件状态管理（并发安全，向后兼容） | `get()`, `set()`, `append()`, `_persist()` |
| `SkillLoader` | Skill 文件加载与缓存 | `load()`, `clearCache()`, `getAvailableSkills()` |
| `StateAdapter` | 核心 State API 适配 | `transaction()`, `savePlan()`, `getPlan()`, `saveSession()`, `getSession()`, `deleteSession()` |
| `TaskFlowAdapter` | 核心 TaskFlow API 适配 | `createPlanFlow()`, `advancePhase()`, `waitForApproval()`, `runSubtask()`, `getByRunId()`, `getByPhase()` |
| `MemoryAdapter` | 核心 Memory API 适配 | `archiveSession()`, `logEvent()`, `queryHistory()` |
| `LogAdapter` | 核心 Log API 适配 | `write()`, `read()`, `query()` |
| `PlanManager` | 计划业务逻辑 | `createPlan()`, `approvePlan()`, `completePhase()` |
| `SessionManager` | 会话业务逻辑 | `createSession()`, `releaseSession()`, `destroySession()` |
| `ArchiveManager` | 归档业务逻辑 | `archivePlan()`, `archiveSession()`, `dailySummary()` |
| `MetacognitionModule` | 元认知闭环调度 | `onBeforePromptBuild()`, `onLlmOutput()`, `onAgentEnd()` |
| `WorkingMemoryModule` | 任务空间生命周期管理 | `onBeforeToolCall()`, `onAfterToolCall()`, `onAgentEnd()` |
| `PersonalityModule` | 每日自我更新触发 | `onBeforePromptBuild()` |

### 状态存储键空间

| 键 | 类型 | 生命周期 | 说明 |
|----|------|----------|------|
| `plan:{runId}` | Plan | runId | 当前运行的 Plan（State API） |
| `output:{runId}` | string | runId | Monitor 引用的最新 LLM 输出（State API） |
| `session_list:{runId}` | Session[] | runId | 本次运行的任务空间快照（State API） |
| `wm:{runId}:tools` | ToolRecord[] | runId | 本次运行的工具记录（State API） |
| `events:{YYYY-MM-DD}` | Event[] | 日期 | 按日累积的错误事件（Memory API） |
| `memory_table:{YYYY-MM-DD}` | Archive[] | 日期 | 按日累积的 completed 归档（Memory API，向后兼容） |
| `working_memory:active_sessions` | Session[] | 全局 | 全局活跃任务空间索引（State API） |
| `taskflow:{flowId}` | Flow | 长期 | 核心 TaskFlow 实例（TaskFlow API） |
| `logs:{YYYY-MM-DD}` | LogEntry[] | 日期 | 按日累积的日志（Log API） |
| `session:{TYPE}:{任务族}` | Session | 长期 | 任务族会话（Session API） |

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
          "personality": { "enabled": true },
          "integration": { "useCoreTaskFlow": true, "useCoreMemory": true, "useCoreState": true }
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
| `metacognition.monitoring` | boolean | `true` | 监控阶段（仅 active 状态注入 monitoring） |
| `workingMemory.enabled` | boolean | `true` | 工作记忆模块总开关 |
| `workingMemory.trackSubagents` | boolean | `true` | 追踪任务空间创建/完成 |
| `workingMemory.autoArchive` | boolean | `true` | 任务结束后 Archive → Memory 归档 |
| `personality.enabled` | boolean | `true` | 人格模块总开关（cron 检测） |
| `integration.useCoreTaskFlow` | boolean | `true` | 使用核心 TaskFlow（v3.0.0 新增） |
| `integration.useCoreMemory` | boolean | `true` | 使用核心 Memory API（v3.0.0 新增） |
| `integration.useCoreState` | boolean | `true` | 使用核心 State API（v3.0.0 新增） |

> **向后兼容**：`config.assimilation` 仍可工作，内部映射到 `personality`
