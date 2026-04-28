---
name: working_memory
description: >
  工作记忆模块路由。管理 Event（事件）、Memory（记忆）、Session（会话）三个对象。基于 Baddeley 工作记忆模型设计。
version: 2.0.0
author: 大管家
dependencies: []
exports:
  - memory_object
  - session_object
routes:
  - memory/
  - session/
---

# working_memory

> 工作记忆模块 - 管理短期认知资源
> 包含 Event（事件对象）、Memory（记忆对象）、Session（会话对象）

---

## 文件说明

本文件为模块路由，索引以下子模块。Agent 通过阅读本文件了解可调用的子模块及其操作的对象：

| 文件 | 子模块 | 功能 | 操作对象 |
|------|--------|------|----------|
| `SKILL.md` | 本文件 | 模块路由，索引子模块 | WorkingMemory |
| `memory/SKILL.md` | 记忆 | 维护看板、追踪表、归档 | Memory 对象 |
| `session/SKILL.md` | 会话 | 创建、更新、追踪会话状态 | Session 对象 |

> **注意**：Event（事件）对象已移动到 `metacognition/regulation/events/SKILL.md`，由 Regulator 对象管理。

---

## 对象

### WorkingMemory（工作记忆对象）

工作记忆对象是三个子对象的容器，负责在 Hook 触发时调度正确的子对象。

#### 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `sessions` | Session[] | 当前运行的会话对象列表 |
| `events` | Event[] | 按日期聚合的事件对象列表 |
| `memoryTables` | Memory[] | 按日期聚合的记忆对象列表 |
| `status` | string | 状态：`idle` / `tracking` / `archiving` |

#### 生命周期

```
idle（空闲）
    ↓ before_tool_call + 会话工具
tracking（追踪中，Session 对象激活）
    ↓ after_tool_call + 报错
事件记录中（Event 对象激活）
    ↓ after_tool_call + 会话完成
会话完成（Session.status = completed）
    ↓ agent_end + autoArchive
archiving（归档中，Session → Memory）
    ↓ 归档完成
idle
```

---

## 子对象概览

### Memory（记忆对象）

**操作目标**：维护「当前活跃任务看板」和「活跃会话清单」，管理 completed Session 的归档

**属性**：

| 属性 | 类型 | 说明 |
|------|------|------|
| `date` | string | 记忆日期（YYYY-MM-DD） |
| `taskBoard` | Markdown 表格 | 当前活跃任务看板 |
| `sessionList` | Markdown 表格 | 活跃会话清单 |
| `archives` | Archive[] | 已完成会话的归档记录数组 |
| `status` | string | `active` / `cleaning` / `archived` |

**taskBoard 字段结构**：

```markdown
| 任务ID | 项目 | 任务描述 | 会话ID | 状态 | 创建时间 | 最后更新 | 备注 |
|--------|------|----------|--------|------|----------|----------|------|
```

| 字段 | 必填 | 格式 | 示例 |
|------|------|------|------|
| 任务ID | 是 | T001, T002... | T001 |
| 项目 | 是 | 字符串 | 数字化存储与自传体记忆 |
| 任务描述 | 是 | 字符串 | 文献检索与综述 |
| 会话ID | 是 | `session:xxx` 或 `agent:xxx` | `session:CORN:steward` |
| 状态 | 是 | `active`/`paused`/`completed`/`killed` | `active` |
| 创建时间 | 是 | `YYYY-MM-DD HH:MM` | `2026-04-17 10:30` |
| 最后更新 | 是 | `YYYY-MM-DD HH:MM` | `2026-04-17 14:00` |
| 备注 | 否 | 字符串 | 进度50% |

**sessionList 字段结构**：

```markdown
| 会话ID | 类型/角色 | 分配任务 | 状态 | 创建时间 | 最后活跃 | 备注 |
|--------|-----------|----------|------|----------|----------|------|
```

