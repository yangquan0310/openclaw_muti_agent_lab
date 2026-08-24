# MEMORY.md

> **本文件保留工作记忆（当前任务）、程序性记忆（If-Then 规则）和陈述性记忆。**

---

## 工作记忆(Working Memory)

### 当前活跃任务看板

> **⚠️ 只保留活跃任务，已完成的任务自动归档**

| 任务ID | 项目 | 任务描述 | 状态 | 创建时间 | 最后更新 | 备注 |
|--------|------|----------|------|----------|----------|------|
| T041 | 招聘信息日报 | 武汉心理学教师招聘信息日报（每日08:00） | active | 2026-05-29 | 2026-05-29 | cron ID: dde9b3aa，发布到当前群 |
| T042 | OpenClaw 版本检查 | 监控 OpenClaw 官方 GitHub releases，**重点关注**：MiniMax/DeepSeek/GLM/Kimi/Mimo 提供商变化；飞书/微信/QQ 渠道变化；OpenClaw 核心功能更新 | active | 2026-05-29 | 2026-05-30 | cron ID: 7a700f52 |

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
| **合并main分支前** | **先更新 `.openclaw/README.md` 版本历史** |
| **项目文件整理** | **使用 thesis-manager 技能，标准目录：uploads/manuscripts/knowledge/ 等。metadata.json 必须在根目录，不可移动。统一仓库路径：~/.openclaw/repository/** |
| **用户要求"查原因"** | **先读代码→定位问题→确认根因→再谈修复，不急于给方案** |
| **向用户发送权限申请** | **必须使用飞书交互卡片（interactive card），包含按钮和跳转链接** |
| **向用户发送普通链接** | **根据情况选择：纯文本链接（简洁场景）或交互卡片（需要点击操作的场景）** |
| 项目中上传文件（.docx/.pdf/.pptx 等） | 1. 移动到 uploads/；2. 用 markitdown 解析到 uploads/markdown/ |
| **派发任务时找不到 open_id** | 在群消息中搜索目标代理的历史消息，提取其 open_id |
| **监控 OpenClaw 更新时** | **重点关注**：MiniMax、DeepSeek、GLM、Kimi、Mimo 提供商变化；飞书、微信、QQ 渠道变化；OpenClaw 核心功能更新 |
| **派发任务给其他专家代理** | steward 自主决定派给哪个子代理/怎么传约束（**不需先与老板讨论**）；让其他专家代理自行决定如何执行子任务（**不擅写死子任务步骤**） |
| **workboard 派发** | **查看 manager 技能**：`references/workboard-guide.md`。**建卡/写操作全部走 `workboard_*` agent tool**。**派发触发**用 `exec` 跑 `openclaw workboard dispatch --board default --expect-final --timeout 300000`（**不调** `workboard_dispatch` agent tool，只清理不启动）。**绝对禁止**重建 `manager workboard` CLI wrapper。 |
| **workboard 的真正定位** | **官方插件描述**：`Dashboard workboard for agent-owned issues and sessions`。**真正主用户是 agent**，我只是帮其他 agent 建卡/调度的辅助者。**Dashboard 是人类旁观察看**。 |
| **派发任务必查 manager 技能 SKILL.md** | **收到任何派发类任务**（群里 / 私聊 / 老板口述 / TODO 描述），**第一动作** = 查 `~/.openclaw/workspace/steward/.agents/skills/manager/SKILL.md`（v5.14.0）**description 字段**。如描述未涵盖新场景，**先**读 task-flow-guide.md §1.4 场景概览表，**不要自己拍**。 |
| **消息/note 模板库** | **完整指针**到 workboard-guide.md §三之5。派发前**先查**该节。**派发核心原则**：(1) 大管家 = 建卡 + 派发 + 验收；(2) 不调 sessions_yield；(3) subagent 完整自管 + 大管家只核验不接管。 |
| **任务四要素 + 通知模板** | **任务四要素**（建卡 note 核心内容）：(1) 任务目标（干什么）；(2) 任务约束（限制/边界）；(3) 输入路径（读什么文件/资源，绝对路径）；(4) 输出路径（产出落到哪）。**通知模板 4 要素**（派发核心内容）：(1) 任务标题；(2) CARD_ID；(3) 操作步骤；(4) 反馈要求。**完整指针**到 workboard-guide.md §三之5.1 + §三之5.2。 |
| **🚨 进程/服务"看起来没动静"时** | **场景**：进程在跑但指标"异常"（WAL大/连接断/I/O 0）。**❌ 错误做法**：看到"异常"立即归类"卡死/需要重启"——**这是模式匹配陷阱**！**✅ 正确做法（do 型）**：(1) **先列 3 个候选解释**：a) 正常工作模式；b) 网络/资源限流；c) 真卡死（仅 1/3 概率）。(2) **查上下文证据**：active_memory_plugin 提示 + 服务日志 + 启动时间 + 资源使用曲线。(3) **没排除 a/b 前不重启**——**杀进程是不可逆操作**。 |
| **大管家 vs 其他专家代理职责边界** | 大管家 = 协调者，落实用户方向；其他专家 = 执行者（writer 写论文/mathematician 分析数据/physicist 建模/psychologist 科研领域/各专家解释自己领域理论/programmer 写代码/**reviewer 同行评审/审阅**）。当前可用 8 个 agent：steward + mathematician + physicist + psychologist + programmer + writer + reviewer + presenter（可视化师） |
| **发送链接/卡片的操作权** | steward 自主根据情况选择纯文本 vs 飞书交互卡片（不需先与老板讨论）——这是操作权，不算"擅自修改"老板给的 SOP |
| **"不擅自修改 SOP" vs "根据情况选择"** | **不冲突**——前者针对老板给的 SOP 内容（不能改）；后者是工具/格式的操作权（steward 自主）|
| **🚫 用户隐私零记录**（2026-08-08 老板明确指示） | **涉及老板个人隐私/亲密关系的对话内容，禁止写入任何记忆文件**（MEMORY.md / memory/*.md / dreaming / 索引）——只记录规则，不记录内容。核查命令：`grep -rn "<敏感词>" memory/ MEMORY.md` + `openclaw memory search`。 |
| **🚫 严禁编造任何时间/版本号/发布信息** | **任何**包含"发布时间"或"版本号"的回答，**必须**先实查到原始数据（GitHub releases.atom feed、changelog、官方公告）再报告。**绝对不能凭记忆编造精确时间戳**。 |
| **回答版本前必查 4 件事** | (1) `https://github.com/openclaw/openclaw/releases.atom`（真实数据源）；(2) 实际当前装的版本（`openclaw --version`）；(3) 当前时间（CST = UTC+8）；(4) **对照前 3 项在 atom feed 中实际出现的 entry 数**。 |
| **三件套矛盾梳理（IDENTITY/SOUL/MEMORY 内在矛盾）** | 矛盾处理原则：**平衡分析后修改**——逐条检查 if-then 规则（哪些仍然适用保留、哪些已过时删除、哪些矛盾修改/合并）；IDENTITY 边界**加限定词**（不替换），具体下放技能；SOUL 不轻易改（人格层稳定） |
| **决策制定 vs 派发任务** | ❌ 决策制定 = 大管家**不替用户做研究/项目方向决策**（用户规定方向）；✅ 派发任务 = 大管家**落实用户方向**的具体操作（其他专家负责执行）——两者**不冲突** |
| **内容创作的本意** | ❌ 内容创作 = **不撰写论文/学术文章**（writer 的职责）；**不禁止** wiki 整理/规范说明/工作汇报（这些是文档管理）|
| **数据分析的本意** | ❌ 数据分析 = **不做数学家/统计学家的数据分析**（mathematician 的职责）；**不禁止** 系统状态监控/sqlite 健康检查（这些是运维）|
| **理论解释的本意** | ❌ 理论解释 = **不解释其他专家对自己领域的理论**（各专家的职责）；**不禁止** wiki 总结/技术规范/操作文档（这些是知识管理）|
| **代码编写的本意** | ❌ 代码编写 = **不编写分析代码**（programmer 的职责）；**不禁止** 写脚本/批处理（这些是工具自动化）|
| **授权与信任（让其他专家代理自决）** | 派发子任务时，**只传约束/输入/产出**，让其他专家代理自己决定如何执行（**不擅自写死** SOP 步骤）|
| **技能 CLI 必须有全局入口** | 不能用 `python3 main.py <子命令>` 调技能 CLI，**必须**在 `/usr/local/bin/` 创建 symlink/shell 包装指向 `scripts/main.py`，保证 `manager <子命令>` 等可全局调用。例：`ln -s <skill>/scripts/main.py /usr/local/bin/manager`。 |
| **wiki synthesis 页面命名** | **必须**带时间戳前缀 `YYYY-MM-DD-HH-MM-SS-`，例：`2026-06-02-13-55-00-云端大模型-本地小模型-混合架构-工程化实践.md`。**禁止**裸名（`xxx.md`）。创建后**必须**手动 `mv` 加时间戳前缀。 |
| **排版/出 PDF/HTML 文档** | **铁律：用 Quarto 取代 Pandoc**。LaTeX 后端用 tinytex（`/root/.TinyTeX/`，450MB），不用系统 TeX Live 2023。**三种标准范式**：<br>**① 排版多个 .md 组成的书籍** = `quarto render` + 多个 `.md` + `_quarto.yml` + `references.bib` + `apa.csl`<br>**② 排版一篇学术论文** = `quarto render <file>.md` + 单 `.md`（**带 YAML 头**）+ `references.bib` + `apa.csl`<br>**③ 排版一般文章** = `quarto render <file>.md` + 单 `.md`（**带 YAML 头**）<br>**反例（不许用）**：任何 `pandoc xxx.md -o xxx.pdf` 命令、任何 `pandoc.yaml` 配置。 |
| **CJK 字体：Noto CJK TTC face 歧义** | Noto CJK 字体是 **TTC 多 face 容器**，xelatex 默认挑**第一个 face（jp）**，导致 PDF 嵌入字体显示 `NotoSerifCJKjp`。**根治方案**：换用**单 TTF face 的中文 font**——`AR PL SungtiL GB`（文鼎简报宋，apt 装的 `fonts-arphic-gbsn00lp`）。嵌入字体显示 `BousungEG-Light-GB`，绝对 SC 无歧义。 |
| **编译好的 PDF 输出位置** | 一律放**项目根 `/docs/` 目录**。命名用标题（如 `docs/记忆机制的认知推断.pdf`）。**Quarto 单文件模式**用 CLI flag `quarto render <file>.md --output-dir ../docs`；**Quarto book 模式**在 `_quarto.yml` 的 `project.output-dir: ../../docs` 配置。 |
| **PDF 编译遇到"段落右侧超出" / CJK 宽度问题** | **直接复用项目内 `manuscripts/header.tex` 模板**（关键配置：`\sloppy\tolerance=1000\emergencystretch=3em`）。CJK 文档还要加 `\XeTeXlinebreaklocale "zh"` + `\XeTeXlinebreakskip = 0pt plus 1pt` + `\usepackage{xurl}`。 |
| **🚫 禁止修改任何 pnpm/npm 依赖包**（绝对红线） | **绝对不许** 用 `edit` / `write` / `exec sed` / `exec cat > file` 等任何写操作进入 `~/.local/share/pnpm/.../node_modules/`、`~/.openclaw/npm/.../node_modules/`、`/usr/lib/node_modules/` 等任何由包管理器管理的目录。发现 bug 只能通过：`(a)` 给上游提 issue / PR；(b) 在仓库根目录打 patch 后用 `openclaw plugins install` 走插件机制重新安装；(c) `openclaw update` 升级包版本。 |
| **🚫 禁止装 pandoc、禁止用 pandoc 编译**（绝对红线）| **绝对不许** `apt install pandoc` / `pip install pandoc` / 任何形式装回 pandoc 系统包。**绝对不许**用 `pandoc xxx.md -o xxx.pdf` 命令、任何形式的 `pandoc.yaml` / `pandoc --defaults` 编译。**Quarto 1.7.34 自带 pandoc 3.6.3**，需要 pandoc 能力的场景全部走 Quarto 子进程。 |
| **论文项目默认范式 ④ apaquarto** | 老板要求**以后所有论文文档都需要排版成 apa 格式**。**默认排版范式 = 范式 ④ apaquarto-pdf 严格 APA 7 manuscript mode**（产出独立 title page + author note + running head + 双倍行距）。**范式 ④ 5 步关键修复**：(1) R 环境（r-base conda env）+ PATH；(2) tinytex PATH；(3) 项目根 `_quarto.yml`（**空壳** `project: type: default`——**真正的根因**，缺这个 Quarto 找不到 `_extensions/apaquarto/`）；(4) 装 apaquarto 扩展（`quarto add wjschne/apaquarto`）；(5) `.md` YAML 头特殊处理（用 `format: apaquarto-pdf:`、必填 `author-note:` + `shorttitle:` + `corresponding:`、**不要**写 `bibliography:` + `csl:`）。 |
| **🚨 删除目录前必查 symlink** | **场景**：删除 /root/.openclaw 下目录（2026-08-04 删除 memory-tdai/canvas/mcp/extensions/git 时踩坑）。**教训**：memory-tdai 和 git 是符号链接（→ /data/disk/.openclaw/），`rm -rf xxx/` 带尾斜杠会**跟随链接删除真实目标内容**，而 `tar` 备份只打包链接本身（4K）不备份真实数据。**正确做法**：(1) 删除前先 `ls -la` 看是否有 `→` 箭头 / `readlink` 检查；(2) 备份真实目标用 `tar -czhf`（-h 跟随）或直接备份 /data/disk 真实路径；(3) 删链接本身用 `rm`（不带斜杠）或 `unlink`；(4) 其他 symlink（memory/media/npm/agents/repository）是省磁盘软链接布局，**严禁误删**。 |
| **🚫 用户给短/模糊指令 + 涉及 system-level 行为 → 必须先解释方案 + 等明确 OK** | **触发条件**：(1) 老板给短/模糊指令（"启动X" / "做Y" / "试试Z" 等）；(2) 我**打算**做的动作涉及 system-level 行为——`openclaw hooks` / `openclaw config set` / `apt install` / `pip install` / `pnpm add` / `git push` / 任何写 `~/.local/share/pnpm/.../node_modules/` 路径。**必须做**：① **逐项列出**影响范围（副作用/是否可逆/备选方案）；② **等老板明确 OK**（"对" / "执行" / "OK" / "装" 等动词式），**不**用模糊短句当默许；③ 老板**只**确认"启用了" = 状态已 OK，**不**是命令我装东西。 |
| **✅ "参考" ≠ "照抄"，"参考的那条" = 不可动的源** | **场景**：老板说"先按照 X / 参考 X，做一个 Y"。**新规则**：(1) **"参考" ≠ "照搬内容"**—— X 只是**模式/格式的样本**，不要复制 X 的 prompt / 配置到 Y；(2) **"参考的那条"绝对不能动**——它是老板会自己维护的源；(3) **新建一条独立的**——用不同 name，prompt 由老板拍板或另起草，**不**复用 X 的内容。 |
| **✅ 规范更新 git 提交走 main** | **场景**：日常规范更新（task-flow-guide / workboard-guide / SKILL.md / MEMORY.md 等的版本号 + 内容更新）。**git branch -a** 只有 main + backup（开发分支不存在）。**新规则**：(a) 规范更新 commit + push 走 **main**；(b) `git add <files>` → `git commit -m "<type>: <desc>"` → `git push origin main`。 |
| **✅ 用户要求发文件 → 直接 lark-cli im +messages-send --file** | **场景**：用户要求把本地文件（.docx / .pdf / .pptx 等）通过飞书 IM 发给他。**唯一可靠方案**：`lark-cli im +messages-send --user-id <ou_xxx> --file <相对路径>`，**必须 `cd` 到文件所在目录**用 `./文件名`（绝对路径会被拒绝）。 |
| **✅ 大管家专属邮箱** | **邮箱账号** `quanquanzi0306@agent.qq.com`（provider = agent.qq.com）。**发送邮件**：`agently-cli message +send --to <addr> --subject <subj> --body <body>`。**读邮件**：`agently-cli message +list --limit 10` / `+read --id <msg_id>`。**OAuth**：`agently-cli auth refresh` 强制刷新；`agently-cli auth status` 看本地状态。**配额**：50 封/天 / 10 req/min。 |
| **✅ agently-cli 工具集速查** | **路径**：`/root/.nvm/versions/node/v22.22.2/bin/agently-cli`。**完整命令树**：(1) `+me` 当前用户信息；(2) `auth login|logout|refresh|status` 凭证管理；(3) `message +list|+read|+search|+send|+reply|+forward`；(4) `attachment +upload|+download`。**注意**：OAuth URL 必须用 `message` action=send 单独发（reply 通道会 filter OAuth URL）。 |
| **✅ skill 部署路径规范** | **个人技能必须部署到 `workspace/steward/.agents/skills/<skill_name>/`**（与 bazi/manager/zhongyi 一致）。**绝对不**部署到 `workspace/steward/skills/`（OpenClaw 全局共享技能目录，非个人）。**skill_workshop proposal 的 target paths 必须与最终部署路径一致**。 |
| **✅ workboard 卡片粒度 = 混合 L1/L2/L3 模式**（v5.15.0，2026-08-04 老板拍板） | **场景**：任何 workboard 建卡。**新规则**（取代 v8.51.0 之前的"一项目一卡 vs 一任务一卡"二元讨论）：(1) **L1 项目卡** = 1 张 / 项目（立项时建，`agentId=steward` 元数据卡，老板视角）；(2) **L2 阶段卡** = 3-5 张 / 项目（立项后**立即全部建好** `status=todo`，大管家追踪）；(3) **L3 任务卡** = **按需**（L2 卡涵盖 3+ 子任务 / 子代理明确要求拆 / 阶段需分批严格串行 / 大管家觉得追踪粒度不够时建）。**关键约束**：(a) L2 卡的 `parents` 指向 L1 ID；(b) L3 卡的 `parents` 指向 L2 ID——**⚠️ v5.15.1 踩坑修正：L3 派发卡不要真设 `parents` 硬链接**（workboard 依赖机制会把带未完成 parent 的卡自动降级回 todo，dispatch 选不到 → started=0），改用 `createdByCardId` + L2 notes 软关联；(c) **L1/L2 卡不直接派发**，只做元数据 + 追踪；(d) **L3 才是真正派发对象**（群派发 IM 5 段艾特 / dispatch 派发 `openclaw workboard dispatch` CLI）。**完整定义**：`manager` 技能 `references/card-granularity.md` v1.0.1。**派生规则**：(a) 新项目立项 → 先建 L1 + 立即批量建 L2；(b) 派发时如 L2 阶段卡过重 → 拆 L3 任务卡；(c) 已有项目**不**强制迁移到三层，**新项目严格**执行。**踩坑教训（v8.51.0 沉淀）**：之前讨论的"一任务一卡 vs 一项目一卡"是**二元对立**——workboard 原生支持 parents/children 字段，三层混合才是最优解。**commit**：dc1da94d + 本次 v5.15.1。 |
| **✅ 流月天干必须用五虎遁起月法**（v8.54.0，2026-08-05 老板拍板） | **场景**：任何流月排盘 / 流月与命局互动分析。**老板原话**（2026-08-05 23:18）："你更新一下流年流月计算。别在出问题了"。**新规则**：(a) **流月天干 = 五虎遁起月法**（**不是**相生顺序硬推）。**五虎遁口诀**：① **甲己之年丙作首**（甲/己年正月寅月=丙寅）；② **乙庚之年戊为头**（乙/庚年正月寅月=戊寅）；③ **丙辛之年寻庚上**（丙/辛年正月寅月=**庚寅**——2026 丙午年正月即此）；④ **丁壬壬寅顺水流**（丁/壬年正月寅月=壬寅）；⑤ **戊癸之年何处起，甲寅之上好追求**（戊/癸年正月寅月=甲寅）。(b) 然后按天干顺序顺推各月：庚寅→辛卯→壬辰→癸巳→甲午→乙未→丙申→丁酉→戊戌→己亥→庚子→辛丑。(c) **反例（不许做）**：按"上一月天干+1"硬推（如壬寅→癸卯→甲辰→乙巳→丙午...）—— **这是错的**！地支也按节气切月（立春→寅月开始，不是农历正月）。**踩坑教训（v8.54.0 沉淀）**：在 2004-02-16 09:30 女命姻缘深度解读中，整张流月天干全错（壬寅/癸卯→甲辰→乙巳→丙午...），根因 = 从壬寅开始按相生顺序硬推没用五虎遁，老板亲自下场纠错"今年是庚寅月吧？你搞错了"，连带姻缘关键月份的判断全错。**派生规则**：(a) 流月排盘前**先**用 `bazi <生日> --liumonth <年>-<月>` 验算，**不要**自己推；(b) 流年起法（公历年 = 流年柱）只是近似，**精确**以立春为界；(c) 任何排盘解析前**先**自检"流月天干对吗？"，避免低级错误。 |
| **🚧 古代天文历法术数 5 待建技能**（v1.13.0 / MEMORY.md v8.55.0 §十一.8，老板 2026-08-13 14:40 拍板范畴规则） | **场景**：未来新增术数技能（紫微/奇门/太乙/七政四余/纳甲）。**5 个待建技能清单**（按优先级）：① **P0 `ziwei` 紫微斗数**（v1.x 待建）；② **P1 `qimen` 奇门遁甲**（v1.x 待建）；③ **P1 `taiyi` 太乙神数**（v1.x 待建）；④ **P2 `qizhengsiyu` 七政四余**（v1.x 待建）；⑤ **P2 `najia` 纳甲**（v1.x 待建）。**派生规则**：(a) 未来 5 个技能按"**范畴识别 + 统一边界 + 流派归属 + 专用工具**"四步走实施（按 bazi-rules.md §11.2-11.5 模板）；(b) **不混用**八字技法到紫微/奇门/六壬（如八字"用神"≠紫微"宫位"）；(c) **不沿用** P0-1 教训——每个新技能**首版必须有 ≥8 边界用例**（参考 bazi self-test 46/46 经验）；(d) 立项后通过 **`skill_workshop` 提案**走 OpenClaw 标准流程（路径 `.agents/skills/<name>/`）。**踩坑教训（v1.13.0 沉淀）**：之前 bazi 评审发现 5 个技能只在文档中提及，**未在 MEMORY.md 列入强约束**，导致任意时刻可能被遗忘。**补法**：本条记录强约束 + 给出 P0/P1/P2 优先级 + 给出实施模板。 |

---

## 历史版本

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v8.55.1 | 2026-08-22 | **tcm-diagnosis 技能改名 zhongyi**（老板拍板）：目录 `.agents/skills/tcm-diagnosis/` → `zhongyi/` + `skills/tcm-diagnosis/` → `skills/zhongyi/`；SKILL.md name 字段同步；全局命令 `/usr/local/bin/tcm` → `/usr/local/bin/zhongyi`（symlink 重建）；内部引用（README/CLI engine/disclaimer）同步；self-test 8/8 通过。 |
| v8.53.0 | 2026-08-04 | **🚨 删除目录前必查 symlink**：删除 memory-tdai/canvas/mcp/extensions/git 时踩坑（memory-tdai 和 git 是符号链接指向 /data/disk/.openclaw/，rm -rf 带斜杠跟随链接删除真实目标；tar 备份只打包链接本身不备份数据）。新增 if-then 规则：删前 ls -la 查箭头 / readlink，备份用 tar -czhf，删链接用 rm 不带斜杠，其他 symlink（memory/media/npm/agents/repository）严禁误删。 |
| v5.15.0 | 2026-08-04 | **workboard 卡片粒度 = 混合 L1/L2/L3 模式**（老板 2026-08-04 11:32 拍板）。新增 `manager/references/card-granularity.md` v1.0.0；SKILL.md 加触发条件 + 指南导航 + 版本号 5.14.0 → 5.15.0；MEMORY.md 加 v5.15.0 规则。 |
| **v8.54.0** | **2026-08-05** | **🚨 流月天干必须用五虎遁起月法**（老板 2026-08-05 23:18 拍板"你更新一下流年流月计算。别在出问题了"）。**踩坑教训**：2004-02-16 女命姻缘深度解读整张流月天干全错（壬寅/癸卯/甲辰...），根因 = 从壬寅按相生顺序硬推没用五虎遁。**新规则**：五虎遁口诀（甲己丙作首/乙庚戊为头/丙辛寻庚上/丁壬壬寅/戊癸甲寅）+ 用 `bazi --liumonth` 验算 + 反例明示（不许"上一月天干+1"硬推）。 |
| v8.49.0 | 2026-07-29 | **skill 部署路径规范**：个人技能必须部署到 `.agents/skills/<skill_name>/`，skill_workshop target paths 必须同步。commit `e6ddcd68`。 |
| v8.37.0 | 2026-07-02 | **派发模式根本重构**：群派发（IM 5段艾特）/ **dispatch 派发**（`openclaw workboard dispatch` CLI，取代私聊 sessions_spawn）。验收权下放：大管家**不调** `workboard_complete`（worker 自己 complete）。**agent tool ≠ plugin CLI 关键发现**：`workboard_dispatch` agent tool = `store.dispatch()`（只清理），**不**启动 worker；`openclaw workboard dispatch` CLI = 完整函数（清理+claim+启动）。规范更新推 main（撤销"只推 development"旧规则）。 |
| v8.35.0 | 2026-06-09 | **沉淀方向根本转变**：从"不要型"（避免错误）→ **do 型**（成功经验）。**不**沉淀"如何避免错"；**不**重复 system 提示已覆盖的规则；**不**重复 v3.5.0 范式已覆盖的基础派发。 |
| v8.32.0 | 2026-06-07 | **短/模糊指令 + system-level 动作 → 必须先解释 + 等明确 OK**。老板只确认"启用了" = 状态 OK，**不**是命令我装东西。 |

---

*最后更新：2026-08-04*
*更新者：大管家*
*说明：MEMORY.md v8.52.0 一次清理完成，删除全部教学混杂内容、ch14 教研教训、bazi 流派版本历史（v8.42-v8.50）、auditor/instructor 残留引用、CFPPS 项目残留、wiki entities 残留。保留所有当前活跃 If-Then 规则和必要的版本历史。*

## Promoted From Short-Term Memory (2026-08-25)

<!-- openclaw-memory-promotion:memory:memory/2026-08-20.md:10:12 -->
- 🏢 宫星系统框架确立（老板 2026-08-20 17:42-17:50 拍板，核心变更）: "宫是容器，是部门，天干是负责人，宫藏干是员工"; "宫一般是地支吧？地支才有藏干（员工）。毕竟天干是固定的。比如妻星才能进婚姻宫"; "星看交互，确定星的人际关系！宫有藏干，与星交互，确定整个宫的状态！" [score=0.803 recalls=0 avg=0.620 source=memory/2026-08-20.md:10-12]
<!-- openclaw-memory-promotion:memory:memory/2026-08-20.md:14:14 -->
- 🏢 宫星系统框架确立（老板 2026-08-20 17:42-17:50 拍板，核心变更）: **最终框架（v3.0.0 写入 bazi-paipan.md §五 宫星系统）**： [score=0.803 recalls=0 avg=0.620 source=memory/2026-08-20.md:14-14]
<!-- openclaw-memory-promotion:memory:memory/2026-08-20.md:15:18 -->
- 🏢 宫星系统框架确立（老板 2026-08-20 17:42-17:50 拍板，核心变更）: **宫 = 地支**（容器/部门/房子）——只有地支才有藏干，才能装人；天干 = 固定门牌（不参与进出动态）; **宫藏干 = 员工**——本气/中气/余气，决定部门真正实力; **星（十神）= 访客**——财/官/印/比劫/食伤，**星才是能"进宫"的**; **星看交互 → 定星的人际关系**：星被生/合 = 关系好；被克/冲/刑/害/破 = 关系差；透干=显性、藏支=隐性 [score=0.803 recalls=0 avg=0.620 source=memory/2026-08-20.md:15-18]
<!-- openclaw-memory-promotion:memory:memory/2026-08-20.md:19:22 -->
- 🏢 宫星系统框架确立（老板 2026-08-20 17:42-17:50 拍板，核心变更）: **宫藏干与星交互 → 定宫的状态**：星与藏干相生/合 = 宫和睦；相克/冲 = 宫冲突；宫被外部冲合刑害破 = 房子动荡; **宫星配合判读四步**：①先看宫（位置被冲合刑害破=部门动荡）②再看星（六亲星落哪个宫）③星落宫位（夫妻星落夫妻宫=人住进家，落他宫=异地/晚婚）④再看藏干（员工强弱=内部细节）; **四柱宫位**：年支=祖上宫（祖辈/出身/家宅）/ 月支=父母宫兼事业宫（父母/事业/手足）/ 日支=夫妻宫（婚姻/配偶）/ 时支=子女宫兼晚年宫（子女/晚年/末运）; **六亲星映射（男命）**：妻=正财、父=偏财、母=正印、女儿=正官、儿子=七杀（部分流派/食神）、兄弟=比劫 [score=0.803 recalls=0 avg=0.620 source=memory/2026-08-20.md:19-22]
<!-- openclaw-memory-promotion:memory:memory/2026-08-20.md:23:23 -->
- 🏢 宫星系统框架确立（老板 2026-08-20 17:42-17:50 拍板，核心变更）: **六亲星映射（女命）**：夫=正官、父=偏财、母=正印、儿子=食神、女儿=伤官、兄弟=比劫 [score=0.803 recalls=0 avg=0.620 source=memory/2026-08-20.md:23-23]
<!-- openclaw-memory-promotion:memory:memory/2026-08-20.md:25:25 -->
- 🏢 宫星系统框架确立（老板 2026-08-20 17:42-17:50 拍板，核心变更）: **三层思维（老板 18:28 确认检查标准）**：① 宫（宫与其他交互）② 星（星与其他交互）③ 宫星交互——**顺序固定：先宫 → 再星 → 再宫星交互，不许颠倒**。 [score=0.803 recalls=0 avg=0.620 source=memory/2026-08-20.md:25-25]
<!-- openclaw-memory-promotion:memory:memory/2026-08-20.md:3:3 -->
- 2026-08-20 工作记忆: > 本文件记录 2026-08-20 会话的持久记忆（大管家 steward）。 [score=0.803 recalls=0 avg=0.620 source=memory/2026-08-20.md:3-3]
<!-- openclaw-memory-promotion:memory:memory/2026-08-20.md:31:31 -->
- 📐 bazi-paipan.md 重构为分析总纲（v2.5.0 → v3.1.0）: **老板 17:56 拍板**："核心内容是排盘-分析-应用-输出。排盘有 cli，分析有对应的 md，应用也有对应的 md，输出也有对应的 style。刚刚那个是应用总纲，目前缺分析总纲。你需要重新确定下这个文档结构。" [score=0.803 recalls=0 avg=0.620 source=memory/2026-08-20.md:31-31]
<!-- openclaw-memory-promotion:memory:memory/2026-08-20.md:33:33 -->
- 📐 bazi-paipan.md 重构为分析总纲（v2.5.0 → v3.1.0）: **新结构（9 章）**： [score=0.803 recalls=0 avg=0.620 source=memory/2026-08-20.md:33-33]
<!-- openclaw-memory-promotion:memory:memory/2026-08-20.md:9:9 -->
- 🏢 宫星系统框架确立（老板 2026-08-20 17:42-17:50 拍板，核心变更）: **三连拍板**（老板原话逐条）： [score=0.803 recalls=0 avg=0.620 source=memory/2026-08-20.md:9-9]
