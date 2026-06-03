# 范式 ④ 严格 APA 7 manuscript mode（apaquarto-pdf）配置指南

> **2026-06-04 实战沉淀**：源自记忆机制认知推断论文（51 页 / 476KB）。
> **核心目标**：让 Quarto 接管 APA 7 期刊稿件结构，产出**独立标题页 + 独立摘要页 + Author Note + Running head + 页码右上角 + 双倍行距**的完整 APA 7 manuscript。

---

## 1. 何时使用范式 ④

| 场景 | 用哪个范式 |
|------|----------|
| 投稿心理学/教育学/社科类期刊 | **范式 ④**（APA 7 强制）|
| 毕业论文中要 APA 7 manuscript 排版的章节 | **范式 ④** |
| 课程作业、研究现状、文献综述（投稿用）| 范式 ②（基础 Quarto + apa.csl，足够）|
| 书/教材/多章节文档 | 范式 ① |
| 科普/博文 | 范式 ③ |

**判断口诀**：要"APA 7 manuscript 期刊投稿风" → 范式 ④；要"APA 7 参考文献" → 范式 ②。

---

## 2. 环境准备（一次性）

### 2.1 R + knitr（apaquarto 5.0.18 预检查要）

```bash
# r-base conda 环境已存在（2026-06-04 验证）
/root/.conda/envs/r-base/bin/R --version
# R version 4.3.1 (2023-06-16) -- "Beagle Scouts"

# 激活 + 配 PATH（必须）
export PATH=/root/.conda/envs/r-base/bin:/root/.TinyTeX/bin/x86_64-linux:$PATH
```

### 2.2 Quarto + tinytex（已装）

```bash
quarto --version   # 1.7.34
xelatex --version  # TeX Live 2026（tinytex）
```

### 2.3 CJK 字体

```bash
fc-list :lang=zh | grep "AR PL SungtiL GB"   # 验证
# 0 输出 → 装：apt install fonts-arphic-gbsn00lp
```

---

## 3. 项目初始化（每个新项目走一次）

### 3.1 建项目根 `_quarto.yml`（**真正的根因**）

> **关键认知**：Quarto 需要 `_quarto.yml` 识别项目根，才能从子目录 `manuscripts/` 上溯找到 `_extensions/apaquarto/`。
> 缺这个文件 → apaquarto-pdf 找不到扩展 → 退回 Pandoc 默认。

```yaml
# 项目根 _quarto.yml（**只有这两行，够了**）
project:
  type: default
```

> ❌ **不要**用 `type: book`（那是范式 ① 书的）。
> ❌ **不要**用 `type: manuscript`（Quarto 1.7 还没原生 manuscript type）。

### 3.2 装 apaquarto 扩展（项目级）

```bash
cd /项目根
quarto add wjschne/apaquarto
# 自动装到 ./_extensions/apaquarto/（48 个文件，含完整 apa.csl）
```

**验证**：
```bash
ls _extensions/apaquarto/
# 看到 apa.csl  apanote.lua  apatemplate.tex  doc-class.tex  ...
```

### 3.3 复制 `header.tex`（CJK 字体 + APA 7 段间距 + 防溢出）

```bash
cat > manuscripts/header.tex <<'EOF'
% ========== CJK 字体配置（apaquarto 默认 Times Roman 不支持中文，必须显式声明）==========
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

% ========== 防段落右侧溢出（v8.20.0 铁律：\sloppy + \tolerance=1000 + \emergencystretch=3em）==========
\sloppy
\tolerance=1000
\emergencystretch=3em
EOF
```

---

## 4. .md 文件 YAML 头完整模板

```yaml
---
title: "论文完整标题（APA 7 Title Case）"
shorttitle: "Running head（≤50 字符大写）"

author:
  - name: "杨权"
    orcid: "0000-0001-6201-4174"
    email: "yangquan0310@163.com"
    corresponding: true        # 🆕 至少一个作者填 true
    roles:                     # 🆕 CRediT: Contributor Roles Taxonomy
      - conceptualization
      - writing
      - methodology
    affiliations:
      - id: ccnupsy            # 🆕 机构 ID，多个作者共享同一机构用 ref:
        name: "华中师范大学心理学院"
        department: "心理学院"
        city: "武汉"
        region: "湖北"
        country: "中国"
  # 多作者：- name: "作者二"  ...  affiliations: - ref: ccnupsy

date: "2026-06-04"
keywords: [关键词1, 关键词2, 关键词3, 关键词4, 关键词5]

abstract: |
  摘要正文（APA 7 严格格式，150-250 字）。
  研究背景 → 主要发现（2-3 句）→ 结论（1 句）。

author-note:                   # 🆕 必填，否则 apaquarto 报错
  disclosures:
    conflict-of-interest: "作者声明无利益冲突。"
  # 可选字段：
  # author-contributions: "第一作者负责 X，第二作者负责 Y。"
  # funding: "本研究受 X 基金资助（项目号：XXXX）。"

floatsintext: true             # 🆕 APA 7：图表嵌在正文里（不集中到末尾）
numbered-lines: false          # 🆕 关闭逐行编号（投稿用）
word-count: false              # 🆕 关闭自动字数统计
draft-date: false              # 🆕 关闭草稿日期

format:                        # 🆕 用 apaquarto-pdf，**不要**用 pdf:
  apaquarto-pdf:
    documentmode: man          # 🆕 manuscript mode（journal article 风格）
    keep-tex: true             # 保留 .tex 源码（排错用）
    include-in-header: "header.tex"

# ❌ 不要写 bibliography: + csl: 字段
# apaquarto 自带 references.bib（默认）+ 完整 apa.csl
# 重复写会冲突
---
```

