---
name: working_memory
description: >
  工作记忆模块。管理当前活跃任务和**命名会话**状态，基于 Baddeley 工作记忆模型设计。一次性任务执行完即销毁，无需追踪。
version: 1.0.0
author: 大管家
dependencies: []
exports:
  - memory_table_schema
  - subagent_tracker_schema
  - state_definitions
routes:
  - memory_table/
  - subagent_tracker/
---

# working_memory

> 工作记忆模块 - 管理当前活跃任务和**命名会话**状态
> 基于 Baddeley 工作记忆模型
>
> **追踪范围**：只追踪命名会话（通过 `sessionTarget` 指定，如 `session:CORN:agentId` 或 `session:PROJECT:xxx`）。一次性任务（无命名会话）执行完即销毁，无需在工作记忆中追踪。

---

## 文件说明

| 文件 | 功能 | 说明 |
|------|------|------|
| `SKILL.md` | 模块路由 | 工作记忆总览，索引子模块 |
| `memory_table/SKILL.md` | 记忆表管理 | 维护表格结构和数据完整性 |
| `subagent_tracker/SKILL.md` | 会话追踪 | 创建、更新和追踪会话任务状态 |

---

## 定时任务配置

### 定时清理任务

| 属性 | 配置 |
|------|------|
| **执行时间** | `0 0 * * *`（每日 00:00，Asia/Shanghai） |
| **执行方式** | 主代理执行 |
| **触发消息** | `[cron:每日自我更新]` 的一部分 |
| **日志路径** | `events/YYYY-MM-DD/HH-MM-SS-cleanup.md` |

### 清理流程

```
定时触发（每日00:00）
    ↓
1. 扫描「活跃会话清单」
    ↓
2. 筛选 `completed` 状态任务
    ↓
3. 归档到「事件记忆」表格
   - 日期: 当前日期
   - 事件: 会话任务归档
   - 涉及实体: 会话ID（sessionKey）
   - 结果: 任务完成
   - 日志位置: `events/YYYY-MM-DD/HH-MM-SS-completed.md`
    ↓
4. 筛选 `killed` 状态任务
    ↓
5. 直接删除 `killed` 任务（不归档）
    ↓
6. 从清单中删除 `completed` 和 `killed` 任务
    ↓
7. 记录清理日志
```

### 状态说明

| 状态 | 含义 | 处理方式 |
|------|------|----------|
| `active` | 正在执行 | 保留在清单中 |
| `paused` | 暂停等待 | 保留在清单中 |
| `completed` | 已完成 | 归档到事件记忆后删除 |
| `killed` | 被终止 | 直接删除，不归档 |

---

## 工作流

### 工作流1：任务生命周期管理

```
创建任务（planning 阶段调用）
    ↓
状态更新（monitoring 阶段调用）
    ↓
完成 / 终止
    ↓
定时清理（每日 00:00）
    ↓
completed → 归档到事件记忆
killed → 直接删除
```

---

## 使用指南

### 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `operation` | string | ✅ | 操作类型：create / update / archive / cleanup |
| `task_data` | object | ✅ (create/update) | 任务数据 |
| `session_id` | string | ✅ (create/update) | 命名会话唯一标识（sessionKey），如 `session:CORN:agentId` |

### 输出结果

| 输出项 | 格式 | 说明 |
|--------|------|------|
| `task_board` | Markdown 表格 | 当前活跃任务看板（含会话ID列） |
| `session_list` | Markdown 表格 | 活跃会话清单 |
| `cleanup_log` | Markdown | 清理日志（cleanup 时） |

---

## 核心数据结构

### 当前活跃任务看板

```markdown
| 任务ID | 项目 | 任务描述 | 会话ID | 状态 | 创建时间 | 最后更新 | 备注 |
|--------|------|----------|--------|------|----------|----------|------|
| [T001] | [项目名] | [任务描述] | [sessionKey] | [状态] | [时间] | [时间] | [备注] |
```

### 活跃会话清单

```markdown
| 会话ID | 类型/角色 | 分配任务 | 状态 | 创建时间 | 最后活跃 | 备注 |
|--------|-----------|----------|------|----------|----------|------|
| [sessionKey] | [类型] | [任务] | [状态] | [时间] | [时间] | [备注] |
```

> **说明**：会话ID用于追踪命名会话（通过 `sessionTarget` 指定）。所有任务都使用命名会话，不再区分一次性任务。会话ID即 `sessionKey`（如 `session:CORN:agentId`、`session:PROJECT:xxx`）。

---

## 与 assimilation_accommodation 的关系

```
working_memory (短期)
    └── completed 任务
            ↓ 归档
assimilation_accommodation (长期)
    └── 事件记忆表
```

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.3.0 | 2026-04-26 | 统一使用命名会话，取消一次性任务区分；更新核心数据结构表格格式 |
| v1.2.0 | 2026-04-19 | 更新存储路径：memory/ → events/ |
| v1.1.0 | 2026-04-19 | 添加定时任务配置章节，规范定时清理流程 |
| v1.0.0 | 2026-04-17 | 初始版本，标准化文档规范 |

---

*创建者: 大管家*  
*创建时间: 2026-04-17*
