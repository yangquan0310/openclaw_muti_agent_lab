---
name: personality
description: >
  人格模块路由。基于皮亚杰认知发展理论，管理 Belief（信念）、Self（自我）、Identity（身份）、Skills（技能）、Diary（日记）五个对象，实现 Agent 持续自我更新。
version: 2.0.0
author: 大管家
dependencies:
  - ../working_memory
exports:
  - belief_object
  - self_object
  - identity_object
  - skills_object
  - diary_object
routes:
  - belief/
  - self/
  - identity/
  - skills/
  - diary/
---

# personality

> 人格模块 - Agent 的持续自我发展系统
> 基于皮亚杰认知发展理论
> 包含 Belief、Self、Identity、Skills、Diary 五个对象

---

## 文件说明

本文件为模块路由，索引以下子模块。Agent 通过阅读本文件了解可调用的子模块及其操作的对象：

| 文件 | 子模块 | 功能 | 操作对象 | 对应文档 |
|------|--------|------|----------|----------|
| `SKILL.md` | 本文件 | 模块路由，索引子模块 | Personality | - |
| `belief/SKILL.md` | 信念 | 更新工作信念、价值观、风格 | Belief 对象 | `SOUL.md` |
| `self/SKILL.md` | 自我 | 更新能力边界、责任边界 | Self 对象 | `MEMORY.md` |
| `identity/SKILL.md` | 身份 | 更新角色集、社会身份 | Identity 对象 | `IDENTITY.md` |
| `skills/SKILL.md` | 技能 | 更新个人技能体系 | Skills 对象 | `skills/README.md` |
| `diary/SKILL.md` | 日记 | 撰写日记、提取触发信号 | Diary 对象 | `diary/YYYY-MM-DD.md` |

---

## 对象

### Personality（人格对象）

人格对象是五个子对象的容器和管理者，负责每日 cron 触发时驱动自我更新流程。

#### 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `belief` | Belief | 信念对象（对应 SOUL.md） |
| `self` | Self | 自我对象（对应 MEMORY.md） |
| `identity` | Identity | 身份对象（对应 IDENTITY.md） |
| `skills` | Skills | 技能对象（对应 skills/ 目录） |
| `diary` | Diary | 日记对象（对应 diary/ 目录） |
| `status` | string | 人格状态：`idle` / `reflecting` / `updating` / `syncing` |

#### 生命周期

```
idle（空闲）
    ↓ 每日 00:00 cron 触发
reflecting（Diary 对象读取 WorkingMemory 事件并撰写日记）
    ↓ 日记撰写完成
updating（对比核心自我，检测变化信号，激活对应子对象）
    ├── 自我认知变化 → Self 对象更新
    ├── 角色变化 → Identity 对象更新
    ├── 信念/风格调整 → Belief 对象更新
    └── 技能变化 → Skills 对象更新
    ↓ 所有更新完成
syncing（同步到 lab_repository）
    ↓ 同步完成
idle
```

---

## 子对象概览

### Belief（信念对象）

**操作目标**：`SOUL.md` 中的「信念」和「风格」章节

**属性**：
- `values`：价值观列表
- `style`：工作风格（交互、文档、代码、执行）
- `redlines`：安全红线
- `version`：版本号

**修改方法**（工作流）：见 `belief/SKILL.md`
- 工作信念更新
- 工作风格更新

**持久化**：更新后同步到 `SOUL.md` 和 `lab_repository/SOUL.md`

---

### Self（自我对象）

**操作目标**：`MEMORY.md` 中的「核心自我认知」章节（能力边界、责任边界）

**属性**：
- `capabilities`：能力边界列表
- `responsibilities`：责任边界列表
- `boundaries`：明确不做的领域
- `version`：版本号

**修改方法**（工作流）：见 `self/SKILL.md`
- 能力边界更新（扩展/收缩）
- 责任边界更新

