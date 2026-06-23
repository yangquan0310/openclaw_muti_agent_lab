# 心理学元分析撰写指南

> **2026-06-12 实战沉淀**。心理学元分析（Meta-analysis in Psychology）是用**统计方法合并**多个原始研究效应量的研究方法。
> **报告标准**：APA 7th + **JARS Table 9: Meta-Analysis Reporting Standards (MARS)**（Appelbaum et al., 2018, *American Psychologist*）。
> **关键认知**：心理学元分析遵循 APA 出版的 **JARS-Quant Table 9 (MARS)**——心理学自己的元分析报告标准。

---

## 何时撰写心理学元分析

| 场景 | 是否适用 |
|------|---------|
| 多个原始研究有**可合并的效应量**（d, r, OR, β）| ✅ |
| 研究**同质**（相同构念、相同方法）| ✅ |
| 异质性可解释 | ✅（random-effects + 亚组）|
| **研究方法异质**（实验 + 问卷 + 神经影像）| ❌（改用叙述性综述）|
| 缺乏效应量或数据 | ❌（考虑 IPD）|

---


---

## YAML 头示例（apaquarto-pdf）

```yaml
---
title: "X 干预对 Y 心理结局的效果：元分析"
shorttitle: "元分析 running head"
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
  用元分析综合 X 干预对 Y 心理结局的效果。检索 PsycINFO 等数据库，
  纳入 K 项研究，N 名参与者，random-effects 合并，
  I² 评估异质性，Egger's 检验发表偏倚。
keywords: [关键词1, 关键词2, 关键词3]
bibliography: references.bib
format:
  apaquarto-pdf:
    documentmode: man
    keep-tex: true
---
```

---

## 标准结构（基于 JARS Table 9 + APA 7 IMRAD）

> JARS Table 9（MARS）的元分析报告**结构上**仍按 APA 7 IMRAD，**额外**强调"统计方法"和"结果综合"两节。

### 1. Title
- ✅ 明示 "meta-analysis"
- ✅ 描述 PICO 要素

### 2. Abstract（APA 7 摘要）
- 背景、目的、方法（来源、纳入、效应量、合并模型、异质性、敏感性）
- 结果（合并效应量 + 95% CI、I²、纳入研究数、样本量）
- 结论

### 3. Introduction
- ✅ PICO/PECO 框架
- ✅ 陈述"为什么需要元分析"（效应大小不明 + 多研究矛盾）

### 4. Method

#### 4.1 Eligibility criteria
- 研究设计
- 参与者特征
- 干预/暴露
- 结局
- 时间范围、语言、发表状态

#### 4.2 Information sources & Search strategy
- **数据库**：PsycINFO, PsycARTICLES, PubMed, Web of Science, Google Scholar, ProQuest Dissertations
- 检索词：关键词 + 主题词
- 检索日期

#### 4.3 Study selection & Data collection
- 筛选流程（**JARS Table 9 要求**）
- 两人独立筛选 + 提取
- 提取：**效应量**（d, r, g, OR, β）

#### 4.4 Risk of bias
- **JARS-Quant Table 2**（实验研究）或 Cochrane RoB 2.0

#### 4.5 **Statistical methods**（元分析核心，JARS Table 9）

**效应量计算**：

| 心理学结局 | 效应量 |
|------------|--------|
| 连续结局（均值差）| Cohen's **d**, Hedges' **g** |
| 相关 | Pearson **r**, Fisher **z** |
| 回归 | **β**（标准化回归系数）|
| 方差分析 | **η²**, partial **η²** |
| 比例 | **OR**, log OR |
| 总体效应估计 | 合成 d / r / OR |

**合并模型**：
- **Fixed-effect**（I² < 25%，研究同质）
- **Random-effects**（I² > 25%，更保守，**多数心理学元分析推荐**）
- 异质性：I², Q 检验, τ²

**软件**：
- R `metafor` (Viechtbauer) — 主流
- R `psychmeta` (心理学专用)
- R `meta`
- SPSS + macros
- JASP
- Stata `metan`, `meta`
- Comprehensive Meta-Analysis (CMA)

**发表偏倚**：
- **漏斗图**（funnel plot）
- **Egger's 检验** / **Begg-Mazumdar 检验**
- **修剪填补法**（trim-and-fill）
- **失安全数**（fail-safe N）

**敏感性 & Subgroup**：
- 按 RoB 分层
- 按 PICO 差异分层
- Leave-one-out

#### 4.6 元分析的开放科学（**APA 强烈推荐**）
- ✅ **预注册**（OSF, PROSPERO for psychology）
- ✅ **数据 + 代码公开**（OSF, GitHub）
- ✅ **完整检索式附录**

### 5. Results

#### 5.1 Study selection
- **Flow diagram 推荐**（JARS Table 9 推荐；非强制但强烈建议）

