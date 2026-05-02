---
name: planning
description: >
  元认知计划子模块。指导 Agent 在任务开始时制定 Plan、向用户汇报并等待确认。
  核心原则：Plan 制定后必须先汇报给用户，用户确认后才能执行。
version: 3.3.0
injected_at: before_prompt_build
module: metacognition
---

# Planning — 计划制定与确认

> 元认知子模块 - 计划阶段
> Plan 不是步骤列表，而是一套完整的上下文语境
> **必须先汇报，确认后才能执行**

---

## 注入上下文

本 skill 在 **`before_prompt_build`** 触发时注入。此时插件已完成以下操作：

| 时机 | 插件已完成的操作 | 存储位置 |
|------|-----------------|----------|
| 用户确认需要 Plan 后 | 插件创建 task JSON 并生成 Plan 模板 | `state/tasks/{runId}.json` |
| Agent 制定 Plan 时 | Agent 自行完善 context、phases、约束条件 | 内存 |

当前 Plan 状态由插件维护在统一 task JSON 中，Agent 负责理解状态并做出正确决策，**无需直接操作存储文件**。

---

## 核心对象：Plan（统一 task JSON 中的 plan 字段）

**存储位置**：`task:{runId}.plan`（统一 task JSON 内）
**读取方式**：插件在注入时已通过 `stateAdapter.getTask(runId)` 获取并附加在上下文里

```json
{
  "runId": "uuid",
  "status": "draft",
  "plan": {
    "prompt": "用户输入前500字",
    "createdAt": 1234567890000,
    "context": {
      "goal": "任务目标",
      "constraints": ["约束1", "约束2"],
      "successCriteria": ["标准1", "标准2"]
    },
    "workspace": {
      "sessions": [],
      "artifacts": [],
      "tools": ["editor", "git", "test_framework"],
      "skills": []
    },
    "execution": {
      "phases": [
        {
          "id": "p1",
          "name": "阶段名",
          "goal": "阶段目标（'达成XX'而非'做XX'）",
          "sessionId": "session:PROJECT:CODE",
          "taskFamily": "CODE",
          "outputs": ["预期产出"],
          "status": "pending"
        }
      ],
      "currentPhase": 0
    }
  },
  "event": { "status": "draft", "deviations": [], "attributions": [], "planRevisions": [], "outcome": {} },
  "sessionIds": [],
  "tools": []
}
```

| 属性 | 类型 | 说明 | 当前值来源 |
|------|------|------|-----------|
| `runId` | string | 本次运行唯一标识 | 插件注入 |
| `status` | string | `draft` / `pending_approval` / `active` / `completed` / `revising` | **由 Agent 决策后通知插件更新** |
| `plan.prompt` | string | 用户原始输入（截断500字） | 插件创建 task 时填充 |
| `plan.context.goal` | string | 任务目标：最终要达成什么 | Agent 制定 Plan 时填写 |
| `plan.context.constraints` | string[] | 约束条件 | Agent 制定 Plan 时填写 |
| `plan.context.successCriteria` | string[] | 验收标准 | Agent 制定 Plan 时填写 |
| `plan.workspace.sessions` | object[] | 已创建的任务空间列表 | 插件在阶段执行时维护 |
| `plan.workspace.artifacts` | string[] | 已产出的文档/文件列表 | Agent 在阶段完成后追加 |
| `plan.workspace.tools` | string[] | 可用工具列表 | Agent 根据任务类型选择 |
| `plan.execution.phases` | object[] | 阶段列表 | Agent 制定 Plan 时设计 |
| `plan.execution.currentPhase` | number | 当前阶段索引 | 插件在阶段推进时维护 |
| `event.deviations` | object[] | 偏差记录列表 | Monitoring 阶段自动追加 |
| `event.attributions` | object[] | 归因分析列表 | Regulation 阶段 Agent 填写 |
| `event.planRevisions` | object[] | 计划修订记录 | Regulation 阶段 Agent 追加 |

---

## Agent 职责

### 职责 A：制定 Plan 并汇报（draft → pending_approval）

**触发条件**：当前 task.status === `draft`

**你需要做的**（决策层）：

1. **理解用户意图**
   - 阅读用户当前 prompt 中的任务需求
   - 识别核心诉求和隐含需求

2. **加载个人记忆配置**
   - 读取 `memory.md` 中的条件-行动规则
   - 若用户任务满足某条规则的条件，在 Plan 中执行对应的行动（添加约束、阶段、验收标准等）

3. **完善 task.plan.context**（评估并调整插件预生成的内容）
   - `goal`：用一句话明确最终交付物
   - `constraints`：列出所有已知约束
   - `successCriteria`：定义可验证的验收标准

