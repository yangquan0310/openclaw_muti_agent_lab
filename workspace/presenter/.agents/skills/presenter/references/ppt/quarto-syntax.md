# Quarto PPT 核心语法

> 完整语法参考。SKILL.md 第 1 节只放速查，详细示例与说明在此。

---

## 1. 幻灯片分隔

| 语法 | 用途 |
|------|------|
| `# 一级标题` | 分隔页（Section Header） |
| `## 二级标题` | 普通幻灯片（默认） |
| `---`（水平线）| 强制分隔一张幻灯片 |
| 标题后 `{.section}` | 显式声明为分隔页 |
| 标题后 `{.inverse}` | 反色（深色背景）|

> YAML 里 `slide-level` 决定哪一级标题对应新幻灯片。pptx 默认 2，revealjs 默认 1。

---

## 2. 列表

```markdown
- 普通列表
- 列表项二
  - 嵌套项
- 列表项三
```

- 配合 `incremental: true` → 逐条出现
- 数字列表：把 `-` 换成 `1.` `2.`
- 任务列表：`- [ ]` `- [x]`

---

## 3. 两列布局

```markdown
:::: {.columns}
::: {.column width="50%"}
左列内容
:::
::: {.column width="50%"}
右列内容
:::
::::
```

- `width` 可写 `40%` / `300px` / `5em`
- 三列：再加一个 `.column` 块
- 不等宽：左 30% / 右 70%

---

## 4. 代码块

**纯语法高亮**（无需 Jupyter 引擎）：

````markdown
```python
# 纯语法高亮，不执行
def f(x): return x**2
```
````

**带引擎的代码块**（执行并嵌入结果）：

````markdown
```{python}
#| echo: false
#| fig-width: 8
#| fig-height: 4
import matplotlib.pyplot as plt
plt.plot([1, 2, 3])
```
````

> 需要 `conda install jupyter nbformat`。

支持语言：`python` `r` `julia` `javascript` `bash` `sql` `mermaid` ...

---

## 5. 公式

```markdown
行内：$E=mc^2$

独立：
$$
\int_0^{\infty} e^{-x^2}dx = \frac{\sqrt{\pi}}{2}
$$
```

支持 LaTeX 数学语法全集。

---

## 6. 图片

```markdown
![替代文字](path/to/image.png){width=80%}

# 居中、附标题
![图](image.png){width=70% fig-align="center"}
```

- 路径相对于 .qmd 所在目录
- 支持 PNG/JPG/SVG/WebP
- `{width="80%"}` 或 `{width=400px}` 都可
- 远程 URL 要带扩展名；调试可用 `https://placehold.co/600x300`

---

## 7. 表格

```markdown
| 列1 | 列2 | 列3 |
|----:|----:|----:|
|  12 |  34 |  56 |
|  78 |  90 |  12 |
```

- 对齐：`----` 左对齐 / `:---:` 居中 / `----:` 右对齐
- 复杂表：HTML 直接嵌入

---

## 8. 演讲者备注

```markdown
## 幻灯片标题

可见内容

::: {.notes}
这些只在演讲者视图出现，不会上屏。
:::
```

- pptx → 生成"备注页"
- revealjs → 按 `s` 键进入演讲者视图

---

## 9. 片段动画（revealjs 专享）

```markdown
::: {.fragment}
第一段
:::

::: {.fragment .fade-in}
第二段（淡入）
:::

::: {.fragment .highlight-red}
第三段（高亮红色）
:::

::: {.fragment .strike}
第四段（删除线）
:::
```

可叠加多个类：`{.fragment .fade-up .highlight-blue}`

---

## 10. 背景图 / 视频（revealjs）

```markdown
## 背景图 {background-image="images/bg.jpg" background-size="cover"}

## 视频背景 {background-video="videos/loop.mp4" background-loop=true}

## 背景颜色 {background-color="#f5f5f5"}
```

---

## 11. 嵌入图表

### 静态图（最常用）

```markdown
![趋势图](charts/trend.png){width=80%}
```

### 动态图（需 Jupyter）

````markdown
```{python}
#| echo: false
import matplotlib.pyplot as plt
import numpy as np
x = np.linspace(0, 2*np.pi, 100)
plt.plot(x, np.sin(x))
plt.title("Sine wave")
plt.show()
```
````

### Mermaid 流程图

````markdown
```{mermaid}
flowchart LR
  A[开始] --> B{判断}
  B -->|是| C[执行]
  B -->|否| D[结束]
```
````

### Graphviz

````markdown
```{dot}
digraph G {
  A -> B;
  B -> C;
}
```
````
