# styles/

自定义主题（SCSS / CSS），主要用于 **revealjs**：

```yaml
# deck.qmd
format:
  revealjs:
    theme: [default, ../assets/styles/custom.scss]
```

示例 `custom.scss`：

```scss
/*-- scss:defaults --*/
$body-bg: #fafafa;
$body-color: #222;
$link-color: #c0392b;
$heading-color: #2c3e50;

/*-- scss:rules --*/
.reveal h1 { border-bottom: 3px solid $link-color; }
```

详见：[references/ppt/quarto-theme.md](../references/ppt/quarto-theme.md)
