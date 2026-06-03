# 排版原则

> 使用 **Quarto** + .md 文件（带 YAML 头）+ `references.bib` + `apa.csl` 进行协作排版。
> 2026-06-04 升级：原 v1 流程（基于独立的 yaml 配置文件）已废，全部切到 Quarto。

---

## 核心原则

1. **分离内容与格式**：内容使用 Markdown，格式由 Quarto YAML 头 + CSL 控制
2. **统一引用管理**：所有参考文献存入 `references.bib`，格式由 `apa.csl` 统一
3. **协作友好**：多人协作时，各自负责的章节存为独立 `.md` 文件，主文件通过 Quarto `chapters` 或 `input-files` 包含
4. **统一 LaTeX 后端**：用 `tinytex`（`/root/.TinyTeX/`，已装），不用系统 TeX Live

---

## 文件分工

| 文件 | 作用 | 负责人 |
|------|------|--------|
| `{论文}.md` | 正文 + YAML 头（自含 format.pdf 块）| 各 Agent 负责 |
| `references.bib` | 参考文献数据库 | 所有人按需添加 |
| `apa.csl` | 引用样式（APA 第7版）| 项目统一 |
| `header.tex` | LaTeX 局部调整（CJK + APA 7th + 防溢出）| 按需修改 |
| `_quarto.yml` | Quarto 项目级配置（多文件书用）| 项目统一 |

---

## Quarto 三种排版范式

| 范式 | 适用 | 命令 |
|------|------|------|
| **① 单文件学术论文** | 投稿论文（有引用）| `quarto render <file>.md --output-dir ../docs`（.md 自带 YAML 头 + `bibliography:` + `csl:`）|
| **② 单文件一般文章** | 科普、博文（无引用）| `quarto render <file>.md --output-dir ../docs`（.md 自带 YAML 头）|
| **③ 多文件书** | 博士论文、教材 | `quarto render`（项目根 `_quarto.yml` 列 19 章 + `references.bib` + `apa.csl`）|

---

## 单文件 .md YAML 头标准结构（范式 ①/②）

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

## 多文件书 `_quarto.yml` 标准结构（范式 ③）

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
| ①/② 单文件 | `cd manuscripts && quarto render 全文整合稿.md --output-dir ../docs && mv ../docs/全文整合稿.pdf ../docs/<标题>.pdf` |
| ③ 多文件书 | `cd manuscripts/博士论文/ && quarto render`（自动输出到 `docs/`） |

**坑**：单文件模式（无 `_quarto.yml`）下 YAML 里的 `output-dir` 不生效，必须 CLI flag 传。

---

## 常见问题

| 问题 | 解决方案 |
|------|----------|
| 中文字体溢出 | 在 `header.tex` 加 `\sloppy\tolerance=1000\emergencystretch=3em` |
| 缺少字体 | `fc-list :lang=zh` 看可用字体；CJK 用 `AR PL SungtiL GB`（apt 装 `fonts-arphic-gbsn00lp`）|
| 引用格式不对 | 确认 `apa.csl` 是 GitHub master 分支完整版（>80KB）|
| 嵌入字体显示 jp face | Noto CJK TTC 默认挑 jp 子 face → 改用单 TTF face 字体（`AR PL SungtiL GB`）|

---

## v1 老流程（已废，仅作历史参考）

**2026-06-04 起不再使用**。如果还在用旧 v1 流程的 yaml 配置文件，请迁移到 Quarto（见 `~/.openclaw/workspace/steward/.agents/skills/manager/references/quarto-pdf-config.md` 迁移 SOP）。
