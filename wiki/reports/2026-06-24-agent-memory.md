# Agent 记忆 日报
> 日期：2026-06-24（周三，Asia/Shanghai 08:13）
> 检索时间窗口：过去 24 小时（2026-06-23 00:13 UTC ~ 2026-06-24 00:13 UTC）
> 检索源：arXiv `cs.AI` / `cs.CL` / `cs.MA` 类目 2026-06-23（Tue, 569 + 246 + 32 = 847 篇新论文）
> 检索工具：jina-ai Reader/Search + arXiv listing 直接抓取
> 筛选标准：标题/摘要含 "agent" ∩ "memory" 关键词，或专题相关（procedural / long-term / personalized / prospective memory）

---

## 📊 总体观察

- **arXiv 2026-06-23 新提交**：cs.AI 569 篇、cs.CL 246 篇、cs.MA 32 篇共 **847 篇**，是 6 月以来单日新论文数最高的一天（受 ICLR 2026 / ICML 2026 截稿日影响）。
- **"Agent Memory" 主题论文**：8 篇核心 + 6 篇补充 ≈ **14 篇**，占比约 1.7%，是当日 LLM 智能体方向最热子主题之一（仅次于 multi-agent 协作、agent evaluation、agentic RAG）。
- **研究热点迁移**：从"如何建记忆库"（2024-2025 主流）迁移到"如何让记忆可靠、可证、可治理"（2026 主流），新出现 4 个具体子方向——上下文重建、过程性记忆、记忆偏差传播、个性化长时记忆。
- **代码 / 数据可用性**：14 篇中 5 篇明确开源（Revelio / AlphaMemo / Negative Knowledge / EvoEmbedding / DynamicMem），链接见各条目。

---

## 🧠 一、长时记忆与上下文重建（Long-term Memory & Context Reconstruction）

### 文章 1：RaMem
- **标题**：RaMem: Contextual Reinstatement for Long-term Agentic Memory
- **作者**：Wei Yang, Bryce Kan, Shixuan Li, Li Li 等
- **时间**：2026-06-23（arXiv: 2606.22844）
- **主要内容**：提出"上下文坍缩（context collapse）"问题——记忆被压缩后因共享实体/用户状态而看似相关，但缺乏事件发生时的时间/会话/参与方等边界信息，使检索证据不可证。RaMem 通过 4 阶段（evidence anchoring → recall condition induction → validity-aware retrieval → context-preserved synthesis）把检索到的记忆片段转为可验证证据。在多个 long-term memory benchmark 上 F1 平均提升 10%+。

### 文章 2：Nous
- **标题**：Nous: A Predictive World Model for Long-Term Agent Memory
- **作者**：Pranav Singh
- **时间**：2026-06-23（arXiv: 2606.22030）
- **主要内容**：颠覆"事实存储"范式，主张"知识是预测而非存储"。对每个 entity-attribute 维护一个 categorical 概率分布（dimension），新观察按信息论惊讶度 S = -log2 P(obs|D) 打分并通过 closed-form Bayesian 后验更新；主存"delta"（prior→posterior 偏移）而非事实本身。在 LoCoMo 长时对话记忆 benchmark 上 F1 达到单跳 63.50 / 多跳 55.32 / 时序 58.57 / 开放域 62.50；无需外部向量数据库或图引擎。

### 文章 3：Learning What Not to Forget（LRE）
- **标题**：Learning What Not to Forget: Long-Horizon Agent Memory from a Few Kilobytes of Learning
- **作者**：Nusrat Jahan Lia, Aritra Mazumder
- **时间**：2026-06-23（arXiv: 2606.20954）
- **主要内容**：把"记忆淘汰"重新定义为**保真度问题**而非压缩问题。LRE 是个仅几 KB、CPU-only、无神经网络的打分器，学习哪些历史单元是"承重"的并 verbatim 保留。在匹配预算比较下，agent 任务上 LRE 与"保留全部历史"持平，峰值上下文缩减 52%；在 LoCoMo 阅读任务上比 dense/token-pruning encoder 更优、token 少 68%。监督可标注免费——仅用系统自身行为训练可恢复 95% 有监督效果。

