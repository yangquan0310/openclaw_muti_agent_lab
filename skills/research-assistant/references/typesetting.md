# 排版原则

> 使用 **Quarto** + .md 文件（带 YAML 头）+ `references.bib` + `apa.csl` 进行协作排版。
> 2026-06-04 升级：原 v1 流程（基于独立的 yaml 配置文件）已废，全部切到 Quarto。
> 2026-06-04 v1.1：新增 **范式 ④ apaquarto-pdf 严格 APA 7 manuscript mode**（投稿期刊标准），源自记忆机制认知推断论文实战。

---

## 核心原则

1. **分离内容与格式**：内容使用 Markdown，格式由 Quarto YAML 头 + CSL 控制
2. **统一引用管理**：所有参考文献存入 `references.bib`，格式由 `apa.csl` 统一
3. **协作友好**：多人协作时，各自负责的章节存为独立 `.md` 文件，主文件通过 Quarto `chapters` 或 `input-files` 包含
4. **统一 LaTeX 后端**：用 `tinytex`（`/root/.TinyTeX/`，已装），不用系统 TeX Live
5. **🆕 学术论文默认 APA 7 manuscript mode（范式 ④）**：投稿期刊、正式论文、心理学/教育学/社科类论文 → **强制用 apaquarto-pdf 范式**，不要用基础 Quarto+apa.csl 范式（基础范式不产出 APA 7 manuscript 的 title page / author note / running head 等结构）

---

## 文件分工

| 文件 | 作用 | 负责人 |
|------|------|--------|
| `{论文}.md` | 正文 + YAML 头（自含 format.pdf 块）| 各 Agent 负责 |
| `references.bib` | 参考文献数据库 | 所有人按需添加 |
| `apa.csl` | 引用样式（APA 第7版，基础范式用）| 项目统一 |
| `header.tex` | LaTeX 局部调整（CJK + APA 7th + 防溢出）| 按需修改 |
| `_quarto.yml` | Quarto 项目级配置（多文件书 / 范式 ④ 根标记）| 项目统一 |
| `_extensions/apaquarto/` | 🆕 范式 ④ 用的 apaquarto 扩展（含完整 apa.csl + doc-class.tex + 排版 Lua 脚本）| 项目级首次配置 |

---

## Quarto 四种排版范式

| 范式 | 适用 | 命令 |
|------|------|------|
| **① 多文件书** | 博士论文、教材（19+ 章）| `quarto render`（项目根 `_quarto.yml` 列 N 章 + `references.bib` + `apa.csl`）|
| **② 单文件学术论文（基础）** | 投稿论文（有引用，宽松 APA 7）| `quarto render <file>.md --output-dir ../docs`（.md 自带 YAML 头 + `bibliography:` + `csl:`）|
| **③ 单文件一般文章** | 科普、博文（无引用）| `quarto render <file>.md --output-dir ../docs`（.md 自带 YAML 头）|
| **🆕 ④ 严格 APA 7 manuscript mode（apaquarto）** | **投稿期刊标准**：心理学/教育学/社科类正式论文、APA 7 强制要求的稿件 | `quarto render <file>.md --to apaquarto-pdf`（项目根必须有 `_quarto.yml` 标记 + `_extensions/apaquarto/` 扩展）|

**默认决策**：
- 正式学术论文（投稿、毕业论文中需要 APA 7 排版的章节）→ **范式 ④**（严格 APA 7）
- 课程作业、研究现状、文献综述（投稿用）→ **范式 ②**（基础 Quarto + apa.csl，足够用）
- 书/教材/多章节文档 → **范式 ①**
- 科普/博文 → **范式 ③**

---

## 单文件 .md YAML 头标准结构（范式 ②/③）

```yaml
---
title: "论文标题"
author: "作者一, 作者二"
date: "2026-06-04"
keywords: [关键词1, 关键词2]
abstract: |
  摘要正文（150-300字）。

bibliography: references.bib
csl: apa.csl

format:
  pdf:
    pdf-engine: xelatex
    documentclass: article
    papersize: letter
    fontsize: 12pt
    geometry: [top=1in, bottom=1in, left=1in, right=1in]
    include-in-header: header.tex
    number-sections: true
    biblio-title: "参考文献"
---
```

---

## 🆕 范式 ④ 严格 APA 7 manuscript mode（apaquarto-pdf）

