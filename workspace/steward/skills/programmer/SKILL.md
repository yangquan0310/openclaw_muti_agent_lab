---
name: programmer
description: >
  programmer的实践技能。
  当需要编写代码、修复Bug、重构优化、技术设计、OOP问题、全栈开发时激活。
  负责代码开发、Bug排查、重构优化、技术设计、全栈开发。
version: 2.0.0
author: Yang Quan
metadata:
  openclaw:
    emoji: 💻
    requires:
      bins: [python3, git]
---

# programmer（程序员技能）

> 代码开发、Bug 排查、重构优化、技术设计、全栈开发

---

## 触发条件

| 场景 | 触发关键词 |
|------|------------|
| 代码开发 | 写代码、编写功能、实现需求、创建脚本 |
| Bug 排查 | 修复 bug、报错排查、程序崩溃 |
| 重构优化 | 重构、优化代码、改善性能 |
| 技术设计 | 设计架构、技术方案、模块划分 |
| OOP 问题 | 面向对象、封装、继承、多态、类设计 |
| 全栈问题 | 前端、后端、数据库、API 设计、部署 |

---

## 核心原则

1. **先理解再编码** — 理解需求、设计接口、最后写代码
2. **代码即文档** — 好代码自解释，注释解释为什么
3. **测试驱动** — 关键逻辑必须有测试
4. **小步提交** — 每次只改一件事

---

## 能力范围

| 能力 | 说明 |
|------|------|
| ✅ 代码开发 | 各类编程语言的开发实现 |
| ✅ Bug 排查 | 定位问题、修复缺陷 |
| ✅ 重构优化 | 代码结构、性能优化 |
| ✅ 技术设计 | 架构设计、技术选型 |
| ✅ 架构设计 | 分层架构、微服务、设计模式 |
| ✅ 工具开发 | 脚本、CLI、自动化 |
| ✅ 全栈开发 | 前端 + 后端 + 数据库 |
| ✅ OOP 实践 | 封装、继承、多态、设计模式 |
| ✅ 测试实践 | 单元测试、集成测试、E2E 测试 |
| ✅ 产品协作 | 需求分析、PRD 撰写、验收标准 |
| ✅ DevOps 实践 | Docker/K8s、CI/CD 流水线、监控告警 |
| ❌ 系统运维 | 不直接操作生产环境 |
| ❌ 内容创作 | 不撰写论文、营销文案 |

---

## 指南导航

| 章节 | 文件 | 内容 |
|------|------|------|
| 开发流程 | [development-workflow.md](references/development-workflow.md) | 从需求到交付的核心原则 |
| 代码质量 | [code-quality.md](references/code-quality.md) | 好代码的标准 |
| 架构设计 | [architecture-design.md](references/architecture-design.md) | 什么时候设计、设计什么 |
| OOP 设计 | [oop-design.md](references/oop-design.md) | 封装/继承/多态的适用判断 |
| 全栈开发 | [fullstack-development.md](references/fullstack-development.md) | 前端后端数据库的协作原则 |
| 测试原则 | [testing-principles.md](references/testing-principles.md) | 为什么要测、测什么 |
| 产品协作 | [product-collaboration.md](references/product-collaboration.md) | 需求评审、验收标准 |
| DevOps | [devops-principles.md](references/devops-principles.md) | 容器化、CI/CD、部署原则 |
| 版本控制 | [version-control.md](references/version-control.md) | Git 分支策略、提交规范 |
| 性能优化 | [performance.md](references/performance.md) | 性能分析、缓存、并发 |
| 安全原则 | [security.md](references/security.md) | 常见漏洞、防御策略 |
| 调试方法论 | [debugging.md](references/debugging.md) | Bug 定位、根因分析 |

---

## 模板资源

| 模板 | 用途 |
|------|------|
| [需求文档模板](assets/templates/需求文档模板.md) | 需求分析记录 |
| [技术方案模板](assets/templates/技术方案模板.md) | 技术方案设计 |
| [用户故事模板](assets/templates/用户故事模板.md) | 敏捷开发用户故事 |
| [PRD模板](assets/templates/PRD模板.md) | 产品需求文档 |

---

## 快速调用

```bash
# 构建索引（references 文档有更新时执行）
lookup index -r references -m index/manifest.json -c index/chunks.json

# 搜索指南
lookup search -i index/manifest.json <关键词>
```

---

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 2.2.0 | 2026-05-26 | 新增4章：版本控制、性能优化、安全原则、调试方法论 |
| 2.1.0 | 2026-05-26 | 重构 references：8章改为原则性章节，文件名改为名词短语风格 |
| 2.0.0 | 2026-05-25 | 重构 references：新框架 8 章，how-to 格式命名 |
| 1.5.0 | 2026-05-23 | 模板从指南中提取到 assets/templates/ |
| 1.0.0 | 2026-05-21 | 初始版本 |

---

*最后重构: 2026-05-26*
