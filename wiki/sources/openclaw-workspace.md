---
pageType: source
id: source.openclaw-workspace
createdAt: "2026-05-12T10:22:00+08:00"
updatedAt: "2026-05-12T10:22:00+08:00"
title: openclaw-workspace
sourceIds:
  - source.system-config
aliases:
  - Agent工作空间
---

# Agent 工作空间

> OpenClaw Agent 统一工作目录。
> 来源：`~/.openclaw/workspace/`

---

## 路径

```
~/.openclaw/workspace/
```

## 结构

```
~/.openclaw/workspace/
├── steward/               # 大管家
├── programmer/            # 程序员
├── mathematician/         # 数学家
├── physicist/             # 物理学家
├── psychologist/          # 心理学家
├── writer/                # 写作助手
├── reviewer/              # 审稿助手
├── instructor/            # 教员
├── presenter/             # 呈现师
├── auditor/               # 督导
└── ...                    # 其他 Agent
```

## 单个 Agent 工作空间结构

```
~/.openclaw/workspace/{agent_id}/
├── MEMORY.md              # 个人记忆
├── IDENTITY.md            # 个人身份
├── SOUL.md                # 个人灵魂
├── USER.md                # 用户偏好（系统管理员维护）
├── TOOLS.md               # 个人工具
├── HEARTBEAT.md           # 心跳任务
├── AGENTS.md              # 工作原则
├── skills/                # 个人技能
│   └── README.md          # 技能索引
├── temp/                  # 临时文件
│   └── README.md
└── memory/                # 工作记忆（OpenClaw 核心）
    └── *.md
```

## 核心文件

| 文件 | 说明 | 维护者 |
|------|------|--------|
| `MEMORY.md` | 工作记忆、任务看板、If-Then 规则 | Agent 自己 |
| `IDENTITY.md` | 核心身份、能力边界 | Agent 自己 |
| `SOUL.md` | 信念、价值观、风格 | Agent 自己 |
| `TOOLS.md` | 个人工具、技能索引 | Agent 自己 |
| `HEARTBEAT.md` | 定时任务列表 | Agent 自己 |
| `AGENTS.md` | 工作原则、安全红线 | 系统管理员 |
| `USER.md` | 用户偏好、交互规则 | 系统管理员 |
| `skills/README.md` | 个人技能索引 | Agent 自己 |

---

## 相关

- [[sources/openclaw-system]] — OpenClaw 系统目录
- [[concepts/bootstrap]] — Agent 初始化模板
- [[concepts/identity]] — 身份配置模板

---

*最后更新：2026-05-12*

## Related
<!-- openclaw:wiki:related:start -->
### Referenced By

- [[syntheses/2026-05-17-18-40-33-agent-memory|Agent Memory（智能体记忆系统）]]
- [[sources/openclaw-system|openclaw-system]]
<!-- openclaw:wiki:related:end -->
