---
pageType: source
id: source.cct-al-kari-2026
createdAt: "2026-06-05T15:40:00+08:00"
updatedAt: "2026-06-21T21:27:38"
title: 范畴论结构先验可在 306M 规模上压低 WikiText-103 困惑度（GT-Full 单独贡献 84%）
sourceIds:
  - raw/papers/2026-05-31_Al-Kari_Cognitive-Categorical-Transformer_arXiv.pdf
zotero_item_key: JBGDN6ZI
zotero_doi: 10.48550/arXiv.2605.28864
aliases:
  - CCT
  - Cognitive Categorical Transformer
  - Al Kari 2026
---

# 范畴论结构先验可在 306M 规模上压低 WikiText-103 困惑度（GT-Full 单独贡献 84%）

> **来源**：`[[raw/papers/2026-05-31_Al-Kari_Cognitive-Categorical-Transformer_arXiv.pdf]]`
> **作者**：Al Kari（Manceps Inc.，单人作者）
> **年份**：2026（arXiv:2605.28864v1，2026-05-22 发布）
> **类型**：paper
> **状态**：confirmed（已通读并整理笔记）

## 一句话总结

CCT（306M）在 WikiText-103 上比微调基线低 **2.92 PPL**（12% 相对），其中 **84% 来自 GT-Full 单纯形消息传递**——这是首个"消融-验证"证据：范畴论提供的**结构通路**确实改善语言建模，而**一致性约束**（sheaf/adjunction/curvature）无效。

## 关键内容

- **方法论**：matched-step 协议——架构与基线共享 backbone 初始化、语料、优化器、步数预算、学习率调度，**唯一差异**是架构增强（这是消融可信度的关键）
- **GT-Full 贡献**：从头重训练消融中，**84% 架构改善（2.45/2.92 PPL）**来自 GT-Full 单纯形消息传递（k-NN 图 + 三角形识别 + 边/三角消息传递 + 门控融合）
- **结构 vs 一致性区分**（最可泛化的概念贡献）：
  - **结构先验**（引入新拓扑/新消息传递通路）→ ✅ 有效（GT-Full +2.45 PPL）
  - **一致性先验**（损失项强制恒等式）→ ❌ 无效或有害（48 组超参搜索）
  - 理论解释：前馈 ReLU 网络前向传播已是 sheaf 上的调和扩展（Bosca & Ghrist 2026），加一致性损失在数学上**冗余**且与交叉熵目标**梯度冲突**
- **PP 条件依赖**：PrecisionWeightedPP 在 RC2 贡献 1.40 PPL，在 E2（无 GT-Full）只贡献 0.07 PPL——**PP 信号依赖 GT-Full 的稀疏化高阶特征**
- **工程实非数学逆**：Vec→K（k-NN 发现拓扑）+ K→Vec（消息传递计算表征），前者是经验构造，后者是函子；**不是求逆函子**，更接近**余极限构造**

## 影响到的页面

- `[[syntheses/2026-05-31-11-00-00-CCT-论文笔记.md]]`——主笔记，最详细的阅读材料
- `[[syntheses/2026-05-31-11-30-00-复形vs流形-关系描述的数学对比.md]]`——复形本体论的第一手数学来源
- `[[syntheses/2026-05-31-12-22-00-认知过程的对称性破缺机制-理论框架.md]]`——余代数与对称性破缺理论的工程来源
- `[[concepts/inductive_bias]]`（如未来建）——结构先验 vs 一致性先验的新案例
- `[[concepts/范畴论]]`（如未来建）——单纯形复型/层/余代数/Yoneda 的应用样例

## 待确认

- [ ] **单种子问题**：实验仅 seed=42，84%/2.45 PPL 这个核心数字需多种子复现
- [ ] **下游任务未重训**：ARC-Easy/HellaSwag 等仅在 RC2 checkpoint 测过，未做头训练对照
- [ ] **非 GT-Full 组件未单独消融**：合计仅 0.47 PPL，可能有负贡献组件被掩盖
- [ ] **代码未公开**：架构细节（k=6、三角形稀疏加速 2500×、DNC 三层容量）无法独立验证
- [ ] **PP 条件依赖的因果性**：观察是相关性，PP 是否需要 GT-Full 的特定输出分布还是任何结构化输入均可，尚无消融
- [ ] **Matched-step 协议是否在所有比较中都严格**：E1（微调基线）和 RC2 共享 GPT-2 Small 初始化，但 RC2 多 182M 参数——能否在参数预算固定下也算"matched"？

## 关联的 raw 文件

- `[[raw/papers/2026-05-31_Al-Kari_Cognitive-Categorical-Transformer_arXiv.pdf]]`

## Related
<!-- openclaw:wiki:related:start -->
### Referenced By

- [[syntheses/2026-05-31-11-00-00-CCT-论文笔记|The Cognitive Categorical Transformer (CCT) - 论文笔记]]
<!-- openclaw:wiki:related:end -->
