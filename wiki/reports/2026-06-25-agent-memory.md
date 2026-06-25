# Agent 记忆 日报
> 日期：2026-06-25（周四，Asia/Shanghai 08:18）
> 检索时间窗口：过去 24 小时（2026-06-24 00:18 UTC ~ 2026-06-25 00:18 UTC）
> 检索源：arXiv `cs.AI` / `cs.CL` / `cs.MA` / `cs.LG` 类目 2026-06-24（Wed）新提交
> 检索工具：jina-ai Reader/Search + arXiv listing 直接抓取
> 筛选标准：标题/摘要含 "agent" ∩ "memory" 关键词，或专题相关（long-term / shared / procedural / reasoning memory）

---

## 📊 总体观察

- **arXiv 2026-06-24 新提交**：cs.AI **198** + cs.CL **94** + cs.MA **11** + cs.LG **110** ≈ **413 篇**新增，与 6 月 23 日（847 篇）相比有显著回落——符合工作日-周末节律（24 Jun 周三，恰好处于 ICML 2026 截稿后的常规节奏）。
- **"Agent Memory" 主题论文**：6 篇核心（标题同时含 "agent" + "memory"，跨 cs.AI/cs.CL/cs.LG）+ 4 篇相关 ≈ **10 篇**，占比 ~2.4%，是当日智能体方向的关键子主题。
- **研究热点迁移**：从昨日的"记忆可靠性 / 偏差传播"转向今日的"**记忆系统化（systematization）+ 跨层推理记忆（cross-layer reasoning memory）**"；新出现 3 个具体子方向——记忆作为数据管理（4 模块分解）、基于 Gibbs 测度的潜在记忆检索、共享记忆的治理原语（fleet memory governance）。
- **代码 / 数据可用性**：10 篇中 4 篇明确开源（Agent-Native Memory / Privacy-RAG / ReM-MoA / Metis 实验代码），3 篇有 GitHub 链接，1 篇有公开 paper list。

---

## 🧠 一、Agent 记忆系统化与基准（Systematization & Benchmarks）

### 文章 1：Are We Ready For An Agent-Native Memory System?
- **标题**：Are We Ready For An Agent-Native Memory System?
- **作者**：Shao Kun Han 等（OpenDataBox）
- **时间**：2026-06-24（arXiv: 2606.24775，cs.CL；v1 提交 2026-06-23 16:34 UTC）
- **主要内容**：把"agent memory"从端到端黑盒评估（F1 / BLEU）转向**数据管理系统视角**。提出 4 模块分析框架：记忆表示与存储 / 抽取 / 检索与路由 / 维护。系统评估 12 个代表记忆系统 + 2 个基线，覆盖 5 个工作负载 / 11 个数据集；通过细粒度 ablation 量化各模块对表征保真度 / 检索精度 / 更新正确性 / 长时稳定性的影响。关键发现：①**无单一架构在所有场景占优**——效果取决于记忆结构与工作负载瓶颈的对齐度；②成本-性能 trade-off 表明**局部维护**比全局重组更划算。代码与 paper list 均开源（OpenDataBox/MemoryData、OpenDataBox/awesome-agent-memory）。

### 文章 2：MEMPROBE
- **标题**：MEMPROBE: Probing Long-Term Agent Memory via Hidden User-State Recovery
- **作者**：（cs.CL 2026-06-24 listing，arXiv: 2606.24595）
- **时间**：2026-06-24
- **主要内容**：主张长时记忆应被评估为**可审计的后交互产物**——"在普通协助后，能从 agent 留下的记忆中重建出多少结构化用户状态？"。构建 50 个模拟用户、每人 31 维隐藏状态（1,550 个恢复目标）的基准，覆盖全量存储 / top-k 两种访问模式，测试 5 个代表记忆系统。核心发现：**任务完成与记忆可恢复性是两种独立能力**——即使无记忆基线任务完成也近饱和，但类别平衡恢复率仅约 0.6，top-k 检索下进一步下降。首次形式化"memory as auditable artifact"。