### 文章 4：EvoEmbedding
- **标题**：EvoEmbedding: Evolvable Representations for Long-Context Retrieval and Agentic Memory
- **作者**：Chang Nie, Chaoyou Fu, Junlan Feng 等
- **时间**：2026-06-23（arXiv: 2606.21649）
- **主要内容**：现有 embedding 静态地、孤立地编码片段，忽略上下文与时序。EvoEmbedding 维护一个连续更新的潜记忆，在顺序处理输入时与原文联合生成"可演化"嵌入。配套 180K 数据集 + memory queue 防表征坍缩 + segment-batching 训练加速 3.8×。在长上下文检索上击败 Qwen3-Embedding-8B / KaLM-Gemma3-12B；朴素 RAG 管线配上 EvoEmbedding 即超越专用 agentic memory 系统。

---

## 🔁 二、过程性记忆与技能演化（Procedural Memory & Self-Evolving）

### 文章 5：AFTER（Managing Procedural Memory）
- **标题**：Managing Procedural Memory in LLM Agents: Control, Adaptation, and Evaluation
- **作者**：Julia Belikova, Rauf Parchiev, Evgeny Egorov, Grigorii Davydenko 等
- **时间**：2026-06-23（arXiv: 2606.23127）
- **主要内容**：发布 AFTER benchmark——382 个企业级任务、6 个职业角色、22 个过程性技能，覆盖 4 种迁移评估（local improvement / cross-task / cross-role / cross-model）。发现：①单轮 refinement 整体性能 +3.7~6.7 分；②多模型执行轨迹融合的技能达 73.1% 跨模型准确率，超过任何单模型源；③部分技能广泛迁移，部分技能特化到角色工作流后迁移失效——为生产 agent 平台的技能构建/评估/部署提供实操指南。

### 文章 6：AlphaMemo
- **标题**：AlphaMemo: Structured Search-Process Memory for Self-Evolving Alpha Mining Agents
- **作者**：Hang Yu, Zifan Zheng, Jeff Z. Pan, Tongliang Liu 等
- **时间**：2026-06-23（arXiv: 2606.20625）
- **主要内容**：针对 LLM alpha 挖掘中组合搜索空间、非平稳反馈、冗余发现、过度拟合旧成功的问题，提出结构化"搜索过程记忆"——不仅记最终因子或全轨迹，而是从 AST diff 中抽取可复用的 edit motif，对搜索账本先验做 confidence-gated 残差学习，并加非对称 veto 抑制高置信失败模式。在 CSI 500 / S&P 500 上改善样本外表现与定预算发现效率；代码开源。

---

## ⚠️ 三、记忆安全与偏差传播（Memory Safety & Bias Propagation）

### 文章 7：Memory Contagion
- **标题**：Memory Contagion: Cross-Temporal Propagation of Evaluator Bias via Agent Memory
- **作者**：Zewen Liu
- **时间**：2026-06-23（arXiv: 2606.23195）
- **主要内容**：首次形式化"记忆传染"——当智能体被有偏评估者训练/引导时，记忆即使**完美整合（oracle）**也会把偏差跨时序传染给未来检索同一记忆库的 agent。三阶段实验证明：①oracle 整合下仍发生传染（输入有偏是充分条件）；②整合对偏差类型有相反效应——稳健衰减长度偏好、初步放大权威偏好；③污染率低至 p=0.2 仍可检测到传播，无安全阈值。暴露当前 agent 记忆设计的关键脆弱性。

### 文章 8：Revelio
- **标题**：Revelio: Cost-Efficient Agentic Memory Safety Vulnerability Detection For Repository-Scale Codebases
- **作者**：Yiwei Hou, Hao Wang, Muxi Lyu, Marius Momeu 等
- **时间**：2026-06-23（arXiv: 2606.22263）
- **主要内容**：端到端 agentic 框架，**针对代码"内存安全漏洞"**（注意：是 C/C++ 内存安全，不是 LLM 记忆机制）。用廉价 LLM + 轻量静态分析生成漏洞假设，生成可执行 Proof-of-Vulnerability 并用 deterministic sanitizer 验证。在被持续 fuzz 5-8 年的 7 个生产项目 + 100 个 Arvo 项目上，约 1 小时/项目、$300 总成本下发现 19 个未知内存安全漏洞，在多模型 backbone 上击败前沿 coding agent。

