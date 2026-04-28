---
name: planning
description: >
  元认知计划子模块。操作 Plan 对象，管理任务上下文、工作空间和阶段化执行。
  核心原则：Plan 制定后必须先汇报给用户，用户确认后才能执行。
version: 2.0.1
author: 大管家
dependencies:
  - ../../working_memory/session
exports:
  - plan_object
  - plan_workflows
---

# planning

> 元认知子模块 - 计划
> Plan 不是步骤列表，而是一套完整的上下文语境
> **必须先汇报，确认后才能执行**

---

## 核心原则

**汇报 → 确认 → 执行**

1. Agent 收到复杂任务后，首先制定完整 Plan
2. **必须向用户汇报 Plan 内容**，等待用户确认或修改意见
3. 用户确认后（回复"确认"、"可以"等），将 Plan.status 设为 `active`
4. 只有 `active` 状态的 Plan 才能进入执行阶段
5. 如果用户要求修改，修改后重新汇报，再次等待确认

---

## 对象

### Plan（计划对象）

**说明**：Plan 是一套完整的上下文语境，Agent 通过阅读 Plan 了解"要做什么、用什么做、在哪里做、做到什么程度"。

#### 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `runId` | string | 所属运行唯一标识 |
| `prompt` | string | 用户原始输入 |
| `createdAt` | number | 创建时间戳 |
| `status` | string | **draft** / **pending_approval** / **active** / **completed** / **destroyed** |
| `context` | object | **任务上下文**（见下） |
| `workspace` | object | **工作空间**（见下） |
| `execution` | object | **执行计划**（见下） |

#### 状态机

```
draft（草稿）
    ↓ Agent 制定完成，向用户汇报
pending_approval（等待用户确认）
    ├─ 用户确认 → active
    ├─ 用户修改 → 修改 Plan，回到 pending_approval（重新汇报）
    └─ 用户取消 → completed
active（执行中）
    ↓ 按 phases 逐阶段推进
    ├─ 正常完成 → completed
    └─ 重大偏差需重新规划 → draft（重新汇报）
completed（完成）
    ↓ agent_end
destroyed（销毁）
```

**状态转换规则**：

| 当前状态 | 触发条件 | 新状态 | 操作 |
|----------|----------|--------|------|
| 不存在 | 收到复杂任务 | `draft` | 生成 Plan 初始结构 |
| `draft` | Agent 制定完成并汇报 | `pending_approval` | 等待用户反馈 |
| `pending_approval` | 用户确认 | `active` | 开始执行 phases |
| `pending_approval` | 用户要求修改 | `pending_approval` | 修改 Plan，重新汇报 |
| `pending_approval` | 用户取消 | `completed` | 终止任务 |
| `active` | 阶段正常推进 | `active` | currentPhase++ |
| `active` | 所有 phases 完成 | `completed` | 任务完成 |
| `active` | 重大偏差需重规划 | `draft` | 回到规划阶段重新汇报 |
| `completed` | `agent_end` | `destroyed` | 清理状态 |

#### context（任务上下文）

| 属性 | 类型 | 说明 |
|------|------|------|
| `goal` | string | 任务目标：最终要达成什么 |
| `constraints` | string[] | 约束条件：时间、资源、规范等限制 |
| `successCriteria` | string[] | 验收标准：什么算"完成" |

#### workspace（工作空间）

| 属性 | 类型 | 说明 |
|------|------|------|
| `sessions` | Session[] | 已创建的任务空间列表 |
| `artifacts` | string[] | 已产出的文档/文件列表 |
| `tools` | string[] | 可用的工具列表 |

#### execution（执行计划）

| 属性 | 类型 | 说明 |
|------|------|------|
| `phases` | Phase[] | 阶段列表 |
| `currentPhase` | number | 当前阶段索引（从0开始） |

#### Phase（阶段对象）

| 属性 | 类型 | 说明 |
|------|------|------|
| `id` | string | 阶段标识 |
| `name` | string | 阶段名称 |
| `goal` | string | 阶段目标 |
| `sessionId` | string \| null | 分配的任务空间 |
| `taskFamily` | string | 任务族 |
| `outputs` | string[] | 阶段预期产出 |
| `status` | string | `pending` / `active` / `completed` / `skipped` |

---

## 工作流

### 工作流1：制定 Plan 并汇报（draft → pending_approval）

**说明**：Agent 收到复杂任务后，首先制定完整 Plan，然后**必须向用户汇报**。

**步骤**：

1. **理解用户意图**
   - 分析用户原始输入（Plan.prompt）
   - 识别核心诉求和隐含需求

2. **加载个人记忆配置**
   - 读取 `memory.md` 中的条件-行动规则
   - 判断用户任务是否满足某条规则的「条件」（关键词匹配）

