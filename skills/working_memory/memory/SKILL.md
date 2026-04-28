---
name: memory
description: >
  工作记忆记忆子模块。操作 Memory 对象，维护「当前活跃任务看板」和「活跃会话清单」，管理 completed Session 的归档。
version: 2.0.0
author: 大管家
dependencies: []
exports:
  - memory_object
  - memory_workflows
  - archive_schema
---

# memory

> 工作记忆子模块 - 记忆
> 操作 Memory 对象：维护看板、追踪表和归档记录

---

## 文件说明

| 文件 | 功能 | 说明 |
|------|------|------|
| `SKILL.md` | 开发规范 | 记忆表管理的执行规范，定义如何修改 Memory 对象 |

本文件告诉 Agent 如何操作 Memory 对象（看板和追踪表）。

---

## 对象

### Memory（记忆对象）

**说明**：Memory 对象维护「当前活跃任务看板」和「活跃会话清单」，接收已完成 Session 转换的 Archive 记录。

**属性**：

| 属性 | 类型 | 说明 |
|------|------|------|
| `date` | string | 记忆日期（YYYY-MM-DD） |
| `taskBoard` | Markdown 表格 | 当前活跃任务看板 |
| `sessionList` | Markdown 表格 | 活跃会话清单 |
| `archives` | Archive[] | 该日期的归档记录数组 |
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

**Archive 记录结构**（由 Session 对象变换产生）：

```json
{
  "sessionRef": "session:TASK:检索_abc1",
  "task": "检索相关文献",
  "role": "助手",
  "status": "completed",
  "toolCount": 3,
  "archivedAt": "2026-04-28T00:30:00.000Z",
  "runId": "uuid"
}
```

**状态变换**：

```
空（archives = []）
    ↓ Session.toArchive() + Memory 接收
active（包含归档记录）
    ↓ 每日定时清理触发
cleaning（清理中）
    ↓ 清理完成
返回 active
    ↓ 长期归档策略执行
archived（已转长期存储）
```

---

## 工作流（修改 Memory 对象的方法）

### 工作流1：表格结构维护

**说明**：通过本工作流修改 Memory 对象的 `taskBoard` 和 `sessionList` 属性，确保数据结构完整。

**步骤**：
1. **检查当前活跃任务看板**（修改 `Memory.taskBoard`）
   - 确认表头完整：任务ID、项目、任务描述、会话ID、状态、创建时间、最后更新、备注
   - 确认无多余空行

2. **检查活跃会话清单**（修改 `Memory.sessionList`）
   - 确认表头完整：会话ID、类型/角色、分配任务、状态、创建时间、最后活跃、备注
   - 确认无多余空行

3. **数据完整性校验**
   - 必填字段不为空
   - 时间格式统一为 `YYYY-MM-DD HH:MM`
   - 状态值在允许范围内：`active` / `paused` / `completed` / `killed`
   - **所有任务都使用会话**，不再区分一次性任务

---

### 工作流2：定时清理（归档方法）

**说明**：通过本工作流修改 Memory 对象，将 completed Session 转为 Archive 存入 `archives`，清理 killed Session。

**触发**：每日 00:00（或 agent_end 时）

**步骤**：
1. **读取「活跃会话清单」**（读取 Memory.sessionList）
2. **筛选状态为 `completed` 的行**（识别可归档 Session）
3. **归档到「事件记忆」表格**（修改 Memory.archives）
   - 从 Session 对象生成 Archive 记录
   - 日期: 当前日期
   - 事件: 会话任务归档
   - 涉及实体: 会话ID
   - 结果: 任务完成
   - 日志位置: `events/YYYY-MM-DD/HH-MM-SS-completed.md`
4. **筛选状态为 `killed` 的行**
5. **直接删除 `killed` 行**（不归档，从 sessionList 移除）
6. **从清单中删除 `completed` 和 `killed` 行**（修改 Memory.sessionList）
7. **记录清理日志**

---

## 使用指南

### 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `table_name` | string | ✅ | 表格名称：`task_board` 或 `session_list` |
| `action` | string | ✅ | 操作类型：`validate` / `cleanup` / `archive` |
| `records` | list | ❌ | 待写入的记录（create 时） |

### 输出结果

| 输出项 | 格式 | 说明 |
|--------|------|------|
| `validation_report` | Markdown | Memory 对象的数据完整性检查报告 |
| `archive_log` | Markdown | Memory.archives 的归档记录清单 |
| `cleaned_count` | integer | 本次清理的记录数 |

---

## 与 Session 对象的关系

```
Session.complete()
    ↓
Session.toArchive() → Archive 值对象
    ↓
Memory.store(archive) → Memory.archives 追加
    ↓
Memory.cleanup() → 从 Memory.sessionList 移除 completed/killed
```

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v2.0.0 | 2026-04-28 | 面向对象重构，明确 Memory 对象属性及看板/归档方法 |
| v1.1.0 | 2026-04-26 | 统一使用会话，取消一次性任务区分 |
| v1.0.0 | 2026-04-17 | 初始版本 |

---

*创建者: 大管家*  
*创建时间: 2026-04-17*
