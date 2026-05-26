# 版本控制

> Git 分支策略、提交规范、协作流程。

---

## 核心原则

### 小步提交

每次 commit 只改一件事。commit 早而小，便于审查和回滚。

### 原子提交

一个 commit 解决一个问题。不把多个改动混在一起。

### 清晰的提交信息

| 格式 | 说明 |
|------|------|
| `feat:` | 新功能 |
| `fix:` | Bug 修复 |
| `refactor:` | 重构（不改功能） |
| `docs:` | 文档更新 |
| `test:` | 测试更新 |
| `chore:` | 杂项 |

---

## 分支策略

### 常用分支类型

| 分支 | 用途 | 命名示例 |
|------|------|----------|
| main/master | 稳定代码 | `main` |
| development | 开发中代码 | `development` |
| feature | 新功能 | `feat/user-login` |
| bugfix | Bug 修复 | `fix/order-display` |
| hotfix | 紧急修复 | `hotfix/payment-crash` |

### 分支流程

```
main (稳定)
  ↑
  │ ← hotfix (紧急修复)
development (开发)
  ↑
  │ ← feature/xxx (新功能)
  │ ← bugfix/xxx (Bug 修复)
```

---

## 判断框架

### 什么时候开新分支？

| 场景 | 决策 |
|------|------|
| 新功能开发 | 开 feature 分支 |
| Bug 修复 | 开 bugfix 分支 |
| 紧急修复 | 开 hotfix 分支 |
| 小改动（1小时内） | 可直接在 development |

### 什么时候合并？

| 场景 | 决策 |
|------|------|
| 功能完成并测试通过 | 合并到 development |
| Release 准备就绪 | 合并到 main |
| 紧急修复完成 | 同时合并到 main 和 development |

---

## 提交信息规范

### 好的提交信息

```
feat: 添加用户登录功能

- 实现用户名密码登录
- 添加记住登录状态
- 集成第三方登录

Closes #123
```

### 坏的提交信息

| 类型 | 问题 |
|------|------|
| `fix bug` | 太模糊 |
| `update` | 不知道更新了什么 |
| `asdfgh` | 无意义 |
| `WIP` | 未完成就提交 |

---

## 常见错误

| 错误 | 后果 |
|------|------|
| commit 消息模糊 | 后期难以追溯 |
| 大量改动一次提交 | 难以审查、难以回滚 |
| 直接在 main 开发 | 稳定性无法保证 |
| 不 push 就关机 | 代码丢失风险 |
| force push 到 shared 分支 | 可能覆盖他人代码 |
