# Workboard 任务发布指南 v1.12.0

> v1.12.0：**派发模式同步 v3.8.0**（dispatch 取代私聊）+ **验收权下放**（worker 自己 complete）+ **v1.11.0 错判修正**（CLI 实际有 dispatch）。详见末尾 §十、版本历史。

---

## 一、Workboard 是什么(官方定义)

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
- **状态机**(`v1.12.0 v3.8.0 同步`)：群派发 `backlog → running → done`；dispatch 派发 `ready → running → done`（**v1.12.0 跳过 review 状态**——worker 主动 complete 推 done）

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
- **两种派发场景（v1.12.0 同步 v3.8.0）**：
  - **群派发**：IM 群里交任务，建卡绑群 session（`workboard_comment` 写 `sessionKey=agent:{agent}:feishu:group:oc_xxx`），Dx 自动同步
  - **dispatch 派发**（v3.8.0 取代私聊）：老板在 DM 或群里交任务（机器启动场景），建卡 `status=ready`，大管家 `openclaw workboard dispatch` CLI 启动 worker（指定 agentId，等价于私聊 spawn）
  - 详见 task-flow-guide.md v3.8.0（§二、群派发 / §三、dispatch 派发）

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

> ❌ **绝对禁止**重建 `manager workboard` CLI（v3.3.0 删除后永不重建）。如需 shell 操作，**只用 `openclaw workboard` plugin CLI**。
> ❌ **绝对禁止**再回退到 `scripts/workboard/` Python 包（v1.7.0 删除后，永不重建）。如需 shell 操作，**只用 `openclaw workboard` plugin CLI**。
>
> **v1.12.0 撤销 v1.6.0 / v1.7.0 错判**："绝对禁止给 workboard CLI 加 spawn / dispatch 子命令"——**错判**。`openclaw workboard dispatch` CLI **已存在并使用**（OpenClaw 2026.6.11），是大管家 dispatch 派发的合法入口（agent tool `workboard_dispatch` ≠ plugin CLI `openclaw workboard dispatch`，前者只清理，后者是完整函数 `dispatchAndStartWorkboardCards`）。

---

## 三之3、大管家使用技巧（v1.8.0 新增）

> 源自 2026-06-06 v8.26.0 联动测试 + 老板指正："claim 是 session/IM 通知其他代理，大管家不需要管中间态"。

### 3.3.1 大管家不做什么（4 条铁律）

| ❌ 大管家**不**做的 | 由谁做 | 机制 |
|------|------|------|
| **不主动 `workboard_claim`** | **代理自己** / **dispatch 自动** | dispatch 派发：dispatch 自动 claim；群派发：群里代理 workboard_claim |
| **不主动 `workboard_proof`** | **执行代理 / worker** | worker 执行完自己调 workboard_proof 附证据 |
| **不主动 `workboard_complete`**（**v1.12.0 新增**） | **worker 自己** | worker 跑完自己调 workboard_complete → status=done（验收权下放）|
| 不盯 ready/todo→running 迁移 | **Dx 自动同步 / dispatch 自动** | 群派发：Dx 推；dispatch 派发：dispatch 推 |
| 不读中间过程 | **无** | 中间态（running/claimed）大管家**不读**——除非有异常 |

**关键洞察**：
- **`claim` 是触发器**，不是大管家的动作
- 群场景：claim 由群 IM 艾特 → 代理自己 workboard_claim
- 私聊场景：claim 由 sessions_spawn 触发子代理 → Dx 看到 agentId 匹配**自动 claim**
- **大管家发完派发通知就完事**——不主动调 claim

### 3.3.2 大管家"看 status" 的简化判断（v1.12.0 修订）

✅ **看 done** → 核验产出 + 汇报老板（**v1.12.0 撤销** `workboard_complete`——worker 已 complete）
✅ **看 blocked** → 人工介入（`workboard_reassign` / `workboard_unblock` / 重新派发 / 接受失败）
❌ **不看 running**（中间态，不管）
❌ **不看 todo / ready**（已派发，等代理 / dispatch claim）

**心智口诀**：**只看头尾，不盯中间**。**v1.12.0 加**：**只追踪不接管**——worker 自己 complete。

### 3.3.3 `workboard_create` `agentId` 副作用及应对（v1.9.0 3 轮测试更新）

