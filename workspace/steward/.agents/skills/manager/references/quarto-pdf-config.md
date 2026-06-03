# Quarto PDF 编译配置指南 v1.1

> 当用户提到"Quarto"、"PDF 编译"、"apa.csl"、"header.tex"、要求迁移/新建/调整论文/科普/书 PDF 构建时，使用本指南。
> **2026-06-04 v1.0**：源自 TeX Live 2023 → tinytex 切换 + 3 个 Pandoc 项目迁移实践。
> **2026-06-04 v1.1**：新增「八、作者 + 单位 + 联系方式 PDF 渲染（authblk 模式）」（源自记忆机制认知推断论文实战）

---

## 一、Quarto 排版三范式（铁律）

> **用 Quarto 取代 Pandoc**（2026-06-04 起）。LaTeX 后端用 **tinytex**（`/root/.TinyTeX/`，450MB），不用系统 TeX Live 2023。

| 范式 | 适用 | 公式 |
|------|------|------|
| **① 书** | 多个 .md 组成的书籍（如博士论文 19 章）| `quarto render` + 多个 `.md` + `_quarto.yml` + `references.bib` + `apa.csl` |
| **② 学术论文** | 单 .md 投稿论文 | `quarto render <file>.md` + 单 `.md`（带 YAML 头）+ `references.bib` + `apa.csl` |
| **③ 一般文章** | 单 .md 科普/博文（无引用）| `quarto render <file>.md` + 单 `.md`（带 YAML 头）|

**反例（不许用）**：`pandoc xxx.md -o xxx.pdf` 任何形式；`pandoc.yaml` 配置。

---

## 二、编译命令（按范式）

### 范式 #1 书（多 .md + `_quarto.yml`）

```bash
cd manuscripts/博士论文/   # 假定 _quarto.yml 在这
quarto render              # 直接 render，配置在 _quarto.yml 里
```

`_quarto.yml` 关键字段：
```yaml
project:
  type: book
  output-dir: ../../docs     # ← book 模式 YAML 里的 output-dir 生效

book:
  title: "..."
  author: "..."
  chapters:
    - 正文/00_title_page.md
    - 正文/01_abstract.md
    - ...
    - 正文/18_acknowledgements.md  # 必须有 19 章
    # ↑ book 模式强制要求首页（通常用 index.md）

bibliography: references.bib
csl: apa.csl

format:
  pdf:
    pdf-engine: xelatex
    documentclass: ctexbook
    papersize: a4
    ...
    include-in-header: header.tex
```

### 范式 #2/#3 单文件

```bash
cd manuscripts
quarto render 全文整合稿.md --output-dir ../docs    # ← 单文件必须 CLI flag
mv ../docs/全文整合稿.pdf ../docs/论文标题.pdf     # 默认文件名=源文件名，建议改名
```

**坑**：单文件模式（无 `_quarto.yml`）下 YAML 里的 `output-dir` **不生效**。必须 CLI flag 传。

---

## 三、PDF 输出位置（铁律）

> **一律放项目根 `/docs/` 目录**。命名用标题（如 `docs/记忆机制的认知推断.pdf`）。

| 范式 | 配置位置 |
|------|---------|
| 范式 #1 书 | `_quarto.yml` 的 `project.output-dir: ../../docs`（相对 `_quarto.yml` 路径）|
| 范式 #2/#3 单文件 | CLI flag `quarto render <file>.md --output-dir ../docs` |

---

## 四、CJK 字体配置（2026-06-04 切换）

> **铁律：用 `AR PL SungtiL GB`（文鼎简报宋）**。apt 包 `fonts-arphic-gbsn00lp` 已装。