3. **完善任务上下文**（修改 `Plan.context`）
   - `goal`：用一句话明确最终交付物
   - `constraints`：列出所有已知约束（时间、资源、规范）
   - `successCriteria`：定义可验证的验收标准

4. **规划阶段**（修改 `Plan.execution.phases`）
   - 每个阶段必须有明确的 `goal`（"达成XX"而非"做XX"）
   - 为需要独立上下文的阶段分配任务空间（`sessionId` + `taskFamily`）
   - 定义每阶段的预期 `outputs`
   - 确定阶段间的依赖关系

5. **准备汇报**（确保 Plan 完整）
   - 检查 context、workspace、execution 三个部分是否完整
   - 确认任务空间分配合理（同任务族复用）

6. **向用户汇报**
   ```markdown
   📋 **计划汇报**

   ▸ 任务目标：[goal]
   ▸ 约束条件：[constraints]
   ▸ 验收标准：[successCriteria]

   ▸ 执行阶段：
     1. [阶段名] — [目标] [任务空间]
     2. [阶段名] — [目标] [任务空间]
     ...

   ▸ 预期产出：[artifacts]

   **计划已制定完毕，请确认或提出修改意见。**
   ```

7. **更新状态**
   - `Plan.status = "pending_approval"`
   - 保存 Plan 到持久化存储

---

### 工作流2：处理用户确认/修改（pending_approval）

**说明**：用户看到汇报后，可能确认、修改或取消。Agent 据此更新 Plan 状态。

**用户确认时**：
1. 读取用户确认消息
2. `Plan.status = "active"`
3. 开始执行 phases（进入工作流3）

**用户修改时**：
1. 读取用户修改意见
2. 修改 Plan 的相应部分（context、phases、workspace 等）
3. 重新向用户汇报修改后的 Plan
4. 保持 `Plan.status = "pending_approval"`

**用户取消时**：
1. 读取取消原因
2. `Plan.status = "completed"`
3. 说明取消原因，结束任务

---

### 工作流3：阶段化执行（active）

**说明**：Plan 已确认，按 execution.phases 逐阶段推进。

**步骤**：

```
读取 Plan.execution.currentPhase → 获取当前阶段
    ↓
读取 Plan.execution.phases[currentPhase]
    ↓
执行任务
    ├── 需要任务空间？→ 检查 workspace.sessions
    │   ├── 存在且 idle → 复用（status = active）
    │   └── 不存在 → 创建新 Session
    │       └── 加入 workspace.sessions
    ↓
阶段目标达成？
    ├── 是 → phase.status = completed，currentPhase++
    │        产出物记录到 workspace.artifacts
    │        相关 Session 标记 idle
    └── 否 → 继续当前阶段
    ↓
所有 phases 完成？
    ├── 是 → Plan.status = completed
    └── 否 → 继续下一阶段
```

**阶段完成标准**：
- 阶段 `goal` 已达成
- 阶段 `outputs` 已产出并记录到 `workspace.artifacts`
- 相关任务空间已正确处理

---

### 工作流4：任务空间管理

**复用规则**：
- 同一 `taskFamily` 的阶段优先复用同一 idle 任务空间
- 不同 `taskFamily` 必须创建独立任务空间（并行执行）
- 任务空间标识格式：`session:{TYPE}:{任务族}`

**生命周期**：

| 阶段 | 操作 | 修改的 Plan 属性 |
|------|------|-----------------|
| 创建 | `sessions_spawn` + 加入 workspace.sessions | `workspace.sessions[].status = active` |
| 复用 | 复用 idle Session | `workspace.sessions[].status = active` |
| 执行 | 在 Session 中完成任务 | `workspace.artifacts` 增加产出 |
| 释放 | Session 标记 idle | `workspace.sessions[].status = idle` |
| 销毁 | 从 workspace.sessions 移除 | 不再使用 |

---

## 使用指南

### 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `task_description` | string | ✅ | 用户任务描述 |

### 输出结果

| 输出项 | 格式 | 说明 |
|--------|------|------|
| `plan_report` | Markdown | 向用户汇报的 Plan 内容 |
| `plan_status_update` | string | 状态变更（draft → pending_approval → active） |

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v2.0.1 | 2026-04-28 | 工作流新增"加载个人记忆配置"步骤，制定 Plan 时需参考 memory.md 条件-行动规则 |
| v2.2.0 | 2026-04-28 | 增加"汇报 → 确认 → 执行"强制流程，状态机增加 pending_approval |
| v2.1.0 | 2026-04-28 | Plan 重构为上下文语境：context + workspace + execution |
| v2.0.0 | 2026-04-28 | 面向对象重构 |
| v1.0.0 | 2026-04-17 | 初始版本 |

---

*创建者: 大管家*  
*创建时间: 2026-04-17*
