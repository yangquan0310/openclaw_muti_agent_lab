# charts/

可复用图表（PNG / SVG）。Quarto 调用方式：

```markdown
![趋势图](charts/trend.png){width=80%}
```

或用 Python 计算块动态生成（需 `conda install jupyter nbformat`）：

````markdown
```{python}
#| echo: false
#| fig-width: 8
#| fig-height: 4
import matplotlib.pyplot as plt
plt.plot([1, 2, 3])
```
````
