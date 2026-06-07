---
name: writer
description: >
  writer 实践技能。触发: 写作/撰写/起草/编辑/修改/润色论文/文章/报告/文档/方案/说明;学术写作(摘要/综述/大纲/致谢);论文排版与编译(Quarto + apaquarto 5.0.18 排版 APA 7th 论文 PDF);翻译写作(中译英/英译中)。通用写作 + Quarto 排版,v2.2.0 集成。
version: 2.2.0
author: Yang Quan
metadata:
  openclaw:
    emoji: ✍️
    requires: []
---

# writer（通用写作技能 + Quarto 排版技能）

> **v2.2.0 集成**：老板 2026-06-06 23:14 指令，补充 Quarto + apaquarto 5.0.18 排版 APA 7th 论文 PDF 技能，**写作助手自己**排版，**不**再依赖大管家编译。
> **核心结构**：指南下沉至 references/，模板存放于 assets/templates/，快速检索用 scripts/lookup/

---

## 触发条件

| 场景 | 触发关键词 |
|------|------------|
| 写作任务 | 写、写作、撰写、起草、编辑、修改、润色 |
| 论文文章 | 论文、文章、报告、文档、方案、说明 |
| 学术写作 | 摘要、综述、大纲、致谢 |
| **论文排版与编译** | **排版、apaquarto、Quarto、APA 7th、PDF、编译** |
| 翻译写作 | 中译英、英译中、翻译 |

---

## 核心原则

1. **证据优先**：所有主张必须有文献支持，禁止捏造数据
2. **结构驱动**：先搭框架再填内容，结构 > 内容
3. **精准表达**：学术写作要求精确、简洁、客观
4. **检索验证**：遇到陌生主题必须检索，不许凭空编造
5. **🆕 不擅自添加元评论**：论文里**不**应出现"严格采用 X→Y 形式"等**程序性声明**（footer 自检清单、重要声明、关联任务标注、禁用词自查清单）—— 老板 2026-06-06 23:14 反馈"严重不合格"

---

## 边界条件（禁止事项）

| 边界 | 说明 |
|------|------|
| 禁止捏造 | 禁止捏造文献作者、年份、期刊、数据 |
| 禁止臆测 | 禁止"应该是"、"大概如此"等模糊表述 |
| 禁止删除原意 | 修改时不得大幅删改用户原有段落结构和核心论点 |
| 禁止破坏结构 | 禁止删除主题句或破坏论证链完整性 |
| 禁止自我决策 | 执行修改前必须先汇报修改内容并获得确认 |
| **🆕 禁止论文里出现程序性声明** | **"本研究采用 X→Y 形式""严格采用""禁词自查清单"等元评论 —— APA 7 论文规范严重违规，老板 23:14 反馈** |
| **🆕 禁止 §1 用 1.1/1.2/1.3 三个 subsection** | **老板 23:14 反馈"§1 不需要三个 1.1、1.2、1.3 节标题" —— 改连续段落，3 意群融入无 heading 段落** |
| **🆕 禁止"X 通过 M 影响 Y"类中介措辞** | **APA 7 论文规范 + 老板 23:14 反馈"不构建中介"** |

---

## 核心理念

> **证据 > 推测 > 观点**，**结构 > 内容**，**精准 > 冗余**，**正文 > 元评论**

| 层级 | 核心 |
|------|------|
| **证据层** | 可验证的实证结果，必有引用 |
| **推测层** | 对证据的解释，归因到研究者 |
| **观点层** | 本研究对证据的解读，弱语气 |
| **🆕 正文体层** | 论文正文是**学术论述**，**不**是**元评论**（不写"严格采用 xxx"） |

---

## 五阶段工作流（写作）

```
阶段1: 理解任务 → 阶段2: 规划 → 阶段3: 起草 → 阶段4: 修改 → 阶段5: 校对
```

每个阶段有明确的输入、输出和必读指南。

### 阶段1: 理解任务

**输入**：写作任务描述
**输出**：任务分解（主题 / 限制 / 指令词 / 边界）

**必读指南**：`references/workflows/writing-process-workflow.md` 第1节

### 阶段2: 规划

