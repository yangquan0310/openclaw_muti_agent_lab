---
pageType: concept
id: concept.delay-discounting
createdAt: 2026-05-23
updatedAt: 2026-05-23
title: 延迟折扣（Delay Discounting）
sourceIds:
  - source.跨期选择的年龄差异_文献综述_v3
aliases:
  - 时间折扣
  - Temporal Discounting
---

# 延迟折扣（Delay Discounting）

> 个体对未来收益价值的主观贬低程度，即随延迟时间增加主观价值逐渐下降的过程

---

## 一、概念定义

**核心定义**：延迟折扣指个体对未来收益价值的主观贬低程度，即相同收益的主观价值随延迟时间的增加而下降的过程。

**核心构念**：折扣率（k值）——k值越大表示折扣越陡峭，即更偏好即时收益。

**概念辨析**：
- 延迟折扣 vs. 概率折扣：前者时间维度，后者概率维度
- 延迟折扣 vs. 风险偏好：前者涉及时间不确定性，后者涉及结果不确定性
- 延迟折扣 vs. 延迟满足：延迟满足是行为表现，延迟折扣是认知机制

---

## 二、操作性定义

### 2.1 行为测量范式

| 范式 | 操作定义 | 代表研究 |
|------|----------|----------|
| **调整金额程序** | 固定延迟，迭代调整确定即时vs.延迟金额无差异点 | Du et al., 2002 |
| **货币选择问卷(MCQ)** | 27道选择题，计算AUC值 | Kirby et al., 1999 |
| **估计时间程序(ITP)** | 估计不同延迟对应的即时等值金额 | Green & Myerson, 2004 |

### 2.2 数学模型

**指数折扣模型**（Samuelson, 1937）：
$$V = A \cdot e^{-kD}$$

**双曲线模型**（Mazur, 1987）：
$$V = A / (1 + kD)$$

**双曲线模型(hyperboloid)**（Green & Myerson, 1995）：
$$V = A / (1 + kD)^s$$

### 2.3 指标计算

**曲线下面积（AUC）法**（Myerson et al., 2001）：
$$AUC = \frac{1}{n-1} \sum_{i=1}^{n-1} \frac{V_i + V_{i+1}}{2}(t_{i+1} - t_i)$$

- 不依赖特定模型假设
- log(k)更符合正态分布

---

## 三、核心特点

| 特点 | 描述 |
|------|------|
| **非线性折扣** | 折扣率随延迟时间递减（非指数模型的恒定比率） |
| **金额效应** | 大额奖励的折扣率低于小额奖励（s < 1） |
| **符号效应** | 延迟损失的折扣率低于延迟收益 |
| **个体差异大** | k值可跨越3个数量级 |
| **可训练性** | 可通过冥想、正念等干预降低 |

---

## 四、理论解释

### 4.1 双曲线折扣模型
**Green & Myerson (1995)**

核心机制：双曲线形状产生时间不一致性——相同延迟在不同时间点对效用的影响不同。

适用性：解释"今天vs.明天"选择悖论。

### 4.2 指数折扣模型
**Samuelson (1937)**

核心机制：假设个体以恒定比率对未来收益折扣。

局限性：无法解释时间不一致性，已被双曲线模型取代。

### 4.3 自我控制理论

核心机制：延迟折扣是自我控制失败的核心机制；高折扣率者难以抵制即时诱惑。

适用性：解释成瘾、肥胖等自我控制失败行为。

### 4.4 神经积分模型
**McClure et al. (2004)**

核心机制：延迟折扣涉及"冷"认知系统（前额叶）和"热"情绪系统（边缘系统）的竞争。

---

## 五、边界条件

| 边界条件 | 调节方向 | 具体发现 | 效应量 | 研究 |
|----------|----------|----------|--------|------|
| 年龄 | 非线性 | U型关系，中年人折扣率最低 | r=-0.068 | Seaman et al., 2022 |
| 收入水平 | 缓冲 | 高收入缓冲年龄对折扣率的负向效应 | 交互 | Wan et al., 2024 |
| 执行功能 | 负向调节 | 高执行功能→低折扣率 | β=-0.35 | Shamosh et al., 2008 |
| 人格(冲动性) | 正向调节 | 高冲动性→高折扣率 | r=0.45 | 【未检索确认】 |
| 情绪状态 | 正向调节 | 焦虑增加折扣率 | d=0.45 | Story et al., 2013 |
| 物质使用 | 正向调节 | 物质成瘾者折扣率更高 | d=0.8 | Bickel et al., 2015 |

---

## 六、影响因素

| 前因变量 | 效应方向 | 效应量 | 代表研究 |
|----------|----------|--------|----------|
| 执行功能 | 负向 | β=-0.35 | Shamosh et al., 2008 |
| 自我控制 | 负向 | r=-0.30 | Kirby et al., 1999 |
| 冲动性 | 正向 | r=0.45 | 【未检索确认】 |
| 主观时间流逝速度 | 正向 | r=0.40 | Takahashi, 2013 |
| 自我连续性 | 负向 | - | Lu & Löckenhoff, 2024 |
| 焦虑/压力 | 正向 | d=0.45 | Story et al., 2013 |

---

## 七、后效结果

| 后果变量 | 效应方向 | 效应量 | 代表研究 |
|----------|----------|--------|----------|
| 物质成瘾 | 正向 | OR=2.3 | Bickel et al., 2015 |
| 酒精依赖 | 正向 | d=0.6 | 【未检索确认】 |
| 肥胖/不健康饮食 | 正向 | r=0.25 | Weller et al., 2008 |
| 病理性赌博 | 正向 | - | MacKillop et al., 2011 |
| 学业拖延 | 正向 | r=0.36 | Steel, 2007 |
| 退休储蓄不足 | 正向 | - | da Silva et al., 2016 |
| HIV风险行为 | 正向 | - | 【未检索确认】 |

---

## 八、核心文献

| 文献 | 核心贡献 |
|------|----------|
| Samuelson (1937) | 指数折扣模型 |
| Mazur (1987) | 双曲线折扣模型 |
| Green & Myerson (1995) | 双曲线模型(hyperboloid)，尺度参数s |
| Kirby et al. (1999) | MCQ问卷开发 |
| Myerson et al. (2001) | AUC测量方法 |
| McClure et al. (2004) | 神经积分模型："冷""热"系统 |
| Bickel et al. (2015) | 延迟折扣与成瘾行为系统综述 |

---

## 九、相关概念

- [[concepts/intertemporal-choice]]（跨期选择）- 上位概念
- [[concepts/self-control]]（自我控制）- 前因/机制
- [[concepts/impulsivity]]（冲动性）- 人格边界条件
- [[concepts/time-perception]]（时间感知）- 前因

---

*最后更新：2026-05-23*
*更新者：心理学家（psychologist）*

## Related
<!-- openclaw:wiki:related:start -->
### Referenced By

- [[concepts/academic-procrastination|学业拖延（Academic Procrastination）]]
- [[concepts/socioemotional-selectivity-theory|社会情绪选择理论（Socioemotional Selectivity Theory）]]
- [[concepts/buffering-hypothesis|缓冲假设（Buffering Hypothesis）]]
- [[concepts/self-control|自我控制（Self-Control）]]
- [[concepts/self-continuity|自我连续性（Self-Continuity）]]
- [[concepts/intertemporal-choice|跨期选择（Intertemporal Choice）]]
<!-- openclaw:wiki:related:end -->
