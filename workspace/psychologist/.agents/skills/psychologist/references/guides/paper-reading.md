# 论文阅读 SOP（v1.0）

> **适用身份**：心理科学家子身份（literature review / research design / meta-analysis）
> **核心原则**：真实性 > 数据安全 > 规范完整 > 伦理严谨 > 方法科学 > 协作效率 > 响应速度
> **沉淀来源**：2026-06-05 Diehl et al. (2026) JARMAC 论文阅读实战（5 个研究、N=709）
> **配套资源**：
> - wiki 模板：`sources/_template_source_summary.md`
> - wiki 模板：`syntheses/` 命名约定 `YYYY-MM-DD-HH-MM-SS-标题.md`
> - 工具：`pdftotext`、`pdfinfo`、Semantic Scholar / CrossRef / APA PsycNet API

---

## 0. 概述：三大产出物

论文阅读的产出不是"读完"，而是**沉淀到 vault 的三层结构**：

```
raw/<category>/<file>              ← 原始 PDF（证据层，零处理）
   ↓ 轻提炼
sources/<name>.md                  ← source summary（4 字段，~3000 字）
   ↓ 重提炼
syntheses/<date>-<title>.md        ← syntheses 笔记（综合分析，~5000 字）
```

**关键约束**：
- raw 不可修改；sources/syntheses 可编辑但要 source-backed
- 每个 raw source 必须配一个 source summary（一对一）
- syntheses 笔记必须可回溯到具体 source summary（**不能直接引用 raw**）

---

## 1. 阅读前清单（Pre-Reading Checklist）

**目的**：避免"读了一篇不知道用来干嘛"。在打开 PDF 之前必须回答 3 个问题：

### 1.1 读什么

| 字段 | 必填 | 示例 |
|------|------|------|
| **DOI / 文件位置** | ✅ | `10.1037/mac0000231` 或 `/root/.openclaw/wiki/raw/papers/2026-06-05_Diehl-et-al_...pdf` |
| **文章类型** | ✅ | paper / article / book / note |
| **学术等级** | ✅ | 顶刊（Q1 JCR）/ 一般期刊 / 预印本 / 灰色文献 |
| **作者机构** | ✅ | USC Marshall / Yale SOM / Colorado Boulder |
| **老板与作者的熟悉度** | ⭕ | 是否之前读过同作者系列（Barasch-Diehl-Zauberman 2026 是系列第 3 篇） |

### 1.2 为什么读

**至少明确 1 个目的**（建议明确 2-3 个）：

- ⬜ **主线证据**：作为老板研究主线（X 项目）的关键实证支柱
- ⬜ **方法学借鉴**：设计巧妙、值得复用的方法（Diehl 2026 的"美学评分 cover story"）
- ⬜ **理论对话**：与现有 source summary 链上的某篇形成引用或反对关系
- ⬜ **批判性案例**：暴露某理论的局限（King 2024 因果性不足 → Diehl 2026 因果补强）
- ⬜ **综述写作素材**：直接用于正在写的 syntheses / 综述章节

### 1.3 预期产出

**用 1-3 句话回答**："读完这篇，我会让老板的 vault 多出什么？"

> 范例："读完 Diehl 2026 会在 `sources/` 多一篇 source summary（含 5 个研究方法表），会在 `syntheses/` 多一篇'照片视角-记忆漂移'综合分析笔记，会连接到已有的 Hutmacher 2026 科普评论和 AMEDIA 框架概念页。"

**如果没有预期产出，停止阅读**——这是"为读而读"的反模式。

---

## 2. 三遍阅读法（Three-Pass Method）

基于 Diehl 2026 实战提炼的**时间分配**（10 页论文，共 30-50 分钟）：

### 2.1 第一遍：鸟瞰（5-10 分钟）

**目标**：判断"值不值得细读"和"它属于哪一类贡献"。