---

## 👤 四、个性化长时记忆与用户建模（Personalized Long-term Memory）

### 文章 9：DynamicMem
- **标题**：DynamicMem: A Long-Horizon Memory Benchmark in Real-World Settings
- **作者**：（cs.AI 2026-06-23 listing，arXiv: 2606.22877）
- **时间**：2026-06-23
- **主要内容**：合成 15 个月/用户的活动数据，平均 2.2M tokens + 1,772 grounded events，跨 16 个 app（电商/健身/社交等）。用户画像（属性/习惯/偏好）从不显式给出——必须从散落小信号中推断，每季度一次 checkpoint。基准测试 5 个代表系统后发现：①profile 重建随历史增长退化，但服务任务准确率持平；②无系统能同时保留"持续事实"和"替换变化事实"，错误集中在偏好和指称；③>93% 失败来自记忆检索而非答案生成——最大改进空间在记忆层。

### 文章 10：RootMem
- **标题**：Towards Root Memories: Benchmarking and Enhancing Implicit Logical Memory Retrieval
- **作者**：（cs.CL 2026-06-23 listing，arXiv: 2606.23283）
- **时间**：2026-06-23
- **主要内容**：现有检索主要靠语义相似度，会漏掉语义重叠低但逻辑关键的"隐式逻辑记忆"。构建 IMLic（首个长对话隐式逻辑记忆 benchmark），提出"根记忆"——结构化、决策保持的表征，从长期用户历史蒸馏可复用个性化逻辑；配合 LLM-based router 激活逻辑相关项，补足语义检索。实验显著超越最强检索基线，并稳定提升现有 memory agent 准确率。

### 文章 11：Latent Personal Memory
- **标题**：Latent Personal Memory: Represent personal memory as dynamic soft prompts
- **作者**：Debrup Das, Avinash Amballa, Yashas Malur Saidutta, Vijay Srinivasan 等
- **时间**：2026-06-23（arXiv: 2606.20911）
- **主要内容**：用 N 个潜 slot 的紧凑持久矩阵表示用户历史，跨注意力投影网络把 slot 映射成动态 soft prompt 前置到冻结 LLM 输入。在 PersonaMem v1 上对 LoRA / Prompt Tuning 整体准确率提升 8.8% / 54.4%，KV-cache 减少 64×；在 LoCoMo 上以 120× 少的可训练参数匹配 LoRA；128K 上下文长度下超越 full-context。

---

## 🔮 五、前瞻性记忆与负知识（Prospective Memory & Negative Knowledge）

### 文章 12：TriggerBench
- **标题**：TriggerBench: Investigating Prospective Memory for Large Language Models
- **作者**：（cs.CL 2026-06-23 listing，arXiv: 2606.23459）
- **时间**：2026-06-23
- **主要内容**：把"前瞻性记忆（PM）"——自发回忆起并执行潜在约束、不需直接提示——作为独立能力评估。覆盖 5 维度（日常助手 + 专业工作流）、配对 RM 对照、正负变体、过载触发器。3 个发现：①PM 有 precision-recall 权衡和注意脆弱性（增强推理可改善主动召回，但会过拟合到"总是提醒"启发式）；②PM 显著难于 RM——同样上下文下 RM 在 100K tokens 近饱和，PM 随上下文增长急剧衰减；③PM 可作为"备用推理容量"行为探针——AIME-2025 数学题成功轨迹的 PM 准确率高于失败轨迹。

### 文章 13：Negative Knowledge as Failure-aware Shared Memory
- **标题**：Negative Knowledge as Failure-aware Shared Memory for AutoResearch
- **作者**：Hanchun Wang
- **时间**：2026-06-23（arXiv: 2606.21024）
- **主要内容**：AI 辅助科研产生大量失败尝试，但极少成为共享知识资产。提出"负知识记忆层"——curator agent 把每次失败转为有界、类型化的记录，下游研究 agent 在提下个实验前显式 adopt/reject。同任务重试（ScienceAgentBench）+ 跨任务（两个非线性数学物理 PDE）上击败 vanilla AutoResearch 且用更少 token；负知识库可跨 PDE 任务迁移；建议把结构化负知识当作"集体科研记忆基础设施"与正向发现并列维护。

