---
name: regulation
description: >
  元认知调节子模块。操作 Regulator 对象，当 Monitor 对象检测到偏差时，进行策略调整、资源重配和计划修正。
version: 2.0.0
author: 大管家
dependencies:
  - ../../working_memory/session
exports:
  - regulator_object
  - regulator_workflows
  - adjustment_strategies
---

# regulation

> 元认知子模块 - 调节
> 操作 Regulator 对象：策略调整与计划修正

---

## 文件说明

| 文件 | 功能 | 说明 |
|------|------|------|
| `SKILL.md` | 开发规范 | 调节阶段的执行规范，定义如何修改 Regulator 对象、Plan 对象和 Session 对象 |
| `events/SKILL.md` | 事件 | 记录调节过程中的关键事件 | Event 对象 |

本文件告诉 Agent 如何操作 Regulator 对象，以及如何通过 Regulator 对象修改 Plan 对象和 Session 对象。

Event 对象由 Regulator 对象管理，见 `events/SKILL.md`。

---

## 对象

### Regulator（调节对象）

**说明**：Regulator 对象接收 Monitor 对象的偏差报告，分析根因，生成并执行调节方案。

**属性**：

| 属性 | 类型 | 说明 |
|------|------|------|
| `runId` | string | 所属运行唯一标识 |
| `deviationType` | string | 偏差类型：`progress` / `quality` / `resource` / `goal` |
| `deviationDetails` | object | 偏差详情 `{ expected, actual, severity, affectedSteps }` |
| `adjustmentPlan` | object | 调节方案 `{ strategy, actions, newPlanItems }` |
| `status` | string | `idle` / `analyzing` / `executing` / `completed` / `destroyed` |

**状态变换**：

```
不存在（null）
    ↓ Monitor.deviation() 触发
待命中（idle）
    ↓ Metacognition.regulate(deviation)
分析中（analyzing，调用 analyze()）
    ↓ 根因明确
方案生成中（调用 generateOptions()）
    ↓ 方案选定
执行中（executing，调用 execute()）
    ↓ 调节完成
完成态（completed）
    ↓ 返回 Monitor 继续追踪
销毁态（destroyed）
```

---

## 工作流（修改 Regulator 对象、Plan 对象和 Session 对象的方法）

### 工作流1：标准调节流程

**说明**：通过本工作流修改 Regulator 对象的 `deviationType`、`deviationDetails` 和 `adjustmentPlan`，并修改 Plan 对象和 Session 对象。

**步骤**：
1. **偏差根因分析**（修改 `Regulator.deviationDetails`）
   - 分析偏差的根本原因
   - 评估偏差对整体任务的影响
   - 填充 `deviationDetails` 属性

2. **影响范围评估**
   - 识别受影响的子任务（Plan.items 中的步骤）
   - 评估是否需要调整最终交付物

3. **生成调节方案**（修改 `Regulator.adjustmentPlan`）
   - 方案A: [描述]
   - 方案B: [描述]
   - 方案C: [描述]
   - 将选定方案写入 `adjustmentPlan`

4. **选择最优方案**
   - 权衡成本、风险、收益
   - 确认方案可行性

5. **执行调节**（修改 Plan 对象和 Session 对象）
   - 更新 Plan 对象的 `items` 和 `sessionAssignments`（如需要）
   - 更新 Session 对象的状态（`paused` → `active`）
   - 通知相关 Session
   - 记录调节决策到 Regulator 对象

6. **返回监控阶段**
   - Regulator.status 设为 `completed`
   - 继续执行并跟踪（返回 Monitor 对象）

---

## 使用指南

### 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `deviation_type` | string | ✅ | 偏差类型：progress / quality / resource / goal |
| `deviation_details` | object | ✅ | 偏差详情（来自 Monitor 对象） |
| `current_plan` | object | ✅ | 当前 Plan 对象 |

### 输出结果

| 输出项 | 格式 | 说明 |
|--------|------|------|
| `adjustment_log` | Markdown | Regulator 对象生成的调节决策记录 |
| `updated_plan` | Markdown | 修正后的 Plan 对象（如需要） |
| `notifications` | list | 需要发送给 Session 的通知清单 |

### 常见偏差与调节策略

| 偏差类型 | 典型表现 | 调节策略 | 修改的对象 |
|----------|----------|----------|-----------|
| 进度落后 | 完成度 < 计划度 | 增加资源、并行执行、缩小范围 | Plan.items, Session |
| 质量不符 | 输出不达标 | 调整方法、增加检查点、更换工具 | Plan.items, Session |
| 资源不足 | 会话/工具不可用 | 寻找替代资源、调整计划、请求支援 | Plan.sessionAssignments |
| 目标模糊 | 需求不明确 | 暂停任务、澄清需求、重新定义 | Plan.items |

### 状态更新格式（修改 Session 对象）

调节过程中，更新 WorkingMemory.Memory 中的会话清单：

```markdown
### 状态更新（调节中）
| 项目 | 任务 | 会话ID | 状态 | 创建时间 | 最后更新 | 备注 |
|------|------|---------------|------|----------|----------|------|
| [项目] | [任务] | [key] | paused | [时间] | [现在] | 调节中: [原因] |

### 调节完成后
| 项目 | 任务 | 会话ID | 状态 | 创建时间 | 最后更新 | 备注 |
|------|------|---------------|------|----------|----------|------|
| [项目] | [任务] | [key] | active | [时间] | [现在] | 已调节: [方案] |
```

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v2.0.0 | 2026-04-28 | 面向对象重构，明确 Regulator 对象属性及修改 Plan/Session 对象的方法 |
| v1.0.0 | 2026-04-17 | 初始版本 |

---

*创建者: 大管家*  
*创建时间: 2026-04-17*
