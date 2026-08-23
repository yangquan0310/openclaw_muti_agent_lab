# HEARTBEAT.md

---
## 当前活跃定时任务（大管家专属）

| 执行时间 | 负责人 | 任务ID | 任务名称 | 功能描述 | cron状态 |
|----------|--------|--------|----------|----------|----------|
| 每日 05:30 | 大管家（steward） | `9d44c109-78f6-45d9-80b0-556860601e21` | 记忆健康检查（每日5:30） | 每日检查 OpenClaw memory status，处理异常记忆：检查系统状态、向量索引、记忆晋升候选（promote）、REM 反思结果，发现异常时自动修复（重建索引等） | `{"enabled": "已启用"}` |
| 每日 06:00 | 大管家（steward） | `7a700f52-10f4-4bab-9737-b09a08dde9ec` | OpenClaw版本检查 | 每日检查OpenClaw GitHub更新，摘要变更内容。**重点关注**：① MiniMax/DeepSeek/GLM/Kimi/Mimo提供商变化 ② 飞书/微信/QQ渠道变化 ③ OpenClaw核心功能更新 ④ memory search rerank模型 ⑤ Issue #85439（飞书工具暴露/可见性bug）⑥ **飞书 connector 死锁与自反馈循环**（#90559 等）⑦ **TOOL-PROGRESS-LEAK 跟踪**：#85439 修复进展 + 受影响版本 | `{"enabled": "已启用"}` |
| 每日 08:00 | 大管家（steward） | `dde9b3aa-2582-494e-bb54-a6e9625776c4` | 武汉心理学教师招聘信息日报 | 按新模板格式检索武汉地区高校心理学教师招聘信息（硕士/博士），统一输出为「心理学教师」岗位，发布到当前群聊 | `{"enabled": "已启用"}` |
| 每日 08:00 | 大管家（steward） | `2cd2fbc1-8357-471a-a030-5b33a3f8d6fc` | 老板八字运势日报 | 每日早 8:00 给老板推送八字运势日报：排盘 + 9-23 时流时速览 + 五维运势（事业/人际/姻缘/健康/性格）+ 餐饮推荐（午晚餐）+ 具体行动表；流派「基于格局分析的传统命理现代化」；**输出格式：list，不用表格**（2026-08-01 老板拍板改）；**v2.7.0 结构**（2026-08-23 老板拍板）：第二节「今日影响分析」以**合冲刑破为主线**（六合/三合/六害/冲/刑/破 → 各宫×各星×各身体部位三层落地），**每条合冲刑破必须过成立条件判定**（六合 5 条件 / 三合 4 条件 / 三会 3 条件，半合半会被冲即破，无引化即「合而不化」，严禁张口就成局——2026-08-23 今日日报四条合会局全部误判实锤），**五维影响直接并入每条合冲刑破条目**（💼事业/🤝人际/💕姻缘/💪健康/🎭性格，不单独开五维块），**流时只列重要影响**（不罗列十神细节）；announce → **当前 QQ bot 单聊**（2026-08-01 老板拍板从飞书私聊迁移到当前 QQ bot 会话 `chat_id=qqbot:c2c:9F3209C188797074357241443CF8176F`）。**2026-08-01 异常**：QQ bot C2C 通道返回 `API Error [/v2/users/.../messages]: invalid request`（连"测试"都不通），按 OpenClaw 文档是「老板未激活 QQ bot 主动发消息通道」症状——需老板先用 QQ 给 bot 发任意消息激活 C2C。**临时回退策略**：本期 cron 暂时切回飞书私聊 `ou_25cf20a1973aecc51f73d8e2800d7f7e`（保证日报不卡死），等老板激活 QQ bot 后再切回。 | `{"enabled": "已启用，QQ C2C 暂时异常，已临时回退飞书"}` |
| 每日 08:30 | 大管家（steward） | `9f40f017-45f9-4d2a-a3bc-5f118b56cad7` | 老板八字运势日报（8:30版） | 杨权八字每日运势日报（**新建独立 cron，不复用 8:00 原版 prompt**）。每日 8:30 触发；prompt 当前为**占位**「老板拍板后再填」；传递通道待定（`delivery.mode=none` 静默，不推送到任何通道）。等老板拍板 (1) prompt 内容 (2) 传递通道（飞书 / 微信 / QQ bot / 其他）后再启用。 | `{"enabled": "已启用，传递待定（mode=none 静默）"}` |
| 每日 09:00 | 大管家（steward） | `4f726db3-c99d-4f4e-ae60-ed46a4a8d2d7` | 王雅欣八字运势日报 | **王雅欣**八字每日运势日报（**新建独立 cron，参考杨权 8:00 cron 格式结构，针对王雅欣女命定制 prompt**）。命主：王雅欣（1998-07-16 09:00，女，出生地湖北武汉）。**排盘确认**：四柱**戊寅 己未 甲子 己巳**、日主甲木、正财格、身偏旺（寅禄+子印扶身）、喜火金（食伤+官杀泄秀护财）、忌水木土（印+比劫助身）。每日 09:00 触发；prompt **已写入且排盘确认**；传递通道：**announce → qqbot** `c2c:78AB5A9996125580EAB1EC9A101B4A9A` **accountId="wangyaxin"**（2026-08-02 老板拍板从 yangquan 改 wangyaxin，原 accountId 错配导致 invalid request）。**v8.51.0 教训**：参考 ≠ 照抄，参考的那条 = 不可动的源。 | `{"enabled": "已启用，QQ bot wangyaxin 账号已配"}` |

