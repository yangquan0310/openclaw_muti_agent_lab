# Nature Style Polishing Prompt（v5.21.0 新增）

> 来源：吸收 Nature-skills（Yuan1z0825/nature-skills）polishing + ARS Academic Paper Style Calibration  
> 用途：把研究助手写的中文笔记润色成 **Nature 风格学术表达**（可直接投稿或转英文）  
> 适配：`summarize` / `synthesize` 输出后接 polish 步骤

---

## 🎯 Nature 风格核心特征

| 维度 | Nature 风格 | 普通学术 |
|------|------------|---------|
| **句式** | 简洁、主动语态、信息密度高 | 冗长、被动、修饰多 |
| **动词** | 精确动词（demonstrate / reveal / establish）| 模糊动词（study / discuss / show）|
| **连接词** | 显式逻辑（however / thus / crucially）| 弱连接（同时 / 另外 / 此外）|
| **观点强度** | 不过度断言（suggest / indicate / appear）| 过度断言（证明 / 显然 / 必然）|
| **避免** | we / I / very / really / obviously | 多用 we + 模糊词 |

---

## 🔧 Polishing Prompt（中文笔记 → Nature 风格中文）

```markdown
# Nature Style Polishing Prompt

## 任务
把以下【原始笔记】润色成 **Nature 期刊风格的学术中文**。

## 润色规则

### 1. 句式
- 改长句为短句（一句话 ≤ 35 字）
- 改被动为主动（如"被研究" → "我们研究"或"研究显示"）
- 删除冗余修饰（"非常/极其/相当"等程度副词）

### 2. 词汇
- 用精确动词替代模糊动词：
  - "研究" → "调查 / 检验 / 评估 / 揭示"
  - "显示" → "表明 / 提示 / 揭示"
  - "讨论" → "分析 / 论证 / 阐释"
- 用名词化表达理论/概念：
  - "能记住" → "表现出工作记忆能力"
  - "做得更好" → "表现优于"

### 3. 逻辑连接
- 显式逻辑词（**然而 / 因此 / 关键地 / 值得注意的是**）
- 因果关系用"鉴于...因此..."结构
- 对比用"相比之下 / 与...不同 / 相反"

### 4. 观点强度校准
- 避免断言（"证明 / 必然 / 显然"）→ 改为推断（"提示 / 表明 / 可能"）
- 相关≠因果：correlation 译"相关"，causation 译"因果"
- 显著性≠重要性：significant 译"显著（统计）"，important 译"重要（实质）"

### 5. 中英对照
- 关键术语首次出现给英文（如"工作记忆（working memory）"）
- 理论/模型首次出现给原文 + 缩写（如"长时程增强（LTP, long-term potentiation）"）

## 输出格式

```markdown
## 原文（Original）
[原始中文]

## 润色后（Polished, Nature Style）
[润色后的中文]

## 关键改动说明（Diff Notes）
- 句式：[哪句改了，为啥]
- 词汇：[哪个模糊词 → 精确词]
- 逻辑：[新增的连接词]
- 强度：[哪个断言 → 推断]
```

## 原始笔记
[粘贴需要润色的笔记]

---

## 📋 Style Calibration Checklist（润色后自检）

每篇润色完跑一次：

| 检查项 | 是/否 |
|--------|-------|
| 一句话 ≤ 35 字 | |
| 主动语态 > 80% | |
| 模糊动词已替换 | |
| 显式逻辑词密度 ≥ 1/段 | |
| 无 "非常/极其/显然/必然" | |
| 相关≠因果 区分 | |
| 关键术语给英文对照 | |
| 缩写首次给全称 | |
```

---

## 🛠️ 集成到 research-assistant

### 工作流

```
summarize / synthesize 输出
        ↓
Polish (本 prompt)
        ↓
Style Calibration Checklist 自检
        ↓
如有英文 paper 需求：再走"中→英转写"prompt（不在本 SOP 范围）
```

### 命令式调用（如果用户装了 polish skill）

```bash
# 假设有 polish skill
polish --input wiki/syntheses/<file>.md \
       --style nature-zh \
       --output wiki/syntheses/<file>-polished.md
```

如果没装 skill，就**手工复制本 prompt + 笔记**到 LLM 跑。

---

## 📋 反例 vs 正例（教学用）

| 反例 ❌ | 正例 ✅ | 改了什么 |
|--------|--------|---------|
| 我们非常仔细地研究了海马中的 theta 振荡，结果显示它非常明显地和工作记忆有关系。 | 我们系统调查了海马 theta 振荡（4-8 Hz）与工作记忆的关系。结果表明，theta 功率与记忆负荷呈显著正相关（r=0.72, p<0.001）。 | 长→短、模糊→精确、断言→推断、加统计量 |
| 这个发现证明了我们之前的假设。 | 这一发现支持我们此前的假设，但因果方向仍需纵向研究验证。 | 断言→支持 + 边界条件 |
| 有很多研究都做了类似的事情。 | 既往研究主要关注 theta 频率分析（Buzsáki 2002; Lisman 2010），但对跨频耦合（theta-gamma coupling）的功能意义研究较少。 | 模糊→具体 + 引用 |

---

## ⚠️ 边界条件

| 不要做 | 原因 |
|--------|------|
| ❌ 不要把所有断言都改"模糊" | Nature 也有强断言（如"已确立"）|
| ❌ 不要把英文术语全删 | 学术中文需要中英对照 |
| ❌ 不要改引用的具体数字 | 数字是事实，不能动 |
| ❌ 不要加新论点 | 这是润色不是改写 |

---

## 📚 参考

- Nature-skills nature-polishing：https://github.com/Yuan1z0825/nature-skills
- ARS Academic Paper Style Calibration：https://github.com/Imbad0202/academic-research-skills
- Nature 写作风格指南（Springer Nature Author Services）

---

*最后更新：2026-06-22 v5.21.0*  
*来源借鉴：Nature-skills + ARS Academic Paper*