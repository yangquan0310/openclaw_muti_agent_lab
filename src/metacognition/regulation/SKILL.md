# regulation

> 元认知子模块 - 调节
> 操作 Regulator 对象：策略调整与计划修正

## 对象

### Regulator

| 属性 | 类型 | 说明 |
|------|------|------|
| `runId` | string | 所属运行唯一标识 |
| `deviationType` | string | 偏差类型：`progress` / `quality` / `resource` / `goal` |
| `deviationDetails` | object | 偏差详情 |
| `adjustmentPlan` | object | 调节方案 `{ strategy, actions, reason }` |
| `status` | string | `idle` / `analyzing` / `executing` / `completed` / `destroyed` |

**状态变迁**:
```
idle → receive(deviation) → analyzing
  → analyze() → executing
  → execute() → completed
  → 返回 Monitor 继续追踪
```

## 工作流

### 标准调节流程
1. **接收偏差**：从 Monitor 获取 `deviationFlags`
2. **根因分析**：分析偏差的根本原因和影响范围
3. **生成方案**：
   - 方案A：调整 Plan（增删改阶段）
   - 方案B：调整 Session（暂停/恢复/替换）
   - 方案C：请求用户介入（重大偏差）
4. **选择最优方案**：权衡成本、风险、收益
5. **执行调节**：
   - 修改 Plan 对象
   - 修改 Session 对象状态
   - 记录调节决策
6. **返回监控**：Regulator 标记 completed，Monitor 恢复 tracking

## 交互

- **输入**：来自 Monitor 的 `deviationFlags`
- **输出**：修改后的 Plan 对象、Session 状态更新
- **触发**：Monitor 状态为 `alert` 时激活
