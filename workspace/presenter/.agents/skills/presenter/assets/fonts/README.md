# fonts/

自定义字体（.ttf / .otf / .woff / .woff2）。

引用方式（CSS @font-face）：

```scss
/* styles/custom.scss */
@font-face {
  font-family: "Brand";
  src: url("../assets/fonts/brand-regular.woff2") format("woff2");
}

.reveal { font-family: "Brand", sans-serif; }
```

或在 reference-doc 的 Slide Master 里改字体设置。