| 阅读范围 | 关键问题 |
|----------|----------|
| 标题 + 摘要 | 主题是什么？核心发现是什么？ |
| 引言末段 / 假设陈述 | 作者要回答什么问题？ |
| 讨论框架（首段） | 作者如何定位自己的贡献？ |
| Figure 1 + Table 1 | 主要结果长什么样？ |
| 参考文献（最后 5-10 条） | 与哪些关键文献对话？ |

**判断动作**：
- 如果发现是同作者 / 同系列的最新成果 → 继续
- 如果发现是教科书级别综述 → 精读
- 如果发现是边缘相关 → 关闭，存入"延后处理"队列

### 2.2 第二遍：细读（30-40 分钟）

**目标**：建立**完整方法+结果**的硬数据基础。

| 阅读范围 | 必抓的字段 |
|----------|----------|
| 方法学（每个研究） | 样本（N, 人口学）、操纵（IV, levels）、因变量（DV, 量表）、程序、排除规则 |
| 结果（每个研究） | M, SD, F/t/χ², df, p, η²p / d / r 效应量，CI（如果有） |
| 表格 | 全部数字过一遍 |
| Figure | 视觉化结果的趋势与交点 |

**关键动作**：
- 把所有数字**抄录**到临时文件（pdftotext + 手工整理）——不要靠记忆
- 建立**跨研究的对照表**（5 个研究的方法学总表 = 第二遍的核心产出）
- 标注每个 p 值的显著性（\* p<.05, \*\* p<.01, \*\*\* p<.001）

**第二遍的产出**：一个完整的研究方法+结果表（约 30-50 行 markdown）

### 2.3 第三遍：精读（30-60 分钟）

**目标**：理解**为什么这样设计、这样分析、这样解读**——为 source summary 和 syntheses 做准备。

| 阅读角度 | 关键问题 |
|----------|----------|
| **方法学巧思** | 作者用了什么 cover story / 操纵范式 / 控制组设计？为什么这样？ |
| **排除规则的合理性** | 排除了多少被试？为什么？preregistered vs ad-hoc？ |
| **跨研究的递进** | Study 1→2→3→4→5 的设计是如何演化的（从 field 到 online，从 2 条件到 3 条件）？ |
| **General Discussion 的局限** | 作者**自己承认的**局限 vs 实际**未提及**的局限 |
| **理论对话** | 引用了谁？被谁引用？理论定位在哪？ |
| **实战价值** | 这篇对老板的具体研究主线（X 项目）有什么可引用的角度？ |

**第三遍的产出**：
- 一段"核心 takeaway"（30-80 字，作为 source summary 的"一句话总结"）
- 3-7 条"关键内容" bullet（已取舍）
- 0-N 个"影响到的页面"（wikilink）
- 0-N 个"待确认"（暴露脆弱性）

---

## 3. 负面结果记录（Negative Results Recording）

**目的**：避免"只看到阳性"的 publication bias 镜像；负面结果是综述的**关键证据**。

### 3.1 三类负面结果

| 类型 | 定义 | 重要性 |
|------|------|--------|
| **A. 推翻假设的负面** | 主假设不成立（p > .05） | ⭐⭐⭐ **关键**——理论修正依据 |
| **B. 边缘显著** | .05 < p < .10 | ⭐⭐ **重要**——需查统计效力、样本量 |
| **C. 假设不涉及但探索性的** | 探索性分析无显著 | ⭐ 一般——避免过度解读 |

### 3.2 记录格式（必填字段）

```markdown
- **[负面类型]** [哪个研究] [哪个因变量] [哪个条件]：
  - 统计量 [F/t/χ² (df) = X, p = Y, η²p = Z]
  - 作者解读 [作者怎么解释的？归因于统计效力？操作失败？理论局限？]
  - 我的评估 [是否合理？是否需要 ANCOVA / Bayesian 替代？]
```

**范例**（来自 Diehl 2026 实战）：

