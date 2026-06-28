---
pageType: concept
id: concept.结构先验-vs-一致性先验
createdAt: 2026-06-27
updatedAt: 2026-06-27
title: 结构先验 vs 一致性先验（Structural Prior vs Consistency Prior）
sourceIds:
  - source.2026-05-31_Al-Kari_Cognitive-Categorical-Transformer_arXiv
aliases:
  - 结构先验
  - 一致性先验
  - Structural vs Consistency Prior
---

# 结构先验 vs 一致性先验（Structural Prior vs Consistency Prior）

> 两种不同的归纳偏置哲学：结构的丰富性 vs 约束的一致性

---

## 一、概念辨析

| 维度 | 结构先验（Structural Prior）| 一致性先验（Consistency Prior）|
|------|------------------------|--------------------------|
| **核心** | 假设数据有丰富的结构（拓扑、范畴论）| 假设变换下结果保持一致（等变性）|
| **来源** | 拓扑学、范畴论、群论 | 几何学、物理对称性 |
| **实现** | 单纯形、范畴、复合 | 等变网络、对称群 |
| **优势** | 表达力强，能编码复杂关系 | 泛化稳定，物理可信 |
| **代价** | 计算成本高 | 表达力受限于群结构 |

---

## 二、典型实现

| 类型 | 代表方法 | 来源 |
|------|---------|------|
| **结构先验** | 单纯形 GNN、范畴论模型、拓扑深度学习 | Al-Kari 2025 (CCT) |
| **一致性先验** | E(3)-等变网络、群等变 CNN | Weiler & Cesa (2019) |
| **混合** | 等变单纯形网络 | Bodnar et al. |

---

## 三、Al-Kari 2025 (CCT) 的核心贡献

| 概念 | CCT 中的应用 |
|------|------------|
| **结构先验** | 范畴论结构（结合律、单位元、复合）压低 WikiText-103 PPL |
| **一致性先验** | （论文中未显式使用，但讨论了"结构 vs 一致"权衡）|
| **核心论点** | 单纯形消息传递 + 范畴论结构 > 单一归纳偏置 |

---

## 四、哲学含义

```
结构先验：世界是层次化的（layered）——信息在不同抽象层
一致性先验：世界是对称的（symmetric）——变换保持本质
```

这是两种**互补的归纳偏置哲学**：
- 结构 = 强调**多样性和复杂性**
- 一致性 = 强调**统一性和稳定性**

**老板研究主轴的连接**：心理学中"建构主义 vs 行为主义"对应类似的张力——建构主义强调认知结构（schema），行为主义强调刺激-反应的一致性。

---

## 五、与现有概念的关系

| 关系类型 | 现有概念 | 关联说明 |
|---------|---------|---------|
| **关联** | [[concepts/inductive-bias|归纳偏置]] | 两种先验都是归纳偏置 |
| **关联** | [[concepts/simplicial-message-passing|单纯形消息传递]] | 结构先验的具体实现 |
| **关联** | [[concepts/范畴论|范畴论]] | 范畴论提供结构先验的语言 |

---

## 六、核心文献

| 文献 | 核心贡献 |
|------|---------|
| Al-Kari et al. (2025) arXiv | 范畴论结构先验的 LM 应用 |
| Weiler & Cesa (2019) | 等变 CNN 综述（一致性先验）|
| Bodnar et al. (2021) | 单纯形神经网络 |

---

*最后更新：2026-06-27*
*更新者：心理学家（psychologist）*
*创建原因：被 [[syntheses/2026-05-31-11-00-00-CCT-论文笔记]] 和 [[syntheses/2026-05-31-11-30-00-复形vs流形-关系描述的数学对比]] 引用*

## Related
<!-- openclaw:wiki:related:start -->
### Referenced By

- [[syntheses/2026-05-31-11-00-00-CCT-论文笔记|The Cognitive Categorical Transformer (CCT) - 论文笔记]]
- [[concepts/simplicial-message-passing|单纯形消息传递（Simplicial Message Passing）]]
- [[syntheses/2026-05-31-11-30-00-复形vs流形-关系描述的数学对比|复形 vs 流形：关系描述的数学对比]]
<!-- openclaw:wiki:related:end -->
