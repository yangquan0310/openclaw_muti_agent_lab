# 心理学观察研究报告撰写指南

> **2026-06-12 实战沉淀**。心理学观察性研究（Observational Study in Psychology）——不施加干预、观察变量间自然关联的研究。
> **报告标准**：APA 7 Publication Manual（Chapter 3）+ **JARS-Quant Tables 1, 5, 6**（Appelbaum et al., 2018, *American Psychologist*）。
> **关键认知**：心理学观察性研究遵循 **APA 7 + JARS-Quant Tables 1, 5, 6**——心理学自己的报告标准。心理学"观察性研究"包括：问卷研究、相关研究、横断面研究、纵向观察、现有数据分析。

---

## 何时撰写心理学观察性研究

| 研究设计 | 报告标准 | 典型场景 |
|----------|----------|----------|
| **问卷研究**（Survey）| JARS-Quant Table 5（无实验操作）| 心理量表施测、态度调查 |
| **相关研究**（Correlational）| JARS-Quant Table 5 | 两个或多个变量的相关 |
| **横断面研究**（Cross-sectional）| JARS-Quant Table 5 | 同一时点测量 |
| **纵向研究**（Longitudinal）| **JARS-Quant Table 6** | 多时点测量，可推断时序 |
| **现有数据分析**（Secondary data analysis）| JARS-Quant Table 1 | 用已有数据集 |
| **临床访谈 / 观察** | APA 7 + JARS-Qual（定性）| 临床案例 |

---


---

## YAML 头示例（apaquarto-pdf）

```yaml
---
title: "X 与 Y 的关系：一项横断面问卷研究"
shorttitle: "观察性研究 running head"
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
  ethics: "本研究经 XX 大学伦理委员会批准。"
abstract: |
  本研究探讨 X 与 Y 的关系。N=XXX 名参与者，
  通过 [量表] 测量 X 和 Y，[统计方法] 分析。
  结果：X 与 Y 显著相关/预测，r / β = ...
keywords: [关键词1, 关键词2, 关键词3]
bibliography: references.bib
format:
  apaquarto-pdf:
    documentmode: man
    keep-tex: true
---
```

---

## 标准结构（APA 7 IMRAD + JARS-Quant Table 5）

### 1. Title
- ✅ 简明描述研究 + 设计（"correlational study" / "survey" / "cross-sectional"）
- ✅ 包含主要变量

### 2. Abstract
- 背景、目的、方法（设计、参与者、测量、统计）、结果、结论

### 3. Introduction
- ✅ 理论背景 + 实证基础
- ✅ 明确研究问题 + **预设假设**
- ✅ 与既有研究关系

### 4. Method

#### 4.1 Participants
- ✅ **JARS-Quant 重点**：**人口学**、招募方式、招募率、流失率
- 样本量计算 + 功效分析（power analysis）
- 伦理审批（IRB）

#### 4.2 Measures
- ✅ **心理学特异**：量表的**信度**（Cronbach's α, McDonald's ω, ICC）
- ✅ **效度**（construct, convergent/discriminant, criterion）
- 完整报告所有测量工具

#### 4.3 Procedure
- ✅ 数据收集流程
- ✅ 知情同意
- ✅ 时间、地点、奖励

#### 4.4 Data analysis
- ✅ 缺失数据处理
- ✅ 异常值检测
- ✅ 假设检验（正态性、方差齐性等）
- ✅ 统计方法（回归 / SEM / HLM / 贝叶斯）
- ✅ 软件 + 版本
- ✅ 效应量 + 95% CI（**不**只是 p 值）
- ✅ 多重比较校正

### 5. Results

#### 5.1 Preliminary analyses
- ✅ 描述性统计（M, SD）
- ✅ 变量相关矩阵
- ✅ 信度（Cronbach's α）
- ✅ 正态性、缺失数据

