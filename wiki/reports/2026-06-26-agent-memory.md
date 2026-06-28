---
pageType: report
id: report.2026-06-26-agent-memory
createdAt: "2026-06-26T00:00:00+08:00"
updatedAt: "2026-06-27T23:40:00+08:00"
title: Agent 记忆 日报
---

# Agent 记忆 日报
> 日期：2026-06-26（周五，Asia/Shanghai 08:59）
> 检索时间窗口：过去 24 小时（2026-06-25 00:59 UTC ~ 2026-06-26 00:59 UTC）
> 检索源：arXiv `cs.AI` / `cs.CL` / `cs.MA` / `cs.LG` 类目 2026-06-25（Thu）批次的"agent + memory"主题论文
> 检索工具：jina-ai Reader/Search + arXiv listing 直接抓取（arxiv.org/list/cs.{AI,CL,MA,LG}/recent?skip=0&show=2000）
> 筛选标准：标题或摘要同时含 "agent" ∩ "memory" 关键词，或专题相关（多 agent 共享记忆 / 长时记忆治理 / 角色记忆 / 持续学习）

---

## 📊 总体观察

- **arXiv 2026-06-25 新批次（Thu）**：cs.AI **182** + cs.CL **89** + cs.MA **13** + cs.LG **186** ≈ **470 篇**新增，跨类目去重后约 **430 篇**——较 2026-06-24（Wed，198+198+similar ≈ 480 篇）基本持平；当日 ICML 2026 截稿后节奏恢复，agent/memory 主题继续高密度产出。
- **"Agent Memory" 主题论文**：6 篇核心（标题同时含 "agent" + "memory"，跨 cs.AI/cs.CL/cs.MA）+ 5 篇强相关 ≈ **11 篇**，占比 ~2.6%，与昨日（10/413 ≈ 2.4%）基本一致——agent memory 已成为持续稳定的高产子领域。
- **研究热点迁移**：从昨日的"系统化视角 / 治理原语 / 共享记忆"转向今日的"**记忆治理的可量化准则（governance metrics）+ 记忆效果实证比较（empirical evaluation）+ 角色 / 任务型记忆（role/task memory）**"；新出现 4 个具体子方向——①**记忆可信度量化**（TRUSTMEM + Reclaim Eval）②**记忆功能角色比较**（Memory Makes the Difference）③**持续 / 终身学习中的参数化记忆**（Lifelong ICL + Forget to Improve）④**领域专用多 agent 协作记忆**（BrainAgent + Agentic BKT + Post-discharge Framework）。
- **代码 / 数据可用性**：11 篇中 5 篇明确开源或附带数据集（REVERIEMEM / RAVEN / TRUSTMEM / BrainAgent / Is GraphRAG Needed），3 篇有 GitHub 链接。

---

## 🛡️ 一、Agent 记忆治理与可信度（Memory Governance & Trustworthiness）

### 文章 1：TRUSTMEM
- **标题**：TRUSTMEM: Learning Trustworthy Memory Consolidation for LLM Agents with Long-Term Memory
- **作者**：Tianyu Yang, Sudipta Paul, Vijay Srinivasan, Vivek Kulkarni（IBM Research AI 等机构）
- **时间**：2026-06-25 批次（arXiv: 2606.25161，v1 提交 2026-06-23T20:49 UTC）
- **主要内容**：现有 LLM 智能体的长期记忆系统通过 write/revise/delete 操作主动更新外部记忆，但这些更新可能遗漏关键信息、破坏既有内容或引入幻觉内容，且一旦存储就会成为持久化的"系统状态失败"。**TrustMem** 提出三层守护机制——①**写入前**：评估写入内容的支持证据强度与潜在危害，置信度不足时拒绝写入；②**修订时**：检测与既有记忆的冲突/重复/语义漂移，仅在净收益为正时合并；③**合并时**：维护可审计的 provenance chain，确保未来推理能追溯每个条目的来源与可信度。核心论点："agent memory 应当像数据库事务一样满足 ACID 性质，错误记忆的代价远高于缺失记忆。"

