# Synthesize Peer Review SOP（v5.21.0 新增）

> 来源：吸收 Academic Research Skills（ARS）Paper Reviewer 的 **7-agent 多视角同行评议**思路  
> 用途：**synthesize 输出综述后**自动跑这套评审 SOP，给出 0-100 分 + 强项/弱项/问题清单  
> 核心思想：**模拟 EIC + 3 动态审稿人 + Devil's Advocate**，避免单一视角偏差

---

## 🎯 为什么需要这个？

研究助手 v5.20.0 的 `synthesize extract` 直接出 markdown，**没有任何评审环节**——质量完全靠用户自己看。

**本 SOP 给 synthesize 加 7 个评审视角**，每视角独立打分，最后汇总。

---

## 📋 7 个评审 Agent

| # | Agent | 角色 | 评估重点 | 评分维度 |
|---|-------|------|---------|---------|
| 1 | **EIC**（Editor-in-Chief）| 总编辑 | 整体投稿价值、研究意义、是否符合综述标准 | 5 维度（0-100）|
| 2 | **Methodologist** | 方法学审稿人 | PICO、PRISMA、检索完整性、偏倚评估 | 4 维度 |
| 3 | **Domain Expert** | 领域专家 | 论点准确性、与既有理论对话、关键文献覆盖 | 4 维度 |
| 4 | **Statistician** | 统计审稿人 | 效应量、置信区间、异质性、PRISMA 数字 | 3 维度 |
| 5 | **Writer / Reviewer 1** | 写作审稿人 | 章节逻辑、文字流畅、APA 规范 | 3 维度 |
| 6 | **Reviewer 2** | 第二视角审稿人 | 论证链完整性、边界条件、future direction | 4 维度 |
| 7 | **Devil's Advocate** | 唱反调审稿人 | 找漏洞、质疑 overclaim、找反例 | 5 维度 |

---

## 🔧 7-Agent 评审工作流

### Stage 1：prepare review dossier

```bash
# 输入
synth_doc=wiki/syntheses/<date>-systematic-review-<topic>.md
# 准备 dossier：
# - synthesize 文档全文
# - 引用的 wiki sources 列表（zotero_item_key）
# - 关联的 Zotero 条目 metadata
# - 数据抽取表（如有）
```

### Stage 2：并行跑 7-agent 评审

每个 agent 独立输出 `{agent}-review.md`：

```
reviews/
├── 01-eic-review.md         # 总评 + 接收/修改/拒绝
├── 02-methodologist-review.md
├── 03-domain-expert-review.md
├── 04-statistician-review.md
├── 05-writer-review.md
├── 06-reviewer2-review.md
└── 07-devils-advocate-review.md
```

### Stage 3：汇总评分（concession threshold protocol）

**Concession Threshold Protocol**（ARS 借鉴）：
- 如果 4/7 agent 给 < 60 分 → **大改**
- 如果 2/7 agent 给 < 50 分 → **小改**
- 如果 Devil's Advocate 找到 ≥ 3 个具体反例 → **必须回应对应章节**
- 如果 EIC 给 ≥ 80 + 6/7 agent ≥ 70 → **可接受**

**汇总输出**：`reviews/00-summary.md`

```markdown
# Synthesize Peer Review Summary

## 总评分（7-agent 平均）

| Agent | Score | Verdict |
|-------|-------|---------|
| EIC | 78/100 | Minor revision |
| Methodologist | 65/100 | Major revision |
| Domain Expert | 82/100 | Accept |
| Statistician | 71/100 | Minor revision |
| Writer | 75/100 | Minor revision |
| Reviewer 2 | 70/100 | Minor revision |
| Devil's Advocate | 58/100 | Major concerns |
| **平均** | **71.3/100** | **Minor revision** |

## 必须修复的 P0 问题
1. [Methodologist] 第 3.2 节 PRISMA 流程图缺数字
2. [Devil's Advocate] 第 4.1 节 overclaim：把"相关"说成"因果"

## 建议修改的 P1 问题
1. [Domain Expert] 缺 2024 年关键文献 XXX
2. [Statistician] 异质性 I² = 78% 应做敏感性分析
...

## R&R Traceability Matrix（作者回复追踪）
| 问题 | 章节 | 状态 | 作者回复 |
|------|------|------|---------|
| P0-1 | 3.2 | 已修 | 加了 n=X |
| P0-2 | 4.1 | 已改 | 改为"显著相关" |
| P1-1 | 4.3 | 待补 | 引用 PMID:xxx |
```

