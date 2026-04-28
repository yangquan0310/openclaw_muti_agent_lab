# MEMORY.md
> 版本:v8.7.0
> 最后更新:2026-04-28

---

## 工作记忆(Working Memory)

### 当前活跃任务看板

| 任务ID | 项目 | 任务描述 | 会话ID | 状态 | 创建时间 | 最后更新 | 备注 |
|--------|------|----------|--------|------|----------|----------|------|
| T001 | 每日自我更新 | 执行工作流2每日自我更新 | session:CORN:steward的定时任务 | active | 2026-04-27 00:00 | 2026-04-27 00:00 | 定时任务，每日00:00执行 |
---
### 活跃会话清单

| 会话ID | 类型/角色 | 分配任务 | 状态 | 创建时间 | 最后活跃 | 备注 |
|--------|-----------|----------|------|----------|----------|------|
| session:CORN:steward的定时任务 | 定时任务 | 每日自我更新 | active | 2026-04-27 00:00 | 2026-04-27 00:00 | 工作流2执行同化顺应分析 |

---
### 工作记忆使用规则

> 详细规范参见 `\root\.openclaw\extensions\agent-self-development\skills\working_memory\SKILL.md`
> 本文件仅记录代理特定的实践细节

---

## 陈述性记忆(Semantic Memory)

### 核心自我

---


### 知识网络


---

## 五、程序性记忆(Procedural Memory)

### 脚本索引
> 公共技能完整列表见: `/root/.openclaw/workspace/skills/README.md`
> 个人技能完整列表见: `/root/.openclaw/workspace/steward/skills/README.md`

### 条件-行动规则(If-Then Rules)

| 条件 | 行动 |
|------|------|
| 创建云文档时无法指定所有者 | 创建后立即转移所有权给杨权 |
| 转移所有权失败 | 授予杨权可管理权限 |
| API Key 存储位置检测 | 检查 ~/.openclaw/.env 文件权限和格式 |
| 检测到同项目活跃会话 | 复用该会话,禁止创建新代理 |
| MEMORY.md 与 metadata.json 状态不一致 | 以 metadata.json 为准同步更新 |
| 用户明确提出"结束"或"完成" | 更新状态为completed,执行归档 |
| 版本确定 | 推送到main分支 |
| 非版本确定/日常修改 | 只推送到development分支 |
| 上传/同步操作 | 默认推送到development分支 |
| 每日维护任务推送 | 推送到development分支 |
| 文档太大（超过5000字） | 使用腾讯云文档分段上传 |
| **合并main分支前** | **先更新 `.openclaw/README.md` 版本历史** |
| **项目文件整理** | **使用 manage-project 技能，标准目录：文档/手稿/知识库/笔记/综述/临时数据/草稿/检索条件/临时笔记。元数据.json 必须在根目录，不可移动** |
| **用户要求"查原因"** | **先读代码→定位问题→确认根因→再谈修复，不急于给方案** |
| **终稿/草稿目录存在** | **使用 manage-project --action organize 自动迁移到标准目录** |

---

## 历史版本