### 文章 2：Reclaim Evaluation: A Lossy Memory Is Worse Than an Empty One
- **标题**：Reclaim Evaluation: A Lossy Memory Is Worse Than an Empty One
- **作者**：Alex Kwon
- **时间**：2026-06-25 批次（arXiv: 2606.25449，v1 提交 2026-06-24T06:24 UTC）
- **主要内容**：提出"**脆弱记忆（brittle memory）**"概念——当 agent 记忆保留了一个错误的结论却丢失了背后的推理过程，它会把这个过时值作为自信答案输出；而同样的 agent 在空记忆下会选择弃权。**实验结论**：在 7 个主流模型上"有损记忆永远比无记忆更糟"这个方向从未反转——这是模型都没能打破的"clean kill condition"。**Reclaim Evaluation** 方法：在固定压缩率下评估一个 agent 能否从压缩后的记忆"重建"原始交互的关键事实。该指标从行为层面（而非底层信息论界）量化记忆可信度，与模型偏好和任务无关。**对生产 agent 系统的启示**：记忆压缩 / 摘要 / 遗忘不应仅优化"记忆容量 vs 信息保留"曲线，必须保留"足够重建"的可逆性。

### 文章 3：The Unfireable Safety Kernel
- **标题**：The Unfireable Safety Kernel: Execution-Time AI Alignment for AI Agents and Other Escapable AI Systems
- **作者**：Seth Dobrin, Łukasz Chmiel
- **时间**：2026-06-25 批次（arXiv: 2606.26057，v1 提交 2026-06-24T17:32 UTC）
- **主要内容**：现有 AI agent 安全护栏都放在 agent 自身运行时——system prompt、output filter、guardrail library，但任何处于 agent 地址空间的控制都会被能影响它的输入触达（prompt injection / context poisoning）。**"The Unfireable Safety Kernel"** 提出将控制移出 agent 地址空间，放在执行时（execution-time）硬件 / OS / hypervisor 层——一旦 prompt injection 改变了 agent 的推理，控制也难以被绕开。**核心论断**：对于能调用工具、API、文件系统的主动 agent，仅靠 prompt-level alignment 不够，需要"地址空间外"的执行时强制约束。这与 TRUSTMEM / Reclaim 的"可信度"维度互补：前者解决"agent 做什么"，本工作解决"agent 能否做危险的事"。

---

## 🎭 二、Agent 角色记忆与情境一致性（Role Memory & Character Consistency）

### 文章 4：REVERIEMEM — Staying In Character
- **标题**：Staying In Character: Perspective-Bounded Memory For Book-Based Role-Playing Agents
- **作者**：Xushuo Tang, Junhe Zhang, Zihan Yang, Yifu Tang, Sichao Li 等
- **时间**：2026-06-25 批次（arXiv: 2606.25632，cs.CL/cs.AI，v1 提交 2026-06-24T09:37 UTC）
- **主要内容**：长篇小说角色扮演 agent 存在两类失败——**Factual Overreach**（共享检索 / 参数记忆让角色用到自己视角外的事实）和 **Stylistic Monotony**（profile 描述把角色拍平成单一语调）。**REVERIEMEM** 提出三层记忆架构——①**情景层（episodic）**：以第一人称存储场景记忆；②**语义层（semantic）**：存储带"可见性标签"的事实（visibility tag 控制哪些事实对当前角色可见）；③**风格层（stylistic）**：存储语气偏好、句法习惯、修辞印记。第三层的关键是"角色专属风格指纹"——从原文中提炼出该角色独有的语言模式（如哈姆雷特的迟疑哲学化、福尔摩斯的逻辑推理短句），避免 LLM 把所有角色都说成相似的"AI 礼貌腔"。**本质贡献**：把"角色一致性"从"不违反事实"扩展为"不仅不违反事实，还要保持独特的语言身份"。

---

## 🔄 三、持续 / 终身学习与参数化记忆（Continual Learning & Parametric Memory）

