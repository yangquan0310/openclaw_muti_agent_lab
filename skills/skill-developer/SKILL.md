---
name: skill-developer
description: >
  当用户要求「创建一个新技能」「新建 OpenClaw 技能」「教我开发技能」「更新技能」「维护技能」时触发。
  用于指导代理创建、扩展和维护可复用的 OpenClaw 技能。
version: 5.2.0
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
4. **CLI 规范**：所有技能必须以 `{技能名} {方法名} {参数}` 格式提供命令行入口，详见 references
5. **方法简洁**：尽可能少建立方法，每一个方法实现一个功能，尽量减少重叠

---

## 边界条件

| 边界 | 说明 |
|------|------|
| 禁止擅自定义 | scripts/ 结构取决于代理目的，不可强制要求特定结构 |
| 禁止缺少 CLI | 所有技能必须提供 `{技能名} {子命令}` 格式的 CLI 入口 |
| 禁止跳过自检 | selfcheck.py 是最后防线，任何更新后都应运行 |

---

## 命令行（CLI）

```bash
# 初始化新技能
skill-developer init my-skill "我的新技能" ./my-skill 📦

# 参数说明
skill-developer init <skill-name> <description> [path] [emoji]
```

---

## 指南导航

| 章节 | 文件 | 内容 |
|------|------|------|
| 技能创建 | [skill-creation.md](references/skill-creation.md) | 什么时候建、什么时候不建 |
| 技能扩展 | [skill-extension.md](references/skill-extension.md) | 什么时候扩展、什么时候新建 |
| 质量标准 | [quality-standards.md](references/quality-standards.md) | 好技能的标准是什么 |
| 设计原则 | [design-principles.md](references/design-principles.md) | 核心设计信念 |
| 边界约束 | [boundaries.md](references/boundaries.md) | 禁止什么、避免什么 |
| 常见错误 | [common-mistakes.md](references/common-mistakes.md) | 错误模式与案例 |
| 命名规范 | [naming.md](references/naming.md) | 名称约定 |
| 版本管理 | [versioning.md](references/versioning.md) | 版本号规则 |
| 渐进式披露 | [progressive-disclosure.md](references/progressive-disclosure.md) | 三层加载模型与触发机制 |

> `mcp/` 目录已移除，如有需要自行添加。

---

## 版本历史

| 版本 | 日期 | 更新 |
|------|------|------|
| 5.5.0 | 2026-05-27 | 移除 mcp/ 目录生成，改为可选项；移除 README.md 和 _meta.json |
| 5.4.0 | 2026-05-27 | 新增 `references/progressive-disclosure.md`：三层加载模型与模型驱动触发 |
| 5.3.0 | 2026-05-26 | references 重构：7章 how-to 改为 8章原则性章节，文件名改为名词短语风格 |
| 5.2.0 | 2026-05-25 | 重构 references：新框架 7 章，how-to 格式命名，问题→方法论→工作流→执行标准结构 |
| 5.1.0 | 2026-05-24 | 新增 pyproject.toml + entry_points，支持 `skill-developer init ...` CLI 格式 |
| 5.0.0 | 2026-05-23 | 精简章节：移除触发条件、三层结构；模板由指南/scripts调用，不在SKILL.md导航 |
| 4.3.0 | 2026-05-20 | SKILL.md 模板化：新增触发条件、核心原则、边界条件 |
| 4.2.0 | 2026-05-20 | 重构 references：新增命名指南/规范，更新指南写作，更名检查清单为标准 |
| 4.1.0 | 2026-05-20 | 新增 MCP 暴露机制，scripts/ 方法通过 mcp/server.py 暴露 |
| 4.0.0 | 2026-05-20 | 重构：约束>流程、目的>形式、进化>固化；scripts不再必须是完整OOP项目 |
