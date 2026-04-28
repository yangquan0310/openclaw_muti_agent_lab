# openclaw-agent-self-development

OpenClaw 插件 —�?Agent 自我发展框架

> **插件定位**：纯钩子框架（Hook Router）。在 Agent 执行任务的特定时机，�?`skills/` 目录下的 skill 文档注入 Agent �?system context，作为脚手架指导 Agent 行为�?>
> **核心原则**：插件只负责"提醒"（注�?skill），Agent 负责"执行"（自行决策、读写文件、管理任务空间）�?
---

## 认知发展理论基础

本框架的设计根植于三大认知科学理论，将人类认知机制映射为 Agent 的软件架构�?
### 皮亚杰认知发展理论（Piaget�?
皮亚杰认为认知发展通过 **同化（Assimilation�?* �?**顺应（Accommodation�?* 的交替作用实现：
- **同化**：将新经验纳入现有认知图式。Agent 执行日常任务时，新经验被整合到既有技能体系（Skills 对象）和工作信念（Belief 对象）中�?- **顺应**：当新经验无法被现有图式容纳时，修改图式本身。Agent 遇到全新的任务类型或工作方式时，需要更新能力边界（Self 对象）、角色集（Identity 对象）甚至创建新的技能文档�?- **平衡（Equilibration�?*：同化与顺应的动态平衡驱动认知发展。每�?cron 触发�?Personality 模块正是这一机制的实现——通过回顾昨日事件（WorkingMemory.Event）、撰写发展日记（Diary 对象）、对比核心自我文件（SOUL.md / IDENTITY.md / MEMORY.md），判断当日经验属于同化还是顺应，并执行相应更新�?
### Baddeley 工作记忆模型

Baddeley 将工作记忆分�?**语音环路**�?*视觉空间画板**�?*情景缓冲�?* �?**中央执行系统**。在 Agent 语境下映射为�?- **中央执行系统** �?`WorkingMemoryModule`：协调任务空间的创建、复用、归档和销毁，管理注意力分配（同任务族复用 idle 空间，不同任务族并行）�?- **情景缓冲�?* �?`Session`（任务空间）：承载单个任务的完整上下文，�?Agent 执行特定任务时的"内存空间"�?- **长期记忆接口** �?`Memory` 对象：completed 任务空间经归档（Archive）后存入按日聚合�?`memory_table`，成为可回顾的长期记忆�?
### Flavell 元认知理�?
Flavell 将元认知定义�?**"对认知的认知"**，包含三个核心成分：
- **元认知知�?* �?`Plan` 对象：Agent �?要做什么、用什么做、做到什么程�?的完整上下文理解，不只是步骤列表�?- **元认知监�?* �?`Monitor` 对象：每�?LLM 输出后，系统注入 monitoring skill，Agent 自行检查当前输出是否与 Plan 偏离�?- **元认知调�?* �?`Regulator` 对象：当 Monitor 检测到偏差时，Agent 自行生成调节方案（调�?phases、重新汇报、或跳过阶段并说明理由）�?
**关键设计**：元认知不是插件�?Agent 做决策，而是插件在正确时机注�?skill 文档，Agent 阅读后自行执行监控与调节�?
---

## 三层架构

```
┌─────────────────────────────────────────────�?�?             用户层（User�?                  �?�? · 下达任务（自然语言�?                       �?�? · 确认/修改/取消 Plan                        �?�? · 查看执行进度                               �?�?             ↑↓ 自然语言对话                  �?└─────────────────────────────────────────────�?              ↑↓
┌─────────────────────────────────────────────�?�?            代理层（Agent�?                  �?�? · 阅读 skill �?制定 Plan �?汇报用户          �?�? · 用户确认后按 phases 在任务空间中推进         �?�? · 每轮 LLM 输出后自检偏差                     �?�? · 任务完成 �?归档产出�?                      �?�?             ↑↓ Hook 事件�?                  �?└─────────────────────────────────────────────�?              ↑↓
┌─────────────────────────────────────────────�?�?          系统层（Plugin/Hooks�?             �?�? before_prompt_build �?注入 planning / 执行上下�?�?�? llm_output          �?注入 monitoring        �?�? before_tool_call    �?记录任务空间创建        �?�? after_tool_call     �?记录事件 / 更新状�?    �?�? agent_end           �?注入 working_memory    �?└─────────────────────────────────────────────�?```

| 层级 | 职责 | 边界 |
|------|------|------|
| **用户�?* | 自然语言下达任务、确�?修改 Plan、提供反�?| 不直接操作系统层 |
| **代理�?* | 阅读 skill 自行决策（制�?Plan、执行监控、归档、写日记�?| 自行管理 Plan 状态、任务空间、核心自我文�?|
| **系统�?* | �?Hook 触发时注入对�?skill 文档，记录状态变�?| 只注�?skill，不�?Agent 做决策；不碰 IDENTITY.md/SOUL.md/MEMORY.md |

