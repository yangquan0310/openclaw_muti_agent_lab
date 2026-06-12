# 心理学实验研究报告撰写指南

> **2026-06-12 实战沉淀**。心理学实验研究（Experimental Study）——研究者**主动操纵**自变量、随机分配参与者、测量因变量的研究。
> **报告标准**：APA 7 Publication Manual（Chapter 3）+ **JARS-Quant Table 2: Experimental Designs**（Appelbaum et al., 2018）。
> **关键认知**：心理学实验研究遵循 **APA 7 + JARS-Quant Table 2**——心理学自己的实验报告标准。心理学实验报告**核心**是 APA 7 IMRAD 结构 + JARS 报告清单。

---

## 何时撰写心理学实验研究报告

| 研究设计 | 报告标准 | 典型场景 |
|----------|----------|----------|
| **完全随机设计** | JARS-Quant Table 2 | 经典心理实验 |
| **因子设计** | JARS-Quant Table 2 | 多自变量交互作用 |
| **随机区组设计** | JARS-Quant Table 2 | 匹配参与者后随机 |
| **重复测量设计** | JARS-Quant Table 2 | 同一参与者接受多个条件 |
| **混合设计** | JARS-Quant Table 2 | 部分被试间 + 部分被试内 |
| **临床试验**（心理治疗干预）| JARS-Quant 临床试验清单 | 干预性心理治疗 RCT |
| **准实验** | JARS-Quant Table 3 | 非随机分配（如自然组）|

---


---

## YAML 头示例（apaquarto-pdf）

```yaml
---
title: "X 操纵对 Y 心理结局的效果：随机对照实验"
shorttitle: "实验研究 running head"
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
  ethics: "本研究经 XX 大学伦理委员会批准（IRB#XXXX）。"
abstract: |
  检验 X 操纵对 Y 心理结局的因果效应。N=XXX 名参与者
  随机分配到 [实验组/对照组]，操纵 [X]，测量 [Y]。
  结果：实验组 Y 显著高于/低于对照组，d = X.XX, p < .05。
  结论：X 影响 Y。
keywords: [关键词1, 关键词2, 关键词3]
bibliography: references.bib
format:
  apaquarto-pdf:
    documentmode: man
    keep-tex: true
---
```

---

## 标准结构（APA 7 IMRAD + JARS-Quant Table 2）

### 1. Title
- ✅ 简明描述研究 + 主要变量
- ✅ 包含操纵+关键自变量

### 2. Abstract
- 背景、目的、方法（设计、参与者、操纵、测量、统计）、结果、结论

### 3. Introduction
- ✅ 理论背景 + 实证基础
- ✅ 明确研究问题 + **预设假设**
- ✅ 与既有研究关系

### 4. Method

#### 4.1 Participants
- 人口学特征
- 招募方式
- 样本量 + 功效分析
- 伦理审批（IRB）+ 知情同意

#### 4.2 Design
- ✅ **JARS-Quant Table 2**：明确报告自变量、因变量、控制变量
- 完全随机 / 因子 / 重复测量 / 混合

#### 4.3 Materials
- ✅ 完整报告所有测量工具
- ✅ 心理量表的信度（Cronbach's α / ω）
- ✅ 操纵材料（图片、文字、刺激）
- ✅ 软件 / 实验程序

#### 4.4 Procedure
- ✅ 完整数据收集流程
- ✅ 随机化方法（计算机随机数表、抽签、掷骰子）
- ✅ 盲法（参与者盲、数据分析者盲）
- ✅ 操控检验（manipulation check）

#### 4.5 Data analysis
- ✅ 缺失数据处理
- ✅ 操控检验结果分析
- ✅ 主要假设检验
- ✅ **效应量 + 95% CI**（**不**只报 p 值）
- ✅ 软件 + 版本

### 5. Results

#### 5.1 Preliminary / Manipulation checks
- ✅ 操控检验结果（是否成功操纵自变量）
- ✅ 描述性统计

#### 5.2 Main analyses
- ✅ 假设检验结果
- ✅ 效应量 + CI
- ✅ **Tables + Figures**（APA 风格）
- ✅ 报告所有分析

#### 5.3 Supplementary analyses
- 探索性分析、敏感性分析

### 6. Discussion

#### Summary
- ✅ 主要发现

#### 与既有研究比较
- ✅ 一致 / 矛盾

