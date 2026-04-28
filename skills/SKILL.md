---
name: agent_self_development
description: >
  Agent 自我发展技能包。基于皮亚杰认知发展理论，将自我发展分为元认知、工作记忆、同化与顺应三大维度，
  提供纯文档规范指导 Agent 理解、构建和迭代自身的元认知能力。
version: 2.0.0
author: 大管家
dependencies: []
exports:
  - metacognition
  - working_memory
  - personality
routes:
  - metacognition/
  - working_memory/
  - personality/
---

# agent_self_development

> Agent 自我发展技能包
> 基于认知发展理论构建的 Agent 自我进化系统

---

## 文件说明

| 文件 | 功能 | 说明 |
|------|------|------|
| `SKILL.md` | 根路由 / 总控 | 技能包总览，提供模块索引和典型工作流 |
| `_meta.json` | 技能元数据 | 机器可读的技能名称、版本、触发词、依赖 |
| `metacognition/SKILL.md` | 元认知模块路由 | 计划、监控、调节三阶段闭环 |
| `working_memory/SKILL.md` | 工作记忆模块路由 | 活跃任务和会话状态管理 |
| `personality/SKILL.md` | 同化顺应模块路由 | 通过日记记录实现自我更新 |
| `README.md` | 人类可读说明 | 项目概述（如需要可额外创建） |

---

## 工作流

### 工作流1：Agent 完整任务生命周期（六阶段闭环）

```
阶段0：会话初始化
    ↓
阶段1：任务决策
    ├── 快速查询 / Cron → 主代理直接执行（跳至阶段5）
    └── 复杂任务 → 进入闭环
        ↓
阶段2：计划（Planning）→ metacognition/planning/SKILL.md
        ↓
阶段3：执行与监控（Monitoring）→ metacognition/monitoring/SKILL.md
        ↓
阶段4：调节（Regulation）（条件触发）→ metacognition/regulation/SKILL.md
        └── 返回阶段3
        ↓
阶段5：任务完成与归档 → working_memory/memory_table/SKILL.md
```

### 工作流2：每日自我更新

```
每日定时
    ↓
[记录日记] personality/diary/SKILL.md
    ↓
[阅读核心自我] MEMORY.md(核心自我认知) / SOUL.md / IDENTITY.md / skills/README.md
    ↓
[同化顺应分析] 对比日记与核心自我 → 识别更新信号
    ↓
[执行更新] core_self_update / identity_update / belief_style_update / skills_update
    ↓
[同步更新] 更新 IDENTITY.md / SOUL.md / MEMORY.md / 固化个人 skills
    ↓
[记录日志] 生成更新事件文件
```

---

## 使用指南

### 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `task_context` | string | ✅ | 当前任务的上下文描述 |
| `agent_identity` | object | ✅ | 当前 Agent 的身份定义（来自 IDENTITY.md） |
| `memory_state` | object | ❌ | 当前工作记忆状态（如已有活跃任务看板） |

### 输出结果

| 输出项 | 格式 | 说明 |
|--------|------|------|
| `task_plan` | Markdown | 结构化任务计划（planning 阶段） |
| `memory_update` | Markdown 表格 | 更新的工作记忆记录（subagent_tracker） |
| `diary_entry` | Markdown | 发展日记条目（diary 阶段） |
| `identity_patch` | Markdown | 自我更新补丁（可选，同化顺应阶段） |

### 调用方式

本技能包为纯文档规范，无代码实现。其他 Agent 或技能通过读取对应 `SKILL.md` 获取执行规范：

```markdown
<!-- 在其他 SKILL.md 中引用 -->
参见 [agent_self_development/metacognition/planning/SKILL.md](metacognition/planning/SKILL.md)
```

---

## 理论基础

### 皮亚杰认知发展理论

- **同化 (Assimilation)**：将新信息纳入现有认知结构
- **顺应 (Accommodation)**：调整认知结构以适应新信息
- **平衡 (Equilibration)**：在同化与顺应之间寻求动态平衡

### Baddeley 工作记忆模型

- **中央执行系统**：控制和协调认知过程
- **语音环路**：处理语音信息
- **视觉空间画板**：处理视觉空间信息
- **情景缓冲器**：整合多模态信息

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.3.0 | 2026-04-26 | 精简planning工作流，聚焦计划制定和会话管理，依托工作记忆进行会话追踪 |
| v1.1.0 | 2026-04-26 | 将"持久会话"改为"会话"，更新 working_memory、planning、monitoring、subagent_tracker、memory_table 模块 |
| v1.0.0 | 2026-04-17 | 初始版本，创建完整目录结构和标准化文档规范 |

---

*创建者: 大管家*  
*创建时间: 2026-04-17*