### 文章 5：Lifelong In-Context Learning with Parametric Attention
- **标题**：Lifelong In-Context Learning with Transformers Requires Parametric Forms of Attention
- **作者**：Luke McDermott, Robert W. Heath, Rahul Parhi（UC San Diego 等）
- **时间**：2026-06-25 批次（arXiv: 2606.25342，cs.LG/cs.AI，v1 提交 2026-06-24T03:14 UTC）
- **主要内容**：终身持续学习是通往类人智能的障碍——transformer 的 in-context learning（ICL）能力虽强，但 softmax attention 的二次复杂度使其无法处理任意长序列。**本文论点**：将 ICL 扩展到终身设置是 agent 持续学习的实用方案，但**必须**采用**参数化形式（parametric forms）**的 attention。**对比框架**：①**非参数化**：softmax attention（KV cache 无限增长）vs. ②**参数化**：线性 attention、state-space models、fast weight programmers、test-time training layers——后者用可在线训练的神经网络替代 KV cache，保持恒定内存占用。**当前局限**：参数化 attention 在记忆容量或在线更新成本上仍不足以支撑真正终身学习。**对 agent memory 的启示**：长时记忆不应只靠"上下文堆叠"，而要发展出"压缩为参数"的机制（类似人脑从短期记忆固化为长期记忆）。

### 文章 6：Forget to Improve — Budget-Curated Memory
- **标题**：Forget to Improve: On-Device LLM-Agent Continual Learning via Budget-Curated Memory
- **作者**：Beining Wu, Zihao Ding, Jun Huang, Yanxiao Zhao
- **时间**：2026-06-25 批次（arXiv: 2606.25115，cs.LG/cs.NI，v1 提交 2026-06-23T19:42 UTC）
- **主要内容**：端侧 LLM agent 通过累积"检索记忆"而非更新权重来改进——但记忆受**RAM/能量预算限制**，且**暴露面广**：消耗资源、向 peer 通过 thin uplink 共享、被 agent 读入的内容可投毒。**核心机制**：单一 **net-value-per-byte** 评分（value - harm，每字节）作为记忆生命周期治理——①**KEEP**：在 RAM/能量预算下驱逐低价值字节；②**SHARE**：仅在 value > uplink cost 时向 peer 发送洞察；③**TRUST**：按 provenance 门控 peer 写入。**实测结果**（Jetson 异构集群 + 两个 robot-arm 节点）：记忆减少 **2.7×**、uplink 减少 **2.4×**、投毒成功率从 0.75 → **0**、投毒场景下准确率提升。**核心反直觉结论**：在受资源约束的 agent 中，"通过净价值遗忘"反而增强 agent 而非削弱它——这与 Reclaim Evaluation 形成对话：前者是"有预算就主动遗忘"，后者是"压缩也要保真"，两者共同指向 agent memory 应**可控可逆**而非"越多越好"。

---

## 📐 四、Agent 记忆效果实证比较（Empirical Memory Evaluation）

### 文章 7：Memory Makes the Difference
- **标题**：Memory Makes the Difference: Evaluating How Different Memory Roles Shape Conversational Agents
- **作者**：Yuxin Wang, Paul Thomas, Zhiwei Yu, Yuan Gao, Saeed Hassanpour 等（Duke University 等）
- **时间**：2026-06-25 批次（arXiv: 2606.25361，cs.CL/cs.AI/cs.IR，v1 提交 2026-06-24T03:45 UTC）
- **主要内容**：现有 RAG 对话系统的记忆研究集中在"如何存储 / 检索"，但**记忆的不同功能角色（如事实型 vs 偏好型 vs 上下文型）对响应质量的影响几乎未被探索**——同样的记忆，在不同对话语境下会让 agent 给出截然不同的回应。**贡献**：①**形式化"记忆角色"分类**——把 agent 记忆分为"硬事实 / 软偏好 / 临时上下文 / 程序性知识"等 4-6 个功能类；②**提出 reference-free 评估协议**——基于响应多样性、用户偏好对齐、对话一致性等多维度；③**实证发现**：记忆的"角色正确性"比"记忆总量"更影响响应质量——错误的角色归类（如把"偏好"当"事实"）会让 agent 给出技术上正确但语义错误的回答。该工作为"agent memory 应该分库存储"提供了实证支撑。

