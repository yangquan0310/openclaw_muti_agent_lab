---
pageType: concept
id: concept.inductive-bias
createdAt: 2026-06-27
updatedAt: 2026-06-27
title: 归纳偏置（Inductive Bias）
sourceIds: ["placeholder"]  # TODO: 引用真实 source
aliases:
  - 归纳偏置
  - Inductive Bias
  - inductive_bias
---

# 归纳偏置（Inductive Bias）

> 机器学习模型从有限训练数据泛化到未见数据时所做的先验假设

---

## 一、概念定义

**核心定义**：归纳偏置（Inductive Bias）指学习算法在从有限样本泛化到新样本时所做的先验假设集合。这些假设让模型在没有见过的数据上能做出合理预测，但同时限制了模型能学习的函数族。

**关键构念**：
- 先验假设：模型架构、内置的等变性/不变性
- 泛化能力：在分布外数据上的表现
- 偏差-方差权衡：过强 → 欠拟合，过弱 → 过拟合

---

## 二、常见归纳偏置类型

| 类型 | 描述 | 例子 |
|------|------|------|
| **平滑性偏置** | 相近输入应有相近输出 | 大多数监督学习 |
| **平移不变性** | 模式识别不依赖位置 | CNN |
| **局部性** | 相近 token 关系更强 | Transformer attention |
| **层次性** | 概念可分解为子概念 | 深度网络、单纯形 |
| **稀疏性** | 多数特征不相关 | L1 正则 |
| **对称性** | 等变变换保持结果关系 | GNN、群等变网络 |
| **范畴论结构** | 复合关系满足结合律/单位元 | CCT（Al-Kari 2025） |

---

## 三、归纳偏置的心理学对应

| ML 概念 | 心理学对应 | 关联 |
|---------|-----------|------|
| 归纳偏置 | 认知图式（schema） | 两者都是先验结构 |
| 偏差-方差权衡 | 自动化 vs. 受控加工 | Stanovich 双系统 |
| 平滑性 | 连续性启发式 | Tversky & Kahneman |
| 稀疏性 | 选择性注意 | Broadbent 过滤器模型 |

---

## 四、与现有概念的关系

| 关系类型 | 现有概念 | 关联说明 |
|---------|---------|---------|
| **应用** | [[concepts/simplicial-message-passing|单纯形消息传递]] | 单纯形结构作为归纳偏置 |
| **应用** | [[concepts/范畴论|范畴论]] | 范畴结构作为先验 |

---

## 五、核心文献

| 文献 | 核心贡献 |
|------|---------|
| Mitchell (1980) | 归纳偏置形式化 |
| Al-Kari et al. (2025) | 范畴论结构先验（CCT）压低 PPL |
| Battaglia et al. (2018) | 关系归纳偏置综述 |

---

*最后更新：2026-06-27*
*更新者：心理学家（psychologist）*
*创建原因：被 [[sources/2026-05-31_Al-Kari_Cognitive-Categorical-Transformer_arXiv]] 等多个页面引用*

## Related
<!-- openclaw:wiki:related:start -->
### Referenced By

- [[syntheses/2026-05-31-11-00-00-CCT-论文笔记|The Cognitive Categorical Transformer (CCT) - 论文笔记]]
- [[concepts/simplicial-message-passing|单纯形消息传递（Simplicial Message Passing）]]
- [[syntheses/2026-05-31-11-30-00-复形vs流形-关系描述的数学对比|复形 vs 流形：关系描述的数学对比]]
- [[concepts/结构先验 vs 一致性先验|结构先验 vs 一致性先验（Structural Prior vs Consistency Prior）]]
- [[sources/2026-05-31_Al-Kari_Cognitive-Categorical-Transformer_arXiv|范畴论结构先验可在 306M 规模上压低 WikiText-103 困惑度（GT-Full 单独贡献 84%）]]
<!-- openclaw:wiki:related:end -->