#### 5.2 Study characteristics
- **特征表**（Table 1）：作者、年份、样本、构念、效应量、CI

#### 5.3 Risk of bias
- RoB 评估结果

#### 5.4 **Results of individual studies**
- 每个纳入研究的效应量表

#### 5.5 **Results of synthesis**（**元分析核心**）
- **Forest plot**（必备）
- 异质性评估结果
- 亚组分析 Forest plot
- 敏感性分析结果
- 发表偏倚（漏斗图 + Egger's）

#### 5.6 Reporting biases
- 漏斗图 + Egger's
- 必要时修剪填补

### 6. Discussion

#### Summary
- 主要发现（合并效应量 + 心理学解释）

#### 与既往元分析比较
- 与 Cochrane Reviews 等对比

#### 异质性来源
- 详细分析

#### 局限
- 研究质量、检索局限、发表偏倚
- 心理学特有限制（如样本量小、效应量估计偏倚）

#### 实践意义
- 临床/应用/政策推荐

#### 未来研究
- 原始研究 + 元分析更新

### 7. References
- APA 7 格式
- 用 `[@key]` 引用

---

## apaquarto 元分析特殊配置

apaquarto 不需要 `meta-analysis: true` 字段。APA 7 引用由 citeproc + CSL 处理。

YAML 头**不要**写：
```yaml
# ❌ 错误
meta-analysis: true
nocite: | @Study1, @Study2
```

**APA 7 风格的元分析** = 普通 APA 7 报告 + 效应量统计章节。

---

## 引用语法

| 类型 | 写法 | 输出 |
|------|------|------|
| 括号引用 | `[@Author2020]` | (Author et al., 2020) |
| 多引用 | `[@Author2020; @Author2021]` | (Author et al., 2020; Author et al., 2021) |
| 叙事引用 | `@Author2020` | Author et al. (2020) |
| 同作者多文献 | `[@Author2020, @Author2020b]` | (Author et al., 2020, 2020b) |

---

## 心理学元分析常用工具

| 工具 | 用途 |
|------|------|
| R `metafor` (Viechtbauer) | 主流元分析包，固定/随机效应、meta-regression |
| R `psychmeta` | 心理学专用元分析 |
| R `meta` | 简单易用，Forest plot |
| JASP | 心理学友好 GUI 元分析 |
| SPSS + macros | 心理学研究者熟悉 |
| Stata `metan` | 经典元分析命令 |
| CMA | 商业软件，心理学常用 |
| OSF | 注册和公开研究材料 |

---

## 实战要点

| 要点 | 说明 |
|------|------|
| **预注册** | OSF（必做）；心理学元分析**强烈推荐**预注册 |
| **公开代码** | R script + 数据 → OSF/GitHub |
| **完整检索式** | 必备附录（**注意**心理学领域）|
| **Flow diagram** | JARS Table 9 **推荐**（非强制）|
| **Forest plot** | 必备 |
| **异质性评估** | I² + Q + τ² |
| **发表偏倚** | 漏斗图 + Egger's |
| **效应量** | 心理学用 d, r, OR（**不**用 RR）|
| **异质性大时** | random-effects + 亚组 + meta-regression |
| **代码可重复性** | 心理学 APA 强烈要求 |

---

## 关键参考文献

- **American Psychological Association**. (2020). *Publication manual* (7th ed.). Chapter 3, Section 3.7 (Meta-Analysis). https://doi.org/10.1037/0000165-000
- Appelbaum, M., Cooper, H., Kline, R. B., Mayo-Wilson, E., Nezu, A. M., & Rao, S. M. (2018). Journal article reporting standards for quantitative research in psychology: The APA Publications and Communications Board task force report. *American Psychologist*, 73(1), 3-25. https://doi.org/10.1037/amp0000191 — **JARS-Quant Table 9** (MARS)
- **Cooper, H.** (2017). *Research synthesis and meta-analysis* (5th ed.). Sage. — **APA 推荐教材**
- American Psychological Association. *Reporting quantitative research in psychology* (2nd ed., revised). — **JARS + MARS 应用指南**
- Borenstein, M., Hedges, L. V., Higgins, J. P. T., & Rothstein, H. R. (2009). *Introduction to meta-analysis*. Wiley. — **经典通用元分析教材**
- Lipsey, M. W., & Wilson, D. B. (2001). *Practical meta-analysis*. Sage. — **心理学应用**
- Viechtbauer, W. (2010). Conducting meta-analyses in R with the metafor package. *Journal of Statistical Software*, 36(3), 1-48.

---

## 版本历史

| 版本 | 日期 | 更新 |
|------|------|------|
| v1.0 | 2026-06-12 | 初版：基于心理学 **JARS-Quant Table 9 (MARS)**；APA 7 风格 IMRAD；效应量用 d/r/OR；强调预注册 + 代码公开。 |