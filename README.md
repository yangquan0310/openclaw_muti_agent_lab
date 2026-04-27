# openclaw-agent-self-development

OpenClaw 插件 —— Agent 自我发展框架

> **插件定位**：纯钩子框架（Hook Router）。在合适的时机，将 `skills/` 目录下的 skill 文档注入 Agent 的 system context。
> 
> **核心原则**：插件只负责"提醒"，Agent 负责"执行"。插件不替 Agent 做决策、不读写 Agent 文件、不管理定时器。

---

## 架构设计

```
┌─────────────────────────────────────────────────────────────┐
│                        Agent (OpenClaw)                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  阅读 Skill  │  │  自行决策    │  │  读写 IDENTITY.md   │  │
│  │  制定计划    │  │  判断偏差    │  │  /SOUL.md/MEMORY.md │  │
│  │  分析同化    │  │  决定更新    │  │  /skills/README.md  │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ↑
                              │ 注入 skill 文档
┌─────────────────────────────────────────────────────────────┐
│                     Plugin (本插件)                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │ metacognition   │  │ working-memory  │  │ assimilation │ │
│  │ · planning      │  │ · 记录事件      │  │ · 检测 cron  │ │
│  │ · monitoring    │  │ · 追踪会话      │  │ · 注入 skill │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 职责边界

| 职责 | 插件 | Agent |
|------|------|-------|
| **计划制定** | 注入 `planning` skill | 阅读 skill，自行制定计划 |
| **偏差检测** | 注入 `monitoring` skill | 阅读 skill，自行判断偏差 |
| **工作记忆** | 记录事件/会话状态 | 阅读 skill，自行管理看板 |
| **每日更新** | 检测 cron，注入 `assimilation` skill | 阅读 skill，自行写日记/分析 |
| **文件读写** | ❌ 不碰 | ✅ 自行读写核心自我文件 |
| **定时任务** | ❌ 不内置定时器 | ✅ 用户配置 OpenClaw cron |

---

## 核心业务

### 1. 元认知（Metacognition）

**触发时机**：`before_prompt_build`（任务开始时）、`llm_output`（LLM 输出时）

**插件行为**：
- 复杂任务：注入 `skills/metacognition/planning/SKILL.md`
- LLM 输出阶段：注入 `skills/metacognition/monitoring/SKILL.md`
- 简单查询（如"今天天气"）：跳过，不注入

**Agent 行为**：阅读注入的 skill，自行制定计划、监控执行、判断偏差。

### 2. 工作记忆（Working Memory）

**触发时机**：`before_tool_call`（会话创建前）、`after_tool_call`（工具执行后）、`agent_end`（任务结束时）

**插件行为**：
- 记录 `sessions_spawn` / `agent` / `subagent` 工具的创建和完成
- 记录工具错误事件
- 任务结束时注入 `skills/working_memory/SKILL.md`

**Agent 行为**：阅读注入的 skill，自行管理工作记忆看板。

### 3. 同化顺应（Assimilation & Accommodation）

**触发时机**：`before_prompt_build` 收到 `[cron:每日自我更新]` 消息时

**插件行为**：注入 `skills/assimilation_accommodation/SKILL.md`

**Agent 行为**：阅读 skill，回顾昨日事件、撰写日记、分析同化/顺应、决定是否更新核心自我文件。

---

## 运行逻辑

```
用户发送消息
    ↓
before_prompt_build
    ├── 简单查询 → 跳过
    └── 复杂任务 → 注入 planning skill
        ↓
Agent 收到 planning skill + 计划建议
    ↓
Agent 自行制定计划、创建会话、执行任务
    ↓
llm_output（每轮输出）
    └── 注入 monitoring skill
        ↓
Agent 收到 monitoring skill，自行检查偏差
    ↓
before_agent_finalize / agent_end
    └── 注入 working_memory skill
        ↓
Agent 收到 working_memory skill，自行归档任务
    ↓
次日 00:00 cron 触发 [cron:每日自我更新]
    ↓
before_prompt_build 检测到 cron 消息
    └── 注入 assimilation skill
        ↓
Agent 收到 assimilation skill，自行回顾/日记/更新
```

---

## 文件结构

```
openclaw-agent-self-development/
├── openclaw.plugin.json          # 插件 manifest（id / type / skills / configSchema）
├── package.json                  # npm 包配置（ESM / files / 无依赖）
├── HOOK.md                       # Hook 事件声明（OpenClaw 安装器必需）
├── README.md                     # 本文档
├── src/
│   ├── index.js                  # 插件入口：注册三大模块
│   ├── metacognition.js          # before_prompt_build / llm_output / agent_end
│   ├── working-memory.js         # before_tool_call / after_tool_call / agent_end
│   ├── assimilation.js           # before_prompt_build（检测 cron 消息）
│   ├── skills-loader.js          # 根据名称读取 skills/ 目录下的 SKILL.md
│   ├── state.js                  # JSON 文件状态管理（带文件锁）
│   ├── utils.js                  # 工具函数（日期、计划模板、会话分配）
│   └── HOOK.md                   # Hook 声明（随源码分发）
└── skills/                       # Skill 文档（插件注入的内容源）
    ├── assimilation_accommodation/
    │   └── SKILL.md              # 每日自我更新：日记、同化顺应、文件更新
    ├── metacognition/
    │   ├── planning/SKILL.md     # 任务计划制定与会话管理
    │   ├── monitoring/SKILL.md   # 执行监控与偏差检测
    │   └── regulation/SKILL.md   # 调节与修正
    ├── working_memory/
    │   └── SKILL.md              # 工作记忆管理与任务归档
    └── _meta.json                # Skill 元数据索引
