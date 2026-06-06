# 任务流指南 v3.3.0

> **v3.3.0 重大修复**（2026-06-06 老板纠错）：
> 1. **删除所有 `manager workboard` CLI 引用**（v2026.6.6）—— `scripts/workboard/` 932 行 Python 已删
> 2. **建卡/验收全部走 `workboard_*` agent tool**（plugin contract tools 一直就有，见 `extensions/workboard/openclaw.plugin.json`）
> 3. **shell 备选用 `openclaw workboard` plugin CLI**（runtime-slash 命令）
> 4. **踩坑教训**：v8.25.0 拍板时漏看了 `workboard_create` agent tool，错让老板创建 932 行 Python 脚本——**完全没必要的**

> **v3.2.0 重构**（2026-06-06 老板指正）：
> 1. 按**场景**为主线分节：群派发 vs 私聊派发——两场景自包含，读者"查群怎么发"或"查私聊怎么发"一节搞定
> 2. **通用规则**集中放一节（TODO 7 字段、文件路径、反馈措辞、监控、禁止行为）
> 3. **异常处理**单独一节（Dx 误判、代理失败、重新派发）
> 4. 从 9 节精简到 6 节，读起来更顺

> **v3.1.0 老板拍板**（2026-06-06）：workboard 永远只管"建卡/管理"，**派发动作（IM 群艾特 / sessions_spawn）由大管家手动做**，不走 workboard CLI
>
> **v3.0.1 老板定型**（2026-06-03）：(1) IM 群艾特是必须；(2) 任务进度反馈走 workboard（proof+comment+status），群消息只用于派发通知 + 完成确认；(3) 中间文件放 temp/，不放 knowledge/；(4) 卡 notes / IM 模板的文件路径必须绝对路径

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
- **文件路径必须绝对**——如 `/data/disk/仓库/.../temp/认知范式补充资料.md`
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
- 卡 notes / IM 模板的文件路径**必须绝对路径**——如 `/data/disk/仓库/.../temp/认知范式补充资料.md`
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

## 五、异常处理

### 5.1 Dx 误判排查

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

### 5.2 子代理失败处理（两场景通用）

| 失败类型 | 表现 | 处理 |
|----------|------|------|
| claim 后 session 卡死 | 卡 `running` 30 分钟+ | 检查 session 活跃度；提醒代理 heartbeat；或 `workboard_block` + 重新派发 |
| 产出不符合约束 | 核验发现错误 | `workboard_comment` 写反馈；`workboard_block`；大管家修改 task 描述后重新派发 |
| 任务理解错误 | proof 不通过 | 同上 |
| 代理崩溃/timeout | session 失败 | Dx 推卡到 `blocked`；大管家读卡看 attempt 错误；重新 spawn |

### 5.3 重新派发

- **群场景**：群里重新发 IM 模板（不传 `--no-dup` 让建新卡；或读旧卡用新 `move --status todo` 复用）
- **私聊场景**：重新 `sessions_spawn`（spawn task 里传新 card_id 或复用旧 card）

---

## 六、版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 3.2.0 | 2026-06-06 01:05 | **结构重构**（老板 2026-06-06 指正）：从 9 节精简到 6 节，按**场景**为主线（群派发 / 私聊派发），通用规则集中放一节，异常处理单独一节。改善 v3.1.0"读起来很乱"问题 |
| 3.1.0 | 2026-06-06 00:55 | **新增私聊派发场景**（老板 2026-06-06 拍板）：用户 DM 交任务时，大管家走"建卡 + sessions_spawn + 验收"3 步（不写 TODO、不艾特群）；workboard 仍是任务进度控制面（建卡 + 验收），派发动作（IM 群艾特 / sessions_spawn）由大管家手动做，**不**走 workboard CLI |
| 3.0.1 | 2026-06-03 03:05 | **老板定型**：(1) IM 群艾特必须（纠正 v3.0.1 草案"可选"）；(2) 任务进度反馈走 workboard（proof+comment）；(3) start 保留但不主动调；(4) 中间文件放 temp/，不放 knowledge/；(5) 采纳 A/B/C/E 提议，撤回 D；(6) 新增 --no-dup 防重复建卡 |
| 3.0.0 | 2026-06-03 02:39 | 基于 T001.1 端到端测试定型：5+1 步 → 3 步派发；Dx 自动行为；代理汇报 |
| 2.3.0 | 2026-06-03 | TODO 7 字段定型 |
| 2.2.0 | 2026-06-03 | 5+1 步新流程 |
| 2.0.0 | 2026-05-21 | task-guide.md v2.0 |

---

*最后更新：2026-06-06 01:05*
*v3.2.0 重构者：大管家（steward）*
*v3.1.0 新增者：大管家（steward）*
*v3.0.1 定稿者：老板（杨权）*
