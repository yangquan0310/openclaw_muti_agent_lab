# 物理工具指南

> 常用物理工具和数值计算库

---

## 一、数值计算工具

### 1.1 Python 科学计算栈

| 库 | 用途 | 导入方式 |
|----|------|----------|
| NumPy | 数值数组、线性代数 | `import numpy as np` |
| SciPy | 特殊函数、数值积分、优化 | `import scipy as sp` |
| SymPy | 符号计算、解析求解 | `import sympy as sp` |
| mpmath | 高精度浮点运算 | `import mpmath as mp` |

### 1.2 常用数值方法

**数值积分**

```python
from scipy import integrate

# 定积分
result, error = integrate.quad(lambda x: x**2, 0, 1)

# 二重积分
result = integrate.dblquad(lambda x, y: x*y, 0, 1, lambda x: 0, lambda x: x)
```

**微分方程求解**

```python
from scipy.integrate import solve_ivp

def odes(t, y):
    return [y[1], -y[0]]

sol = solve_ivp(odes, [0, 10], [0, 1], dense_output=True)
```

**矩阵特征值**

```python
import numpy as np

A = np.array([[2, 1], [1, 2]])
eigenvalues, eigenvectors = np.linalg.eig(A)
```

### 1.3 特殊函数

```python
from scipy import special

# 贝塞尔函数
special.jn(n, x)

# 勒让德多项式
special.legendre(n)(x)

# 伽马函数
special.gamma(z)

# 误差函数
special.erf(x)
```

---

## 二、符号计算工具

### 2.1 SymPy 基础

```python
import sympy as sp

# 定义符号
x, y, z = sp.symbols('x y z')
n = sp.symbols('n', integer=True)

# 定义表达式
expr = (x + y)**3
expr.expand()

# 求导
sp.diff(expr, x)

# 积分
sp.integrate(expr, x)

# 方程求解
sp.solve(x**2 - 4, x)
```

### 2.2 物理专用符号

```python
# 量子力学符号
from sympy.physics.quantum import *

# 张量运算
from sympy.tensor.array import *
```

---

## 三、可视化工具

### 3.1 Matplotlib 基础

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2*np.pi, 100)
y = np.sin(x)

plt.plot(x, y)
plt.xlabel(r'$\omega t$')
plt.ylabel(r'$\sin(\omega t)$')
plt.title('Simple Harmonic Oscillator')
plt.grid(True)
plt.show()
```

### 3.2 物理场可视化

```python
# 二维电场/势能场
import numpy as np
import matplotlib.pyplot as plt

def potential(x, y, q1, q2):
    return q1/np.sqrt((x-1)**2 + y**2) + q2/np.sqrt((x+1)**2 + y**2)

x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)
Z = potential(X, Y, 1, -1)

plt.contourf(X, Y, Z, levels=20)
plt.colorbar(label='Potential')
plt.xlabel(r'$x$')
plt.ylabel(r'$y$')
plt.title('Electric Potential')
plt.show()
```

### 3.3 3D 表面图

```python
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()
```

---

## 四、常用物理常数

```python
import scipy.constants as const

# 基本常数
const.c       # 光速
const.h       # 普朗克常数
const.hbar    # 约化普朗克常数
const.e       # 元电荷
const.m_e     # 电子质量
const.m_p     # 质子质量
const.alpha    # 精细结构常数
const.G       # 万有引力常数
const.k_B     # 玻尔兹曼常数

# 换算
const.epsilon_0  # 真空介电常数
const.mu_0      # 真空磁导率
```

---

## 五、单位制转换

```python
# SI 到原子单位
const.physical_constants['atomic unit of length']

# 能量单位转换
const.eV    # 电子伏特
const.cal    # 卡路里
const.keV    # 千电子伏特
const.MeV    # 兆电子伏特
const.GeV    # 吉电子伏特
```

---

## 六、脚本工具使用

### 6.1 计算工具

```bash
python3 scripts/calculate.py --help
```

### 6.2 可视化工具

```bash
python3 scripts/visualize.py --help
```

---

## 七、资源链接

- [NumPy 文档](https://numpy.org/doc/)
- [SciPy 文档](https://docs.scipy.org/)
- [SymPy 文档](https://docs.sympy.org/)
- [Matplotlib 文档](https://matplotlib.org/stable/contents.html)
- [Physics Handbook](http://www.users.howard.edu/~rafid/phys/Phys handbook.pdf)

---

*最后更新：2026-05-23*
*更新者：杨权*
