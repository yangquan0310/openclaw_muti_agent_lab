# openclaw-agent-self-development

OpenClaw 插件 —— Agent 自我发展系统

基于皮亚杰认知发展理论 + Baddeley 工作记忆模型，将原本依赖文档指导的 `agent_self_development` 技能升级为**官方 Hook 驱动插件**。

---

## 插件版与技能版的本质区别

| 能力 | 技能版 (SKILL.md) | 插件版 (OpenClaw Hooks) |
|------|-------------------|------------------------|
| 计划 | Agent 读文档后自觉制定 | `before_prompt_build` → 自动生成并注入计划 |
| Prompt 注入 | Agent 自觉引用计划 | `before_prompt_build` → 自动注入 system context |
| 监控 | Agent 自觉调用 MCP 工具 | `llm_output` → 自动分析偏差与阻塞 |
| 调节 | Agent 自觉修正 | `before_agent_finalize` → 自动请求 revise |
| 会话追踪 | Agent 手动调用 `track_subagent` | `before_tool_call` → 自动追踪 agent/subagent 工具 |
| 记忆归档 | Agent 手动调用 `archive_completed` | `agent_end` → 自动归档 completed，删除 killed |
| 每日更新 | 等 Cron 消息触发 Agent | `registerService` → 后台定时服务自动执行 |

---

## 核心业务流程

### 流程一：任务生命周期（六阶段闭环）

Agent 处理**单个任务**的完整流程，从接到需求到最终归档。

```
阶段0：会话初始化
    ├── 载入 SOUL.md / IDENTITY.md / MEMORY.md / TOOLS.md
    └── 初始化工作记忆（读取当前活跃任务看板、活跃会话清单）
    ↓
阶段1：任务决策
    ├── 快速查询 / Cron → 主代理直接执行（跳至阶段5）
    └── 复杂任务 → 进入元认知闭环
    ↓
阶段2：计划（Planning）
    ├── 目标澄清、约束识别
    ├── 任务层级拆解
    ├── 检查工作记忆中的会话（复用或创建）
    ├── 为子任务分配建议的会话标识（session:{TYPE}:{任务标识}）
    └── 在工作记忆创建任务记录（状态：active）
    ↓
阶段3：执行与监控（Monitoring）
    ├── 检查并复用会话（读取工作记忆）
    ├── 向会话分配任务，通过会话ID调用 session_send 通信
    ├── 持续跟踪会话状态
    ├── 更新工作记忆（最后活跃时间、进度）
    └── 偏差检测（错误信号 / 阻塞 / 方案偏离）
    ↓
阶段4：调节（Regulation）（条件触发）
    ├── 根因分析
    ├── 生成调节方案
    ├── 执行调节（paused → active）
    └── 返回阶段3继续监控
    ↓
阶段5：任务完成与归档
    ├── 更新状态为 completed / killed
    ├── 记录完成摘要到工作记忆
    ├── completed → 归档到事件记忆表后删除
    └── killed → 直接删除，不归档
```

**会话管理规则**：
- 创建：通过 `agent` / `subagent` 工具创建，使用 `id` / `name` 作为标识
- 通信：创建后直接使用该 ID 调用 `session_send` 传递消息
- 复用：执行前检查「活跃会话清单」，若已存在相同标识的会话则复用

---

### 流程二：自我发展生命周期（每日同化与顺应）

Agent **每天自我进化**的流程，固定在北京时间每天 00:00 触发。

```
每日 00:00 定时触发
    ↓
1. 阅读昨日事件记忆（events/YYYY-MM-DD/*.md）
    ↓
2. 撰写/完善发展日记（diary/YYYY-MM-DD.md）
    ├── 任务回顾、成功经验提取、失败教训总结
    └── 新技能/知识记录、更新触发检查
    ↓
3. 阅读核心自我与配置文件
    ├── MEMORY.md（核心自我认知）
    ├── SOUL.md（风格与信念）
    ├── IDENTITY.md（身份定义）
    └── skills/README.md（个人技能索引）
    ↓
4. 同化与顺应分析（对比日记与核心自我）
    ├── 同化：原有内容的细化（置信度 < 0.8）
    └── 顺应：新结构的出现（置信度 ≥ 0.8）
    ↓
5. 检测更新触发信号
    ├── 自我认知变化 → core_self_update
    ├── 角色变化 → identity_update
    ├── 信念/风格调整 → belief_style_update
    └── 技能变化 → skills_update
    ↓
6. 执行相应更新
    ├── 更新 IDENTITY.md / SOUL.md / MEMORY.md
    ├── 固化个人 skills（创建/更新技能文件，更新 skills/README.md 索引）
    └── 同步到 lab_repository
    ↓
7. 记录更新日志
    ├── 更新 MEMORY.md 历史版本
    └── 生成 self-update 事件文件（events/YYYY-MM-DD/HH-MM-SS-self-update.md）
```

**发展循环**：
```
执行任务 → 记录日记 → 同化顺应分析 → 自我更新 → 能力进化 → 更好地执行任务
     ↑                                                                    ↓
     └──────────────────────── 持续循环 ←─────────────────────────────────┘
```

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

