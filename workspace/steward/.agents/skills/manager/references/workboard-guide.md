# Workboard 任务发布指南 v1.8.0

> **v1.8.0 重大补充**（2026-06-06 老板指正 + 联动测试验证）：
> 1. **新加"三之3、大管家使用技巧"**——明确"大管家不做什么"、"看 status 简化判断"、"agentId 副作用及应对"
> 2. 4 场联动测试验证（v8.26.0 实测）：A done 路径 / B blocked 路径 / C subagent 自管 workboard / D notify_subscribe 链路
>
> **v1.7.0 重大修复**（2026-06-06 老板纠错，老板拍板）：
> 1. **删除 `manager workboard` CLI**（v2026.6.6）—— `scripts/workboard/` 整个目录（932 行 Python）已删除
> 2. **建卡改用 agent tool**（`workboard_create`）或 **plugin 自带 CLI**（`openclaw workboard create`）
> 3. **核验/验收改用 agent tool**（`workboard_read` / `workboard_comment` / `workboard_complete` / `workboard_delete` 等）
> 4. **大管家 3 动作铁律保持**（建卡 + im/spawn 派发 + 验收），但"建卡"和"验收"全部走 agent tool，**不再走 manager CLI**
> 5. **踩坑教训**：v8.25.0 拍板时漏看了 `workboard_create` agent tool 一直就在 plugin contract tools 里（`extensions/workboard/openclaw.plugin.json:18`），错让老板创建 932 行 Python 脚本——**完全没必要的**。**v1.7.0 撤销 v8.25.0 沉淀，建卡用 tool/plugin CLI**
>
> **v1.6.0 同步升级**（2026-06-06，对接 SKILL.md v5.12.0 老板拍板）：
> 1. **明确 workboard 永远只管"建卡/管理"**（v3.2.0 铁律）—— workboard CLI 不接派发能力，**绝对禁止**加 spawn / dispatch 子命令
> 2. **加"3 动作铁律"章节**（v1.6.0 新增）——大管家 3 个动作：建卡 + im/spawn 派发 + 验收
> 3. **§二、什么时候用 Workboard** 加"私聊派发也用"——workboard 在 DM 场景下走 `--no-session` 建卡
> 4. **§三、能力边界"关键分工"**重写——大管家 = 建卡层（CLI），派发动作走 IM 群 / sessions_spawn，不走 workboard
> 5. 同步 task-flow-guide.md v3.2.0 导航（§二、群派发 / §三、私聊派发）

> **v1.5.0 重大简化**（2026-06-06）—— 已被 v1.6.0 取代，仅作历史参考：
> 1. **删除 `start` 子命令**（代码 + 文档）——卡建好后大管家不再"启 session"，代理自己 claim + 启动 run
> 2. 派发流程从 **5+1 步 → 4 步**（create → IM 艾特 → 代理 claim → 代理执行 + proof）
> 3. 卡状态机去掉"start 步骤"——"running"转换由代理手动 chat.send / 调度触发
> 4. "Dashboard 限制"章节删"manager workboard start"推荐路径
> 5. 三件套架构改"create 派发"
> 6. 错误排查删 3 条 start 相关

> **v1.4.0 重大更新**(2026-06-03)--已被 v1.5.0 取代,仅作历史参考:

> **v1.3.0 认知更正**:本指南之前定位为"大管家调度控制台"。**错的**。
> 正确理解(从 OpenClaw 官方插件 `plugin.json` 描述):**`Dashboard workboard for agent-owned issues and sessions`**。
> **Workboard 的真正主用户是 agent**(writer / reviewer / psychologist / ...),不是大管家/用户。Dashboard 只是人类旁观察看。

---

## 一、Workboard 是什么(官方定义)

**官方插件描述**(`@openclaw/workboard/plugin.json`):

> `"description": "Dashboard workboard for agent-owned issues and sessions."`

**三个关键点**:
- **Dashboard** - 跑在 Dashboard 标签页,人类旁观察看
- **agent-owned** - 卡片归**代理**所有,**不归用户**所有
- **issues and sessions** - issue(工单) + session(执行载体)**两个并列的一等公民**

**绝对禁止**的误解:
- ❌ 把 workboard 当 TODO 平替
- ❌ 把 workboard 当 "大管家调度控制台"
- ❌ 把 Dashboard 编辑表单渲染当真理(数据对就行,Dashboard 编辑表单有已知 UX bug)