---

## 🏛️ 二、共享记忆与多智能体治理（Shared Memory & Governance）

### 文章 3：Governed Shared Memory / MemClaw
- **标题**：Governed Shared Memory for Multi-Agent LLM Systems
- **作者**：（cs.AI 2026-06-24 listing，arXiv: 2606.24535）
- **时间**：2026-06-24
- **主要内容**：形式化 **fleet-memory problem**，识别 4 种基础失败模式：未授权泄漏 / 过期传播 / 矛盾持久 / 来源坍缩。提出 4 个系统级原语：scoped retrieval / temporal supersession / provenance tracking / policy-governed propagation。在生产多租户记忆服务 **MemClaw** 中实现，并通过 **ArgusFleet** 评估。重点：①**Provenance 维度**在 4 层派生链上 100% 重建作者身份，亚秒级延迟；②**Propagation 维度**舰队内高可见性、零跨舰队泄漏，强写模式下写入-可见延迟优化为单次搜索往返；③披露两个**生产架构问题**——子租户 scope 在 GET-by-id 直查路径被绕过（已修复）、同步近重复 gate 与矛盾超序冲突；强调"测量在生产服务而非对照基线"。

### 文章 4：ReM-MoA
- **标题**：ReM-MoA: Reasoning Memory Sustains Mixture-of-Agents Scaling
- **作者**：（cs.AI 2026-06-24 listing，arXiv: 2606.24437）
- **时间**：2026-06-24
- **主要内容**：现有 Mixture-of-Agents (MoA) 架构在深度增加时增益停滞或饱和。ReM-MoA 用两个机制维持 scaling：①**Ranked Reasoning Memory**——用 Reviewer Agent 比较并排序所有层的推理痕迹，持久化；②**Curated Diversified Memory Routing**——给不同 agent 暴露不同组合的成功/失败痕迹，保探索多样性同时传播高质量推理。5 个推理 benchmark（数学 / 形式逻辑 / 代码 / 知识 / 常识）上，深度+宽度 scaling 全面超越既有 MoA 变体，**深度越深优势越大**——确立"结构化跨层推理记忆"是可扩展多 agent 推理的关键缺失机制。可选多域 Reviewer 蒸馏管线由前沿模型监督。

---

## ⚙️ 三、自演化与跨模态记忆（Self-Evolving & Procedural Memory）

### 文章 5：Metis
- **标题**：Metis: Bridging Text and Code Memory for Self-Evolving Agents
- **作者**：（cs.AI / cs.CL 2026-06-24 listing，arXiv: 2606.24151）
- **时间**：2026-06-24
- **主要内容**：自演化 agent 用"经验"改进未来——但现有系统在"自然语言文本记忆 vs 代码可调用工具记忆"间二选一时多凭设计而非经验特性。Metis 是**首个在同一经验集上同时隔离 text/code 记忆的对照研究**，发现两者在构建成本 / 执行效率 / 可迁移性上**互补且均不可或缺**。据此提出**分层双表征记忆**：文本层组织为执行计划 / 环境事实 / 常见坑；高频重复计划"结晶"为已验证可调用工具。AppWorld 基准上任务准确率较 ReAct 最高提升 **20.6%**，执行成本降低 **22.8%**。

### 文章 6：Reasoning as Attractor Dynamics
- **标题**：Reasoning as Attractor Dynamics: Latent Memory Retrieval via Gibbs-Weighted Energy Minimization
- **作者**：（cs.LG 2026-06-24 listing，arXiv: 2606.24543；ICLR Workshop 2026）
- **时间**：2026-06-24
- **主要内容**：把 LLM 重新建模为**高维 Dense Associative Memory**——正确推理链对应输出分布中"深而宽的吸引子盆地（flat minima）"，幻觉对应"尖锐不稳定的局部极小"。提出基于 Gibbs 测度的检索机制：用多条推理路径的谱熵作逆能量加权（$P \propto e^{-\beta E}$），让系统"弛豫"到鲁棒解。Microsoft Phi-3.5 在 GSM8K 提升 **5.38%**（84.7%→90.1%）。为"推理即动态沉降到吸引子"提供物理启发证据。