`workboard_create({ agentId: "writer" })` 会触发**副作用**（v8.26.0 C 测试 + v1.9.0 3 轮测试发现）：

1. **Dx 看到 agentId → spawn 阶段**可能**自动 claim 到该 agent**（kind: "claimed" 事件自动写入）——**但不稳定**（3 轮测试有时序窗口）
2. **claim 后 workboard_comment / workboard_block 等"卡操作"只允许 owner**（报 "card is claimed by writer"）
3. **大管家自己 comment** 到已 claim 的卡 → 报错（除非 workboard_reassign 接管）

**subagent claim 行为时序窗口**（v1.9.0 3 轮测试实测）：

| subagent 跑得快（22s）| subagent 跑得慢（39s+） |
|------------------------|------------------------|
| Dx 还没 auto-claim | Dx 先 claim |
| subagent claim **成功** | subagent claim **失败**（"already claimed"）|
| 拿 token + 完整自管 | 大管家接管 fallback |

**应对策略**：

| 场景 | 应对 |
|------|------|
| 群派发 | workboard_create 后让群里代理**自己 claim + comment**——大管家不介入 |
| 私聊派发（subagent claim 成功）| sessions_spawn 含**完整自管 task**——subagent 跑得快时 claim + comment + proof + complete 一气呵成 |
| 私聊派发（subagent claim 失败）| 大管家接管：reassign + claim + complete（详见 §三之4 fallback） |
| 大管家想 comment | 选项 A：`workboard_reassign({ id, agentId: "steward" })` 接管 → claim → comment<br>选项 B：建新卡（不与已 claim 的卡冲突）|

### 3.3.4 workboard 状态机 vs 大管家介入点（v1.12.0 同步 v3.8.0）

```
   create                          ← 大管家 [1] 建卡
     ↓
   ready    ← dispatch 派发场景（v1.12.0 新增）
   backlog  ← 群派发场景（Dx 同步）
     ↓ (dispatch / 代理 claim)
   running                         ← 代理/dispatch 执行，**大管家不盯**
     ↓ (worker 主动调 workboard_complete)
   done                            ← **v1.12.0 跳过 review 状态**（worker 主动推）
     ↓
   archived                        ← 大管家可选

   ready / backlog / running
     ↓ (卡失败 / 超时)
   blocked                         ← 大管家人工介入

   done ↔ blocked                  ← 大管家可 reassign / unblock 反复折腾
```

**大管家介入点（v1.12.0 简化）**：**起点 (create) + 终点 (status=done 汇报老板) + 中间异常 (blocked 反复)**——**不**盯 running 中间过程，**不**调 workboard_complete（worker 自己）。

### 3.3.5 大管家 workboard_claim 强行覆盖行为总结（v1.9.0 3 轮测试）

| 情况 | workboard_claim 强行覆盖结果 | 原因 |
|------|----------------------------|------|
| 卡 status=ready/todo（没人 claim）| ✅ 成功 | 没 active claim，steward 直接认领 |
| Dx auto-claim 占先（Dx claim 是"软"）| ✅ 成功 | Dx claim 不持久，steward 可覆盖（v3.4.0 写诗测试时实测）|
| subagent / dispatch claim 占先（subagent claim 是"硬"）| ❌ 失败 "card already claimed by writer" | subagent 拿 token 持续 5 分钟（ttl），覆盖失败（轮 1 实测）|

**结论（v1.12.0 同步 v3.8.0）**：
- **Dx claim 是"软"** —— 大管家可覆盖（**v1.12.0 不推荐**——验收权下放后大管家不主动 claim）
- **subagent / dispatch claim 是"硬"** —— 大管家覆盖失败 → 需 sessions_send 续接让 subagent 调 workboard_complete
- **v1.12.0 简化**：大管家**不主动 claim**——让代理 / dispatch 调

---

---

## 三之4、dispatch 派发场景（v1.12.0 新增，**取代 v3.5.0 私聊派发**）

> **v1.12.0 撤销 §三之4、v3.5.0 私聊派发新范式（v1.9.0）**——dispatch 派发**取代**私聊 `sessions_spawn` 派发。详见 task-flow-guide.md v3.8.0 §三、dispatch 派发场景。

### 3.4.1 dispatch CLI 实测（v1.12.0 闭环验证）

测试卡 `d7709861-1412-4e2d-9976-812419aa1e27`（v1.12.0 行为验证）：

