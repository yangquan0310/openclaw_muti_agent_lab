# daily_self_update

> 教务助手每日自我更新脚本
> 基于 agent_self_development 工作流2 执行每日自我更新

---

## 功能说明

本脚本用于教务助手每日自动执行自我更新，包括：

1. **记录发展日记** - 回顾今日任务、提取经验、总结教训
2. **阅读核心自我** - 读取 SOUL.md、IDENTITY.md、MEMORY.md
3. **同化顺应分析** - 对比日记与核心自我，识别更新信号
4. **执行自我更新** - 根据检测到的信号更新配置文件
5. **记录更新日志** - 生成日记文件和更新事件文件

---

## 执行方式

### 定时任务（推荐）

由 HEARTBEAT.md 配置的 cron 任务自动触发：
- 执行时间：每日 00:00（Asia/Shanghai）
- 任务ID：`c513ab6c-5a06-4393-b94b-5692dcafb5e0`

### 手动执行

如需手动执行，请：

1. 读取 `skills/daily_self_update/SKILL.md`
2. 按照「工作流：每日自我更新」章节逐步执行

---

## 输出文件

| 文件 | 位置 | 说明 |
|------|------|------|
| 发展日记 | `memory/YYYY-MM-DD/diary.md` | 每日任务回顾和经验总结 |
| 更新事件 | `memory/YYYY-MM-DD/HH-MM-SS-self_update.md` | 自我更新记录（如执行更新） |

---

## 更新触发条件

脚本会自动检测以下更新信号：

| 检查项 | 更新信号 | 触发动作 |
|--------|----------|----------|
| 自我认知 | 能力边界扩展/收缩 | 更新 IDENTITY.md 能力边界 |
| 角色 | 新增/调整/移除角色 | 更新 IDENTITY.md 角色集 |
| 信念/风格 | 价值观/工作方式变化 | 更新 SOUL.md |
| 技能 | 习得/细化/淘汰技能 | 更新 skills/README.md |

---

## 依赖

- agent_self_development/assimilation_accommodation/diary
- agent_self_development/assimilation_accommodation/core_self_update
- agent_self_development/assimilation_accommodation/identity_update
- agent_self_development/assimilation_accommodation/belief_style_update
- agent_self_development/assimilation_accommodation/skills_update

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0.0 | 2026-04-19 | 初始版本 |

---

*维护者：教务助手 (academicassistant)*