> **适用**：投稿期刊、正式学术论文（心理学/教育学/社科类）。产出**独立标题页 + 独立摘要页 + Author Note + Running head + 页码右上角 + 双倍行距**，完整 APA 7 期刊稿件结构。
> **2026-06-04 实战验证**：记忆机制认知推断论文（51 页 / 476KB，严格 APA 7 manuscript mode）

### 范式 ④ 的 5 步关键修复（必读，否则报错/退回基础范式）

1. **装 R 环境**：apaquarto 5.0.18 预检查要 R+knitr（即使不用 R chunks）。
   ```bash
   conda activate r-base  # r-base 环境已存在，R 4.3.1
   ```
2. **PATH 配 r-base + tinytex**（缺一不可）：
   ```bash
   export PATH=/root/.conda/envs/r-base/bin:/root/.TinyTeX/bin/x86_64-linux:$PATH
   ```
3. **建项目根 `_quarto.yml`**（**空壳** + `project: type: default`）—— **真正的根因**！Quarto 需要 `_quarto.yml` 识别项目根，才能从子目录 `manuscripts/` 上溯找到 `_extensions/apaquarto/`。
   ```yaml
   # 项目根 _quarto.yml（只有这两行，够了）
   project:
     type: default
   ```
4. **装 apaquarto 扩展**（项目级，不是用户级）：
   ```bash
   cd /项目根
   quarto add wjschne/apaquarto  # 自动装到 ./_extensions/apaquarto/
   ```
5. **.md YAML 头特殊处理**：
   - ✅ 用 `format: apaquarto-pdf:`（**不要**用 `pdf:` 块）
   - ✅ 必填 `author-note:`（含 disclosures / conflict-of-interest）
   - ✅ 必填 `shorttitle:`（= running head 上限 50 字符）
   - ✅ `author:` 必填 `corresponding: true/false` + `orcid:` + `roles:` + `affiliations:`
   - ❌ **不要**写 `bibliography:` + `csl:` 字段（apaquarto 自带，重复写会冲突）

### 范式 ④ 的 .md YAML 头标准结构

```yaml
---
title: "论文完整标题"
shorttitle: "Running head 上限 50 字符"
author:
  - name: "杨权"
    orcid: "0000-0001-6201-4174"
    email: "yangquan0310@163.com"
    corresponding: true
    roles:
      - conceptualization
      - writing
      - methodology
    affiliations:
      - id: ccnupsy
        name: "华中师范大学心理学院"
        department: "心理学院"
        city: "武汉"
        region: "湖北"
        country: "中国"
date: "2026-06-04"
keywords: [关键词1, 关键词2, 关键词3]
abstract: |
  摘要正文（APA 7 严格格式，150-250 字）。

author-note:
  disclosures:
    conflict-of-interest: "作者声明无利益冲突。"

floatsintext: true
numbered-lines: false
word-count: false
draft-date: false

format:
  apaquarto-pdf:
    documentmode: man    # 关键：manuscript mode（journal article 风格）
    keep-tex: true
    include-in-header: "header.tex"
---
```

### 范式 ④ 渲染命令

```bash
# 在项目根（有 _quarto.yml + _extensions/apaquarto/）
quarto render manuscripts/全文整合稿.md --to apaquarto-pdf

# 完整版（指定输出位置 + 改名）
quarto render manuscripts/全文整合稿.md --to apaquarto-pdf --output-dir docs
mv docs/全文整合稿.pdf docs/记忆机制的认知推断.pdf
```

### 范式 ④ 产出的 PDF 特征

| 特征 | 是否产出 |
|------|---------|
| 独立标题页（Title page）| ✅ |
| 独立摘要页（Abstract page）| ✅ |
| Author Note 段（ORCID + Conflict of interest + CRediT roles + 通讯作者）| ✅ |
| Running head（短标题大写）| ✅ |
| 页码右上角 | ✅ |
| 双倍行距 | ✅ |
| APA 7 宏包接管 documentclass（不再用 Pandoc 默认 scrartcl）| ✅ |
| Title case（标题自动 APA 7 风格）| ✅ |

### 范式 ④ 详细配置 → 见 [apaquarto-manuscript.md](apaquarto-manuscript.md)

包含：环境/扩展安装的完整命令、YAML 头字段详解、5 步关键修复的踩坑记录、常见错误排错。

---

## 多文件书 `_quarto.yml` 标准结构（范式 ①）