```bash
$ openclaw workboard dispatch --board default --expect-final --timeout 300000
dispatch complete: started=1 failures=0
```

**核心行为**：
- dispatch 选 ready 卡（agentId 匹配）
- **自动 claim** 卡（ownerId = card.agentId）
- **自动启动** subagent worker（engine=codex, mode=autonomous）
- 写入 card metadata：sessionKey + runId + execution
- 卡片事件链：created → ready → dispatch → claimed → moved(ready→running) → linked → orchestration → heartbeat → moved(running→done)
- worker 跑完**自己**调 `workboard_complete` → status=done（**v1.12.0 跳过 review 状态**）

### 3.4.2 agent tool vs plugin CLI 区别（**v1.12.0 关键发现**）

| 入口 | 调什么 | 行为 |
|------|--------|------|
| `workboard_dispatch` **agent tool**（line 775-781） | `store.dispatch()` | **只清理**（promote/reclaim/block/orchestrate），**不**启动 worker |
| `openclaw workboard dispatch` **plugin CLI** | `dispatchAndStartWorkboardCards`（line 86-94） | 完整：清理 + claim + 启动 subagent |
| `/workboard dispatch` **runtime-slash** | `dispatchAndStartWorkboardCards` | 同 plugin CLI，完整函数 |

**大管家派发必须用 plugin CLI 或 runtime-slash**——agent tool 不派发。

### 3.4.3 dispatch 派发 3 步流程（v1.12.0 同步 v3.8.0）

#### 步骤 1：建 workboard 卡

```js
workboard_create({
  title: "...",
  notes: "任务目标：...\n任务约束：...\n输入路径：...（绝对路径）\n输出路径：...",
  agentId: "{agent}",            // 必填
  priority: "normal",
  labels: ["..."],
  status: "ready"                // dispatch 派发场景默认 ready
})
```

#### 步骤 2：dispatch CLI 启动 worker

```bash
openclaw workboard dispatch \
  --board default \
  --expect-final \
  --timeout 300000
```

#### 步骤 3：worker 自动 complete + 大管家追踪

```
worker 跑完自动：
1. workboard_heartbeat（如需要）
2. 执行任务（按 notes 任务四要素）
3. workboard_proof 附产出
4. workboard_comment 留进度
5. workboard_complete → status=done

大管家（v1.12.0 验收权下放，**只追踪不接管**）：
1. workboard_read({ id: cardId }) 看到 status=done
2. 读 proof + 产出核验
3. 汇报老板"卡已 done"
4. ❌ 不调 workboard_complete
```

---

## 三之5、消息/note 模板库（v1.10.0 新增，v1.12.0 同步 v3.8.0）

> 源自 v8.26.0 + v3.4.0 + v3.5.0 多轮实测，**模板测试**验证可跑通。task-flow-guide.md v3.6.0 §六 与本节同表。

### 3.5.1 workboard_create 模板（**任务四要素**）

```js
{
  title: "[<前缀>] <任务描述>",
  notes: `任务目标：...
任务约束：...
输入路径：...
输出路径：...`,
  agentId: "<writer/reviewer/psychologist/...>",
  priority: "low/normal/high/urgent",
  labels: ["test", "v3.5.0", "..."],
  status: "todo"（私聊）/ "backlog"（群派发）
}
```

**任务四要素**（v1.11.0 老板拍板）：

| 要素 | 含义 | 示例 |
|------|------|------|
| **任务目标** | 干什么 | 写一首中文诗（主题/格律自选）|
| **任务约束** | 限制 / 边界 | 不调任何 workboard 工具 / 不少于 4 句 / 严守格律 |
| **输入路径** | 读什么文件 / 资源 | `~/.openclaw/workspace/steward/IDENTITY.md`（v3.5.0 重测示例）|
| **输出路径** | 产出落到哪 | 主 DM 回复（v3.5.0 私聊派发） / `/tmp/...md`（文件产出）|

> **任务四要素是建卡 note 的核心内容**——老板 2026-06-06 拍板。

**实测示例**（v3.5.0 完整流程 写词）：
```
notes: 任务目标：写一首词（蝶恋花/水调歌头/念奴娇/满江红自选，主题自选）
任务约束：不少于词牌规定句数；严守格律（平仄押韵）；不调 workboard_reassign / message tool
输入路径：（无——纯创作）
输出路径：主 DM 回复词作全文 + 简短说明
```