OpenClaw Workboard 是 Dashboard 看板系统(http://10.0.0.9:18098/estqvr/),提供:

- **结构化任务卡片**(id / status / priority / labels / assignee / claim / proof)
- **认领 + 心跳 + 释放** 机制(防抢任务、防崩、防僵死)
- **SQLite 持久化**(重启不丢)
- **状态机**:`backlog → todo → running → review / blocked → done → archived`

**与 MEMORY.md 任务看板的区别**:

| 维度 | MEMORY.md | Workboard |
|------|-----------|-----------|
| 形态 | Markdown 文本 | 结构化卡片 |
| 协作 | 单 Agent 记事 | 多 Agent 互斥认领 |
| 进度 | 手动更新 | 自动状态机 |
| 证据 | 文字描述 | proof artifact |
| 持久化 | 文本文件 | SQLite |

---

## 二、什么时候用 Workboard

### ✅ 适合用

- 多 Agent 协作任务（写作助手 → 数学家 → 审稿人 接力）
- 长任务（数小时到数天，需要 claim 防僵死）
- 需要可追溯证据的任务（v1→v7 版本演进、proof 沉淀）
- Bug 追踪（已知 bug 建卡跟踪）
- 每日定时任务的报告卡（T042 每日 OpenClaw 检查）
- **两种派发场景（v1.6.0 新增）**：
  - **群派发**：IM 群里交任务，建卡绑群 session（`--session feishu:group:oc_xxx`），Dx 自动同步
  - **私聊派发**（v3.2.0）：老板在 DM 里交任务，建卡不绑 session（`--no-session`），大管家手动 sessions_spawn 启子代理
  - 详见 task-flow-guide.md v3.2.0（§二、群派发 / §三、私聊派发）

### ❌ 不必用

- 单 Agent 短期任务（一句话能说完的）
- 临时讨论、IM 问询
- 简单进度跟踪（MEMORY.md 够用）

---

## 三、能力边界(重要)

### Agent 工具集(代理直接可用)

| 工具 | 用途 | 谁用 |
|------|------|------|
| `workboard_list` | 列卡 | 代理 + 大管家 |
| `workboard_read` | 读卡 | 代理 + 大管家 |
| `workboard_claim` | 认领(独占)| **代理**(大管家不调) |
| `workboard_heartbeat` | 续约(防 claim 过期)| **代理** |
| `workboard_release` | 释放(指定下一状态)| **代理** |
| `workboard_comment` | 评论 | 代理 + 大管家 |
| `workboard_proof` | 附证据(artifact)| **代理**(执行完附产出) |
| `workboard_unblock` | 解阻塞卡 | 代理 + 大管家 |

### 大管家建卡/验收（agent tool / plugin CLI，v1.7.0 重写）

**会话内**（大管家主用）：**直接用 `workboard_*` agent tool**——plugin contract tools 里**一直就有**（见 `extensions/workboard/openclaw.plugin.json`）。
**shell / cron 场景**（次用）：**用 `openclaw workboard` plugin 自带 CLI**（runtime-slash 命令）。

| 动作 | agent tool（推荐） | plugin CLI（shell 备选） |
|------|---------------------|---------------------------|
| 建卡 | `workboard_create({ title, notes, agentId, status, priority, labels, ... })` | `openclaw workboard create "title" --notes "..." --agent writer --priority high --labels ...` |
| 读卡 | `workboard_read({ id: cardId })` | `openclaw workboard show <id>` |
| 列卡 | `workboard_list({ status, boardId, limit })` | `openclaw workboard list [--board ...] [--status ...]` |
| 评论 | `workboard_comment({ id, body })` | （plugin CLI 无此子命令，用 tool） |
| 验收归档（move done） | `workboard_complete({ id, summary, proof })` | （plugin CLI 无此子命令，用 tool） |
| 删卡 | `workboard_delete({ id })` | （plugin CLI 无此子命令，用 tool） |
| 批量（archive/move） | 多次循环调 `workboard_*` tool | （plugin CLI 无 bulk，循环调 create/list） |

**关键分工**（v1.7.0 重写）：
- **大管家** = **建卡/验收层**（agent tool）。负责：**建卡**（`workboard_create`）+ **验收**（`workboard_read` + `workboard_comment` + `workboard_complete` / `workboard_delete`）
- **代理** = 执行层（agent tool）。负责：claim、heartbeat、release、proof、comment
- **派发动作**（im 群艾特 / sessions_spawn）**由大管家在会话里手动做**，**不走 workboard**

> ❌ **绝对禁止**重建 `manager workboard` CLI 或新增 spawn / dispatch 子命令（v1.6.0 + v1.7.0 拍板）——派发动作永远在会话里手动做。
> ❌ **绝对禁止**再回退到 `scripts/workboard/` Python 包（v1.7.0 删除后，永不重建）。如需 shell 操作，**只用 `openclaw workboard` plugin CLI**。

---

## 三之3、大管家使用技巧（v1.8.0 新增）

> 源自 2026-06-06 v8.26.0 联动测试 + 老板指正："claim 是 session/IM 通知其他代理，大管家不需要管中间态"。

### 3.3.1 大管家不做什么（4 条铁律）

| ❌ 大管家**不**做的 | 由谁做 | 机制 |
|------|------|------|
| 不主动 `workboard_claim` | **代理自己** / **Dx 自动** | Dx 看到 `agentId=writer` 的卡 → spawn 时**自动 claim** 到 writer（实测 C 测试发现） |
| 不主动 `workboard_proof` | **执行代理** | 代理执行完自己调 workboard_proof 附证据 |
| 不盯 todo→running 迁移 | **Dx 自动同步** | 卡绑 sessionKey + session running → 卡 status=running（**大管家不介入**）|
| 不读中间过程 | **无** | 中间态（running/claimed）大管家**不读**——除非有异常 |

**关键洞察**：
- **`claim` 是触发器**，不是大管家的动作
- 群场景：claim 由群 IM 艾特 → 代理自己 workboard_claim
- 私聊场景：claim 由 sessions_spawn 触发子代理 → Dx 看到 agentId 匹配**自动 claim**
- **大管家发完派发通知就完事**——不主动调 claim

### 3.3.2 大管家"看 status" 的简化判断

✅ **看 done** → 核验产出 + `workboard_complete` + archive（可选）
✅ **看 blocked** → 人工介入（`workboard_reassign` / `workboard_unblock` / 重新派发 / 接受失败）
❌ **不看 running**（中间态，不管）
❌ **不看 todo**（已派发，等代理 claim / Dx 自动 claim）

**心智口诀**：**只看头尾，不盯中间**。

### 3.3.3 `workboard_create` `agentId` 副作用及应对

`workboard_create({ agentId: "writer" })` 会触发**副作用**（v8.26.0 实测 C 测试发现）：

1. **Dx 看到 agentId → spawn 阶段自动 claim 到该 agent**（kind: "claimed" 事件自动写入）
2. **claim 后 workboard_comment / workboard_block 等"卡操作"只允许 owner**（报 "card is claimed by writer"）
3. **大管家自己 comment** 到已 claim 的卡 → 报错（除非 workboard_reassign 接管）

**应对策略**：

| 场景 | 应对 |
|------|------|
| 群派发 | workboard_create 后让群里代理**自己 claim + comment**——大管家不介入 |
| 私聊派发 | workboard_create 后 sessions_spawn 触发 Dx auto-claim，子代理**自己调** workboard_comment |
| 大管家想 comment | 选项 A：`workboard_reassign({ id, agentId: "steward" })` 接管 → claim → comment<br>选项 B：建新卡（不与已 claim 的卡冲突）|

### 3.3.4 workboard 状态机 vs 大管家介入点

```
   create                          ← 大管家 [1] 建卡
     ↓
   todo                            ← Dx/代理 auto-claim
     ↓ (claim - 必走！)
   running                         ← Dx 自动同步，**大管家不盯**
     ↓ (代理 workboard_proof + workboard_complete)
   done                            ← 大管家 [3] 核验 + complete + archive
     ↓
   archived                        ← 大管家 [3] 可选

   todo / running
     ↓ (卡失败 / 超时)
   blocked                         ← 大管家 [3] 人工介入

   done ↔ blocked                  ← 大管家可 reassign / unblock 反复折腾
```

**大管家介入点**：**起点 (create) + 终点 (done/blocked) + 中间异常 (blocked 反复)**——**不**盯 running 中间过程。

---

## 三之2、Workboard 永远只管"建卡/管理"（v1.6.0 新增铁律）

> **v1.6.0 老板拍板**（2026-06-06）：workboard 是**任务进度控制工具**（看 §五、卡状态机），**不**包含派发能力本身。

### 大管家 3 动作铁律（v1.7.0 重写）

```
[1] 建卡    →  workboard_create（agent tool，主用）/ openclaw workboard create（plugin CLI，shell 备选）
[2] 派发    →  IM 群艾特（群场景）  /  sessions_spawn（私聊场景）
[3] 验收    →  workboard_read + workboard_comment + workboard_complete（agent tool，全部走 tool）
```

### 两种派发场景下 workboard 的角色

| 场景 | workboard 动作 | 不做的动作 |
|------|----------------|------------|
| **群派发** | `create --session feishu:group:oc_xxx` 建卡，绑群 session | 不启 session（Dx 自动）|
| **私聊派发** | `create --no-session` 建卡，不绑 session | 不启 session（大管家手动 sessions_spawn）|

### 为什么 workboard 不接派发

- workboard plugin 暴露的**所有 35 个 agent tool**（`extensions/workboard/openclaw.plugin.json` 里的 `contracts.tools`）都是"建卡/管理/执行"类动作：
- **建卡/验收**（大管家用）：`workboard_create` / `workboard_read` / `workboard_list` / `workboard_comment` / `workboard_complete` / `workboard_delete` / `workboard_attachment_*` / `workboard_board_*` / `workboard_stats` / `workboard_link` / `workboard_promote` / `workboard_reassign` / `workboard_unblock` / `workboard_specify` / `workboard_decompose` / `workboard_notify_*`
- **执行**（代理用）：`workboard_claim` / `workboard_heartbeat` / `workboard_release` / `workboard_proof` / `workboard_runs` / `workboard_block` / `workboard_reclaim` / `workboard_dispatch` / `workboard_worker_log` / `workboard_protocol_violation`
- **plugin CLI 备选**（shell 场景）：`openclaw workboard create / list / show / dispatch`
- **没有** spawn / dispatch / start 子命令（v1.5.0 删除 start，v1.6.0 确认永远不再加回来）
- 派发动作（IM 群艾特 / sessions_spawn）**永远**由大管家在会话里手动做

### 与 task-flow-guide.md 的关系

- **task-flow-guide.md v3.2.0 §二、群派发场景**：完整 4 步流程（写 TODO → 建卡 → IM 5 段模板 → 核验+群完成确认）
- **task-flow-guide.md v3.2.0 §三、私聊派发场景**：完整 3 步流程（建卡 → sessions_spawn → 核验，不发群、不写 TODO）

**读 workboard-guide.md = 学会 workboard CLI 怎么用**  
**读 task-flow-guide.md v3.2.0 = 学会完整派发流程（含 IM/spawn 派发动作）**

---

## 四、发布任务的 4 步新流程（v1.5.0 简化）

### 心智模型(三件套架构)

```
老板交任务
    ↓
[1] 大管家 workboard_create({...}) 建卡（agent tool，可绑 session，agentId=接收人）
    ↓
[2] 大管家 群里艾特代理(IM 模板,**开头**带 workboard 信息)
    ↓
[3] 代理 收到 → workboard_claim 认领 → 群里回"已认领 card=xxx"
    ↓ (代理自己 chat.send / 调度启 run,不走 workboard start)
[4] 代理执行完 → 群里发完成消息 + workboard_proof 附产出
    ↓
[5] 大管家核验产出 → workboard_read + workboard_complete → done / blocked
```

> v1.5.0 重要变化:**大管家不再调 `manager workboard start`**。代理认领后自己启 run(`chat.send` 触发或 scheduler 调起)。workboard 卡只作"任务声明/看板",派发用 IM 群,启 run 由代理负责。
> v1.7.0 重大修复:**`manager workboard` CLI 整个删除**（`scripts/workboard/` 932 行 Python 已删）。建卡/验收全部走 agent tool，shell 备选用 `openclaw workboard`。

### 步骤 1:明确任务

回答三个问题:
- 任务目标(一句话)
- 指派对象(哪个 agent:`writer` / `reviewer` / `psychologist` / ...)
- 优先级 + 标签(`low/normal/high/urgent` + `labels`)

### 步骤 2:建卡（agent tool / plugin CLI，v1.7.0 重写）

```js
// 主用：agent tool（会话内）
workboard_create({
  title: "...",
  notes: "...",
  agentId: "{agent}",           // 接收人
  priority: "high",              // low / normal / high / urgent
  labels: ["..."],
  status: "todo",                // 可选；不传默认 todo
  // 可选：绑定 session（与不绑互斥，二选一）
  // boardId: "default",
  // tenant: "...",
  // idempotencyKey: "..."        // 避免重复建卡
})
```

**shell 备选**：plugin CLI
```bash
openclaw workboard create "title" \
  --notes "..." \
  --agent {agent} \
  --priority high \
  --labels "label1,label2" \
  [--board default]
```

> ⚠️ **plugin CLI 不支持** `--session` / `--no-session` / `--no-dup` / `--assignee` / 自定义字段。**复杂建卡必须用 agent tool**。

**关键选项**（agent tool `workboard_create` 参数）：
- `title`（必填）：卡标题
- `notes`（可选）：详细描述
- `agentId`（必填，建议）：接收代理 ID（`writer` / `reviewer` / `psychologist` / ...）
- `status`（可选，默认 `todo`）：初始状态
- `priority`（可选，默认 `normal`）：low / normal / high / urgent
- `labels`（可选）：标签数组
- `tenant`（可选）：租户命名空间
- `boardId`（可选，默认 `default`）：看板命名空间
- `idempotencyKey`（可选）：幂等键（避免重复建卡）
- `parents`（可选）：父卡 ID 数组（依赖关系）
- `workspace`（可选）：workspace 配置
- `maxRetries` / `maxRuntimeSeconds` / `scheduledAt`（可选）：运行时参数
- `skills`（可选）：建议技能

**绑定 session 的正确方式**（v1.7.0）：
- **plugin CLI / agent tool 都不直接支持 `--session`**（plugin CLI 没有这个 flag，agent tool 也没有 `sessionKey` 参数）
- **改用 metadata.sessionKey**：建卡后用 `workboard_comment({ id, body: "sessionKey=agent:xxx:feishu:group:oc_xxx" })` 写软关联
- **或**用 `workboard_notify_subscribe({ cardId, sessionKey, target, eventKinds: ["completed","failed"] })` 建立通知通道

**互斥校验**（v1.7.0 已无 `--session` / `--no-session` 概念）：agent tool 的所有参数都通过单一对象传入，没有 CLI 风格的"互斥 flag"问题。

### 步骤 3:IM 群里艾特代理

**IM 模板**(workboard 信息**在开头**,原有派发模板内容保持不变):

```
🔧 workboard 信息:
- card_id: {{card_id}}(短 8 位:{{card_short}})
- session: {{sessionKey}}
- dashboard: {{card_url}}

{{task_desc}}

{{艾特代理}}

📋 前置要求:
- 明确自己的角色:{{agent_role}}
- 找到对应的 .agents/agents/{{agent}}.md 阅读
- 查看 TODO.md 中的 {{subtask}} 子任务

🎯 任务目标:{{任务目标}}
📌 任务约束:{{任务约束}}
📁 输入文件:{{input_file}}
📄 输出文件:{{output_file}}

💬 反馈:完成后在群里艾特大管家汇报
```

**模板要点**:
- workboard 信息**在开头**(不是末尾),让代理一进群就看到
- 原有派发模板内容**一字不动**
- **只一个模板**(不要拆派发/启动/完成多个模板)
- 后续状态变化由 workboard 自己管(Dx + dashboard),群里**不重复发**

### 步骤 4:等代理 claim + 启动 run

代理收到模板后:
1. 用 `workboard_claim` 插件工具认领
2. 群里回复 `已认领 card={{card_short}}`
3. 卡片 metadata.claim 写入(ownerId、token、claimedAt)
4. **claim 后立即 `workboard_heartbeat` 续约**--避免 claim token 过期被 Dx 误判 blocked
5. **代理自己启动 run**:`chat.send` 带 idempotencyKey 触发新 run(v1.5.0:大管家不介入)

**大管家动作**(v1.5.0):**什么都不用做**。看到代理群里回"已认领"后,等产出即可。不要再调 start(已删)。

### 步骤 5:代理执行

代理在 session 里干活,通过插件工具:
- `workboard_heartbeat` 续约(防 claim 过期)
- `workboard_comment` 留评论
- 执行完用 `workboard_proof` 附产出

执行完成后,代理**在群里发完成消息**(艾特大管家)。

**Dx 自动同步**:run 完成后,Dashboard Dx 把卡从 `running` 移到 `review`。

### 步骤 6:大管家核验 + 归档（v1.7.0 全部走 agent tool）

```js
// 1. 读卡看产出
workboard_read({ id: card_id })

// 2. 核验通过:workboard_complete 移到 done（带 summary + proof）
workboard_complete({
  id: card_id,
  summary: "大管家核验通过：...",
  proof: { status: "passed", label: "...", note: "..." },
  artifacts: [{ label: "...", path: "/path/to/output" }]
})

// 3. 核验失败（人工介入）：workboard_block 移到 blocked
workboard_block({ id: card_id, reason: "核验失败：..." })

// 4. 归档（可选）
workboard_board_archive({ id: card_id, archived: true })

// 5. 删卡（不可恢复）
workboard_delete({ id: card_id })

// 6. 批量：循环调 workboard_*（无 bulk 子命令）
for (const id of cardIds) {
  workboard_board_archive({ id, archived: true })
}
```

---

## 五、卡状态机

```
   create
     ↓
   backlog   ← Dx 不会从 backlog 同步出去
     ↓ (move to todo)
   todo       ← 已在群里艾特,等代理 claim
     ↓ (claim 写入)
   [claimed]  ← metadata 状态,不是卡片 status
     ↓ (代理手动 chat.send / scheduler 启 run,v1.5.0)
   running    ← runId 活跃
     ↓ (run 完成)
   review     ← Dx 自动从 running 挪过来
     ↓
     ├─→ done      (大管家核验通过)
     ├─→ blocked   (大管家核验失败/超时)
     └─→ running   (重跑)
```

> v1.5.0 变化:`running` 状态不再由 `start` 子命令推。代理认领后自己 `chat.send` 触发 run(OpenClaw runtime 自动同步 execution.status)。

**Dx 自动同步规则**(dashboard 控制台 `Dx()` 函数):
- 卡有 `sessionKey` + session 是 `done` → 卡 → `review`
- 卡有 `sessionKey` + session 是 `running` → 卡 → `running`
- 卡有 `sessionKey` + session 是 `failed` → 卡 → `blocked`
- 卡有 `sessionKey` + session 是 `idle` → 不动
- 卡无 `sessionKey` → 不动

**为什么 `--session` 配默认 `backlog`?**
- Dx 只从 `backlog → running` 同步,不会从 `backlog` 冲到 `review`
- 卡在 `backlog` 时**稳态**,不被 Dx 乱动
- 想进 `todo`?手动 `move --status todo`(大管家显式启动派发)

---

## 六、Dashboard 限制(重要!踩过坑)

⚠️ **不能点 Dashboard 上的"开始"按钮**。原因:

Dashboard 控制台的 `Ix()` 函数硬编码 `e.client.request("sessions.create", ...)`,**无视 card 上的 sessionKey**。每次点"开始"都会:
1. 强制调 `sessions.create` 建**新** session
2. 用新 session key 覆盖卡上的 `sessionKey`
3. 卡上原本指定 `{oc_id}` 被覆盖成 `agent:{agent}:dashboard:...`

**v1.5.0 后的正确路径**:**完全不点 dashboard 的开始按钮**。代理认领后自己 `chat.send` 启 run(不需任何 CLI 介入)。如果卡已被 dashboard 覆盖,把卡移到 `blocked` 状态,由代理手动重 claim。

---

## 七、设备身份认证(首次使用)

首次调用 `openclaw workboard`（plugin CLI）或 `workboard_*`（agent tool）时都会自动触发 **device pairing flow**（plugin 已配对，agent tool 走 plugin 上下文，CLI 走 Python 设备身份认证）。

1. Python 脚本自动生成 Ed25519 密钥对
2. 用私钥签名 connect 握手
3. gateway **自动批准** CLI 设备配对(无需手动操作)
4. scopes 自动获取 `operator.admin`

**配对过程全自动**。CLI 模式下 gateway 自动批准设备,无需在 Dashboard 手动操作。

---

## 八、常见错误与排查

| 错误 | 原因 | 解决 |
|------|------|------|
| `missing scope: operator.admin` | 设备未配对 / scopes 不足 | 批准设备配对 |
| `claim ownerId is required` | 调 claim 没传 ownerId | 必传 `ownerId` 参数 |
| `card already claimed by X` | 已被其他 agent 认领 | 等释放或换一张卡 |
| `claim token does not match` | 续约/释放的 token 错了 | 用 claim 返回的 token |
| `400 Invalid 'tools[N].function.name'` | DeepSeek 拒收带点号 tool 名 | 不要动插件!已加红线(v8.19.0) |
| `invalid chat.send params: must have required property 'idempotencyKey'` | chat.send 漏 idempotencyKey | 代理 chat.send 时手动加 idempotencyKey |
| `execution dropped by normalizeExecution` | execution 缺 model 字段 | v1.5.0 修复(create 默认 `minimax`,不指具体模型) |
| Dx 自动从 backlog 移到 review | --session 时没传 --status | v1.4.0 修复(默认 backlog) |
| 卡执行完 writer 不在群里 | 用 dashboard 点"开始"(强制 sessions.create) | v1.5.0 后不点 dashboard 开始;让代理手动 `chat.send` 启 run |

---

## 九、与其他工具的协作

### 三件套架构:TODO 纪律 + workboard 执行 + IM 可见

| 层级 | 工具 | 角色 | 谁看 |
|------|------|------|------|
| **纪律层** | `TODO.md` | 看板、状态记录 | 大管家 + 老板 |
| **数据/执行层** | `workboard` 卡片 | `create` 派发、状态机、运行轨迹 | 子代理 + Dashboard |
| **可见层** | **IM 群艾特** | 1 个通知模板(开头带 workboard 信息) | 群里所有人 |

**三者缺一不可**:TODO 没纪律会失控,workboard 没 IM 群里看不到,IM 没 workboard 没结构化数据。

### TODO.md 配合

```markdown
- [ ] **T-001**:{task_desc}  [card={{card_id_占位}}]
  - 🎯 目标:在 {oc_id} 群写 {output_name}
  - 📁 输入:{input_name}
  - 📄 产出:{output_name}
  - 👤 负责人:{agent}(claim 后自己启 run)
  - 📄 状态:⬜ 待认领
```

`[card={{card_id}}]` 是 workboard 引用,便于从 TODO 跳到 Dashboard 查完整状态。

### 完整同步规则

详见 [`sync-standards.md`](./sync-standards.md) v2.0(TODO ↔ task 工具 ↔ workboard 三方同步)。

### IM 派发配合

**只一个模板**(开头带 workboard 信息),不要重复发多个模板。状态变化由 workboard Dx 自动同步到 Dashboard,群里不重复通知。

---

## 十、版本历史

| 版本 | 日期 | 更新 |
|------|------|------|
| **1.6.0** | 2026-06-06 | **同步升级，对接 SKILL.md v5.12.0**：(1) 顶部加 v1.6.0 更新说明（6 项变更）；(2) §二、什么时候用 Workboard 加"两种派发场景"段；(3) §三、能力边界"关键分工"重写——大管家 = 建卡层（CLI），派发动作走 IM 群 / sessions_spawn；(4) **新章节"三之2、Workboard 永远只管建卡/管理"**——明确 3 动作铁律 + 两种派发场景下 workboard 角色 + 为什么 workboard 不接派发；(5) 同步 task-flow-guide.md v3.2.0 导航；(6) 源自私聊派发端到端测试 + SKILL.md v5.12.0 同步 |
| 1.5.0 | 2026-06-06 | **重大简化**：(1) 删除 `start` 子命令（cli.py + WorkboardClient.py）；(2) 5+1 步 → 4 步流程；(3) 卡状态机去掉 `start` 步骤；(4) `create` 默认 model 改成 `minimax`（不指具体模型）；(5) 反馈措辞按 session 场景动态化；(6) 删 3 条 start 相关错误排查 |
| 1.4.0 | 2026-06-03 | **重大升级**:(1) 加 `--session` flag + 默认 backlog(commit `f18df719`);(2) 修 `ejecución`→`execution` 拼写 + start 默认 model(commit `9e78459e`);(3) start 路径 A/B 真触发 run + idempotencyKey(commit `58094e59`);(4) 加 Dashboard 限制章节;(5) 加卡状态机章节;(6) 5+1 步新派发流程;(7) 三件套架构整合 |
| 1.3.0 | 2026-06-02 | 认知更正:workboard 主用户是 agent,不是大管家 |
| 1.2.0 | 2026-06-02 | 修复 UX bug:新增 `claim --auto-start` 选项(claim 后自动设置 execution.status=running) |
| 1.1.0 | 2026-06-02 | Python 迁移:脚本从 Node.js (wb-rpc.mjs) 迁移至 Python 包 |
| 1.0.0 | 2026-06-02 | 初始版本:明确 workboard 任务发布的标准流程 |

---

*最后更新:2026-06-03*