```markdown
- **[B. 边缘显著]** Study 5：3rd-person vs control 条件记忆视角
  - F(1, 208) = 3.60, p = .06, η²p = .017
  - 作者解读：review 行为越多效应越大，但控制组（不上传评价）已接近 baseline
  - 我的评估：与 3rd vs mixed (p = .05) 效力差距小，作者未深讨论——综述时需明确指出

- **[C. 探索性负面]** Study 2/5：vividness 量表跨研究
  - Study 2: F(1, 34) = .75, p > .39（用 1-15 量表）
  - Study 5: p > .64（用 1-7 量表）
  - 作者解读：reviewing photos 本身已抬高 vividness ceiling
  - 我的评估：两研究用了**不同量表**，跨研究合并时**需做测量不变性检验**
```

### 3.3 为什么负面结果必须显式记录

- 综述时反驳"X 效应总是显著"的过强论断
- 暴露作者**未讨论**的局限（老板的"暴露脆弱性"原则）
- 帮助未来研究**做 power analysis**：已知效应量（η²p=.018-.06）

---

## 4. 代码与复现性检查（Code & Reproducibility Check）

**目的**：心理科学的**复制危机**要求每篇论文附**复现性证据**。本节是给"心理科学家"做"研究方法审核"时的**必检清单**。

### 4.1 复现性五要素

| 要素 | 必检 | 范例（Diehl 2026）|
|------|------|-------------------|
| **公开数据** | ⬜ | ✅ `https://researchbox.org/2598&PEER_REVIEW_passcode=DHJZRL` |
| **预注册** | ⬜ | ✅ Studies 3-5：`aspredicted.org/ZT8_67W` / `MQ7_125` / `H7N_L7F` |
| **分析代码** | ⬜ | ❌ 未在论文 / box 链接中明示 |
| **样本量决定** | ⬜ | ⚠️ Studies 3-5 用了**subject pool allocation**（max=200/400），**非 power analysis** |
| **排除规则 preregistered** | ⬜ | ✅ 在 box 链接中明示 |
| **材料（stimuli）公开** | ⬕ | ⚠️ Figure 1 的照片需作者授权 |
| **软件版本** | ⬜ | ✅ SPSS 28（统一） |

### 4.2 检查流程

```bash
# 1. 找研究 box / OSF / aspredicted 链接（多数现代论文都有）
grep -E "researchbox|aspredicted|osf\.io|data\.mentoi" <pdf>

# 2. 找样本量决定方式（power analysis / rule of thumb / pool allocation）
grep -iE "power|sample size|subject pool|determined by" <pdf>

# 3. 找软件 + 版本
grep -iE "SPSS|R version|jamovi|JASP|python|Rstudio" <pdf>
```

### 4.3 复现性评级（输出到 source summary 的"待确认"项）

| 评级 | 标准 |
|------|------|
| **A. 完全可复现** | 数据 + 代码 + preregistration + 材料全部公开 |
| **B. 基本可复现** | 数据 + preregistration 公开，代码未公开 |
| **C. 难以复现** | 仅 preregistration 或仅有数据 |
| **D. 不可复现** | 无任何公开材料（**对 2020 年后 APA 期刊罕见**） |

**老板的默认**：综述引用时**只引用 A/B 级**研究；C/D 级研究**在脚注注明**，不作为关键证据。

---

## 5. 与同领域论文对比（Cross-Paper Comparison）

**目的**：任何一篇论文都不是孤岛——必须放在**文献树**中理解。

### 5.1 文献树的三个维度

```
            [本文]
           /  |  \
   引用前序  平行对照  后续延伸
   (前序工作) (同主题竞争) (新发现)
```

| 维度 | 必找 |
|------|------|
| **前序工作** | 本文作者**自己**之前的相关论文（"Building on..."） |
| **平行对照** | 同主题**竞争流派**（"In contrast, X et al. found..."） |
| **后续延伸** | 本文发表后**引用本文**的关键论文（截至阅读时） |

### 5.2 检索方法