---

## 面向对象模型

框架由三个模块（Module）和一组对象（Object）构成。模块负�?Hook 调度，对象是 Agent 操作的数据实体�?
### 元认知模块（MetacognitionModule�?
管理 **Plan �?Monitor �?Regulator** 的闭环。复杂任务时注入 planning skill，active 状态时注入 monitoring skill�?
| 对象 | 职责 | 状态机 | 关联 |
|------|------|--------|------|
| **Plan** | 完整的任务上下文语境（目�?约束/工作空间/阶段化执行） | `draft �?pending_approval �?active �?completed �?destroyed` | 驱动 Session 创建，为 Monitor 提供参照 |
| **Monitor** | 跟踪 LLM 输出�?Plan 的偏离程�?| `idle �?tracking �?alert �?destroyed` | 引用 Plan，触�?Regulator |
| **Regulator** | 接收偏差报告，生成并执行调节方案 | `idle �?analyzing �?executing �?completed �?destroyed` | 修改 Plan 或回�?draft 重新汇报 |

**Plan 状态转换规�?*�?
| 当前状�?| 触发条件 | 新状�?|
|----------|----------|--------|
| 不存�?| 收到复杂任务 | `draft` |
| `draft` | Agent 制定完成并汇�?| `pending_approval` |
| `pending_approval` | 用户确认 | `active` |
| `pending_approval` | 用户要求修改 | `pending_approval`（重新汇报） |
| `pending_approval` | 用户取消 | `completed` |
| `active` | 阶段正常推进 | `active`（currentPhase++�?|
| `active` | 所�?phases 完成 | `completed` |
| `active` | 重大偏差需重规�?| `draft`（重新汇报） |
| `completed` | `agent_end` | `destroyed` |

**核心原则**：`draft` 必须汇报，`pending_approval` 必须等待用户确认，只�?`active` 才能执行�?
**Plan 对象结构**（Agent 通过 skill 了解完整属性，�?`skills/metacognition/planning/SKILL.md`）：

```json
{
  "runId": "uuid",
  "prompt": "用户原始输入",
  "status": "draft",
  "context": { "goal": "", "constraints": [], "successCriteria": [] },
  "workspace": { "sessions": [], "artifacts": [], "tools": [] },
  "execution": { "phases": [], "currentPhase": 0 }
}
```

> **工作流详�?*：见 `skills/metacognition/planning/SKILL.md`（制定并汇报、处理确认、阶段化执行、任务空间管理）�?
### 工作记忆模块（WorkingMemoryModule�?
管理 **Session �?Event �?Archive �?Memory** 的全生命周期。任务空间跨 runId 复用，completed 归档，killed 销毁�?
| 对象 | 职责 | 生命周期 | 持久�?|
|------|------|----------|--------|
| **Session** | 执行特定任务的内存空�?| `pending �?active �?completed/killed/paused`；completed �?`idle`（可复用）；killed �?销�?| `session_list:{runId}`（运行级�? `working_memory:active_sessions`（全局索引�?|
| **Event** | 工具调用错误记录 | 按日累积 | `events:{YYYY-MM-DD}` |
| **ToolRecord** | 工具调用创建/完成记录 | runId �?| `wm:{runId}:tools` |
| **Archive** | completed Session 的归档记�?| 日期�?| `memory_table:{YYYY-MM-DD}` |
| **Memory** | 按日聚合的归档记录集�?| 长期保留 | `memory_table:{YYYY-MM-DD}` |

**Session 状态转�?*�?
```
不存�?�?before_tool_call �?pending �?开始执�?�?active
  ├─ 正常完成 �?completed �?agent_end �?Archive �?Memory + idle
  ├─ 工具报错 �?killed �?agent_end �?销�?  └─ 主动暂停 �?paused �?恢复 �?active
```

**任务空间复用规则**：同一 `taskFamily`（CODE/RESEARCH/ANALYSIS/WRITING/TEST/DESIGN/TASK）的后续任务复用 idle 空间，标识格�?`session:{TYPE}:{任务族}`�?
> **工作流详�?*：见 `skills/working_memory/session/SKILL.md`（创�?监控/完成/终止）和 `skills/working_memory/memory/SKILL.md`（归�?清理）�?
### 人格模块（PersonalityModule�?
基于皮亚杰同�?顺应理论，每�?cron 触发时驱�?Agent 回顾昨日事件、撰写发展日记、更新核心自我文件�?
| 对象 | 职责 | 对应文件 |
|------|------|----------|
| **Personality** | 容器，驱动每日更新流�?| �?|
| **Diary** | 撰写日记、提取更新触发信�?| `diary/YYYY-MM-DD.md` |
| **Belief** | 工作信念与风�?| `SOUL.md` |
| **Self** | 能力边界与责任边�?| `MEMORY.md` |
| **Identity** | 角色集与社会身份 | `IDENTITY.md` |
| **Skills** | 个人技能体�?| `skills/README.md` |

