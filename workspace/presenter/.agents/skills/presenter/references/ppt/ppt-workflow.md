# PPT 任务工作流

> 完整工作流。SKILL.md 第 1.12 节放精简版，详细步骤与模板清单在此。

---

## 1. 决策阶段（必做）

明确以下 4 点：

| 决策 | 选项 | 默认 |
|------|------|------|
| 输出格式 | `pptx` / `revealjs` | pptx |
| 主题/品牌 | 公司母版 / 内置主题 | simple |
| 模板 | basic / lesson / 自建 | lesson |
| 是否要 PDF | 是 / 否 | 否 |

> 收齐决策后再开始写内容。**最常见的返工原因是没明确"目标受众"和"使用场景"**。

---

## 2. 模板选择

| 场景 | 模板 | 文件 |
|------|------|------|
| 简单 5-10 页 | 最小模板 | `assets/templates/basic-pptx.qmd` |
| 课程/培训 | 课程模板（封面+目录+章节+小结）| `assets/templates/lesson-pptx.qmd` |
| 内部技术分享 | 简单 HTML | `assets/templates/basic-revealjs.qmd` |
| 公司有现成 PPT 母版 | 套 reference-doc | `assets/templates/brand-template.pptx` |
| 旧 .pptx 资产维护 | python-pptx | `scripts/ppt/`（**DEPRECATED**）|

复制模板：
```bash
cp assets/templates/lesson-pptx.qmd ./deck.qmd
```

---

## 3. 编写内容

### 内容结构（课程模板示例）

```
# 封面
## 学习目标
# 章节一
## 概念引入
## 定义
## 关键要素
## 案例
# 章节二
## 方法
## 公式
## 代码
## 注意事项
# 总结
## 本讲回顾
## 思考题
## 参考资料
## 致谢
```

### 编写要点

- **一页一个核心信息**：避免大段文字
- **列表用要点**：3-7 个最佳
- **代码必须可运行**：示例不能有 bug
- **图片必标注来源**：避免版权问题
- **每页加备注**：写给演讲者看

### 拆分章节文件（推荐）

```
project/
├── deck.qmd                # 主文件
└── chapters/               # 子文件
    ├── 01-intro.qmd
    ├── 02-content.qmd
    └── 03-summary.qmd
```

主文件引用：
```markdown
{{< include chapters/01-intro.qmd >}}
{{< include chapters/02-content.qmd >}}
```

---

## 4. 渲染

```bash
# 渲染指定格式
quarto render deck.qmd --to pptx
quarto render deck.qmd --to revealjs

# 同时输出两种
quarto render deck.qmd

# 实时预览（推荐开发时用）
quarto preview deck.qmd

# 用本仓库的封装脚本
bash scripts/render.sh deck.qmd pptx
bash scripts/render.sh deck.qmd revealjs
bash scripts/render.sh deck.qmd both
```

---

## 5. 调样式

### revealjs

1. 创建 `custom.scss`：
   ```scss
   /*-- scss:defaults --*/
   $body-bg: #fafafa;
   $heading-color: #2c3e50;
   ```
2. YAML 引用：
   ```yaml
   format:
     revealjs:
       theme: [default, custom.scss]
   ```
3. 实时预览：`quarto preview deck.qmd`

### pptx

1. 打开 `assets/templates/brand-template.pptx`（用 PowerPoint）
2. View → Slide Master
3. 改背景色、字体、页脚
4. 保存回原位
5. 重新渲染

详见 [quarto-theme.md](quarto-theme.md)

---

## 6. 嵌入资产

```markdown
![图](images/case.png){width=80%}
```

```markdown
| 字段 | 值 |
|------|----|
| 数量 | 42 |
```

```python
# 代码块
print("hello")
```

```markdown
公式：$E=mc^2$

独立公式：
$$
\int_0^{\infty} e^{-x^2}dx = \frac{\sqrt{\pi}}{2}
$$
```

---

## 7. 演讲者备注

每页加：

```markdown
## 幻灯片标题

可见内容

::: {.notes}
这页是给演讲者看的。讲解时强调 XX 概念。
可以举一个生活化的例子：……
:::
```

---

## 8. 质量自检

用 [references/quality-standards.md](../quality-standards.md) 逐项检查：

- [ ] 每页只表达一个核心信息
- [ ] 字体大小 ≥ 24px（后排能看清）
- [ ] 配色对比度足够
- [ ] 图、表、公式有标题/编号
- [ ] 演讲者备注完整
- [ ] 中文字体显示正常
- [ ] 页码正确
- [ ] 末尾有致谢页

---

## 9. 交付

```bash
# 最终渲染
quarto render deck.qmd --to pptx
# → deck.pptx（可直接交付）

# 或者
quarto render deck.qmd --to revealjs --embed-resources
# → deck.html（单文件，方便分发）
```

提交：
```bash
git add deck.qmd images/ custom.scss deck.pptx
git commit -m "feat(ppt): 新增 XXX 课件"
```

---

## 10. 提交督导审核

完成视觉设计后，提交督导（auditor）做质量终审。

---

## 完整示例

完整工作流见 [assets/examples/](../../assets/examples/)：
- `demo-pptx.qmd` — PPTX 完整示例
- `demo-revealjs.qmd` — RevealJS 完整示例
- `demo-with-template.qmd` — PPTX + reference-doc 示例