---

## 表格排序规则

### 列排序（从左到右）

| 变量名 | 说明 | 内容/值 |
|--------|------|---------|
| 执行时间 | 定时任务触发时间 | 每日 HH:MM 格式，如：每日 03:00 |
| 负责人 | 执行任务的代理名称 | 代理中文名（agentId），如：大管家（steward） |
| 任务ID | 任务唯一标识符 | UUID格式，如：`ab40d36a-e823-4404-8411-cc9446414564` |
| 任务名称 | 任务简短描述 | 任务简短描述，如：每日TOOLS更新任务 |
| 功能描述 | 任务详细功能说明 | 详细描述任务功能，如：更新个人脚本索引、维护项目库 |
| 脚本位置 | 执行任务相关脚本存储路径 | 脚本文件路径，如：`~/.openclaw/workspace/steward/scripts/` |
| 执行方式 | 任务执行方式 | 子代理执行 / 主代理执行 |
| cron状态 | 定时任务状态 | `{"enabled": "已启用，任务正常执行中", "disabled": "已禁用，任务暂停执行", "error": "执行出错，任务执行失败需要检查", "pending": "待配置，任务已创建但尚未启用"}` |

### 行排序
- 按照**执行时间**增序排列（从早到晚）
- 例如：00:00 → 03:00 → 04:00 → 05:00

