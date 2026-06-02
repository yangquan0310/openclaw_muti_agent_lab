# MEMORY.md

> **本文件保留工作记忆（当前任务）、程序性记忆（If-Then 规则）和陈述性记忆。**

---

## 工作记忆(Working Memory)

### 当前活跃任务看板

> **⚠️ 只保留活跃任务，已完成的任务自动归档**

| 任务ID | 项目 | 任务描述 | 状态 | 创建时间 | 最后更新 | 备注 |
|--------|------|----------|------|----------|----------|------|
| T036 | 教育科学研究方法 | ch12 个案研究法（2学时，v1-v7） | active | 2026-05-21 | 2026-05-21 | 待启动 |
| T037 | 教育科学研究方法 | ch13 教育叙事研究（2学时，v1-v7） | active | 2026-05-21 | 2026-05-21 | 待启动 |
| T038 | 教育科学研究方法 | ch14 量的研究与质的研究的整合（2学时，v1-v7） | active | 2026-05-21 | 2026-05-21 | 待启动 |
| T039 | 教育科学研究方法 | ch15 研究设计（2学时，v1-v7） | active | 2026-05-21 | 2026-05-21 | 待启动 |
| T040 | 教育科学研究方法 | ch16 教育科学研究论文的撰写（2学时，v1-v7） | active | 2026-05-21 | 2026-05-21 | 待启动 |
| T041 | 招聘信息日报 | 武汉心理学教师招聘信息日报（每日08:00） | active | 2026-05-29 | 2026-05-29 | cron ID: dde9b3aa，发布到当前群 |
| T042 | OpenClaw 版本检查 | 监控 OpenClaw 官方 GitHub releases，**重点关注**：MiniMax/DeepSeek/GLM/Kimi/Mimo 提供商变化；飞书/微信/QQ 渠道变化；OpenClaw 核心功能更新 | active | 2026-05-29 | 2026-05-30 | cron ID: 7a700f52（2026-05-30重新创建，原ID 07bad57e 丢失） |


---

## 程序性记忆(Procedural Memory)

### 条件-行动规则(If-Then Rules)