```

---

## 安装

### 前置条件

- OpenClaw >= 2026.4.0
- Node.js >= 18
- `plugins.entries.agent-self-development.hooks.allowConversationAccess = true`

### 步骤

```bash
# 1. 下载并安装插件
openclaw plugins install https://github.com/yangquan0310/openclaw_muti_agent_lab/releases/download/v1.2.4/openclaw-agent-self-development-1.2.4.tgz --force

# 2. 启用插件
openclaw plugins enable agent-self-development

# 3. 配置 cron（必需）
# 创建 ~/.openclaw/cron/jobs.json，添加每日自我更新任务
# 如果不存在 cron 目录，先创建
mkdir -p ~/.openclaw/cron
cat > ~/.openclaw/cron/jobs.json << 'EOF'
{
  "jobs": [
    {
      "id": "daily-self-update",
      "name": "每日自我更新",
      "schedule": "0 0 * * *",
      "timezone": "Asia/Shanghai",
      "message": "[cron:每日自我更新]",
      "enabled": true
    }
  ]
}
EOF

# 4. 配置 Agent 白名单
# 编辑 ~/.openclaw/openclaw.json，在 agents.list[].tools.alsoAllow 中添加插件 ID

# 5. 配置 hooks 权限
# 编辑 ~/.openclaw/openclaw.json，确保 allowConversationAccess = true

# 6. 重启 Gateway
openclaw gateway restart
```

---

## CRON 配置详解

本插件**不内置任何定时器**，每日自我更新完全依赖 OpenClaw 的 cron 机制触发。

### jobs.json 文件位置

```
~/.openclaw/cron/jobs.json
```

如果目录不存在，手动创建：
```bash
mkdir -p ~/.openclaw/cron
```

### 最小配置

```json
{
  "jobs": [
    {
      "id": "daily-self-update",
      "name": "每日自我更新",
      "schedule": "0 0 * * *",
      "timezone": "Asia/Shanghai",
      "message": "[cron:每日自我更新]",
      "enabled": true
    }
  ]
}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | ✅ | 任务唯一标识 |
| `name` | string | ❌ | 任务名称（便于识别） |
| `schedule` | string | ✅ | Cron 表达式，如 `0 0 * * *`（每天 00:00） |
| `timezone` | string | ❌ | 时区，默认 UTC。建议设为 `Asia/Shanghai` |
| `message` | string | ✅ | 触发时发送给 Agent 的消息。必须包含 `[cron:每日自我更新]` |
| `enabled` | boolean | ❌ | 是否启用，默认 `true` |

### 常用 schedule 示例

| 需求 | Cron 表达式 |
|------|------------|
| 每天 00:00 | `0 0 * * *` |
| 每天 08:00 | `0 8 * * *` |
| 每周一 00:00 | `0 0 * * 1` |
| 每 6 小时 | `0 */6 * * *` |

### 多个任务

```json
{
  "jobs": [
    {
      "id": "daily-self-update",
      "schedule": "0 0 * * *",
      "timezone": "Asia/Shanghai",
      "message": "[cron:每日自我更新]",
      "enabled": true
    },
    {
      "id": "weekly-review",
      "schedule": "0 9 * * 1",
      "timezone": "Asia/Shanghai",
      "message": "[cron:每周回顾]",
      "enabled": true
    }
  ]
}
```

### 验证 cron 是否生效

```bash
# 查看已配置的 cron 任务
openclaw cron list

# 手动触发测试（不会等待定时器）
openclaw cron run daily-self-update
```

### 故障排查

| 现象 | 原因 | 解决 |
|------|------|------|
| 到点未触发 | Gateway 未重启 | `openclaw gateway restart` |
| 时区不对 | 未设置 `timezone` | 添加 `"timezone": "Asia/Shanghai"` |
| 插件未响应 | message 不匹配 | 确保包含 `[cron:每日自我更新]` |
| jobs.json 被覆盖 | 安装插件时重置 | 备份后重新写入 |

---

### 配置示例（openclaw.json）

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "tools": {
          "alsoAllow": ["agent-self-development"]
        }
      }
    ]
  },
  "plugins": {
    "entries": {
      "agent-self-development": {
        "enabled": true,
        "hooks": {
          "allowConversationAccess": true
        },
        "config": {
          "metacognition": {
            "enabled": true,
            "planning": true,
            "monitoring": true
          },
          "workingMemory": {
            "enabled": true,
            "trackSubagents": true,
            "autoArchive": true
          },
          "assimilation": {
            "enabled": true
          }
        }
      }
    }
  }
}
```

---

## 配置项

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `metacognition.enabled` | boolean | `true` | 元认知模块总开关 |
| `metacognition.planning` | boolean | `true` | 计划阶段（注入 planning skill） |
| `metacognition.monitoring` | boolean | `true` | 监控阶段（注入 monitoring skill） |
| `workingMemory.enabled` | boolean | `true` | 工作记忆模块总开关 |
| `workingMemory.trackSubagents` | boolean | `true` | 追踪会话创建/完成 |
| `workingMemory.autoArchive` | boolean | `true` | 任务结束时注入 working_memory skill |
| `assimilation.enabled` | boolean | `true` | 同化顺应模块总开关（检测 cron 消息） |

---

## 验证

```bash
# 查看插件列表
openclaw plugins list

# 查看插件详情
openclaw plugins inspect agent-self-development --json

# 查看钩子列表
openclaw hooks list

# 查看 cron 任务
openclaw cron list
```

---

## 卸载

```bash
openclaw plugins uninstall agent-self-development
openclaw gateway restart
```

---

*版本: 1.2.4*