| 检索源 | 用途 | 工具 |
|--------|------|------|
| **Semantic Scholar** | 引用网络（谁引了本文）| API + paperId |
| **Google Scholar** | 引用网络（更全）+ "Cited by" | 手动 |
| **Connected Papers** | 视觉化相关论文图 | connectedpapers.com |
| **OpenAlex** | 引用数据 + 概念 | API |

### 5.3 必做：建一份"同主题论文清单"

老板研究主线（数字化存储与自传体记忆）的论文清单范例（部分）：

```markdown
## 数字痕迹—记忆视角 主题论文链

### 综述层
- Hutmacher & Schramm (2026). Scrolling through the past. In-Mind Magazine.
- Dombrowski & Zhang (2026). 综述评论. in-mind.org.

### 实证层
- King, Panjwani & St. Jacques (2024). When having photographs of events influences the visual perspective of autobiographical memories. *Applied Cognitive Psychology*.
- Diehl, Barasch, Ko & Zauberman (2026). Captured memories. *JARMAC*.

### 前序方法学
- Barasch, Diehl, Silverman & Zauberman (2017). Photographic Memory. *Psychological Science*.
- Diehl, Zauberman & Barasch (2016). How taking photos increases enjoyment of experiences. *JPSP*.

### 经典理论
- Nigro & Neisser (1983). Point of view in personal memories.
- Libby & Eibach (2011). Visual perspective in mental imagery.
- Butler et al. (2016). Visual imagery in autobiographical memory.
```

### 5.4 综述中的"对比维度"

| 维度 | 必对比 |
|------|--------|
| **样本** | N、年龄、文化背景 |
| **设计** | 现场 vs 在线、横截面 vs 纵向、预注册 vs 探索性 |
| **关键变量** | 操纵的"X"是什么？因变量的"视角"怎么测？ |
| **核心发现方向** | 一致 vs 矛盾 |
| **效应量** | η²p / d / r 直接比较 |

---

## 6. 写笔记中"待确认项"的规范

**目的**：暴露脆弱性是 source summary 模板的明文要求。本节规范**何时记录、记录什么、如何处理**。

### 6.1 待确认的 4 个子类

| 子类 | 定义 | 处理方式 |
|------|------|----------|
| **A. 数字层面** | 样本量太小、量表跨研究不一致、效应量 CI 过宽 | 综述引用时**加注脚**或**讨论局限** |
| **B. 解读分歧** | 作者解读 vs 我的评估 / 与其他文献的解读冲突 | **写明**"X 解读 vs Y 解读" + 我的取舍依据 |
| **C. 引用位置犹豫** | 不知道这篇该进综述的哪一节、影响哪个 wikilink | **写明候选位置**，请老板拍板 |
| **D. 老板拍板事项** | 需要老板研究主线（X 项目）的特定决策 | 标 `[@老板]` trigger |

### 6.2 必填字段格式

```markdown
- [ ] **[子类]** [具体疑点]
  - **细节**：[完整数据 / 引用 / 链接]
  - **影响**：[如果误判会怎样]
  - **候选方案**：[A / B / C 各自的处理思路]
```

### 6.3 范例（Diehl 2026 实战）

```markdown
- [ ] **[A. 数字层面]** vividness 跨研究量表不一致
  - **细节**：Study 2 用 1-15 Likert，Study 5 用 1-7 Likert
  - **影响**：跨研究合并分析会失真
  - **候选方案**：(A) 仅在每个研究内报告，不合并；(B) 做 measurement invariance 检验后合并

- [ ] **[B. 解读分歧]** Study 2 流失率解读
  - **细节**：7 个月后从 102 → 46（45% 流失率），作者说"we did not find any significant differences in response rate between conditions"
  - **影响**：流失率本身偏高，结论**对坚持参与者**而非全样本
  - **候选方案**：(A) 接受作者判断；(B) 用 Heckman selection model 重分析

- [ ] **[D. 老板拍板]** 是否在 syntheses 笔记中专门讨论 King 2024
  - **细节**：King 2024 是本文的引用率最高的"对话 partner"（截至 2026-06 引用 3 次）
  - **影响**：决定 syntheses 的论证重心（是聚焦机制证据还是聚焦"从相关到因果"链）
  - **候选方案**：(A) 在 syntheses 单设一节；(B) 嵌入"前序工作"小节
```