---

## 5. 渲染命令

### 5.1 基础渲染

```bash
cd 项目根
quarto render manuscripts/全文整合稿.md --to apaquarto-pdf
```

输出位置：`manuscripts/全文整合稿.pdf`（默认）。

### 5.2 输出到 `docs/`（铁律：项目根 docs/）

```bash
quarto render manuscripts/全文整合稿.md --to apaquarto-pdf --output-dir docs
mv docs/全文整合稿.pdf docs/记忆机制的认知推断.pdf
```

### 5.3 排错渲染（保留 .tex）

```bash
# keep-tex: true 已经在 YAML 头，渲染后看：
ls manuscripts/全文整合稿.tex
# 检查 .tex 的 ① 字体声明 ② 标题页结构 ③ author-note 渲染
```

---

## 6. 5 步关键修复的踩坑记录

| 步 | 错误信息 | 根因 | 修复 |
|------|---------|------|------|
| 1 | `Rscript not found` | apaquarto 预检查要 R | `export PATH=/root/.conda/envs/r-base/bin:$PATH` |
| 2 | `xelatex not found` 或 `! LaTeX Error: File 'apa7.sty' not found` | tinytex 不在 PATH | `export PATH=/root/.TinyTeX/bin/x86_64-linux:$PATH` |
| 3 | `apaquarto-pdf format not found` 或退回 Pandoc 默认 | ①项目根没 `_quarto.yml` ②扩展没装 | `touch _quarto.yml` + `echo "project:\n  type: default" > _quarto.yml` + `quarto add wjschne/apaquarto` |
| 4 | 渲染出 PDF 但**没标题页/没 author note** | `.md` YAML 头写的是 `format: pdf:` 而非 `format: apaquarto-pdf:` | 改 `pdf:` → `apaquarto-pdf:` |
| 5 | 渲染出 PDF 但**没 author note** | `author-note:` 字段缺失 | 补 `author-note: disclosures: conflict-of-interest: "..."` |

---

## 7. 常见问题排错

### 7.1 "I'm using apaquarto but getting Pandoc default output"

**根因**：`.md` YAML 头的 `format:` 块写的是 `pdf:` 而非 `apaquarto-pdf:`。

**检查**：
```bash
grep "format:" manuscripts/全文整合稿.md
# 必须看到 format:  apaquarto-pdf:，不是 format:  pdf:
```

### 7.2 中文显示成方块/乱码

**根因**：`header.tex` 没正确加载中文字体。

**修复**：检查 `header.tex` 是否有：
```latex
\usepackage{xeCJK}
\setCJKmainfont{AR PL SungtiL GB}
```

验证字体存在：`fc-list :lang=zh | grep "AR PL SungtiL GB"`。

### 7.3 段落右侧超出（文字溢出右边距）

**根因**：apaquarto 默认 `\emergencystretch` 不够。

**修复**：在 `header.tex` 末尾加：
```latex
\sloppy
\tolerance=1000
\emergencystretch=3em
```

### 7.4 参考文献格式不对

**根因**：范式 ④ 不需要 `csl:` 字段，apaquarto 自带完整 apa.csl。

**检查**：YAML 头**不要**有 `csl:` 行。

### 7.5 找不到 `references.bib`

**根因**：apaquarto 默认在**项目根**找 `references.bib`（不在 manuscripts/）。

**修复**：把 `references.bib` 放在**项目根**（与 `_quarto.yml` 同级）。

---

## 8. 范式 ④ vs 范式 ② 对比

| 维度 | 范式 ②（基础 Quarto + apa.csl）| 范式 ④（apaquarto manuscript）|
|------|------------------------------|-------------------------------|
| 标题页 | ❌ 没（标题直接放正文）| ✅ 独立 title page |
| 摘要页 | ❌ 没（摘要放第一段）| ✅ 独立 abstract page |
| Author Note | ❌ 没 | ✅ ORCID + Conflict of interest + CRediT roles + 通讯作者 |
| Running head | ❌ 没 | ✅ 上限 50 字符大写 |
| 页码位置 | 默认底部居中 | ✅ 右上角 |
| 行距 | 单倍（默认）| ✅ 双倍 |
| documentclass | article（Pandoc 默认）| apacls（APA 7 宏包）|
| 图表 | 浮动 | floatsintext（嵌在正文）|
| 安装复杂度 | 低 | 高（5 步修复 + R 环境 + 扩展）|
| 适用 | 课程作业、研究现状 | 投稿期刊、正式论文 |

**判断口诀**：
- 投稿 / 严格 APA 7 期刊稿件 → **范式 ④**
- 课程作业 / 简单论文 → 范式 ②

---

## 9. 完整实战示例

参考项目：`/data/disk/仓库/记忆机制认知推断论文/`

- 根 `_quarto.yml`（空壳 2 行）
- `_extensions/apaquarto/`（48 文件，quarto add 装）
- `manuscripts/header.tex`（CJK + APA 7 + 防溢出三件套）
- `manuscripts/全文整合稿.md`（apaquarto YAML 头 + 全文）
- `references.bib`（在**项目根**，不在 manuscripts/）
- 输出：`docs/记忆机制的认知推断.pdf`（51 页 / 476KB）

---

## 版本历史

| 版本 | 日期 | 更新 |
|------|------|------|
| v1.0 | 2026-06-04 | 初版：5 步关键修复 + YAML 头完整模板 + 踩坑记录。源自记忆机制认知推断论文实战。 |
