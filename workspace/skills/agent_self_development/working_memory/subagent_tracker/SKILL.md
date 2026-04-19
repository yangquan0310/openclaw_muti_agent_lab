---
name: subagent_tracker
description: >
  工作记忆子代理追踪。创建、更新和追踪子代理任务状态，管理子代理生命周期。
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

> 工作记忆 - 子代理追踪
> 创建、更新和追踪子代理任务状态

---

## 文件说明

| 文件 | 功能 | 说明 |
|------|------|------|
| `SKILL.md` | 开发规范 | 子代理追踪的执行规范 |

---

## 工作流

### 工作流1：创建子代理任务

**触发时机**：计划阶段完成、准备创建子代理前

**步骤**：
1. 主代理制定计划
2. 在「当前活跃任务看板」添加记录
   ```markdown
   | 项目 | 任务 | 负责子代理key | 状态 | 创建时间 | 最后更新 | 备注 |
   | [项目] | [任务] | 待分配 | active | [现在] | [现在] | [计划ID] |
   ```
3. 创建子代理（`sessions_spawn`）
4. 获取子代理 key
5. 更新「负责子代理key」字段
6. 在「活跃子代理清单」添加记录
   ```markdown
   | 子代理key | 类型/角色 | 分配任务 | 状态 | 创建时间 | 最后活跃 | 备注 |
   | [key] | [角色] | [任务] | active | [现在] | [现在] | - |
   ```

### 工作流2：监控子代理

**触发时机**：监控阶段定期执行

**步骤**：
1. 定期查询子代理状态（`subagents action=list`）
2. 更新「最后活跃」时间
3. 评估任务进度
4. 更新「备注」字段

### 工作流3：子代理完成

**触发时机**：收到子代理完成通告

**步骤**：
1. 接收子代理完成通告
2. 更新「状态」为 `completed`
3. 在「备注」记录完成摘要
4. 等待定时清理归档

### 工作流4：子代理终止

**触发时机**：用户要求终止子代理

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
| `subagent_key` | string | ✅ (update) | 子代理唯一标识 |
| `status` | string | ✅ (update) | 新状态：`active`/`paused`/`completed`/`killed` |

### 输出结果

| 输出项 | 格式 | 说明 |
|--------|------|------|
| `task_board` | Markdown 表格 | 当前活跃任务看板 |
| `agent_list` | Markdown 表格 | 活跃子代理清单 |

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
| v1.0.0 | 2026-04-17 | 初始版本，标准化文档规范 |

---

*创建者: 大管家*  
*创建时间: 2026-04-17*