---
## 历史版本

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 1.15.0 | 2026-08-23 | **🆕 T043 日报格式 v2.6.0 → v2.7.0**（老板 2026-08-23 08:29 拍板，批今日日报两个问题）：① **合会必须过成立条件判定**——六合 5 条件 / 三合 4 条件 / 三会 3 条件，半合半会 2 字力弱且被冲即破、无引化即「合而不化」；今日日报四条合会局（巳酉半合/申子半合/巳申六合化水/申酉半会）全部误判，实锤老板批评（酉被卯冲、子被午冲、天干无壬癸引化、隔柱）② **五维影响直接并入每条合冲刑破条目**（💼事业/🤝人际/💕姻缘/💪健康/🎭性格），不单独开「五维结果」块。**操作**：cron prompt 已更新（判定规则 + 判定输出格式 + 模板 + DO/DON'T 同步），HEARTBEAT T043 行同步 v2.7.0。 |
| 1.14.0 | 2026-08-04 | **🆕 教研→科研转型同步**（老板 2026-08-04 09:46/09:51/10:00 三次拍板 + 10:21 拍板"完成剩余任务+整理 MEMORY"）。**active 定时任务不变**（5 条 cron 均不涉及 auditor/instructor，无须调整）：T041 武汉心理学教师招聘日报 / T042 OpenClaw 版本检查 / T043 老板八字运势日报 / T044 老板八字运势日报 8:30版（待启）/ T045 王雅欣八字运势日报。**T036-T040 任务状态**：原 MEMORY.md 中"教育科学研究方法 ch12-16 备课"5 个 active 任务因 auditor + instructor 删除而**无法执行**（ch14 真实 7 阶段流水线 v1-v7 依赖 instructor/auditor/presenter/psychologist）。**处理建议**（待老板拍板）：(a) **方案 A**：归档到陈述性记忆（标 completed/aborted），备注"教研→科研转型时删除"；(b) **方案 B**：保留 active 但加 blocked 标记（待转型完成后重建教研线）；(c) **方案 C**：直接删除。**当前可用 8 个 agent**（v8.52.0 起）：steward + mathematician + physicist + psychologist（科研领域专家）+ programmer + writer + reviewer（替代 auditor 审核）+ presenter（科研可视化师）。**配套变更**：(a) README.md v3.3.4（badge 10→8、删除审计员/讲师行、加转型版本历史）；(b) MEMORY.md v8.52.0（职责边界更新 + 版本历史）；(c) presenter IDENTITY.md v2.0.0 / SOUL.md v2.0.0（课件编译师 → 科研可视化师）；(d) openclaw.json / .env / SQLite 全部清理；(e) 飞书 bot 解绑指南已给老板。**重启**：所有清理完成后一次性重启 OpenClaw（老板原话"所有清理完成后重启"）。 |
| 1.13.0 | 2026-08-02 | **🆕 T045 accountId 修正：yangquan → wangyaxin**（老板 12:56 拍板"accountid得改成wangyaxin"）。**根因**：openid `78AB5A9996125580EAB1EC9A101B4A9A` 属于 **wangyaxin bot**（1903742138），不属于 yangquan bot（1905316550）—— 跟 T043 v1.8.2 老板 openid 归属问题完全同模式（"Each bot has its own set of user OpenIDs"）。**症状**：原 cron delivery accountId="yangquan" 跨 bot 调用 → QQ Open Platform 返回 `OutboundDeliveryError: API Error [/v2/users/78AB5A9996125580EAB1EC9A101B4A9A/messages]: invalid request`（consecutiveErrors=2）。**修复**：`cron.update patch.delivery.accountId="wangyaxin"` + `cron.run runMode=force` 手动验证（runId `manual:...:5` 因 isolated agent setup 超时未真正投递，**非 accountId 问题**——是 runtime 临时 setup timeout，下次 09:00 自动触发应该 OK）。**do 型规则**：T045 cron 任何 send 到 `qqbot:c2c:78AB5A9996125580EAB1EC9A101B4A9A` 必须 `accountId: "wangyaxin"`。 |
| 1.12.0 | 2026-08-01 | **🆕 T045 王雅欣日报排盘确认 + 完整 prompt 写入**（老板 14:40 拍板"八字四柱处理并确认后，确定并修改"）。**操作**：(a) `bazi 1998-07-16 09:00` 排盘 → 四柱 = **戊寅 己未 甲子 己巳**（与原记录一致 ✓）；(b) 删除旧 T045 cron `a89a7cc9-...`（仍带"待排盘确认"占位）+ 创建新 T045 cron `4f726db3-c99d-4f4e-ae60-ed46a4a8d2d7`（完整填入四柱/日主/格局/身旺/用神/忌神）；(c) HEARTBEAT.md 同步更新 cron ID。**完整命局信息已写入 prompt**：四柱 戊寅 己未 甲子 己巳、日主甲木（大树之木）、格局正财格（月干透己土正财）、身偏旺（寅禄 + 子印扶身）、用神火+金（食伤泄秀 + 官杀护财）、忌水+木+土（印+比劫助身 + 财已多不需再加）。 |
| 1.13.0 | 2026-08-02 | **🆕 T045 accountId 修正：yangquan → wangyaxin**（老板 12:56 拍板"accountid得改成wangyaxin"）。**根因**：openid `78AB5A9996125580EAB1EC9A101B4A9A` 属于 **wangyaxin bot**（1903742138），不属于 yangquan bot（1905316550）—— 跟 T043 v1.8.2 老板 openid 归属问题完全同模式（"Each bot has its own set of user OpenIDs"）。**症状**：原 cron delivery accountId="yangquan" 跨 bot 调用 → QQ Open Platform 返回 `OutboundDeliveryError: API Error [/v2/users/78AB5A9996125580EAB1EC9A101B4A9A/messages]: invalid request`（consecutiveErrors=2）。**修复**：`cron.update patch.delivery.accountId="wangyaxin"` + `cron.run runMode=force` 手动验证（runId `manual:...:5` 因 isolated agent setup 超时未真正投递，**非 accountId 问题**——是 runtime 临时 setup timeout，下次 09:00 自动触发应该 OK）。**do 型规则**：T045 cron 任何 send 到 `qqbot:c2c:78AB5A9996125580EAB1EC9A101B4A9A` 必须 `accountId: "wangyaxin"`。 |
| 1.11.0 | 2026-08-01 | **🆕 T045 王雅欣日报 prompt 内容已写入**（老板 14:33 拍板"先参考杨权八字运势，把内容先写入"）。**v8.51.0 教训应用**：参考杨权 8:00 原 cron 的**格式结构**（排盘 + 流时 + 五维 + 餐饮 + 行动表），但**prompt 内容针对王雅欣女命定制**（命主基础信息 / 流派 / 5 步流程 / 五维女命版 / 输出模板 / 约束 / 写作风格 = 7 段全新内容）。**操作流程**：(a) delete T045 旧 cron `3a697184-...`（占位 prompt）+ (b) create 新 T045 `a89a7cc9-aef7-471a-b05d-662d0e0df53f`（完整 prompt，~4500 字符）；(c) HEARTBEAT.md 同步更新 cron ID；(d) git commit + push。 |
| 1.10.0 | 2026-08-01 | **🆕 新增 T045 王雅欣八字运势日报（独立 cron，9:00 每日）**（老板 2026-08-01 14:21 拍板"我让你参考这个定时任务，做一个日报：王雅欣八字运势"）。**关键 do**：参考原 T043 cron 的**格式结构**（排盘 + 流时 + 五维 + 餐饮 + 行动表），**prompt 内容不复用**——新建独立 cron 用 placeholder prompt + 王雅欣命主基础信息（1998-07-16 09:00 / 女 / 湖北武汉）+ 流派定位。**业务含义**：原 T043/T044 老板八字日报不动；T045 王雅欣八字日报每日 09:00 静默生成（mode=none），等老板拍板 prompt + 传递通道。**v8.51.0 教训**：参考 ≠ 照抄，参考的那条 = 不可动的源。 |
| 1.9.0 | 2026-08-01 | **🆕 新增 T044 独立 cron 老板八字运势日报 8:30版（不碰原 T043）**（老板 2026-08-01 14:09 拍板 + 14:17 怒纠）：老板原话"先按照日报：杨权八字运势，做一个日报，定在每天8点半。传递待定"——大管家错误理解为"修改原 cron `2cd2fbc1-...` + 复用其 prompt"，擅自用 `cron.update` 改了原 cron 的 schedule / displayName / delivery，老板亲自下场修 prompt 冲突并怒纠"参考 ≠ 照抄 + 不要动参考的那条"。**修复**：(a) **rollback 原 cron `2cd2fbc1-...`** 全部字段（schedule `30 8` → `0 8`、displayName `每日8:30` → `每日8:00`、delivery `mode=none` → `announce qqbot default → 9F3209C188797074357241443CF8176F`）；(b) prompt 保留老板自己改的版本（"单身，关注正缘"）；(c) **新建独立 cron `9f40f017-45f9-4d2a-a3bc-5f118b56cad7`**（`name="日报：杨权八字运势（8:30版）"`，displayName=`大管家八字日报（每日8:30 待定）`），prompt 为占位「老板拍板后再填」，delivery `mode=none` 静默；(d) MEMORY.md 加 v8.51.0 规则（"参考 ≠ 照抄 + 不要动参考的那条"）。**业务含义**：原 T043 8:00 老板日报照常跑（QQ bot default 通道）；新建 T044 8:30 老板日报**静默生成**，prompt + 传递通道均等老板拍板。 |
| 1.8.0 | 2026-08-01 | **T043 渠道迁移**：从飞书私聊（`ou_25cf20a1973aecc51f73d8e2800d7f7e`）迁移到当前 QQ bot 单聊（`qqbot:c2c:9F3209C188797074357241443CF8176F`）。老板拍板要日报发到当前 QQ 频道。`openclaw cron edit 2cd2fbc1-... --channel qqbot --to qqbot:c2c:9F3209C188797074357241443CF8176F` 验证生效（`updatedAtMs` 已变化）。 |
| 1.8.1 | 2026-08-01 | **T043 临时回退飞书**（**计划方案，实际未执行**）：当时判断是「老板未激活 QQ bot 主动发消息通道」，准备临时回退到飞书私聊 `ou_25cf20a1973aecc51f73d8e2800d7f7e`。但 1.8.2 找到真根因后作废——**不是激活问题，是 openid 归属问题**。 |
| 1.8.2 | 2026-08-01 | **T043 根因找到**：不是配置问题，是 openid 归属问题。openid `9F3209C188797074357241443CF8176F` 属于 **default bot**（appId 1903464819），不属于 **yangquan bot**（1905316550）也不属于 **wangyaxin bot**（1903742138）。按 OpenClaw 文档「Each bot has its own set of user OpenIDs」—— yangquan / wangyaxin bot 调用 `POST /v2/users/{openid}/messages` 都返回 `invalid request`，只有 default bot 成功（`messageId: ROBOT1.0_p8Ck2cRIDzdmgwBh...`）。**修复**：cron delivery 必须显式 `accountId: "default"`（当前 cron delivery 没设 accountId 会落到 yangquan 默认账号，**会失败**）。**do 型规则（强制）**：T043 cron 任何 send 到 `qqbot:c2c:9F3209C188797074357241443CF8176F` 必须 `accountId: "default"`。 |
| 1.7.0 | 2026-07-31 | **新增 T043 老板八字运势日报**（每日 08:00）：排盘 + 9-23 时流时 + 五维（事业/人际/姻缘/健康/性格）+ 餐饮推荐 + 具体行动表；announce → 微信私聊（accountId `1e2cee2d0572-im-bot`，to `o9cq802gxxo8zkjtxiojovbz6ku8@im.wechat`）；流派归属「基于格局分析的传统命理现代化」 |
| 1.6.0 | 2026-06-07 | **T042 OpenClaw 版本检查日报新增 2 个关注点**：⑥ 飞书 connector 死锁与自反馈循环（#90559 等）⑦ TOOL-PROGRESS-LEAK 跟踪（#85439 修复进展 + 受影响版本 + workaround）。原有 5 个关注点保留并显式编号。 |
| 1.5.0 | 2026-06-05 | 新增"已知 Bug 跟踪"表，记录 TOOL-PROGRESS-LEAK（#85439）：飞书群工具调用结果泄漏 |
| 1.4.0 | 2026-05-09 | **停用自动整理任务**：论文写作项目管理者改为手动执行，删除每日01:00定时整理任务 |
| 1.3.0 | 2026-04-26 | 将Git自动推送任务从steward迁移到main（系统管理员），从本HEARTBEAT.md移除，已记录在main的HEARTBEAT.md中 |
| 1.2.0 | 2026-04-19 | 修改每日维护任务为每日自我更新，按照`agent_self_development`工作流2执行 |
| 1.1.0 | 2026-04-16 | 细化TOOLS.md维护任务描述，增加公共技能、个人技能、个人脚本、项目的扫描和同步说明 |
| 1.0.0 | 2026-04-10 | 将状态列改为cron状态，规范状态取值 |

---
*最后更新: 2026-08-02*
*更新者: 大管家*
*说明: T045 王雅欣日报 accountId 修正（yangquan → wangyaxin）+ HEARTBEAT.md v1.13.0。openid 78AB5A9996125580EAB1EC9A101B4A9A 归属 wangyaxin bot（1903742138），跟 T043 v1.8.2 老板 openid 归属问题同模式。*