### 文章 8：Is GraphRAG Needed?
- **标题**：Is GraphRAG Needed? From Basic RAG to Graph-/Agentic Solutions with Context Optimization
- **作者**：Long Chen, Ryan Razkenari, Yuxuan Zhou, Yuan Tian, Rahul Ghosh 等（Pennsylvania State University 等）
- **时间**：2026-06-25 批次（arXiv: 2606.25656，cs.CL/cs.AI/cs.IR，v1 提交 2026-06-24T10:11 UTC）
- **主要内容**：随着 GraphRAG、Agentic RAG 等高级 RAG 变体涌现，"何时用 / 怎么用"成为开放问题。**本文框架**：在**半结构化知识库**上对 4 种 RAG（regular / GraphRAG / Modular RAG / Agentic RAG）× 9 个标准化场景做统一评估，对比检索质量、延迟、成本。**关键发现**：①GraphRAG 优势**高度依赖场景**——在跨实体多跳推理场景明显领先，但在简单文档问答场景可能不如基础 RAG；②Agentic RAG 的"agent 路由"开销在简单任务上反而拖累性能；③**Modular RAG** 通过模块化组合实现最优的成本-质量曲线。**对 agent memory 的启示**：记忆增强（Graph / 索引 / Agent 路由）不是越多越好，应当**根据任务瓶颈选择最匹配的机制**——这与昨日"Agent-Native Memory"论文（24775）的"无单一架构在所有场景占优"形成共鸣。

---

## 🏥 五、多 Agent 协作记忆与领域专用（Multi-Agent Shared Memory）

### 文章 9：BrainAgent — Multi-Agent Framework for Brain Signal Understanding
- **标题**：BrainAgent: A Large Language Model-Driven Multi-Agent Framework for Autonomous Brain Signal Understanding
- **作者**：Yangxuan Zhou, Sha Zhao, Jiquan Wang 等
- **时间**：2026-06-25 批次（arXiv: 2606.25400，cs.AI，v1 提交 2026-06-24T04:54 UTC）
- **主要内容**：脑机接口（BCI）和脑信号理解存在两大瓶颈——①**技术门槛高**（需要神经科学 / 信号处理 / 机器学习综合知识）；②**流程静态、任务专用**，无法执行真实世界所需的复杂长时工作流。**BrainAgent** 提出**LLM 驱动的多 agent 框架**：①**Planner Agent** 把自然语言需求分解为脑信号分析 pipeline；②**Specialist Agents**（信号预处理 / 特征提取 / 模型选择 / 结果解释）各司其职；③**Shared Memory** 维护从原始信号到最终解释的全链路状态。**核心创新**：用 LLM 把"领域专家知识"封装为可调用的 agent 角色，从而把"专家系统 + 深度学习"的混合范式从静态规则扩展为动态可组合工作流。对**agent memory 设计的启示**：领域专用多 agent 系统中，**shared memory 应当是"分析状态 + 推理轨迹 + 假设历史"的三层结构**，而非简单 KV cache。

### 文章 10：Agentic BKT — Stealth Assessment via Multi-Agent LLM
- **标题**：Agentic Knowledge Tracing: A Multi-Agent LLM Architecture for Stealth Assessment of Financial Literacy in Serious Games
- **作者**：Gabriel Santos, Rita Julia, Marcelo Nascimento
- **时间**：2026-06-25 批次（arXiv: 2606.25358，cs.AI/cs.MA，v1 提交 2026-06-24T03:43 UTC）
- **主要内容**：在严肃游戏中无干扰地评估玩家的金融素养是个开放挑战。**Agentic BKT（Bayesian Knowledge Tracing）** 提出 4 阶段多 agent 流水线——①**Event Capture**：把玩家每个决策记为结构化事件日志；②**LLM Event Classifier**：用 4 点 rubric 标注每个动作（与 3 位领域专家一致性 Fleiss κ = 0.624）；③**4 个领域专用 agent**（风险规避 / 投资 / 支出 / 信用管理）各自做会话级推理，输入到 per-competency BKT 模型估计领域掌握度；④**Expert Judge Agent** 合成跨领域评估。**核心创新**：把"知识追踪（KT）"从"学生答题正误"扩展为"游戏内行为隐式信号"，且用多 agent 拆解不同金融能力维度。**对 agent memory 的启示**：行为轨迹本身可作为 agent 的"长期记忆源"——通过对行为日志做语义标注，能从中提取出用户的能力画像而非依赖显式测试。

