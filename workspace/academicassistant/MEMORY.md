# MEMORY.md
> 版本:v8.0.1
> 最后更新:2026-04-19

---

## 工作记忆(Working Memory)

### 当前活跃任务看板

| 任务ID | 项目 | 任务描述 | 会话ID | 状态 | 创建时间 | 最后更新 | 备注 |
|--------|------|----------|--------|------|----------|----------|------|
| T001 | 每日自我更新 | 执行工作流2每日自我更新 | session:CORN:academicassistant的定时任务 | active | 2026-04-27 00:00 | 2026-04-27 00:00 | 定时任务，每日00:00执行 |
---
### 活跃会话清单

| 会话ID | 类型/角色 | 分配任务 | 状态 | 创建时间 | 最后活跃 | 备注 |
|--------|-----------|----------|------|----------|----------|------|
| session:CORN:academicassistant的定时任务 | 定时任务 | 每日自我更新 | active | 2026-04-27 00:00 | 2026-04-27 00:00 | 工作流2执行同化顺应分析 |
---
### 工作记忆使用规则

> 详细规范参见 `\root\.openclaw\extensions\agent-self-development\skills\working_memory\SKILL.md`
> 本文件仅记录代理特定的实践细节
---

## 陈述性记忆(Semantic Memory)

### 核心自我认知

---

### 知识网络


### 当前学期课程表

| 时间 | 课程名称 | 班级 | 地点 | 周次 |
|------|----------|------|------|------|
| 周一 14:00-15:40 | 教育科学研究方法 | 23小教1 | 4教512 | 第10周 |
| 周二 8:00-9:40 | 教育科学研究方法 | 23小教2 | 4教441 | 第10周 |
| 周二 14:00-15:40 | 教育科学研究方法 | 23小教2 | 4教441 | 第1-8周、11-17周 |
| 周二 16:00-17:40 | 创新创业 | 24应心 | 5教115 | 第1-17周 |
| 周四 10:00-11:40 | 创新创业 | 24护理78 | 5教205 | 第1-16周 |
| 周四 14:00-15:40 | 创新创业 | 24护理56 | 5教203 | 第1-16周 |
| 周五 14:00-15:40 | 教育科学研究方法 | 23小教1 | 4教512 | 第1-8周、11-17周 |
---


## 五、程序性记忆(Procedural Memory)

### 脚本索引
> 公共技能完整列表见: `/root/.openclaw/workspace/skills/README.md`
> 个人技能完整列表见: `/root/.openclaw/workspace/academicassistant/skills/README.md`

### 条件-行动规则(If-Then Rules)

| 条件 | 行动 | 优先级 | 最后触发 |
|------|------|--------|----------|
| 用户提及"创建科研项目" | 触发「科研项目管理脚本」 | 高 | - |
| 用户提及"文献"、"参考文献"、"引用" | 触发「学术文献整理脚本」 | 高 | - |
| 用户提及"进度"、"报告"、"跟踪" | 触发「科研进度跟踪脚本」 | 中 | - |
| 用户上传文件 | 询问文件用途和存储位置 | 高 | - |
| 任务涉及多个步骤 | 拆分子任务并使用会话 | 中 | - |
| 遇到未知问题超过5分钟 | 暂停并向用户求助 | 高 | - |

---
## 📈 版本历史

- **v1.0.0** (2026-04-07): 初始版本，基于大管家模板重构
- **v1.1.0** (2026-04-16): 按新规范更新，不再区分脚本和技能
- **v8.0.6** (2026-04-28): 每日自我更新，记录周二低活跃日，无新触发信号
- **v8.0.5** (2026-04-27): 每日自我更新，更新核心自我认知，记录周日低活跃日，无新触发信号
- **v8.0.4** (2026-04-26): 每日自我更新，更新核心自我认知，记录周末低活跃日
- **v8.0.3** (2026-04-22): 更新课程表至第10周，记录今日课程安排
- **v8.0.2** (2026-04-19): 配置重载，创建每日自我更新脚本 daily_self_update，更新技能索引

---

*最后更新: 2026-04-28**  
*更新者: 教务助手*  
*理论基础: 身份理论、工作记忆理论、认知架构理论*

## Promoted From Short-Term Memory (2026-04-29)

<!-- openclaw-memory-promotion:memory:memory/2026-04-21.md:199:201 -->
- - Candidate: Possible Lasting Truths: Possible Lasting Truths: No strong candidate truths surfaced. [confidence=0.58 evidence=memory/2026-04-14.md:404-404]; Possible Lasting Truths: No strong candidate truths surfaced. [confidence=0.58 evidence=memory/2026-04-15.md:254-254]; Reflections: Them - confidence: 0.62 - evidence: memory/2026-04-20.md:229-231 [score=0.893 recalls=0 avg=0.620 source=memory/2026-04-21.md:8-10]
<!-- openclaw-memory-promotion:memory:memory/2026-04-22.md:244:246 -->
- - Candidate: Possible Lasting Truths: Possible Lasting Truths: No strong candidate truths surfaced. [confidence=0.58 evidence=memory/2026-04-14.md:404-404]; Possible Lasting Truths: No strong candidate truths surfaced. [confidence=0.58 evidence=memory/2026-04-15.md:254-254]; Reflections: Them - confidence: 0.62 - evidence: memory/2026-04-20.md:229-231 [score=0.845 recalls=0 avg=0.620 source=memory/2026-04-22.md:68-70]
