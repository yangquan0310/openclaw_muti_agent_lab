# OOP 原则

> 封装、继承、多态详解

---

## 一、封装（Encapsulation）

### 核心思想

把数据和方法包在一起，对外隐藏实现细节，只暴露必要的接口。

### 目的

- **数据保护**：防止外部随意修改内部状态
- **接口简化**：隐藏复杂逻辑，提供简单调用方式
- **模块独立**：内部修改不影响外部调用方

### Python 实现

```python
class BankAccount:
    def __init__(self, balance: float):
        # `_` 前缀表示受保护，不应直接访问
        self._balance = balance
    
    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("存款金额必须为正")
        self._balance += amount
    
    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("取款金额必须为正")
        if amount > self._balance:
            raise ValueError("余额不足")
        self._balance -= amount
    
    def get_balance(self) -> float:
        return self._balance
```

### 访问控制

| 标记 | 含义 | Python 实现 |
|------|------|-------------|
| `public` | 公开 | `self.name` |
| `protected` | 子类可见 | `self._name` |
| `private` | 仅自身可见 | `self.__name` |

---

## 二、继承（Inheritance）

### 核心思想

子类复用父类的属性和方法，不需要重复代码。

### 目的

- **代码复用**：子类复用父类逻辑
- **is-a 关系**：子类是父类的一种
- **统一接口**：子类和父类有相同的接口

### Python 实现

```python
# 父类
class Animal:
    def __init__(self, name: str):
        self.name = name
    
    def speak(self) -> str:
        raise NotImplementedError

# 子类
class Dog(Animal):
    def speak(self) -> str:
        return "汪"

class Cat(Animal):
    def speak(self) -> str:
        return "喵"

# 使用
animals = [Dog("旺财"), Cat("咪咪")]
for a in animals:
    print(f"{a.name}: {a.speak()}")
```

### 继承类型

| 类型 | 说明 | 示例 |
|------|------|代价|
| 单继承 | 一个父类 | `class Dog(Animal)` |
| 多继承 | 多个父类 | `class A(B, C)` |
| 多层继承 | 祖孙类 | `class A(B), class B(C)` |

### 方法覆盖（Override）

子类重写父类方法：

```python
class Animal:
    def speak(self):
        return "..."

class Dog(Animal):
    def speak(self):  # 覆盖父类方法
        return "汪汪"
```

### super() 调用父类

```python
class Cat(Animal):
    def __init__(self, name: str, color: str):
        super().__init__(name)  # 调用父类 __init__
        self.color = color
```

---

## 三、多态（Polymorphism）

### 核心思想

同一接口，不同实现。调用方不需要知道具体是哪个子类。

### 目的

- **解耦**：调用方依赖抽象，不依赖具体实现
- **扩展**：新增子类不影响现有代码
- **灵活**：同一套逻辑处理多种类型

### Python 实现

```python
# 同一接口，不同实现
def make_them_speak(animals: list[Animal]) -> None:
    for a in animals:
        print(a.speak())  # 调用的是实际对象的方法

make_them_speak([Dog("旺财"), Cat("咪咪")])
# 输出:
# 旺财 says 汪
# 咪咪 says 喵
```

### 鸭子类型（Duck Typing）

Python 的多态不依赖显式继承，只要对象有相应方法即可：

```python
class Duck:
    def swim(self):
        return "鸭子游泳"

class Fish:
    def swim(self):  # 也有 swim 方法
        return "鱼游泳"

def let_them_swim(thing):
    print(thing.swim())

let_them_swim(Duck())  # 鸭子游泳
let_them_swim(Fish())  # 鱼游泳
```

### 抽象基类（ABC）

定义必须被子类实现的方法：

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass

class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    def area(self) -> float:
        return self.width * self.height
```

---

## 三大原则的关系

```
        封装
     ┌────┴────┐
     │         │
     ▼         ▼
   继承  ←→  多态
     │         │
     └────┴─────┘
         │
         ▼
      抽象
```

- **封装**是基础，把数据和方法绑在一起
- **继承**复用代码，建立 is-a 关系
- **多态**统一接口，灵活扩展

---

## 常见误区

| 误区 | 正确做法 |
|------|----------|
| 滥用继承 | 优先组合，继承层次不超过 3 层 |
| 过度封装 | 平衡数据保护和可用性 |
| 假多态 | 使用抽象基类确保接口一致 |

---

*详见 [OOP 指南](oop-guide.md)*
*详见 [索引](index.md)*
