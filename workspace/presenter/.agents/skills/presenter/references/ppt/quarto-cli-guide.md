# Quarto CLI 速查（presenter 技能专用）

> **本技能不使用任何 shell 包装脚本**。所有 PPT 工作直接调 `quarto` 命令。
> 这份速查覆盖 presenter 技能会用到的所有子命令。

---

## 1. 渲染（核心命令）

### 编译 .qmd → .pptx

```bash
quarto render deck.qmd --to pptx
```

### 编译 .qmd → .html（revealjs）

```bash
quarto render deck.qmd --to revealjs
```

### 同时输出两种格式

```bash
quarto render deck.qmd
```

> YAML 头部声明了哪些 `format: [pptx, revealjs]`，Quarto 自动全部渲。

### 指定输出文件名

```bash
quarto render deck.qmd --to pptx --output final.pptx
```

### 4:3 / 16:9 切换

```bash
# 16:9 宽屏（默认，推荐）
quarto render deck.qmd --to pptx

# 4:3 传统（不推荐，已过时）
# YAML 里指定
```

---

## 2. 预览（开发热重载）

### 启动热重载预览（推荐开发时用）

```bash
quarto preview deck.qmd
```

浏览器自动打开 http://localhost:XXXX/ ，改 .qmd 自动刷新。

### 预览到指定格式

```bash
quarto preview deck.qmd --to pptx
quarto preview deck.qmd --to revealjs
```

> `quarto preview` 是**唯一**需要本地服务器的命令。`render` 不需要。

---

## 3. 章节库标准命令

### 编译章节 pptx（带品牌母版）

```bash
quarto render chXX.pptx.qmd --to pptx
```

YAML 头部已指 `reference-doc: assets/templates/brand-template-teal-orange.pptx`，无需额外参数。

### 编译章节 + 表格样式后处理

```bash
# Step 1: Quarto 渲染
quarto render chXX.pptx.qmd --to pptx

# Step 2: 表格样式注入（覆盖 Office 默认丑陋表格）
python3 scripts/style_pptx_tables.py chXX.pptx -o chXX_styled.pptx
```

> **没有 shell 包装**。这两行直接打。如果你觉得烦，写个 `make` rule 或 `package.json` script——但**不是 .sh 包装**。

### 双格式输出

```bash
quarto render chXX.qmd
```

> 需要 .qmd 头部同时声明 `format: [pptx, revealjs]`，否则只出 yaml 里第一个 format。

---

## 4. 母版（reference-doc）

```yaml
# .qmd 头部
format:
  pptx:
    reference-doc: assets/templates/brand-template-teal-orange.pptx
```

引用母版后，**所有页**用该母版的 slide master / layouts 装饰。换母版只改这一行。

---

## 5. 调试 / 排错

### 详细日志

```bash
quarto render deck.qmd --to pptx --debug
```

### 只渲不打开浏览器

```bash
quarto render deck.qmd --to pptx --no-preview
```

### 强制重新渲（绕过缓存）

```bash
quarto render deck.qmd --to pptx --force
```

### 清理中间产物

```bash
quarto clean deck.qmd
# 或清理全部
quarto clean
```

### 看 Quarto 版本

```bash
quarto --version
```

---

## 6. 装依赖

### 装 Chromium（revealjs 转 PDF / 截图需要）

```bash
quarto install chromium
```

### 装 TinyTex（要 LaTeX/PDF 输出才需要，presenter 不用）

```bash
quarto install tinytex
```

---

## 7. 项目级命令

### 在项目目录里渲指定文件

```bash
cd /path/to/chapter
quarto render ch14.pptx.qmd --to pptx
```

### 列项目

```bash
quarto list
```

---

## 8. 完整参数参考

```bash
quarto render --help
```

`--to`、`--output`、`--debug`、`--force`、`--no-preview` 是 presenter 技能最常用的几个。

---

## 9. 速查表

| 想做的事 | 命令 |
|----------|------|
| 渲 pptx | `quarto render deck.qmd --to pptx` |
| 渲 html | `quarto render deck.qmd --to revealjs` |
| 双格式 | `quarto render deck.qmd` |
| 改名输出 | 加 `--output final.pptx` |
| 开发预览 | `quarto preview deck.qmd` |
| 看错误 | 加 `--debug` |
| 强刷 | 加 `--force` |
| 清缓存 | `quarto clean deck.qmd` |
| 装 Chromium | `quarto install chromium` |
| 看版本 | `quarto --version` |

---

## 10. 为什么不写 .sh 包装

之前有 `scripts/render.sh` 和 `scripts/render-with-tables.sh`，2026-06-04 全删了。理由：

1. **Quarto CLI 本身就是完整接口**。`--to`、`--output`、`--debug` 等参数已经覆盖 90% 场景
2. **包装 = 学习额外抽象**。不如直接学 Quarto CLI，迁移性更好
3. **包装 = 维护负担**。Quarto 升版改了 CLI，包装要跟着改
4. **不优雅**。"一行 `quarto render`" 已经够简洁，再包一层 `.sh` 是噪声

如果未来有**复杂的多文件并行 / 依赖链 / 部署**需求，写 `Makefile` 或 `package.json` script——**不是 .sh**。
