---
title: "[X 干预对 Y 心理结局的效果：系统综述与元分析]"
shorttitle: "Running head（≤50 字符）"

author:
  - name: "TBD"
    corresponding: true
    affiliations:
      - id: tbd
        name: "TBD"
        city: "TBD"
        country: "TBD"

author-note:
  disclosures:
    conflict-of-interest: "作者声明无利益冲突。"

abstract: |
  [背景 + 目的 + 方法（数据库、纳入标准、效应量类型、合并模型、I² 异质性、敏感性）+ 结果（合并效应量 + 95% CI）+ 结论]

keywords:
  - 关键词1
  - 关键词2
  - 关键词3

floatsintext: false
numbered-lines: false
word-count: false
draft-date: false

bibliography: references.bib

format:
  apaquarto-pdf:
    documentmode: man
    keep-tex: true
---


# Introduction

## 背景

[理论背景 + 实证基础 + 元分析必要性]

## 研究问题

[用 PICO 框架明确]

## 假设

[主要假设 + 次要假设]


# Method

## Eligibility Criteria

- **研究设计**：[RCT / 队列 / 病例对照 / 横断面]
- **PICO 要素**：
  - P（参与者）：[年龄、性别、特征]
  - I（干预）：[类型、剂量、持续时间]
  - C（对照）：[对照类型]
  - O（结局）：[主要结局 + 次要结局]
- **时间范围**：[YYYY-YYYY]
- **语种**：[中 / 英 / 不限]
- **发表状态**：[已发表 / 灰色文献也收]

## Information Sources & Search Strategy

- **数据库**：PsycINFO, PsycARTICLES, PubMed, Web of Science, Google Scholar
- **关键词**：[关键词1, 关键词2]（含 MeSH 和 free text）
- **检索日期**：[YYYY-MM-DD]
- **完整检索式**：附录 A

## Study Selection & Data Extraction

- 筛选流程：两人独立筛选 + 第三方仲裁
- 提取内容：第一作者、年份、样本量、干预细节、结局效应量

## Risk of Bias Assessment

[JARS-Quant Table 2 / Cochrane RoB 2.0]

## Statistical Methods

### 效应量选择

- **连续结局（同一量表）**：[Cohen's d, MD]
- **连续结局（不同量表）**：[SMD, Hedges' g]
- **二分类结局**：[OR, RR, RD]
- **回归/相关**：[β, r]

### 合并模型

- **Fixed-effect**：[理由 I² < 25%]
- **Random-effects**：[理由 I² > 25%，多数心理学元分析推荐]
- **异质性评估**：I², Q 检验, τ²
- **软件 + 版本**：[R `metafor` 4.x / Stata 18 / JASP 0.x]

### Publication Bias

- **漏斗图**（funnel plot）
- **Egger's 检验** / **Begg-Mazumdar 检验**
- **修剪填补法**（trim-and-fill）
- **失安全数**（fail-safe N）

### Sensitivity & Subgroup

- 按 RoB 分层
- 按 PICO 差异分层
- Leave-one-out


# Results

## Study Selection

[Flow diagram / 文字描述各阶段筛选数]

## Study Characteristics

[Table 1：作者、年份、样本、构念、效应量、CI]

## Risk of Bias

[RoB 评估结果汇总]

## Results of Synthesis

- **Forest plot**（必备）—— 每个研究 + 合并效应量
- 异质性评估结果（I², Q, τ²）
- 亚组分析 Forest plot
- 敏感性分析
- 发表偏倚（漏斗图 + Egger's）

## Reporting Biases

[漏斗图 + Egger's + 必要时修剪填补]


# Discussion

## Summary

[主要发现（合并效应量 + 心理学解释）]

## 与既往元分析比较

[对比]

## 异质性来源

[详细分析]

## Limitations

[研究质量、检索局限、发表偏倚、心理学特有限制]

## 实践意义

[临床/应用/政策推荐]

## 未来研究

[原始研究 + 元分析更新方向]


# References

::: {#refs}
:::