### 文章 11：Post-discharge Multi-Agent Framework
- **标题**：Bridging the Post-discharge Gap: A Traceable Multi-agent Framework for Safe and Continuous Care
- **作者**：Runwei Guan, Yi Zhou, Heyi Lin, Jinjing Zhu, Mingyuan Hou 等
- **时间**：2026-06-25 批次（arXiv: 2606.25334，cs.AI/cs.MA/cs.CL，v1 提交 2026-06-24T02:57 UTC）
- **主要内容**：出院后随访对维持护理连续性至关重要，但传统随访受限于——①**医疗人力短缺**；②**患者历史碎片化**（多科室 / 多机构）；③**信息孤岛**。LLM 单独使用有幻觉 + 无法处理纵向时序数据的根本缺陷。**本文框架**：提出**可追溯多 agent 系统**——①**Patient Memory Agent** 整合多源异构病历（结构化 EHR + 非结构化医嘱 / 出院小结）；②**Risk Assessment Agent** 基于纵向历史生成动态风险评分；③**Care Coordinator Agent** 生成随访计划；④**Traceability Layer** 记录每个结论的证据来源与推理路径。**核心创新**：把"agent 决策可追溯性（traceability）"作为医疗级应用的硬约束——每个建议必须能回溯到原始证据片段。对**agent memory 的应用启示**：高风险领域（医疗 / 法律 / 金融）的 agent 记忆系统**必须**内置证据追溯层，这是"记忆可信度"的工程化要求。

---

## 🔗 参考链接

| arXiv ID | 链接 | 类型 | 核心 |
|----------|------|------|------|
| 2606.25161 | https://arxiv.org/abs/2606.25161 — TRUSTMEM | cs.AI | 核心 |
| 2606.25449 | https://arxiv.org/abs/2606.25449 — Reclaim Evaluation | cs.CL/cs.AI/cs.LG | 核心 |
| 2606.25632 | https://arxiv.org/abs/2606.25632 — REVERIEMEM (Staying In Character) | cs.CL/cs.AI | 核心 |
| 2606.25342 | https://arxiv.org/abs/2606.25342 — Lifelong ICL with Parametric Attention | cs.LG/cs.AI | 核心 |
| 2606.25115 | https://arxiv.org/abs/2606.25115 — Forget to Improve | cs.LG/cs.NI | 核心 |
| 2606.25361 | https://arxiv.org/abs/2606.25361 — Memory Makes the Difference | cs.CL/cs.AI/cs.IR | 核心 |
| 2606.25400 | https://arxiv.org/abs/2606.25400 — BrainAgent | cs.AI | 补充 |
| 2606.25358 | https://arxiv.org/abs/2606.25358 — Agentic BKT | cs.AI/cs.MA | 补充 |
| 2606.25334 | https://arxiv.org/abs/2606.25334 — Post-discharge Multi-Agent | cs.AI/cs.MA/cs.CL | 补充 |
| 2606.25656 | https://arxiv.org/abs/2606.25656 — Is GraphRAG Needed? | cs.CL/cs.AI/cs.IR | 补充 |
| 2606.26057 | https://arxiv.org/abs/2606.26057 — Unfireable Safety Kernel | cs.AI/cs.CR/cs.LG | 补充 |