> **导入约定**：本插件使用官方推荐的 ESM 入口方式
> ```js
> import { definePluginEntry } from 'openclaw/plugin-sdk/plugin-entry';
> export default definePluginEntry({ id, name, register(api) { ... } });
> ```

---

## 文件结构

```
openclaw-agent-self-development/
├── openclaw.plugin.json      # Native plugin manifest (id / name / version / main / configSchema)
├── package.json              # npm 包配置 (type: module / openclaw.extensions / bundledDependencies)
├── README.md
├── src/
│   ├── index.js              # 插件入口: export default definePluginEntry({ register(api) })
│   ├── state.js              # 插件状态管理（JSON 文件）
│   ├── utils.js              # 工具函数 + LLM HTTP 调用 + 会话分配
│   ├── metacognition.js      # before_prompt_build / llm_output / before_agent_finalize / agent_end
│   ├── working-memory.js     # before_tool_call / after_tool_call / agent_end
│   └── assimilation.js       # registerService 后台定时服务
└── skills/                   # 技能文档（原始文档规范）
    ├── metacognition/
    ├── working_memory/
    └── assimilation_accommodation/
```

---

## 配置要求

本插件使用了 `llm_output`、`before_agent_finalize`、`agent_end` 等 **Conversation Hook**，必须在 `openclaw.json` 中设置 `allowConversationAccess: true`。安装后通过 `openclaw plugins enable` 启用时，CLI 会自动处理配置。

默认配置项：

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `metacognition.enabled` | boolean | `true` | 元认知模块总开关 |
| `metacognition.planning` | boolean | `true` | 计划阶段（生成并注入执行计划） |
| `metacognition.monitoring` | boolean | `true` | 监控阶段（llm_output 偏差检测） |
| `metacognition.regulation` | boolean | `true` | 调节阶段（before_agent_finalize revise） |
| `workingMemory.enabled` | boolean | `true` | 工作记忆模块总开关 |
| `workingMemory.trackSubagents` | boolean | `true` | 追踪 agent/subagent 工具调用 |
| `workingMemory.autoArchive` | boolean | `true` | agent_end 时自动归档 completed 任务 |
| `assimilation.enabled` | boolean | `true` | 同化顺应模块总开关 |
| `assimilation.dailyCron` | string | `"0 0 * * *"` | 每日自我更新定时表达式 |
| `assimilation.autoUpdate` | boolean | `false` | 是否自动应用更新（ false 则仅记录待确认信号） |
| `assimilation.updateThreshold` | number | `0.8` | 自动更新置信度阈值 |
| `llm.model` | string | `"kimi-for-coding"` | LLM 模型 |
| `llm.provider` | string | `"kimicode"` | LLM 提供商 |

---

## 安装与卸载

> **⚠️ 安装前必读**
> 1. **备份配置**：`cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak`
> 2. **清理旧版本**：如果之前安装过，先删除旧目录或加 `--force` 覆盖
> 3. **安装依赖**：本插件依赖 `node-cron`，如果 `.tgz` 未包含 `node_modules`，安装后需在插件目录运行 `npm install`
> 4. **配置白名单**：安装后需手动将 `agent-self-development` 添加到 Agent 的 `tools.alsoAllow`

本插件通过 **GitHub Release** 发布，不依赖 npm。

### 安装

```bash
# 方式一：从本地源码目录安装（开发/自建）
# 先进入插件目录安装依赖
npm install
openclaw plugins install ./openclaw-agent-self-development

# 方式二：从 GitHub Release 下载 .tgz 后安装
# 1. 从 Release 页面下载 openclaw-agent-self-development-1.2.1.tgz
# 2. 执行安装（如旧版本存在，加 --force 强制覆盖）
openclaw plugins install ./openclaw-agent-self-development-1.2.1.tgz --force

# 方式三：开发模式链接（免复制，代码修改即时生效）
openclaw plugins install -l ./openclaw-agent-self-development

# 启用插件
openclaw plugins enable agent-self-development

# 重启 Gateway
openclaw gateway restart
```

### 更新

```bash
# 重新下载最新 Release 的 .tgz 后强制覆盖安装
openclaw plugins install ./openclaw-agent-self-development-1.2.1.tgz --force

# 或从本地源码路径强制覆盖（开发时常用）
openclaw plugins install ./openclaw-agent-self-development --force

# 重启 Gateway
openclaw gateway restart
```

### 卸载

```bash
# 卸载插件（移除配置和注册表记录）
openclaw plugins uninstall agent-self-development

# 重启 Gateway
openclaw gateway restart
```

### 安装后配置

#### 1. Agent 工具白名单

安装后需将插件 ID 添加到 Agent 的 `tools.alsoAllow`，否则 Agent 无法调用插件功能：

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
  }
}
```

#### 2. Hooks 权限

本插件使用了 `llm_output`、`before_agent_finalize`、`agent_end` 等 **Conversation Hook**，需在 `openclaw.json` 中设置：

```json
{
  "plugins": {
    "entries": {
      "agent-self-development": {
        "enabled": true,
        "hooks": {
          "allowConversationAccess": true
        }
      }
    }
  }
}
```

#### 3. 清理无效路径

如果之前有通过 `plugins.load.paths` 加载旧版本，运行以下命令清理：

```bash
openclaw doctor --fix
```

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
