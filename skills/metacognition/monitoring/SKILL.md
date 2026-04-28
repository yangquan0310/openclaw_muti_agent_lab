---
name: monitoring
description: >
  元认知监控子模块。操作 Monitor 对象，负责任务执行过程中的进度跟踪、偏差检测和状态评估。
version: 2.0.0
author: 大管家
dependencies:
  - ../../working_memory/session
exports:
  - monitor_object
  - monitor_workflows
  - deviation_thresholds
---

# monitoring

> 元认知子模块 - 监控
> 操作 Monitor 对象：任务执行进度跟踪与状态评估

---

## 文件说明

| 文件 | 功能 | 说明 |
|------|------|------|
| `SKILL.md` | 开发规范 | 监控阶段的执行规范，定义如何修改 Monitor 对象和 Session 对象 |

本文件告诉 Agent 如何操作 Monitor 对象，以及如何通过 Monitor 对象修改 Session 对象的状态。

---

## 对象

### Monitor（监控对象）

**说明**：Monitor 对象持续跟踪 Agent 输出与 Plan 对象的偏离程度，检测偏差并触发调节。

**属性**：

| 属性 | 类型 | 说明 |
|------|------|------|
| `runId` | string | 所属运行唯一标识 |
| `targetPlan` | Plan | 引用的 Plan 对象 |
| `lastOutput` | string | 最新 LLM 输出缓存 |
| `deviationFlags` | object[] | 已检测到的偏差列表 |
| `status` | string | `idle` / `tracking` / `alert` / `destroyed` |

**状态变换**：

```
不存在（null）
    ↓ Plan 对象就绪后
待命中（idle，等待 Agent 输出）
    ↓ llm_output 触发
追踪中（tracking，已记录输出并检查）
    ↓ check() 发现偏差
告警态（alert，已构造 deviation 消息）
    ↓ Regulator 处理完成
返回追踪中
    ↓ 任务完成
销毁态（destroyed）
```

---

## 工作流（修改 Monitor 对象和 Session 对象的方法）

### 工作流1：自行执行监控

**说明**：通过本工作流修改 Monitor 对象的 `lastOutput`，并更新 Session 对象的状态。

**步骤**：
1. **准备上下文**
   - 读取 Plan 对象的 `items` 和 `sessionAssignments`
   - 读取 Session 对象的当前状态

2. **执行与记录**（修改 `Monitor.lastOutput`）
   - 执行当前步骤
   - 将输出记录到 `Monitor.lastOutput`

3. **结果核验与处理**
   - 对照 Plan 对象定义的成功标准逐项验证
   - 核查版本控制、文件存储、技能执行真实性
   - 核查通过 → 进入下一步
   - 核查未通过 → 重新执行

4. **阶段结果汇总与反馈**（修改 Session 对象）
   - 更新 Memory 对象看板中对应 Session 的状态为 `paused`
   - 汇总所有子任务执行结果

---

### 工作流2：标准监控循环（会话）

**说明**：通过本工作流持续追踪 Session 对象的状态，修改 Monitor 对象和 Session 对象的属性。

**步骤**：
1. **准备上下文**
   - 读取 Plan 对象和 Session 对象

2. **检查并复用会话**（读取/修改 Session 对象）
   - 读取 Memory 对象中的「活跃会话清单」
   - 确认计划阶段分配的 Session 是否存在：
     - 若存在 → 复用该 Session，更新 `Session.lastActive`
     - 若不存在 → 创建新 Session（通过 `sessionTarget` 指定）
   - 更新 Memory 对象任务看板与会话清单

3. **传递上下文与会话执行**
   - 向 Session 传递上下文并执行
   - 更新 Memory 对象（最后活跃时间、进度）

4. **进度追踪与偏差检测**（修改 `Monitor.deviationFlags`）
   - 偏差检查：
     - 未按计划使用指定技能/工具
     - 自行更换方案或使用计划外的其他方案
     - 实际进度与计划偏差超过10%
     - 发现偏差立即暂停执行，详细说明偏差情况
   - 阻塞检查：监控任务处理时长，识别阻塞情况
     - 发现阻塞立即停止硬撑，向用户求助

5. **会话结果同步**
   - 捕获 Session 完成通告，提取结果摘要

6. **结果核验与处理**
   - 核查通过 → 进入下一步
   - 核查未通过 → 要求 Session 修正问题，重新执行

7. **阶段结果汇总与反馈**（修改 Session 对象状态）
   - 更新 Memory 对象看板中对应 Session 的状态为 `paused`
   - 汇总所有子任务执行结果

---

### 工作流3：复用会话监控

**说明**：通过本工作流复用已有 Session 对象并持续监控。

**步骤**：
1. **准备上下文**
2. **检查并复用会话**（读取 Session 对象）
   - 读取 Memory 对象「活跃会话清单」
   - 查找与当前任务共享上下文的 Session：
     - 相同项目/领域
     - 相同任务类型
     - 状态为 `active` 或 `paused`
   - 若找到 → 复用该 Session，更新 `Session.lastActive`
   - 若未找到 → 创建新 Session
3. **执行与监控**（修改 Monitor 对象）
   - 向 Session 传递任务并执行
   - 持续跟踪 Session 状态
   - 偏差检测（>10% / >80% / >30min）
4. **结果核验与处理**
5. **执行反馈**

---

### 工作流4：每日同化顺应监控（定时任务）

**说明**：通过本工作流在每日 cron 时修改 Monitor 对象，监控 Personality 对象的自我更新进度。

**步骤**：
1. **触发时机**：每日 00:00 cron 定时触发 `[cron:每日自我更新]`
2. **执行方式**：主代理直接执行（不创建新 Session）
3. **执行内容**：
   - 阅读前一日事件记忆（WorkingMemory.Event）
   - 撰写/完善发展日记（Personality.Diary）
   - 阅读核心自我与配置文件（Personality 各子对象）
   - 同化与顺应分析
   - 检测更新触发信号
   - 执行相应更新
4. **结果核验**：核验日记是否完成、历史版本是否更新、事件文件是否生成
5. **阶段结果汇总**：更新 Memory 对象看板状态为 `completed`，记录完成摘要

---

## 使用指南

### 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `task_plan` | object | ✅ | Plan 对象输出的任务计划 |
| `current_time` | string | ✅ | 当前时间，格式 `YYYY-MM-DD HH:MM` |
| `session_outputs` | list | ❌ | 会话已提交的产出 |

### 输出结果

| 输出项 | 格式 | 说明 |
|--------|------|------|
| `status_report` | Markdown | Monitor 对象输出的当前任务状态报告 |
| `deviation_flag` | boolean | 是否检测到偏差 |
| `deviation_details` | object | 偏差类型、程度、影响范围 |

### 监控指标（修改 Monitor.deviationFlags 的阈值）

| 指标 | 计算方法 | 阈值 | 触发动作 |
|------|----------|------|----------|
| 进度偏差率 | (计划进度-实际进度)/计划进度 | > 10% | 触发调节 |
| 时间消耗率 | 已用时间/预计总时间 | > 80% | 预警提醒 |
| 会话活跃度 | 最后活跃时间距现在 | > 30min | 检查状态 |

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v2.0.0 | 2026-04-28 | 面向对象重构，明确 Monitor 对象属性及修改 Session 对象的方法 |
| v1.1.0 | 2026-04-26 | 统一使用会话，取消一次性任务区分 |
| v1.0.0 | 2026-04-17 | 初始版本 |

---

*创建者: 大管家*  
*创建时间: 2026-04-17*
