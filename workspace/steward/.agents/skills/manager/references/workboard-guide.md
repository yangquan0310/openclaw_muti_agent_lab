# Workboard 任务发布指南 v1.5.0

> **v1.5.0 重大简化**(2026-06-06):
> 1. **删除 `start` 子命令**(代码 + 文档)--卡建好后大管家不再"启 session",代理自己 claim + 启动 run
> 2. 派发流程从 **5+1 步 → 4 步**(create → IM 艾特 → 代理 claim → 代理执行 + proof)
> 3. 卡状态机去掉"start 步骤"--"running"转换由代理手动 chat.send / 调度触发
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

- 多 Agent 协作任务(写作助手 → 数学家 → 审稿人 接力)
- 长任务(数小时到数天,需要 claim 防僵死)
- 需要可追溯证据的任务(v1→v7 版本演进、proof 沉淀)
- Bug 追踪(已知 bug 建卡跟踪)
- 每日定时任务的报告卡(T042 每日 OpenClaw 检查)

### ❌ 不必用

- 单 Agent 短期任务(一句话能说完的)
- 临时讨论、IM 问询
- 简单进度跟踪(MEMORY.md 够用)

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

### 大管家 CLI(仅派发层)

| CLI 子命令 | 用途 |
|-----------|------|
| `manager workboard create` | 建卡 |
| ~~`manager workboard start`~~ | ~~start(claim 之后才调)~~ v1.5.0 删除 |
| `manager workboard move` | 移动(看板拖拽的 CLI 等价) |
| `manager workboard list` | 列卡 |
| `manager workboard read` | 读卡 |
| `manager workboard bulk` | 批量(archive/delete/move) |
| `manager workboard delete` | 删卡 |

**关键分工**:
- **大管家** = 派发层(CLI)。负责:建卡、start(认领后)、核验后归档
- **代理** = 执行层(插件工具)。负责:claim、heartbeat、release、proof

> ❌ **不暴露给大管家 CLI 的工具**:claim / heartbeat / release / proof。代理**直接用插件工具**,不绕大管家。

---

## 四、发布任务的 4 步新流程(v1.5.0 简化)

### 心智模型(三件套架构)

```
老板交任务
    ↓
[1] 大管家 create card(--session, 默认 backlog)
    ↓
[2] 大管家 群里艾特代理(IM 模板,**开头**带 workboard 信息)
    ↓
[3] 代理 收到 → workboard_claim 认领 → 群里回"已认领 card=xxx"
    ↓ (代理自己 chat.send / 调度启 run,不走 workboard start)
[4] 代理执行完 → 群里发完成消息 + workboard_proof 附产出
    ↓
[5] 大管家核验产出 → 插件工具 move → done / blocked
```

> v1.5.0 重要变化:**大管家不再调 `manager workboard start`**。代理认领后自己启 run(`chat.send` 触发或 scheduler 调起)。workboard 卡只作"任务声明/看板",派发用 IM 群,启 run 由代理负责。

### 步骤 1:明确任务

回答三个问题:
- 任务目标(一句话)
- 指派对象(哪个 agent:`writer` / `reviewer` / `psychologist` / ...)
- 优先级 + 标签(`low/normal/high/urgent` + `labels`)

### 步骤 2:建卡(大管家 CLI)

```bash
manager workboard create \
  --assignee {agent} \
  --priority high \
  --session 'agent:{agent}:feishu:group:{oc_id}' \
  --task-desc "..." \
  --agent-role {agent} \
  --goal "..." \
  --constraints "..." \
  --feedback "..." \
  --no-dup                    # v3.0.1 新增:避免重复建卡
```

**关键选项**:
- `--session X`:指定关联 session(与 `--no-session` 互斥)
- `--no-dup`(v3.0.1 新增):建卡前查同 title + sessionKey 是否已有活跃卡(backlog/todo/running),有则返回已存在卡 ID 不创建
- **不传 `--status` 时**:有 `--session` → 默认 `backlog`;无 `--session` → 默认 `todo`
  - **为什么 backlog?** Dx 自动同步只从 `backlog → running` 同步,不会从 `backlog` 冲到 `review`
  - **禁止**手动 `move --status todo`(Dx 自动覆盖)
- `--engine {codex,claude}`:execution.engine
- `--model`:execution.model(不传默认 `minimax/MiniMax-M3`)

