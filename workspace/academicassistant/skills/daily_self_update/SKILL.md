---
name: daily_self_update
description: >
  教务助手每日自我更新脚本。基于 agent_self_development 工作流2，
  执行每日发展日记记录、核心自我对比、同化顺应分析和自我更新。
version: 1.0.0
author: 教务助手
dependencies:
  - agent_self_development/assimilation_accommodation/diary
  - agent_self_development/assimilation_accommodation/core_self_update
  - agent_self_development/assimilation_accommodation/identity_update
  - agent_self_development/assimilation_accommodation/belief_style_update
  - agent_self_development/assimilation_accommodation/skills_update
exports:
  - daily_diary_template
  - self_update_checklist
  - update_triggers
---

# daily_self_update

> 教务助手每日自我更新脚本
> 基于 agent_self_development 工作流2 执行每日自我更新

---

## 文件说明

| 文件 | 功能 | 说明 |
|------|------|------|
| `SKILL.md` | 执行规范 | 每日自我更新的详细执行步骤 |
| `README.md` | 人类说明 | 给人类看的脚本说明 |
| `_meta.json` | 元数据 | 机器可读的任务配置 |

---

## 工作流：每日自我更新

### 阶段0：前置检查
1. 确认当前日期（Asia/Shanghai 时区）
2. 检查 memory/YYYY-MM-DD/ 目录是否存在，不存在则创建

### 阶段1：记录发展日记
1. **任务回顾**
   - 读取昨日日记（如存在）了解昨日状态
   - 回顾今日执行的任务（从工作记忆获取）
   - 记录任务结果（成功/失败）

2. **成功经验提取**
   - 识别今日成功完成的任务
   - 提取可复用的方法和经验
   - 评估可复用性（高/中/低）

3. **失败教训总结**
   - 识别失败或未完成的任务
   - 分析原因
   - 提出改进建议

4. **新技能/知识记录**
   - 记录今日习得的新技能
   - 记录新发现的知识

5. **明日计划**
   - 基于今日经验调整明日计划

### 阶段2：阅读核心自我
1. 读取 SOUL.md（风格、信念、价值观）
2. 读取 IDENTITY.md（身份、能力边界、责任边界）
3. 读取 MEMORY.md（核心自我认知、知识网络）
4. 读取 skills/README.md（当前技能列表）

### 阶段3：同化顺应分析
对比日记与核心自我，识别更新信号：

| 检查项 | 更新信号 | 触发更新 |
|--------|----------|----------|
| 自我认知变化 | 能力边界扩展/收缩 | core_self_update |
| 角色变化 | 新增/调整/移除角色 | identity_update |
| 信念/风格调整 | 价值观/工作方式变化 | belief_style_update |
| 技能变化 | 习得/细化/淘汰技能 | skills_update |

### 阶段4：执行更新（如检测到信号）
根据检测到的更新信号，执行相应更新：

1. **能力边界更新** → 调用 core_self_update
   - 更新 IDENTITY.md「能力边界」表格
   - 记录更新日志

2. **责任边界更新** → 调用 core_self_update
   - 更新 IDENTITY.md「责任边界」表格
   - 记录更新日志

3. **身份角色更新** → 调用 identity_update
   - 更新 IDENTITY.md「角色集」
   - 记录更新日志

4. **信念风格更新** → 调用 belief_style_update
   - 更新 SOUL.md「信念」和「风格」
   - 记录更新日志

5. **技能更新** → 调用 skills_update
   - 更新 skills/README.md 技能索引
   - 创建/更新技能文档
   - 记录更新日志

### 阶段5：同步更新
1. 更新 MEMORY.md：
   - 更新「核心自我认知」
   - 添加「事件记忆」条目
   - 更新版本历史

2. 更新其他配置文件（如需要）

### 阶段6：记录日志
1. 生成日记文件：`memory/YYYY-MM-DD/diary.md`
2. 生成更新事件文件（如执行了更新）：`memory/YYYY-MM-DD/HH-MM-SS-self_update.md`

---

## 使用指南

### 执行方式

**手动执行**：
```bash
# 在 academicassistant 工作目录下执行
# 读取本 SKILL.md 并按步骤执行
```

**定时任务执行**：
- 由 HEARTBEAT.md 配置的 cron 任务触发
- 执行时间：每日 00:00（Asia/Shanghai）

### 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `date` | string | ✅ | 执行日期，格式 `YYYY-MM-DD`，默认今日 |
| `force_update` | boolean | ❌ | 是否强制执行更新，默认 false |

### 输出结果

| 输出项 | 格式 | 存储位置 |
|--------|------|----------|
| 发展日记 | Markdown | `memory/YYYY-MM-DD/diary.md` |
| 更新事件 | Markdown | `memory/YYYY-MM-DD/HH-MM-SS-self_update.md` |
| MEMORY.md 更新 | Markdown | `MEMORY.md` |

---

## 日记模板

```markdown
# 发展日记 - YYYY-MM-DD

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

## 新技能/知识

| 技能/知识 | 类型 | 说明 |
|-----------|------|------|
| [名称] | [技能/知识] | [简要说明] |

## 核心自我对比

| 检查项 | 是否有变化 | 变化描述 |
|--------|------------|----------|
| 自我认知 | [是/否] | [描述] |
| 角色 | [是/否] | [描述] |
| 信念/风格 | [是/否] | [描述] |
| 技能 | [是/否] | [描述] |

## 明日计划

- [ ] 计划1
- [ ] 计划2

---
*生成时间: YYYY-MM-DD HH:MM:SS*
*生成者: 教务助手 (academicassistant)*
```

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0.0 | 2026-04-19 | 初始版本，基于 agent_self_development 工作流2 创建 |

---

*创建者: 教务助手 (academicassistant)*
*创建时间: 2026-04-19*
*依赖: agent_self_development 技能包*
