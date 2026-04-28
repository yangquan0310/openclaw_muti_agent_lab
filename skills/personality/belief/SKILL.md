---
name: belief
description: >
  人格信念子模块。操作 Belief 对象，管理 SOUL.md 中的工作信念、价值观和工作风格。
version: 2.0.0
author: 大管家
dependencies:
  - ../diary
exports:
  - belief_object
  - belief_workflows
  - belief_update_methods
---

# belief

> 人格子模块 - 信念
> 操作 Belief 对象：管理工作信念、价值观和工作风格

---

## 文件说明

| 文件 | 功能 | 说明 |
|------|------|------|
| `SKILL.md` | 开发规范 | 信念与风格更新的执行规范，定义如何修改 Belief 对象 |

本文件告诉 Agent 如何操作 Belief 对象，以及如何同步到 `SOUL.md`。

---

## 对象

### Belief（信念对象）

**说明**：Belief 对象维护 Agent 的工作信念体系，对应 `SOUL.md` 中的「信念」和「风格」章节。

**属性**：

| 属性 | 类型 | 说明 |
|------|------|------|
| `values` | object[] | 价值观列表 `{ name, priority, definition }` |
| `style` | object | 工作风格 `{ interaction, documentation, coding, execution }` |
| `redlines` | string[] | 安全红线列表 |
| `version` | string | 当前版本号 |
| `history` | object[] | 更新历史 `{ date, type, detail }` |

**状态变换**：

```
稳定态（当前信念生效中）
    ↓ Diary 触发信念更新信号
评估中（分析差异）
    ↓ 差异确认
更新中（修改 values / style / redlines）
    ↓ 更新完成
同步中（同步到 SOUL.md）
    ↓ 同步完成
返回稳定态
```

---

## 工作流（修改 Belief 对象的方法）

### 工作流1：工作信念更新

**说明**：通过本工作流修改 Belief 对象的 `values` 和 `redlines` 属性。

**步骤**：
1. **识别变化原因**
   - 实践中发现原有信念不适用
   - 用户明确反馈价值观冲突
   - 团队规范调整

2. **评估影响范围**
   - 仅影响当前 Agent
   - 影响多个 Agent（需同步）
   - 影响整个实验室（需规范更新）

3. **更新 Belief 对象**（修改 `Belief.values`）
   - 修改「信念」章节
   - 调整价值观优先级
   - 更新安全红线

4. **同步到 `SOUL.md`**（Belief.sync()）
   - 更新 `lab_repository/SOUL.md`

5. **通知相关方**（如影响其他 Agent）

6. **记录更新历史**（修改 `Belief.history`）

---

### 工作流2：工作风格更新

**说明**：通过本工作流修改 Belief 对象的 `style` 属性。

**步骤**：
1. **识别变化维度**
   - 交互风格：与用户和团队的交互方式
   - 文档风格：文档写作的习惯和规范
   - 代码风格：代码编写的方式和偏好
   - 任务执行风格：执行任务的方法和习惯

2. **评估变化原因**
   - 用户明确反馈风格偏好
   - 实践中发现风格效率问题
   - 团队协作需要统一风格

3. **更新 Belief 对象**（修改 `Belief.style`）
   - 修改「风格」章节

4. **同步到 `SOUL.md`**（Belief.sync()）
   - 更新 `lab_repository/SOUL.md`

5. **通知相关方**

6. **记录更新历史**（修改 `Belief.history`）

---

## 使用指南

### 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `update_category` | string | ✅ | 更新类别：`belief` / `style` |
| `dimension` | string | ✅ | 维度：work_belief / value_priority / safety_redline / interaction / documentation / coding / execution |
| `old_definition` | string | ✅ | 原定义 |
| `new_definition` | string | ✅ | 新定义 |
| `update_reason` | string | ✅ | 更新原因 |

### 输出结果

| 输出项 | 格式 | 说明 |
|--------|------|------|
| `belief_update_log` | Markdown | Belief 对象更新的信念记录 |
| `style_update_log` | Markdown | Belief 对象更新的风格记录 |

### 信念更新模板

```markdown
## 信念更新 - YYYY-MM-DD

### 更新的信念
| 信念 | 原定义 | 新定义 | 更新原因 |
|------|--------|--------|----------|
| [信念名] | [原描述] | [新描述] | [原因] |

### 价值观优先级调整
| 优先级 | 价值观 | 调整 |
|--------|--------|------|
| [顺序] | [价值观] | [升/降] |

### 安全红线变化
| 操作 | 红线内容 | 说明 |
|------|----------|------|
| [新增/移除] | [内容] | [说明] |

### 更新位置
- SOUL.md: [章节]
- lab_repository/SOUL.md: [同步状态]
```

### 风格更新模板

```markdown
## 风格更新 - YYYY-MM-DD

### [维度]更新
| 维度 | 原风格 | 新风格 | 更新原因 |
|------|--------|--------|----------|
| [维度] | [原描述] | [新描述] | [原因] |

### 更新位置
- SOUL.md: [章节]
- lab_repository/SOUL.md: [同步状态]
```

---

## 与其他对象的关系

```
Diary.extract() ──→ 检测到信念变化信号
    ↓
Personality ──→ Belief.update(dimension, change)
    ↓
Belief.compare() ──→ 确认差异
    ↓
Belief.update() ──→ 修改 values / style / redlines
    ↓
Belief.sync() ──→ 写入 SOUL.md
```

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v2.0.0 | 2026-04-28 | 面向对象重构，明确 Belief 对象属性及修改方法 |
| v1.0.0 | 2026-04-17 | 初始版本 |

---

*创建者: 大管家*  
*创建时间: 2026-04-17*
