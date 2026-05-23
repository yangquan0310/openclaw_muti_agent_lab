# 测试指南

> 软件测试方法与实践

---

## 测试基础知识

### 测试分层

```
┌─────────────────┐
│   E2E 测试       │  ← 少量，代表性场景
├─────────────────┤
│   集成测试       │  ← 适量，模块间协作
├─────────────────┤
│   单元测试       │  ← 大量，函数/类级别
└─────────────────┘
```

### 测试金字塔

```
           /\
          /  \       E2E (End-to-End)
         /----\      UI 交互、完整流程
        /      \     
       /--------\    集成测试
      /          \   模块间交互
     /____________\  单元测试
    覆盖最多        覆盖最少
```

---

## 单元测试

### 什么是单元测试

对代码的最小单位（函数、方法、类）进行测试。

### 单元测试原则（FIRST）

| 原则 | 说明 |
|------|------|
| **F**ast | 测试要快 |
| **I**ndependent | 测试之间相互独立 |
| **R**epeatable | 测试结果可重复 |
| **S**elf-validating | 测试自己判断通过/失败 |
| **T**imely | 测试要及时写（测试驱动） |

### Python 单元测试示例

```python
import pytest

# 被测函数
def add(a: int, b: int) -> int:
    return a + b

def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b

# 测试类
class TestMathOperations:
    def test_add_positive(self):
        assert add(1, 2) == 3
    
    def test_add_negative(self):
        assert add(-1, -2) == -3
    
    def test_add_zero(self):
        assert add(0, 0) == 0
    
    def test_divide_success(self):
        assert divide(6, 2) == 3
    
    def test_divide_by_zero(self):
        with pytest.raises(ValueError, match="除数不能为零"):
            divide(1, 0)
```

### 单元测试命名

```
test_{被测函数}_{场景}_{预期结果}

test_user_create_success
test_user_create_duplicate_email
test_user_delete_not_found
```

---

## 集成测试

### 什么是集成测试

测试多个模块/组件协同工作的正确性。

### 集成测试示例

```python
import pytest
from app import create_app
from db import init_db, seed_test_data

@pytest.fixture
def client():
    """测试客户端 fixture"""
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client

@pytest.fixture
def auth_token(client):
    """获取认证 token"""
    response = client.post("/api/login", json={
        "email": "test@example.com",
        "password": "test123"
    })
    return response.json["token"]

def test_create_order_with_auth(client, auth_token):
    """测试带认证的创建订单"""
    response = client.post(
        "/api/orders",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"product_id": 1, "quantity": 2}
    )
    assert response.status_code == 201
    assert response.json["product_id"] == 1
```

---

## E2E 测试

### 什么是 E2E 测试

模拟真实用户行为，测试完整的产品流程。

### E2E 测试示例（Playwright）

```python
from playwright.sync_api import sync_playwright

def test_user_login_flow():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # 访问登录页
        page.goto("https://example.com/login")
        
        # 填写表单
        page.fill("#email", "user@example.com")
        page.fill("#password", "password123")
        
        # 点击登录
        page.click("#login-button")
        
        # 验证跳转
        page.wait_for_url("**/dashboard")
        assert page.is_visible("#welcome-message")
        
        browser.close()
```

---

## 测试策略

### 测试策略矩阵

| 测试类型 | 覆盖内容 | 工具 |
|----------|----------|------|
| 单元测试 | 函数、类、方法 | pytest, JUnit |
| 集成测试 | 模块间接口 | pytest, Postman |
| E2E 测试 | 完整用户流程 | Playwright, Selenium |
| 性能测试 | 响应时间、并发 | locust, JMeter |
| 安全测试 | 漏洞、注入 | OWASP ZAP |

### TDD 开发流程

```
1. 写一个失败的测试  → RED
2. 写最少的代码通过   → GREEN  
3. 重构代码          → REFACTOR
4. 重复
```

---

## 测试报告

### 测试覆盖率

```bash
# pytest + coverage
pytest --cov=src --cov-report=html tests/

# 覆盖率报告
Coverage.py: platform linux, Python 3.x.x
Name                      Stmts   Miss  Cover
-------------------------------------------------
src/models/user.py           50      5    90%
src/services/order.py        80     15    81%
-------------------------------------------------
TOTAL                      130     20    85%
```

### CI/CD 中的测试

```yaml
# .github/workflows/test.yml
- name: Run Tests
  run: |
    pytest tests/ --cov=src --junitxml=report.xml
  
- name: Upload Coverage
  uses: codecov/codecov-action@v3
```

---

## 常见测试问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 测试太慢 | IO 操作多 | Mock 外部依赖 |
| 测试不稳定 | 依赖顺序 | 使用 fixture |
| 测试难维护 | 断言太具体 | 分离数据与逻辑 |
| 覆盖率低 | 没写测试 | 补充测试用例 |

---

## 测试检查清单

| 阶段 | 检查项 |
|------|--------|
| 编写前 | 明确测试目标、准备测试数据 |
| 编写时 | 遵循 FIRST 原则、命名清晰 |
| 编写后 | 检查覆盖率、审查测试逻辑 |
| 运行时 | 确认测试通过、无警告 |

---

*详见 [索引](index.md)*
