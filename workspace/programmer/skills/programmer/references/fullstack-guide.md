# 全栈开发

> 全栈开发知识与技术栈概览

---

## 什么是全栈开发

一个人能独立完成前端、后端、数据库、部署等全部层面的开发。

---

## 技术栈分层

```
┌─────────────────────────────────┐
│          前端 (Frontend)         │
│   React / Vue / Angular / Svelte │
├─────────────────────────────────┤
│          后端 (Backend)          │
│  Node.js / Python / Go / Java   │
├─────────────────────────────────┤
│           数据库 (DB)            │
│  PostgreSQL / MySQL / MongoDB    │
├─────────────────────────────────┤
│           缓存层 (Cache)         │
│       Redis / Memcached         │
├─────────────────────────────────┤
│           消息队列               │
│     RabbitMQ / Kafka / Redis     │
├─────────────────────────────────┤
│            部署 (DevOps)         │
│   Docker / K8s / CI/CD / Nginx   │
└─────────────────────────────────┘
```

---

## 前端技术

### 框架选择

| 框架 | 特点 | 适用场景 |
|------|------|----------|
| React | 组件化、灵活 | 中大型应用 |
| Vue | 上手快、文档好 | 中小型应用 |
| Svelte | 编译时优化 | 轻量应用 |

### 核心概念

```javascript
// 组件化
function Button({ label, onClick }) {
  return <button onClick={onClick}>{label}</button>;
}

// 状态管理
const [count, setCount] = useState(0);

// 生命周期
useEffect(() => {
  // 组件挂载时执行
  return () => {
    // 组件卸载时清理
  };
}, []);
```

---

## 后端技术

### 常见后端框架

| 语言 | 框架 | 特点 |
|------|------|------|
| JavaScript | Express / Fastify | 轻量、异步 |
| Python | FastAPI / Django | 快速开发、性能好 |
| Go | Gin / Echo | 高性能、并发强 |

### RESTful API 设计

```python
# FastAPI 示例
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id, "name": "张三"}

@app.post("/users")
def create_user(name: str):
    return {"name": name, "id": 1}

@app.put("/users/{user_id}")
def update_user(user_id: int, name: str):
    return {"user_id": user_id, "name": name}

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    return {"success": True}
```

### API 命名规范

| 方法 | 用途 | 示例 |
|------|------|------|
| GET | 获取资源 | `GET /users` |
| POST | 创建资源 | `POST /users` |
| PUT | 更新资源 | `PUT /users/1` |
| DELETE | 删除资源 | `DELETE /users/1` |

---

## 数据库设计

### SQL vs NoSQL

| 类型 | 代表 | 适用场景 |
|------|------|----------|
| 关系型 | PostgreSQL, MySQL | 结构化数据、复杂查询 |
| 文档型 | MongoDB | 灵活 schema、快速迭代 |
| KV 型 | Redis | 缓存、session |

### 基本 SQL

```sql
-- 创建表
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(255) UNIQUE,
  created_at TIMESTAMP DEFAULT NOW()
);

-- 查询
SELECT * FROM users WHERE name LIKE '张%';

-- 关联查询
SELECT u.name, o.total
FROM users u
JOIN orders o ON u.id = o.user_id;
```

---

## 部署与 DevOps

### Docker 基础

```dockerfile
# Dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

### Docker Compose

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    depends_on:
      - db
      - redis
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: myapp
  redis:
    image: redis:7-alpine
```

### CI/CD 流程

```
代码提交 → 单元测试 → 构建镜像 → 集成测试 → 部署
    │           │           │           │
    ▼           ▼           ▼           ▼
  Git Hook   JUnit      Docker      K8s/Nginx
```

---

## 全栈开发检查清单

| 阶段 | 检查项 |
|------|--------|
| 前端 | 响应式设计、错误处理、加载状态 |
| 后端 | 输入验证、错误处理、日志记录 |
| 数据库 | 索引优化、事务处理、备份策略 |
| 安全 | 认证授权、输入过滤、HTTPS |
| 部署 | 环境配置、监控告警、回滚方案 |

---

*详见 [索引](index.md)*
