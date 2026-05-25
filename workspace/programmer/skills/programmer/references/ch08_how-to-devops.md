# 如何进行 DevOps

> Docker 容器化、CI/CD 流水线、监控告警、日志管理。

---

## 问题

### DevOps 的目标是什么？

| 目标 | 说明 |
|------|------|
| **快速交付** | 从代码到生产的时间最短 |
| **稳定可靠** | 频繁发布不出问题 |
| **可追溯** | 问题能快速定位 |

### 程序员需要懂多少 DevOps？

| 必需 | 加分 |
|------|------|
| Dockerfile 编写 | K8s 运维 |
| CI/CD 流水线配置 | 监控告警调优 |
| Docker Compose 本地开发 | 日志分析 |
| 环境变量管理 | 容量规划 |

---

## 方法论

### 12-Factor App

| 原则 | 说明 |
|------|------|
| 代码资产 | 代码和配置分离 |
| 依赖声明 | 明确声明依赖 |
| 配置外置 | 环境变量存储配置 |
| 后端服务 | 把数据库等当资源 |

### CI/CD 流水线

```
代码提交 → 构建 → 单元测试 → 集成测试 → 部署测试环境 → 部署生产
```

---

## 工作流

### Docker 化

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

### CI 配置

```yaml
# .github/workflows/ci.yml
test:
  script:
    - pip install -r requirements.txt
    - pytest tests/
```

### 部署检查

1. 确认配置正确
2. 确认回滚方案
3. 确认监控到位

---

## 执行标准

### DevOps 检查清单

- [ ] 有 Dockerfile
- [ ] 有 docker-compose.yml（本地开发）
- [ ] CI 流水线有测试
- [ ] 有日志记录
- [ ] 有健康检查
- [ ] 知道如何回滚
