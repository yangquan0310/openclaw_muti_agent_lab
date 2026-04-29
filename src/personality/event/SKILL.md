# Event

> 事件对象
> 记录任务执行过程中各阶段的关键事件

## 对象

### Event

| 属性 | 类型 | 说明 |
|------|------|------|
| `eventId` | string | 事件唯一标识 |
| `runId` | string | 所属运行 |
| `type` | string | `plan` / `deviation` / `attribution` / `session` / `tool` |
| `phaseId` | string | 所属阶段（可选） |
| `timestamp` | number | 发生时间 |
| `summary` | string | 事件摘要 |
| `data` | object | 事件详情 |

**生命周期**：
- 由各阶段 Manager 在执行过程中记录到 State
- agent_end 时由 EventManager 批量转移到 Memory EventLog

## 工作流

### 记录事件
各阶段 Manager 在执行关键动作时，调用 EventManager.recordEvent()：
1. Plan 制定完成 → type: plan
2. Deviation 检测到 → type: deviation
3. Attribution 完成 → type: attribution
4. Session 创建/完成 → type: session
5. 工具调用错误 → type: tool

### 事件聚合（agent_end）
EventManager 将 State 中所有 Event 按日期聚合到 `memory:event:{YYYY-MM-DD}`。
