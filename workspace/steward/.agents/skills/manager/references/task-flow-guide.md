# 任务流指南 v3.7.0

> v3.7.0：任务四要素（建卡 note 核心）+ 通知模板 4 要素（派发核心）。详见末尾 §八、版本历史。

---

## 一、心智模型（读前必看）

### 1.1 三件套架构

| 层级 | 工具 | 角色 | 谁用 |
|------|------|------|------|
| **纪律层** | `TODO.md` | 看板、状态记录（仅群场景） | 大管家 |
| **执行层** | `workboard` 卡片 | 任务声明、状态机、进度反馈 | 大管家 agent tool（建卡/验收）+ 代理 agent tool（claim/heartbeat/proof/comment）|
| **通知层** | **IM 群艾特**（群场景）/ **`sessions_spawn`**（私聊场景） | 派发通道 | 大管家手动 |

**关键洞察**：
- **三件套缺一不可**：TODO（纪律）+ workboard（执行）+ IM/spawn（通知）
- **workboard 永远只管"建卡/管理"**——**不**提供派发能力
- **dashboard 是任务进度主可见层**——老板通过 dashboard 看进度

### 1.2 大管家 3 动作铁律（v3.3.0 重写）

```
[1] 建卡     →  workboard_create（agent tool，主用）/ openclaw workboard create（plugin CLI，shell 备选）
[2] 派发     →  IM 群艾特（群场景）  /  sessions_spawn（私聊场景）
[3] 验收     →  workboard_read + workboard_comment + workboard_complete（agent tool，全部走 tool）
```

**绝对禁止**给 workboard 加 spawn / dispatch 子命令。**绝对禁止**重建 `manager workboard` CLI（v3.3.0 删除后永不重建）。派发动作永远在大管家会话里手动做。

### 1.3 workboard 状态机（Dx 自动）

```
   create (大管家)
     ↓
   backlog   ← 卡创建（**Dx 自动推**）
     ↓ (Dx 自动，代理 claim)
   running    ← 代理执行
     ↓ (Dx 自动，session 完成)
   review     ← Dx 推→review（等待核验）
     ↓ (大管家手动)
   done       ← 核验通过
     ↓ (大管家手动)
   archived   ← 归档（可选）
```

**Dx 自动行为**：
- 卡有 sessionKey + session 开始 → `backlog → running`
- 卡有 sessionKey + session 完成 → `running → review`
- 卡有 sessionKey + session 失败 → `running → blocked`
- 卡无 sessionKey → **不动**（这正是 v3.1.0 私聊建卡时 `--no-session` 的语义——大管家手动管状态）

### 1.4 两种派发场景概览

