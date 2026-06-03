# Quarto PPT 主题与样式

> 主题定制详细文档。SKILL.md 第 1.5 节只放速查。

---

## 1. RevealJS 主题

### 内置 11 套

`beige` `blood` `dark` `default` `dracula` `league` `moon` `night` `serif` `simple` `sky` `solarized`

```yaml
format:
  revealjs:
    theme: dracula
```

### 自适应亮/暗

```yaml
format:
  revealjs:
    theme:
      light: [default, custom-light.scss]
      dark: [dark, custom-dark.scss]
```

---

## 2. 自定义主题（SCSS）

```yaml
format:
  revealjs:
    theme: [default, custom.scss]
```

`custom.scss`：

```scss
/*-- scss:defaults --*/
$body-bg: #fafafa;
$body-color: #222;
$link-color: #c0392b;
$heading-color: #2c3e50;
$presentation-font-size-root: 28px;

/*-- scss:rules --*/
.reveal .slide-title {
  font-weight: 700;
  letter-spacing: -0.02em;
}

.reveal h1 {
  color: $heading-color;
  border-bottom: 3px solid $link-color;
  padding-bottom: 0.2em;
}
```

> 关键变量：`$body-bg` `$body-color` `$link-color` `$heading-color` `$presentation-font-size-root` `$code-color`

---

## 3. PPTX 主题：用 reference-doc 套品牌

PowerPoint 没有"主题"概念，要用**母版模板**：

```yaml
format:
  pptx:
    reference-doc: assets/templates/brand-template.pptx
```

### 模板必备布局（Pandoc 按名字匹配）

模板 Slide Master 必须包含这些布局名：

- `Title Slide`
- `Title and Content`
- `Section Header`
- `Two Content`
- `Comparison`
- `Content with Caption`
- `Blank`

缺失的布局 Pandoc 会告警并兜底。

### 生成默认模板做起点

```bash
quarto pandoc -o template.pptx --print-default-data-file reference.pptx
# 用 PowerPoint 打开 template.pptx → 修改 Slide Master → 保存
```

### 在 PowerPoint 中改色

1. 打开 `brand-template.pptx`
2. View → Slide Master
3. 选中主版式 → Format Background → Solid Fill → 选色
4. 字体：Home → Font → 选品牌字体
5. 关闭母版视图，回到普通视图保存

### 临时文字颜色

```html
<span style="color:#c0392b">红字</span>
```

> 颜色字体改在 reference-doc 的 Slide Master 里做最稳。临时颜色用 `<span style>`。

---

## 4. 品牌一致性

### 一致性要点

- **配色**：每份 PPT 用同一套主色（建议 3-5 色）
- **字体**：标题 / 正文 / 代码各一个字体，不混用
- **布局**：固定几种版式（封面/目录/正文/章节/小结/致谢）
- **页脚**：左下角放章节名，右下角放页码

### 配色推荐工具

- Adobe Color：https://color.adobe.com
- Coolors：https://coolors.co
- 中国色：https://zhongguose.com

详见 [references/color-theory-guide.md](../color-theory-guide.md) / [brand-guide.md](../brand-guide.md)