```yaml
project:
  type: book
  output-dir: ../../docs

book:
  title: "书标题"
  author: "作者"
  chapters:
    - index.md
    - 正文/01_abstract.md
    - 正文/02_intro.md
    # ... 更多章节

bibliography: references.bib
csl: apa.csl

format:
  pdf:
    pdf-engine: xelatex
    documentclass: ctexbook
    papersize: a4
    fontsize: 10.5pt
    geometry: [top=3.9cm, bottom=3.5cm, left=2.9cm, right=2.9cm]
    linestretch: 1.5
    include-in-header: header.tex
```

---

## header.tex 示例（CJK + APA 7th + 防溢出三件套）

```tex
\usepackage{xeCJK}
\setCJKmainfont{AR PL SungtiL GB}
\setCJKsansfont{AR PL SungtiL GB}
\setCJKmonofont{AR PL SungtiL GB}
\XeTeXlinebreaklocale "zh"
\XeTeXlinebreakskip = 0pt plus 1pt
\usepackage{xurl}
\usepackage{indentfirst}
\setlength{\parindent}{2em}
\usepackage{setspace}
\doublespacing
\sloppy
\tolerance=1000
\emergencystretch=3em
```

---

## references.bib 添加文献

```bibtex
@article{Author2024,
  author = {Author, A. and Coauthor, B.},
  title = {Title of the work},
  journal = {Journal Name},
  year = {2024},
  volume = {1},
  pages = {1--10},
  doi = {10.xxxx/xxxxx}
}
```

正文引用：`[@Author2024]`（Quarto citeproc 自动生成 APA 7th 格式）

---

## 编译命令

| 范式 | 命令 |
|------|------|
| ②/③ 单文件 | `cd manuscripts && quarto render 全文整合稿.md --output-dir ../docs && mv ../docs/全文整合稿.pdf ../docs/<标题>.pdf` |
| ① 多文件书 | `cd manuscripts/博士论文/ && quarto render`（自动输出到 `docs/`） |
| 🆕 ④ 严格 APA 7 manuscript mode | `cd 项目根 && quarto render manuscripts/全文整合稿.md --to apaquarto-pdf --output-dir docs && mv docs/全文整合稿.pdf docs/<标题>.pdf` |

**坑**：单文件模式（无 `_quarto.yml`）下 YAML 里的 `output-dir` 不生效，必须 CLI flag 传。

---

## 常见问题

| 问题 | 解决方案 |
|------|----------|
| 中文字体溢出 | 在 `header.tex` 加 `\sloppy\tolerance=1000\emergencystretch=3em` |
| 缺少字体 | `fc-list :lang=zh` 看可用字体；CJK 用 `AR PL SungtiL GB`（apt 装 `fonts-arphic-gbsn00lp`）|
| 引用格式不对 | 基础范式：确认 `apa.csl` 是 GitHub master 分支完整版（>80KB）；范式 ④：apaquarto 自带完整 apa.csl，无需额外检查 |
| 嵌入字体显示 jp face | Noto CJK TTC 默认挑 jp 子 face → 改用单 TTF face 字体（`AR PL SungtiL GB`）|
| 🆕 范式 ④ 报错 "R not found" | `conda activate r-base` + `export PATH=/root/.conda/envs/r-base/bin:$PATH`（apaquarto 5.0.18 预检查要 R）|
| 🆕 范式 ④ 报错 "apaquarto-pdf format not found" | ①项目根没建 `_quarto.yml`（空壳 `project: type: default`）②`_extensions/apaquarto/` 不在项目根；缺一个 Quarto 就找不到扩展 |
| 🆕 范式 ④ 退回 Pandoc 默认（没出 title page / author note） | `_quarto.yml` 里 `type: default` 丢了，或 `.md` 写了 `format: pdf:` 而非 `format: apaquarto-pdf:` |

---

## v1 老流程（已废，仅作历史参考）

**2026-06-04 起不再使用**。如果还在用旧 v1 流程的 yaml 配置文件，请迁移到 Quarto（见 `~/.openclaw/workspace/steward/.agents/skills/manager/references/quarto-pdf-config.md` 迁移 SOP）。

---

## 版本历史

| 版本 | 日期 | 更新 |
|------|------|------|
| v1.1 | 2026-06-04 | 新增 **范式 ④ 严格 APA 7 manuscript mode（apaquarto-pdf）** + 5 步关键修复；明确学术论文默认范式 ④；新增 3 条 apaquarto 常见错误排错。源自记忆机制认知推断论文实战。 |
| v1.0 | 2026-06-04 | 初版：Quarto 三范式（书 / 单文件学术论文 / 单文件一般文章）。源自 v8.20.0 TeX Live 2023 → tinytex 切换。 |
