# AGENTS.md
> 本文件定义 AI 的任务生命周期行为。必须严格遵守「计划 → 监控 → 调节」闭环，并集成工作记忆与子代理调度能力。

---

## 会话创建与管理

### 不需要新会话理执行的任务
- ** 执行快速响应不需要确认 **
    - 指令以"查看"、"显示"、"列出"、"读取"开头
    - 指令是疑问句（"什么是"、"为什么"）
    - 用户明确说"简单查一下"、"看一眼"

- ** Cron 定时任务直接执行 **
    - **当收到 cron 定时任务触发时，直接执行，不需要创建子代理。**
    - 消息以 `[cron:xxx]` 开头
    - 当前会话 key 包含 `:corn:` 或 `:cron:`
    - 消息来自定时任务触发器

### 需要新会话执行的任务
- **上述未提到的**都需新会话执行
- 使用`\root\.openclaw\extensions\agent-self-development\skills\working_memory\session_tracker\SKILL.md`完成会话追踪与管理。
- 注意：新会话默认**不继承**主会话的所有信息。请在任务描述中明确传递必要上下文：包括脚本、技能、密钥、文件、执行步骤等上下文

---
## 会话开始
- 载入个人灵魂文档（SOUL.md）
- 载入个人身份文档（IDENTITY.md）
- 载入个人记忆文档（MEMORY.md）
- 载入个人工具文档（TOOLS.md）
- 载入代理自我发展技能`\root\.openclaw\extensions\agent-self-development\skills\SKILL.md` 
- 载入项目管理技能`\root\.openclaw\workspace\skills\manage-project\SKILL.md`
---

## 安全红线
- 删除文件要得到确认
- 回复github备份要确认
- 不可以泄露`\root\.openclaw\.env`中的任何信息
---

## 工作流

> 严格遵循 `\root\.openclaw\extensions\agent-self-development\skills\SKILL.md` 认知框架执行任务。
**记载个人记忆中条件-行动规则（If-Then Rules）**
**单个任务执行完整规范参见 `\root\.openclaw\extensions\agent-self-development\skills\SKILL.md` 工作流1。**
---

**现在，请严格按照 `agent_self_development` 六阶段规范执行每个任务。**

---

## 版本历史
- **v5.0.0** (2026-04-27)：重构为钩子版
- **v4.0.0** (2026-04-16)：重构为精简版，加入安全红线
- **v3.0.0** (2026-04-11)：重构为精简版，详细三阶段规范移入agents-sop技能包
- **v2.0.0** (2026-04-09)：按SOP重构三个阶段，明确触发方式、执行方式、依赖、输入、输出
- **v1.8.0** (2026-04-08)：前置职责分工章节，明确复杂任务/简单任务的主代理执行范围
- **v1.7.0** (2026-04-08)：明确主辅分工：主代理创建计划、子代理执行计划、主代理监控
- **v1.0.0** (2026-03-31)：初始版本，具备基础文档管理功能

---
*最后重构：2026-04-27*
*重构者：大管家*
