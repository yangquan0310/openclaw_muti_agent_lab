---
name: self
description: >
  人格自我子模块。操作 Self 对象，管理 MEMORY.md 中的核心能力边界和责任边界。
version: 2.0.0
author: 大管家
dependencies:
  - ../diary
exports:
  - self_object
  - self_workflows
  - boundary_update_methods
---

# self

> 人格子模块 - 自我
> 操作 Self 对象：管理核心能力边界和责任边界

---

## 文件说明

| 文件 | 功能 | 说明 |
|------|------|------|
| `SKILL.md` | 开发规范 | 核心自我更新的执行规范，定义如何修改 Self 对象 |

本文件告诉 Agent 如何操作 Self 对象，以及如何同步到 `MEMORY.md`。

---

## 对象

### Self（自我对象）

**说明**：Self 对象维护 Agent 的核心自我认知，对应 `MEMORY.md` 中的「核心自我认知」章节（能力边界、责任边界）。

**属性**：

| 属性 | 类型 | 说明 |
|------|------|------|
| `capabilities` | object[] | 能力边界列表 `{ name, level, verified, description }` |
| `responsibilities` | object[] | 责任边界列表 `{ name, scope, authority }` |
| `boundaries` | string[] | 明确不做的领域 |
| `version` | string | 当前版本号 |
| `history` | object[] | 更新历史 |

**状态变换**：

```
稳定态
    ↓ Diary 触发自我认知变化信号
反思中（基于事件反思）
    ↓ 变化确认
评估中（评估扩展或收缩的合理性）
    ↓ 决策确定
更新中（调用 expand() 或 shrink()）
    ↓ 更新完成
同步中（同步到 MEMORY.md）
    ↓ 同步完成
返回稳定态
```

---

## 工作流（修改 Self 对象的方法）

### 工作流1：能力边界更新

**说明**：通过本工作流修改 Self 对象的 `capabilities` 属性。

**步骤**：
1. **识别变化来源**
   - 掌握新工具或技能
   - 发现原有能力的新应用场景
   - 通过实践验证能力的有效性（扩展）
   - 发现能力盲区（收缩）

2. **评估变化性质**
   - 能力扩展 → 验证能力有效性
   - 能力收缩 → 确认限制必要性

3. **更新 Self 对象**（修改 `Self.capabilities`）
   - 修改「能力边界」表格

4. **同步到 `MEMORY.md`**（Self.sync()）
   - 更新 `lab_repository/IDENTITY.md`

5. **记录更新历史**（修改 `Self.history`）

---

### 工作流2：责任边界更新

**说明**：通过本工作流修改 Self 对象的 `responsibilities` 属性。

**步骤**：
1. **识别变化来源**
   - 承担新的职责（扩展）
   - 职责转移给其他 Agent（收缩）

2. **评估变化性质**
   - 责任扩展 → 确认授权来源
   - 责任收缩 → 确认转移对象

3. **更新 Self 对象**（修改 `Self.responsibilities`）
   - 修改「责任边界」表格

4. **同步到 `MEMORY.md`**（Self.sync()）

5. **记录更新历史**（修改 `Self.history`）

---

## 使用指南

### 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `update_type` | string | ✅ | 更新类型：`capability` / `responsibility` |
| `change_direction` | string | ✅ | 变化方向：`expand` / `shrink` |
| `change_details` | object | ✅ | 变化详情（能力/责任名称、描述、原因） |

### 输出结果

| 输出项 | 格式 | 说明 |
|--------|------|------|
| `update_record` | Markdown | 能力/责任边界更新记录 |
| `identity_patch` | Markdown | 应用到 MEMORY.md 的补丁 |

### 能力边界更新记录模板

```markdown
## 能力边界更新 - YYYY-MM-DD

### 新增能力
| 能力 | 说明 | 验证方式 |
|------|------|----------|
| [能力名] | [描述] | [验证方法] |

### 移除能力
| 能力 | 说明 | 移除原因 |
|------|------|----------|
| [能力名] | [描述] | [原因] |

### 更新位置
- MEMORY.md: [行号范围]
- lab_repository/IDENTITY.md: [同步状态]
```

### 责任边界更新记录模板

```markdown
## 责任边界更新 - YYYY-MM-DD

### 新增责任
| 责任 | 说明 | 授权来源 |
|------|------|----------|
| [责任名] | [描述] | [来源] |

### 移除责任
| 责任 | 说明 | 转移对象 |
|------|------|----------|
| [责任名] | [描述] | [对象] |

### 更新位置
- MEMORY.md: [行号范围]
- lab_repository/IDENTITY.md: [同步状态]
```

---

## 与其他对象的关系

```
Diary.extract() ──→ 检测到自我认知变化信号
    ↓
Personality ──→ Self.update(selfChange)
    ↓
Self.reflect(events)
    ↓
Self.expand() / Self.shrink()
    ↓
Self.sync() ──→ 写入 MEMORY.md
```

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v2.0.0 | 2026-04-28 | 面向对象重构，明确 Self 对象属性及能力边界管理方法 |
| v1.0.0 | 2026-04-17 | 初始版本 |

---

*创建者: 大管家*  
*创建时间: 2026-04-17*