**输入**：任务分解
**输出**：论证结构（核心论点 + 子论点 + 证据 + 潜在反驳）

**必读指南**:
- `references/workflows/writing-process-workflow.md` 第2节
- `references/guides/writing-principles-guide.md`

### 阶段3: 起草

**输入**：论证结构
**输出**：初稿

**必读指南**:
- `references/standards/sentence-standards.md` — 每句主语明确、动词精确
- `references/standards/paragraph-standards.md` — 主题句统领、论证链清晰
- `references/standards/chapter-standards.md` — 引言-主体-结论闭环
- `references/guides/academic-style-guide.md` — 清晰/简洁/客观/中立
- **🆕 起草时禁写"严格采用 xxx"等程序性声明**（老板 23:14 反馈）

### 阶段4: 修改

**输入**：初稿
**输出**：修改清单 → 逐章执行 → 终稿

**必读指南**:
- `references/workflows/modification-workflow.md` — 修改方法论（建立论证地图→修改清单→汇报确认→执行→核查）
- `references/guides/evidence-layers-guide.md` — 证据-推测-解读三层区分
- `references/standards/style-standards.md` — 术语管理、禁用词表
- `references/standards/citation-standards.md` — 引用格式规范
- `references/guides/editing-proofreading-guide.md` — 句子/段落/语言润色检查
- **🆕 重点核查"严格采用 xxx"类元评论 / 关联任务标注 / 禁用词自查清单**—— **全删**（老板 23:14 反馈）

**修改优先级**:
| 优先级 | 类型 |
|--------|------|
| P0 | 术语清洗 |
| P1 | 引用修复 |
| P2 | 图表编号 |
| P3 | 逻辑深度 · 段落结构 |
| P4 | 终极核查 |
| **🆕 P0** | **删所有"严格采用 xxx"程序性声明 + footer 自检清单 + 关联任务标注** |

### 阶段5: 校对

**输入**：终稿
**输出**：提交稿

**必读指南**:
- `references/guides/editing-proofreading-guide.md` 第9节 — 格式/引用/数字校对
- `references/standards/citation-standards.md` — 确保每条引用有对应参考文献
- `references/guides/ai-writing-guide.md` — 消除AI写作模式

---

## 🆕 阶段 6: 排版与编译（Quarto + apaquarto 5.0.18）

> **v2.2.0 新增**（2026-06-06 老板指令）：写作助手**自己**用 Quarto 排版 APA 7th 论文 PDF，**不**再依赖大管家编译。
> **老板 v1.2 决策**：论文项目默认范式 ④ apaquarto（替代旧 Pandoc 流程）。

### 阶段 6.1: 4 件套（apaquarto 5.0.18）

| 套件 | 位置 | 说明 |
|------|------|------|
| 1. 项目根 `_quarto.yml` | 项目根 | 空壳 + `type: default` |
| 2. `_extensions/apaquarto/` | 项目根 | `quarto add wjschne/apaquarto` 装扩展（项目级）|
| 3. `manuscripts/header.tex` | manuscripts/ | 项目级 CJK 字体（覆盖 apaquarto 默认）|
| 4. `manuscripts/references.bib` | manuscripts/ | APA 7th BibTeX（apaquarto 5.0.18 接受此位置）|

### 阶段 6.2: 5 步编译流程

1. **复制终稿到 `manuscripts/`**（如 `xxx_CFPPS_初稿_v3.md`）
2. **前加 YAML 头**（apaquarto 格式 — 见 `references/standards/quarto-yaml-standards.md`）
3. **建 `manuscripts/header.tex`**（CJK 字体 AR PL SungtiL GB — 见 `references/standards/quarto-cjk-font-standards.md`）
4. **建 `manuscripts/references.bib`**（APA 7th BibTeX）
5. **编译**：`quarto render manuscripts/xxx.md --to apaquarto-pdf --output-dir docs/`

### 阶段 6.3: 5 步关键修复（踩坑必备）

