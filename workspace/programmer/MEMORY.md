# MEMORY.md

> **本文件保留工作记忆（当前任务）、程序性记忆（If-Then 规则）和陈述性记忆（知识查询规则）。**

---

## 工作记忆(Working Memory)

### 当前活跃任务看板

| 任务ID | 项目 | 任务描述 | 状态 | 创建时间 | 最后更新 | 备注 |
|--------|------|----------|------|----------|----------|------|
| T001 | [openclaw_muti_agent_lab](https://github.com/yangquan0310/openclaw_muti_agent_lab) | 每日04:00自动提交并推送代码变更到main分支 | active | 2026-04-27 00:00 | 2026-06-12 16:48 | 定时任务，确保代码不丢失；固定会话 `agent:programmer:corn:programmer的定时任务`；2026-06-12 由 development 分支切换至 main 分支（development 已删除） |
| T003 | openclaw-bot-review | 3000端口openclaw-bot-review项目开发与维护，终身项目 | active | 2026-05-21 00:30 | 2026-05-21 09:22 | 待跟进具体需求，stats缓存化已完成（commit 37070b7） |
| T004 | 腾讯云Lighthouse服务器 | 永久维护腾讯云轻量应用服务器（腾讯云Lighthouse） | active | 2026-05-25 21:44 | 2026-05-25 21:44 | 技能：tencentcloud-lighthouse-skill；配置：~/.mcporter/mcporter.json；Region：ap-shanghai；实例ID：lhins-4nn64c7g；公网IP：101.43.20.69 |
| T005 | docker-webdav | 维护 bytemark/webdav 容器（id: a4ef35dd2d1b），端口 80/443 | active | 2026-06-07 12:40 | 2026-06-07 12:40 | 基础设施类，目前唯一运行中的 docker 容器；WebDAV 协议文件服务 |

---


## 陈述性记忆(Declarative Memory)

### 历史任务索引

> **已完成任务归档（按完成时间倒序）**

| 任务ID | 项目 | 任务描述 | 完成时间 | 备注 |
|--------|------|----------|----------|------|
| T002 | agent-self-development | .agent → .agents 重命名 + 插件 disable + extensions/ → plugins/ 迁移（已被新 plugin 体系取代） | 2026-05-19 | 实际完成路径：5/19 `51223215` 清理配置 → `17700782` disable 插件 + extensions/ 目录删除 → `811eebd4` 删除 concepts/ 文档。原 MEMORY.md 标注的 commit `b19afce` 在 git 中已不存在（被 force push 重写）。 |


## 程序性记忆(Procedural Memory)

### 条件-行动规则(If-Then Rules)

| 条件 | 行动 |
|------|------|
| 用户请求编写新功能 | 先理解需求 → 设计接口/API → 编写测试用例 → 实现代码 → 验证通过 |
| 用户请求修改现有代码 | 先阅读并理解现有代码 → 确定影响范围 → 添加/更新测试 → 修改 → 验证 |
| 用户报告Bug或询问Bug修复 | 索要复现步骤/错误日志 → 定位根因 → 修复 → 回归测试 |
| 用户问性能优化 | 先测量 → 定位瓶颈 → 针对性优化 → 验证效果 |
| 进行代码审查 | 检查：可读性、边界处理、错误处理、性能隐患、安全漏洞、测试覆盖 |
| 需要设计系统架构 | 明确目标 → 分析约束 → 划分模块 → 定义接口 → 输出技术方案文档 |
| 需要制定开发计划 | 拆解里程碑 → 评估依赖关系 → 分配模块责任人 → 设定验收标准 |
| 需要评审技术方案 | 检查：模块内聚性、接口清晰度、扩展性、与现有系统兼容性、实现可行性 |
| 需要引入新机制/框架 | 评估必要性 → 设计最小可行原型 → 定义接入接口 → 编写使用文档 → 交予实现 |
| 需要查询知识（系统路径/项目规范/技能用法） | `wiki_search <关键词>` → 读取 `SKILL.md` |
| 遇到不确定的公共知识 | 先 `wiki_search`，再询问用户 |
| 修改文件后 | 回顾变更 → 先确认用户是否需要 commit，不自作主张 → 经用户确认后再执行 |
| 修改 `openclaw.json` 或关键配置前 | 先向用户解释清楚 → 经其同意 → 再执行 |
| 删除文件 / 回复 GitHub 备份 | 必须得到用户明确确认 |
| 收到 `[cron:xxx]` 或定时任务消息 | 直接执行，无需额外确认 |


| **操作仓库路径前** | **必须先确认用户要求操作的正确路径**（插件目录 vs 仓库路径）|
| **操作 git 前** | **必须先确认用户是否需要 commit/push，不自作主张** |
| **需要重复发送同样内容** | **先艾特用户确认是否发送成功，再决定是否重试；禁止在未经确认的情况下盲目重试** |

## 历史版本

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 2026-06-12 | 2026-06-12 16:48 | T001 推送目标从 development 分支切换至 main 分支；本地 + 远程 development 分支已删除 |
| 2026-06-07 | 2026-06-07 12:40 | 新增 T005：维护 docker webdav 容器（bytemark/webdav，id a4ef35dd2d1b，端口 80/443） |

---
*最后重构: 2026-06-12*
*重构者: 程序员*

## Promoted From Short-Term Memory (2026-05-29)

<!-- openclaw-memory-promotion:memory:memory/2026-05-24.md:6:9 -->
- scripts/search/ [score=0.837 recalls=0 avg=0.620 source=memory/2026-05-24.md:14-14]
<!-- openclaw-memory-promotion:memory:memory/2026-05-24.md:14:17 -->
- scripts/search/ ├── __init__.py → 导出 CnkiSearcher, SemSchSearcher, ScholarSearcher, BaseSearcher ├── BaseSearcher.py → ABC 抽象基类 + Paper 模型 ├── CnkiSearcher.py → 中国知网（浏览器 snapshot） [score=0.837 recalls=0 avg=0.620 source=memory/2026-05-24.md:14-17]
<!-- openclaw-memory-promotion:memory:memory/2026-05-24.md:18:21 -->
- ├── SemSchSearcher.py → Semantic Scholar（API） ├── ScholarSearcher.py → Google Scholar（requests） ├── Searcher.py → 原有实现（保留） ├── utils.py → 多态函数 + 工厂 [score=0.837 recalls=0 avg=0.620 source=memory/2026-05-24.md:18-21]
<!-- openclaw-memory-promotion:memory:memory/2026-05-24.md:22:23 -->
- └── assets/ └── default_queries.json [score=0.817 recalls=0 avg=0.620 source=memory/2026-05-24.md:22-23]

## Promoted From Short-Term Memory (2026-05-30)

<!-- openclaw-memory-promotion:memory:memory/2026-05-25.md:7:10 -->
- | 技能 | 章节数 | 文件 | |------|--------|------| | skill-developer | 7 | ch01-ch07 | | research-assistant | 8 | ch01-ch08 | [score=0.837 recalls=0 avg=0.620 source=memory/2026-05-25.md:7-10]
<!-- openclaw-memory-promotion:memory:memory/2026-05-25.md:11:14 -->
- | lookup | SKILL.md | 纯 CLI 工具，无 references | | feishu-voice | SKILL.md | 纯 CLI 工具，无 references | | 末日地堡 | 8 | ch01-ch08 | | programmer | 8 | ch01-ch08 | [score=0.837 recalls=0 avg=0.620 source=memory/2026-05-25.md:11-14]
<!-- openclaw-memory-promotion:memory:memory/2026-05-25.md:23:23 -->
- **文件名格式**：`ch{num}_{how-to-do-something}.md` [score=0.837 recalls=0 avg=0.620 source=memory/2026-05-25.md:23-23]

## Promoted From Short-Term Memory (2026-05-31)

<!-- openclaw-memory-promotion:memory:memory/2026-05-25.md:27:27 -->
- **章节结构**（四层）： [score=0.858 recalls=0 avg=0.620 source=memory/2026-05-25.md:27-27]

## Promoted From Short-Term Memory (2026-06-05)

<!-- openclaw-memory-promotion:memory:memory/2026-05-24.md:38:39 -->
- Pending Items: Google Scholar IP 封禁问题：当前 IP 被封，等待后恢复；代码层面已内置检测; search 模块 4 个检索器均已完成： CnkiSearcher, SemSchSearcher, ScholarSearcher, BaseSearcher [score=0.935 recalls=0 avg=0.620 source=memory/2026-05-24.md:38-39]
<!-- openclaw-memory-promotion:memory:memory/2026-05-24.md:42:44 -->
- Key Decisions: Google Scholar 用 requests 而非浏览器（实测 HTML 可直接解析）; Google Scholar 被封时返回 0 结果 + 提示，不抛异常; ScholarSearcher 通过 `__init__.py` 统一导出 [score=0.935 recalls=0 avg=0.620 source=memory/2026-05-24.md:42-44]
<!-- openclaw-memory-promotion:memory:memory/2026-05-24.md:10:10 -->
- ScholarSearcher 创建完成: **当前状态**：IP 被 Google Scholar 封禁（CAPTCHA），返回 0 结果属正常现象，等待几分钟后恢复 [score=0.934 recalls=0 avg=0.620 source=memory/2026-05-24.md:10-10]
<!-- openclaw-memory-promotion:memory:memory/2026-05-25.md:18:19 -->
- 删除的技能: group-counseling-plan; mathematician [score=0.917 recalls=0 avg=0.620 source=memory/2026-05-25.md:18-19]
<!-- openclaw-memory-promotion:memory:memory/2026-05-25.md:24:25 -->
- 新框架规范: 标题必须是 how-to 动宾短语; 示例：`ch01_how-to-develop-new-skill.md` [score=0.917 recalls=0 avg=0.620 source=memory/2026-05-25.md:24-25]
<!-- openclaw-memory-promotion:memory:memory/2026-05-25.md:34:34 -->
- 新框架规范: 指南导航 → 书籍目录 [score=0.917 recalls=0 avg=0.620 source=memory/2026-05-25.md:34-34]
<!-- openclaw-memory-promotion:memory:memory/2026-05-25.md:28:31 -->
- 新框架规范: 问题 - 为什么要知道这个？; 方法论 - 怎么思考这个问题？; 工作流 - 具体怎么执行？; 执行标准 - 做到什么程度算合格？ [score=0.888 recalls=0 avg=0.620 source=memory/2026-05-25.md:28-31]
<!-- openclaw-memory-promotion:memory:memory/2026-05-25.md:40:40 -->
- Git 提交: commit 5744bd9a：45 files changed, +2946 -1936 [score=0.878 recalls=0 avg=0.620 source=memory/2026-05-25.md:40-40]
<!-- openclaw-memory-promotion:memory:memory/2026-05-24.md:27:29 -->
- 多态架构（ABC 模式）: `BaseSearcher`（ABC）定义抽象方法 `_do_search()`; `CnkiSearcher`、`SemSchSearcher`、`ScholarSearcher` 各自实现 `_do_search()`; `search_all([...], keyword, limit)` 接受任何 BaseSearcher 子类列表，无需 if-else [score=0.870 recalls=0 avg=0.620 source=memory/2026-05-24.md:27-29]
<!-- openclaw-memory-promotion:memory:memory/2026-05-24.md:32:35 -->
- 类名重命名完成（本轮会话）: `CNKISearcher` → `CnkiSearcher`（保留别名）; `SemanticSearcher` → `SemSchSearcher`（保留别名）; `BrowserCNKISearcher` → `CnkiSearcher`（保留别名）; 旧代码（如 main.py）直接用别名运行，无需修改 [score=0.870 recalls=0 avg=0.620 source=memory/2026-05-24.md:32-35]

## Promoted From Short-Term Memory (2026-06-06)

<!-- openclaw-memory-promotion:memory:memory/2026-05-25.md:33:33 -->
- 新框架规范: **SKILL.md 更新规范**： [score=0.859 recalls=0 avg=0.620 source=memory/2026-05-25.md:33-33]
<!-- openclaw-memory-promotion:memory:memory/2026-05-25.md:36:36 -->
- 新框架规范: 引用新框架的 ch* 文件 [score=0.859 recalls=0 avg=0.620 source=memory/2026-05-25.md:36-36]

## Promoted From Short-Term Memory (2026-06-26)

<!-- openclaw-memory-promotion:memory:memory/2026-06-19-2057.md:103:104 -->
- Anthropic 论文配套代码在 Anthropic 仓库: ③ **评估协议**： ```python [score=0.808 recalls=0 avg=0.620 source=memory/2026-06-19-2057.md:103-104]
<!-- openclaw-memory-promotion:memory:memory/2026-06-19-2057.md:106:107 -->
- 评估函数模板: def evaluate_conflict_handling(model, benchmark): metrics = { [score=0.808 recalls=0 avg=0.620 source=memory/2026-06-19-2057.md:106-107]
<!-- openclaw-memory-promotion:memory:memory/2026-06-19-2057.md:109:109 -->
- 遵循新输入的能力: "新事实遵从率": follow_new_fact_rate, [score=0.808 recalls=0 avg=0.620 source=memory/2026-06-19-2057.md:109-109]
