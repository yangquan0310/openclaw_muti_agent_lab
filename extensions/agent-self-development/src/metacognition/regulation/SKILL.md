---
name: regulation
description: >
  元认知调节子模块。指导 Agent 在 Deviation 创建后分析根因（Attribution）、
  制定调节方案，并在归因完成后撰写 Event 对象。
version: 3.0.0
injected_at: Deviation 创建后触发
module: metacognition
---

# Regulation — 归因分析与 Event 撰写

> 元认知子模块 - 调节阶段
> 在 Monitoring 创建 Deviation 后，分析根因、制定调节方案、撰写事件记录
> **先归因分析，再撰写 Event；重大偏差需请示用户**

---

## 注入上下文

本 skill 在 **Monitoring 创建 Deviation 后** 触发。此时插件已完成以下操作：

| 时机 | 插件已完成的操作 | 存储位置 |
|------|-----------------|----------|
| Deviation 创建后 | 通过 `deviationManager.createDeviation()` 保存 Deviation 记录 | `~/.openclaw/state/agent-self-development/deviations.json` |
| 注入前 | 通过 `attributionManager.analyzeAttribution()` 创建 Attribution 骨架 | `~/.openclaw/state/agent-self-development/attributions.json` |

当前 Deviation 和 Attribution 对象已由插件创建，Agent 负责分析内容并做出决策。

---

## 核心对象（底层存储形态）

### Deviation（偏差记录，由 Monitoring 阶段创建）

**存储位置**：`~/.openclaw/state/agent-self-development/deviations.json`  
**存储键**：`{runId}:{phaseId}`

```json
{
  "runId": "uuid",
  "phaseId": "p2",
  "status": "detected",
  "type": "progress",
  "description": "实际进度落后于计划 30%",
  "severity": "major"
}
```

### Attribution（归因分析）

**存储位置**：`~/.openclaw/state/agent-self-development/attributions.json`  
**存储键**：`{runId}:{deviationId}`

```json
{
  "runId": "uuid",
  "deviationId": "dev-xxx",
  "status": "analyzing",
  "rootCause": "根因分析",
  "adjustmentPlan": {
    "strategy": "调节策略",
    "actions": ["行动1", "行动2"]
  }
}
```

### Event（事件记录，归因完成后撰写）

**存储位置**：`~/.openclaw/memory/{agentId}.sqlite`（`asd_events` 表）  
**聚合位置**：`asd_eventlogs` 表（按日期聚合）

```json
{
  "eventId": "evt-xxx",
  "timestamp": 1234567890000,
  "type": "deviation_resolved",
  "runId": "uuid",
  "summary": "事件摘要：偏差原因、调节措施、结果"
}
```

---

## Agent 职责

### 职责 A：归因分析（detected → acknowledged）

**触发条件**：Deviation.status === `"detected"`

**你需要做的**（决策层）：

1. **阅读 Deviation 记录**
   - 了解偏差发生的阶段（`phaseId`）
   - 了解偏差的类型（`type`）和严重度（`severity`）
   - 了解偏差描述（预期 vs 实际）

2. **根因分析**
   - **计划问题**：Plan 制定不合理？阶段划分有误？任务空间分配不当？
   - **执行问题**：Agent 偏离了 Plan？工具使用错误？会话执行异常？
   - **外部因素**：用户需求变化？资源不足？环境异常？

3. **制定调节方案**

   | 方案 | 适用场景 | 操作 |
   |------|---------|------|
   | **A. 调整 Plan** | 计划本身不合理 | 增删改 phases、重新分配任务空间、回到 draft 重新汇报 |
   | **B. 调整执行** | 执行偏离但计划合理 | 修正当前输出方向、重新执行当前阶段 |
   | **C. 请求用户介入** | critical 级别或需求变更 | 向用户汇报偏差和根因，提供选项，等待决策 |