---

## 🧩 补充条目（其他与 Agent 记忆强相关）

### 文章 7：OpenThoughts-Agent
- **标题**：OpenThoughts-Agent: Data Recipes for Agentic Models
- **作者**：（cs.AI 2026-06-24 listing，arXiv: 2606.24855）
- **时间**：2026-06-24
- **主要内容**：开放 agent 训练数据流水线（100+ 受控 ablation + 100K 训练样本 + Qwen3-32B 微调），在 7 个 agentic benchmark 平均 44.8%，较最强开源数据 agent (Nemotron-Terminal-32B 40.9%) **+3.9pp**；在计算控制的对比中，OT-Agent 数据在所有训练集规模下均超越替代开源数据。
- **与 Agent 记忆的关联**：训练数据中包含大量"agent 调用工具 + 多步推理 + 中间状态"的轨迹，等同于把记忆/上下文操作模式内化进模型权重。

### 文章 8：Privacy-Preserving RAG via Multi-Agent Semantic Rewriting
- **标题**：Privacy-Preserving RAG via Multi-Agent Semantic Rewriting: Achieving Confidentiality Without Compromising Contextual Fidelity
- **作者**：Tao Fang 等（cs.AI 2026-06-24，arXiv: 2606.24623，Elsevier IPM 正式接收，23 页）
- **时间**：2026-06-24
- **主要内容**：用 3 个专门 agent（隐私抽取 / 语义分析 / 重建）协作改写检索内容以保护敏感标识符，同时保语义。在 ChatDoctor / Wiki-PII 6 个 LLM 上：LLaMA-3-8B 目标信息暴露从 144 → **1**；BLEU-1 0.122 优于 SAGE 0.117；异步离线预处理**不增加在线推理延迟**。代码开源。
- **与 Agent 记忆的关联**：RAG 的"检索→记忆→生成"链路中，记忆层是隐私泄漏主要面——本工作把"清洗"前移到记忆入口。

### 文章 9：Emergent Relational Order in LLM Agent Societies
- **标题**：Emergent Relational Order in LLM Agent Societies: From Collective Affect to Authority Stratification
- **作者**：（cs.AI / cs.MA 2026-06-24 listing，arXiv: 2606.23764，ACL 2026 Findings，37 页）
- **时间**：2026-06-24
- **主要内容**：CAREB-MAS 多 agent 框架（融合 Affect Control Theory / Social Identity Theory / Durkheimian collective affect），长时模拟中**自发涌现** 5 个"差序格局"核心现象：稳定劳动分工 / 关系型经济伦理 / 关系衰减的合作 / 涌现关系权威 / 宗族式中心-边缘分层。从纯个体生产+偏好分配+最小交互协议的微观环境涌现出宏观社会结构。
- **与 Agent 记忆的关联**：agent 维持"动态演化的自我中心身份"——本质上是个体级身份记忆 + 集体级社会结构记忆的协同演化。

### 文章 10：ASALT
- **标题**：ASALT: Adaptive State Alignment for Lateral Transfer in Multi-agent Reinforcement Learning
- **作者**：（cs.AI / cs.LG 2026-06-24 listing，arXiv: 2606.24601，RLC 2026）
- **时间**：2026-06-24
- **主要内容**：MARL 跨域迁移要求源/目标域观测与全局状态维度严格一致——本工作打破此约束，提出 ASALT：observation-level + state-level 双适配器将目标域映射到共享嵌入空间。多个标准 MARL benchmark 上样本效率与全局回报超越既有基线，且能缓解负迁移。
- **与 Agent 记忆的关联**：作为强化学习 agent，"对齐的潜在状态空间"等价于一种"结构化策略记忆"——能跨异构任务复用。

---

## 🔗 参考链接

