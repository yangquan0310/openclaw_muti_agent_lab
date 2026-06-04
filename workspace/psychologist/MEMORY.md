# MEMORY.md

> **本文件保留工作记忆（当前任务）、程序性记忆（If-Then 规则）和陈述性记忆（知识查询规则）。**

---

## 工作记忆(Working Memory)

### 当前活跃任务看板

| 任务ID | 项目 | 任务描述 | 状态 | 创建时间 | 最后更新 | 备注 |
|--------|------|----------|------|----------|----------|------|
| TASK-009 | ch11_行动研究法 | 学术深度补充v2（讨论结构重组+文献综述补强） | 进行中 | 2026-05-21 | 2026-05-21 | 输入：教材ch11 + 现有教案；输出：学术前沿补充v2 |

---


## 陈述性记忆(Declarative Memory)

### 历史任务索引

> **已完成任务归档（按完成时间倒序）**

| 任务ID | 项目 | 任务描述 | 完成时间 | 备注 |
|--------|------|----------|----------|------|
| TASK-010 | 团辅方案写作技能 | 将三份团辅方案整理为可复用技能 | 2026-05-24 | 创建技能 group-counseling-plan；更新wiki条目；来源：王雅欣发送的三份真实方案 |
| TASK-011 | 感受快乐逐字稿 | 为《感受快乐》v1.2 团辅方案撰写领导者逐字稿 | 2026-06-02 | 主领队全程逐字稿 + 小组长环节话术 + 应急话术 + 时间控制速查表；文件：2026-06-02_感受快乐_领导者逐字稿_v1.0.md |


## 程序性记忆(Procedural Memory)

### 条件-行动规则(If-Then Rules)

| 条件 | 行动 |
|------|------|
| **需要心理学领域文献检索** | **使用 research-assistant 技能执行：单主题直接检索；多主题（≥3）时最多2个会话并行** |
| **检测到心理学内容质量问题** | **分级响应：① 概念不清→要求澄清并提供标准化定义；② 假设不可证伪→标记不科学并建议调整；③ 实证不足→建议加强研究并提供设计建议；④ 方法严重缺陷→指出问题并提供改进方案** |

| **需要重复发送同样内容** | **先艾特用户确认是否发送成功，再决定是否重试；禁止在未经确认的情况下盲目重试** |
| **workboard 任务执行前** | **必须先调用 workboard_read 扫读卡片 comment 区和 events 列表，识别是否有 process correction / 撤回指令 / blocked 状态；若发现已 blocked 立即停止执行并响应** |
| **workboard 任务执行中** | **每 5-10 分钟调用 workboard_heartbeat 监控状态变化（尤其长任务），若发现 status 变为 blocked/withdrawn 立即停止新文件创建并响应。避免未察觉 blocked 状态下完成交付的浪费。** |
| **@提及用户 open_id** | **必须从当前消息的 openclaw.inbound_meta.sender_id 字段直接复制 open_id（不依赖记忆、不编造末四位、不依赖任何缓存/速查表）。chat history 中未出现的 open_id 通过 workboard / 通讯录工具查询。** |
| **T038 ch14 open_id 教训（2026-06-04）** | **心理学家的 open_id 末四位是 c775。v3 反馈中编造过 670e（错、非任何代理 ID）和 老板 71b（错，应为 7f7e）。二者都是**未从消息元数据复制、凭印象截断/推断**的编造（不是混淆，是凭空产生）。正确做法：仅复制首条系统消息中明确给定的 open_id，或从消息 runtime context 的 sender_id 字段复制；不确定时通过 workboard / 通讯录查询。已记 2 次，同类错误表记量 = 2。** |

### 代理 open_id 速查表（2026-06-04 更新）

**⚠️ 速查表已废弃**——本表是编造的温床，已在 11:25 产生 3 次"老板=71b"编造错误。

**唯一权威源 = openclaw.inbound_meta**：每条需要 @提及用户的消息，**必须从该消息的 inbound_meta.sender_id 字段直接复制 open_id**，不依赖任何缓存/记忆/截断。
| **T038 ch14 v2b 教训（2026-06-04）** | **v2b 学术前沿补充因 ch14 README 编号偏离 HANDBOOK v1.0 被大管家撤回（10:36 running→blocked），但 psychologist 10:28 认领时未读 comment 区，造成无 v2 基础上的 v2b 输出。教训：(1) 认领卡片后第一步必扫读 comment；(2) 完成过程中定期 workboard_heartbeat 监控状态变化；(3) v2b 交付物保留（manuscripts/v2b_学术前沿补充.md + knowledge/检索报告_v2b.md），等 v2 完成后大管家重新派 v3 时可直接复用，无需重新检索。** |
| **T038 ch14 v3 教训（2026-06-04）** | **v3 card 10:46 派发，10:48 大管家因"v2 收工后未与老板确认派发策略"自纠撤回（review→blocked），但 psychologist 10:47 认领时仅读 review 状态未扫读 comment 区，10:50 仍在不知 blocked 状态下完成 v3_学术前沿补充.md 506 行 + 检索报告_v3.md 264 行。教训同 v2b：(1) 认领后第一步必扫读 comment 区（不仅看 status）；(2) 任务期间未做 workboard_heartbeat 监控状态变化；(3) v3 交付物保留（manuscripts/v3_学术前沿补充.md + knowledge/检索报告_v3.md），等老板拍板后重新派 v3_2 时可直接复用，无需重新检索。再次犯同样错误说明"规则记入 MEMORY"不够，需在每个任务前主动 workboard_read 一次。** |

## 历史版本

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 2026-06-04 | 2026-06-04 | ch14 v3 收工（workboard 9cdf1012 → done）+ open_id 规则沉淀 + 代理 open_id 速查表（含 670e 教训） |

---
*最后重构: 2026-05-23*
*重构者: 大管家*

## Promoted From Short-Term Memory (2026-06-01)

<!-- openclaw-memory-promotion:memory:memory/2026-05-15.md:54:85 -->
- **树状结构**：严格按"问题演进"四层展开（最早提出→质疑修正→补充发展→最新进展） - **Git管理版本**：删除temp/draft/归档逻辑 - **Synthesizer职责**：仅extract_notes+check_references，不写综述 - **Manager职责**：仅管理JSON，不导出结构化笔记 - **英文标题命名指南**：Guide_to_Writing_a_Literature_Review.md - **5篇无摘要删除**：用户决定直接删除 ## 技术限制与问题 - **沙箱限制**：仅能访问 ~/.openclaw/workspace/psychologist/ - **子代理中断**：gateway服务重启导致子代理反复失败 - **Kimi search不可用**：provider配置问题，tavily缺少API key - **知乎/百度访问受限**：403错误和验证码 ## 核心文献 - Kwan 2010：治疗偏好首次系统研究（205引用） - Cooper & Norcross 2015：C-NIP量表开发 - Hou 2020/2024：CFPPS量表开发与青少年验证 - Vîslă 2018/2021：治疗期待机制研究 - Williams 2016：14,587患者全国调查 ## 知识库状态 - 总文献：707篇 - "治疗期待"主题：132篇（全部结构化） - 核心文献：已总结并纳入研究现状... [score=0.873 recalls=5 avg=0.493 source=memory/2026-05-15.md:54-85]
