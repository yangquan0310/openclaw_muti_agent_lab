---
name: subagent_tracker
description: >
  工作记忆会话追踪。创建、更新和追踪**命名会话**任务状态，管理命名会话生命周期。一次性任务执行完即销毁，无需追踪。
version: 1.0.0
author: 大管家
dependencies:
  - ../../metacognition/planning
  - ../../metacognition/monitoring
  - ../../metacognition/regulation
exports:
  - lifecycle_flow
  - state_transition_map
  - tracking_procedures
---

# subagent_tracker

> 工作记忆 - 会话追踪
> 创建、更新和追踪**命名会话**任务状态
> 
> **注意**：一次性任务（无命名会话）执行完即销毁，无需在工作记忆中追踪。

---

## 文件说明

| 文件 | 功能 | 说明 |
|------|------|------|
| `SKILL.md` | 开发规范 | 会话追踪的执行规范 |

---

## 工作流

### 工作流1：创建命名会话任务

**触发时机**：计划阶段完成、用户确认使用命名会话后

**步骤**：
1. **检查工作记忆中的现有命名会话**
   - 读取 MEMORY.md 中的「当前活跃任务看板」和「活跃会话清单」
   - 检查是否存在与当前任务**共享上下文**的命名会话：
     - 相同项目/领域
     - 相同任务类型
     - 相同目标或交付物
     - 状态为 `active` 或 `paused`
   - **复用规则**：
     - 若存在共享上下文的命名会话 → **复用该会话**，不创建新命名会话
     - 若不存在共享上下文的命名会话 → **创建新命名会话**（通过 `sessionTarget` 指定）

2. 主代理制定计划
3. 在「当前活跃任务看板」添加记录
   ```markdown
   | 任务ID | 项目 | 任务描述 | 会话ID | 状态 | 创建时间 | 最后更新 | 备注 |
   | [T001] | [项目] | [任务] | [待分配] | active | [现在] | [现在] | [计划ID] |
   ```
4. 创建命名会话（通过 `sessionTarget` 指定，如 `session:PROJECT:xxx`）
5. 获取会话ID
6. 更新「会话ID」字段
7. 在「活跃会话清单」添加记录
   ```markdown
   | 会话ID | 类型/角色 | 分配任务 | 状态 | 创建时间 | 最后活跃 | 备注 |
   | [ID] | [角色] | [任务] | active | [现在] | [现在] | - |
   ```

### 工作流2：监控会话

**触发时机**：监控阶段定期执行

**步骤**：
1. 定期查询会话状态（`subagents action=list` 或 `sessions_list`）
2. 更新「最后活跃」时间
3. 评估任务进度
4. 更新「备注」字段

### 工作流3：会话完成

**触发时机**：收到会话完成通告

**步骤**：
1. 接收会话完成通告
2. 更新「状态」为 `completed`
3. 在「备注」记录完成摘要
4. 等待定时清理归档

### 工作流4：会话终止

**触发时机**：用户要求终止会话

**步骤**：
1. 将状态更新为 `killed`
2. 在备注中记录终止原因
3. 等待定时清理任务删除

---

## 使用指南

### 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `operation` | string | ✅ | 操作类型：`create` / `monitor` / `complete` / `kill` |
| `task_info` | object | ✅ (create) | 任务信息（项目、任务描述） |
| `session_id` | string | ✅ (update) | 命名会话唯一标识（sessionKey），如 `session:CORN:agentId` |
| `status` | string | ✅ (update) | 新状态：`active`/`paused`/`completed`/`killed` |

### 输出结果

| 输出项 | 格式 | 说明 |
|--------|------|------|
| `task_board` | Markdown 表格 | 当前活跃任务看板 |
| `session_list` | Markdown 表格 | 活跃会话清单 |

### 状态流转图

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
│ 事件记忆 │
└─────────┘
```

---

## 与 metacognition 的集成

```
metacognition/planning
    └── 调用 subagent_tracker 创建任务记录

metacognition/monitoring
    └── 调用 subagent_tracker 更新状态

metacognition/regulation
    └── 调用 subagent_tracker 修改状态 (paused/active)
```

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.1.0 | 2026-04-26 | 统一使用命名会话；工作流1添加上下文共享检查步骤 |
| v1.0.0 | 2026-04-17 | 初始版本，标准化文档规范 |

---

*创建者: 大管家*  
*创建时间: 2026-04-17*