```latex
% 在 header.tex 或 header-includes 里
\usepackage{xeCJK}
\setCJKmainfont{AR PL SungtiL GB}
\setCJKsansfont{AR PL SungtiL GB}
\setCJKmonofont{AR PL SungtiL GB}
\setmainfont{AR PL SungtiL GB}
\setsansfont{AR PL SungtiL GB}
\setmonofont{AR PL SungtiL GB}

% CJK 断行（必须）
\XeTeXlinebreaklocale "zh"
\XeTeXlinebreakskip = 0pt plus 1pt
\usepackage{xurl}    % URL 换行
```

### 为什么不推荐 Noto CJK SC

| 字体名 | 嵌入 PDF 的元数据 | 视觉 |
|--------|-----------------|------|
| `Noto Serif CJK SC` | `NotoSerifCJKjp`（日文 subface）| 中文正常（jp 共享 CJK 字符）|
| `AR PL SungtiL GB` | `BousungEG-Light-GB`（绝对 SC）| 中文正常 |

**根因**：Noto CJK TTC 文件含 5 个 subface（JP/KR/SC/TC/HK），xelatex 默认挑第一个 jp。fontspec 的 `Path=`、`UprightFont=`、`Renderer=HarfBuzz` **都救不了**。唯一根治是换用单 TTF face 字体。

---

## 五、APA 7th 排版

```bibtex
% references.bib
@article{Conway2000,
  author = {Conway, Martin A.},
  title = {Memory and the self},
  journal = {Journal of Memory and Language},
  year = {2000}
}
```

```yaml
# .md YAML 头
bibliography: references.bib
csl: apa.csl          # ← GitHub master 分支下载完整版（>80KB）
```

**正文引用语法**：
- `[@key]` — 括号引用（多篇用分号分隔：`[@key1; @key2]`）
- `@key` — 叙事引用（"@Author 提出..."）

**Key 规则**：`AuthorSurnameYear`，同年同姓加 `a`/`b`（如 `Wang2025a`/`Wang2025b`）

**坑**：
- 简化版 `apa.csl`（< 50KB 缺 `<citation>` 元素）会触发 `CiteprocParseError` → 必须用完整版
- 范式 #1（多文件书）若有正文 `\citep{}`（原始 LaTeX natbib 命令），需 `_quarto.yml` 设 `citeproc: false` + `from: markdown+raw_tex`

---

## 六、LaTeX 头部写法（两种等价）

### 方式 A：`header-includes`（YAML 内联）

适合简短 LaTeX（1-5 行）：

```yaml
header-includes:
  - |
    \usepackage{xeCJK}
    \setCJKmainfont{AR PL SungtiL GB}
    \XeTeXlinebreaklocale "zh"
    ...
```

### 方式 B：`include-in-header: header.tex`（外部文件）

适合复杂 LaTeX（CJK + APA 7th + 防溢出 三件套）：

```yaml
format:
  pdf:
    include-in-header: "header.tex"   # 路径相对 .md
```

`header.tex` 独立文件，便于编辑器语法高亮、版本控制。

### 选哪种

| 场景 | 推荐 |
|------|------|
| 一般文章 / 短论文 | `header-includes` 内联 |
| 学术论文（APA 7th 复杂）| `include-in-header: header.tex` |
| 书（多 .md 复杂配置）| `include-in-header: header.tex` |

两者**可混用**（`include-in-header` 先加载，`header-includes` 后追加）。

---

## 七、APA 7th 标准 header.tex 模板

```latex
% === CJK 字体 ===
\usepackage{xeCJK}
\setCJKmainfont{AR PL SungtiL GB}
\setCJKsansfont{AR PL SungtiL GB}
\setCJKmonofont{AR PL SungtiL GB}
\setmainfont{AR PL SungtiL GB}
\setsansfont{AR PL SungtiL GB}
\setmonofont{AR PL SungtiL GB}

% === CJK 断行 ===
\XeTeXlinebreaklocale "zh"
\XeTeXlinebreakskip = 0pt plus 1pt
\usepackage{xurl}

% === APA 7th 段落 ===
\usepackage{indentfirst}
\setlength{\parindent}{2em}
\usepackage{setspace}
\doublespacing

% === 章节标题左对齐加粗 ===
\usepackage{sectsty}
\sectionfont{\normalfont\bfseries\large}
\subsectionfont{\normalfont\bfseries\normalsize}

% === 参考文献悬挂缩进 ===
\renewenvironment{thebibliography}[1]{%
  \section*{参考文献}%
  \singlespacing%
  \list{}{%
    \setlength{\leftmargin}{2em}%
    \setlength{\itemindent}{-2em}%
    \setlength{\itemsep}{2pt}%
  }%
  \sloppy\clubpenalty4000\widowpenalty4000%
}{\endlist}

% === 防段落右侧超出 ===
\sloppy
\tolerance=1000
\emergencystretch=3em
```