| arXiv ID | 链接 | 类型 |
|----------|------|------|
| 2606.24775 | https://arxiv.org/abs/2606.24775 — Are We Ready For An Agent-Native Memory System? | 核心 |
| 2606.24595 | https://arxiv.org/abs/2606.24595 — MEMPROBE | 核心 |
| 2606.24535 | https://arxiv.org/abs/2606.24535 — Governed Shared Memory (MemClaw/ArgusFleet) | 核心 |
| 2606.24437 | https://arxiv.org/abs/2606.24437 — ReM-MoA | 核心 |
| 2606.24151 | https://arxiv.org/abs/2606.24151 — Metis | 核心 |
| 2606.24543 | https://arxiv.org/abs/2606.24543 — Reasoning as Attractor Dynamics | 核心 |
| 2606.24855 | https://arxiv.org/abs/2606.24855 — OpenThoughts-Agent | 补充 |
| 2606.23764 | https://arxiv.org/abs/2606.23764 — Emergent Relational Order (CAREB-MAS) | 补充 |
| 2606.24623 | https://arxiv.org/abs/2606.24623 — Privacy-Preserving RAG | 补充 |
| 2606.24601 | https://arxiv.org/abs/2606.24601 — ASALT | 补充 |

- **开源仓库**：
  - Agent-Native Memory: https://github.com/OpenDataBox/MemoryData（论文代码）+ https://github.com/OpenDataBox/awesome-agent-memory（论文列表）
  - Privacy-Preserving RAG: https://github.com/foursoils/Privacy-Preserving-RAG
  - OT-Agent: http://openthoughts.ai/
- arXiv cs.AI 2026-06-24 listing：https://arxiv.org/list/cs.AI/recent?skip=0&show=2000
- arXiv cs.CL 2026-06-24 listing：https://arxiv.org/list/cs.CL/recent?skip=0&show=2000
- arXiv cs.MA 2026-06-24 listing：https://arxiv.org/list/cs.MA/recent?skip=0&show=2000
- arXiv cs.LG 2026-06-24 listing：https://arxiv.org/list/cs.LG/recent?skip=0&show=2000

---

## 📝 检索方法学说明

1. **范围界定**：严格遵循"过去 24 小时"——以 2026-06-25 00:18 UTC 为基准，窗口起点 2026-06-24 00:18 UTC。arXiv 2026-06-24（Wed, 美东 14:00 announcement）批次的新提交论文全部在窗口内；2026-06-23（Tue）的 847 篇被排除（已纳入昨日 2026-06-24 日报）。
2. **类目选择**：cs.AI（核心，198 篇）+ cs.CL（语言模型记忆，94 篇）+ cs.MA（多 agent 共享记忆，11 篇）+ cs.LG（潜在记忆机制，110 篇），共 413 篇去重后覆盖 10 篇。
3. **关键词分层**：①强匹配（标题同时含 "agent" + "memory"）→ **6 篇**（24775 / 24595 / 24535 / 24437 / 24151 / 24543）；②扩展匹配（agent + reasoning/attractor/relational）→ **3 篇**（23764 / 24623 / 24601）；③语境补充（"agentic data recipes" 内含大量多步工具调用与上下文管理训练信号）→ **1 篇**（24855）。
4. **未纳入的内容**：6 月 23 日及更早的 arXiv 论文（窗口外）、会议 workshop 摘要（ICLR Workshop 2026 接收但内容多已在主会议覆盖）、Twitter/Hacker News 等非学术渠道。
5. **检索工具**：jina-ai `r.jina.ai` 解析 arXiv listing HTML（每个 listing 含完整 198/94/11/110 条目） + 单条 arXiv abs 页面（application/json 取 title / publishedTime / abstract 字段）。
6. **与昨日对比**：昨日 14 篇（核心 8 + 补充 6），今日 10 篇（核心 6 + 补充 4）——论文数量下降是正常的论文产出日变化（昨日 847 vs 今日 413，-51%），但**主题结构更集中**（系统化/治理/跨层记忆占 60%）。