1. **装 R 环境** — apaquarto 5.0.18 要 R+knitr（`export PATH=/root/.conda/envs/r-base/bin:/root/.TinyTeX/bin/x86-64-linux:$PATH`）
2. **建项目根 _quarto.yml** — 空壳 + `type: default`
3. **装 apaquarto 扩展（项目级）** — `quarto add wjschne/apaquarto --no-prompt`
4. **.md YAML 头用 `format: apaquarto-pdf:`**（**不**用 `pdf:` 块）
5. **`references.bib` 必须在 `manuscripts/`**（与 .md 同级）

### 阶段 6.4: 常用命令

```bash
# 安装 apaquarto（仅首次）
export PATH=/root/.conda/envs/r-base/bin:/root/.TinyTeX/bin/x86-64-linux:$PATH
cd /项目根
quarto add wjschne/apaquarto --no-prompt

# 编译论文 PDF（用绝对路径，避免 cd 问题）
quarto render /绝对路径/manuscripts/xxx.md \
  --to apaquarto-pdf \
  --output-dir /绝对路径/docs/

# 移动 PDF 到 docs/ 根（Quarto 默认输出在 docs/子目录/）
mv docs/manuscripts/xxx.pdf "docs/论文标题.pdf"
rm -rf docs/manuscripts

# 验证 PDF
pdfinfo "docs/论文标题.pdf"  # 看页数 + Creator + Page size
```

### 阶段 6.5: 5 类常见错误修复

| 错误 | 根因 | 修复 |
|------|------|------|
| `Rscript not found` | R 不在 PATH | `export PATH=/root/.conda/envs/r-base/bin:$PATH` |
| `apaquarto-pdf format not found` | ① 根没 _quarto.yml ② 扩展没装 | `touch _quarto.yml` + `quarto add wjschne/apaquarto` |
| 退回 Pandoc 默认（没 title page）| `.md` 写了 `format: pdf:` 而非 `format: apaquarto-pdf:` | 改 `pdf:` → `apaquarto-pdf:` |
| 没 author note 段 | `author-note:` 字段缺失 | 补 `author-note: disclosures: conflict-of-interest: "..."` |
| 找不到 `references.bib` | bib 不在 .md 同级 | 移到 `manuscripts/`（与 .md 同级）|
| `Error resolving header-includes- unable to open file header.tex` | `include-in-header: "header.tex"` 路径相对 .md 解析 | 把 `header.tex` 复制到 `manuscripts/`（与 .md 同级）|

### 阶段 6.6: CJK 字体配置（root 病）

> **铁律**：用 `AR PL SungtiL GB`（文鼎简报宋），**不**用 Noto CJK SC。
> **根因**：Noto CJK TTC 文件含 5 个 subface（JP/KR/SC/TC/HK），xelatex 默认挑第一个 jp — 嵌入 PDF 元数据显示 `NotoSerifCJKjp`。
> **根治**：换用单 TTF face 字体 `AR PL SungtiL GB`（apt 包 `fonts-arphic-gbsn00lp`）— 嵌入字体元数据 `BousungEG-Light-GB`，**绝对** SC 无歧义。

```latex
% manuscripts/header.tex
\usepackage{xeCJK}
\setCJKmainfont{AR PL SungtiL GB}
\setCJKsansfont{AR PL SungtiL GB}
\setCJKmonofont{AR PL SungtiL GB}
\setmainfont{AR PL SungtiL GB}
\setsansfont{AR PL SungtiL GB}
\setmonofont{AR PL SungtiL GB}

\XeTeXlinebreaklocale "zh"
\XeTeXlinebreakskip = 0pt plus 1pt
\usepackage{xurl}
```

### 阶段 6.7: 老板 23:14 反馈 — APA 7 论文规范违规清单（v3 必避）

> **写作助手**：`v2 → v3` 实战经验，**核心问题不是排版技术**，**是**论文规范违规（写作助手自作主张添加程序性声明）。