4. **审视并调整 task.plan.execution.phases**
   - 每个阶段必须有明确的 `goal`（"达成XX"而非"做XX"）
   - 检查插件预分配的任务空间是否合理（同任务族复用同一 session）
   - 定义每阶段的预期 `outputs`
   - 如需增删改阶段，说明理由

5. **向用户汇报**
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

6. **通知插件状态变更**
   - 汇报完成后，告知插件将 task.status 更新为 `"pending_approval"`
   - （插件通过 `stateAdapter.saveTask()` 执行实际存储更新）

**插件已自动完成的**（执行层，无需你操作）：
- 已根据用户 prompt 生成 Plan 模板（含 context、workspace、execution）
- 已保存到 `state/tasks/{runId}.json`

**你可以参考的上下文**（注入时附加在 skill 下方）：
- task.status（draft / pending_approval / active）
- 阶段数量和已分配任务空间数
- 可用工具列表
- 个人记忆配置提示（`MEMORY.md` 条件-行动规则）

---

### 职责 B：处理用户确认/修改/取消（pending_approval / revising）

**触发条件**：当前 task.status === `pending_approval` 或 `revising`，且用户已回复

**你需要做的**（决策层）：

1. **读取用户反馈内容**

2. **如果用户确认**（"确认"、"可以"、"开始执行"等）：
   - 告知插件将 task.status 更新为 `"active"`
   - 开始按 phases 执行
   - （插件通过 `stateAdapter.saveTask()` 执行状态切换）

3. **如果用户要求修改**：
   - 修改 task.plan.context / task.plan.execution.phases 的相应部分
   - 重新向用户汇报修改后的 Plan
   - 保持 task.status 为 `"pending_approval"`（或 `"revising"`）
   - （插件维持当前状态，等待下一次用户反馈）

4. **如果用户取消任务**：
   - 告知插件将 task.status 更新为 `"completed"`
   - 说明取消原因

**插件已自动完成的**（执行层，无需你操作）：
- 已保存当前 task 状态到统一 task JSON
- 若状态转为 `active`，已调用 `flowAdapter.advancePhase()` 推进第一阶段

---

## 决策检查点

在汇报 Plan 之前，请确认：

- [ ] `plan.context.goal` 是否用一句话明确了最终交付物？
- [ ] `plan.context.constraints` 是否列出了所有已知限制？
- [ ] `plan.context.successCriteria` 是否可验证（"通过测试"而非"做好"）？
- [ ] 每个阶段的 `goal` 是否以"达成"开头（可验证）？
- [ ] 需要任务空间的阶段是否已分配 `sessionId`（格式：`session:{TYPE}:{任务族}`）？
- [ ] 同任务族的阶段是否复用了同一 session？
- [ ] 是否已加载 `memory.md` 中的条件-行动规则并应用？
- [ ] 是否已向用户汇报并明确请求确认？

---

## 状态流转（由插件维护，Agent 负责触发状态变更）

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
    └─ 重大偏差需重新规划 → revising（修改后回到 pending_approval）
revising（修订中）
    ↓ Agent 修改 Plan
    └─ 回到 pending_approval（重新汇报）
completed（完成）
    ↓ agent_end 时插件自动聚合事件到 Memory
```

**关键规则**：
- `draft` → `pending_approval`：Agent 汇报完成后通知插件更新
- `pending_approval` → `active`：用户确认后，Agent 通知插件更新，插件同时调用 `flowAdapter.advancePhase()`
- `active` → `revising`：重大偏差需重新规划时，Agent 通知插件更新
- `revising` → `pending_approval`：修改完成后重新汇报
- `active` → `completed`：所有 phases 完成后，插件自动维护
- 任何状态变更的实际存储操作由插件通过 `stateAdapter.saveTask()` 完成

---

## 与其他 Skill 的关系

| Skill | 注入时机 | 职责边界 |
|-------|---------|---------|
| `monitoring` | `llm_output` | 负责在 Plan active 时检查 Agent 输出是否与 Plan 一致 |
| `working_memory` | `agent_end` | 负责在运行结束时归档 session，管理任务空间复用 |
| `regulation` | `llm_output`（偏差触发） | 负责在检测到重大偏差时分析原因并制定调节方案 |
| `development` | `agent_end` | 任务完成后基于 task.event 分析同化/顺应 |

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v3.4.0 | 2026-04-29 | 延迟创建：Plan 不再预生成，Agent 评估 + 用户确认后才创建 task |
| v3.3.0 | 2026-04-29 | 适配统一 task JSON：Plan 存储在 task.plan 中；状态流转增加 revising；移除 destroyed 状态 |
| v3.0.0 | 2026-04-29 | v3 重构：对象操作移交插件层，skill 变为纯 Agent 指导文档 |