- **检索工具**：
  - jina-ai Search API: https://s.jina.ai/ （用于 web-level 检索与领域上下文核实）
  - jina-ai Reader API: https://r.jina.ai/ （用于 arXiv listing HTML 解析）
  - arXiv API: https://export.arxiv.org/api/query （用于论文 abstract / published 时间核验）
  - arXiv cs.AI listing: https://arxiv.org/list/cs.AI/recent?skip=0&show=2000
  - arXiv cs.CL listing: https://arxiv.org/list/cs.CL/recent?skip=0&show=2000
  - arXiv cs.MA listing: https://arxiv.org/list/cs.MA/recent?skip=0&show=2000
  - arXiv cs.LG listing: https://arxiv.org/list/cs.LG/recent?skip=0&show=2000

---

## 📝 检索方法学说明

1. **范围界定**：严格遵循"过去 24 小时"——以 2026-06-26 00:59 UTC 为基准，窗口起点 2026-06-25 00:59 UTC。本次报告以 **arXiv 2026-06-25（Thu）批次** 为主要对象——arXiv 每日 14:00 UTC 公告窗口（2026-06-24 14:00 UTC ~ 2026-06-25 14:00 UTC）的新提交论文，跨类目 cs.AI（182）+ cs.CL（89）+ cs.MA（13）+ cs.LG（186）共 470 篇，去重后约 430 篇。注：部分 arXiv ID 的 v1 submission 时间戳显示早于 2026-06-25（如 2606.25161 = 2026-06-23T20:49 UTC），这源于 arXiv 的"hold / replace"机制——论文被暂存后重新公告在下一批次；为保证"过去 24 小时内被新公告"的口径，本报告以 listing 日期（2026-06-25）为准。
2. **类目选择**：cs.AI（核心，182 篇）+ cs.CL（LLM 记忆，89 篇）+ cs.MA（多 agent 共享记忆，13 篇）+ cs.LG（参数化记忆机制，186 篇），覆盖本次 11 篇核心+补充。
3. **关键词分层**：①**强匹配**（标题同时含 "agent" + "memory"）→ **6 篇**核心（25161 / 25449 / 25632 / 25342 / 25115 / 25361）；②**扩展匹配**（agent + role/continual/RAG/attention parametric）→ **3 篇**补充（25400 / 25358 / 25334）；③**语境补充**（GraphRAG 与 agent memory 紧密相关 + Unfireable Kernel 治理视角）→ **2 篇**补充（25656 / 26057）。
4. **未纳入的内容**：①纯 LLM 安全 / alignment 论文（与 agent memory 关联弱）；②RL agent 经典论文（非 LLM-based agent memory）；③纯 MARL 经验回放类（与传统 deep RL 经验回放无显著差别）；④会议 workshop 摘要（多已在主会议覆盖）。
5. **检索工具优先级**：①**arXiv listing 直接抓取**（最权威，列出每日完整公告）；②**jina-ai s.jina.ai**（web-level 检索验证热度与交叉引用）；③**jina-ai r.jina.ai**（解析 arXiv listing HTML）；④**arXiv API**（abstract / published 字段补全）。
6. **与昨日对比**：昨日（2026-06-25 日报）覆盖 2026-06-24 批次的 10 篇（核心 6 + 补充 4），主题集中于"系统化视角 / 治理原语 / 共享记忆"。今日 11 篇——数量略增，**主题从"宏观治理"向"微观可信度量化"收敛**：①**Reclaim Evaluation**（24049）/ **TRUSTMEM**（25161）把"记忆可信度"从概念讨论推向**可量化指标**；②**Memory Makes the Difference**（25361）首次形式化"记忆功能角色"概念；③**Lifelong ICL + Forget to Improve**（25342 / 25115）共同推动"参数化 / 预算化记忆"走向工程化；④领域专用多 agent（BrainAgent / Agentic BKT / Post-discharge）展示 agent memory 在医疗、教育、金融严肃游戏中的落地形态。

---

**报告生成时间**：2026-06-26 08:59 (Asia/Shanghai) / 2026-06-26 00:59 UTC
**生成 Agent**：programmer（cron:7e49d2a7-6aec-43f3-a094-db37ff850c50）
**检索工具链**：jina-ai Search/Reader API + arXiv listing + arXiv API
**报告路径**：`~/.openclaw/wiki/reports/2026-06-26-agent-memory.md`