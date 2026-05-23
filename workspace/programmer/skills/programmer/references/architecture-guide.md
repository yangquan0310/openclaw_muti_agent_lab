# 架构指南

> 系统架构、设计模式、微服务架构

---

## 架构核心概念

### 架构是什么

架构是**系统的骨架** — 定义组件、组件之间的关系、组件与外部环境交互的原则。

### 好架构的特征

| 特征 | 说明 |
|------|------|
| **高内聚** | 每个组件只做一件事 |
| **低耦合** | 组件之间依赖最小化 |
| **可扩展** | 新增功能不需要改现有代码 |
| **可测试** | 组件可以独立测试 |
| **可部署** | 可以独立部署 |

---

## 系统架构风格

### 分层架构

```
┌─────────────────────────┐
│       表示层 (UI)        │  ← 用户界面、API 网关
├─────────────────────────┤
│       应用层             │  ← 用例、编排、业务流程
├─────────────────────────┤
│       领域层            │  ← 业务规则、实体、值对象
├─────────────────────────┤
│       基础设施层         │  ← 数据库、外部服务、文件存储
└─────────────────────────┘
```

### 微服务架构

```
┌──────────┐  ┌──────────┐  ┌──────────┐
│ 用户服务  │  │ 订单服务  │  │ 支付服务  │
└────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │             │
     └─────────────┼─────────────┘
                   │
            ┌──────┴──────┐
            │  API Gateway │
            └─────────────┘
```

### 事件驱动架构

```
事件发布者 → 事件总线 → 事件订阅者
                            ↓
                    ┌───────────────┐
                    │  事件处理器   │
                    └───────────────┘
```

---

## 设计模式

### 创建型模式

| 模式 | 用途 | 示例 |
|------|------|------|
| **单例** | 全局唯一实例 | 数据库连接、配置管理 |
| **工厂** | 封装对象创建 | 不同支付方式创建 |
| **建造者** | 分步构建复杂对象 | SQL 查询构建 |

### 单例模式

```python
class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connected = False
        return cls._instance
    
    def connect(self):
        if not self._connected:
            print("Connecting to database...")
            self._connected = True

# 全局唯一实例
db1 = Database()
db2 = Database()
assert db1 is db2  # True
```

### 工厂模式

```python
from abc import ABC, abstractmethod

class Payment(ABC):
    @abstractmethod
    def pay(self, amount: float) -> bool:
        pass

class Alipay(Payment):
    def pay(self, amount: float) -> bool:
        print(f"Alipay: {amount}")
        return True

class WechatPay(Payment):
    def pay(self, amount: float) -> bool:
        print(f"WechatPay: {amount}")
        return True

class PaymentFactory:
    @staticmethod
    def create_payment(method: str) -> Payment:
        payments = {
            "alipay": Alipay,
            "wechat": WechatPay
        }
        return payments[method]()

# 使用
payment = PaymentFactory.create_payment("alipay")
payment.pay(100)
```

### 结构型模式

| 模式 | 用途 | 示例 |
|------|------|------|
| **适配器** | 接口转换 | 旧接口适配新接口 |
| **装饰器** | 动态增强功能 | 日志增强、缓存 |
| **代理** | 控制访问 | 延迟加载、权限控制 |

### 装饰器模式

```python
def log_calls(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

@log_calls
def add(a, b):
    return a + b

add(1, 2)
# Output:
# Calling add
# add returned 3
```

### 行为型模式

| 模式 | 用途 | 示例 |
|------|------|------|
| **策略** | 多种算法切换 | 排序算法、支付方式 |
| **观察者** | 一对多通知 | 事件监听、订阅 |
| **命令** | 请求封装 | 撤销/重做 |

### 策略模式

