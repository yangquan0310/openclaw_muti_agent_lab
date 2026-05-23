# 代码规范

> 整洁代码原则与实践

---

## 核心原则

**好代码的标准**：
1. 可读（别人能理解）
2. 可维护（改起来容易）
3. 可测试（能验证正确性）

---

## 命名规范

### 基本原则

| 对象 | 规范 | 示例 |
|------|------|------|
| 变量 | 小写 + 下划线 / 驼峰 | `user_name`, `userName` |
| 常量 | 全大写 + 下划线 | `MAX_RETRY_COUNT` |
| 函数 | 动词/动宾短语 | `get_user()`, `send_email()` |
| 类 | 名词，PascalCase | `UserService`, `OrderController` |
| 文件 | 小写 + 横线/下划线 | `user_service.py`, `order_controller.py` |

### 命名好坏对比

```python
# ❌ 差：含糊、缩写
def calc(u, n, d):
    pass

# ✅ 好：清晰、完整
def calculate_user_order_discount(user_id: int, order_id: int, discount: float):
    pass

# ❌ 差：类型前缀
strUserName = "张三"
intCount = 10

# ✅ 好：自然命名
user_name = "张三"
count = 10
```

---

## 函数设计

### 原则

| 原则 | 说明 |
|------|------|
| **单一职责** | 一个函数只做一件事 |
| **参数少** | 最好 ≤ 3 个 |
| **返回值明确** | 要么返回值，要么抛异常，不要两者都做 |

### 好 vs 差

```python
# ❌ 差：做太多件事
def process_user(user):
    validate(user)
    save_to_db(user)
    send_email(user)
    update_stats(user)

# ✅ 好：职责分离
def validate_user(user):
    pass

def create_user(user):
    validate_user(user)
    save_to_db(user)
    notify_user_created(user)

def notify_user_created(user):
    send_email(user)
    update_stats(user)
```

### 参数处理

```python
# ❌ 差：太多参数
def create_user(name, email, age, phone, address, city, country, zipcode):
    pass

# ✅ 好：使用配置对象
@dataclass
class UserCreateParams:
    name: str
    email: str
    age: int

def create_user(params: UserCreateParams):
    pass
```

---

## 错误处理

### 原则

| 原则 | 说明 |
|------|------|
| **早失败** | 输入验证前置 |
| **具体异常** | 不抛裸 Exception |
| **记录日志** | 异常要记录上下文 |

### 模式

```python
# 1. 输入验证
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b

# 2. 结果包装
def get_user(user_id: int) -> Result[User]:
    user = db.find_user(user_id)
    if not user:
        return Result.error(f"User {user_id} not found")
    return Result.ok(user)

# 3. 日志记录
try:
    process_order(order)
except OrderError as e:
    logger.error(f"Order processing failed: {e}", exc_info=True)
    raise
```

---

## 代码结构

### 模块组织

```
project/
├── models/          # 数据模型
│   ├── __init__.py
│   └── user.py
├── services/        # 业务逻辑
│   ├── __init__.py
│   └── user_service.py
├── repositories/     # 数据访问
│   ├── __init__.py
│   └── user_repository.py
├── api/             # 接口层
│   ├── __init__.py
│   └── user_api.py
└── utils/           # 工具函数
    ├── __init__.py
    └── validators.py
```

### 导入顺序

```python
# 1. 标准库
import os
from typing import List, Optional

# 2. 第三方库
import numpy as np
from pydantic import BaseModel

# 3. 本地模块
from models import User
from services import UserService
```

---

## 注释与文档

### 原则

| 类型 | 何时写 |
|------|--------|
| **为什么** | 业务逻辑复杂、做了不直观的选择 |
| **接口文档** | 公共 API 要写 docstring |
| **TODO** | 有已知问题待后续处理 |

### 示例

```python
# ❌ 差：解释代码做什么（代码本身已说明）
# 增加 i
i += 1

# ✅ 好：解释为什么
# 跳过已处理的用户，从下一个开始
i += 1

# ✅ 好：公共接口要文档
def calculate_discount(user: User, order: Order) -> float:
    """
    计算用户订单折扣。
    
    Args:
        user: 用户对象
        order: 订单对象
    
    Returns:
        折扣金额（0-1 之间的小数）
    
    Raises:
        ValueError: 用户或订单无效
    """
    pass
```

---

## 代码审查清单

| 检查项 | 说明 |
|--------|------|
| 命名 | 变量/函数/类名是否清晰 |
| 职责 | 函数是否只做一件事 |
| 错误 | 错误处理是否完善 |
| 测试 | 关键逻辑是否有测试 |
| 安全 | 是否有注入、越权风险 |
| 性能 | 是否有明显性能问题 |

---

*详见 [索引](index.md)*
