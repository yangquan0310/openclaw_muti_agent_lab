# Extensions 目录

此目录用于存放 OpenClaw 插件。

## 说明

- 第三方插件通过 `openclaw plugins install` 安装，不会同步到 Git
- 自己开发的插件可以放在此处，并修改 `.gitignore` 添加例外规则

## 当前安装的插件（不同步）

| 插件 | 版本 | 来源 |
|------|------|------|
| adp-openclaw | 0.0.77 | npm |
| ddingtalk | 2.0.1 | npm |
| lightclawbot | 1.1.2 | npm |
| memory-tencentdb | 0.2.2 | npm |
| openclaw-lark | 2026.4.7 | archive |
| openclaw-plugin-yuanbao | 2.10.0 | npm |
| openclaw-weixin | 2.1.9 | npm |
| wecom | 2026.3.24 | npm |

## 添加自研插件到 Git

在 `.gitignore` 的 extensions 区域添加：
```gitignore
!/extensions/your-plugin-name/
```

---

## 🤖 Agent 自我发展机制（agent_self_development v1.2.0）

基于皮亚杰认知发展理论 + Baddeley 工作记忆模型构建的 Agent 自我进化系统。

### 核心功能

| 功能 | 说明 |
|------|------|
| **同化与顺应** | 新信息与现有认知结构的整合 |
| **元认知监控** | 自我监控、计划、调节 |
| **工作记忆管理** | 事件记录、记忆表、子代理追踪 |

### 发展流程

```
每日 00:00 定时触发
 ↓
1. 阅读当日事件记忆（memory/YYYY-MM-DD/HH-MM-SS-{event}.md）
 ↓
2. 撰写/完善发展日记（memory/YYYY-MM-DD/diary.md）
 ↓
3. 阅读核心自我（MEMORY.md/SOUL.md/IDENTITY.md/skills/README.md）
 ↓
4. 同化与顺应分析
 ↓
5. 检测更新触发信号（自我认知/角色/风格-信念/技能）
 ↓
6. 执行相应更新
 ↓
7. 记录更新日志
```

## 💬 会话管理机制（v1.2.0 重要更新）

### 功能说明

| 特性 | 描述 |
|------|------|
| **会话命名** | 自动识别会话主题并生成命名建议 |
| **会话归档** | 自动归档历史会话，支持搜索和恢复 |
| **会话关联** | 识别相关会话，建立知识图谱 |
| **上下文继承** | 跨会话保持关键上下文信息 |

### 使用场景

- 长对话自动分段归档
- 多主题会话智能拆分
- 历史会话快速检索
- 跨会话知识连贯性维护
