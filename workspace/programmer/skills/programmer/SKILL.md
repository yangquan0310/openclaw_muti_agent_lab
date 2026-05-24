---
name: programmer
description: >
  programmer的实践技能。
  当需要编写代码、修复Bug、重构优化、技术设计、OOP问题、全栈开发时激活。
  负责代码开发、Bug排查、重构优化、技术设计、全栈开发。
version: 1.0.0
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

| 指南 | 说明 |
|------|------|
| [使用指南](references/guide.md) | 技能使用说明与触发条件 |
| [OOP 指南](references/oop-guide.md) | 面向对象编程核心概念 |
| [OOP 原则](references/oop-principles.md) | 封装、继承、多态详解 |
| [架构指南](references/architecture-guide.md) | 系统架构、设计模式、微服务 |
| [全栈开发](references/fullstack-guide.md) | 前端、后端、数据库全栈知识 |
| [开发流程](references/development-workflow.md) | 从需求到交付的最佳实践 |
| [代码规范](references/coding-standards.md) | 命名、注释、代码结构规范 |
| [产品经理](references/product-guide.md) | 需求分析、PRD、用户故事 |
| [测试指南](references/testing-guide.md) | 单元测试、集成测试、E2E测试 |
| [运维指南](references/devops-guide.md) | Docker/K8s、CI/CD、监控告警 |
| [索引目录](references/index.md) | 全部指南索引 |

## 快速检索

| 脚本 | 命令 |
|------|------|
| 索引构建 | `python3 -m scripts.lookup.indexer` |
| 搜索 | `python3 -m scripts.lookup.searcher <关键词>` |
| 列出文件 | `python3 -m scripts.lookup.searcher --list` |

**脚本结构**：
```
scripts/lookup/
├── __init__.py
├── indexer.py      # 索引构建器
├── searcher.py     # 搜索引擎
└── index/          # 索引数据（manifest.json + chunks.json）
```

**搜索示例**：
```bash
# 构建索引（首次使用或更新文档后）
python3 -m scripts.lookup.indexer

# 搜索
python3 -m scripts.lookup.searcher "什么是多态"
python3 -m scripts.lookup.searcher "docker 部署"
python3 -m scripts.lookup.searcher "单元测试 怎么写"
```
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
# 构建索引
lookup index -r /root/.openclaw/workspace/programmer/skills/programmer/references \
  -m /root/.openclaw/workspace/programmer/skills/programmer/index/manifest.json \
  -c /root/.openclaw/workspace/programmer/skills/programmer/index/chunks.json

# 搜索指南
lookup search -i /root/.openclaw/workspace/programmer/skills/programmer/index/manifest.json <关键词>

# 列出已索引文件
lookup list -i /root/.openclaw/workspace/programmer/skills/programmer/index/manifest.json
```

## 版本历史

| 版本 | 日期 | 更新 |
|------|------|------|
| 1.5.0 | 2026-05-23 | 模板从指南中提取到 assets/templates/；SKILL.md 添加模板导航 |
| 1.4.0 | 2026-05-21 | 新增 references 快速检索脚本（indexer + searcher） |
| 1.3.0 | 2026-05-21 | 新增运维指南 |
| 1.2.0 | 2026-05-21 | 新增产品经理指南、测试指南 |
| 1.0.0 | 2026-05-21 | 初始版本 |

---

*最后重构: 2026-05-23*
