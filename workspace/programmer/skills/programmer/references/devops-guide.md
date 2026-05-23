# 运维指南

> 部署、监控、日志、容器化、CI/CD

---

## 运维核心职责

| 职责 | 说明 |
|------|------|
| 部署发布 | 应用打包、上线、回滚 |
| 监控告警 | 系统监控、性能指标、异常告警 |
| 日志管理 | 日志收集、分析、存储 |
| 容器编排 | Docker、K8s 服务管理 |
| 自动化 | CI/CD 流水线、基础设施即代码 |

---

## 容器化（Docker）

### Dockerfile 基础

```dockerfile
# 基础镜像
FROM node:18-alpine

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY package*.json ./

# 安装依赖
RUN npm ci --only=production

# 复制源代码
COPY . .

# 暴露端口
EXPOSE 3000

# 启动命令
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
    environment:
      - NODE_ENV=production
      - DB_HOST=db
    depends_on:
      - db
      - redis
    restart: unless-stopped

  db:
    image: postgres:15
    volumes:
      - db-data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    volumes:
      - redis-data:/data
    restart: unless-stopped

volumes:
  db-data:
  redis-data:
```

### 常用命令

```bash
# 构建镜像
docker build -t myapp:latest .

# 运行容器
docker run -d -p 3000:3000 --name myapp myapp:latest

# 查看日志
docker logs -f myapp

# 进入容器
docker exec -it myapp sh

# 停止删除
docker stop myapp && docker rm myapp
```

---

## Kubernetes（K8s）

### Pod 定义

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
spec:
  containers:
  - name: myapp
    image: myapp:latest
    ports:
    - containerPort: 3000
    resources:
      limits:
        memory: "128Mi"
        cpu: "500m"
    livenessProbe:
      httpGet:
        path: /health
        port: 3000
      initialDelaySeconds: 3
      periodSeconds: 10
```

### Deployment 定义

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:latest
        ports:
        - containerPort: 3000
        env:
        - name: DB_HOST
          value: "mysql-service"
```

### 常用命令

```bash
# 部署应用
kubectl apply -f deployment.yaml

# 查看 pods
kubectl get pods

# 查看日志
kubectl logs -f pod/myapp-pod

# 扩缩容
kubectl scale deployment myapp --replicas=5

# 回滚
kubectl rollout undo deployment/myapp
```

---

## CI/CD 流水线

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Tests
        run: npm ci && npm test

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build Docker Image
        run: docker build -t myapp:${{ github.sha }} .

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Server
        run: |
          docker stop myapp || true
          docker run -d -p 3000:3000 --name myapp myapp:${{ github.sha }}
```

### GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

test:
  stage: test
  script:
    - npm ci
    - npm test

build:
  stage: build
  script:
    - docker build -t myapp:$CI_COMMIT_SHA .
  only:
    - main

deploy:
  stage: deploy
  script:
    - docker-compose up -d
  only:
    - main
```

---

## 监控与告警

### 监控指标（USE 方法）

| 类型 | 指标 | 说明 |
|------|------|------|
| 利用率 | CPU %、内存 % | 资源使用程度 |
| 饱和度 | 队列深度、延迟 | 资源排队情况 |
| 错误率 | 5xx 错误、失败率 | 系统异常 |

### Prometheus + Grafana

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'myapp'
    static_configs:
      - targets: ['myapp:3000']
```

### 告警规则

```yaml
# alert.yml
groups:
  - name: myapp
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
```

### 常用命令

```bash
# 查看服务状态
systemctl status myapp

# 重启服务
sudo systemctl restart myapp

# 查看资源使用
top / htop
df -h
free -h

# 网络连接
netstat -tlnp | grep 3000
```

---

## 日志管理

### 日志分层

```
应用日志 → 容器日志 → 系统日志 → 日志收集器 → 存储/分析
```

### 日志规范

```python
# Python 日志配置
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_data)

# 使用
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
```

### ELK Stack

```yaml
# docker-compose.yml 片段
  elasticsearch:
    image: elasticsearch:8.0
    environment:
      - discovery.type=single-node
    volumes:
      - es-data:/usr/share/elasticsearch/data

  logstash:
    image: logstash:8.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf

  kibana:
    image: kibana:8.0
    ports:
      - "5601:5601"
```

---

## 部署流程

### 部署检查清单

| 阶段 | 检查项 |
|------|--------|
| 部署前 | 配置正确、备份完成、回滚方案准备 |
| 部署中 | 监控指标、灰度发布、增量更新 |
| 部署后 | 健康检查、冒烟测试、监控告警 |

### 蓝绿部署

```
旧版本 (蓝) ← 流量 ←→ 新版本 (绿)
```

### 滚动更新

```
v1.0 → v1.1:00% → v1.1:50% → v1.1:100% → 旧版本下线
```

### 回滚操作

```bash
# Docker Compose 回滚
docker-compose down
docker-compose -f docker-compose.backup.yml up -d

# Kubernetes 回滚
kubectl rollout undo deployment/myapp

# Git 回滚
git revert HEAD
git push origin main
```

---

## 安全运维

### 安全检查项

| 项目 | 说明 |
|------|------|
| 密钥管理 | 使用 Vault 或环境变量，不硬编码 |
| 最小权限 | 按需授权，不过度授权 |
| 网络隔离 | 内网服务不暴露公网 |
| 日志审计 | 记录所有敏感操作 |

### 密钥管理

```bash
# 环境变量
export DB_PASSWORD=$(vault read -field=password secret/myapp/db)

# Docker Secrets
echo "$PASSWORD" | docker secret create db_password -

# K8s Secret
kubectl create secret generic db-credentials \
  --from-literal=password=$DB_PASSWORD
```

---

## 故障处理

### 故障响应流程

```
发现 → 确认 → 通知 → 定位 → 止血 → 恢复 → 复盘
```

### 常用排查命令

```bash
# CPU/内存
top / htop
free -h
vmstat 1

# 磁盘
df -h
du -sh /var/log/*

# 网络
netstat -tlnp
ss -s
ping / curl

# 进程
ps aux | grep myapp
pkill -f myapp

# 日志
tail -f /var/log/myapp.log
grep -r "ERROR" /var/log/myapp.log
```

---

*详见 [索引](index.md)*