| 条件 | 行动 |
|------|------|
| 使用 `feishu_create_doc` 创建云文档 | **工具底层为应用身份**，文档所有者显示为"大管家"；创建后**必须提醒用户手动转移所有权** |
| 用户要求以用户身份创建文档 | 说明限制：当前工具无法实现；建议用户先在飞书界面创建空白文档，再使用 `feishu_update_doc` 写入内容 |
| 已创建文档需要转移所有权 | 提供文档链接和操作步骤：打开文档 → 分享 → 添加自己 → 权限选"可管理" → 再转移所有权 |
| **需要修改被 gateway tool 拦截的配置项** | **优先用 CLI**：`openclaw config set <path> <value>`，不受 protected 路径限制；`gateway config.patch` 只适合未受保护的字段 |
| API Key 存储位置检测 | 检查 ~/.openclaw/.env 文件权限和格式 |
| 检测到同项目活跃会话 | 复用该会话,禁止创建新代理 |
| MEMORY.md 与 metadata.json 状态不一致 | 以 metadata.json 为准同步更新 |
| 用户明确提出"结束"或"完成" | 更新状态为completed,执行归档 |
| 章节备课完成(v6收工) | 同时推送到main和development |
| 日常备课(v1-v5)/规范更新 | 只推送到development分支 |
| 上传/同步操作 | 默认推送到development分支 |
| 每日维护任务推送 | 推送到development分支 |
| 文档太大（超过5000字） | 使用腾讯云文档分段上传 |
| **合并main分支前** | **先更新 `.openclaw/README.md` 版本历史** |
| **项目文件整理** | **使用 thesis-manager/course-manager 技能，标准目录：uploads/manuscripts/knowledge/ 等。metadata.json 必须在根目录，不可移动。统一仓库路径：/data/disk/仓库/** |
| **用户要求"查原因"** | **先读代码→定位问题→确认根因→再谈修复，不急于给方案** |
| **终稿/草稿目录存在** | **使用 thesis-manager/course-manager 技能手动整理，迁移到标准目录** |
| **向用户发送权限申请** | **必须使用飞书交互卡片（interactive card），包含按钮和跳转链接** |
| **向用户发送普通链接** | **根据情况选择：纯文本链接（简洁场景）或交互卡片（需要点击操作的场景）** |
| "数字化存储与自传体记忆"项目任务完成 | 执行本地 git 提交 |
| 项目中上传文件（.docx/.pdf/.pptx 等） | 1. 移动到 uploads/；2. 用 markitdown 解析到 uploads/markdown/ |
| **派发任务时找不到 open_id** | 在群消息中搜索目标代理的历史消息，提取其 open_id |
| **用户报告飞书/微信/QQ 工具结果泄漏** | **不要花时间调 streaming/blockStreaming 参数**——已验证完全非流式（streaming=false + blockStreaming=false）仍泄漏；这是 OpenClaw 上游 bug（#85439），等官方修复。在 HEARTBEAT.md `TOOL-PROGRESS-LEAK` 行跟踪 |
| **更新 TODO.md 后** | **先与老板讨论修改策略与内容，确认后再通知子代理执行。禁止在未经讨论的情况下直接派发任务。** |
| **分配子任务给子代理** | **只传递约束目标/输入/产出，让子代理自己决定如何执行** |
| **需要重复发送同样内容** | **先艾特用户确认是否发送成功，再决定是否重试；禁止在未经确认的情况下盲目重试** |
| **发送飞书原生语音消息** | ~~使用 feishu-voice 技能~~（已迁移至 wiki：syntheses/如何用语音回复用户.md） |
| **监控 OpenClaw 更新时** | **重点关注**：MiniMax、DeepSeek、GLM、Kimi、Mimo 提供商变化；飞书、微信、QQ 渠道变化；OpenClaw 核心功能更新 |
| **派发任务给其他专家代理** | steward 自主决定派给哪个子代理/怎么传约束（**不需先与老板讨论**）；让其他专家代理自行决定如何执行子任务（**不擅写死子任务步骤**） |
| **修改 TODO.md 任务描述** | 必须先与老板讨论修改策略与内容（**这是任务本身调整，不是派发**） |
| **大管家 vs 其他专家代理职责边界** | 大管家 = 协调者，落实用户方向；其他专家 = 执行者（writer 写论文/数学家分析数据/各专家解释自己领域理论/programmer 写代码/auditor 审核等）|
| **发送链接/卡片的操作权** | steward 自主根据情况选择纯文本 vs 飞书交互卡片（不需先与老板讨论）——这是操作权，不算"擅自修改"老板给的 SOP |
| **"不擅自修改 SOP" vs "根据情况选择"** | **不冲突**——前者针对老板给的 SOP 内容（不能改）；后者是工具/格式的操作权（steward 自主）|
| **三件套矛盾梳理（IDENTITY/SOUL/MEMORY 内在矛盾）** | 矛盾处理原则：**平衡分析后修改**——逐条检查 if-then 规则（哪些仍然适用保留、哪些已过时删除、哪些矛盾修改/合并）；IDENTITY 边界**加限定词**（不替换），具体下放技能；SOUL 不轻易改（人格层稳定） |
| **决策制定 vs 派发任务** | ❌ 决策制定 = 大管家**不替用户做研究/项目方向决策**（用户规定方向）；✅ 派发任务 = 大管家**落实用户方向**的具体操作（其他专家负责执行）——两者**不冲突** |
| **内容创作的本意** | ❌ 内容创作 = **不撰写论文/学术文章**（writer 的职责）；**不禁止** wiki 整理/规范说明/工作汇报（这些是文档管理）|
| **数据分析的本意** | ❌ 数据分析 = **不做数学家/统计学家的数据分析**（数学家的职责）；**不禁止** 系统状态监控/sqlite 健康检查（这些是运维）|
| **理论解释的本意** | ❌ 理论解释 = **不解释其他专家对自己领域的理论**（各专家的职责）；**不禁止** wiki 总结/技术规范/操作文档（这些是知识管理）|
| **代码编写的本意** | ❌ 代码编写 = **不编写分析代码**（programmer 的职责）；**不禁止** 写脚本/批处理（这些是工具自动化）|
| **授权与信任（让其他专家代理自决）** | 派发子任务时，**只传约束/输入/产出**，让其他专家代理自己决定如何执行（**不擅自写死** SOP 步骤）|
| **需要发布 workboard 任务卡**（建/改/移/删/批量/归档）| **查看 manager 技能**：`references/workboard-guide.md`（v5.4.0 新增）。agent 工具集只覆盖读/认领/评论/续约/释放/证明/解锁；写操作走 gateway WebSocket RPC + 设备身份认证，脚本：`scripts/workboard/`（Python 包，`manager workboard <子命令>` 调用）|
| **技能 CLI 必须有全局入口**（skill-developer 规范）| 不能用 `python3 main.py <子命令>` 调技能 CLI，**必须**在 `/usr/local/bin/` 创建 symlink/shell 包装指向 `scripts/main.py`，保证 `manager <子命令>` / `rps <子命令>` 等可全局调用。例：`ln -s <skill>/scripts/main.py /usr/local/bin/manager`。已验证：`manager` symlink 路径错误会导致调用失败，需用绝对路径。 |



### 待跟进事项(Suspended)

| 项目 | 说明 | 状态 | 挂起时间 |
|------|------|------|----------|
| rock-paper-scissors-tournament | **老板未授权，自作主张启动的项目**。已建成（31测试+CLI+git），但**不再继续推进**。位于 `/root/.openclaw/workspace/rock-paper-scissors-tournament/`，独立 git repo。未经老板明确指令前不许碰。 | 挂起 | 2026-06-02 |

## 陈述性记忆(Declarative Memory)

### 历史任务索引

> **已完成任务归档（按完成时间倒序），共34项**

| 任务ID | 项目 | 任务描述 | 完成时间 | 备注 |
|--------|------|----------|----------|------|
| T034 | 数字化存储与自传体记忆 | 第十二轮：Minor问题修复 | 2026-05-20 23:51 | 10.5.1节重复修复，commit ba2b8f0 |
| T033 | 数字化存储与自传体记忆 | 第十二轮：审稿助手全文审核 | 2026-05-20 23:38 | 评级🟢优秀 |
| T032 | 数字化存储与自传体记忆 | 第十二轮：全文写作质量修复 | 2026-05-20 19:21 | commit 20e1cec，ch10 v3 |
| T031 | 数字化存储与自传体记忆 | 第十一轮：讨论结构重组（6节） | 2026-05-20 16:22 | 讨论6节重组，PDF 3.4MB |
| T030 | 数字化存储与自传体记忆 | 第十轮：语言润色 | 2026-05-20 09:30 | PDF v3.0.0（3.0MB） |
| T029 | 数字化存储与自传体记忆 | 第九轮：10.5节AI记忆工程 | 2026-05-14 20:17 | v2.5.0已编译，Git f1ba600 |
| T028 | 创业指导 | 终稿最终修正 | 2026-05-13 12:43 | PDF编译0警告 |
| T027 | 创业指导 | 终稿+修改说明核查 | 2026-05-13 12:12 | 评级🟢基本可提交 |
| T026 | 创业指导 | 修改说明更新 | 2026-05-13 11:49 | — |
| T025 | 创业指导 | 终稿最终修正 | 2026-05-13 11:48 | 3项必改+5项建议完成 |
| T024 | 创业指导 | 第三轮审核 | 2026-05-13 10:50 | 评级🟢修改到位 |
| T023 | 创业指导 | 内容改写与润色 | 2026-05-13 10:37 | v6，Git d401e9f |
| T022 | 创业指导 | 学术内容深化 | 2026-05-13 10:27 | P0 2项+P1 3项+P2 3项 |
| T021 | 创业指导 | 内容质量深度审核 | 2026-05-13 10:27 | 评级🟡需重大修改 |
| T020 | 创业指导 | 引用格式全面修正 | 2026-05-13 10:00 | v5 |
| T019 | 创业指导 | 终稿归档 | 2026-05-13 08:37 | v4.2_final，Git 5ffeb6c |
| T018 | 创业指导 | 第二轮审核 | 2026-05-13 00:12 | 评分🟢良 |
| T017 | 创业指导 | 理论审核 | 2026-05-12 23:40 | 5项🔴问题已反馈 |
| T016 | 创业指导 | 终稿整合 | 2026-05-12 23:33 | v4终稿 |
| T015 | 教育科学研究方法 | ch10 质的研究法 v7 收工 | 2026-05-14 02:42 | Git 9ffd114，23页PPT |
| T014 | 优秀论文匿名评审 | 6篇论文评审 | 2026-05-12 12:32 | ✅ 已完成 |
| T015b | 教育科学研究方法 | ch10 重新走流程v1-v7 | 2026-05-14 21:37 | ✅ 已完成 |
| T013 | wiki维护 | wiki瘦身：内容精简与结构优化 | 2026-05-12 10:07 | — |
| T011 | 数字化存储与自传体记忆 | 归档与版本管理 | 2026-05-12 17:49 | 终稿归档、Pandoc编译 |
| T010 | 数字化存储与自传体记忆 | 第五轮：规范核查 | 2026-05-12 17:37 | 术语/结构/论证/引用/格式 |
| T009 | 数字化存储与自传体记忆 | 第四轮：审阅 | 2026-05-12 17:14 | 理论贡献增量、跨章一致性 |
| T008 | 数字化存储与自传体记忆 | 第四轮：总论与收尾 | 2026-05-12 17:14 | 总讨论理论整合+结论扩充 |
| T007 | 数字化存储与自传体记忆 | 第三轮：审阅 | 2026-05-12 16:48 | 实验讨论质量、DDM/RSA讨论 |
| T006 | 数字化存储与自传体记忆 | 第六轮：终极核查+编译归档 | 2026-05-12 17:49 | 终稿归档、PDF编译 |
| T005 | 数字化存储与自传体记忆 | 第五轮：规范核查 | 2026-05-12 17:37 | 术语/结构/论证/引用/格式 |
| T004 | 数字化存储与自传体记忆 | 第四轮：总论与收尾 | 2026-05-12 17:14 | 总讨论理论整合+结论扩充 |
| T003 | 数字化存储与自传体记忆 | 第三轮：实验讨论深化 | 2026-05-12 16:48 | 实验讨论理论深化+文字优化 |
| T002 | 数字化存储与自传体记忆 | 第二轮：前导章节深化 | 2026-05-12 13:50 | 理论补充、文字优化、审阅意见 |

## 历史版本

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v8.14.0 | 2026-05-28 | 新增 If-Then 规则：`config set` CLI 可绕过 protected 限制，优于 `gateway config.patch` |
| v8.15.0 | 2026-06-02 | 新增 If-Then 规则：workboard 写操作（建/改/移/删/批量/归档）需走 gateway WebSocket RPC + 设备身份认证（脚本：`scripts/wb-rpc.mjs`）。**v8.15.1**：精简规则为指针，详情下沉到 manager 技能 `references/workboard-guide.md`（v5.4.0）。**v8.15.2**：脚本从 Node.js 迁移至 Python 包 `scripts/workboard/`（`manager workboard <子命令>`）。**v8.15.3**：修正全局入口 symlink（`/usr/local/bin/manager` 路径错误），所有技能 CLI 文档同步为裸命令格式 |
| v8.16.0 | 2026-06-02 | 新增 If-Then 规则：技能 CLI 必须有全局入口（skill-developer 规范），禁止 `python3 main.py` 调用 |
| v8.13.0 | 2026-05-28 | 新增协调者身份边界If-Then规则：读技能/用模板/不分身/只协调 |
| v8.12.1 | 2026-05-21 | T014/T015b确认完成，状态标记移除 |


| v8.10.0 | 2026-05-06 | 精简：删除陈述性记忆、工作记忆使用规则、会话清单，只保留 If-Then 规则 |
| v8.9.0 | 2026-05-01 | 每日自我更新：无个人更新触发，纯维护日 |
| v8.0.0 | 2026-04-19 | 初始版本，作为大管家创建 |

<!-- openclaw-memory-promotion:memory:memory/2026-05-23.md:98:116 -->
- | 数学家 | mathematician | 数学建模、统计分析 | | 物理学家 | physicist | 物理建模、公式推导 | ### 技能结构 ``` {agent}/skills/{agent}/ ├── SKILL.md # 入口文件 ├── references/ # 指南目录 ├── scripts/ # 脚本工具 └── assets/ # 模板资源 ``` ### 设计意图 - 实践命名 - 指南下沉 - 边界明确 - 快速检索 - 版本追踪 [score=0.812 recalls=30 avg=0.502 source=memory/2026-05-23.md:98-116]

## Promoted From Short-Term Memory (2026-05-30)

<!-- openclaw-memory-promotion:memory:memory/2026-05-12.md:55:69 -->
- **source 定义**: 指向外部真实文件系统的来源页面，有具体文件路径，被 concept/entity 引用作为溯源依据 - **核心目的**: 让代理快速定位外部文件、为声明提供溯源依据 - **五种 pageType 分工**: concept（这是什么）、entity（这是谁）、source（这在哪里）、synthesis（这怎么用）、report（状态如何） - **.env 来源处理**: 创建 sources/openclaw-env.md，只记录路径+配置类型+访问权限，具体值脱敏为 `***`，绝不暴露密钥 - **sources/ 现状**: 19 个页面 = 系统来源 5 个（openclaw-system、openclaw-workspace、openclaw-env、repository、agent-self-development）+ 项目来源 15 个 ### 3. Miniconda 安装与环境管理 - **安装路径**: `~/miniconda3/` - **配置**: `~/.condarc` 指定 envs_dirs 和 pkgs_dirs 为 `~/.conda/envs` 和 `~/.conda/pkgs` - **创建环境**: - `py311`: Python 3.11.15，注册 Jupyter 内核 - `r-base`: R 4.3.1，安装 irkernel 注册 Jupyter 内核 - **Jupyter 内核**: python3 (base)、py311、r-base 三个可用 - **磁盘占用**: `~/.conda` 3.3G + `~/miniconda3` 867M [score=0.863 recalls=5 avg=0.524 source=memory/2026-05-12.md:55-69]

## Promoted From Short-Term Memory (2026-05-31)

<!-- openclaw-memory-promotion:memory:memory/2026-05-28.md:118:121 -->
- variables: [score=0.815 recalls=0 avg=0.620 source=memory/2026-05-28.md:40-40]

## Promoted From Short-Term Memory (2026-06-01)

<!-- openclaw-memory-promotion:memory:memory/2026-05-28.md:13:16 -->
- | 章节 | 问题 | |------|------| | §3.5 | 放置位置存疑 | | §4.4 | 需补充经典认知范式（工作记忆N-back、联想记忆配对联想学习、错误记忆与幻觉评估） | [score=0.828 recalls=0 avg=0.620 source=memory/2026-05-28.md:13-16]
<!-- openclaw-memory-promotion:memory:memory/2026-05-28.md:17:18 -->
- | §4.5 | 在理论框架中间讲意义，逻辑不通 | | §6.1 | 内容堆砌，与§6.2完全脱节 | [score=0.828 recalls=0 avg=0.620 source=memory/2026-05-28.md:17-18]

## Promoted From Short-Term Memory (2026-06-02)

<!-- openclaw-memory-promotion:memory:memory/2026-05-28.md:34:34 -->
- **pandoc.yaml**：仅含配置变量 [score=0.851 recalls=0 avg=0.620 source=memory/2026-05-28.md:34-34]
<!-- openclaw-memory-promotion:memory:memory/2026-05-28.md:36:38 -->
- standalone: true pdf-engine: xelatex input-files: [score=0.851 recalls=0 avg=0.620 source=memory/2026-05-28.md:36-38]
<!-- openclaw-memory-promotion:memory:memory/2026-05-28.md:40:42 -->
- variables: mainfont: "Noto Serif CJK SC" geometry: [score=0.851 recalls=0 avg=0.620 source=memory/2026-05-28.md:40-42]
<!-- openclaw-memory-promotion:memory:memory/2026-05-28.md:49:49 -->
- **全文整合稿.md开头YAML块**： [score=0.851 recalls=0 avg=0.620 source=memory/2026-05-28.md:49-49]
<!-- openclaw-memory-promotion:memory:memory/2026-05-28.md:52:53 -->
- title: AI Agent 的技术原理与心理学应用 subtitle: 面向管理心理学背景读者的科普文章 [score=0.851 recalls=0 avg=0.620 source=memory/2026-05-28.md:52-53]