### 3.5.2 sessions_spawn task 模板（**通知模板 4 要素**）

```
任务标题：<title>
CARD_ID：<cardId>（看 prompt 实际替换值）
操作步骤：
  1. workboard_claim({ id: CARD_ID, ttlSeconds: 300 }) —— 拿 token
  2. <实际任务>
  3. workboard_comment({ id, body: "✅ v3.5.0 完整自管测试认领 + <产出>" })（带 token）
  4. workboard_proof({ id, status: "passed", label: "...", note: "..." })（带 token）
  5. workboard_complete({ id, token: <claim token>, summary: "...", proof: { status: "passed" } })（带 token）
反馈要求：
  - 完成后在主 DM 回复：<产出> + 简短说明
  - **反馈要求**（老板拍板）：...
```

**通知模板 4 要素**（v1.11.0 老板拍板）：

| 要素 | 含义 | 示例 |
|------|------|------|
| **任务标题** | 告诉代理做什么 | 写一首词（蝶恋花/水调歌头自选）|
| **CARD_ID** | 告知 workboard 卡 ID（让代理自管）| `34b4d37f-704b-4a8e-bdeb-d2db19b73a73` |
| **操作步骤** | 按 v3.5.0 范式自管 workboard | claim → comment → proof → complete |
| **反馈要求** | 完成后怎么反馈 | 主 DM 回复 + 简短说明 / 调 specific 工具 |

> **通知模板是派发通知的核心内容**——老板 2026-06-06 拍板。**4 要素**结构清晰，让代理知道**做什么 / 在哪做 / 怎么做 / 怎么反馈**。

**实测示例**（v3.5.0 完整流程 写词）：
```
任务标题：写一首词（蝶恋花/水调歌头/念奴娇/满江红 自选，主题自选）
CARD_ID：34b4d37f-704b-4a8e-bdeb-d2db19b73a73
操作步骤：
  1. workboard_claim({ id: CARD_ID, ttlSeconds: 300 }) —— 拿 token
  2. 写词（按所选词牌格律）
  3. workboard_comment({ id, body: "✅ v3.5.0 完整流程测试认领 + 词作\n\n【词牌名】\n（词作全文）" })（带 token）
  4. workboard_proof({ id, status: "passed", label: "v3.5.0-complete-flow", note: "..." })（带 token）
  5. workboard_complete({ id, token: <claim token>, summary: "...", proof: { status: "passed" } })（带 token）
反馈要求：完成后在主 DM 回复词作全文 + 简短说明（词牌/主题/格律/灵感）
```

### 3.5.3 workboard_comment 软关联模板（v3.5.0 大管家用）

```
🔗 软关联 sessionKey（<场景>）：
- childSessionKey=<childSessionKey>
- runId=<runId>
- taskName=<taskName>
- 实际 CARD_ID: <cardId>
- <场景>：<任务> + <期望>
```

### 3.5.4 v3.5.0 流式 reply 模板（**不调 yield**）

```
v3.5.0 派发完成（**不 yield**）：

🔧 workboard 卡：
- card_id: <cardId>
- childSessionKey: <childSessionKey>
- runId: <runId>
- taskName: <taskName>

🧪 **v3.5.0 范式 6 步**：
1. ✅ workboard_create
2. ✅ sessions_spawn（task 含**完整自管**）
3. ✅/⚠️ workboard_comment 软关联（成功/失败）
4. 🔜 流式 reply（**不调 yield**）
5. 🔜 turn 自然结束
6. 🔜 runtime auto-push event → 大管家下一轮

子代理任务：<任务>
大管家**只**核验不接管——按 v3.5.0 文档。
```

### 3.5.5 workboard_proof 模板

```js
proof: {
  status: "passed/failed",
  label: "<test-name>",
  command: "<action>",
  note: "<explanation>"
}
```

### 3.5.6 workboard_complete summary 模板

```
"<大管家/代理>验收<通过/失败>：<任务>已<完成/失败>。v3.5.0 派发范式<总结>。"
```

### 3.5.7 大管家核验 reply 模板（v3.5.0 不接管）

```
v3.5.0 验收<通过/失败>：
- 卡 status=<done/blocked>
- 事件流：...
- 关键产出：...
- 关键认知：...
```

### 3.5.8 大管家接管路径模板（v3.5.0 fallback A）

