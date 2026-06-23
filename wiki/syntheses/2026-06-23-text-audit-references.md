# references/ 文字内容审计报告（18 个文件）

> **审计对象**：`/root/.openclaw/skills/research-assistant/references/` 下 18 个 .md 文件
> **审计时间**：2026-06-23 22:25 GMT+8
> **审计范围**：仅文字内容质量
> **总体规模**：18 文件 / 2988 行 / ~110KB

---

## 一、文件清单 + 单文件评分

| # | 文件 | 行数 | KB | 单文件评分 | 类别 |
|---|------|------|------|------|------|
| 1 | index.md | 103 | 6.6 | 76 | 索引 |
| 2 | research-workflow.md | 80 | 2.2 | 88 | 工作流 |
| 3 | apaquarto-manuscript-guide.md | 260 | 8.3 | 92 | 排版指南 |
| 4 | module-search.md | 140 | 4.0 | 85 | 模块指南 |
| 5 | module-manage.md | 51 | 2.0 | 70 | 模块指南 |
| 6 | module-maintain.md | 170 | 7.1 | 80 | 模块指南 |
| 7 | module-summarize.md | 118 | 3.8 | 78 | 模块指南 |
| 8 | module-synthesize.md | 59 | 2.0 | 82 | 模块指南 |
| 9 | module-download.md | 200 | 6.2 | 80 | 模块指南 |
| 10 | module-upload.md | 156 | 5.6 | 85 | 模块指南 |
| 11 | narrative-review-guide.md | 225 | 8.8 | 90 | 文体指南 |
| 12 | meta-analysis-guide.md | 264 | 8.4 | 91 | 文体指南 |
| 13 | observational-study-guide.md | 196 | 6.9 | 87 | 文体指南 |
| 14 | experimental-study-guide.md | 242 | 7.7 | 88 | 文体指南 |
| 15 | prisma-workflow.md | 165 | 5.7 | 86 | 工作流 SOP |
| 16 | apa7-standards.md | 198 | 6.8 | 89 | 标准清单 |
| 17 | originality-standards.md | 170 | 6.1 | 87 | 标准清单 |
| 18 | manuscript-audit-standards.md | 191 | 6.6 | 85 | 标准清单 |

**整体评分**（加权平均）：**84.5 / 100**

| 维度 | 平均分 | 区间 |
|------|--------|------|
| A. 中文表达质量（30） | **25.4** | 22-28 |
| B. 信息密度（20） | **17.0** | 14-19 |
| C. 结构清晰度（20） | **17.3** | 14-19 |
| D. 一致性（20） | **16.2** | 12-18 |
| E. 用户友好度（10） | **8.6** | 7-10 |

---

## 二、各维度审计

### A. 中文表达质量（平均 25.4 / 30）

#### 跨文件优点

1. **文体指南（narrative / meta / observational / experimental）** 中文流畅度最佳：
   - 4 文件用同一段落模板（"何时撰写" → "YAML 头" → "标准结构" → "实战要点" → "参考文献"）
   - 章节标题用名词短语 + 学术术语（如"效应量 / 异质性 / 偏倚"）
   - 标点用全角中文逗号 / 句号 + 半角数字混排——规范统一

2. **apaquarto-manuscript-guide.md** 是 18 文件中文字最精致的：
   - 章节标题用数字 + 名词（"1. 何时使用范式 ④"）
   - 每节先说"是什么"再讲"为什么"再给"怎么做"——逻辑链清晰

3. **prisma-workflow.md** 流程描述准确：
   - "PICO 拆解 / 数据库检索 / 去重 / 全文筛选 / 数据抽取 / 偏倚评估 / PRISMA 流程图 / 证据综合 / GRADE 评级" 9 阶段——动词开头，平行工整

#### 跨文件问题

1. **module-*.md 6 个文件** 风格不一致：
   - module-search.md / module-summarize.md 用"## 一、" / "## 二、"中文数字
   - module-manage.md 用"## 一、Manager" / "## 二、WikiZoteroManager" 数字+标题
   - module-maintain.md 用"## 一、维护对象" / "## 二、维护操作" / "## 三、维护操作" — **"二、维护操作"和"三、维护操作"重名！**
   - module-upload.md 用"## 一、能力" / "## 二、CLI 用法" — 中文数字+名词

2. **表述口语化**（出现在多文件）：
   - "攥写笔记"（module-summarize.md / module-upload.md / module-synthesize.md 多处）——"攥写"是动词口语化，建议统一为"撰写"
   - "工具不攥写 narrative"（SKILL.md / module-summarize.md / module-upload.md 多处）——半中半英，LLM 视角不友好