---

## 八、作者 + 单位 + 联系方式 PDF 渲染（authblk 模式）

> **Quarto 默认 PDF 模板不渲染 `author.affiliations` / `orcid` / `email`**——这是长期 bug（GitHub Issue #10639、StackOverflow #75040607），HTML 和期刊模板（JATS/ACM/IEEE）支持，但默认 LaTeX 模板只渲染 `\author{姓名}`。
> 解决方案：用 `template-partials` 引用自定义 `title.tex` + `authblk` 宏包。

### 完整四件套配置

**1. `header.tex` 加 `authblk`**（一次性，全局复用）：

```latex
\usepackage{authblk}    % Pandoc 默认模板用 \affil{} 渲染 affiliation,需要 authblk
```

**2. `manuscripts/title.tex` 模板 partial**（Quarto Pandoc 模板语法）：

```latex
$if(title)$
\title{$title$}
$endif$

$if(subtitle)$
\subtitle{$subtitle$}
$endif$

$for(by-author)$
\author$if(by-affiliation)$[$for(by-affiliation)$$it.number$$sep$,$endfor$]$endif${$it.name.literal$}
$endfor$

$for(by-affiliation)$
\affil[$it.number$]{$it.name$$if(it.department)$, $it.department$$endif$$if(it.city)$, $it.city$$endif$$if(it.state)$, $it.state$$endif$$if(it.country)$, $it.country$$endif$$if(it.url)$. URL: $it.url$.$endif$}
$endfor$

$if(date)$
\date{$date$}
$endif$
```

**3. `.md` YAML 头**（注意 `number` 而非 `id`）：

```yaml
author:
  - name: "杨权"
    orcid: "0000-0001-6201-4174"
    email: "yangquan0310@163.com"
    corresponding: true        # ← Quarto 不展开为 \thanks,纯文档用途
    affiliations:
      - number: 1              # ← 必须是 number,不是 id
        name: "华中师范大学心理学院"
        department: "心理学院"
        city: "武汉"
        state: "湖北"
        country: "中国"
        url: "https://psych.ccnu.edu.cn/"

format:
  pdf:
    include-in-header: "header.tex"
    template-partials:          # ← 关键:让 Quarto 用我们的 title.tex
      - title.tex
```

**4. 通讯作者联系方式**（email + ORCID）—— **手动 LaTeX 块**（绕开 Quarto `\thanks` 不展开的坑）：

放在 H1 之后、第一节正文之前（H1 之前会跑到 abstract 区，H1 之后是节标题+正文之间）：

```markdown
# 历史回顾：从Transformer到记忆机制的技术演进

\begin{center}
\small
\textbf{通讯作者}: 杨权 \quad \href{mailto:yangquan0310@163.com}{yangquan0310@163.com} \quad ORCID: \href{https://orcid.org/0000-0001-6201-4174}{0000-0001-6201-4174}
\end{center}

现代大规模语言模型的崛起...
```

### 坑速查