---

## 🎁 补充条目（其他与"记忆机制"高度相关）

### 文章 14：Code Isn't Memory
- **标题**：Code Isn't Memory: A Structural Codebase Index Inside a Coding Agent
- **作者**：Ishaan Bhola, Adithyan Krishnan, Sravanth Kurmala, Mukunda NS
- **时间**：2026-06-23（arXiv: 2606.22417）
- **主要内容**：在固定 coding agent harness + Claude Opus 4.7 上做 with/without 索引的 ablation，发现结构化代码库索引在 SWE-PolyBench Verified / SWE-bench Pro 上带来显著定位 + 解决率提升且无成本惩罚。结论：部署结构化代码库索引的问题不是"是否太贵"而是"工作负载是否含多文件变更"。
- **与 Agent 记忆的关联**：呼应 RaMem / LRE 中"记忆 ≠ 事实陈列"的论点——索引不是存储，结构化检索才能让 coding agent 真正"记起"代码库的拓扑。

---

## 🔗 参考链接

| arXiv ID | 链接 |
|----------|------|
| 2606.22844 | https://arxiv.org/abs/2606.22844 — RaMem |
| 2606.22030 | https://arxiv.org/abs/2606.22030 — Nous |
| 2606.20954 | https://arxiv.org/abs/2606.20954 — LRE |
| 2606.21649 | https://arxiv.org/abs/2606.21649 — EvoEmbedding |
| 2606.23127 | https://arxiv.org/abs/2606.23127 — AFTER (Procedural Memory) |
| 2606.20625 | https://arxiv.org/abs/2606.20625 — AlphaMemo |
| 2606.23195 | https://arxiv.org/abs/2606.23195 — Memory Contagion |
| 2606.22263 | https://arxiv.org/abs/2606.22263 — Revelio |
| 2606.22877 | https://arxiv.org/abs/2606.22877 — DynamicMem |
| 2606.23283 | https://arxiv.org/abs/2606.23283 — RootMem |
| 2606.20911 | https://arxiv.org/abs/2606.20911 — Latent Personal Memory |
| 2606.23459 | https://arxiv.org/abs/2606.23459 — TriggerBench |
| 2606.21024 | https://arxiv.org/abs/2606.21024 — Negative Knowledge |
| 2606.22417 | https://arxiv.org/abs/2606.22417 — Code Isn't Memory |

- arXiv cs.AI 2026-06-23 完整 listing：https://arxiv.org/list/cs.AI/recent?skip=0&show=2000
- arXiv cs.CL 2026-06-23 listing：https://arxiv.org/list/cs.CL/recent?skip=0&show=2000
- arXiv cs.MA 2026-06-23 listing：https://arxiv.org/list/cs.MA/recent?skip=0&show=2000

---

## 📝 检索方法学说明

1. **范围界定**：严格遵循"过去 24 小时"——以 2026-06-24 00:13 UTC 为基准，窗口起点 2026-06-23 00:13 UTC。arXiv 2026-06-23（Tue, 美东时区 14:00 announcement）批次的新提交论文全部在窗口内；上一批 2026-06-19 ~ 2026-06-22 的论文被排除。
2. **类目选择**：cs.AI（核心，569 篇） + cs.CL（语言模型记忆，246 篇） + cs.MA（多 agent 共享记忆，32 篇），共 847 篇去重后覆盖 14 篇。
3. **关键词分层**：①强匹配（标题同时含 "agent" + "memory"）→ 8 篇；②扩展匹配（标题含 "long-term memory" / "prospective memory" / "personal memory" / "negative knowledge"）→ 5 篇；③语境补充（"memory safety vulnerability" 虽属 C/C++ 漏洞但通过 agentic 框架呈现，对程序员的 agent 视角有借鉴价值）→ 1 篇。
4. **未纳入的内容**：6月22日及更早的 arXiv 论文（窗口外）、会议 workshop 摘要（ICML 2026 7 月才开，无 24h 内新论文）、Twitter/Hacker News 等非学术渠道。
5. **检索工具**：jina-ai `s.jina.ai` 搜索 + `r.jina.ai` 解析摘要；arXiv listing HTML 直抓（含完整 569 篇 23 Jun 论文）作为 ground truth。
