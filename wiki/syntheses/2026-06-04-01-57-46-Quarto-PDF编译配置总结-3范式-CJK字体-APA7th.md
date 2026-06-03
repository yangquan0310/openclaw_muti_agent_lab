---
pageType: synthesis
id: synthesis.quarto-pdf-config
createdAt: "2026-06-04T01:57:46+08:00"
updatedAt: "2026-06-04T01:57:46+08:00"
title: Quarto PDF 编译配置总结：3 范式 + CJK 字体 + APA 7th
sourceIds:
  - source.system-config
  - source.openclaw-env
aliases:
  - Quarto 配置
  - Quarto PDF 编译
  - APA 7th 排版
---

# Quarto PDF 编译配置总结：3 范式 + CJK 字体 + APA 7th

> **核心问题**：怎样用 Quarto 排版 PDF 论文/科普文章/书？
> **答案**：3 种范式（书 / 学术论文 / 一般文章）+ CJK 用 `AR PL SungtiL GB`（避 Noto TTC 坑）+ APA 7th 用 `apa.csl` + `references.bib`。

---

## 核心要点

1. **三范式固定**：
   - **书**（多 .md）= `_quarto.yml` + 多个 `.md` + `references.bib` + `apa.csl`
   - **学术论文**（单 .md）= 单 `.md`（带 YAML 头）+ `references.bib` + `apa.csl`
   - **一般文章**（单 .md）= 单 `.md`（带 YAML 头），无引用

2. **PDF 输出位置固定** = 项目根 `/docs/`
   - 单文件用 CLI flag：`quarto render <file>.md --output-dir ../docs`（YAML 里 `output-dir` 不生效）
   - 书用 `_quarto.yml.project.output-dir: ../../docs`

3. **CJK 字体固定** = `AR PL SungtiL GB`（文鼎简报宋），单 TTF face，绝对 SC
   - 不用 Noto CJK（xelatex 会嵌入 jp face，PDF 元数据显示 `NotoSerifCJKjp`）
   - 视觉：从 Noto 切到报宋（仍可读，学术风格）

4. **APA 7th 三件套** = `apa.csl`（GitHub master 完整版 > 80KB） + `references.bib`（BibTeX） + `header.tex`（APA 段落样式）

---

## 详细分析

### 一、Quarto 三范式（2026-06-04 老板统一明确）

| 范式 | 公式 | 编译命令 |
|------|------|---------|
| **书** | `quarto render` + 多 `.md` + `_quarto.yml` + `references.bib` + `apa.csl` | `cd <book>; quarto render`（配置全在 YAML）|
| **学术论文** | `quarto render <file>.md` + 单 `.md`（YAML 头）+ `references.bib` + `apa.csl` | `cd manuscripts && quarto render 全文整合稿.md --output-dir ../docs` |
| **一般文章** | `quarto render <file>.md` + 单 `.md`（YAML 头）| 同上，但无 `bibliography:` / `csl:` |

**反例（不许用）**：任何 `pandoc xxx.md -o xxx.pdf` 命令、任何 `pandoc.yaml` 配置。

### 二、CJK 字体：Noto CJK TTC 坑（2026-06-04 大管家踩坑）

**问题**：
- `\setCJKmainfont{Noto Serif CJK SC}` + xelatex 默认挑 Noto CJK TTC 的 **JP face**（第一个 subface）
- PDF 嵌入字体元数据显示 `NotoSerifCJKjp`
- 视觉是中文（jp 共享 CJK 字符），但元数据不对
- fontspec 的 `Path=`、`UprightFont=`、`Renderer=HarfBuzz` 全部**救不了**

**根治**：换用单 TTF face 字体 `AR PL SungtiL GB`（文鼎简报宋）
- apt 包 `fonts-arphic-gbsn00lp` 已装
- 嵌入字体元数据显示 `BousungEG-Light-GB`，**绝对 SC**
- 视觉：报宋（替代 Noto），仍可读

### 三、PDF 输出位置：必须放 `docs/`

- 单文件模式 YAML 里 `output-dir` **不生效**，必须 CLI flag
- 命名用标题（如 `docs/记忆机制的认知推断.pdf`）
- `mv ../docs/全文整合稿.pdf ../docs/<标题>.pdf` 重命名（quarto 默认输出文件名 = 源文件名）

