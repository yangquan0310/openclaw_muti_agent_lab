---
pageType: entity
entityType: system
id: entity.openclaw-gateway
createdAt: "2026-05-08T11:30:00+08:00"
updatedAt: "2026-05-10T18:20:00+08:00"
sourceIds:
  - source.openclaw-docs
  - source.system-config
canonicalId: openclaw.main.gateway
aliases:
  - OpenClaw
  - 网关
---

# OpenClaw 系统架构

多 Agent 智能协作系统的网关配置和目录结构。

## 全局配置路径

| 文件 | 路径 | 说明 |
|------|------|------|
| 主配置 | `~/.openclaw/openclaw.json` | OpenClaw 主配置文件 |
| 环境变量 | `~/.openclaw/.env` | API 密钥和环境变量 |
| 插件目录 | `~/.openclaw/extensions/` | 插件安装位置 |
| 日志目录 | `~/.openclaw/logs/` | 系统日志 |

## 工作空间路径

| 层级 | 路径 | 说明 |
|------|------|------|
| 工作空间根 | `~/.openclaw/workspace/` | 所有 Agent 工作空间 |
| 公共技能 | `~/.openclaw/workspace/skills/` | 共享技能库 |
| 代理工作空间 | `~/.openclaw/workspace/<agent>/` | 各代理独立目录 |

## 代理目录结构

```
workspace/<agent>/
├── AGENTS.md          # 代理行为定义
├── SOUL.md            # 人格/风格
├── TOOLS.md           # 工具配置
├── IDENTITY.md        # 身份定义
├── USER.md            # 用户信息
├── HEARTBEAT.md       # 定时任务
├── MEMORY.md          # 工作记忆 + If-Then 规则
├── memory/            # 记忆存储（ dreaming 分层架构）
│   ├── dreaming/light/  # 浅层梦境：近期事件快速联想
│   ├── dreaming/deep/   # 深层梦境：模式提取、冲突检测
│   └── dreaming/rem/    # REM 梦境：跨会话整合、人格更新
└── skills/            # 代理专属技能
```

## 会话存储

| 路径 | 说明 |
|------|------|
| `~/.openclaw/agents/{agentId}/sessions/` | 按代理隔离的会话记录 |

## 自动化

| 路径 | 说明 |
|------|------|
| `~/.openclaw/cron/jobs.json` | 定时任务定义 |
| `~/.openclaw/cron/jobs-state.json` | 运行时状态（不纳入 Git） |

## 知识库

| 路径 | 说明 |
|------|------|
| `~/.openclaw/wiki/` | 全局共享 wiki |
| `~/.openclaw/workspace/skills/` | 公共技能目录 |

## 常用命令

```bash
openclaw status          # 查看系统状态
openclaw doctor          # 诊断系统问题
openclaw gateway restart # 重启网关
openclaw config get      # 查看配置
openclaw config patch    # 修改配置
openclaw plugins list    # 列出插件
openclaw hooks list      # 列出钩子
openclaw memory status   # 查看记忆状态
```

## 当前代理列表

| Agent ID | 名称 | 工作空间 |
|----------|------|----------|
| programmer | 程序员 | `workspace/programmer/` |
| steward | 大管家 | `workspace/steward/` |
| mathematician | 数学家 | `workspace/mathematician/` |
| physicist | 物理学家 | `workspace/physicist/` |
| psychologist | 心理学家 | `workspace/psychologist/` |
| writer | 写作助手 | `workspace/writer/` |
| reviewer | 审稿助手 | `workspace/reviewer/` |
| teachingassistant | 教学助手 | `workspace/teachingassistant/` |
| academicassistant | 教务助手 | `workspace/academicassistant/` |
| studentaffairsassistant | 学工助手 | `workspace/studentaffairsassistant/` |

## Related
<!-- openclaw:wiki:related:start -->
### Referenced By

- [[syntheses/2026-05-17-18-40-33-agent-memory|Agent Memory（智能体记忆系统）]]
- [[syntheses/2026-05-19-18-25-37-tools|TOOLS 工具配置模板（TOOLS.md）]]
<!-- openclaw:wiki:related:end -->