3. **module-manage.md / module-synthesize.md 篇幅过短**（51 / 59 行）：
   - 内容确实简单（4 方法 / 1 方法），但作为"使用指南"缺少实战示例 + 常见错误段
   - 建议：补"实战示例" + "常见错误"段（与 module-search.md 看齐）

#### 改进建议

- module-*.md 统一章节编号风格——建议全部用 `## 1.` / `## 2.` 半角数字（apaquarto-manuscript-guide.md 范式）
- "攥写" 全部替换为 "撰写"
- module-manage.md / module-synthesize.md 各补 1 段"实战示例"

---

### B. 信息密度（平均 17.0 / 20）

#### 跨文件优点

1. **文体指南（4 文件）** 信息密度最佳：
   - 章节结构平行（"何时撰写 / YAML 头 / 标准结构 / 引用语法 / 实战要点 / 关键参考文献 / 版本历史"）
   - 每节都有具体动作（"✅ 简明描述研究 + 主要变量"），新人可立即执行

2. **3 个 standards（apa7 / originality / manuscript-audit）** 信息密度合理：
   - 每文件都是"核心规则 + N 项 checklist + 自动化辅助 + 边界条件 + 参考"5 段
   - checklist 项目数合理（50 / 30 / 60）

#### 跨文件问题

1. **重复信息多**：
   - 引用语法（`[@key]` 表格）在 4 文体指南 + apaquarto + apa7-standards 6 个文件重复出现——每个文件独立完整，但维护成本高
   - YAML 头模板在 4 文体指南 + apaquarto 5 个文件重复——同上
   - 建议：抽取"引用语法 + YAML 头"为单独 `references/_common-templates.md`，5 文件引用之

2. **research-workflow.md 太短**（80 行）：
   - 工作流 5 阶段本应是核心文档，但内容比 module-search.md 还薄
   - 缺"实战示例 / 常见错误 / 工具对应表"
   - 建议：补 1 段"5 阶段工具对应表"（阶段 → 模块 → CLI 命令）+ 1 段"实战要点"

3. **module-maintain.md 篇幅过长且有"## 二、"和"## 三、"重名段**：
   - 170 行 / 7.1KB——比 module-search.md 还厚
   - 但内容集中在"维护对象 / 维护操作 / WikiZoteroManager"三块，重复度高
   - 建议：合并重名段，删除冗余

4. **index.md 信息密度低**：
   - 103 行但 ~30 行是 workboard tracker（v5-roadmap 状态）
   - 建议：workboard tracker 移到 `wiki/syntheses/` 单独文档

#### 改进建议

- 抽取共用模板（引用语法 / YAML 头）为 1 个 `_common-templates.md`
- research-workflow.md 补"5 阶段工具对应表"
- module-maintain.md 重名段合并
- index.md 的 workboard tracker 段独立

---

### C. 结构清晰度（平均 17.3 / 20）

#### 跨文件优点

1. **apaquarto-manuscript-guide.md** 结构最完整：
   - 1-9 编号章节，每章节标题用动词 / 名词
   - 每个 H3 有 1 段说明 + 1 段示例 + 1 段提示——"3 段式"统一

2. **3 个 standards（apa7 / originality / manuscript-audit）** 结构统一：
   - "🎯 核心规则 / 📋 N 项 Checklist / 🔧 自动化辅助 / ⚠️ 边界条件 / 📚 参考"5 段模板

3. **4 文体指南** 结构几乎完全平行——易于对比阅读

#### 跨文件问题

1. **module-*.md 6 文件结构不统一**：
   | 文件 | 章节数 | 章节标题风格 |
   |------|--------|-------------|
   | module-search.md | 5 | "## 语言路由原则" + "## 检索引擎选择" + "## 检索条件设计原则" + "## query 语法" + "## 补检索原则（系统级工具）" |
   | module-manage.md | 1 | "## 一、Manager" |
   | module-maintain.md | 6 | "## 一、维护对象" + "## 二、维护操作" + "## 三、维护操作"（重名）+ "## 四、删除记录" + "## 五、数据一致性原则" + "## 六、参考" + "## 二、WikiZoteroManager"（重名）|
   | module-summarize.md | 2 | "## 一、Summarizer" + "## 二、多模态精读" |
   | module-synthesize.md | 1 | "## 一、Synthesizer" |
   | module-download.md | 8 | 无 H2，仅 H3 |
   | module-upload.md | 6 | "## 一、能力" / "## 二、CLI 用法" / "## 三、流水线详情" / "## 四、明确边界" / "## 五、典型工作流" / "## 六、版本历史" |