### 6.4 "待确认"的处理边界

| 该记录的 | 不该记录的 |
|----------|------------|
| 数据/方法学的**具体疑点** | "文章写得不错"（主观评价） |
| 跨研究**可量化的矛盾** | "读起来有点累"（体验评价） |
| 引用位置的**具体候选** | "老板可能不同意"（揣测） |
| 老板**研究主线相关的决策** | "心理学界可能不认可"（行业揣测） |

---

## 7. 完整流水线（End-to-End Pipeline）

老板研究主线（"数字化存储与自传体记忆"项目）单篇论文的完整阅读流程：

```
Step 1: 阅读前清单（5 分钟）
  ├─ 读什么（DOI/位置/类型/作者机构）
  ├─ 为什么读（与研究主线的连接点）
  └─ 预期产出（1-3 句话）

Step 2: 第一遍鸟瞰（5-10 分钟）
  ├─ 读 abstract / intro / discussion 首段
  └─ 判断：值得细读吗？属于哪类贡献？

Step 3: 第二遍细读（30-40 分钟）
  ├─ pdftotext 提取全文
  ├─ 抓所有方法学字段
  ├─ 建跨研究方法+结果表
  └─ 标记所有 p 值显著性

Step 4: 负面结果记录（10 分钟）
  ├─ 分类：推翻假设 / 边缘显著 / 探索性负面
  └─ 记录：统计量 + 作者解读 + 我的评估

Step 5: 复现性检查（5 分钟）
  ├─ 找研究 box / OSF / aspredicted
  ├─ 评级：A / B / C / D
  └─ 输出到 source summary 的"待确认"项

Step 6: 与同领域论文对比（15 分钟）
  ├─ 建文献树（前序 / 平行 / 后续）
  ├─ 检索 Semantic Scholar "Cited by"
  └─ 列出 5 维度对比

Step 7: 第三遍精读 + 写笔记大纲（30-60 分钟）
  ├─ 一句话总结（30-80 字）
  ├─ 关键内容 bullet（3-7 条）
  ├─ 影响到的页面（0-N 个 wikilink）
  └─ 待确认（暴露脆弱性，0-N 条）

Step 8: 写 source summary（15-30 分钟）
  └─ sources/<name>.md（按 _template_source_summary.md 模板）

Step 9: （可选）写 syntheses 笔记（30-60 分钟）
  └─ syntheses/<date>-<title>.md（综合分析）

总耗时：约 1.5-3 小时/篇（10 页标准论文）
```

---

## 8. 工具与模板

### 8.1 PDF 提取工具

```bash
# 提取全文到 txt
pdftotext <pdf> /tmp/output.txt

# 验证页数和元数据
pdfinfo <pdf>

# 按页提取（用于大文件分页）
pdftotext -l 1 <pdf> /tmp/page1.txt
pdftotext -f 2 -l 5 <pdf> /tmp/page2-5.txt
```

### 8.2 wikilink 引用规范

| 类型 | 格式 | 范例 |
|------|------|------|
| 同 vault 页面 | `[[syntheses/...]]` | `[[syntheses/2026-06-05-...-Diehl-2026]]` |
| 表格内 wikilink（需转义管道符） | `[[syntheses/...\|入口]]` | `[[sources/index\|入口]]` |
| raw 文件 | `[raw/.../file.pdf](<relative-path>)` | `[Diehl 2026 PDF](../../raw/papers/2026-06-05_Diehl-et-al_...pdf)` |
| 外部 DOI | `[10.1037/mac0000231](https://doi.org/10.1037/mac0000231)` | — |

### 8.3 模板清单