**持久化**：更新后同步到 `MEMORY.md` 和 `lab_repository/IDENTITY.md`

---

### Identity（身份对象）

**操作目标**：`IDENTITY.md` 中的「角色集」和「群体归属」章节

**属性**：
- `roles`：角色列表（期望、行为、产出）
- `groups`：所属群体
- `relationships`：协作关系
- `version`：版本号

**修改方法**（工作流）：见 `identity/SKILL.md`
- 角色集更新（新增/调整/移除）
- 社会身份更新（加入/离开群体）

**持久化**：更新后同步到 `IDENTITY.md` 和 `lab_repository/IDENTITY.md`

---

### Skills（技能对象）

**操作目标**：`skills/` 目录下的技能索引和技能文档

**属性**：
- `skillIndex`：技能索引列表
- `templates`：技能文档模板
- `deprecated`：已淘汰技能
- `version`：版本号

**修改方法**（工作流）：见 `skills/SKILL.md`
- 同化更新（现有技能细化）
- 顺应更新（新技能创建）
- 技能淘汰与迁移

**持久化**：更新后同步到 `skills/README.md` 和 `lab_repository`

---

### Diary（日记对象）

**操作目标**：`diary/YYYY-MM-DD.md` 文件

**属性**：
- `date`：日记日期
- `entries`：日记条目
- `experiences`：经验记录
- `triggers`：更新触发信号
- `status`：draft / reviewing / completed

**修改方法**（工作流）：见 `diary/SKILL.md`
- 撰写每日发展日记
- 提取更新触发信号

**持久化**：写入 `diary/YYYY-MM-DD.md`

---

## 工作流（对象协作方法）

### 工作流1：任务工作流（六阶段闭环）

> 从接受用户需求到任务完成并归档的完整生命周期。

```
接受用户需求
    ↓
阶段0：会话初始化
    ├── 载入 SOUL.md（Belief 对象当前状态）
    ├── 载入 IDENTITY.md（Identity 对象当前状态）
    ├── 载入 MEMORY.md（Self 对象当前状态）
    └── 初始化 WorkingMemory（读取 Memory 对象看板）
    ↓
阶段1：任务决策
    ├── 快速查询 / Cron → 主代理直接执行（跳至阶段5）
    └── 复杂任务 → 进入 Metacognition 闭环
        ↓
阶段2：计划（Planning）→ metacognition/planning/SKILL.md
        ├── 目标澄清、约束识别
        ├── 任务层级拆解
        ├── 检查 WorkingMemory.Session（复用或创建）
        ├── 会话与工具分配
        └── 在 WorkingMemory.Memory 创建任务记录（状态：active）
        ↓
阶段3：执行监控（Monitoring）→ metacognition/monitoring/SKILL.md
        ├── 检查并复用会话（读取 WorkingMemory.Session）
        ├── 向会话分配任务
        ├── 持续跟踪会话状态
        ├── 更新 WorkingMemory.Memory（最后活跃时间、进度）
        └── 偏差检测（>10% / >80% / >30min）
        ↓
阶段4：调节（Regulation）→ metacognition/regulation/SKILL.md（条件触发）
        ├── 根因分析
        ├── 生成调节方案
        ├── 执行调节（Session.paused → Session.active）
        └── 返回阶段3继续监控
        ↓
阶段5：任务完成与归档 → working_memory/session/SKILL.md
        ├── 更新 Session.status 为 completed
        ├── 记录完成摘要到 WorkingMemory.Memory
        ├── 归档到 Memory：生成 Archive 存入 memory_table
        └── killed 任务：直接删除（不归档）
```

### 工作流2：每日同化与顺应（定时执行）

> 每日 00:00 定时执行，完成系统性反思与自我更新。

**步骤**：

1. **阅读当日事件记忆**（修改 Diary 对象）
   - Diary 读取 `WorkingMemory.Event`（昨日事件）
   - Diary 读取 `WorkingMemory.Memory`（昨日归档）
   - 梳理 completed / killed / regulation 事件的完整脉络

