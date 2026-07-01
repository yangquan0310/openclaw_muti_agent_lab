# 任务流指南 v3.8.0

> v3.8.0：派发模式 = 群派发（IM）/ dispatch 派发（CLI）。验收权下放给 worker。详见末尾 §八、版本历史。

---

## 一、心智模型（读前必看）

### 1.1 三件套架构（v3.8.0 重构）

| 层级 | 工具 | 角色 | 谁用 |
|------|------|------|------|
| **纪律层** | `TODO.md` | 看板、状态记录（**仅群场景**） | 大管家 |
| **执行层** | `workboard` 卡片 | 任务声明、状态机、进度反馈 | 大管家 agent tool（建卡/追踪）+ 代理 agent tool（claim/complete）|
| **通知层** | **IM 群艾特**（群场景）/ **`openclaw workboard dispatch`**（群+私聊，指定 agentId 等价私聊） | 派发通道 | 大管家手动 |

**关键洞察**：
- **三件套缺一不可**：TODO（纪律）+ workboard（执行）+ IM/dispatch（通知/触发）
- **workboard 只管"建卡/管理/追踪"**——派发通道由大管家手动
- **dashboard 是任务进度主可见层**——老板通过 dashboard 看进度

### 1.2 大管家 2 动作铁律（v3.8.0 重大简化）

```
[1] 建卡     →  workboard_create（agent tool，必设 agentId + status）
[2] 触发     →  IM 群艾特（群场景）/ openclaw workboard dispatch（群+私聊，指定 agentId 等价私聊）
```

**大管家不做什么（v3.8.0 验收权下放）**：
- ❌ **不调** `workboard_claim`（让代理 / dispatch 调）
- ❌ **不调** `workboard_complete`（让 worker 自己 complete）
- ✅ **只**用 `workboard_read` 追踪 status
- ✅ status=done 时**汇报老板**

**绝对禁止**重建 `manager workboard` CLI（v3.3.0 删除后永不重建）。派发动作永远在大管家会话里手动做（IM 艾特 / dispatch CLI）。

### 1.3 workboard 状态机（v3.8.0 重大修改）

```
   create (大管家)
     ↓
   ready    ← dispatch 派发场景（v3.8.0 默认）
   backlog  ← 群派发场景（Dx 自动同步 sessionKey）
     ↓ (dispatch / 代理 claim)
   running  ← 代理执行
     ↓ (worker 主动调 workboard_complete)
   done     ← **v3.8.0 跳过 review 状态**（worker 主动推）
```

- worker 主动 complete 推 done（**跳过 review 状态**）
- dispatch 派发场景默认 status=ready；群派发场景默认 status=backlog

### 1.4 两种派发场景概览（v3.8.0 重构）