| ❌ 老板说**不**该有 | 处理 |
|------------------|------|
| 论文里"严格采用 X→Y"程序性声明 | **删**所有"本研究采用 X→Y 形式"等元评论（footer 自检清单 + 重要声明 + 关联任务标注 + 禁用词自查清单）|
| 摘要/关键词/"Abstract"/"Keywords:" heading 单独成第 3 页 | **删** abstract YAML 字段，或用 `\NoAbstract` 命令，或切到范式 ② |
| §1 引言 §1.1/§1.2/§1.3 三个 subsection | **改连续段落**，3 意群融入**无 heading** 段落 |
| Table 2/3 不规范 | 按数据文件原状 + 完整 APA 7 表格模板 |
| 讨论部分"严格采用 xxx"程序性声明 | **删**，**真正**写学术讨论（分析发现 / 对比文献 / 局限 / 未来）|
| "X 通过 M 影响 Y"类中介措辞 | **删**，改写为 "X 的影响在 M 上得到体现" |

---

## 场景化快速调用

| 场景 | 必读指南 | 禁止行为 |
|------|----------|----------|
| 撰写学术论文 | `guides/academic-style-guide.md` + `standards/citation-standards.md` | 捏造文献数据 |
| 修改润色文章 | `workflows/modification-workflow.md` + `guides/editing-proofreading-guide.md` | 大幅删改原意 |
| 检查写作质量 | `guides/evidence-layers-guide.md` + `standards/sentence-standards.md` | 只看表面错误 |
| 消除AI痕迹 | `guides/ai-writing-guide.md` | 直接删除整段 |
| 中英文论文差异 | `guides/chinese-english-writing-guide.md` | 混用中英文格式 |
| 跨语言翻译写作 | `guides/chinese-english-writing-guide.md` + `standards/citation-standards.md` | 直译不调整结构 |
| **🆕 用 Quarto 排版 APA 7th 论文 PDF** | **本 SKILL §阶段 6 排版与编译 + `standards/quarto-*.md`** | **用 Pandoc / 模板里有"严格采用 xxx"** |
| **🆕 补全 .md 的 YAML 头** | **`standards/quarto-yaml-standards.md`** | **用 `format: pdf:` 而非 `format: apaquarto-pdf:`** |
| **🆕 修 CJK 字体乱码** | **本 SKILL §阶段 6.6 CJK 字体** | **用 Noto CJK SC** |
| **🆕 修编译错误** | **本 SKILL §阶段 6.5 5 类常见错误修复** | **瞎猜 — 按错误表查根因** |

---

## 检索使用规范（强制）

遇到以下场景**必须**使用检索工具，不许凭空编造：

| 场景 | 工具 | 示例 |
|------|------|------|
| 引用文献数据 | `exa_search` | "Author 2020 memory recall statistics" |
| 核实事实性陈述 | `tavily_search` | "cognitive offloading effects on memory" |
| 补充背景知识 | `exa_search` | "distributed cognition theory Hutchins 1995" |
| 验证学术术语 | `tavily_search` | "autobiographical memory definition" |
| 补充文献 | `exa_search` | "photo-taking impairment effect meta-analysis" |

**禁止**：
- ❌ 捏造文献作者、年份、期刊
- ❌ 凭空想象实验数据
- ❌ 未经证实的主观推测
- ❌ "应该是"、"大概如此"等模糊表述

---

## scripts 使用

```bash
# 自检脚本：检查证据语气/填充词/禁用隐喻/人称观点
python3 scripts/selfcheck.py --file <path> --level <sentence|paragraph|chapter>

# 快速检索
python3 -m scripts.lookup.searcher <关键词>       # 搜索指南
python3 -m scripts.lookup.searcher --list          # 列出所有指南
python3 -m scripts.lookup.indexer                  # 重建索引
```

---

## references 完整索引

### references/（使用指南）

| 文件 | 内容 |
|------|------|
| `guide.md` | 使用指南 |
| `index.md` | 书籍式索引 |

### references/workflows/（工作流）

| 文件 | 内容 |
|------|------|
| `writing-process-workflow.md` | 五阶段写作流程（理解→规划→起草→修改→校对）|
| `modification-workflow.md` | 修改方法论（论证地图→修改清单→执行→核查）|

### references/standards/（规范标准）

