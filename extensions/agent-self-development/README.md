# openclaw-agent-self-development

OpenClaw 官方插件 —— Agent 自我发展系统

基于皮亚杰认知发展理论 + Baddeley 工作记忆模型，将原本依赖文档指导的 `agent_self_development` 技能升级为**官方 Hook 驱动插件**。

---

## 与技能版的本质区别

| 能力 | 技能版 (SKILL.md) | 插件版 (OpenClaw Hooks) |
|------|-------------------|------------------------|
| 计划 | Agent 读文档后自觉制定 | `before_agent_start` → 自动生成计划 |
| Prompt 注入 | Agent 自觉引用计划 | `before_prompt_build` → 自动注入 system context |
| 监控 | Agent 自觉调用 MCP 工具 | `llm_output` → 自动分析偏差 |
| 调节 | Agent 自觉修正 | `before_agent_finalize` → 自动请求 revise |
| 子代理追踪 | Agent 手动调用 `track_subagent` | `before_tool_call` → 自动追踪 agent/subagent 工具 |
| 记忆归档 | Agent 手动调用 `archive_completed` | `agent_end` → 自动归档 |
| 每日更新 | 等 Cron 消息触发 Agent | `registerService` → 后台定时服务自动执行 |

---

## 官方 SDK 规范

本插件严格遵循 OpenClaw 官方 SDK：

- **入口**: `module.exports = { id, name, register(api) }`
- **配置读取**: `api.pluginConfig`
- **日志输出**: `api.logger.info/debug/warn/error`
- **Hook 注册**: `api.on(name, async (event, ctx) => {}, { priority })`
- **后台服务**: `api.registerService({ id, start: (ctx) => {}, stop: (ctx) => {} })`
- **状态管理**: 插件自管 `~/.openclaw/plugin-state/agent-self-development.json`

参考文档:
- [SDK Overview](https://docs.openclaw.ac.cn/plugins/sdk-overview)
- [Hooks](https://docs.openclaw.ai/plugins/hooks)
- [Plugin API](https://github.com/openclaw/openclaw/blob/main/docs/tools/plugin.md)

---

## 文件结构

```
openclaw-agent-self-development/
├── package.json              # scripts: setup / setup:dry / uninstall
├── README.md
├── scripts/
│   └── install.js            # 自动配置写入脚本
└── src/
    ├── index.js              # 插件入口: { id, name, register(api) }
    ├── state.js              # 插件状态管理（JSON 文件）
    ├── utils.js              # 工具函数 + LLM HTTP 调用
    ├── metacognition.js      # before_agent_start / before_prompt_build / llm_output / before_agent_finalize / agent_end
    ├── working-memory.js     # before_tool_call / after_tool_call / agent_end
    └── assimilation.js       # registerService 后台定时服务
```

---

## 配置要求

本插件使用了 `llm_output`、`before_agent_finalize`、`agent_end` 等 **Conversation Hook**，必须在 `openclaw.json` 中设置：

```json
{
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
            "monitoring": true,
            "regulation": true
          },
          "workingMemory": {
            "enabled": true,
            "trackSubagents": true,
            "autoArchive": true
          },
          "assimilation": {
            "enabled": true,
            "dailyCron": "0 0 * * *",
            "autoUpdate": false,
            "updateThreshold": 0.8
          },
          "llm": {
            "model": "kimi-for-coding",
            "provider": "kimicode"
          }
        }
      }
    },
    "load": {
      "paths": [
        "/root/projects/openclaw-agent-self-development"
      ]
    },
    "allow": [
      "agent-self-development"
    ]
  }
}
```

---

## 安装方式

### 方式一：自动安装脚本（推荐）

```bash
# 预览变更（不写入）
npm run setup:dry

# 正式安装（自动修改 openclaw.json）
npm run setup

# 卸载
npm run uninstall
```

### 方式二：手动配置

1. 将代码同步到目标机器（如 `/root/projects/openclaw-agent-self-development`）
2. 修改 `openclaw.json` 添加 `plugins.entries`、`plugins.load.paths`、`plugins.allow`
3. 重启 Gateway：`openclaw gateway restart`

---

## 验证

```bash
# 查看插件列表
openclaw plugins list

# 查看插件注册详情（含 hooks）
openclaw plugins inspect agent-self-development --json

# 查看钩子列表
openclaw hooks list
```

---

*创建时间: 2026-04-27*