| 场景 | 触发 | 派发通道 | workboard 角色 | 流程序号 |
|------|------|----------|----------------|----------|
| **群派发** | 老板在群里交任务 | IM 5 段模板艾特 | 建卡 + 看板 + Dx 同步 | [§二、群派发场景](#二群派发场景v301-主线) |
| **dispatch 派发**（v3.8.0 新增，取代私聊） | 老板在 DM 或群里交任务（机器启动场景）| `openclaw workboard dispatch` CLI（指定 agentId） | 建卡 + dispatch 自动 claim + 启动 worker | [§三、dispatch 派发场景](#三dispatch-派发场景v380-新增) |

- 派发模式 = 2 种：群派发（IM）/ dispatch 派发（CLI）
- dispatch 通过 `card.agentId` 等价私聊 spawn 启动子代理

---

## 二、群派发场景（v3.0.1 主线）

### 2.1 适用场景

老板**在群聊里**交任务给大管家。群里有现成的"艾特代理"通道，代理**必须**通过群里 @ 才知道有新任务。

### 2.2 群派发 4 步流程

#### 步骤 1：写 TODO.md

```markdown
- [ ] **T-001.1** 子任务描述  [card={{card_id_占位}}]
  - 👤 负责人：{agent}
  - 🎯 目标：...
  - 📌 约束：...
  - 📁 输入：{绝对路径}
  - 📄 产出：{绝对路径}
  - 📊 状态：⬜ 待认领
```

**TODO 7 字段规范**（仅群场景用，dispatch 派发场景不写）见 [§四、通用规则 §4.1](#41-todo-7-字段规范仅群场景用)。

#### 步骤 2：建 workboard 卡（绑群 session）

```js
// agent tool（主用，完整功能）
workboard_create({
  title: "...",
  notes: "目标：... 约束：... 任务描述：...",
  agentId: "{agent}",            // 接收人
  priority: "high",              // high / normal / urgent
  labels: ["..."],
  status: "backlog",             // 群场景默认 backlog（Dx 自动同步）
  // 不绑 session 直接传（agent tool 无 --session 概念）
  // 改用 workboard_comment 写软关联：sessionKey=agent:{agent}:feishu:group:{oc_id}
  idempotencyKey: "{title}|{oc_id}"  // v3.0.1 防重复建卡
})

// 建卡后立即建软关联
workboard_comment({
  id: cardId,
  body: "sessionKey=agent:{agent}:feishu:group:{oc_id}\nfeedback: 完成后在群聊中艾特大管家汇报"
})
```

**shell 备选**（plugin CLI 不支持 session 绑定，仅最简建卡）：
```bash
openclaw workboard create "title" --agent {agent} --priority high --labels "..."
# ⚠️ plugin CLI 无 --session / --no-dup / 自定义字段，复杂建卡必须用 agent tool
```

#### 步骤 3：IM 5 段模板艾特（**必须**）

**完整 IM 模板**（5 段齐全）：

```
{{task_desc}}

{{@代理}}

🔧 workboard 信息：
- card_id: {{card_id}}（短 8 位：{{card_short}}）
- session: {{sessionKey}}
- dashboard: {{card_url}}

📋 前置要求：
- 明确自己的角色：{{agent_role}}
- 找到对应的 .agents/agents/{{agent}}.md 阅读
- 查看 TODO.md 中的 {{subtask}} 子任务

☁ 完成反馈：
- 在群里艾特大管家
- 汇报结果
```

#### 步骤 4：代理自动执行 + 大管家追踪（v3.8.0 简化）

```
代理收到 @ 后自动：
1. 看到 dashboard 有 backlog 卡 → workboard_claim（自动）
2. Dx 看到 claim → 卡 backlog → running（自动）
3. 代理执行任务
4. 代理 workboard_proof 附产出
5. 代理 workboard_comment 留进度反馈
6. 代理 workboard_complete → 卡 running → done（**v3.8.0 跳过 review**）
7. 代理在群里发"完成 + 艾特大管家"消息

大管家（v3.8.0 验收权下放，**只追踪不接管**）：
1. 群里收到代理完成消息
2. workboard_read({ id: cardId }) 看 status=done
3. 读 proof + 产出文件核验
4. 更新 TODO.md 为 [x] + 核验结果
5. 汇报老板"卡已 done"
6. ❌ **不调** workboard_complete（worker 已 complete）
```

**大管家不需要**（Dx 全包）：
- ❌ 手动 `move --status todo`（Dx 自动）
- ❌ 手动 `move --status done`（v3.8.0 撤销——worker 自己 complete）
- ❌ 手动 `workboard_claim`（代理自己 claim）
- ❌ 手动 `workboard_complete`（worker 自己 complete）

---

## 三、dispatch 派发场景（v3.8.0 新增，**取代私聊**）

### 3.1 适用场景

老板在 **DM 或群里**交任务给大管家，需要**机器自动启动** subagent 跑任务（不需要群里人艾特 + 看）。

dispatch 派发**取代** v3.7.0 私聊派发（`sessions_spawn`）——通过指定 `agentId`，等价于私聊 spawn 启动子代理。

### 3.2 dispatch 派发 3 步流程（v3.8.0 简化）

#### 步骤 1：建 workboard 卡（**必设** agentId，status=ready）

```js
// agent tool（主用）
workboard_create({
  title: "...",
  notes: "任务目标：...\n任务约束：...\n输入路径：...（绝对路径）\n输出路径：...",
  agentId: "{agent}",            // **必填**（dispatch 启动 worker = 这个 agent）
  priority: "normal",
  labels: ["..."],
  status: "ready"                // **v3.8.0 dispatch 派发场景默认 ready**
  // 不传 idempotencyKey（dispatch 派发任务由 dashboard 监管）
  // 不传 sessionKey（dispatch 自动 link）
})
```

**关键约束（v3.8.0）**：
- **agentId 必填**（不知道派给谁就别建卡）
- **status=ready**（dispatch 选 ready 卡自动 claim）
- **不写 TODO.md**（dispatch 派发是单人任务）
- **任务四要素**写进 notes（任务目标 / 任务约束 / 输入路径 / 输出路径）

#### 步骤 2：`openclaw workboard dispatch` 启动 worker

```bash
openclaw workboard dispatch \
  --board default \
  --expect-final \
  --timeout 300000
```

**核心行为**（v3.8.0 实测）：
- dispatch 选 ready 卡（agentId 匹配）
- **自动 claim** 卡（ownerId = card.agentId）
- **自动启动** subagent worker（engine=codex, mode=autonomous）
- 写入 card metadata：sessionKey + runId + execution
- **输出**：`dispatch complete: started=N failures=0`

**关键参数**：
- `--board <id>` 限定 board（默认 default）
- `--expect-final` 等待最终响应（实验性，可能不等——**实测**仍 fire-and-forget）
- `--timeout <ms>` 默认 30s，dispatch 派发建议 300000（5 分钟）

**等价私聊 spawn 的关键**：通过 `card.agentId` 指定目标代理，dispatch 内部用 `params.subagent.run({ sessionKey, ... })` 启动 subagent session——**效果等价**于 `sessions_spawn({ agentId, task, isolate: true })`。

#### 步骤 3：worker 自动 complete + 大管家追踪

```
worker 跑完自动：
1. workboard_heartbeat（如需要）
2. 执行任务（按 notes 任务四要素）
3. workboard_proof 附产出（status=passed）
4. workboard_comment 留进度
5. workboard_complete → 卡 running → done（**v3.8.0 worker 主动 complete**）

大管家（v3.8.0 验收权下放，**只追踪不接管**）：
1. workboard_read({ id: cardId }) 看到 status=done
2. 读 proof + 产出文件核验
3. 汇报老板"卡已 done，验证通过"
4. ❌ **不调** workboard_complete（worker 已 complete）
```

### 3.3 dispatch 派发 vs 群派发对比

| 维度 | 群派发 | dispatch 派发 |
|------|--------|--------------|
| 触发 | 老板在群里交任务 | 老板在 DM 或群里交任务（机器启动） |
| 派发动作 | IM 5 段模板艾特 | `openclaw workboard dispatch` CLI |
| 卡 status 默认 | backlog | ready |
| 卡 sessionKey | 群 session（workboard_comment 写软关联）| 不传（dispatch 自动 link） |
| 代理收任务方式 | 群里被 @ + 看到 dashboard 卡 | worker prompt（dispatch 自动构造 + token 透传） |
| claim 触发 | 群里代理 workboard_claim | dispatch 自动 claim |
| 完成信号 | 群里代理发"完成"消息 | **status=done**（大管家 workboard_read） |
| TODO.md 写？ | 写（群场景强制）| **不写**（dispatch 派发单人任务） |
| subagent 失败 fallback | 群里重新艾特 | dispatch 内部已处理（block 卡 + 记录原因） |
| 大管家调 complete | ❌ | ❌ |

### 3.4 dispatch 派发常见 Q&A

**Q1：dispatch 派发时 agentId 没设会怎样？**

A：dispatch fallback 到 `DEFAULT_DISPATCH_OWNER`（配置默认 agent）。**不推荐**——工作流层面 agentId 必填。规范（v3.8.0）规定"必填"，技术（dispatch 内部）允许"可选 fallback"。

**Q2：dispatch 启动多个 worker 会冲突吗？**

A：dispatch 默认 `maxStarts=3`（每 pass 最多 3 worker）。同 owner 在同一 pass 只能启动 1 个（`selectStartableCards` 去重）。

**Q3：dispatch 失败了怎么办？**

A：dispatch 内部已处理——claim 成功但 subagent 启动失败 → block 卡 + 记录原因。大管家读卡（status=blocked）看 attempt 错误，重新派发。

**Q4：dispatch CLI vs `workboard_dispatch` agent tool 区别？**（**v3.8.0 关键发现**）

| 入口 | 调什么 | 行为 |
|------|--------|------|
| `workboard_dispatch` **agent tool** | `store.dispatch()` | **只清理**（promote/reclaim/block/orchestrate），**不**启动 worker |
| `openclaw workboard dispatch` **plugin CLI** | `dispatchAndStartWorkboardCards` | 完整：清理 + claim + 启动 subagent |
| `/workboard dispatch` **runtime-slash** | `dispatchAndStartWorkboardCards` | 同 plugin CLI，完整函数 |

**大管家派发必须用 plugin CLI 或 runtime-slash**——agent tool 不派发。

**Q5：dispatch 派发后大管家还需要 IM 通知吗？**

A：**不需要**。dispatch 自动启动 worker，worker 直接读 notes 干活——不需要群里@。如果群里也想知道派发情况，可以额外 IM 通知（可选）。

**Q6：dispatch 派发后大管家要等多久？**

A：worker 跑完自动 complete（不等大管家）。大管家**不需要阻塞等**——下次轮内 `workboard_read` 看 status=done 即可。

---

## 四、通用规则（两场景共用）

### 4.1 TODO 7 字段规范（仅群场景用）

```markdown
- [ ] **T-001.1** 子任务描述  [card={{card_id}}]
  - 👤 负责人：{agent}
  - 🎯 目标：...
  - 📌 约束：...
  - 📁 输入：{绝对路径}
  - 📄 产出：{绝对路径}
  - 📊 状态：⬜ 待认领
```

dispatch 派发场景**不**写 TODO.md（单人任务不必建看板）。

### 4.2 文件路径规范

| 目录 | 用途 | 示例 |
|------|------|------|
| `manuscripts/` | 最终交付物 | 全文整合稿.md、references.bib |
| `temp/` | **中间过程文件** | 心理家家产出的认知范式补充资料 |
| `knowledge/` | **知识沉淀**（长期保存）| 文献综述笔记、理论详解 |

**硬要求**：
- 卡 notes / IM 模板的文件路径**必须绝对路径**——如 `~/OneDrive/Applications/openclaw repository/.../temp/认知范式补充资料.md`
- **中间文件放 `temp/`，不放 `knowledge/`**——知识沉淀才放 `knowledge/`

### 4.3 核验清单（两场景共用，v3.8.0 简化）

- [ ] 产出文件是否存在（绝对路径）
- [ ] 中间文件放 `temp/`，最终产出放 `manuscripts/`
- [ ] 产出内容是否符合 4 必填（目标 / 约束 / 输入 / 产出）
- [ ] 引用格式是否规范
- [ ] 是否有 `workboard_proof`（status: passed）
- [ ] **status 是否变 done**（v3.8.0 验收权下放标志）

### 4.4 反馈措辞

`workboard create` 反馈措辞**按 session 场景自动切换**：

| session 类型 | 反馈措辞 |
|---|---|
| `feishu:group:oc_xxx`（群）| "完成后在群聊中艾特大管家汇报" |
| 其他（dashboard / DM / main）| "完成后在当前会话中向派发者反馈" |

### 4.5 监控规则（两场景共用）

如果卡超过 30 分钟仍在 `running`：
1. 读卡看 attempt 状态 + session 活跃度
2. 检查群里（或 DM 里）是否有"已认领"消息
3. 如代理卡死 → 提醒续 `workboard_heartbeat` 或手动重派

### 4.6 禁止行为清单（v3.8.0 修订）

1. **一个任务只艾特一个代理**（群派发）——不得在同一条消息中艾特多个代理
2. ~~禁止私信汇报~~（v3.2.0 撤销；v3.8.0 私聊派发改成 dispatch 派发，DM 是合法通道）
3. **禁止用 Dashboard 的"开始"按钮**——必须用 CLI
4. **不要重复发 IM 模板**——只一个模板（群派发）
5. ~~不要在 create 后手动 move 到 todo~~（v3.8.0 删除——不再适用）
6. **不要在 agent 执行中用群消息发进度**——走 workboard（群派发）
7. **不要把 workboard 当 TODO 平替**——各管一段
8. ~~不要给 workboard CLI 加 spawn / dispatch 子命令~~（已撤销——CLI 实际已存在）
9. **卡 notes / IM 模板的文件路径必须绝对路径**
10. **中间文件放 `temp/`，不放 `knowledge/`**
11. **v3.8.0 新增**：大管家**不调** `workboard_complete` 验收——worker 自己 complete
12. **v3.8.0 新增**：大管家**不调** `workboard_claim` 抢任务——让代理 / dispatch 调

---

## 五、完整工作流（v3.8.0 简化）

### 5.1 二阶段总览（v3.8.0 简化）

```
┌─────────────────────────────────────────────────────────────┐
│ Phase 1：建卡 + 触发（一次性）  5-30s                          │
│   workboard_create + (IM 艾特 | openclaw workboard dispatch) │
├─────────────────────────────────────────────────────────────┤
│ Phase 2：追踪（被动观察）  数秒到数分钟                          │
│   Dx 自动 / 代理自管 / worker 自动 complete                   │
│   大管家在这里 100% 不介入，只 workboard_read 看 status       │
│   status=done → 汇报老板                                     │
└─────────────────────────────────────────────────────────────┘
```

- Phase 1 大管家主动（建卡 + 触发）
- Phase 2 大管家被动（`workboard_read` 看 status）
- status=done 时汇报老板，不调 `workboard_complete`

### 5.2 派发双通道对比（v3.8.0 重构）

| 维度 | 群派发 | dispatch 派发 |
|------|--------|--------------|
| 触发 | 老板在群里交任务 | 老板在 DM 或群里交任务（机器启动）|
| 派发动作 | IM 5 段模板艾特 | `openclaw workboard dispatch` CLI |
| 卡 status 默认 | backlog | ready |
| claim 触发 | 群里代理 workboard_claim | dispatch 自动 claim |
| 同步方式 | Dx 推：backlog → running | dispatch 推：ready → running |
| 完成信号 | 群里代理发"完成"消息 | **status=done**（大管家 workboard_read） |
| TODO.md 写？ | 写 | **不写** |

### 5.3 跨场景大管家工作流（v3.8.0 简化）

**群场景**完整 4 步：

```
[1] workboard_create({ agentId, priority, labels, status: "backlog" })
    注：plugin CLI 不支持 session 绑定，用 workboard_comment 写软关联
[2] workboard_comment({ id, body: "sessionKey=agent:writer:feishu:group:oc_xxx" })
[3] IM 5 段模板艾特（开头带 workboard 信息：cardId/short + sessionKey + dashboard URL）
[4] 群里代理 claim + 执行 + proof + complete（Dx 全包同步）
[5] 大管家被动追踪：workboard_read 看 status=done → 汇报老板
    ❌ 不调 workboard_complete
```

**dispatch 派发场景**完整 3 步（v3.8.0 新增，**取代私聊 spawn**）：

```
[1] workboard_create({ agentId, priority, labels, status: "ready" })
[2] openclaw workboard dispatch --board default --expect-final --timeout 300000
    → dispatch 自动 claim + 启动 subagent worker
[3] workboard_read 看 status=done → 汇报老板
    ❌ 不调 workboard_complete
```

- 群场景 4 步（写 TODO + 建卡 + IM + 追踪）
- dispatch 派发场景 3 步（建卡 + dispatch + 追踪）
- 大管家不调 `workboard_complete`（验收权下放）

---

## 六、消息/note 模板库

### 6.1 workboard_create 模板（任务四要素）

```js
{
  title: "[<前缀>] <任务描述>",
  notes: `任务目标：...
任务约束：...
输入路径：...
输出路径：...`,
  agentId: "<writer/reviewer/psychologist/...>",
  priority: "low/normal/high/urgent",
  labels: ["test", "v3.8.0", "..."],
  status: "backlog"（群派发）/ "ready"（dispatch 派发）
}
```

**任务四要素**：

| 要素 | 含义 | 示例 |
|------|------|------|
| **任务目标** | 干什么 | 写一首中文诗（主题/格律自选）|
| **任务约束** | 限制 / 边界 | 不调任何 workboard 工具 / 不少于 4 句 / 严守格律 |
| **输入路径** | 读什么文件 / 资源 | `~/.openclaw/workspace/steward/IDENTITY.md` |
| **输出路径** | 产出落到哪 | 主 DM 回复 / `/tmp/...md`（文件产出）|

### 6.2 IM 5 段模板（群派发）

```
{{task_desc}}

{{@代理}}

🔧 workboard 信息：
- card_id: {{card_id}}（短 8 位：{{card_short}}）
- session: {{sessionKey}}
- dashboard: {{card_url}}

📋 前置要求：
- 明确自己的角色：{{agent_role}}
- 找到对应的 .agents/agents/{{agent}}.md 阅读
- 查看 TODO.md 中的 {{subtask}} 子任务

☁ 完成反馈：
- 在群里艾特大管家
- 汇报结果
```

### 6.3 dispatch 派发 CLI 模板（v3.8.0 新增）

```bash
openclaw workboard dispatch \
  --board default \
  --expect-final \
  --timeout 300000
```

**前置 workboard_create 必须满足**：
- `agentId` 必填（dispatch 启动 worker = 这个 agent）
- `status: "ready"`（dispatch 选 ready 卡）
- `notes` 含任务四要素（任务目标 / 任务约束 / 输入路径 / 输出路径）

**追踪步骤**（worker 跑完后）：
```bash
# 大管家被动追踪
workboard_read({ id: cardId })
# status=done → 汇报老板
# ❌ 不调 workboard_complete
```

### 6.4 通知模板 4 要素（v3.7.0 保留）

**通知模板是派发通知的核心内容**——4 要素：

| 要素 | 含义 | 示例 |
|------|------|------|
| **任务标题** | 告诉代理做什么 | 写一首词（蝶恋花/水调歌头自选）|
| **CARD_ID** | 告知 workboard 卡 ID | `34b4d37f-704b-4a8e-bdeb-d2db19b73a73` |
| **操作步骤** | 按 v3.5.0 范式自管 workboard | claim → comment → proof → complete |
| **反馈要求** | 完成后怎么反馈 | 主 DM 回复 / 调 specific 工具 |

**注意（v3.8.0）**：dispatch 派发场景下不需要 IM 5 段模板——dispatch 自动启动 worker，worker 直接读 notes。

### 6.5 派发范式 3 句话总结（v3.5.0 保留）

1. **大管家核心原则**：大管家 = 建卡（定任务）+ 触发（通知代理 / dispatch 启动 worker）+ 追踪（看 done 汇报老板）。中间执行全由 subagent / worker 自治完成。
2. **v3.5.0 流式关键**（群派发）：派发后**不调 sessions_yield**——reply 即本回合最终流式回复——turn 自然结束——runtime auto-push event 触发大管家下一轮。
3. **大管家只核验不接管**（v3.8.0 升级）：subagent / worker 完整自管 workboard 卡（claim + comment + proof + complete）——大管家仅 `workboard_read` 追踪 status——除 dispatch 内部已处理的失败外**不**调 reassign / claim / complete。

---

## 七、异常处理

### 7.1 Dx 误判排查

如果卡在 5 分钟内 `blocked` 3+ 次：

```js
// 1. 读卡确认 attempt 状态
workboard_read({ id: cardId })

// 2. 如果 attempt 状态是 running（Dx 误判），unblock
workboard_unblock({ id: cardId })

// 3. 如果 attempt 状态是 blocked（真失败），看 attempt 错误信息
// 4. retry：手动重新派发（群里重新 @ / 重新 dispatch CLI）
```

**预防**：代理 claim 后立即 `workboard_heartbeat` 续约，避免 claim token 过期被 Dx 误判。

### 7.2 子代理失败处理（两场景通用）

| 失败类型 | 表现 | 处理 |
|----------|------|------|
| claim 后 session 卡死 | 卡 `running` 30 分钟+ | 检查 session 活跃度；提醒代理 heartbeat；或 `workboard_block` + 重新派发 |
| 产出不符合约束 | 核验发现错误 | `workboard_comment` 写反馈；`workboard_block`；大管家修改 task 描述后重新派发 |
| 任务理解错误 | proof 不通过 | 同上 |
| 代理崩溃/timeout | session 失败 | Dx 推卡到 `blocked`；大管家读卡看 attempt 错误；重新派发 |
| dispatch 启动失败 | status=blocked | dispatch 内部已 block + 记录原因；大管家读卡看 attempt 错误，重新 dispatch |

### 7.3 重新派发（v3.8.0 修改）

- **群场景**：群里重新发 IM 模板（不传 `--no-dup` 让建新卡；或读旧卡用新 `move --status todo` 复用）
- **dispatch 派发场景**：重新 `openclaw workboard dispatch`（dispatch 内部已处理 claim 失败）；或读 blocked 卡重新派发

---

## 八、版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| **v3.8.0** | 2026-07-02 | (1) 派发模式重构：群派发（IM）/ dispatch 派发（CLI）；(2) 新增 §三、dispatch 派发场景；(3) 删除 §三、私聊派发场景；(4) §1.2 铁律改为 2 动作 + 验收权下放；(5) §1.3 状态机跳过 review；(6) §1.4 = 2 种场景；(7) §4.6 取消 dispatch 禁令；(8) §5.1 二阶段总览；(9) §6.3 dispatch CLI 模板；(10) v3.7.0 撤销 CLI 错判 |
| **v3.7.0** | 2026-06-06 | **重大补充**（老板拍板）：(1) **任务四要素**（建卡 note 核心）——任务目标 / 任务约束 / 输入路径 / 输出路径；(2) **通知模板 4 要素**（派发核心）——任务标题 / CARD_ID / 操作步骤 / 反馈要求；(3) 其他模板保持（10 个原模板不变）。**v3.8.0 撤销部分** |
| **v3.6.0** | 2026-06-06 | **重大补充**（老板拍板 + 模板测试验证）：(1) **新加"§六、消息/note 模板库"**——指向 workboard-guide.md §三之5（v3.5.0 范式所有消息/note 模板）；(2) 序号顺移：原"§六、异常处理" → §七；原"§七、版本历史" → §八；(3) 异常处理子小节 6.x → 7.x 重编号；(4) 模板来源：5 轮测试验证（轮 1-3 / 重测 / 完整流程 / 模板测试）|
| **v3.5.0** | 2026-06-06 | **重大修正**（3 轮多轮测试验证，老板拍板）：(1) **§五.4 私聊派发防中断**：删除"立即发'已派发'消息"——改为"**不调 yield**——流式 reply——turn 自然结束——runtime auto-push event 触发下一轮"；(2) **§五.5 私聊派发 6 步**（v3.4.0 写 7 步）：重写——subagent 完整自管 workboard（claim + comment + proof + complete）——大管家**只**核验——**不**接管；(3) **§五.5 接管 fallback**：3 种 fallback 场景（subagent claim 失败 / 没调 workboard / 没 complete）——大管家 reassign + claim + complete 或 sessions_send 续接；(4) **v3.4.0 §五.4 §五.5 错误**（已撤销） |
| **v3.4.0** | 2026-06-06 | **重大补充**（老板指正 + 联动测试验证）：(1) **新加"§五、完整工作流"**——3 阶段总览（建卡+派发 / 等待 / 验收）/ 派发双通道对比 / 验收三态详细流程；(2) **加"§五之2、私聊派发防中断兜底"**；(3) **加"§五之3、跨场景大管家工作流整合"**——群场景 + 私聊场景完整 5 步流程；(4) 原"§五、异常处理" → §六（序号顺移）|
| **v3.3.0** | 2026-06-06 | **重大修复**（老板纠错）：(1) **删除所有 `manager workboard` CLI 引用**（v2026.6.6）—— `scripts/workboard/` 932 行 Python 已删；(2) **建卡/验收全部走 `workboard_*` agent tool**（plugin contract tools 一直就有，见 `extensions/workboard/openclaw.plugin.json`）；(3) **shell 备选用 `openclaw workboard` plugin CLI**（runtime-slash 命令）；(4) **踩坑教训**：v8.25.0 拍板时漏看了 `workboard_create` agent tool，错让老板创建 932 行 Python 脚本——**完全没必要的** |
| 3.2.0 | 2026-06-06 01:05 | **结构重构**（老板 2026-06-06 指正）：从 9 节精简到 6 节，按**场景**为主线（群派发 / 私聊派发），通用规则集中放一节，异常处理单独一节。改善 v3.1.0"读起来很乱"问题 |
| 3.1.0 | 2026-06-06 00:55 | **新增私聊派发场景**（老板 2026-06-06 拍板）：用户 DM 交任务时，大管家走"建卡 + sessions_spawn + 验收"3 步（不写 TODO、不艾特群）；workboard 仍是任务进度控制面（建卡 + 验收），派发动作（IM 群艾特 / sessions_spawn）由大管家手动做，**不**走 workboard CLI。**v3.8.0 撤销**——dispatch 取代 sessions_spawn 私聊派发 |
| 3.0.1 | 2026-06-03 03:05 | **老板定型**：(1) IM 群艾特必须（纠正 v3.0.1 草案"可选"）；(2) 任务进度反馈走 workboard（proof+comment）；(3) start 保留但不主动调；(4) 中间文件放 temp/，不放 knowledge/；(5) 采纳 A/B/C/E 提议，撤回 D；(6) 新增 --no-dup 防重复建卡 |
| 3.0.0 | 2026-06-03 02:39 | 基于 T001.1 端到端测试定型：5+1 步 → 3 步派发；Dx 自动行为；代理汇报 |
| 2.3.0 | 2026-06-03 | TODO 7 字段定型 |
| 2.2.0 | 2026-06-03 | 5+1 步新流程 |
| 2.0.0 | 2026-05-21 | task-guide.md v2.0 |

---

*最后更新：2026-07-02 06:00*
*v3.8.0 整理者：大管家（steward）*
*v3.8.0 派发闭环验证：测试卡 d7709861-1412-4e2d-9976-812419aa1e27（status=done）*