2. **撰写/完善发展日记**（修改 Diary 对象）
   - Diary 写入 `diary/YYYY-MM-DD.md`
   - 整合全天任务回顾
   - 提取跨任务的成功经验与失败教训
   - 评估可复用性，标记需固化的技能点

3. **阅读核心自我与配置文件**
   - 读取 `MEMORY.md`（Self 对象当前状态）
   - 读取 `SOUL.md`（Belief 对象当前状态）
   - 读取 `IDENTITY.md`（Identity 对象当前状态）
   - 读取 `skills/README.md`（Skills 对象当前状态）

4. **同化与顺应分析**（Personality 对象对比 Diary 与核心自我）
   - **同化**：原有内容的细化 → 调用对应子对象的更新方法
   - **顺应**：新结构的出现 → 调用对应子对象的创建方法

5. **检测更新触发信号**（Personality 对象分析 Diary.triggers）
   - [ ] 自我认知变化 → 调用 `self/SKILL.md` 修改 Self 对象
   - [ ] 角色变化 → 调用 `identity/SKILL.md` 修改 Identity 对象
   - [ ] 信念/风格调整 → 调用 `belief/SKILL.md` 修改 Belief 对象
   - [ ] 技能变化 → 调用 `skills/SKILL.md` 修改 Skills 对象

6. **执行相应更新**（修改各子对象）
   - 调用对应子模块 SKILL.md 的方法
   - 更新 `IDENTITY.md` / `SOUL.md` / `MEMORY.md`
   - 固化个人 skills（创建/更新技能文件，更新 `skills/README.md` 索引）
   - 同步到 `lab_repository`

7. **记录更新日志**
   - 将变更记录到 `MEMORY.md` 历史版本
   - 生成 `events/YYYY-MM-DD/HH-MM-SS-self-update.md` 事件文件

---

## 使用指南

### 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `daily_events` | list | ✅ | 今日执行任务清单 |
| `memory_archive` | object | ❌ | 从 WorkingMemory 归档的事件 |
| `current_identity` | object | ✅ | Identity 对象当前状态（IDENTITY.md 内容） |

### 输出结果

| 输出项 | 格式 | 说明 |
|--------|------|------|
| `diary_entry` | Markdown | Diary 对象生成的发展日记条目 |
| `update_log` | Markdown | 自我更新日志 |
| `identity_patch` | Markdown | 身份/信念/技能更新补丁 |

### 同化与顺应判定

| 类型 | 判定标准 | 处理方式 |
|------|----------|----------|
| **同化** | 原有内容的细化 | 调用子对象的更新方法（如 Belief.update()） |
| **顺应** | 新结构的出现 | 调用子对象的创建方法（如 Skills.create()） |

**示例**：
- 同化：工作风格有"细心"，将"细心"操作化为具体流程 → 调用 Belief.update(style)
- 顺应：用户提出全新风格要求（如"不要过度扩展"），需新增约束规则 → 调用 Belief.update(redlines)

---

## 与 WorkingMemory 的关系

```
WorkingMemory (短期)
    └── Session.completed
            ↓ 归档
    Memory.archives
            ↓ 每日 cron
Personality (长期)
    ├── Diary 读取 Event + Memory
    ├── 事件记忆（events/ 目录，陈述性记忆）
    └── 发展日记（diary/ 目录，经验积累）
            ↓ 反思
    Self / Identity / Belief / Skills 更新
```

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v2.0.0 | 2026-04-28 | 面向对象重构，明确 Belief/Self/Identity/Skills/Diary 五个对象及其属性 |
| v1.3.0 | 2026-04-26 | 统一使用会话，取消一次性任务区分 |
| v1.0.0 | 2026-04-17 | 初始版本 |

---

*创建者: 大管家*  
*创建时间: 2026-04-17*