```js
// subagent claim 失败时（Dx 先占 + subagent 跑得慢）
workboard_reassign({ id, agentId: "steward", resetFailures: false, reason: "..." })
workboard_claim({ id, ttlSeconds: 300 })  // 拿新 token
workboard_complete({ id, token, summary, proof })  // 标 done
```

### 3.5.9 sessions_send 续接模板（v3.4.0 §五.4 fallback C）

```
续接指令（<轮 N> 收尾）：
你刚才 workboard_claim 拿到了 token（<token>）。**大管家自己 claim 被拒**（"card already claimed by writer"），所以请你**用你自己的 token** 调 workboard_complete 归档此卡。

调用参数（务必带 token）：
workboard_complete({
  id: "<cardId>",
  token: "<token>",
  summary: "...",
  proof: { status: "passed", label: "..." }
})

完成后只回 "pong <label> done"，然后结束本轮。
```

### 3.5.10 v3.5.0 私聊派发范式 3 句话总结（子代理模板测试写的）

> 3 句话**就是范式核心**——所有其他模板都围绕这 3 句话

1. **大管家核心原则**：大管家 = 建卡（定任务）+ 派发（通知代理）+ 验收；中间执行全由 subagent 自治完成，大管家不介入细节。
2. **v3.5.0 派发关键改进**：派发后**不调 sessions_yield**——reply 即本回合最终流式回复——turn 自然结束——runtime auto-push event 触发大管家下一轮——**流式输出全程保留**。
3. **大管家只核验不接管**：subagent 完整自管 workboard 卡（claim + comment + proof + complete）——大管家仅 workboard_read 核验——除 fallback 路径外**不**调 reassign / claim / complete。

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
| **v1.12.0** | 2026-07-02 | **重大重构**（老板拍板 + dispatch 闭环验证）：(1) **派发模式同步 v3.8.0**——2 种（群派发 / dispatch 派发）——**dispatch 取代私聊 sessions_spawn**；(2) **新增 §三之4、dispatch 派发场景**——3 步流程 + agent tool vs CLI 区别；(3) **删除 §三之4、v3.5.0 私聊派发新范式**（v1.9.0 整段删除）；(4) **§3.3.1 大管家 4 铁律改写**——加 2 条 v1.12.0（不主动 claim / 不调 complete）；(5) **§3.3.2 看 status 简化判断改写**——撤销 `workboard_complete`；(6) **§3.3.4 状态机图改写**——加 ready 状态（dispatch 派发）/ 跳过 review；(7) **v1.11.0 / v1.6.0 / v1.7.0 错判修正**——撤销"绝对禁止给 workboard CLI 加 dispatch 子命令"——`openclaw workboard dispatch` CLI 实际已存在并使用；(8) **派发闭环验证**——测试卡 d7709861 status=done 跑通 |
| **v1.11.0** | 2026-06-06 | **重大补充**（老板拍板）：(1) **3.5.1 任务四要素**——建卡 note 核心内容（**任务目标 / 任务约束 / 输入路径 / 输出路径**）；(2) **3.5.2 通知模板**——派发核心内容（**任务标题 / CARD_ID / 操作步骤 / 反馈要求**）；(3) 其他模板保持（comment 软关联 / 流式 reply / proof / complete summary / 核验 reply / fallback A 接管 / fallback C 续接 / 3 句话总结）。详见 §三之5、消息/note 模板库。**v1.12.0 撤销部分** |
| **v1.10.0** | 2026-06-06 | **重大补充**（老板拍板 + 模板测试验证）：(1) **新加"三之5、消息/note 模板库"**——10 个模板（workboard_create / spawn task / comment 软关联 / v3.5.0 流式 reply / proof / complete summary / 核验 reply / fallback A 接管 / fallback C 续接 / 派发范式 3 句话总结）；(2) 模板来源：5 轮测试验证（轮 1-3 / 重测 / 完整流程 / 模板测试）；(3) 指向：task-flow-guide.md v3.6.0 "§六、消息/note 模板库" 与本节同表 |
| **v1.9.0** | 2026-06-06 | **重大补充**（3 轮多轮测试验证，老板拍板）：(1) **新加"三之4、v3.5.0 私聊派发新范式"**——基于 3 轮测试（subagent claim 行为 / 不 yield auto-trigger / 大管家接管 fallback）；(2) **§3.3.3 加 subagent claim 时序说明**——Dx auto-claim 不稳定，subagent 跑得快时 claim 成功（实测）；(3) **大管家 workboard_claim 强行覆盖行为总结**——Dx claim 是"软"（可覆盖）/ subagent claim 是"硬"（覆盖失败）；(4) **v1.9.0 撤销 v3.4.0 §5.4 §5.5 错误**：v3.4.0 写"❌ workboard_claim / ❌ workboard_complete"是错的——实测 subagent 可完整自管 |
| **v1.8.0** | 2026-06-06 | **重大补充**（老板指正 + 联动测试验证）：(1) **新加"三之3、大管家使用技巧"**——明确"大管家不做什么"、"看 status 简化判断"、"agentId 副作用及应对"；(2) 4 场联动测试验证（v8.26.0 实测）：A done 路径 / B blocked 路径 / C subagent 自管 workboard / D notify_subscribe 链路 |
| **v1.7.0** | 2026-06-06 | **重大修复**（老板纠错，老板拍板）：(1) **删除 `manager workboard` CLI**（v2026.6.6）—— `scripts/workboard/` 整个目录（932 行 Python）已删除；(2) **建卡改用 agent tool**（`workboard_create`）或 **plugin 自带 CLI**（`openclaw workboard create`）；(3) **核验/验收改用 agent tool**（`workboard_read` / `workboard_comment` / `workboard_complete` / `workboard_delete` 等）；(4) **大管家 3 动作铁律保持**（建卡 + im/spawn 派发 + 验收），但"建卡"和"验收"全部走 agent tool，**不再走 manager CLI**；(5) **踩坑教训**：v8.25.0 拍板时漏看了 `workboard_create` agent tool 一直就在 plugin contract tools 里（`extensions/workboard/openclaw.plugin.json:18`），错让老板创建 932 行 Python 脚本——**完全没必要的**。**v1.7.0 撤销 v8.25.0 沉淀，建卡用 tool/plugin CLI** |
| **v1.6.0** | 2026-06-06 | **同步升级，对接 SKILL.md v5.12.0**：(1) 顶部加 v1.6.0 更新说明（6 项变更）；(2) §二、什么时候用 Workboard 加"两种派发场景"段；(3) §三、能力边界"关键分工"重写——大管家 = 建卡层（CLI），派发动作走 IM 群 / sessions_spawn；(4) **新章节"三之2、Workboard 永远只管建卡/管理"**——明确 3 动作铁律 + 两种派发场景下 workboard 角色 + 为什么 workboard 不接派发；(5) 同步 task-flow-guide.md v3.2.0 导航；(6) 源自私聊派发端到端测试 + SKILL.md v5.12.0 同步 |
| 1.5.0 | 2026-06-06 | **重大简化**：(1) 删除 `start` 子命令（cli.py + WorkboardClient.py）；(2) 5+1 步 → 4 步流程；(3) 卡状态机去掉 `start` 步骤；(4) `create` 默认 model 改成 `minimax`（不指具体模型）；(5) 反馈措辞按 session 场景动态化；(6) 删 3 条 start 相关错误排查 |
| 1.4.0 | 2026-06-03 | **重大升级**:(1) 加 `--session` flag + 默认 backlog(commit `f18df719`);(2) 修 `ejecución`→`execution` 拼写 + start 默认 model(commit `9e78459e`);(3) start 路径 A/B 真触发 run + idempotencyKey(commit `58094e59`);(4) 加 Dashboard 限制章节;(5) 加卡状态机章节;(6) 5+1 步新派发流程;(7) 三件套架构整合 |
| 1.3.0 | 2026-06-02 | 认知更正:workboard 主用户是 agent,不是大管家 |
| 1.2.0 | 2026-06-02 | 修复 UX bug:新增 `claim --auto-start` 选项(claim 后自动设置 execution.status=running) |
| 1.1.0 | 2026-06-02 | Python 迁移:脚本从 Node.js (wb-rpc.mjs) 迁移至 Python 包 |
| 1.0.0 | 2026-06-02 | 初始版本:明确 workboard 任务发布的标准流程 |

---

*最后更新：2026-07-02 06:05*
*v1.12.0 整理者：大管家（steward）*
*v1.12.0 派发闭环验证：测试卡 d7709861-1412-4e2d-9976-812419aa1e27（status=done）*
