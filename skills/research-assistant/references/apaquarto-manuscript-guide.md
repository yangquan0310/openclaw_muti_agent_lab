# 范式 ④ APA 7 manuscript mode（apaquarto-pdf）配置指南

> **2026-06-12 重写**：基于跨期选择年龄差异论文实战（19 页 / 287KB）。
> **v2.0 修正 v1.0 的关键错误**：_quarto.yml / _extensions / references.bib 位置；header.tex 不需要；引用必须用 `[@key]` 语法。

---

## 1. 何时使用范式 ④

| 场景 | 范式 |
|------|------|
| 投稿心理学/教育学/社科类期刊 | **范式 ④**（APA 7 强制）|
| 毕业论文 APA 7 manuscript 排版 | **范式 ④** |
| 课程作业、研究现状、文献综述 | 范式 ②（基础 Quarto + apa.csl）|
| 书/教材/多章节文档 | 范式 ① |
| 科普/博文 | 范式 ③ |

---

## 2. 环境准备（一次性）

### 2.1 R + knitr

```bash
# r-base conda 环境
export PATH=/root/.conda/envs/r-base/bin:/root/.TinyTeX/bin/x86_64-linux:$PATH
R --version
```

### 2.2 Quarto + tinytex

```bash
quarto --version   # 1.7.34+
xelatex --version  # TeX Live 2026 (tinytex)
```

---

## 3. 项目初始化（每个新项目走一次）

### 3.1 目录结构

```
项目根/
├── docs/                          ← 编译输出
│   └── Manuscript.pdf
└── manuscripts/
    ├── _quarto.yml                ← Quarto 项目配置（必须）
    ├── _extensions/apaquarto/     ← apaquarto 扩展（quarto add 装）
    ├── Manuscript.md              ← 正文（带 YAML 头）
    ├── references.bib             ← 参考文献库
    └── figures/                   ← 图片
        ├── image1.png
        ├── image2.png
        └── image3.png
```

**关键认知**：`_quarto.yml`、`_extensions/`、`references.bib` 全部在 `manuscripts/` 目录下（不是项目根）。

### 3.2 创建 `_quarto.yml`

```yaml
# manuscripts/_quarto.yml（只需这两行）
project:
  type: default
```

### 3.3 安装 apaquarto 扩展

```bash
cd manuscripts
quarto add wjschne/apaquarto
# 自动装到 ./_extensions/apaquarto/
```

**注意**：直接 cd 到 `manuscripts/` 目录执行，不要在项目根执行后复制。

### 3.4 不需要 header.tex

apaquarto 通过 YAML 字段控制所有排版参数，**不需要自建 header.tex**。
CJK 字体等特殊需求可通过 YAML 的 `include-in-header` 字段处理（见下方 YAML 模板）。

---

## 4. YAML 头模板

```yaml
---
title: "论文完整标题"
shorttitle: "Running head（≤50 字符）"

author:
  - name: "作者姓名"
    corresponding: true
    affiliations:
      - id: aff1
        name: "机构名称"
        department: "院系"
        city: "城市"
        region: "省份"
        country: "中国"

author-note:
  disclosures:
    conflict-of-interest: "作者声明无利益冲突。"

abstract: |
  摘要正文（150-250 字）。

keywords:
  - 关键词1
  - 关键词2
  - 关键词3

# 不需要 bibliography: 和 csl: 字段
# apaquarto 自带 apa.csl，bibliography 默认找 references.bib
# 如果文件名不是 references.bib，需要显式声明：
# bibliography: references.bib

floatsintext: false    # false = 图表集中到末尾（期刊投稿常用）
numbered-lines: false
word-count: false
draft-date: false

format:
  apaquarto-pdf:
    documentmode: man
    keep-tex: true
    # include-in-header: "header.tex"  # 仅 CJK 等特殊需求时用
---
```

---

## 5. 引用语法（核心！）