| 字段 | 必填 | 格式 | 示例 |
|------|------|------|------|
| 会话ID | 是 | `session:xxx` 或 `agent:xxx` | `session:CORN:steward` |
| 类型/角色 | 是 | 字符串 | 文献检索助手 |
| 分配任务 | 是 | 字符串 | 检索自传体记忆相关文献 |
| 状态 | 是 | `active`/`paused`/`completed`/`killed` | `active` |
| 创建时间 | 是 | `YYYY-MM-DD HH:MM` | `2026-04-17 10:30` |
| 最后活跃 | 是 | `YYYY-MM-DD HH:MM` | `2026-04-17 14:00` |
| 备注 | 否 | 字符串 | 已检索50篇 |

**修改方法**（工作流）：见 `memory/SKILL.md`
- 表格结构维护（校验完整性）
- 定时清理（completed → 归档，killed → 删除）

**持久化**：跨 runId，按日聚合到 `memory_table:{YYYY-MM-DD}`

---

### Session（会话对象）

**操作目标**：追踪一次 `agent/subagent/sessions_spawn` 工具调用的完整生命周期

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

**状态变换触发**：

| 当前状态 | 触发条件 | 新状态 | 方法 |
|----------|----------|--------|------|
| 不存在 | `before_tool_call` + 会话工具 | `pending` | `create()` |
| `pending` | 开始执行 | `active` | `activate()` |
| `active` | 成功完成 | `completed` | `complete(result)` |
| `active` | 执行报错 | `killed` | `kill(error)` |
| `active` | 主动暂停 | `paused` | `pause()` |
| `paused` | 恢复执行 | `active` | `activate()` |
| `completed` | `agent_end` | 销毁 | `toArchive()` → `Memory.store()` |
| `killed` | `agent_end` | 销毁 | 直接移除 |

**修改方法**（工作流）：见 `session/SKILL.md`
- 创建会话任务
- 监控会话
- 会话完成
- 会话终止

**持久化**：runId 级，运行结束后 completed 转为 Archive 存入 Memory，killed 直接删除

---

## 工作流（对象协作方法）

### 工作流1：任务生命周期管理

```
创建任务（planning 阶段调用 session/SKILL.md 修改 Session 对象）
    ↓
状态更新（monitoring 阶段调用 session/SKILL.md 修改 Session 对象）
    ↓
完成 / 终止（session/SKILL.md 修改 Session.status）
    ↓
定时清理（每日 00:00 调用 memory/SKILL.md 修改 Memory 对象）
    ↓
completed Session ──→ Memory.store(Archive)
killed Session ──→ 直接销毁
```

## 使用指南

### 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `operation` | string | ✅ | 操作类型：create / update / archive / cleanup |
| `task_data` | object | ✅ (create/update) | 任务数据 |
| `session_id` | string | ✅ (update) | 会话唯一标识（sessionKey） |

### 输出结果

| 输出项 | 格式 | 说明 |
|--------|------|------|
| `task_board` | Markdown 表格 | Memory 对象的当前活跃任务看板 |
| `session_list` | Markdown 表格 | Memory 对象的活跃会话清单 |
| `cleanup_log` | Markdown | Memory 对象的清理日志 |

---

## 状态说明（Session 对象属性参考）

| 状态 | 含义 | Memory 对象处理方式 |
|------|------|---------------------|
| `active` | 正在执行 | 保留在活跃会话清单 |
| `paused` | 暂停等待 | 保留在活跃会话清单 |
| `completed` | 已完成 | 归档到 Memory.archives 后删除 |
| `killed` | 被终止 | 直接删除，不归档 |

---

## 与 Personality 的关系

```
WorkingMemory.Event 对象 ──→ Personality.Diary 读取（回顾事件）
WorkingMemory.Memory.archives ──→ Personality 反思（已完成任务分析）
```

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v2.0.0 | 2026-04-28 | 面向对象重构，明确 Event/Memory/Session 三个对象及其属性 |
| v1.3.0 | 2026-04-26 | 统一使用会话，取消一次性任务区分 |
| v1.0.0 | 2026-04-17 | 初始版本 |

---

*创建者: 大管家*  
*创建时间: 2026-04-17*