**Personality 生命周期**�?
```
idle �?cron 触发 �?reflecting（Diary 撰写�?  �?updating（对比核心自我，检测变化信号）
    ├── 自我认知变化 �?Self 更新
    ├── 角色变化 �?Identity 更新
    ├── 信念调整 �?Belief 更新
    └── 技能变�?�?Skills 更新
  �?syncing �?idle
```

**同化 vs 顺应判定**�?- **同化**：原有内容的细化 �?调用子对象的 update 方法
- **顺应**：新结构的出�?�?调用子对象的 create 方法

> **工作流详�?*：见 `skills/personality/SKILL.md`（任务工作流六阶段闭环、每日同化与顺应）�?
### 模块协作关系

```
Metacognition.Plan ──�?WorkingMemory.Session 创建/复用
Metacognition.Monitor ──�?WorkingMemory.Session 状态同�?Metacognition.Regulator ──�?WorkingMemory.Session 暂停/恢复

WorkingMemory.Session.completed ──�?WorkingMemory.Archive ──�?Memory
WorkingMemory.Event ──�?Personality.Diary（每日回顾）
WorkingMemory.Memory.archives ──�?Personality（反思已完成任务�?```

---

## 系统层：Hook 注入映射

| Hook | 条件 | 注入 skill | 操作对象 |
|------|------|------------|----------|
| `before_prompt_build` | 复杂任务 + Plan 不存�?draft | `planning` | Plan |
| `before_prompt_build` | Plan pending_approval | `planning` | Plan |
| `before_prompt_build` | Plan active | 执行上下文（当前阶段提醒�?| Plan |
| `llm_output` | Plan active | `monitoring` | Monitor |
| `before_tool_call` | 会话工具调用 | —（仅记录） | Session |
| `after_tool_call` | 任意 | —（仅记录错�?状态） | Event / Session |
| `agent_end` | 任意 | `working_memory` | Memory |
| `before_prompt_build` | cron 消息 | `personality` | Personality |

---

## 职责边界

| 职责 | 用户�?| 代理�?| 系统�?|
|------|--------|--------|--------|
| 下达任务 | �?| �?| �?|
| 确认/修改 Plan | �?| �?| �?|
| 制定 Plan | �?| �?阅读 skill 自行制定 | �?注入 planning skill |
| 汇报 Plan | �?| �?| �?|
| 执行监控 | �?| �?阅读 skill 自行检�?| �?注入 monitoring skill |
| 任务空间管理 | �?| �?自行决定复用/创建 | �?记录状态变�?|
| 每日自我更新 | �?| �?阅读 skill 自行写日�?| �?注入 personality skill |
| 核心文件读写 | �?| �?自行读写 | �?不碰 |
| 定时任务 | �?| �?| �?不内置定时器（用户配�?OpenClaw cron�?|

---

## 技术实�?
### 源码结构

```
openclaw-agent-self-development/
├── openclaw.plugin.json          # 插件 manifest
├── package.json                  # npm 包配置（ESM�?├── HOOK.md                       # Hook 事件声明
├── README.md                     # 本文�?├── src/
�?  ├── index.js                  # 插件入口：依赖注入，创建并注册三大模�?�?  ├── metacognition.js          # MetacognitionModule（Plan/M/Regulator 调度�?�?  ├── working-memory.js         # WorkingMemoryModule（Session 生命周期�?�?  ├── assimilation.js           # PersonalityModule（cron 检�?/ skill 注入�?�?  ├── skills-loader.js          # SkillLoader（带缓存�?�?  ├── state.js                  # PluginState（并发安�?JSON 持久化）
�?  └── utils.js                  # 工具函数（日期、Plan 模板、任务族推断�?└── skills/                       # Skill 文档（面向对象结构）
    ├── metacognition/
    �?  ├── SKILL.md              # 模块路由：Plan / Monitor / Regulator
    �?  ├── planning/SKILL.md     # Plan 对象操作指南
    �?  ├── monitoring/SKILL.md   # Monitor 对象操作指南
    �?  └── regulation/SKILL.md   # Regulator 对象操作指南
    ├── working_memory/
    �?  ├── SKILL.md              # 模块路由：Session / Memory
    �?  ├── memory/SKILL.md       # Memory 对象操作指南
    �?  └── session/SKILL.md      # Session 对象操作指南
    ├── personality/
    �?  ├── SKILL.md              # 模块路由：Belief / Self / Identity / Skills / Diary
    �?  ├── belief/SKILL.md       # Belief 对象操作指南
    �?  ├── self/SKILL.md         # Self 对象操作指南
    �?  ├── identity/SKILL.md     # Identity 对象操作指南
    �?  ├── skills/SKILL.md       # Skills 对象操作指南
    �?  └── diary/SKILL.md        # Diary 对象操作指南
    └── _meta.json                # Skill 元数据索�?```