引用格式严格按 [Quarto Citations 文档](https://quarto.org/docs/authoring/citations.html)。

### 5.1 基本语法

| 类型 | 写法 | 输出 |
|------|------|------|
| 括号引用 | `[@frederick2002]` | (Frederick et al., 2002) |
| 多引用 | `[@frederick2002; @seaman2022]` | (Frederick et al., 2002; Seaman et al., 2022) |
| 叙事引用 | `@frederick2002` | Frederick et al. (2002) |
| 页码 | `[@frederick2002, pp. 33-35]` | (Frederick et al., 2002, pp. 33–35) |
| 仅年份 | `[-@frederick2002]` | (2002) |

**错误示例**（不能这样写）：
- ❌ `(Frederick et al., 2002)` — 纯文本，citeproc 不处理
- ❌ `Frederick et al. (2002)` — 纯文本

### 5.2 apaquarto 扩展功能

apaquarto 在标准 Quarto 引用基础上增加了：
- **所有格引用**：`@frederick2002 ['s]` → Frederick et al.'s (2002)
- **带页码所有格**：`@frederick2002 ['s, pp. 1-2]` → Frederick et al.'s (2002, pp. 1–2)
- **匿名审稿引用**：`mask: true` + `masked-citations` 字段

详见 [apaquarto 引用文档](https://wjschne.github.io/apaquarto/writing.html#citations)。

---

## 6. References 段

在正文末尾（Conflict of Interest 之后）加：

```markdown
# References

::: {#refs}
:::
```

`::: {#refs}:::` div 让 citeproc 在该位置插入自动生成的参考文献列表。
**不要手动写参考文献列表**——citeproc 从 `references.bib` 自动生成。

---

## 7. 图表

图表**直接放在正文里**（与文字混排）。apaquarto 通过 `floatsintext` 设置自动处理位置：
- `floatsintext: true`（默认）→ 图表嵌在正文
- `floatsintext: false` → 图表集中到 References 之后末尾

### 7.1 Markdown 图片（直接引用）

```markdown
![实验流程图](figures/image1.png){#fig-exp-proc width=80%}

: 实验流程图 {#fig-exp-proc}
```

### 7.2 R 代码生成图表（推荐）

apaquarto 支持 R 代码块直接生成图表（详见 [example.qmd](https://github.com/wjschne/apaquarto/blob/main/example.qmd)）：

````markdown
```{r}
#| label: fig-myplot
#| fig-cap: "图表标题（Title Case）"
#| fig-height: 4
#| fig-width: 6

library(ggplot2)
ggplot(data, aes(x, y)) + geom_point()
```
````

### 7.3 表格

```markdown
| 列1 | 列2 | 列3 |
|:---|:---:|---:|
| 数据 | 数据 | 数据 |

: 表格标题 {#tbl-label}
```

---

## 8. 渲染命令

```bash
cd manuscripts
export PATH=/root/.conda/envs/r-base/bin:/root/.TinyTeX/bin/x86_64-linux:$PATH
quarto render Manuscript.md --to apaquarto-pdf --output-dir ../docs --resource-path .
```

**关键参数**：
- `--to apaquarto-pdf`：用 apaquarto 扩展渲染
- `--output-dir ../docs`：输出到 `docs/` 目录
- `--resource-path .`：让 citeprocr.lua 找到 `references.bib`（**必须**）

---

## 9. 踩坑记录

| 问题 | 根因 | 修复 |
|------|------|------|
| `Unable to read the extension 'apaquarto'` | `_quarto.yml` 或 `_extensions/` 不在正确位置 | 确保都在 `manuscripts/` 下 |
| `CiteprocParseError: No citation element present` | 简化版 apa.csl 有问题 | 用 apaquarto 自带的完整 apa.csl（不要自建简化版）|
| `File bibliography.bib not found` | `references.bib` 不在 `manuscripts/` | 移到 `manuscripts/` |
| 引用显示为 `[@key]` 原文 | 用了 APA 文本格式 `(Author, Year)` | 改用 `[@key]` 语法 |
| 参考文献重复出现 | 手动写了 # References 段 + citeproc 自动生成 | 删手动列表，只保留 `::: {#refs}:::` |
| Figure 编号变 A1/A2/A3 | `# Tables and Figures` 标题被 apaquarto 当附录 | 去掉标题，直接放表格和图 |
| `[H]` 出现在 PDF | YAML 里有 `fig-pos: H` 或 `tbl-pos: H` | 删掉这些字段 |
| Figure caption 在图上方 | apaquarto 默认 `fig-cap-location: top` | 这是 apaquarto 的设计选择，与 APA 7 标准（caption 在图下方）不同 |
| Figure caption 位置改不了 | `_extension.yml` common 段强制 top | 需改 vendor 扩展（谨慎）|
| `CiteprocParseError` 编译失败 | 正文引用用了 `(Author, Year)` 而非 `[@key]` | 全部改为 `[@key]` 语法 |

---

## 版本历史

| 版本 | 日期 | 更新 |
|------|------|------|
| v2.1 | 2026-06-12 | **老板纠错**：① 3.3 安装命令改为 `cd manuscripts`（不是项目根），不复制；② 5 引用语法参考 Quarto Citations 文档 + apaquarto 扩展功能（所有格引用 `@key ['s]`）；③ 7 图表可直接放正文，apaquarto 自动处理 `floatsintext`，支持 R 代码块生成图表。 |
| v2.0 | 2026-06-12 | **重大重写**：修正 _quarto.yml/_extensions/references.bib 位置（全在 manuscripts/）；移除 header.tex；新增引用语法 + References div + 图表章节 + 渲染命令 `--resource-path .` + 踩坑记录。基于跨期选择年龄差异论文实战。 |
| v1.0 | 2026-06-04 | 初版：5 步关键修复 + YAML 头完整模板。源自记忆机制认知推断论文实战。 |