### 四、APA 7th 完整配置

```latex
% header.tex（标准模板）
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

\usepackage{indentfirst}
\setlength{\parindent}{2em}
\usepackage{setspace}
\doublespacing

\usepackage{sectsty}
\sectionfont{\normalfont\bfseries\large}
\subsectionfont{\normalfont\bfseries\normalsize}

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

\sloppy
\tolerance=1000
\emergencystretch=3em
```

### 五、LaTeX 头部两种写法（功能等价）

| 方式 | 写法 | 适合 |
|------|------|------|
| `header-includes`（YAML 内联）| `header-includes: - \| \usepackage{...}` | 简短 LaTeX（1-5 行）|
| `include-in-header: header.tex`（外部文件）| `format.pdf.include-in-header: "header.tex"` | 复杂 LaTeX（CJK + APA 7th 三件套）|

**可混用**：`include-in-header` 先加载，`header-includes` 后追加。

### 六、3 项目实战案例（2026-06-04 完成迁移）

| 项目 | 范式 | commit | PDF |
|------|------|--------|-----|
| 记忆机制认知推断论文 | #2 学术论文 | `1fc8f1f` | 541K / 57 页 |
| AI-Agent 科普文章 | #3 一般文章 | `78c6ed5` + `2a484af` CJK fix + `6978aa2` SC fix | 41K → 视觉中文正常 |
| 数字化存储·博士论文 | #1 书（19 章）| `b6755826` | 2.7M / 152 页 |

**全部用 tinytex 2026**（`/root/.TinyTeX/`，450MB）+ Quarto 1.7.34。

### 七、迁移 SOP

完整 Pandoc → Quarto 迁移 SOP 沉淀在：
- `~/.openclaw/workspace/steward/temp/pandoc-to-quarto-sop.md`
- `~/.openclaw/workspace/steward/.agents/skills/manager/references/quarto-pdf-config.md`

---

## 来源

- `~/.openclaw/workspace/steward/MEMORY.md` If-Then 规则（v8.20.0 + CJK TTC 经验）
- `~/.openclaw/workspace/steward/TOOLS.md` TinyTeX 章节
- `~/.openclaw/workspace/steward/.agents/skills/manager/references/quarto-pdf-config.md`（同步沉淀）
- `~/.openclaw/workspace/steward/temp/pandoc-to-quarto-sop.md` 迁移 SOP
- 3 个实战项目 git log（见 commit 列表）

---

## 待解决问题

- 简化版 `apa.csl`（< 50KB 缺 `<citation>` 元素）仍可能在某些子代理迁移时出现 → 需要在 SOP 强化下载来源（GitHub master 完整 URL）
- 范式 #1（多文件书）若有正文 `\citep{}`（原始 LaTeX natbib 命令），需 `_quarto.yml` 设 `citeproc: false` + `from: markdown+raw_tex` —— 已在 MEMORY 记录但 SOP v1 未含
- AR PL SungtiL GB 视觉与 Noto 不同，未来如需"现代风格"中文，需找其他单 TTF face 字体（Source Han Serif SC 单文件？）

---

## 相关（待沉淀）

以下是本 synthesis 涉及、但 wiki 暂无独立页的子主题，未来可建：

- `concepts/quarto-范式` — 3 种排版范式的对比
- `concepts/cjk-字体配置` — 各类 CJK 字体在 xelatex 下的行为
- `concepts/apa-7th-排版` — APA 7th 引用样式与文档样式
- `concepts/pdf-输出位置` — 项目 docs/ 规范
- `sources/tex-live-2023-迁移` — 2026-06-04 系统切换过程
- `sources/tinytex-安装` — tinytex 用户级 TeX Live 安装

**当前指向沉淀在 manager 技能的 `references/quarto-pdf-config.md`（v1.0，2026-06-04）**。

---

*最后更新：2026-06-04*
*更新者：大管家*
*源自：3 个 Pandoc 项目迁移 Quarto 实战沉淀*

## Related
<!-- openclaw:wiki:related:start -->
### Sources

- [[sources/openclaw-env|openclaw-env]]
<!-- openclaw:wiki:related:end -->