- **source summary 模板**：`wiki/sources/_template_source_summary.md`（4 字段：总结/关键/影响页面/待确认）
- **syntheses 命名约定**：`YYYY-MM-DD-HH-MM-SS-标题.md`（17 字符紧凑时间戳）
- **vault 架构原则**：见 `wiki/AGENTS.md`（6 个核心目录 + 写入规则）

### 8.4 检索 API 速查

| 用途 | 工具 | 调用 |
|------|------|------|
| 引文元数据（DOI→title/authors/year/venue）| CrossRef | `curl api.crossref.org/works/<doi>` |
| 摘要 + TLDR + 引用网络 | Semantic Scholar | `curl api.semanticscholar.org/graph/v1/paper/DOI:<doi>?fields=...` |
| 全文兜底 | Tavily / Sci-Hub | `tavily_search` / `scihub-paper-downloader.py` |
| OA 链接 | Unpaywall | `curl api.unpaywall.org/v2/<doi>?email=<mail>` |

---

## 9. 自我审查清单（Self-Review Checklist）

写完 source summary / syntheses 笔记后**自查**：

| 维度 | 必查 |
|------|------|
| **真实性** | 数字、引用、DOI 都已二次核验？未编造未文献？ |
| **完整性** | 5 个研究都覆盖了？Table 1 抓了？Figure 描述了？ |
| **可追溯性** | 每个论断都指向具体 source / raw？无 wikilink 断裂？ |
| **脆弱性** | 至少 3 条"待确认"？含数字层面 + 解读分歧 + 老板拍板？ |
| **简洁性** | 一句话总结 ≤ 80 字？关键内容 ≤ 7 条 bullet？ |
| **跨研究对比** | 至少 3 篇同主题论文已加入 vault 索引？ |
| **可复用性** | 我下次能不能用这个 SOP 复现同样的笔记？ |

---

## 10. 与老板工作流的衔接

| 老板指令类型 | 我该做的 |
|--------------|---------|
| "读这篇" / "介绍这篇" | 跑 Step 1-8（出 source summary）|
| "总结这篇" / "写总结笔记" | 跑 Step 1-9（出 source summary + syntheses）|
| "综述 X 主题" | 先**全面检索**建文献树（Step 6），再批量执行 Step 1-9 |
| "对比 X 和 Y" | Step 6 加深（5 维度对比表），可选 Step 9 写综合笔记 |
| "找一篇关于 X 的" | **只**做 Step 2 鸟瞰 → 给老板 1-2 篇候选 → 等老板定 → 再走完整流水线 |

---

## 11. 失败模式（Failure Modes to Avoid）

| 反模式 | 后果 | 正确做法 |
|--------|------|---------|
| **跳过 Step 1 直读 PDF** | 读完不知"为什么读" | 严格走 5 分钟阅读前清单 |
| **第二遍只读 positive results** | 综述时漏掉反证 | 强制 Step 4 负面结果记录 |
| **source summary 写成 abstract 复述** | 失去"主观提炼"价值 | 严格按模板 4 字段，每字段独立信息 |
| **syntheses 直接引用 raw 不经 source** | 违反 vault 流向规则 | 强制 raw → sources → syntheses 路径 |
| **"待确认"只写 1 条凑数** | 暴露脆弱性不足 | 至少 3 条，含 4 个子类 |
| **5 个研究只读 1 个** | 综述结论不稳健 | 第二遍必须覆盖**所有**研究 |
| **DOI / 数字抄错** | 真实性违规 | 全部数字与 PDF 二次核验 |
| **未找前序/后续** | 失去文献树定位 | 强制 Step 6 找对话 partner |

---

## 版本历史

| 版本 | 日期 | 更新 | 作者 |
|------|------|------|------|
| v1.0 | 2026-06-05 | 初版（沉淀自 Diehl et al. 2026 JARMAC 论文阅读实战：杨权 15:51 指令）| 心理学家（psychologist）|
