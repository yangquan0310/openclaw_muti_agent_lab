---
name: event
description: >
  调节事件子模块。操作 Event 对象，记录调节过程中的关键事件，按日期聚合，供人格模块回顾。
version: 2.0.0
author: 大管家
dependencies: []
exports:
  - event_object
  - event_workflows
  - event_types
---

# event

> 调节子模块 - 事件
> 操作 Event 对象：记录调节过程中的关键事件

---

## 文件说明

| 文件 | 功能 | 说明 |
|------|------|------|
| `SKILL.md` | 开发规范 | 事件日志记录的执行规范，定义如何创建和管理 Event 对象 |
| `templates/事件日志模板.md` | 模板 | 创建事件日志时使用的模板 |

本文件告诉 Agent 如何操作 Event 对象。

> **位置说明**：Event 对象原属 WorkingMemory 模块，现移动到 Regulation 子模块下，由 Regulator 对象管理。

---

## 对象

### Event（事件对象）

**说明**：Event 对象记录元认知和调节过程中的关键事件（工具错误、会话创建/完成、偏差检测、调节执行等），按日期聚合，供 Personality.Diary 回顾。

**属性**：

| 属性 | 类型 | 说明 |
|------|------|------|
| `time` | string | 事件时间（ISO 8601） |
| `type` | string | 事件类型（见下表） |
| `runId` | string | 所属运行唯一标识 |
| `source` | string | 事件来源（工具名/模块名） |
| `payload` | object | 事件载荷（错误信息/会话数据等） |
| `date` | string | 聚合日期（YYYY-MM-DD） |

**事件类型**：

| 类型 | 触发场景 | payload 内容 |
|------|----------|-------------|
| `tool_error` | 任意工具报错 | `{ error, toolName, params }` |
| `session_spawn` | 会话创建 | `{ sessionId, purpose, role }` |
| `session_complete` | 会话完成 | `{ sessionId, result, duration }` |
| `deviation_detected` | Monitor 检测到偏差 | `{ type, severity, step }` |
| `regulation_executed` | Regulator 执行调节 | `{ strategy, affectedSteps }` |
| `plan_updated` | Plan 被调节更新 | `{ oldItems, newItems }` |

**状态变换**：

```
不存在
    ↓ 触发事件（工具报错、状态变更、调节执行）
已生成（Event 对象创建）
    ↓ Event 写入持久化存储
已持久化（写入 PluginState events:{date}）
    ↓ 被 Personality.Diary 读取
被引用（用于日记撰写）
    ↓ 30天后（按策略）
已归档（长期存储）
```

---

## 工作流（创建和管理 Event 对象的方法）

### 工作流1：创建事件日志

**说明**：通过本工作流创建 Event 对象并持久化。

**触发条件**：

| 事件类型 | 触发阶段 | 示例 |
|----------|----------|------|
| `session_spawn` | 计划 | 创建文献检索子代理 |
| `deviation_detected` | 监控 | 检测到进度偏差 |
| `regulation_executed` | 调节 | 调整检索策略 |
| `session_complete` | 完成 | 文献检索完成 |
| `session_kill` | 终止 | 终止分析子代理 |
| `plan_updated` | 调节 | 修正分析范围 |
| `tool_error` | 任意阶段 | 工具调用报错 |

**步骤**：
1. **确定事件属性**
   - 设置 `type`：根据触发场景选择事件类型
   - 设置 `source`：记录触发来源（工具名/模块名）
   - 设置 `payload`：填充事件载荷
   - 设置 `runId`：关联当前运行
   - 设置 `time`：当前时间
   - 设置 `date`：当前日期（YYYY-MM-DD）

2. **创建 Event 对象**
   - 使用上述属性构造 Event 对象

3. **持久化**
   - 将 Event 对象追加到 `events:{date}` 存储键

4. **生成文件（可选）**
   - 从 `templates/事件日志模板.md` 复制模板
   - 填写 Event 对象属性
   - 保存到 `events/YYYY-MM-DD/HH-MM-SS-事件描述.md`

---

### 工作流2：读取事件日志

**说明**：通过本工作流读取 Event 对象，供 Diary 对象使用。

**步骤**：
1. **确定日期**
   - 计算目标日期（通常为昨日）

2. **检索 Event 对象**
   - 从 `events:{date}` 读取所有 Event 对象
   - 或扫描 `events/YYYY-MM-DD/*.md` 文件

3. **按时间排序**
   - 按 `time` 属性排序

4. **提取关键信息**
   - 事件类型
   - 执行结果
   - 经验总结

5. **输出**
   - 将 Event 对象列表传递给 Diary 对象

---

### 工作流3：管理事件日志

**说明**：通过本工作流管理 Event 对象的保留策略。

**保留策略**：

| 类型 | 保留时间 | 处理方式 |
|------|----------|----------|
| Event 对象 | 30 天 | 自动归档到长期存储 |
| 发展日记 | 永久 | 保留在 diary/ 目录 |

---

## 存储规范

### 存储位置

- **事件目录**: `~/.openclaw/workspace/{agentId}/events/YYYY-MM-DD/`
- **日记目录**: `~/.openclaw/workspace/{agentId}/diary/`

### 文件命名

**事件日志**：
- **格式**: `HH-MM-SS-事件描述.md`
- **示例**: `14-30-00-创建文献检索子代理.md`
- **完整路径**: `events/2026-04-17/14-30-00-创建文献检索子代理.md`

**发展日记**：
- **格式**: `YYYY-MM-DD.md`
- **示例**: `2026-04-17.md`
- **完整路径**: `diary/2026-04-17.md`

---

## 与 Personality 的关系

```
Event 对象创建（Regulator 中）
    ├── 创建 Event 对象
    └── 添加日记标记
            ↓ (每日 01:00)
    Diary 读取 Event 对象
        └── 读取所有事件日志
                ↓
    Diary 生成日记
        └── 创建 diary/YYYY-MM-DD.md
                ↓ (每日 02:00)
    Personality 自我更新
        ├── Self 更新
        ├── Identity 更新
        ├── Belief 更新
        └── Skills 更新
```

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v2.0.0 | 2026-04-28 | 面向对象重构，明确 Event 对象属性及创建方法；从 WorkingMemory 移动到 Regulation |
| v1.1.0 | 2026-04-19 | 更新存储路径：memory/ → events/ 和 diary/ |
| v1.0.0 | 2026-04-17 | 初始版本 |

---

*创建者: 大管家*  
*创建时间: 2026-04-17*  
*最后更新: 2026-04-19*