| 场景 | 触发 | 派发通道 | workboard 角色 | 流程序号 |
|------|------|----------|----------------|----------|
| **群派发** | 老板在群里交任务 | IM 5 段模板艾特 | 建卡 + 看板 | 看 [二、群派发场景](#二群派发场景v301-主线) |
| **私聊派发** | 老板在 DM 交任务 | `sessions_spawn` 手动启子代理 | 建卡 + 看板 | 看 [三、私聊派发场景](#三私聊派发场景v310) |

**派发通道决定一切**：群里 → IM（人看）；私聊 → spawn（机器看，没群可发）。

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

**TODO 7 字段规范**（仅群场景用，私聊不写 TODO.md）见 [四、通用规则 § 4.1](#41-todo-7-字段规范仅群场景用)。

#### 步骤 2：建 workboard 卡（绑群 session，v3.3.0 改用 agent tool）

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

**关键约束**（v3.3.0）：
- **绑定群 session**用 `workboard_comment` 写软关联（plugin CLI 不支持 sessionKey，agent tool 也没有 `--session` flag）
- **Dx 自动同步**依赖 `metadata.sessionKey`——所以建卡后**必须** comment 写明
- **文件路径必须绝对**——如 `/data/disk/OneDrive/Applications/openclaw repository/.../temp/认知范式补充资料.md`
- 传 `idempotencyKey`（v3.0.1 等价 `--no-dup`）——建卡前查同 title + sessionKey 是否有活跃卡

#### 步骤 3：IM 5 段模板艾特（**必须**）

**完整 IM 模板**（5 段齐全，老板 2026-06-04 拍板）：

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

**模板要点**：
- workboard 信息**在开头**——让代理一进群就看到
- 目标/约束/输入/产出**双轨**（群里可见 + 卡 notes）
- **只一个模板**，不要拆派发/启动/完成多个模板
- 派发前自检 **5 段齐全**

#### 步骤 4：代理自动执行 + 大管家验收

```
代理收到 @ 后自动：
1. 看到 dashboard 有 backlog 卡 → workboard_claim（自动）
2. Dx 看到 claim → 卡 backlog → running（自动）
3. 代理执行任务
4. 代理 workboard_proof 附产出
5. 代理 workboard_comment 留进度反馈
6. Dx 看到 session 完成 → 卡 running → review（自动）
7. 代理在群里发"完成 + 艾特大管家"消息

大管家核验（review 状态时介入）：
1. `workboard_read({ id: cardId })` 看产出
2. 读文件手动核验（4 必填 / 引用规范 / proof status: passed）
3. `workboard_comment({ id, body: "核验结果..." })` 写核验结果
4. 更新 TODO.md 为 [x] + 核验结果
5. `workboard_complete({ id, summary, proof })` → done
6. （可选）群里发简短完成确认（**不是模板**，自己写）
```

**大管家不需要**（Dx 全包）：
- ❌ 手动 `move --status todo`（Dx 自动）
- ❌ 手动 `move --status done`（Dx 自动）

**核验清单**（详）见 [四、通用规则 § 4.3](#43-核验清单两场景共用)。

---

## 三、私聊派发场景（v3.1.0）

### 3.1 适用场景

老板**在 DM 里**（飞书私聊、聊人不在群里）交任务给大管家。群里派发的 IM 艾特通道**不适用**——大管家必须**手动 `sessions_spawn` 启子代理**。

### 3.2 私聊派发 3 步流程

#### 步骤 1：建 workboard 卡（**不**绑 session，v3.3.0 改用 agent tool）

```js
// agent tool（主用）
workboard_create({
  title: "...",
  notes: "目标：... 约束：... 任务描述：...",
  agentId: "{agent}",
  priority: "normal",             // normal / high / urgent
  labels: ["..."],
  status: "todo"                  // 私聊场景默认 todo（不需 Dx 同步）
  // 不传 idempotencyKey（私聊单人任务，重复概率低）
})

// （可选）反馈措辞直接写 notes 里：完成后在当前会话中向派发者反馈
```

**关键调整（vs 群派发建卡，v3.3.0）**：
- **不传 sessionKey**——agent tool 没有 sessionKey 字段（plugin CLI 也没有 `--no-session` flag）
- **不需 `workboard_comment` 写软关联**——私聊场景下 sessions_spawn 返回的 childSessionKey 才需要 comment 写
- **不传 `idempotencyKey`**（私聊单人任务，重复概率低）
- **反馈措辞直接写 notes** 里：默认"在当前会话中向派发者反馈"

#### 步骤 2：sessions_spawn 启子代理（大管家手动，**不**走 workboard CLI）

**workboard 不提供 spawn 派发能力**（v1.5.0 删了 start，v3.2.0 仍维持）。大管家在当前 DM session 里手动启子代理：

```python
# 以 sessions_spawn 隔离模式启子代理
sessions_spawn(
    agentId="{agent}",            # 卡上的 assignee，如 mathematician
    task="""Work on this OpenClaw Workboard card:
- card_id: {card_id}
- card_url: {dashboard_url}
- title: {title}

{notes 全文}

完成后：
1. workboard_proof status=passed 附产出
2. workboard_comment 写进度
3. 在本 DM 会话回复"已完成 + 产出路径"
""",
    isolate=True,                # 隔离子代理，不污染主 DM 会话上下文
    model="minimax",              # v1.5.0 默认，不指具体模型
)
```

**为什么手 sessions_spawn 而不靠 workboard CLI**：
- `workboard_*` agent tool / `openclaw workboard` CLI **不**提供 spawn 派发能力（v1.5.0 删了 start，v3.3.0 仍维持）——派发永远在大管家会话里手动做
- 私聊派发没有"群艾特"通道，**必须**由大管家主动启 session
- 隔离 `isolate=True` 保证子代理不污染主 DM 会话上下文
- spawn 时**显式传 card_id + card_url**——让子代理知道"干的是这张卡"

#### 步骤 3：子代理自动执行 + 大管家验收

```
子代理被 spawn 后自动：
1. 读 card 看 goal/constraints/input/output（task 里给了 dashboard URL）
2. workboard_claim 认领卡
3. 子代理执行（调工具、写文件、读资料）
4. workboard_proof 附产出（status=passed）
5. workboard_comment 写进度
6. Dx 看到 session 完成 → 卡 running → review（自动）
7. 子代理在 DM 会话里回复"已完成 + 产出路径"（spawn task 里显式要求）

大管家核验：
1. `workboard_read({ id: cardId })` 看产出
2. 读文件手动核验
3. `workboard_comment({ id, body })` 写核验结果
4. `workboard_complete({ id, summary, proof })` → done
5. **不**更新 TODO.md（私聊单人任务不必建 TODO）
6. **不**发群完成确认（没群可发；DM 会话里大管家直接读 proof 就知道完成了）
```

### 3.3 spawn task 模板（可复用）

```python
TASK_TEMPLATE = f"""
Work on this OpenClaw Workboard card:
- card_id: {card_id}
- card_url: {dashboard_url}
- title: {title}

{notes 全文}

工作流：
1. workboard_claim 认领卡
2. 按 notes 里的 goal/constraints/input/output 干活
3. workboard_proof status=passed 附产出
4. workboard_comment 留进度反馈
5. 在本 DM 会话回复 "已完成 + 产出路径"
"""
```

### 3.4 私聊 vs 群场景差异

| 维度 | 群派发（v3.0.1） | 私聊派发（v3.1.0） |
|------|------------------|-------------------|
| 触发 | 老板在群里交任务 | 老板在 DM 里交任务 |
| 派发通道 | IM 群 5 段模板艾特 | **大管家手动 `sessions_spawn`** |
| 代理收任务方式 | 群里被 @ + 看 workboard | 启新 session + 传任务 + 看 workboard |
| workboard session | `workboard_comment` 写 `sessionKey=agent:writer:feishu:group:oc_xxx`（agent tool / CLI 都不直接支持 `--session`） | 不传 sessionKey，私聊无 session 关联 |
| 默认 status | backlog（Dx 推） | todo（无 Dx 同步） |
| 进度反馈 | workboard（proof + comment） | **同群派发** |
| 完成汇报 | 群里艾特大管家 | DM 会话里大管家自己看 proof |
| 核验 | 大管家读卡 + comment + move done | **同群派发** |
| TODO 更新 | 核验后更新 | **不写 TODO**（单人任务不必建） |

### 3.5 私聊派发常见 Q&A

**Q1：私聊派发需要大管家会话清单吗？**
不需要。`sessions_spawn` 是隔离子代理，子代理会话**不**进大管家主会话的子任务列表。

**Q2：子代理能在 DM 里回消息吗？**
能——但默认**不**会调 `chat.send` 发到 DM 渠道（spawn 时 task 显式要求才回）。如需 DM 可见回复，在 spawn task 里明说"在 DM 里回一条完成消息"。

**Q3：能不能"多私聊任务"并行？**
能。每个私聊任务 = 独立卡 + 独立 spawn session，互不干扰。

**Q4：子代理出错了怎么办？**
看卡 attempt 状态 → Dx 会把 failed session 推卡到 `blocked` → 大管家读卡看错误 → 手动重派（重新 spawn 或改任务描述）。

**Q5：私聊派发用 `im` 还是 `spawn`？**
用 `spawn`——v3.2.0 定型。`im` 是群派发专用（艾特群成员）。私聊没群，im 不能用。

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

私聊场景**不**写 TODO.md（单人任务不必建看板）。

### 4.2 文件路径规范

| 目录 | 用途 | 示例 |
|------|------|------|
| `manuscripts/` | 最终交付物 | 全文整合稿.md、references.bib |
| `temp/` | **中间过程文件** | 心理家家产出的认知范式补充资料 |
| `knowledge/` | **知识沉淀**（长期保存）| 文献综述笔记、理论详解 |

**v3.0.1 硬要求**：
- 卡 notes / IM 模板的文件路径**必须绝对路径**——如 `/data/disk/OneDrive/Applications/openclaw repository/.../temp/认知范式补充资料.md`
- **中间文件放 `temp/`，不放 `knowledge/`**——知识沉淀才放 `knowledge/`

### 4.3 核验清单（两场景共用）

- [ ] 产出文件是否存在（绝对路径）
- [ ] 中间文件放 `temp/`，最终产出放 `manuscripts/`
- [ ] 产出内容是否符合 4 必填（目标 / 约束 / 输入 / 产出）
- [ ] 引用格式是否规范
- [ ] 是否有 `workboard_proof`（status: passed）

### 4.4 反馈措辞（v1.5.0 动态化）

`workboard create` 反馈措辞**按 session 场景自动切换**（v1.5.0）：

| session 类型 | 反馈措辞 |
|---|---|
| `feishu:group:oc_xxx`（群）| "完成后在群聊中艾特大管家汇报" |
| 其他（dashboard / DM / main）| "完成后在当前会话中向派发者反馈" |

不需要手动传 `--feedback`——CLI 根据 `--session` 自动选措辞。

### 4.5 监控规则（两场景共用）

如果卡超过 30 分钟仍在 `running`：
1. 读卡看 attempt 状态 + session 活跃度
2. 检查群里（或 DM 里）是否有"已认领"消息
3. 如代理卡死 → 提醒续 `workboard_heartbeat` 或手动重派

### 4.6 禁止行为清单

1. **一个任务只艾特一个代理**——不得在同一条消息中艾特多个代理
2. **禁止私信汇报**——进度反馈走 workboard，不私聊（私聊派发场景除外，DM 是派发通道本身）
3. **禁止用 Dashboard 的"开始"按钮**——必须用 CLI
4. **不要重复发 IM 模板**——只一个模板
5. **不要在 create 后手动 move 到 todo**——Dx 自动
6. **不要在 agent 执行中用群消息发进度**——走 workboard
7. **不要把 workboard 当 TODO 平替**——各管一段
8. **不要给 workboard CLI 加 spawn / dispatch 子命令**——派发动作永远在会话里手动做
9. **卡 notes / IM 模板的文件路径必须绝对路径**
10. **中间文件放 `temp/`，不放 `knowledge/`**

---

## 五、完整工作流（v3.4.0 新增）

> 源自 2026-06-06 联动测试 + 老板指正："大管家只需要看最后 done 状态，或者干预一下 blocked 的。claim 是 session/IM 去通知其他代理。"

### 5.1 三阶段总览

```
┌─────────────────────────────────────────────────────────────┐
│ Phase 1：建卡 + 派发（一次性）  5-10s                          │
│   workboard_create + (IM 艾特 | sessions_spawn)              │
├─────────────────────────────────────────────────────────────┤
│ Phase 2：等待（不盯中间）  6s ~ 数分钟                          │
│   Dx 自动同步 / 代理自管理 / OpenClaw runtime push           │
│   大管家在这里 100% 不介入                                       │
├─────────────────────────────────────────────────────────────┤
│ Phase 3：验收（只动 done/blocked）  5-30s                       │
│   done:  workboard_read → 核验 → workboard_comment →         │
│          workboard_complete → archive（可选）                  │
│   blocked: workboard_read → reassign / unblock /             │
│            重新派发 / 接受失败                                 │
└─────────────────────────────────────────────────────────────┘
```

**关键洞察**：
- Phase 1 是**大管家主动动作**（5-10s 一次性）
- Phase 2 是**大管家完全不介入**（Dx / 代理 / runtime 三方自动化）
- Phase 3 是**大管家再次主动**（5-30s，但只对 done/blocked 两种状态）

### 5.2 派发双通道对比

| 维度 | 群派发 | 私聊派发 |
|------|--------|----------|
| 触发 | 老板在群里交任务 | 老板在 DM 交任务 |
| 派发动作 | **IM 5 段模板艾特**（开头带 workboard 信息） | **`sessions_spawn` + `workboard_comment` 软关联** |
| 卡 status 默认 | backlog（Dx 推 running） | todo（Dx/手动推） |
| claim 触发 | 群里代理看到艾特 → 调 workboard_claim | Dx 看到 agentId 匹配 spawn → auto-claim |
| 同步方式 | Dx 推：backlog → running → review | 手动管（spawn + comment 软关联） |
| 完成信号 | 群里代理发"完成"消息 | **announce event 推回主 DM** |
| 兜底 | 群里能看到 @ 状态 | spawn 后**立即发"已派发 + cardId"消息**（防中断）|
| TODO.md 写？ | 写（群场景强制） | **不写**（私聊单人任务） |

### 5.3 验收三态详细流程

```
[卡 status = done]（或 review 状态但已 proof 完毕）
  ↓
workboard_read({ id: cardId })
  查 metadata.proof + artifacts + comments
  ↓
读产出文件（人工核验）
  - 目标达成？
  - 约束符合？
  - 4 必填字段？引用规范？proof status=passed？
  ↓
workboard_comment({ id, body: "核验通过/不通过" })
  ↓
workboard_complete({
  id, token, summary: "...",
  proof: { status: "passed", label, command, note }
})
  ↓
workboard_board_archive({ id, archived: true })  // 可选


[卡 status = blocked]
  ↓
workboard_read({ id: cardId })
  查 failure reason + failureCount
  ↓
决策（4 选 1）：
  ├─ 换人重做：workboard_reassign({ id, agentId: "新代理" })
  │            → workboard_unblock({ id })  // 解阻塞
  │
  ├─ 解阻塞让原代理继续：workboard_unblock({ id })
  │            → 代理 workboard_heartbeat + workboard_proof + workboard_complete
  │
  ├─ 接受失败归档：workboard_complete({
  │     id, proof: { status: "failed", note: "原因..." }
  │   })
  │
  └─ 完全放弃：workboard_board_archive({ id, archived: true })


[卡 status = running]
  ↓
大管家：什么都不做
  ↓
等 announce event 触发
  或等 Dx 推卡到 review
```

### 5.4 私聊派发防中断（v3.5.0 重写：3 轮测试验证）

**老板之前担心**："spawn 后子代理不向你发消息，IM 流中断"

**实测结果（v3.5.0）**：
- ❌ 旧方案"spawn + sessions_yield"：**断流式**（yield message 整段出现，不流式）
- ✅ 新方案"spawn + **不调 yield**"：**保留流式**（runtime auto-push event 触发下一轮）

**v3.5.0 兜底方案**（不调 yield）：

```
[1] workboard_create + sessions_spawn + workboard_comment（顺序）
[2] 流式 reply：派发信息（**不**调 sessions_yield）
[3] turn 自然结束
[4] runtime auto-push 子代理完成 event → 大管家下一轮
[5] 大管家从 history 看到子代理产出 + 核验
```

**关键**：
- **老板 DM 流字字流式**（reply 是本回合最终流式回复）
- **不**依赖 yield 消息（runtime auto-push event 自然触发）
- **不**需要 message tool 独立发"已派发"消息（reply 已包含派发信息）

### 5.5 跨场景大管家工作流（v3.5.0 整合 + 3 轮测试修正）

**群场景**完整 6 步（不变）：
```
[1] workboard_create({ agentId, priority, labels, status: "backlog" })
    注：plugin CLI 不支持 session 绑定，用 workboard_comment 写软关联
[2] workboard_comment({ id, body: "sessionKey=agent:writer:feishu:group:oc_xxx" })
[3] IM 5 段模板艾特（开头带 workboard 信息：cardId/short + sessionKey + dashboard URL）
[4] 群里代理 claim + 执行 + proof + complete（Dx 全包同步）
[5] Dx 推 running → review
[6] 大管家 read + 核验 + comment + complete + archive
```

**私聊场景**完整 7 步（v3.5.0 新版，3 轮测试验证）：

```
[1] workboard_create({ agentId: "writer", priority, labels, status: "todo" })
[2] sessions_spawn({
      task: "用 CARD_ID 调 workboard_claim + comment + proof + complete（完整自管）"
    })
[3] workboard_comment({ id, body: "sessionKey=" + childSessionKey })  // 软关联
[4] 流式 reply（**不**调 sessions_yield）
[5] turn 自然结束
[6] runtime auto-push announce event → 大管家下一轮
[7] 大管家核验（workboard_read + comment 核验意见）—— **不**接管（subagent 已自管）
```

**关键修正（v3.4.0 错误 → v3.5.0 正确）**：
- ❌ v3.4.0 写"❌ workboard_claim"——**错**（实测 subagent 可 claim，**有时序窗口**）
- ❌ v3.4.0 写"❌ workboard_complete"——**错**（实测 subagent 可 complete，用自己 token）
- ✅ v3.5.0 改为"subagent **完整自管**"——大管家**只**核验——**不**接管

**subagent 失败 fallback 路径**（3 种场景，v3.5.0 修正）：

**A. claim 失败**（Dx 先占 + subagent 跑得慢）：
```
大管家 workboard_reassign({ agentId: "steward" })  // 改 agentId
        ↓
大管家 workboard_claim                              // 拿 token
        ↓
大管家 workboard_complete                            // 标 done
```

**B. 没调 workboard**（runtime 太短没机会）：大管家接管（同 A）—— reassign + claim + complete

**C. 没 complete**（异常 / token 过期）：
```
大管家 sessions_send 续接 subagent
        ↓
subagent 用自己 token 调 workboard_complete
        ↓
大管家核验
```

**关键差异**（v3.5.0 vs v3.4.0）：
- 群场景靠 **Dx 自动同步 + IM 群可见**——大管家只发一次艾特
- 私聊场景靠 **runtime auto-push event**（**不**需要 yield 消息）——老板 DM 流**字字流式**

---

## 六、消息/note 模板库（v3.6.0 新增）

> 详见 **workboard-guide.md v1.10.0 §三之5、消息/note 模板库**（10 个模板 + 派发范式 3 句话总结）。

**模板索引**（按使用场景分类）：

| 模板 | 用途 | 场景 |
|------|------|------|
| §三之5.1 workboard_create | 建卡 | 大管家派发前 |
| §三之5.2 sessions_spawn task | spawn 完整自管 task | 大管家派发 |
| §三之5.3 workboard_comment 软关联 | 软关联 childSessionKey | 大管家派发后 |
| §三之5.4 v3.5.0 流式 reply | **不调 yield** 派发完成 | 大管家派发（v3.5.0 核心）|
| §三之5.5 workboard_proof | 附证据 | subagent 验收 / 大管家验收 |
| §三之5.6 workboard_complete summary | 完整归档 | subagent 验收 / 大管家接管 |
| §三之5.7 大管家核验 reply | 核验报告 | 大管家 v3.5.0 不接管 |
| §三之5.8 大管家接管 fallback A | 接管路径 | subagent claim 失败时 |
| §三之5.9 sessions_send 续接 fallback C | 续接子代理 | subagent 跑完没 complete |
| §三之5.10 v3.5.0 派发范式 3 句话总结 | 范式核心 | 所有派发的核心原则 |

**派发核心原则**（v3.5.0 子代理模板测试写的 3 句话）：

1. **大管家核心原则**：大管家 = 建卡（定任务）+ 派发（通知代理）+ 验收；中间执行全由 subagent 自治完成，大管家不介入细节。
2. **v3.5.0 派发关键改进**：派发后**不调 sessions_yield**——reply 即本回合最终流式回复——turn 自然结束——runtime auto-push event 触发大管家下一轮——**流式输出全程保留**。
3. **大管家只核验不接管**：subagent 完整自管 workboard 卡（claim + comment + proof + complete）——大管家仅 workboard_read 核验——除 fallback 路径外**不**调 reassign / claim / complete。

**详细模板内容**：见 workboard-guide.md v1.11.0 §三之5（10 个完整模板）。

**任务四要素**（v3.7.0 老板拍板）——**建卡 note 核心内容**：
- **任务目标**：干什么（写诗/写词/分析数据/审核……）
- **任务约束**：限制/边界（格律/字数/工具/时间/不调什么）
- **输入路径**：读什么文件/资源（绝对路径）
- **输出路径**：产出落到哪（主 DM 回复/具体文件路径/卡 metadata）

**通知模板 4 要素**（v3.7.0 老板拍板）——**派发通知核心内容**：
- **任务标题**：告诉代理做什么
- **CARD_ID**：告知 workboard 卡 ID（让代理自管）
- **操作步骤**：按 v3.5.0 范式自管 workboard（claim → comment → proof → complete）
- **反馈要求**：完成后怎么反馈（主 DM 回复 / 调 specific 工具 / 给具体路径）

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
// 4. retry：手动重新 spawn（私聊）/ 群里重新 @ 代理（群场景）
```

**预防**：代理 claim 后立即 `workboard_heartbeat` 续约，避免 claim token 过期被 Dx 误判。

### 7.2 子代理失败处理（两场景通用）

| 失败类型 | 表现 | 处理 |
|----------|------|------|
| claim 后 session 卡死 | 卡 `running` 30 分钟+ | 检查 session 活跃度；提醒代理 heartbeat；或 `workboard_block` + 重新派发 |
| 产出不符合约束 | 核验发现错误 | `workboard_comment` 写反馈；`workboard_block`；大管家修改 task 描述后重新派发 |
| 任务理解错误 | proof 不通过 | 同上 |
| 代理崩溃/timeout | session 失败 | Dx 推卡到 `blocked`；大管家读卡看 attempt 错误；重新 spawn |

### 7.3 重新派发

- **群场景**：群里重新发 IM 模板（不传 `--no-dup` 让建新卡；或读旧卡用新 `move --status todo` 复用）
- **私聊场景**：重新 `sessions_spawn`（spawn task 里传新 card_id 或复用旧 card）

---

## 八、版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| **v3.7.0** | 2026-06-06 | **重大补充**（老板拍板）：(1) **任务四要素**（建卡 note 核心）——任务目标 / 任务约束 / 输入路径 / 输出路径；(2) **通知模板 4 要素**（派发核心）——任务标题 / CARD_ID / 操作步骤 / 反馈要求；(3) 其他模板保持（10 个原模板不变）。详见 §六、消息/note 模板库 |
| **v3.6.0** | 2026-06-06 | **重大补充**（老板拍板 + 模板测试验证）：(1) **新加"§六、消息/note 模板库"**——指向 workboard-guide.md §三之5（v3.5.0 范式所有消息/note 模板）；(2) 序号顺移：原"§六、异常处理" → §七；原"§七、版本历史" → §八；(3) 异常处理子小节 6.x → 7.x 重编号；(4) 模板来源：5 轮测试验证（轮 1-3 / 重测 / 完整流程 / 模板测试）|
| **v3.5.0** | 2026-06-06 | **重大修正**（3 轮多轮测试验证，老板拍板）：(1) **§五.4 私聊派发防中断**：删除"立即发'已派发'消息"——改为"**不调 yield**——流式 reply——turn 自然结束——runtime auto-push event 触发下一轮"；(2) **§五.5 私聊派发 6 步**（v3.4.0 写 7 步）：重写——subagent 完整自管 workboard（claim + comment + proof + complete）——大管家**只**核验——**不**接管；(3) **§五.5 接管 fallback**：3 种 fallback 场景（subagent claim 失败 / 没调 workboard / 没 complete）——大管家 reassign + claim + complete 或 sessions_send 续接；(4) **v3.4.0 §五.4 §五.5 错误**（已撤销） |
| **v3.4.0** | 2026-06-06 | **重大补充**（老板指正 + 联动测试验证）：(1) **新加"§五、完整工作流"**——3 阶段总览（建卡+派发 / 等待 / 验收）/ 派发双通道对比 / 验收三态详细流程；(2) **加"§五之2、私聊派发防中断兜底"**；(3) **加"§五之3、跨场景大管家工作流整合"**——群场景 + 私聊场景完整 5 步流程；(4) 原"§五、异常处理" → §六（序号顺移）|
| **v3.3.0** | 2026-06-06 | **重大修复**（老板纠错）：(1) **删除所有 `manager workboard` CLI 引用**（v2026.6.6）—— `scripts/workboard/` 932 行 Python 已删；(2) **建卡/验收全部走 `workboard_*` agent tool**（plugin contract tools 一直就有，见 `extensions/workboard/openclaw.plugin.json`）；(3) **shell 备选用 `openclaw workboard` plugin CLI**（runtime-slash 命令）；(4) **踩坑教训**：v8.25.0 拍板时漏看了 `workboard_create` agent tool，错让老板创建 932 行 Python 脚本——**完全没必要的** |
| 3.2.0 | 2026-06-06 01:05 | **结构重构**（老板 2026-06-06 指正）：从 9 节精简到 6 节，按**场景**为主线（群派发 / 私聊派发），通用规则集中放一节，异常处理单独一节。改善 v3.1.0"读起来很乱"问题 |
| 3.1.0 | 2026-06-06 00:55 | **新增私聊派发场景**（老板 2026-06-06 拍板）：用户 DM 交任务时，大管家走"建卡 + sessions_spawn + 验收"3 步（不写 TODO、不艾特群）；workboard 仍是任务进度控制面（建卡 + 验收），派发动作（IM 群艾特 / sessions_spawn）由大管家手动做，**不**走 workboard CLI |
| 3.0.1 | 2026-06-03 03:05 | **老板定型**：(1) IM 群艾特必须（纠正 v3.0.1 草案"可选"）；(2) 任务进度反馈走 workboard（proof+comment）；(3) start 保留但不主动调；(4) 中间文件放 temp/，不放 knowledge/；(5) 采纳 A/B/C/E 提议，撤回 D；(6) 新增 --no-dup 防重复建卡 |
| 3.0.0 | 2026-06-03 02:39 | 基于 T001.1 端到端测试定型：5+1 步 → 3 步派发；Dx 自动行为；代理汇报 |
| 2.3.0 | 2026-06-03 | TODO 7 字段定型 |
| 2.2.0 | 2026-06-03 | 5+1 步新流程 |
| 2.0.0 | 2026-05-21 | task-guide.md v2.0 |

---

*最后更新：2026-06-06 14:25*
*v3.7.0/v3.6.0/v3.5.0/v3.4.0/v3.3.0 整理者：大管家（steward）*
