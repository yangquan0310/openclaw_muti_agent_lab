# PRISMA Systematic Review SOP（v5.21.0 新增）

> 来源：吸收 Academic Research Skills（ARS）Deep Research 的 13-agent + Socratic + PRISMA 思路  
> 用途：当 `synthesize` 需要"系统综述"（区别于"快速综述/narrative review"）时调用  
> 落地：写到 `wiki/reports/<date>-prisma-<topic>.md` + `wiki/syntheses/<date>-systematic-review-<topic>.md`

---

## 🎯 触发条件

| 触发短语 | 中文 |
|---|---|
| "systematic review" | "系统综述" |
| "PRISMA" | "系统筛选" |
| "meta-analysis" | "元分析" |
| "需要严格筛选证据" | "用 PRISMA 流程跑一下" |

**不触发**：单纯 narrative review、scoping review、rapid review（用现有 synthesize 即可）。

---

## 📋 9 阶段流程（ARS Deep Research 思路）

### Stage 1：PICO 拆解

把研究问题拆为：
- **P**opulation（人群/对象）
- **I**ntervention（干预/暴露）
- **C**omparator（对照）
- **O**utcome（结局）

**输出**：`wiki/concepts/<date>-pico-<topic>.md`（PICO 表）

### Stage 2：数据库检索（多源）

| 数据源 | 工具 | 输出 |
|---|---|---|
| Semantic Scholar | `WikiSearchReport` | papers_count + 引用图 |
| CrossRef | API | DOI 验证 |
| CNKI / Scholar | jina-ai/exa 补充 | 中文文献 |
| arXiv | API | 预印本 |
| Zotero 库 | `WikiZoteroManager.find_missing_zotero_keys()` | 已有但未纳入的文献 |

**输出**：每源一个 `cache/<source>-raw.json` + 一个合并去重的 `cache/deduped.json`

### Stage 3：去重 + 标题/摘要筛选

- **去重**：DOI + title fuzzy match
- **筛选标准**：标题/摘要是否符合 PICO
- **记录**：每个排除的 paper 必须有**排除理由**

**输出**：`cache/screening-title-abstract.csv`（含 include/exclude 标签 + 理由）

### Stage 4：全文筛选

- 读全文（PDF → markdown via markitdown）
- 二次筛选：研究设计/样本量/方法学质量
- 排除理由：非原始研究/无对照组/数据不全/语言不符

**输出**：`cache/screening-fulltext.csv`

### Stage 5：数据抽取

按 PRISMA-Data 模板抽：
- 作者/年份/国家
- 研究设计（RCT/队列/横断面…）
- 样本量
- 干预/暴露细节
- 结局指标（含 effect size + CI）
- 偏倚评估（Cochrane RoB 2.0 / ROBINS-I）

**输出**：`wiki/reports/<date>-prisma-extraction-<topic>.md`（每个 study 一节）

### Stage 6：偏倚评估

- RCT：Cochrane Risk of Bias 2.0
- 非 RCT：ROBINS-I
- 观察性：Newcastle-Ottawa Scale

**输出**：每研究一个 `cache/bias-<study-id>.json`

### Stage 7：PRISMA 流程图（必出）

```
Identification → Screening → Eligibility → Included
   ↓             ↓             ↓            ↓
Records from   Records after  Full-text   Studies in
 databases     deduplication  assessed    synthesis
 (n=X)         (n=Y)          (n=Z)       (n=N)
                               Excluded
                               with reasons
                               (n=Z-N)
```

**输出**：`wiki/reports/<date>-prisma-flow-<topic>.md`（含 mermaid 图 + 数字）

### Stage 8：证据综合

二选一：
- **Meta-analysis**：fixed/random effects model + forest plot + I² 异质性
- **Narrative synthesis**：按主题/方法学分组对比

**输出**：`wiki/syntheses/<date>-systematic-review-<topic>.md`

### Stage 9：GRADE 评级（可选）

- 证据质量：High / Moderate / Low / Very Low
- 5 因素降级：偏倚/不一致/间接性/不精确/发表偏倚
- 3 因素升级（观察性）：大效应/剂量反应/残余混杂

**输出**：合成文档末尾 GRADE Summary of Findings 表

---

## 🛠️ 工作流（与 research-assistant 模块对应）

| 阶段 | 用什么模块 |
|---|---|
| 1 PICO | `wiki/concepts/` 手写 + 模板 |
| 2 检索 | `search --queries <PICO.json>` |
| 3 筛选 | 人工 + `WikiZoteroManager.list_wiki_sources()` 辅助 |
| 4 全文 | `download --zotero-key` 拉 PDF → markitdown 转 md |
| 5-6 抽取 | 人工 + `wiki/sources/<id>.md` YAML 字段 |
| 7 流程图 | mermaid + 模板 |
| 8 综合 | `synthesize extract` + `synthesize check` |
| 9 GRADE | 模板 + 人工评级 |

---

## ⚠️ 边界条件

| 不要做 | 原因 |
|---|---|
| ❌ 不要替用户拍 PICO | 用户的研究问题由用户决定 |
| ❌ 不要自动排除文献 | 每个排除必须有理由 + 留痕 |
| ❌ 不要省略 PRISMA 流程图 | PRISMA 强制要求 |
| ❌ 不要 1 轮跑完 9 阶段 | 每阶段结果用户核验后再进下一阶段 |
| ❌ 不要把 PRISMA 当 narrative review 跑 | PRISMA 严格筛选 ≠ 快速综述 |

---

## 📤 产出物清单（最终交付）

```
wiki/
├── concepts/<date>-pico-<topic>.md            # Stage 1
├── reports/<date>-prisma-flow-<topic>.md      # Stage 7（必出）
├── reports/<date>-prisma-extraction-<topic>.md # Stage 5-6
└── syntheses/<date>-systematic-review-<topic>.md # Stage 8-9
```

---

## 📚 参考

- PRISMA 2020 Statement：https://www.prisma-statement.org/
- Cochrane Handbook for Systematic Reviews of Interventions
- GRADE Handbook：https://gdt.gradepro.org/app/handbook/handbook.html
- 来源 ARS Deep Research skill：https://github.com/Imbad0202/academic-research-skills

---

*最后更新：2026-06-22 v5.21.0*  
*来源借鉴：ARS Deep Research（Imbad0202/academic-research-skills）*