### Stage 4：backport 到 synthesize

根据 summary 修改 synthesize 文档（修订要留痕——加在文档末尾"Revision History"）。

---

## 🛠️ 集成到 research-assistant 工作流

| 阶段 | 用什么 |
|------|--------|
| synthesize extract 后 | **必跑**本 SOP |
| 改稿时 | 看 R&R Traceability Matrix |
| 终稿前 | 必须 P0 = 0，P1 ≥ 80% 已修 |

---

## 📋 各 Agent 评审清单

### Agent 1：EIC（5 维度 × 0-100）

- **Novelty**（新颖性）：是否填补研究缺口
- **Significance**（意义）：研究/实践价值
- **Rigor**（严谨性）：方法学质量
- **Clarity**（清晰度）：写作 + 结构
- **Impact**（影响力）：领域影响

**Verdict 阈值**：≥ 80 Accept / 60-79 Minor / 40-59 Major / < 40 Reject

### Agent 2：Methodologist（4 维度）

- PICO 是否明确
- 检索策略是否穷尽（多源 + 完整关键词）
- PRISMA 流程是否完整（流程图 + 数字 + 排除理由）
- 偏倚评估是否标准（Cochrane / ROBINS-I / NOS）

### Agent 3：Domain Expert（4 维度）

- 论点是否准确（事实性错误）
- 关键文献是否覆盖（近 3 年 + 经典）
- 与既有理论是否对话
- 概念使用是否规范

### Agent 4：Statistician（3 维度）

- 效应量 + 置信区间是否报告
- 异质性是否评估（I² + Q 检验）
- 偏倚评估是否定量（Egger's / funnel plot）

### Agent 5：Writer（3 维度）

- 章节逻辑（motivation 一致）
- APA 7 规范（引用 + 缩写 + 数字）
- 中英文学术表达

### Agent 6：Reviewer 2（4 维度）

- 论证链完整性（每个 claim 有支撑）
- 边界条件是否讨论
- future direction 是否具体
- 局限性是否诚实

### Agent 7：Devil's Advocate（5 维度）

- 找 3 个反例（是否有反例？作者忽略了？）
- 找 overclaim（"相关"vs"因果"/"显著"vs"重要"）
- 找 alternative explanation（其他解释是否讨论）
- 找选择性引用（只引支持自己观点的文献？）
- 找 cherry-picking（数据/结果是否选择性报告）

---

## ⚠️ 边界条件

| 不要做 | 原因 |
|--------|------|
| ❌ 不要把 7-agent 评审当成 LLM 单次提问 | 必须**结构化**每个 agent 独立 prompt |
| ❌ 不要跳过 Devil's Advocate | 它是**唯一主动找反例**的视角 |
| ❌ 不要让 EIC 给分后自动 Accept | 必须**所有** P0 修复后才能 Accept |
| ❌ 不要修改原 synthesize 文档而不留痕 | 必须在末尾加 Revision History |

---

## 🧪 测试用例（v5.21.0 内部测试用）

把现有的 `wiki/syntheses/2026-06-22-05-30-34-extract-buzsaki-2002-hippocampal-theta.md`（之前测试生成的）作为测试用例，跑 7-agent 评审，记录 baseline。

---

## 📚 参考

- ARS Paper Reviewer skill（7-agent + concession threshold protocol + R&R traceability）
- 来源仓库：https://github.com/Imbad0202/academic-research-skills
- 学术综述同行评议指南（Cochrane / PRISMA / Campbell Collaboration）

---

*最后更新：2026-06-22 v5.21.0*  
*来源借鉴：ARS Paper Reviewer（Imbad0202/academic-research-skills）*