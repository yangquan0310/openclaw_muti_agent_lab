---
name: diary
description: >
  人格日记子模块。操作 Diary 对象，记录每日经验、提取触发信号，驱动其他子对象更新。
version: 2.0.0
author: 大管家
dependencies:
  - ../self
  - ../identity
  - ../belief
  - ../skills
exports:
  - diary_object
  - diary_workflows
  - trigger_extraction_rules
---

# diary

> 人格子模块 - 日记
> 操作 Diary 对象：记录每日经验、提取触发信号

---

## 文件说明

| 文件 | 功能 | 说明 |
|------|------|------|
| `SKILL.md` | 开发规范 | 发展日记的执行规范，定义如何修改 Diary 对象 |
| `read.md` | 阅读指南 | 读取事件日志和归档的参考方法 |

本文件告诉 Agent 如何操作 Diary 对象，以及如何写入 `diary/YYYY-MM-DD.md`。

---

## 对象

### Diary（日记对象）

**说明**：Diary 对象读取 WorkingMemory 的 Event 和 Memory，撰写发展日记，提取可触发自我更新的信号。

**属性**：

| 属性 | 类型 | 说明 |
|------|------|------|
| `date` | string | 日记日期（YYYY-MM-DD） |
| `entries` | object[] | 日记条目 `{ type, content, timestamp }` |
| `experiences` | object[] | 经验记录 `{ scene, method, result, reusability }` |
| `triggers` | object[] | 更新触发信号 `{ target, type, reason, confidence }` |
| `status` | string | `draft` / `reviewing` / `completed` |

**状态变换**：

```
空（未撰写）
    ↓ 每日 cron 触发
draft（草稿中，正在读取事件和撰写）
    ↓ 撰写完成
reviewing（审阅中，对比核心自我）
    ↓ extract() 完成
completed（已完成，triggers 已生成）
    ↓ triggers 分发到各子对象
触发中（向 Self/Identity/Belief/Skills 发送更新请求）
    ↓ 所有更新完成
空（等待次日）
```

---

## 工作流（修改 Diary 对象的方法）

### 工作流1：撰写每日发展日记

**说明**：通过本工作流修改 Diary 对象的 `entries` 和 `experiences` 属性，生成 `diary/YYYY-MM-DD.md`。

**步骤**：
1. **任务回顾**（写入 `Diary.entries`）
   - 列出今日执行的主要任务
   - 记录任务结果（成功/失败）

2. **成功经验提取**（写入 `Diary.experiences`）
   - 场景描述
   - 使用方法
   - 效果评估
   - 可复用性判断（高/中/低）

3. **失败教训总结**（写入 `Diary.entries`）
   - 场景描述
   - 原因分析
   - 改进建议

4. **新技能/知识记录**
   - 技能/知识名称
   - 简要说明

5. **更新触发检查**（生成 `Diary.triggers`）
   - 与核心自我对比：
     - [ ] 自我认知变化（能力边界扩展/收缩）→ `self_change`
     - [ ] 角色变化（新增/调整/移除）→ `identity_change`
     - [ ] 信念/风格调整（价值观/工作方式变化）→ `belief_change`
     - [ ] 技能变化（习得/细化/淘汰）→ `skills_change`

6. **明日计划**
   - 基于今日经验调整明日计划

7. **写入文件**
   - Diary.status 设为 `completed`
   - 生成 `diary/YYYY-MM-DD.md`

---

### 工作流2：读取事件与归档

**说明**：通过本工作流读取 Event 对象和 Memory 对象，为 Diary 对象提供素材。

**步骤**：
1. **读取 Event 对象**
   - 从 `events:{昨日日期}` 读取 Event 对象列表
   - 或扫描 `events/YYYY-MM-DD/*.md`

2. **读取 Memory 对象**
   - 从 `memory_table:{昨日日期}` 读取 Archive 记录

3. **按时间排序**
   - 按事件时间排序

4. **分类整理**
   - completed 事件
   - killed 事件
   - regulation 事件

---

## 使用指南

### 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `date` | string | ✅ | 日记日期，格式 `YYYY-MM-DD` |
| `events` | object[] | ✅ | 昨日 Event 对象列表 |
| `archives` | object[] | ❌ | 昨日 Archive 记录列表 |

### 输出结果

| 输出 | 类型 | 说明 |
|------|------|------|
| 发展日记文件 | Markdown | Diary 对象生成的日记文件，存储在 `diary/YYYY-MM-DD.md` |
| 触发信号列表 | object[] | Diary.triggers，用于驱动其他子对象更新 |

### 日记模板

```markdown
# 日记 - YYYY-MM-DD

## 今日任务回顾

| 任务 | 项目 | 结果 | 备注 |
|------|------|------|------|
| [描述] | [项目] | [成功/失败] | [简要说明] |

## 成功经验

### 经验1: [标题]
- **场景**: [描述]
- **方法**: [描述]
- **效果**: [描述]
- **可复用性**: [高/中/低]

## 失败教训

### 教训1: [标题]
- **场景**: [描述]
- **原因**: [分析]
- **改进**: [建议]

## 更新触发信号

| 目标对象 | 类型 | 原因 | 置信度 |
|----------|------|------|--------|
| Self | 能力扩展 | 掌握了新工具 | 高 |

## 明日计划

- [ ] 计划项1
```

### 触发检测规则

**自动检测需要更新的信号**（基于与核心自我的对比）：
- 日记显示能力边界变化 → 触发 `self_change`
- 连续多次使用新方法成功 → 同化到标准流程
- 发现现有方法不适用的场景 → 顺应调整
- 用户明确反馈偏好变化 → 触发 `belief_change`
- 新角色分配或职责变化 → 触发 `identity_change`
- 习得新的结构化能力 → 触发 `skills_change`

---

## 与其他对象的关系

```
发展日记（Diary 对象对比核心自我后）
    ├── 检测自我认知变化 → 调用 Self 子模块
    ├── 检测角色变化 → 调用 Identity 子模块
    ├── 检测信念/风格调整 → 调用 Belief 子模块
    └── 检测技能变化 → 调用 Skills 子模块
```

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v2.0.0 | 2026-04-28 | 面向对象重构，明确 Diary 对象属性及触发提取方法 |
| v1.0.0 | 2026-04-17 | 初始版本 |

---

*创建者: 大管家*  
*创建时间: 2026-04-17*