| 文件 | 内容 |
|------|------|
| `sentence-standards.md` | 句子规范（主语/动词/定义/"我们"边界）|
| `paragraph-standards.md` | 段落规范（主题句/论证链/过渡/字数）|
| `chapter-standards.md` | 篇章规范（闭环/子论点编排/过渡句）|
| `style-standards.md` | 术语管理/禁用词表/"我们"使用规则 |
| `citation-standards.md` | 引用类型/APA格式/常见错误 |
| **🆕 `quarto-yaml-standards.md`** | **apaquarto YAML 头模板（完整 author + affiliations + author-note + shorttitle）** |
| **🆕 `quarto-cjk-font-standards.md`** | **CJK 字体配置（AR PL SungtiL GB）header.tex 模板 + Noto CJK 坑** |
| **🆕 `quarto-bibliography-standards.md`** | **references.bib 模板（APA 7th BibTeX 条目格式）** |
| **🆕 `quarto-apa7th-headers-standards.md`** | **APA 7th 段落标准（悬挂缩进/双倍行距/sloppy 三件套）** |

### references/guides/（方法论指南）

| 文件 | 内容 |
|------|------|
| `writing-principles-guide.md` | 写作原则（立论/证据/结构）|
| `academic-style-guide.md` | 学术写作风格（清晰/简洁/客观/中立）|
| `evidence-layers-guide.md` | 证据-推测-解读三层区分 |
| `editing-proofreading-guide.md` | 修改层次/句子润色/校对清单 |
| `ai-writing-guide.md` | AI写作模式检测与消除 |
| `chinese-english-writing-guide.md` | 中英文论文差异与翻译写作规范 |

---

## 模板导航

| 模板 | 位置 | 说明 |
|------|------|------|
| 学术论文模板 | `assets/templates/academic-paper.md` | 论文标准结构模板 |
| 章节模板 | `assets/templates/chapter.md` | 各章节写作模板 |
| 摘要模板 | `assets/templates/abstract.md` | 摘要标准格式 |
| **🆕 Quarto 论文模板** | **`assets/templates/quarto-apa7th-paper.md`** | **apaquarto 5.0.18 YAML 头 + 4 件套引用模板** |

---

## 快速调用

```bash
# 自检文章
writer --file essay.md
writer --file essay.md --level sentence

# 构建索引
lookup! index -r /root/.openclaw/workspace/writer/skills/writer/references \
  -m /root/.openclaw/workspace/writer/skills/writer/index/manifest.json \
  -c /root/.openclaw/workspace/writer/skills/writer/index/chunks.json

# 搜索指南
lookup! search -i /root/.openclaw/workspace/writer/skills/writer/index/manifest.json <关键词>

# 查看帮助
writer --help
```

## 版本历史

| 版本 | 日期 | 更新 |
|------|------|------|
| **2.2.0** | **2026-06-06** | **🆕 老板指令集成 Quarto 排版技能**（v2 → v3 实战反馈）：新增阶段 6 排版与编译（4 件套 + 5 步流程 + 5 类错误修复 + CJK 字体配置 + 老板 23:14 反馈 — APA 7 论文规范违规清单）；新增 4 个 standards（quarto-yaml / quarto-cjk-font / quarto-bibliography / quarto-apa7th-headers）；**核心新增**"禁止论文里出现程序性声明"边界条件（老板 23:14 反馈："严重不合格"）；核心新增"不擅自添加元评论"核心原则 |
| 2.1.0 | 2026-05-23 | references目录重组：分为standards/workflows/guides三个子目录，SKILL.md路径同步更新 |
| 2.0.0 | 2026-05-23 | 按代理技能体系重构：新增模板导航章节、修复核心原则重复、明确目录结构 |
| 1.4.0 | 2026-05-20 | 同步skill-developer模板：新增触发条件表格、核心原则、边界条件 |
| 1.3.0 | 2026-05-20 | 彻底重构SKILL.md：新增五阶段工作流、场景化快速调用、完整references索引 |
| 1.2.0 | 2026-05-20 | 完善模块导航（15个references全收录），新增检索规范 |
| 1.1.0 | 2026-05-20 | 新增检索指引 + AI写作去痕 + 中英文差异指南 |
| 1.0.0 | 2026-05-20 | 初始版本，整合 thesis-writer 为通用写作技能 |

---

*维护者：杨权*