### 面向对象类设�?
| �?| 职责 | 方法 |
|---|------|------|
| `PluginState` | JSON 文件状态管理（并发安全�?| `get()`, `set()`, `append()`, `_persist()` |
| `SkillLoader` | Skill 文件加载与缓�?| `load()`, `clearCache()`, `getAvailableSkills()` |
| `MetacognitionModule` | 元认知闭环调�?| `onBeforePromptBuild()`, `onLlmOutput()`, `onAgentEnd()` |
| `WorkingMemoryModule` | 任务空间生命周期管理 | `onBeforeToolCall()`, `onAfterToolCall()`, `onAgentEnd()` |
| `PersonalityModule` | 每日自我更新触发 | `onBeforePromptBuild()` |

### 状态存储键空间

| �?| 类型 | 生命周期 | 说明 |
|----|------|----------|------|
| `plan:{runId}` | Plan | runId | 当前运行�?Plan |
| `output:{runId}` | string | runId | Monitor 引用的最�?LLM 输出 |
| `session_list:{runId}` | Session[] | runId | 本次运行的任务空间快�?|
| `wm:{runId}:tools` | ToolRecord[] | runId | 本次运行的工具记�?|
| `events:{YYYY-MM-DD}` | Event[] | 日期 | 按日累积的错误事�?|
| `memory_table:{YYYY-MM-DD}` | Archive[] | 日期 | 按日累积�?completed 归档 |
| `working_memory:active_sessions` | Session[] | 全局 | 全局活跃任务空间索引（Memory Table 管理中心�?|

---

## 安装

### 前置条件

- OpenClaw >= 2026.4.0
- Node.js >= 18
- `plugins.entries.agent-self-development.hooks.allowConversationAccess = true`

### 步骤

```bash
# 1. 安装插件
openclaw plugins install https://github.com/yangquan0310/openclaw_muti_agent_lab/releases/download/v2.0.2/openclaw-agent-self-development-2.0.2.tgz --force

# 2. 启用
openclaw plugins enable agent-self-development

# 3. 配置 cron（必需�?mkdir -p ~/.openclaw/cron
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

# 4. 编辑 ~/.openclaw/openclaw.json 配置 Agent 白名单与 hooks 权限

# 5. 重启 Gateway
openclaw gateway restart
```

### 配置示例

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "tools": { "alsoAllow": ["agent-self-development"] }
      }
    ]
  },
  "plugins": {
    "entries": {
      "agent-self-development": {
        "enabled": true,
        "hooks": { "allowConversationAccess": true },
        "config": {
          "metacognition": { "enabled": true, "planning": true, "monitoring": true },
          "workingMemory": { "enabled": true, "trackSubagents": true, "autoArchive": true },
          "personality": { "enabled": true }
        }
      }
    }
  }
}
```

### 配置�?
| 配置�?| 类型 | 默认�?| 说明 |
|--------|------|--------|------|
| `metacognition.enabled` | boolean | `true` | 元认知模块总开�?|
| `metacognition.planning` | boolean | `true` | 计划阶段（draft �?pending_approval �?active�?|
| `metacognition.monitoring` | boolean | `true` | 监控阶段（仅 active 状态注�?monitoring�?|
| `workingMemory.enabled` | boolean | `true` | 工作记忆模块总开�?|
| `workingMemory.trackSubagents` | boolean | `true` | 追踪任务空间创建/完成 |
| `workingMemory.autoArchive` | boolean | `true` | 任务结束�?Archive �?Memory 归档 |
| `personality.enabled` | boolean | `true` | 人格模块总开关（cron 检测） |

> **向后兼容**：`config.assimilation` 仍可工作，内部映射到 `personality`�?
---

## 验证

```bash
openclaw plugins list
openclaw plugins inspect agent-self-development --json
openclaw hooks list
openclaw cron list
openclaw cron run daily-self-update   # 手动触发每日更新测试
```

---

## 卸载

```bash
openclaw plugins uninstall agent-self-development
openclaw gateway restart
```

---

*版本: 2.0.1*