#### 理论意义
- ✅ 解释为什么发现支持/拒绝假设

#### Limitations
- ✅ 内部效度威胁
- ✅ 外部效度（generalizability）
- ✅ 测量局限

#### Implications & future research
- ✅ 理论
- ✅ 实践
- ✅ 未来研究

### 7. References

---

## 心理学实验研究特有问题

### 操控检验（Manipulation Check）
- ✅ **必报**：自变量操纵是否成功
- 用独立样本 t-test 或 ANOVA
- 不通过 = 整篇 paper 受影响

### 内部效度
- ✅ 随机化（避免选择偏倚）
- ✅ 操控自变量
- ✅ 控制混淆变量
- ✅ 控制需求特征（demand characteristics）

### 外部效度
- ✅ 样本的**代表性**
- ✅ 任务/情境的**生态效度**（ecological validity）

### 效应量报告
- ✅ **必报** Cohen's d, η², partial η², β
- 心理学约定：**p 值 + 效应量**
- 与 Power Analysis 对照

### 预注册（Pre-registration）
- ✅ **OSF**（Open Science Framework）
- ✅ 区分**预设**vs**探索性**分析

---

## 引用语法

| 类型 | 写法 | 输出 |
|------|------|------|
| 括号引用 | `[@Author2020]` | (Author et al., 2020) |
| 多引用 | `[@Author2020; @Author2021]` | (Author et al., 2020; Author et al., 2021) |
| 叙事引用 | `@Author2020` | Author et al. (2020) |
| 同作者多文献 | `[@Author2020, @Author2020b]` | (Author et al., 2020, 2020b) |

---

## 心理学实验研究实战要点

| 要点 | 说明 |
|------|------|
| **预注册** | OSF 预注册**强烈推荐**（区分 confirmatory vs exploratory）|
| **样本量** | 必报告功效分析（power analysis）|
| **随机化** | 报告具体随机化方法（**不**是"随机"两字）|
| **操控检验** | 必报，否则不发表 |
| **盲法** | 报告谁被盲（参与者/分析者/评估者）|
| **效应量** | 必报（不只 p 值）|
| **数据共享** | OSF / GitHub 公开 |
| **数据处理** | 报告预处理决策（异常值、缺失、转换）|
| **APA 7 标题级别** | Level 1-5 按需用 |

---

## 多实验论文结构

心理学常**多实验报告**（如 3 个研究验证效应稳健性）：

```
Introduction（总背景 + 总假设）
Experiment 1
  Method
  Results
  Discussion
Experiment 2
  Method
  Results
  Discussion
Experiment 3
  Method
  Results
  Discussion
General Discussion（总讨论 + 理论贡献）
References
```

每个实验有**独立**的 Method/Results/Discussion，**最后** General Discussion 综合所有实验。

---

## 关键参考文献

- **American Psychological Association**. (2020). *Publication manual* (7th ed.). Chapter 3: Journal Article Reporting Standards. https://doi.org/10.1037/0000165-000
- Appelbaum, M., Cooper, H., Kline, R. B., Mayo-Wilson, E., Nezu, A. M., & Rao, S. M. (2018). Journal article reporting standards for quantitative research in psychology: The APA Publications and Communications Board task force report. *American Psychologist*, 73(1), 3-25. https://doi.org/10.1037/amp0000191 — **JARS-Quant Table 2 (Experimental)**
- Cohen, J. (1988). *Statistical power analysis for the behavioral sciences* (2nd ed.). — **效应量必读**
- Field, A. (2024). *Discovering statistics using IBM SPSS Statistics* (6th ed.). Sage. — **SPSS 实战**
- Maxwell, S. E., Delaney, H. D., & Kelley, K. (2018). *Designing experiments and analyzing data* (3rd ed.). — **实验设计**
- Nosek, B. A., Ebersole, C. R., et al. (2018). The preregistration revolution. *PNAS*, 115(11), 2600-2606. — **预注册**
- Simmons, J. P., Nelson, L. D., & Simonsohn, U. (2011). False-positive psychology. *Psychological Science*, 22(11), 1359-1366. — **p-hacking 警告**

---

## 版本历史

| 版本 | 日期 | 更新 |
|------|------|------|
| v1.0 | 2026-06-12 | 初版：基于心理学 APA 7 + JARS-Quant Table 2；强调操控检验、内部效度、效应量、预注册。 |