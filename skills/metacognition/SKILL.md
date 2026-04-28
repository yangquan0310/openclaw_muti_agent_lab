---
name: metacognition
description: >
  元认知模块路由。提供计划、监控、调节三个子模块的索引。Agent 通过阅读本文件了解可调用的子模块及其对象关系。
version: 2.0.0
author: 大管家
dependencies:
  - ../working_memory
exports:
  - planning_object
  - monitoring_object
  - regulation_object
routes:
  - planning/
  - monitoring/
  - regulation/
---

# metacognition

> 元认知模块 - 对认知的认知
> 管理 Plan（计划）、Monitor（监控）、Regulator（调节）三个对象的生命周期

---

## 文件说明

本文件为模块路由，索引以下子模块。Agent 根据当前阶段调用对应子模块的 SKILL.md：

| 文件 | 子模块 | 功能 | 操作对象 |
|------|--------|------|----------|
| `SKILL.md` | 本文件 | 模块路由，索引子模块 | Metacognition |
| `planning/SKILL.md` | 计划 | 任务拆解、会话分配、计划生成 | Plan 对象 |
| `monitoring/SKILL.md` | 监控 | 进度跟踪、偏差检测、状态评估 | Monitor 对象 |
| `regulation/SKILL.md` | 调节 | 策略调整、资源重配、计划修正 | Regulator 对象 |

---

## 对象

### Metacognition（元认知对象）

元认知对象是三个子对象的容器和管理者，负责在正确时机激活正确的子对象。

#### 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `plan` | Plan | 当前运行的计划对象 |
| `monitor` | Monitor | 当前运行的监控对象 |
| `regulator` | Regulator | 当前运行的调节对象（条件激活） |
| `status` | string | 元认知状态：`idle` / `planning` / `executing` / `regulating` |

#### 生命周期

```
idle（空闲）
    ↓ 接收复杂任务
draft（Plan 草稿，Agent 制定并汇报）
    ↓ 汇报完成
pending_approval（等待用户确认）
    ├─ 用户确认 → active
    ├─ 用户修改 → draft（重新汇报）
    └─ 用户取消 → completed
active（Monitor 对象激活，按 phases 执行）
    ↓ 检测到偏差
regulating（Regulator 对象激活）
    ├─ 调节完成 → 返回 active
    └─ 重大变更需重规划 → draft（重新汇报）
    ↓ 所有 phases 完成
completed（任务完成）
    ↓ agent_end
idle（销毁所有子对象）
```

**核心原则：必须先汇报，确认后才能执行。**

---

## 子对象概览

### Plan（计划对象）

**操作目标**：构建一套完整的任务上下文语境，不只是步骤列表

**属性**：
- `runId`：运行标识
- `prompt`：用户原始输入
- `context`：任务上下文（goal / constraints / successCriteria）
- `workspace`：工作空间（sessions / artifacts / tools）
- `execution`：执行计划（phases / currentPhase）
- `status`：draft / active / completed / destroyed

**Phase（阶段）**：
- `id`：阶段标识
- `name`：阶段名称
- `goal`：阶段目标
- `sessionId`：分配的任务空间
- `taskFamily`：任务族（CODE/RESEARCH/ANALYSIS/WRITING/TEST/DESIGN/TASK）
- `outputs`：预期产出
- `status`：pending / active / completed / skipped

**修改方法**（工作流）：见 `planning/SKILL.md`
- 制定完整任务上下文
- 阶段化推进
- 任务空间管理

---

### Monitor（监控对象）

**操作目标**：跟踪 Agent 输出与 Plan 的偏离程度

**属性**：
- `targetPlan`：引用的 Plan 对象
- `lastOutput`：最新 LLM 输出
- `deviationFlags`：已检测到的偏差列表
- `status`：idle / tracking / alert / destroyed

**修改方法**（工作流）：见 `monitoring/SKILL.md`
- 标准监控循环
- 偏差检测与告警

---

### Regulator（调节对象）

**操作目标**：接收偏差报告，生成并执行调节方案

**属性**：
- `deviationType`：偏差类型
- `deviationDetails`：偏差详情
- `adjustmentPlan`：调节方案
- `status`：idle / analyzing / executing / completed / destroyed

**修改方法**（工作流）：见 `regulation/SKILL.md`
- 标准调节流程

---

## 工作流（对象协作方法）

### 工作流1：三阶段闭环执行

```
┌─────────┐     ┌─────────┐     ┌─────────┐
│  Plan   │ ──→ │ Monitor │ ──→ │Regulator│
│ 计划对象 │     │ 监控对象 │     │ 调节对象 │
└─────────┘     └─────────┘     └────┬────┘
      ↑                              │
      └──────────────────────────────┘
              (反馈循环)
```

**步骤**：
1. 调用 `planning/SKILL.md` 修改 Plan 对象（生成计划）
2. Plan 对象向 WorkingMemory.Session 发送创建请求
3. 调用 `monitoring/SKILL.md` 修改 Monitor 对象（启动监控）
4. 若 Monitor 对象检测到偏差，调用 `regulation/SKILL.md` 修改 Regulator 对象
5. Regulator 对象修改 Plan 对象和 Session 对象后，返回 Monitor 继续追踪

### 工作流2：快速计划-执行（无偏差场景）

```
[修改 Plan 对象] → [修改 Monitor 对象] → 任务完成
```

---

## 使用指南

### 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `task_description` | string | ✅ | 待执行任务的详细描述 |
| `available_sessions` | list | ✅ | 可用会话列表及其能力 |
| `constraints` | object | ❌ | 时间、资源等约束条件 |

### 输出结果

| 输出项 | 格式 | 说明 |
|--------|------|------|
| `execution_plan` | Markdown | Plan 对象生成的结构化任务计划 |
| `status_report` | Markdown | Monitor 对象输出的状态报告 |
| `adjustment_log` | Markdown | Regulator 对象输出的变更记录 |

### 调用方式

```markdown
<!-- 计划阶段：修改 Plan 对象 -->
参见 [metacognition/planning/SKILL.md](planning/SKILL.md)

<!-- 监控阶段：修改 Monitor 对象 -->
参见 [metacognition/monitoring/SKILL.md](monitoring/SKILL.md)

<!-- 调节阶段：修改 Regulator 对象 -->
参见 [metacognition/regulation/SKILL.md](regulation/SKILL.md)
```

---

## 与 WorkingMemory 的关系

```
Metacognition.Plan 修改后 ──→ WorkingMemory.Session 创建/更新
Metacognition.Monitor 追踪中 ──→ WorkingMemory.Session 状态更新
Metacognition.Regulator 调节中 ──→ WorkingMemory.Session 暂停/恢复
```

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v2.0.0 | 2026-04-28 | 面向对象重构，明确 Plan/Monitor/Regulator 三个对象及其属性 |
| v1.0.0 | 2026-04-17 | 初始版本 |

---

*创建者: 大管家*  
*创建时间: 2026-04-17*
