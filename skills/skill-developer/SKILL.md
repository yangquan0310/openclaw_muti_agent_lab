---
name: skill-developer
description: >
  当用户要求「创建一个新技能」「新建 OpenClaw 技能」「教我开发技能」「更新技能」「维护技能」时触发。
  用于指导代理创建、扩展和维护可复用的 OpenClaw 技能。
version: 5.0.0
author: Yang Quan
metadata:
  openclaw:
    emoji: 🛠️
    requires:
      bins: [python3]
---

# skill-developer（技能开发元技能）

> **元技能定位**：不解决具体业务，而是指导如何**创造其他技能**。

---

## 核心原则

1. **约束优先**：技能必须有明确的触发条件和边界
2. **目的驱动**：每个技能解决一个问题，而非万能工具
3. **进化迭代**：技能随使用迭代优化，而非一次性完美
4. **命令行约束**：所有 scripts 必须支持命令行入口（`python3 {方法}.py --help`），便于代理之间互相调用

---

## 边界条件

| 边界 | 说明 |
|------|------|
| 禁止复制 | 自检脚本 scripts/selfcheck.py 通过 skill-developer 调用，不在初始化时复制 |
| 禁止擅自定义 | scripts/ 结构取决于代理目的，不可强制要求特定结构 |
| 禁止缺少命令行 | 所有 scripts 必须支持命令行入口（`python3 {方法}.py --help`）|

---

## 快速调用

```bash
# 初始化技能
python3 scripts/init.py <skill-name> <description> [path] [emoji]
```

---

## 指南导航

| 指南 | 位置 |
|------|------|
| 使用指南 | [references/guide.md](references/guide.md) |
| 命名指南 | [references/naming-guide.md](references/naming-guide.md) |
| 命名规范 | [references/naming-standards.md](references/naming-standards.md) |
| 指南写作 | [references/guide-writing-guide.md](references/guide-writing-guide.md) |
| 质量标准 | [references/quality-standards.md](references/quality-standards.md) |
| 代码规范 | [references/coding-standards.md](references/coding-standards.md) |
| 开发工作流 | [references/development-workflow.md](references/development-workflow.md) |
| 更新工作流 | [references/update-workflow.md](references/update-workflow.md) |

---

## 版本历史

| 版本 | 日期 | 更新 |
|------|------|------|
| 5.0.0 | 2026-05-23 | 精简章节：移除触发条件、三层结构；模板由指南/scripts调用，不在SKILL.md导航 |
| 4.3.0 | 2026-05-20 | SKILL.md 模板化：新增触发条件、核心原则、边界条件 |
| 4.2.0 | 2026-05-20 | 重构 references：新增命名指南/规范，更新指南写作，更名检查清单为标准 |
| 4.1.0 | 2026-05-20 | 新增 MCP 暴露机制，scripts/ 方法通过 mcp/server.py 暴露 |
| 4.0.0 | 2026-05-20 | 重构：约束>流程、目的>形式、进化>固化；scripts不再必须是完整OOP项目 |
