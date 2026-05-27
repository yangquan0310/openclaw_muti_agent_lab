# 数学工具指南

> 常用数学工具和库的详细说明

---

## 一、数值计算基础

### 1.1 基本运算

| 运算 | 命令 | 示例 |
|------|------|------|
| 加法 | `add` | `python3 scripts/calculate.py basic 3 5 add` → 8 |
| 减法 | `sub` | `python3 scripts/calculate.py basic 10 4 sub` → 6 |
| 乘法 | `mul` | `python3 scripts/calculate.py basic 6 7 mul` → 42 |
| 除法 | `div` | `python3 scripts/calculate.py basic 20 4 div` → 5 |
| 幂运算 | `pow` | `python3 scripts/calculate.py basic 2 8 pow` → 256 |
| 取模 | `mod` | `python3 scripts/calculate.py basic 17 5 mod` → 2 |

### 1.2 矩阵运算

| 运算 | 命令 | 说明 |
|------|------|------|
| 转置 | `transpose` | `python3 scripts/calculate.py matrix --A '[[1,2],[3,4]]' --op transpose` |
| 逆矩阵 | `inverse` | `python3 scripts/calculate.py matrix --A '[[1,2],[3,4]]' --op inverse` |
| 行列式 | `det` | `python3 scripts/calculate.py matrix --A '[[1,2],[3,4]]' --op det` |
| 特征值 | `eigen` | `python3 scripts/calculate.py matrix --A '[[1,2],[3,4]]' --op eigen` |
| 矩阵乘法 | `multiply` | `python3 scripts/calculate.py matrix --A '[[1,2],[3,4]]' --B '[[5,6],[7,8]]' --op multiply` |
| 矩阵加法 | `add` | `python3 scripts/calculate.py matrix --A '[[1,2],[3,4]]' --B '[[5,6],[7,8]]' --op add` |

---

## 二、微积分

### 2.1 数值积分

**方法说明**：

| 方法 | 适用场景 | 精度 |
|------|----------|------|
| `quad` | 一般函数，高精度要求 | 高 |
| `simpson` | 平滑函数，中等精度 | 中 |
| `trapezoid` | 粗略估计，快速计算 | 低 |

**示例**：

```bash
# 积分 x^2 从 0 到 1
python3 scripts/calculate.py integrate --func "x**2" --a 0 --b 1 --method quad

# 积分 sin(x) 从 0 到 π
python3 scripts/calculate.py integrate --func "np.sin(x)" --a 0 --b 3.14159 --method quad

# 积分 e^(-x^2) 从 -∞ 到 ∞
python3 scripts/calculate.py integrate --func "np.exp(-x**2)" --a -1000 --b 1000 --method quad
```

### 2.2 微分方程求解

**常用方法**：

| 方法 | 说明 |
|------|------|
| `RK45` | 4-5阶龙格-库塔，默认方法 |
| `RK23` | 2-3阶龙格-库塔，高精度 |
| `DOP853` | 8阶Dormand-Prince |

**示例**：

```bash
# dy/dt = -y, y(0) = 1
python3 scripts/calculate.py ode --func "-y[0]" --y0 "1" --t0 0 --t1 5 --method RK45

# dy/dt = t*y, y(0) = 1
python3 scripts/calculate.py ode --func "t*y[0]" --y0 "1" --t0 0 --t1 2 --method RK45
```

---

## 三、线性代数

### 3.1 求根运算

**方法对比**：

| 方法 | 适用场景 | 需要区间 |
|------|----------|----------|
| `bisection` | 连续函数，有区间 | 是 |
| `newton` | 导数已知，收敛快 | 否 |
| `brentq` | 通用，高效稳定 | 是 |
| `fsolve` | 非线性方程组 | 否 |

**示例**：

```bash
# 求 x^2 - 2 = 0 的根
python3 scripts/calculate.py root --func "x**2-2" --x0 "0,2" --method bisection

# 求 x^3 - x - 1 = 0 的根
python3 scripts/calculate.py root --func "x**3-x-1" --x0 "1,2" --method brentq
```

### 3.2 插值

**方法说明**：

| 方法 | 特点 |
|------|------|
| `linear` | 线性插值，速度快 |
| `cubic` | 三次样条插值，平滑 |

**示例**：

```bash
# 已知点 (0,0), (1,1), (2,4)，求 x=1.5 时的 y 值
python3 scripts/calculate.py interp --x "0,1,2" --y "0,1,4" --xe "1.5" --method cubic
```

---

## 四、算法复杂度分析

### 4.1 复杂度等级

| 复杂度 | 名称 | 示例算法 |
|--------|------|----------|
| $O(1)$ | 常数时间 | 数组索引 |
| $O(\log n)$ | 对数时间 | 二分查找 |
| $O(n)$ | 线性时间 | 遍历数组 |
| $O(n \log n)$ | 线性对数时间 | 快速排序 |
| $O(n^2)$ | 平方时间 | 冒泡排序 |
| $O(2^n)$ | 指数时间 | 递归斐波那契 |
| $O(n!)$ | 阶乘时间 | 全排列 |

### 4.2 分析方法

1. **循环分析**：找出最内层操作的执行次数
2. **递归树**：展开递归调用，统计各层工作量
3. **主定理**：$T(n) = aT(n/b) + f(n)$ 形式

---

## 五、可视化

### 5.1 函数绘图

```bash
# 绘制 sin(x)
python3 scripts/visualize.py function --func "np.sin(x)" --x0 0 --x1 6.28 --title "sin(x)"

# 绘制高斯函数
python3 scripts/visualize.py function --func "np.exp(-x**2)" --x0 -5 --x1 5 --title "Gaussian"

# 绘制多个函数
python3 scripts/visualize.py multi --x "0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1" \
    --y "0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1" \
    --y2 "0,0.05,0.2,0.45,0.8,1.25,1.8,2.45,3.2,4.05,5" \
    --labels "linear,quadratic"
```

### 5.2 数据可视化

```bash
# 散点图
python3 scripts/visualize.py scatter --x "1,2,3,4,5" --y "2,4,6,8,10" --title "线性关系"

# 直方图
python3 scripts/visualize.py histogram --data "1,2,2,3,3,3,4,4,5" --bins 5

# 柱状图
python3 scripts/visualize.py bar --categories "A,B,C,D" --values "10,20,15,25"
```

---

## 六、常用公式

### 6.1 数值微分

前向差分：$f'(x) \approx \frac{f(x+h) - f(x)}{h}$

后向差分：$f'(x) \approx \frac{f(x) - f(x-h)}{h}$

中心差分：$f'(x) \approx \frac{f(x+h) - f(x-h)}{2h}$

### 6.2 数值积分

矩形公式：$\int_a^b f(x)dx \approx (b-a)f(\frac{a+b}{2})$

梯形公式：$\int_a^b f(x)dx \approx \frac{b-a}{2}[f(a)+f(b)]$

辛普森公式：$\int_a^b f(x)dx \approx \frac{b-a}{6}[f(a)+4f(\frac{a+b}{2})+f(b)]$

### 6.3 拉普拉斯变换

| $f(t)$ | $F(s)$ |
|---------|---------|
| $\delta(t)$ | $1$ |
| $u(t)$ | $\frac{1}{s}$ |
| $t$ | $\frac{1}{s^2}$ |
| $e^{at}$ | $\frac{1}{s-a}$ |
| $\sin(\omega t)$ | $\frac{\omega}{s^2+\omega^2}$ |
| $\cos(\omega t)$ | $\frac{s}{s^2+\omega^2}$ |

---

*最后更新：2026-05-23*
*更新者：杨权*
