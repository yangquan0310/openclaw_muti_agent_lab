# 心理学叙述性综述撰写指南

> **2026-06-12 实战沉淀**。心理学叙述性综述（Narrative Review / Narrative Synthesis in Psychology）是用**叙述性**方法（文字+表格）综合某一研究主题的原始文献，**不**做定量合并（不做 meta-analysis）。
> **报告规范**：APA 7 Publication Manual（Chapter 3: Journal Article Reporting Standards）+ APA 7 文献综述原则。
> 心理学叙述性综述遵循心理学领域的文献综述传统，以 APA 7th 为报告标准。
> **质量评估**（可选）：SANRA scale（Baethge 2019, *PLOS Medicine*）。
> **记住**：心理学叙述性综述是心理学的文献综合传统，与元分析、元分析**不**同。APA 7 文献综述结构是心理学领域的标准。

---

## 何时撰写心理学叙述性综述

| 场景 | 是否适用 |
|------|---------|
| 心理学领域某主题需要**综合**已有研究 | ✅ |
| 需要发展**理论框架**或**提出新模型** | ✅（叙述性综述的**独特优势**——可以 post hoc theorizing）|
| 异质性大 / 不适合定量合并 | ✅ |
| **需要**做定量合并 | ❌（改用元分析，JARS Table 9）|
| 不属于心理学文献综述 | ❌ |

---

## 心理学叙述性综述的特点

心理学叙述性综述在心理学领域有其**独特定位**：

- 关注**理论综合**和**概念框架**
- 允许**post hoc theorizing**（Baumeister & Leary 1997）
- 检索多个心理学数据库（PsycINFO, PsycARTICLES, Google Scholar 等）
- 用 APA 7 IMRAD 风格报告
- 主题综合（thematic synthesis）而非定量合并


## YAML 头示例（apaquarto-pdf）

```yaml
---
title: "某心理学构念的叙述性综述"
shorttitle: "叙述性综述 running head"
author:
  - name: "作者姓名"
    orcid: "0000-0000-0000-0000"
    corresponding: true
    affiliations:
      - id: aff1
        name: "机构名称"
        city: "城市"
        country: "中国"
author-note:
  disclosures:
    conflict-of-interest: "作者声明无利益冲突。"
abstract: |
  心理学文献综述用 narrative synthesis 综合某主题的已有研究。
  本文综述 X 主题，涵盖 4 个主要理论视角，提出整合性框架。
keywords: [关键词1, 关键词2, 关键词3]
bibliography: references.bib
format:
  apaquarto-pdf:
    documentmode: man
    keep-tex: true
---
```

---

## 标准结构（APA 7 风格 IMRAD）

> **APA 7 文献综述结构与一般实验/观察研究**类似：Introduction → Method → Results → Discussion → References，但**内容侧重**不同——Results 章节是 narrative synthesis 而非统计分析。

### 1. Title
- ✅ 明示 "review" 或 "narrative review"

### 2. Abstract
- ✅ 150-250 字结构化或非结构化摘要
- ✅ 简述范围、综述问题、主要发现

### 3. Introduction

#### 背景与综述问题
- ✅ 主题背景 + 文献缺口
- ✅ 综述目的（明确问题或假设）
- ✅ 范围界定

#### 心理学综述特有的"理论驱动"
- ✅ 早期就**提出理论框架**（Baumeister & Leary 1997 强调：文献综述**必须**有理论贡献）
- ✅ "One is to present one's full theoretical framework, then review the literature relevant to the theory. Alternatively, an author might provide a brief 'bottom-line' preview of the theory early, postponing its full elaboration until after the literature has been reviewed."

### 4. Method

> **APA 7 文献综述需要** Method 章节——描述检索/筛选/综合过程（让综述可评估）。

#### Search strategy
- ✅ 检索的**数据库**（PsycINFO, PsycARTICLES, PubMed, Web of Science, Google Scholar）
- ✅ 检索**关键词**和**时间范围**
- ✅ 纳入/排除标准

#### Selection process
- ✅ 文献选择的**理由**和**反思**
- ✅ 检索**限制**和**潜在偏倚**

#### Synthesis approach
- ✅ **Thematic synthesis**：按主题/理论/方法分组
- ✅ 或**Narrative synthesis**：按时间线或主题叙事
- ✅ **Critical appraisal**（每篇文献的优缺点）

### 5. Results / Synthesis

> **这是文献综述的核心**——不是统计分析，是**综合叙述**。

#### 主题综合（Thematic synthesis）
按主题分组，每组综合多篇文献：

```
主题一：X 理论视角
- 主要观点
- 代表性研究
- 证据强度
- 局限性
```

#### 理论贡献
- ✅ **不只是描述**——要**整合**多文献，**提出新理解**或**整合性模型**
- Baumeister & Leary 强调："It is usually necessary to present a full and vigorously integrative theoretical analysis"