**互斥校验**:`--session` 和 `--no-session` 不能同时用。

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

### 步骤 6:大管家核验 + 归档

```bash
# 读卡看产出
manager workboard read --id <card_id>

# 核验通过:移到 done
manager workboard move --id <card_id> --status done

# 核验失败:移到 blocked(人工介入)
manager workboard move --id <card_id> --status blocked

# 归档(可选)
manager workboard archive --id <card_id>
# 或批量
manager workboard bulk --action archive --archive true --ids <id1>,<id2>
```

---

## 五、卡状态机

```
   create
     ↓
   backlog   ← Dx 不会从 backlog 同步出去
     ↓ (move to todo)
   todo       ← 已在群里艾特，等代理 claim
     ↓ (claim 写入)
   [claimed]  ← metadata 状态，不是卡片 status
     ↓ (代理手动 chat.send / scheduler 启 run，v1.5.0)
   running    ← runId 活跃
     ↓ (run 完成)
   review     ← Dx 自动从 running 挪过来
     ↓
     ├─→ done      (大管家核验通过)
     ├─→ blocked   (大管家核验失败/超时)
     └─→ running   (重跑)
```

> v1.5.0 变化：`running` 状态不再由 `start` 子命令推。代理认领后自己 `chat.send` 触发 run（OpenClaw runtime 自动同步 execution.status）。

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

## 六、Dashboard 限制（重要！踩过坑）

⚠️ **不能点 Dashboard 上的“开始”按钮**。原因：

Dashboard 控制台的 `Ix()` 函数硬编码 `e.client.request("sessions.create", ...)`，**无视 card 上的 sessionKey**。每次点“开始”都会：
1. 强制调 `sessions.create` 建**新** session
2. 用新 session key 覆盖卡上的 `sessionKey`
3. 卡上原本指定 `{oc_id}` 被覆盖成 `agent:{agent}:dashboard:...`

**v1.5.0 后的正确路径**：**完全不点 dashboard 的开始按钮**。代理认领后自己 `chat.send` 启 run（不需任何 CLI 介入）。如果卡已被 dashboard 覆盖，把卡移到 `blocked` 状态，由代理手动重 claim。

---

## 七、设备身份认证(首次使用)

首次调用 `manager workboard` 时会自动触发 **device pairing flow**:

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
| `execution dropped by normalizeExecution` | execution 缺 model 字段 | v1.5.0 修复（create 默认 `minimax`，不指具体模型） |
| Dx 自动从 backlog 移到 review | --session 时没传 --status | v1.4.0 修复（默认 backlog） |
| 卡执行完 writer 不在群里 | 用 dashboard 点“开始”（强制 sessions.create） | v1.5.0 后不点 dashboard 开始；让代理手动 `chat.send` 启 run |

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
  - 👤 负责人：{agent}（claim 后自己启 run）
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
| 1.5.0 | 2026-06-06 | **重大简化**：(1) 删除 `start` 子命令（cli.py + WorkboardClient.py）；(2) 5+1 步 → 4 步流程；(3) 卡状态机去掉 `start` 步骤；(4) `create` 默认 model 改成 `minimax`（不指具体模型）；(5) 反馈措辞按 session 场景动态化；(6) 删 3 条 start 相关错误排查 |
| 1.4.0 | 2026-06-03 | **重大升级**：(1) 加 `--session` flag + 默认 backlog（commit `f18df719`）；(2) 修 `ejecución`→`execution` 拼写 + start 默认 model（commit `9e78459e`）；(3) start 路径 A/B 真触发 run + idempotencyKey（commit `58094e59`）；(4) 加 Dashboard 限制章节；(5) 加卡状态机章节；(6) 5+1 步新派发流程；(7) 三件套架构整合 |
| 1.3.0 | 2026-06-02 | 认知更正:workboard 主用户是 agent,不是大管家 |
| 1.2.0 | 2026-06-02 | 修复 UX bug:新增 `claim --auto-start` 选项(claim 后自动设置 execution.status=running) |
| 1.1.0 | 2026-06-02 | Python 迁移:脚本从 Node.js (wb-rpc.mjs) 迁移至 Python 包 |
| 1.0.0 | 2026-06-02 | 初始版本:明确 workboard 任务发布的标准流程 |

---

*最后更新:2026-06-03*
