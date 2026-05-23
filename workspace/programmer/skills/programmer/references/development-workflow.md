# 开发流程

> 从需求到交付的最佳实践

---

## 开发流程总览

```
需求分析 → 技术设计 → 编码实现 → 测试验证 → 部署交付
    │            │            │            │            │
    ▼            ▼            ▼            ▼            ▼
  理解问题    架构设计    写代码      单元测试     上线部署
```

---

## 1. 需求分析

### 理解问题三步法

1. **用户要解决什么问题？**
2. **现有方案是什么？**
3. **最佳方案是什么？**

### 需求文档模板

📄 模板位置：[需求文档模板](../assets/templates/需求文档模板.md)

---

## 2. 技术设计

### 先设计后编码

```
问题定义 → 方案设计 → 接口定义 → 评审 → 编码
```

### 接口设计示例

```python
# 定义清晰的接口
class UserRepository:
    def get_by_id(self, user_id: int) -> User | None:
        """根据 ID 获取用户"""
        pass
    
    def create(self, name: str, email: str) -> User:
        """创建新用户"""
        pass
    
    def update(self, user_id: int, **kwargs) -> User:
        """更新用户信息"""
        pass
    
    def delete(self, user_id: int) -> bool:
        """删除用户"""
        pass
```

### 技术方案文档

📄 模板位置：[技术方案模板](../assets/templates/技术方案模板.md)

---

## 3. 编码实现

### 代码写作原则

| 原则 | 说明 |
|------|------|
| **清晰优于聪明** | 代码是给人看的 |
| **先跑通再优化** | 不要过度设计 |
| **小步提交** | 每次提交做一件事 |
| **写好注释** | 解释为什么，不解释是什么 |

### 编码检查清单

```python
def process_order(order_id: int) -> OrderResult:
    # ✅ 验证输入
    if order_id <= 0:
        raise ValueError("order_id must be positive")
    
    # ✅ 获取数据
    order = get_order(order_id)
    if not order:
        raise ValueError(f"Order {order_id} not found")
    
    # ✅ 处理业务逻辑
    result = OrderProcessor(order).process()
    
    # ✅ 记录日志
    logger.info(f"Order {order_id} processed: {result.status}")
    
    # ✅ 返回结果
    return result
```

### 错误处理模式

```python
# 不好：裸 except
try:
    do_something()
except:
    pass

# 好：具体异常 + 处理
try:
    result = risky_operation()
except ValueError as e:
    logger.warning(f"Invalid input: {e}")
    return None
except NetworkError as e:
    logger.error(f"Network failed: {e}")
    raise  # 重新抛出
```

---

## 4. 测试验证

### 测试金字塔

```
           /\
          /  \       E2E 测试（少量）
         /----\
        /      \     集成测试（适量）
       /--------\
      /          \   单元测试（大量）
     /____________\
```

### 单元测试示例

```python
import pytest

class TestCalculator:
    def test_add(self):
        assert add(1, 2) == 3
    
    def test_divide_by_zero(self):
        with pytest.raises(ValueError):
            divide(1, 0)
    
    def test_add_negative(self):
        assert add(-1, -2) == -3
```

### 测试命名规范

```
test_{方法名}_{场景}_{预期结果}

test_user_create_success
test_user_create_duplicate_email
test_user_delete_not_found
```

---

## 5. 部署交付

### 部署检查清单

| 检查项 | 说明 |
|--------|------|
| 配置正确 | 环境变量、数据库连接 |
| 监控到位 | 日志、告警、指标 |
| 回滚方案 | 如何快速回退 |
| 文档更新 | API 文档、运维手册 |

### Git 提交规范

```bash
# 格式
<type>: <subject>

# type: feat | fix | docs | style | refactor | test | chore

# 示例
git commit -m "feat: add user login endpoint"
git commit -m "fix: handle null pointer in order processor"
git commit -m "docs: update API documentation"
```

### 版本号管理

| 场景 | 规则 | 示例 |
|------|------|------|
| Bug 修复 | patch | 1.0.0 → 1.0.1 |
| 新功能 | minor | 1.0.0 → 1.1.0 |
| 不兼容 | major | 1.0.0 → 2.0.0 |

---

## 开发流程核心原则

1. **理解问题再动手** — 不要急于写代码
2. **设计优先** — 接口定了，编码就快了
3. **小步提交** — 每次只改一件事
4. **测试驱动** — 关键逻辑必须有测试
5. **持续优化** — 重构是日常，不是项目结尾

---

*详见 [索引](index.md)*
