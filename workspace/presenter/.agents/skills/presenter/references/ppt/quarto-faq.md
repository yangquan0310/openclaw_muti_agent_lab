# Quarto PPT 常见问题

> 排错参考。SKILL.md 第 1.10 节只放最常见 6 个，详细案例在此。

---

## Q1. 中文 / 字体乱码

**现象**：中文显示为方块或乱码

**解决**：
1. 在 reference-doc 的 Slide Master 里：
   - 选中所有占位符
   - 字体 → 亚洲字体选"微软雅黑"或"思源黑体"
   - 西文字体选"Calibri"或品牌字体
2. YAML 加上 `lang: zh-CN`
3. Linux 服务器：用 `fc-list :lang=zh` 检查已装中文字体

---

## Q2. 渲染 .pptx 后配色丢了

**现象**：在 qmd 里写的颜色在 .pptx 里不生效

**原因**：Pandoc 渲染 .pptx 的 CSS 能力有限，颜色全在 reference-doc 里配

**解决**：
- **首选**：在 reference-doc 的 Slide Master 里改色
- **临时**：在 qmd 里用 `<span style="color:#xxx">` 内联覆盖

---

## Q3. 图片不显示

**现象**：预览或 PPT 里图片是破图

**解决**：
- 路径用相对路径（相对于 .qmd）
- 远程 URL 要带扩展名（`?text=...` 不行就用 `https://placehold.co/600x300`）
- 检查文件权限
- 中文字符路径可能有问题，建议全英文

---

## Q4. revealjs 的 Python 代码块报错 "no module nbformat"

**现象**：
```
ModuleNotFoundError: No module named 'nbformat'
```

**解决**：
- 装 Jupyter：`conda install jupyter nbformat`
- 或改用三反引号纯语法高亮（不需要引擎）

---

## Q5. 一份 .qmd 同时输出 pptx 和 revealjs

```yaml
format:
  pptx: default
  revealjs: default
```

`quarto render deck.qmd` 同时得到两个文件。

---

## Q6. 打印 revealjs 为 PDF

**方法 A**（浏览器）：
1. 浏览器打开 `deck.html`
2. URL 末尾加 `?print-pdf`
3. Ctrl+P → 另存 PDF

**方法 B**（单文件）：
```bash
quarto render deck.qmd --to revealjs --embed-resources
```

---

## Q7. 字体太小 / 太大

**revealjs**：
```yaml
format:
  revealjs:
    theme: [default, custom.scss]
```
```scss
$presentation-font-size-root: 32px;  /* 默认 28px */
```

**pptx**：
在 reference-doc 的 Slide Master 里改字号

---

## Q8. 段落间距太大

**revealjs**：
```scss
.reveal p { margin: 0.5em 0; }
```

**pptx**：在 reference-doc 的 Slide Master 里调段落格式

---

## Q9. 列表/代码块对齐问题

**常见原因**：
- 中英文混排时全角空格被识别为英文
- Tab 和空格混用

**解决**：
- 用 2 空格缩进，不用 Tab
- 中文段落用全角标点

---

## Q10. 报 "file not found" 但文件明明存在

**检查**：
- 路径是否相对当前工作目录而非 .qmd 目录
- 文件名大小写（Linux 严格区分）
- 软链接是否断链

**调试**：
```bash
ls -la path/to/file
quarto render deck.qmd --debug
```

---

## Q11. 渲染慢 / 卡住

**原因**：
- 大量 Python 代码块（每次都跑）
- 大图片未压缩
- Mermaid 渲染

**解决**：
- 用 `#| eval: false` 跳过执行
- 图片预先压缩到 200KB 以内
- 把 Python 块改成静态图

---

## Q12. 怎么预览 .pptx 的效果

**方法 A**：用 LibreOffice 转 PDF 看效果
```bash
libreoffice --headless --convert-to pdf deck.pptx
```

**方法 B**：直接 PowerPoint 打开看

**方法 C**：revealjs 模式预览
```yaml
format:
  pptx: default
  revealjs: default  # 同样内容用 revealjs 看排版
```

---

## Q13. 怎么加页码

**revealjs**：
```yaml
format:
  revealjs:
    slide-number: true
```

**pptx**：在 reference-doc 的 Slide Master 里加页码占位符

---

## Q14. 怎么加 logo

**revealjs**：
```yaml
format:
  revealjs:
    logo: images/logo.png
```

**pptx**：在 reference-doc 的 Slide Master 里插入 logo 占位符

---

## Q15. 升级 Quarto 后样式变了

Quarto 升级可能改变默认行为。解决方案：
1. 固定主题版本号
2. 升级前先看 changelog
3. 在 reference-doc 里固化样式
