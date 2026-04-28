---
name: session
description: >
  工作记忆会话子模块。操作 Session 对象，管理单个会话的生命周期（创建、更新、完成、归档）。
version: 2.0.0
author: 大管家
dependencies:
  - ../../metacognition/planning
  - ../../metacognition/monitoring
  - ../../metacognition/regulation
exports:
  - session_object
  - session_workflows
  - state_transition_map
---

# session

> 工作记忆子模块 - 会话
> 操作 Session 对象：创建、更新、追踪会话任务状态

---

## 文件说明

| 文件 | 功能 | 说明 |
|------|------|------|
| `SKILL.md` | 开发规范 | 会话追踪的执行规范，定义如何修改 Session 对象 |

本文件告诉 Agent 如何操作 Session 对象。

---

## 对象

### Session（会话对象）

**说明**：Session 对象追踪一次 `agent/subagent/sessions_spawn` 工具调用的完整生命周期。

**属性**：

| 属性 | 类型 | 说明 |
|------|------|------|
| `sessionId` | string | 会话唯一标识（sessionKey） |
| `role` | string | 会话角色/类型 |
| `task` | string | 分配的任务描述 |
| `status` | string | `pending` / `active` / `paused` / `completed` / `killed` |
| `createdAt` | string | 创建时间（ISO 8601） |
| `lastActive` | string | 最后活跃时间 |
| `parentRunId` | string | 所属运行 ID |
| `toolRecords` | object[] | 该会话的工具调用记录 |
| `resultSummary` | string | 结果摘要（completed 时填充） |
| `error` | string | 错误信息（killed 时填充） |

**状态变换**：

```
不存在
    ↓ before_tool_call（Agent 调用 agent/subagent/sessions_spawn）
pending（待激活，已创建但未开始执行）
    ↓ 开始执行
active（执行中）
    ├── 正常完成 → complete(result) → completed
    ├── 工具报错 → kill(error) → killed
    └── 主动暂停 → pause() → paused
        ↓ 恢复
        返回 active

completed（已完成）
    ↓ agent_end
转换为 Archive ──→ Memory.store()

killed（已终止）
    ↓ agent_end
直接销毁（不归档）
```

**状态流转图**：

```
        ┌─────────┐
        │  创建   │
        │ (active)│
        └────┬────┘
             │
    ┌────────┼────────┐
    ↓        ↓        ↓
┌───────┐ ┌───────┐ ┌───────┐
│ 正常  │ │ 暂停  │ │ 终止  │
│completed│ │paused │ │killed │
└───┬───┘ └───────┘ └───────┘
    │
    ↓ 定时清理
┌─────────┐
│  归档   │
│ Memory  │
│archives │
└─────────┘
```

---

## 工作流（修改 Session 对象的方法）

### 工作流1：创建会话任务

**说明**：通过本工作流修改 Session 对象，从「不存在」到 `pending` 再到 `active`。

**触发时机**：计划阶段完成、用户确认使用会话后

**步骤**：
1. **检查工作记忆中的现有会话**（读取 Memory.sessionList）
   - 读取 Memory 对象中的「当前活跃任务看板」和「活跃会话清单」
   - 检查是否存在与当前任务**共享上下文**的 Session：
     - 相同项目/领域
     - 相同任务类型
     - 相同目标或交付物
     - 状态为 `active` 或 `paused`
   - **复用规则**：
     - 若存在共享上下文的 Session → **复用该 Session**，不创建新 Session，更新 `Session.lastActive`
     - 若不存在共享上下文的 Session → **创建新 Session**（通过 agent/subagent 工具创建）

2. 主代理制定计划

3. **在 Memory.taskBoard 添加记录**（修改 Memory 对象）
   ```markdown
   | 任务ID | 项目 | 任务描述 | 会话ID | 状态 | 创建时间 | 最后更新 | 备注 |
   | [T001] | [项目] | [任务] | [待分配] | active | [现在] | [现在] | [计划ID] |
   ```

4. **创建 Session 对象**（如 `session:PROJECT:xxx`）
   - 设置 `sessionId`
   - 设置 `role`
   - 设置 `task`
   - 设置 `status = 'pending'`
   - 设置 `createdAt = now`
   - 设置 `lastActive = now`

5. **获取会话ID**

6. **更新 Memory.taskBoard「会话ID」字段**（修改 Memory 对象）

7. **在 Memory.sessionList 添加记录**（修改 Memory 对象）
   ```markdown
   | 会话ID | 类型/角色 | 分配任务 | 状态 | 创建时间 | 最后活跃 | 备注 |
   | [ID] | [角色] | [任务] | active | [现在] | [现在] | - |
   ```

8. **激活 Session 对象**
   - `Session.status = 'active'`

---

### 工作流2：监控会话

**说明**：通过本工作流读取并更新 Session 对象的 `lastActive` 和状态。

**触发时机**：监控阶段定期执行

**步骤**：
1. **定期查询会话状态**（读取 Session 对象）
   - `subagents action=list` 或 `sessions_list`
2. **更新「最后活跃」时间**（修改 `Session.lastActive`）
3. **评估任务进度**
4. **更新 Memory 对象「备注」字段**（修改 Memory 对象）

---

### 工作流3：会话完成

**说明**：通过本工作流修改 Session 对象从 `active` 到 `completed`。

**触发时机**：收到会话完成通告

**步骤**：
1. **接收会话完成通告**
2. **更新 Session.status 为 `completed`**（修改 Session 对象）
3. **在 Session.resultSummary 记录完成摘要**（修改 Session 对象）
4. **更新 Memory.sessionList 状态**（修改 Memory 对象）
5. **等待定时清理归档**（由 Memory 对象执行）

---

### 工作流4：会话终止

**说明**：通过本工作流修改 Session 对象从 `active` 到 `killed`。

**触发时机**：用户要求终止会话，或工具报错

**步骤**：
1. **将 Session.status 更新为 `killed`**（修改 Session 对象）
2. **在 Session.error 记录终止原因**（修改 Session 对象）
3. **更新 Memory.sessionList 状态**（修改 Memory 对象）
4. **等待定时清理任务删除**（由 Memory 对象执行，直接删除不归档）

---

## 使用指南

### 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `operation` | string | ✅ | 操作类型：`create` / `monitor` / `complete` / `kill` |
| `task_info` | object | ✅ (create) | 任务信息（项目、任务描述） |
| `session_id` | string | ✅ (update) | 会话唯一标识（sessionKey） |
| `status` | string | ✅ (update) | 新状态：`active`/`paused`/`completed`/`killed` |

### 输出结果

| 输出项 | 格式 | 说明 |
|--------|------|------|
| `task_board` | Markdown 表格 | Memory 对象的当前活跃任务看板 |
| `session_list` | Markdown 表格 | Memory 对象的活跃会话清单 |

---

## 与 Metacognition 的关系

```
Metacognition.Plan ──→ Session 创建（工作流1）
Metacognition.Monitor ──→ Session 监控（工作流2）
Metacognition.Regulator ──→ Session 暂停/恢复（工作流2/3）
```

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v2.0.0 | 2026-04-28 | 面向对象重构，明确 Session 对象属性及四个修改方法 |
| v1.1.0 | 2026-04-26 | 统一使用会话；添加上下文共享检查 |
| v1.0.0 | 2026-04-17 | 初始版本 |

---

*创建者: 大管家*  
*创建时间: 2026-04-17*