2. **module-download.md 没有 H2 标题**——直接进 H3"## YAML 头示例"——读者进文件不知道主结构。

3. **module-maintain.md 有 2 个 `## 二、` 重复**（"## 二、维护操作" 和 "## 二、WikiZoteroManager Python 类"）——明显遗漏 H1 或顺序错乱。

#### 改进建议

- module-*.md 6 文件统一 H2 风格（建议"## 核心方法" / "## CLI 用法" / "## 实战要点" / "## 版本历史" 4 段模板）
- module-download.md 顶部加 1 个 H2 标题（如"## PDF 下载模块使用指南"）
- module-maintain.md 修复重名段

---

### D. 一致性（平均 16.2 / 20）

#### 关键不一致点

1. **模块数不一致（与 SKILL.md / README 三方不一致）**：
   - SKILL.md "7 模块 CLI"：search / download / upload / summarize / synthesize / manage / maintain
   - README 七大功能：检索 / 保存到 Zotero / 管理 WebDAV / 管理 wiki / 精读 / 攥写 / 排版
   - references/ 有 7 个 module-*.md（search / manage / maintain / summarize / synthesize / download / upload）——与 SKILL.md 一致
   - **references/ 与 SKILL.md 一致，但与 README 视角不同**

2. **index.md 与各 module-*.md 的模块描述不一致**：
   - index.md "管理模块"段：`Manager（v5.16.0+ 走 wiki，按 zotero_item_key 去重）`——是 `Manager.py`
   - 但 module-maintain.md 实际是 `WikiZoteroManager`——index.md 描述简略
   - 建议：index.md 各模块描述加 1 句"`scripts/<dir>/<Class>.py` 类名 + 行数"

3. **术语不统一**：
   - "攥写 / 撰写 / 写作 / 写" 4 种说法在 references 多文件混用
   - "工具不替代 agent" vs "工具不攥写 narrative"——同一原则两种说法（SKILL.md / module-summarize.md / module-upload.md）
   - "wiki 后端 / 三联动"——同一概念两种说法（research-workflow.md / index.md）

4. **版本号标注风格不统一**：
   - index.md 章节标注：`WikiZoteroManager（v6.0.6+ 单一入口，Maintainer.py 已删）`
   - module-search.md：`ZoteroSearcher / ZoteroAdder（v5.15.0 新增）`
   - module-summarize.md：`Summarizer（v5.16.0+ wiki 版本，规则版）`
   - **标注逻辑不统一**——"vX.Y.Z 新增" / "vX.Y.Z+ 可用" / "vX.Y.Z 单一入口"混用

5. **目录结构 vs SKILL.md 不一致**：
   - SKILL.md `scripts/` 子目录：search / summarize / synthesize / download / manage / maintain（**6 个**）
   - README `scripts/` 子目录：search / summarize / synthesize / download / manage / maintain（**6 个**）
   - 实际 `scripts/` 下有 **upload/ 子目录**（v6.0.3 新增）
   - **两边都没列 upload/ 子目录**——references/module-upload.md 实际指向 `scripts/upload/Uploader.py`——三方不一致

#### 改进建议

- 术语统一：选定"撰写 / 工具不替代 agent / 三联动"——其他替换
- 版本号标注规范化：`(vX.Y.Z+ 表示可用版本)` / `(vX.Y.Z 引入)` / `(vX.Y.Z 替换)` 三种标注
- SKILL.md / README 的 `scripts/` 子目录补 upload/ 第 7 项

---

### E. 用户友好度（平均 8.6 / 10）

#### 跨文件优点

1. **apaquarto-manuscript-guide.md** 实战要点表 + 踩坑记录表——新人排错最快
2. **3 个 standards** 的 checklist 表格——可打印做核验单
3. **module-upload.md "典型工作流（agent 视角）"段**——5 步走完，新人能跟

#### 跨文件问题

1. **index.md 不友好**：
   - 没有"按场景查找"提示——读者得自己翻 103 行找模块
   - 实际上 index.md 有"按场景查找"段，但**位置在文件末尾**——读者进来第一眼看不到
   - 建议：把"按场景查找"移到顶部

2. **module-search.md / module-summarize.md** 的"## 补检索原则"段对新人理解成本高：
   - "jina-ai / Exa / Tavily" 3 个工具同时出现，无前后文
   - 建议：补 1 段"什么是 jina-ai / Exa / Tavily"

