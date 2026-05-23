# 数学公式模板

> LaTeX 格式的常用数学公式模板

---

## 一、基础算术

### 加减乘除

```latex
a + b = c
a - b = c
a \times b = c
a \div b = c
\frac{a}{b} = c
```

### 指数和对数

```latex
a^b = c
\sqrt[n]{a} = b
\log_a c = b
\ln a = \log_e a
```

---

## 二、代数

### 多项式

```latex
ax^2 + bx + c = 0

x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
```

### 不等式

```latex
a < b
a \leq b
a > b
a \geq b
|a| < b \Rightarrow -b < a < b
```

### 数列

```latex
等差数列：a_n = a_1 + (n-1)d
等比数列：a_n = a_1 \cdot r^{n-1}
```

---

## 三、微积分

### 极限

```latex
\lim_{x \to a} f(x) = L
\lim_{x \to 0} \frac{\sin x}{x} = 1
```

### 导数

```latex
一阶导数：f'(x) = \frac{df}{dx}
高阶导数：f^{(n)}(x)
莱布尼茨公式：(uv)^{(n)} = \sum_{k=0}^{n} \binom{n}{k} u^{(k)} v^{(n-k)}
```

### 积分

```latex
不定积分：\int f(x) dx = F(x) + C
定积分：\int_a^b f(x) dx = F(b) - F(a)
分部积分：\int u dv = uv - \int v du
```

---

## 四、线性代数

### 矩阵运算

```latex
矩阵乘法：(AB)_{ij} = \sum_{k=1}^{n} a_{ik} b_{kj}
转置：(A^T)_{ij} = a_{ji}
逆矩阵：AA^{-1} = A^{-1}A = I
行列式：\det(A) = \sum_{j=1}^{n} (-1)^{i+j} a_{ij} M_{ij}
```

### 向量

```latex
点积：\vec{a} \cdot \vec{b} = \sum_{i=1}^{n} a_i b_i = |\vec{a}||\vec{b}|\cos\theta
叉积：\vec{a} \times \vec{b} = (a_2b_3 - a_3b_2, a_3b_1 - a_1b_3, a_1b_2 - a_2b_1)
范数：||\vec{v}|| = \sqrt{v_1^2 + v_2^2 + \cdots + v_n^2}
```

### 特征值

```latex
特征方程：\det(A - \lambda I) = 0
特征值：Av = \lambda v
```

---

## 五、概率统计

### 概率公式

```latex
加法公式：P(A \cup B) = P(A) + P(B) - P(A \cap B)
乘法公式：P(A \cap B) = P(A)P(B|A)
贝叶斯公式：P(A|B) = \frac{P(B|A)P(A)}{P(B)}
全概率公式：P(B) = \sum_{i=1}^{n} P(B|A_i)P(A_i)
```

### 分布函数

```latex
二项分布：P(X=k) = \binom{n}{k} p^k (1-p)^{n-k}
正态分布：f(x) = \frac{1}{\sqrt{2\pi\sigma^2}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}
泊松分布：P(X=k) = \frac{\lambda^k e^{-\lambda}}{k!}
```

### 统计量

```latex
样本均值：\bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_i
样本方差：s^2 = \frac{1}{n-1} \sum_{i=1}^{n} (x_i - \bar{x})^2
协方差：Cov(X,Y) = E[(X-\mu_X)(Y-\mu_Y)]
相关系数：r = \frac{Cov(X,Y)}{\sigma_X \sigma_Y}
```

---

## 六、微分方程

### 一阶方程

```latex
可分离变量：\frac{dy}{dx} = f(x)g(y) \Rightarrow \int \frac{dy}{g(y)} = \int f(x) dx
齐次方程：\frac{dy}{dx} = f(\frac{y}{x})
线性方程：\frac{dy}{dx} + P(x)y = Q(x)
```

### 二阶方程

```latex
二阶线性齐次：y'' + p(x)y' + q(x)y = 0
二阶线性非齐次：y'' + p(x)y' + q(x)y = f(x)
常系数特征方程：r^2 + ar + b = 0
```

---

## 七、最优化

### 目标函数

```latex
线性规划：\min c^T x \quad \text{s.t.} \quad Ax \leq b, x \geq 0
二次规划：\min \frac{1}{2} x^T H x + c^T x
拉格朗日乘数：\mathcal{L}(x,\lambda) = f(x) + \lambda g(x)
KKT条件：\nabla f(x^*) + \sum_{i=1}^{m} \lambda_i \nabla g_i(x^*) = 0
```

---

## 八、数值方法

### 迭代公式

```latex
牛顿迭代：x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}
二分法：c = \frac{a+b}{2}, 收敛条件：|b-a| < \epsilon
梯度下降：x_{n+1} = x_n - \alpha \nabla f(x_n)
```

---

## 九、常用符号

### 希腊字母

```latex
\alpha, \beta, \gamma, \delta, \epsilon, \zeta, \eta, \theta,
\iota, \kappa, \lambda, \mu, \nu, \xi, \pi, \rho, \sigma, \tau,
\upsilon, \phi, \chi, \psi, \omega
```

### 数学符号

```latex
\sum_{i=1}^{n}    % 求和
\prod_{i=1}^{n}    % 连乘
\int_{a}^{b}       % 积分
\oint_{C}          % 环路积分
\partial           % 偏导
\nabla             % 梯度/散度/旋度
\infty             % 无穷大
\neq               % 不等于
\leq               % 小于等于
\geq               % 大于等于
\approx           % 约等于
\equiv            % 恒等于
\in               % 属于
\subset           % 子集
\cup              % 并集
\cap              % 交集
\emptyset          % 空集
\forall           % 对所有
\exists           % 存在
```

---

## 十、矩阵模板

### 通用格式

```latex
% 2x2矩阵
\begin{pmatrix}
a_{11} & a_{12} \\
a_{21} & a_{22}
\end{pmatrix}

% 行列式
\begin{vmatrix}
a_{11} & a_{12} \\
a_{21} & a_{22}
\end{vmatrix}

% 分块矩阵
\left(
\begin{array}{c|c}
A & B \\
\hline
C & D
\end{array}
\right)
```

---

*模板版本：v1.0.0*
*最后更新：2026-05-23*