```python
from abc import ABC, abstractmethod

class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: list) -> list:
        pass

class QuickSort(SortStrategy):
    def sort(self, data: list) -> list:
        return sorted(data)  # 简化

class BubbleSort(SortStrategy):
    def sort(self, data: list) -> list:
        # 简化实现
        return sorted(data)

class Sorter:
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: SortStrategy):
        self._strategy = strategy
    
    def execute(self, data: list) -> list:
        return self._strategy.sort(data)

# 使用
sorter = Sorter(QuickSort())
sorter.execute([3, 1, 2])

sorter.set_strategy(BubbleSort())
sorter.execute([3, 1, 2])
```

---

## 微服务设计

### 服务拆分原则

| 原则 | 说明 |
|------|------|
| **单一职责** | 每个服务只负责一个业务领域 |
| **松耦合** | 服务之间通过 API 通信，不共享数据 |
| **高内聚** | 相关功能放在同一个服务 |

### API 设计

```python
# RESTful API 结构
# GET    /users/{id}      获取用户
# POST   /users           创建用户
# PUT    /users/{id}      更新用户
# DELETE /users/{id}      删除用户

# 服务间通信
class UserServiceClient:
    def __init__(self, http_client):
        self.http = http_client
    
    def get_user(self, user_id: int):
        return self.http.get(f"/users/{user_id}")
    
    def create_order(self, user_id: int, order_data: dict):
        return self.http.post(f"/users/{user_id}/orders", order_data)
```

### 服务间通信

```python
# 同步通信 (REST/gRPC)
response = requests.get("http://user-service/users/1")

# 异步通信 (消息队列)
# 生产者
queue.publish("order.created", {"order_id": 1, "user_id": 1})

# 消费者
@queue.subscribe("order.created")
def handle_order_created(event):
    user_service.notify_user(event["user_id"])
```

---

## 数据库设计

### 数据库选择

| 场景 | 推荐 |
|------|------|
| 事务性数据 | PostgreSQL / MySQL |
| 缓存 | Redis |
| 文档存储 | MongoDB |
| 搜索 | Elasticsearch |
| 时序数据 | InfluxDB |

### 读写分离

```
写入 ──→ 主库 (Master)
          │
          └──→ 从库 (Slave) ──→ 读取
          └──→ 从库 (Slave) ──→ 读取
```

### 分库分表

```python
# 哈希分片
def get_shard(user_id: int) -> int:
    return user_id % NUM_SHARDS

# 范围分片
def get_partition(user_id: int) -> int:
    if user_id < 10000:
        return 0
    elif user_id < 50000:
        return 1
    else:
        return 2
```

---

## 架构文档

### ADR（架构决策记录）

```markdown
# ADR-001: 使用 PostgreSQL 作为主数据库

## 状态
已接受

## 背景
需要选择主数据库存储业务数据

## 决策
使用 PostgreSQL 作为主数据库

## 理由
- 支持 JSON 类型
- 事务支持完善
- 社区活跃
- 性能优秀

## 后果
- 需要管理数据库迁移
- 需要配置备份策略
```

### 系统架构图

```text
┌─────────────────────────────────────────────────┐
│                   用户端                         │
└─────────────────────┬───────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────┐
│                 CDN / Nginx                      │
└─────────────────────┬───────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────┐
│              API Gateway / Load Balancer         │
└──────┬──────────────┬───────────────┬───────────┘
       │              │               │
┌──────▼────┐ ┌───────▼─────┐ ┌─────▼─────────┐
│ 用户服务   │ │  订单服务    │ │   支付服务    │
└───────────┘ └─────────────┘ └───────────────┘
       │              │               │
       └──────────────┼───────────────┘
                      │
┌─────────────────────▼───────────────────────────┐
│              Message Queue (Kafka)               │
└─────────────────────┬───────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────┐
│              Notification Service                │
└─────────────────────────────────────────────────┘
```

---

## 架构评审检查清单

| 检查项 | 说明 |
|--------|------|
| 组件职责清晰 | 每个组件有明确职责 |
| 接口设计合理 | 接口稳定、版本兼容 |
| 数据一致性 | 分布式事务处理方案 |
| 容错设计 | 降级、熔断、超时 |
| 监控告警 | 日志、指标、链路追踪 |
| 安全设计 | 认证、授权、加密 |

---

*详见 [索引](index.md)*