4. **通知插件完成归因**
   - 撰写 `rootCause`（根因分析）
   - 撰写 `adjustmentPlan`（调节策略 + 具体行动）
   - 告知插件将 Attribution.status 更新为 `"completed"`
   - 告知插件将 Deviation.status 更新为 `"acknowledged"`

**插件已自动完成的**（执行层，无需你操作）：
- 已通过 `deviationManager.createDeviation()` 创建 Deviation 记录
- 已通过 `attributionManager.analyzeAttribution()` 创建 Attribution 骨架
- 已保存到 `deviations.json` 和 `attributions.json`

---

### 职责 B：执行调节并撰写 Event（acknowledged → resolved）

**触发条件**：归因分析已完成，调节方案已制定

**你需要做的**（决策层）：

1. **执行调节方案**
   - 若方案 A（调整 Plan）：修改 Plan 后向用户汇报（如为 major/critical），获得确认后通知插件更新
   - 若方案 B（调整执行）：修正当前输出，重新推进当前阶段
   - 若方案 C（用户介入）：向用户清晰呈现偏差、根因、选项，等待决策

2. **撰写 Event 对象**（调节完成后必做）

   Event 是对本次偏差的完整记录，供后续 development（每日回顾）使用。内容应包括：

   ```markdown
   ## 事件记录

   - **事件类型**：deviation_resolved / tool_error / plan_adjusted / session_aborted
   - **涉及阶段**：{phaseId}
   - **偏差描述**：{Deviation.description}
   - **根因分析**：{Attribution.rootCause}
   - **调节措施**：{Attribution.adjustmentPlan.actions}
   - **结果**：成功解决 / 待观察 / 需进一步处理
   - **影响评估**：对五个人格成分的影响（自我/风格/信念/身份/技能）
   ```

3. **通知插件完成调节**
   - 告知插件将 Deviation.status 更新为 `"resolved"`
   - 告知插件将 Attribution.status 更新为 `"executed"`
   - 通过 `eventManager.recordEvent()` 保存 Event 到长期存储

**插件已自动完成的**（执行层，无需你操作）：
- 已通过 `stateAdapter.saveDeviation()` 和 `stateAdapter.saveAttribution()` 保存对象
- 已通过 `eventManager.recordEvent()` 将 Event 聚合到 `asd_eventlogs`

---

## 决策检查点

在 regulation 阶段结束时，请确认：

- [ ] Deviation 的根因是否已明确区分"计划问题"和"执行问题"？
- [ ] 调节方案是否已权衡成本、风险和收益？
- [ ] 若为 major/critical 级别，是否已向用户汇报并获得确认？
- [ ] Event 对象是否已撰写并保存？（供 development 阶段回顾）
- [ ] Event 内容是否包含：偏差描述、根因、调节措施、结果、影响评估？

---

## 状态流转

```
Monitoring 检测到重大偏差
    ↓ 插件自动创建 Deviation + Attribution
detected
    ↓ Agent 完成根因分析 + 制定调节方案
acknowledged
    ├─ 执行调节方案（调整 Plan / 调整执行 / 用户介入）
    ↓ Agent 撰写 Event
resolved（Deviation）/ executed（Attribution）
    ↓ Event 保存到 asd_eventlogs
    ↓ 返回 Monitoring 继续追踪 / 或返回 Planning 重新制定
```

---

## 与其他 Skill 的关系

| Skill | 注入时机 | 职责边界 |
|-------|---------|---------|
| `planning` | `before_prompt_build` | 提供 Plan 基准，调节后可能需要回到 planning 重新汇报 |
| `monitoring` | `llm_output` | 负责检测偏差并创建 Deviation，触发本 skill 的介入 |
| `development` | `before_prompt_build`（cron） | 每日回顾本阶段撰写的 Event，分析同化/顺应 |

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v3.0.0 | 2026-04-29 | v3 重构：调节核心从"方案制定"扩展为"Attribution + Event 撰写"，明确 Event 在归因完成后撰写，供 development 阶段回顾 |
