# monitoring

> 元认知子模块 - 监控
> 操作 Monitor 对象：任务执行进度跟踪与状态评估

## 对象

### Monitor

| 属性 | 类型 | 说明 |
|------|------|------|
| `runId` | string | 所属运行唯一标识 |
| `targetPlan` | Plan | 引用的 Plan 对象 |
| `lastOutput` | string | 最新 LLM 输出缓存 |
| `deviationFlags` | object[] | 已检测到的偏差列表 |
| `status` | string | `idle` / `tracking` / `alert` / `destroyed` |

**状态变迁**:
```
idle → llm_output 触发 → tracking
  → check() 发现偏差 → alert → Regulator 处理完成 → tracking
  → 任务完成 → destroyed
```

## 工作流

### 标准监控循环
1. **准备上下文**：读取 Plan 对象、Session 对象
2. **记录输出**：将 LLM 输出记录到 `Monitor.lastOutput`
3. **偏差检测**：
   - 未按计划使用指定技能/工具
   - 实际进度与计划偏差超过阈值
   - 发现偏差立即标记 `alert`，触发 Regulator
4. **返回结果**：无偏差则继续 tracking

## 交互

- **输入**：来自 `llm_output` Hook 的 Agent 输出
- **输出**：`deviationFlags` 数组（空表示无偏差）
- **触发**：`alert` 状态时通知 Regulator 介入
