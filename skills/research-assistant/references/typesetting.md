# 排版原则

> 使用 pandoc + pandoc.yaml + reference.bib + apa.csl 进行协作排版。

---

## 核心原则

1. **分离内容与格式**：内容使用 Markdown，格式由 pandoc.yaml + CSL 控制
2. **统一引用管理**：所有参考文献存入 reference.bib，格式由 apa.csl 统一
3. **协作友好**：多人协作时，各自负责的章节存为独立 .md 文件，主文件通过 `input-files` 包含

---

## 文件分工

| 文件 | 作用 | 负责人 |
|------|------|--------|
| `pandoc.yaml` | 编译配置（引擎、变量） | 项目统一 |
| `header.tex` | LaTeX 局部调整（必要） | 按需修改 |
| `reference.bib` | 参考文献数据库 | 所有人按需添加 |
| `apa.csl` | 引用样式（APA 第七版） | 项目统一 |
| `{chapter}.md` | 各章节内容 | 各 Agent 负责 |
| `全文整合稿.md` | 整合所有章节 | 写作助手 |

---

## pandoc.yaml 标准结构

```yaml
standalone: true
pdf-engine: xelatex
from: markdown
to: latex
input-files:
  - 章节1.md
  - 章节2.md
  - 章节3.md
output-file: 论文.pdf
bibliography: reference.bib
csl: apa.csl
citeproc: false
number-sections: true
include-in-header: header.tex
variables:
  mainfont: "Noto Serif CJK SC"
  CJKmainfont: "Noto Serif CJK SC"
  geometry:
    - top=1in
    - bottom=1in
    - left=1in
    - right=1in
  fontsize: 12pt
  papersize: a4
metadata:
  title: "论文标题"
  author: "作者一 作者二"
```

---

## header.tex 示例

```tex
\usepackage{indentfirst}\setlength{\parindent}{2em}\sloppy\tolerance=1000\emergencystretch=3em
```

---

## reference.bib 添加文献

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

---

## 编译命令

```bash
cd manuscripts
pandoc --defaults pandoc.yaml
```

---

## 常见问题

| 问题 | 解决方案 |
|------|----------|
| 中文字体溢出 | 在header.tex中添加 `\sloppy` |
| 缺少字体 | 使用 `fc-list :lang=zh` 检查可用字体 |
| 引用格式不对 | 确认 apa.csl 路径正确 |