#### 5.2 Main analyses
- ✅ 假设检验结果
- ✅ 效应量 + CI
- ✅ **Tables + Figures**（APA 风格）
- ✅ 报告所有分析（含不显著的结果）

### 6. Discussion

#### Summary
- ✅ 主要发现

#### 与既往研究比较
- ✅ 一致 / 矛盾 / 拓展

#### Limitations
- ✅ 因果推断局限（观察性研究**不能**推断因果）
- ✅ 共同方法偏差（common method bias）
- ✅ 自我选择偏差（self-selection）
- ✅ 测量局限

#### Implications
- ✅ 理论
- ✅ 实践
- ✅ 未来研究

### 7. References

### 8. Tables / Figures

---

## 心理学观察性研究特有问题

### 共同方法偏差（Common Method Bias）
- ✅ **必报**：自我报告问卷研究**几乎**有共同方法偏差
- 用 Harman 单因子检验
- 用 Common Latent Factor (CLF) 控制

### 因果推断局限
- ✅ **不**可推断因果（横断面/相关研究**不能**说 X 引起 Y）
- 用相关、预测、关联等措辞
- **只有**纵向 + 实验 + 反事实推理才可推断因果

### 量表信效度报告
- ✅ Cronbach's α / McDonald's ω
- ✅ CFA 验证 factor structure
- ✅ 收敛/区分效度（如适用）

---

## 引用语法

| 类型 | 写法 | 输出 |
|------|------|------|
| 括号引用 | `[@Author2020]` | (Author et al., 2020) |
| 多引用 | `[@Author2020; @Author2021]` | (Author et al., 2020; Author et al., 2021) |
| 叙事引用 | `@Author2020` | Author et al. (2020) |
| 同作者多文献 | `[@Author2020, @Author2020b]` | (Author et al., 2020, 2020b) |

---

## 心理学观察性研究实战要点

| 要点 | 说明 |
|------|------|
| **样本量** | 必报告功效分析，pilot test 验证测量 |
| **量表** | 必报告信度 + 效度（不能只用 α）|
| **缺失数据** | 报告缺失率 + 处理方法（多插补 / FIML）|
| **效应量** | 必报告（**不**只报 p 值）—— Cohen's d, r², β |
| **共同方法偏差** | 自我报告问卷必检 |
| **因果** | 不用"cause"，用"predict", "associate" |
| **多变量** | 用 SEM / 路径分析，**不**用单纯相关 |
| **纵向** | 用 HLM / LMM 处理嵌套数据 |

---

## 关键参考文献

- **American Psychological Association**. (2020). *Publication manual* (7th ed.). Chapter 3: Journal Article Reporting Standards. https://doi.org/10.1037/0000165-000
- Appelbaum, M., Cooper, H., Kline, R. B., Mayo-Wilson, E., Nezu, A. M., & Rao, S. M. (2018). Journal article reporting standards for quantitative research in psychology: The APA Publications and Communications Board task force report. *American Psychologist*, 73(1), 3-25. https://doi.org/10.1037/amp0000191 — **JARS-Quant Table 5 (Observational) + Table 6 (Longitudinal)**
- Podsakoff, P. M., MacKenzie, S. B., Lee, J. Y., & Podsakoff, N. P. (2003). Common method biases in behavioral research: A critical review of the literature and recommended remedies. *Journal of Applied Psychology*, 88(5), 879-903. — **共同方法偏差必读**
- Cohen, J. (1988). *Statistical power analysis for the behavioral sciences* (2nd ed.). — **效应量必读**
- Hayes, A. F. (2022). *Introduction to mediation, moderation, and conditional process analysis* (3rd ed.). — **中介调节分析**

---

## 版本历史

| 版本 | 日期 | 更新 |
|------|------|------|
| v1.0 | 2026-06-12 | 初版：基于心理学 APA 7 + JARS-Quant Tables 1, 5, 6；强调量表信效度、共同方法偏差、因果推断局限。 |