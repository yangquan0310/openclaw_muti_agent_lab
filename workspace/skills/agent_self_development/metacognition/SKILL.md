---
name: metacognition
description: >
  元认知模块。提供计划、监控、调节三阶段闭环模型，帮助 Agent 对认知过程进行认知和监控。
version: 1.0.0
author: 大管家
dependencies:
  - ../working_memory
exports:
  - planning_template
  - monitoring_metrics
  - regulation_strategy_map
routes:
  - planning/
  - monitoring/
  - regulation/
---

# metacognition

> 元认知模块 - 对认知的认知
> 基于「计划 → 监控 → 调节」三阶段闭环模型

---

## 文件说明

| 文件 | 功能 | 说明 |
|------|------|------|
| `SKILL.md` | 模块路由 | 元认知总览，索引三个子阶段 |
| `planning/SKILL.md` | 计划阶段 | 任务拆解、资源分配、策略选择 |
| `monitoring/SKILL.md` | 监控阶段 | 进度跟踪、偏差检测、状态评估 |
| `regulation/SKILL.md` | 调节阶段 | 策略调整、资源重配、计划修正 |

---

## 工作流

### 工作流1：三阶段闭环执行

```
┌─────────┐     ┌─────────┐     ┌─────────┐
│  计划   │ ──→ │  监控   │ ──→ │  调节   │
│Planning │     │Monitoring│    │Regulation│
└─────────┘     └─────────┘     └────┬────┘
      ↑                              │
      └──────────────────────────────┘
              (反馈循环)
```

**步骤**：
1. 调用 `planning/SKILL.md` 制定执行计划
2. 调用 `working_memory/subagent_tracker/SKILL.md` 创建任务记录
3. 调用 `monitoring/SKILL.md` 持续跟踪进度
4. 若检测到偏差，调用 `regulation/SKILL.md` 调整策略
5. 调节完成后返回监控阶段，形成闭环

### 工作流2：快速计划-执行（无偏差场景）

```
[计划] → [监控] → 任务完成
```

---

## 使用指南

### 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `task_description` | string | ✅ | 待执行任务的详细描述 |
| `available_agents` | list | ✅ | 可用子代理列表及其能力 |
| `constraints` | object | ❌ | 时间、资源等约束条件 |

### 输出结果

| 输出项 | 格式 | 说明 |
|--------|------|------|
| `execution_plan` | Markdown | 结构化任务计划 |
| `status_report` | Markdown | 监控阶段状态报告 |
| `adjustment_log` | Markdown | 调节阶段变更记录 |

### 调用方式

```markdown
<!-- 计划阶段 -->
参见 [metacognition/planning/SKILL.md](planning/SKILL.md)

<!-- 监控阶段 -->
参见 [metacognition/monitoring/SKILL.md](monitoring/SKILL.md)

<!-- 调节阶段 -->
参见 [metacognition/regulation/SKILL.md](regulation/SKILL.md)
```

---

## 与 working_memory 的关系

```
元认知 (Metacognition)
    ├── 计划 → 写入 working_memory（创建任务记录）
    ├── 监控 → 读取 working_memory（获取任务状态）
    └── 调节 → 更新 working_memory（修改任务状态）
```

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0.0 | 2026-04-17 | 初始版本，标准化文档规范 |

---

*创建者: 大管家*  
*创建时间: 2026-04-17*