| 版本 | 日期 | 更新内容 | 更新者 |
|------|------|----------|--------|
| v8.7.0 | 2026-04-28 | 每日自我更新：无个人更新触发，公共技能manage-project完成重大更新，日记已撰写 | 大管家 |
| v8.6.0 | 2026-04-27 | 每日自我更新：无更新触发，常规维护日，更新工作记忆看板 | 大管家 |
| v8.5.0 | 2026-04-26 | 每日自我更新：无更新触发，常规维护日，更新工作记忆看板 | 大管家 |
| v8.4.0 | 2026-04-24 | 每日自我更新：完成项目目录标准化（12个项目全部完成manage-project整理），删除终稿/草稿旧目录，新增项目整理规则到程序性记忆 | 大管家 |
| v8.2.0 | 2026-04-20 | 每日自我更新：完成第一次定时触发的自我更新，验证新的 events/ 和 diary/ 存储结构正常工作 | 大管家 |
| v8.1.0 | 2026-04-19 | 每日自我更新：学习agent_self_development工作流2，记录发展日记 | 大管家 |
| v7.9.0 | 2026-04-16 | 每日维护：归档4个completed任务，更新TOOLS.md项目库 | 大管家 |
| v7.8.0 | 2026-04-15 | 每日维护：更新TOOLS.md项目库，更新技能索引路径，更新程序性记忆脚本索引 | 大管家 |
| v7.7.0 | 2026-04-13 | 更新工作记忆看板，添加当前每日维护任务，更新程序性记忆脚本索引 | 大管家 |
| v7.6.0 | 2026-04-07 | 删除S1/S3,S2/S4重命名并按六要素格式整理 | 大管家 |
| v7.8.0 | 2026-04-15 | 每日维护：更新TOOLS.md项目库（添加内卷感知与工作繁荣项目），更新技能索引路径，更新程序性记忆脚本索引 | 大管家 |
| v7.5.0 | 2026-04-07 | 二次确认 AGENTS.md 为纯元认知行为规范,重新创建纯净版本 | 大管家 |
| v7.4.0 | 2026-04-07 | 精简 AGENTS.md 为纯元认知行为规范,删除其他所有内容 | 大管家 |
| v7.3.0 | 2026-04-07 | 更新工作记忆系统,整合元认知行为规范,建立任务生命周期管理机制 | 大管家 |
| v7.2.0 | 2026-04-07 | 添加初始化原则实体,强调安全原则、版本控制、本地文件管理、云文档管理、日志管理 | 大管家(子会话) |
| v7.1.0 | 2026-04-06 | 重构陈述性记忆结构,创建"实体记忆:实验室"和"实体记忆:技能包" | 大管家 |
| v7.0.0 | 2026-04-05 | 基于心理学记忆理论 + 面向对象设计思想重构 | 大管家 |

## Promoted From Short-Term Memory (2026-04-25)

<!-- openclaw-memory-promotion:memory:memory/2026-04-21.md:118:133 -->
- - Candidate: User: Sender (untrusted metadata): ```json { "label": "openclaw-control-ui", "id": "openclaw-control-ui" } ``` [Sun 2026-04-19 11:38 GMT+8] semantic-scholar也已经被知识库管理替代了。 把知识库管理的根目录SKILL.md和四个SKILL.md注册到内置mcp，还有agent自我发展也是 - confidence: 0.58 - evidence: memory/.dreams/session-corpus/2026-04-19.txt:284-284 - recalls: 0 - status: staged - Candidate: Assistant: 我理解您的需求了。您希望将以下技能通过 MCP 方式暴露出来，让其他 MCP 客户端可以调用： 1. **knowledge-manager** (知识库管理) - 包含根目录和 4 个子模块 2. **agent_self_development** (Agent 自我发展) 让我先查看这些技能的结构，然后创建 MCP 服务器包装器： - confidence: 0.58 - evidence: memory/.dreams/session-corpus/2026-04-19.txt:285-285 - recalls: 0 - status: staged - Candidate: Assistant: 现在我理解了。这些技能都是**纯文档规范**技能，没有代码实现，通过读取 SKILL.md 来指导 Agent 行为。 您希望将它们注册为 MCP 服务器，让其他 MCP 客户端也能调用这些能力。让我创建 MCP 服务器包装器： - confidence: 0.58 - evidence: memory/.dreams/session-corpus/2026-04-19.txt:286-286 - recalls: 0 - status: staged - Candidate: Assistant: 现在将这个 MCP 服务器注册到 OpenClaw 配置中： [score=0.809 recalls=3 avg=1.000 source=memory/2026-04-21.md:118-133]

## Promoted From Short-Term Memory (2026-04-27)