3. **4 文体指南** 没有"我应该选哪个文体"提示——读者可能不知道 narrative review 和 meta-analysis 的区别：
   - 建议：在 index.md 或 4 文体指南顶部加 1 张"文体选择决策表"

#### 改进建议

- index.md "按场景查找"段移到顶部
- module-search.md / module-summarize.md "补检索"段加 1 句话介绍工具
- 4 文体指南顶部加 1 张"文体选择决策表"

---

## 三、跨文件 Top 10 修复清单

| # | 修复点 | 涉及文件 | 严重度 |
|---|--------|---------|--------|
| 1 | "攥写" → "撰写" | module-summarize / synthesize / upload + SKILL.md | 🟡 术语统一 |
| 2 | "工具不攥写 narrative" → "工具不替代 agent" | module-summarize + SKILL.md | 🟡 术语统一 |
| 3 | module-maintain.md 重名段（"## 二、" x 2）合并 | module-maintain | 🔴 结构断裂 |
| 4 | module-*.md 章节编号风格统一 | 6 个 module-*.md | 🟠 一致性 |
| 5 | module-download.md 加 1 个 H2 标题 | module-download | 🟠 结构 |
| 6 | references 共用模板（引用语法/YAML 头）抽取 | 5 文件 → 1 文件 | 🟢 维护性 |
| 7 | SKILL.md/README scripts/ 子目录补 upload/ | SKILL.md + README | 🟡 不一致 |
| 8 | index.md "按场景查找" 段移到顶部 | index.md | 🟢 友好度 |
| 9 | 4 文体指南顶部加"文体选择决策表" | 4 文体指南 + index.md | 🟡 友好度 |
| 10 | module-manage / synthesize 各补"实战示例"段 | 2 文件 | 🟢 信息密度 |

---

## 四、Top 3 最佳文件（值得保持 + 推广其范式）

### 🥇 apaquarto-manuscript-guide.md（92 / 100）

**范式亮点**：
- 1-9 编号 H2 章节 + "是什么 / 为什么 / 怎么做" 3 段式 H3
- "踩坑记录" 表是新人最大帮助
- 关键源码文件 / 关键参考文献 段——可追溯

**推广建议**：作为 references/ 写作范式——其他文件照这个模板重构。

### 🥈 meta-analysis-guide.md（91 / 100）

**范式亮点**：
- 章节标题用学术术语（如"效应量 / 异质性 / 发表偏倚 / 敏感性分析 / GRADE"）
- "YAML 头示例"段直接给完整 YAML——可复制即用
- "实战要点" 表 + "心理学元分析常用工具" 表——工具链完整

### 🥉 narrative-review-guide.md（90 / 100）

**范式亮点**：
- "心理学叙述性综述的关键认知"段——把抽象差异说清楚（"可以 post hoc theorizing"）
- SANRA Scale 表——质量评估工具

---

## 五、Top 3 待改进文件

### ⚠️ module-manage.md（70 / 100）

**问题**：
- 51 行 / 2.0KB——最短
- 缺"实战示例 / 常见错误"段
- 与 module-maintain.md 内容重叠（都讲"管理 wiki source 列表"）

**改进建议**：
- 补 1 段"实战示例"（5-10 行 CLI 命令 + 输出示例）
- 与 module-maintain.md 明确分工（module-manage.md 管"列表 / 筛选 / 合并"，module-maintain.md 管"三方一致性 / 漂移检测"）

### ⚠️ module-summarize.md（78 / 100）

**问题**：
- 多模态精读段（## 二）与基础段（## 一）结构差异大
- "未来扩展"段（v5.17.0+ 可加 LLM）——与"严格遵循工具不替代 agent"原则矛盾

**改进建议**：
- 统一 ## 一 / ## 二 结构（都用 H3 子节）
- "未来扩展"段删除或改为"vX.Y.Z TODO"——避免误导

### ⚠️ index.md（76 / 100）

**问题**：
- 18 文件索引但 workboard tracker 段占 ~30 行——比例失衡
- "按场景查找" 段位置在末尾——友好度差

**改进建议**：
- workboard tracker 移到 `wiki/syntheses/` 单独文档
- "按场景查找" 段移到顶部

---

*审计完成时间：2026-06-23 22:35 GMT+8*
*审计者：writer subagent*
*下次审计建议：v6.1.0 发布前复审 + 模块新增时同步评估*
