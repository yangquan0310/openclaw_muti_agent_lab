---
name: identity
description: >
  人格身份子模块。操作 Identity 对象，管理 IDENTITY.md 中的角色集和社会身份。
version: 2.0.0
author: 大管家
dependencies:
  - ../diary
exports:
  - identity_object
  - identity_workflows
  - role_management_methods
---

# identity

> 人格子模块 - 身份
> 操作 Identity 对象：管理角色集和社会身份

---

## 文件说明

| 文件 | 功能 | 说明 |
|------|------|------|
| `SKILL.md` | 开发规范 | 身份更新的执行规范，定义如何修改 Identity 对象 |

本文件告诉 Agent 如何操作 Identity 对象，以及如何同步到 `IDENTITY.md`。

---

## 对象

### Identity（身份对象）

**说明**：Identity 对象维护 Agent 的角色定义和群体归属，对应 `IDENTITY.md` 中的「角色集」和「群体归属」章节。

**属性**：

| 属性 | 类型 | 说明 |
|------|------|------|
| `roles` | object[] | 角色列表 `{ name, expectations, behaviors, outputs }` |
| `groups` | string[] | 所属群体/团队 |
| `relationships` | object[] | 协作关系 `{ agent, role, mode }` |
| `version` | string | 当前版本号 |
| `history` | object[] | 更新历史 |

**状态变换**：

```
稳定态
    ↓ Diary 触发身份更新信号
评估中（分析角色变化影响）
    ↓ 变化确认
更新中（add / update / remove）
    ↓ 更新完成
通知中（通知受影响协作者）
    ↓ 通知完成
同步中（同步到 IDENTITY.md）
    ↓ 同步完成
返回稳定态
```

---

## 工作流（修改 Identity 对象的方法）

### 工作流1：角色集更新

**说明**：通过本工作流修改 Identity 对象的 `roles` 属性。

**步骤**：
1. **识别变化类型**
   - 新增角色：被分配新的职责角色、在项目中承担新功能
   - 角色调整：角色期望变化、行为模式优化、产出标准调整
   - 角色移除：职责转移、项目结束、角色合并

2. **定义/更新角色**（修改 `Identity.roles`）
   - 角色期望（Role Expectations）
   - 角色行为（Role Behaviors）
   - 角色产出

3. **更新 Identity 对象**
   - 修改「角色集」章节

4. **同步到 `IDENTITY.md`**（Identity.sync()）
   - 更新 `lab_repository/IDENTITY.md`

5. **通知相关 Agent**（Identity.notifyPeers()）
   - 告知身份变化（如影响协作）

6. **记录更新历史**（修改 `Identity.history`）

---

### 工作流2：社会身份更新

**说明**：通过本工作流修改 Identity 对象的 `groups` 和 `relationships` 属性。

**步骤**：
1. **识别群体变化**
   - 加入新的团队/组织
   - 离开原有团队/组织
   - 群体认同调整

2. **更新协作网络**（修改 `Identity.relationships`）
   - 新的协作关系建立
   - 协作模式调整
   - 冲突与协调机制更新

3. **同步到 `IDENTITY.md`**（Identity.sync()）

4. **记录更新历史**（修改 `Identity.history`）

---

## 使用指南

### 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `change_type` | string | ✅ | 变化类型：`role_add` / `role_update` / `role_remove` / `group_change` |
| `role_name` | string | ✅ (role_*) | 角色名称 |
| `group_name` | string | ✅ (group_*) | 群体名称 |
| `change_details` | object | ✅ | 变化详情 |

### 输出结果

| 输出项 | 格式 | 说明 |
|--------|------|------|
| `role_definition` | Markdown | Identity 对象生成的角色定义文档 |
| `update_log` | Markdown | 身份更新记录 |

### 角色定义模板

```markdown
### [角色名称]

**角色期望（Role Expectations）**
- 期望1: [描述]
- 期望2: [描述]

**角色行为（Role Behaviors）**
- 场景1: [条件] → [行为]
- 场景2: [条件] → [行为]

**角色产出**
- 产出1: [描述]
- 产出2: [描述]
```

### 更新记录模板

```markdown
## 身份更新 - YYYY-MM-DD

### 角色变化
| 操作 | 角色 | 说明 | 影响 |
|------|------|------|------|
| [新增/调整/移除] | [角色名] | [描述] | [影响范围] |

### 群体归属变化
| 操作 | 群体 | 说明 |
|------|------|------|
| [加入/离开] | [群体名] | [描述] |

### 更新位置
- IDENTITY.md: [章节]
- lab_repository/IDENTITY.md: [同步状态]

### 通知记录
- [Agent名称]: [通知内容]
```

---

## 与其他对象的关系

```
Diary.extract() ──→ 检测到角色变化信号
    ↓
Personality ──→ Identity.update(roleChange)
    ↓
Identity.addRole() / updateRole() / removeRole()
    ↓
Identity.notifyPeers()
    ↓
Identity.sync() ──→ 写入 IDENTITY.md
```

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v2.0.0 | 2026-04-28 | 面向对象重构，明确 Identity 对象属性及角色管理方法 |
| v1.0.0 | 2026-04-17 | 初始版本 |

---

*创建者: 大管家*  
*创建时间: 2026-04-17*