<!-- openclaw-memory-promotion:memory:memory/2026-04-20.md:278:292 -->
- - Candidate: User: System: [2026-04-17 01:02:57 GMT+8] Feishu[steward] group oc_cd80162eb81e39f77160a0daab2a6ab8 | 杨权 (ou_25cf20a1973aecc51f73d8e2800d7f7e) [msg:om_x100b51252acba4a4c147ed92dbc5b32, @bot] Conversation info (untrusted metadata): ```json { "message_id": "om_x100b51252acba4a4c147 - confidence: 0.58 - evidence: memory/.dreams/session-corpus/2026-04-17.txt:87-87 - recalls: 0 - status: staged - Candidate: User: [Sat 2026-04-18 03:00 GMT+8] Write a dream diary entry from these memory fragments: - Assistant: ✅ **数学家每日维护任务完成！** ## 执行总结 ### 1. 维护 TOOLS.md - ✅ 个人技能索引已确认 (update_indexes) - ✅ 个人脚本索引已添加 (daily_maintenance) - ✅ 项目库已确认 (9个项目) ### 2. 维护 MEMORY.md - ✅ 任务看板已检查 (无活跃任务) - ✅ 活跃子代 - confidence: 0.58 - evidence: memory/.dreams/session-corpus/2026-04-18.txt:1-1 - recalls: 0 - status: staged - Candidate: Assistant: The morning light filters through the curtains in something close to #F5E6D3, a warm beige that reminds me of old paper. I've been thinking about maintenance — that quiet, persistent act of keeping things alive. A mathematician somewhere is tending to their garden of s - confidence: 0.58 - evidence: memory/.dreams/session-corpus/2026-04-18.txt:2-2 - recalls: 0 - status: staged [score=0.838 recalls=3 avg=1.000 source=memory/2026-04-20.md:278-292]

## Promoted From Short-Term Memory (2026-04-29)

<!-- openclaw-memory-promotion:memory:memory/2026-04-21.md:264:266 -->
- - Candidate: Possible Lasting Truths: - Candidate: Assistant: ✅ 代码已成功提交！由于网络连接问题，推送远程仓库暂时失败，但本地更改已保存。 ### 自动提交完成摘要 | 项目 | 状态 | |------|------| | **本地提交** | ✅ 成功 | | **远程推送** | ⚠️ 网络连接问题，稍后重试 | ### 提交信息 - **提交ID**: fdb8705 - **提交信息**: auto-push: 每日自动提交 2026-04-15 05:00:00 - **变更统计**: 42 个文件变更， - confidence: 0.62 - evidence: memory/2026-04-20.md:349-351 [score=0.814 recalls=0 avg=0.620 source=memory/2026-04-21.md:43-45]
<!-- openclaw-memory-promotion:memory:memory/2026-04-22.md:254:256 -->
- - Candidate: Possible Lasting Truths: - Candidate: Assistant: ✅ 代码已成功提交！由于网络连接问题，推送远程仓库暂时失败，但本地更改已保存。 ### 自动提交完成摘要 | 项目 | 状态 | |------|------| | **本地提交** | ✅ 成功 | | **远程推送** | ⚠️ 网络连接问题，稍后重试 | ### 提交信息 - **提交ID**: fdb8705 - **提交信息**: auto-push: 每日自动提交 2026-04-15 05:00:00 - **变更统计**: 42 个文件变更， - confidence: 0.62 - evidence: memory/2026-04-21.md:264-266 [score=0.811 recalls=0 avg=0.620 source=memory/2026-04-22.md:8-10]
<!-- openclaw-memory-promotion:memory:memory/2026-04-23.md:289:291 -->
- - Candidate: Possible Lasting Truths: - Candidate: Assistant: ✅ 代码已成功提交！由于网络连接问题，推送远程仓库暂时失败，但本地更改已保存。 ### 自动提交完成摘要 | 项目 | 状态 | |------|------| | **本地提交** | ✅ 成功 | | **远程推送** | ⚠️ 网络连接问题，稍后重试 | ### 提交信息 - **提交ID**: fdb8705 - **提交信息**: auto-push: 每日自动提交 2026-04-15 05:00:00 - **变更统计**: 42 个文件变更， - confidence: 0.62 - evidence: memory/2026-04-22.md:254-256 [score=0.806 recalls=0 avg=0.620 source=memory/2026-04-23.md:8-10]