| 坑 | 症状 | 解决 |
|---|------|------|
| `id: ccnupsy` 写入 affiliation | PDF 显示 "ccnupsy" 字符串 | 改用 `number: 1`（`id` 是 Quarto 内部引用，不应渲染）|
| `\author[1]` + `\textsuperscript{1}` 同时用 | 作者名后出现 "¹¹"（双上标）| 删 `\textsuperscript{}`，只让 authblk 自动加 |
| `note: "..."` 当 thanks 内容 | `\thanks{true}`（Quarto 把 note 解析为 boolean）| 用 LaTeX `\begin{center}` 块手动渲染，不用 `note` 字段 |
| `corresponding: true` 想自动加 \* | 没星号标 | 配合 `\begin{center}` 块手动写"通讯作者"字样 |
| `\thanks{Corresponding author...}` 不显示 | 模板不展开 `it.note`/`it.acknowledgements` | LaTeX `\begin{center}` 块绕开 |
| `\href{$it.url$}{$it.url$}` 报错 | pandoc 模板 "unexpected '}'" | URL 改用 `$it.url$` 直接字符串输出，不嵌套 `\href{}` |

### 元数据来源

- 老板的 `orcid` / `email` / 单位：来自 `~/.openclaw/wiki/entities/yangquan.md`（基础信息表 行 49-50）
- 标准流程：派发论文任务前**先查 wiki 实体**确认作者元信息，而不是让作者重报

### 已知替代方案

| 方案 | 优 | 劣 |
|------|---|---|
| **authblk + title.tex** ← 本指南 | 完全可控、依赖少 | 需手写 title.tex |
| Quarto 期刊模板（`format.pdf.journal: acm`）| 完整 author/affiliation schema | 模板风格固定，仅适合期刊投稿 |
| `apa-pdf` 模板 | APA 7th 自动 | CJK 字体兼容性差，xelatex 下常错位 |

---

## 九、迁移 SOP（Pandoc → Quarto）

见 `~/.openclaw/workspace/steward/temp/pandoc-to-quarto-sop.md`（3 个项目迁完后已沉淀）。

---

## 十、常见坑速查

| 坑 | 症状 | 解决 |
|---|------|------|
| 简化版 apa.csl | `CiteprocParseError: No citation element present` | 用 GitHub master 完整版（>80KB）|
| output-dir 不生效 | PDF 落 `manuscripts/` | 单文件必须 CLI flag `quarto render --output-dir ../docs`|
| Noto CJK 嵌入 jp | `pdffonts` 显示 `NotoSerifCJKjp` | 改 `AR PL SungtiL GB`（单 TTF face）|
| 中文段落右侧溢出 | 文字超出右边距 | `\emergencystretch=3em`（不是 2em）|
| `\citep` 报 undefined | 范式 #1 用 natbib 命令 | `_quarto.yml` 加 `citeproc: false` + `from: markdown+raw_tex`|
| tlmgr `Can't locate TeXLive/TLConfig.pm` | symlink 导致 perl @INC 错位 | 设 `PERL5LIB=/root/.TinyTeX/tlpkg:/root/.TinyTeX/texmf-dist/scripts/texlive`|

---

## 十一、Quarto 引擎探测

```bash
$ quarto check
[✓] Checking LaTeX....................OK
      Using: TinyTex
      Path: /root/.TinyTeX/bin/x86_64-linux
      Version: 2026
```

`TinyTeX 2026` + `xeTeX 3.141592653-2.6-0.999998 (TeX Live 2026)` = 正常。

---

## 十二、版本

| 版本 | 日期 | 说明 |
|------|------|------|
| **1.1.0** | **2026-06-04** | **新增「八、作者 + 单位 + 联系方式 PDF 渲染（authblk 模式）」**：源自记忆机制论文实战。Quarto 默认 PDF 模板不渲染 `affiliations/orcid/email`（Issue #10639），用 `authblk` 宏包 + 自定义 `title.tex` partial 修复。同步坑速查 6 条 + 替代方案对比 + wiki 实体作为元数据源 |
| 1.0.0 | 2026-06-04 | 初始版本（3 个 Pandoc 项目迁 Quarto 实践沉淀） |

*详见 [索引](../index.md)*