#### 文献可视化
- 表格：研究特征（作者、年份、样本、方法、主要发现）
- 表格：理论对比
- 图：理论框架图

#### 与既往综述的关系
- 何时与既往综述一致/矛盾
- 本综述的**新贡献**

### 6. Discussion

#### Summary of evidence
- ✅ 简述主要发现

#### Limitations
- ✅ 检索范围局限（语言、数据库）
- ✅ 选择偏倚
- ✅ 作者主观性

#### Implications
- ✅ 理论意义
- ✅ 实践意义（应用、干预、政策）
- ✅ 未来研究

### 7. References
- APA 7 格式
- 用 `[@key]` 引用
- 不需要元分析风格的 `*` 标记

---

## SANRA Scale（质量评估工具，可选）

> **SANRA**（Baethge 2019, *PLOS Medicine*）是**叙述性综述质量评估**的 6 项工具，可用于自检或审稿。

| # | 项目 |
|---|------|
| 1 | 重要性（Justification of the article's importance）|
| 2 | 目标（Statement of concrete aims）|
| 3 | 方法描述（Description of literature search）|
| 4 | 检索（Referencing）|
| 5 | 推理（Scientific reasoning）|
| 6 | 表达（Presentation of relevant endpoints）|

每项 0-2 分，总分 ≥ 11 算高质量。

---

## 引用语法

| 类型 | 写法 | 输出 |
|------|------|------|
| 括号引用 | `[@Author2020]` | (Author et al., 2020) |
| 多引用 | `[@Author2020; @Author2021]` | (Author et al., 2020; Author et al., 2021) |
| 叙事引用 | `@Author2020` | Author et al. (2020) |
| 同一作者多文献 | `[@Author2020, @Author2020b]` | (Author et al., 2020, 2020b) |

**错误**：❌ `(Author, 2020)` — citeproc 不处理。

---

## 心理学叙述性综述的关键认知

1. **可以 post hoc theorizing** — 其他文体（系统综述/元分析）**严格禁止**（避免 capitalizing on chance），心理学叙述性综述**鼓励**（理论发展是核心贡献）
2. **必须有理论贡献** — 不仅是"文献清单"，要**整合**、**创新**
3. **可以结论为"证据不足"** — "the hypothesis has not been conclusively established but is the currently best guess" / "evidence permits no conclusion"（Baumeister & Leary 1997）
4. **APA 7 IMRAD 结构** — 与一般研究报告结构相同
5. **APA 7 IMRAD 风格**——和一般实验研究结构一致
7. **可参考 SANRA 自检** — 评估综述质量

---

## 实战要点

| 要点 | 说明 |
|------|------|
| **理论框架** | 早期就提出，不要"先罗列文献再理论化" |
| **批判性评估** | 每篇文献的优缺点、方法局限、矛盾结果 |
| **整合性表格** | 研究特征表 + 理论对比表 |
| **APA 7 标题页** | 标题、作者、单位、Author Note、Running head |
| **APA 7 标题级别** | 1-5 级，按需用 |
| **APA 7 引用** | 严格 author-date + 完整 References |
| **SANRA 自检** | 投前 6 项自评 |

---

## 关键参考文献

- **American Psychological Association**. (2020). *Publication manual of the American Psychological Association* (7th ed.). Chapter 3: Journal Article Reporting Standards. https://doi.org/10.1037/0000165-000
- Appelbaum, M., Cooper, H., Kline, R. B., Mayo-Wilson, E., Nezu, A. M., & Rao, S. M. (2018). Journal article reporting standards for quantitative research in psychology: The APA Publications and Communications Board task force report. *American Psychologist*, 73(1), 3-25. https://doi.org/10.1037/amp0000191
- **Baumeister, R. F., & Leary, M. R.** (1997). Writing narrative literature reviews. *Review of General Psychology*, 1(3), 311-320. https://doi.org/10.1037/1089-2680.1.3.311 — **心理学叙述性综述的奠基论文**
- Baethge, C., Goldbeck-Wood, S., & Mertens, S. (2019). SANRA—a scale for the quality assessment of narrative review articles. *Research Integrity and Peer Review*, 4, 5. https://doi.org/10.1186/s41073-019-0064-8
- Cooper, H. (2017). *Research synthesis and meta-analysis* (5th ed.). Sage. — **APA 推荐综合方法教材**
- American Psychological Association. *Reporting quantitative research in psychology* (2nd ed., revised). — **JARS + MARS 应用指南**

---

## 版本历史

| 版本 | 日期 | 更新 |
|------|------|------|
| v1.0 | 2026-06-12 | 初版：基于心理学 APA 7 + JARS-Quant 规范；融入 Baumeister & Leary 1997 理论贡献核心。 |