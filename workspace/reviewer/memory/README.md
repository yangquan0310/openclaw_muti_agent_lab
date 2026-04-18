# Memory 文件夹

> 大管家（Steward）记忆存储目录
> 遵循 `agent_self_development/assimilation_accommodation/diary/SKILL.md` 规范维护发展日记与事件记忆

---

## 功能说明

本文件夹用于存储大管家的**发展日记**和**事件记忆**，是 `assimilation_accommodation` 同化顺应模块的实践落地目录。

- **发展日记**：每日任务回顾、成功经验、失败教训、新技能记录
- **事件记忆**：从工作记忆中归档的 completed/killed 任务记录
- **更新日志**：自我更新（IDENTITY/SOUL）的变更记录

---

## 文件夹结构

```
memory/
├── README.md                          # 本文件 - 记忆目录说明与规范
└── YYYY-MM-DD/                        # 日期目录
    ├── diary.md                       # 当日发展日记
    └── HH-MM-SS-{event}.md            # 事件记忆（按时间顺序）
```

---

## 发展日记模板

> 完整规范参见 `skills/agent_self_development/assimilation_accommodation/diary/SKILL.md`

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

```

---

## 事件记忆归档格式

> 由 `working_memory/memory_table/SKILL.md` 定时清理任务自动生成，按时间顺序存入日期目录

### 文件命名规范

```
HH-MM-SS-{event_type}.md
```

| 字段 | 说明 | 示例 |
|------|------|------|
| `HH-MM-SS` | 事件发生时间（24小时制） | `04-00-00` |
| `{event_type}` | 事件类型 | `completed`、`killed`、`regulation`、`self-update` |

### 示例事件文件

```markdown
# 04-00-00-completed.md

## 任务完成
| 子代理key | 类型/角色 | 分配任务 | 完成时间 | 备注 |
|-----------|-----------|----------|----------|------|
| [key] | [类型] | [任务] | [时间] | [摘要] |
```

---

## 与 agent_self_development 的关系

```
agent_self_development
    └── assimilation_accommodation/diary/SKILL.md  （规范源）
            ↓ 实践落地
steward/memory/
    └── YYYY-MM-DD/
        ├── diary.md              （发展日记）
        └── HH-MM-SS-{event}.md   （事件记忆，按时间顺序）
```

---

## 使用方式

1. **每日撰写**：任务结束后按模板撰写当日 `YYYY-MM-DD/diary.md`
2. **定时归档**：每日 04:00 由 `维护工作记忆` 技能自动归档事件记忆到 `YYYY-MM-DD/HH-MM-SS-{event}.md`
3. **触发更新**：检测到能力/角色/信念/技能变化时，以 `self-update` 类型事件记录在同日目录下

---

*维护者：大管家（Steward）*  
*规范来源：`skills/agent_self_development/assimilation_accommodation/diary/SKILL.md`*  
*最后更新：2026-04-18*
