# 任务流指南 v3.0.1

> **v3.0.1 老板定型**（2026-06-03 03:05）：
> 1. **IM 群艾特是必须**（v3.0.1 草案写"可选"——**老板纠正，撤回**）
> 2. **任务进度反馈走 workboard**（proof + comment + status），群消息只用于派发通知 + 完成确认
> 3. **start 保留但不主动调**——CLI 不删除，应对未来 Dx bug 修复或新场景
> 4. **中间文件放 temp/，不放 knowledge/**——knowledge/ 只放知识沉淀
> 5. 采纳提议 A/B/C/E，撤回 D

---

## 一、心智模型

```
老板交任务
    ↓
[1] 大管家：写 TODO.md + 创建 workboard 卡（**只到 backlog**）
    ↓
[2] **IM 群艾特代理（必须）**—— 派发通知
    ↓
[3] 代理自取 + claim：workboard dashboard 找卡 → workboard_claim
    ↓
[4] 代理自动：spawn → running → 完成 → done（Dx 全包）
    ↓
[5] 代理通过 workboard 反馈：workboard_proof + workboard_comment（任务进度）
    ↓
[6] 大管家：核验（workboard_comment 写核验结果） + 更新 TODO + move to done
    ↓
（可选）大管家在群里发完成确认
```

| 层级 | 工具 | 角色 | 谁用 |
|------|------|------|------|
| **纪律层** | `TODO.md` | 看板、状态记录 | 大管家 |
| **执行层** | `workboard` 卡片 | 自取任务 + 状态机 + 进度反馈 | 大管家 CLI（create）+ 代理插件工具（claim/heartbeat/proof/comment）|
| **通知层** | **IM 群艾特**（**必须**）| 派发通知 + 完成确认 | 大管家 |
| **可见层** | **dashboard** | 任务进度查看（人类旁观察看）| 老板 + 大管家 |

**关键洞察**：
- **IM 群艾特是必须**——不艾特 = 代理不知道有新任务
- **dashboard 是主可见层**——老板通过 dashboard 看任务进度
- **任务进度反馈走 workboard**（proof / comment / status），群消息**不重复发**
- **三件套（TODO + workboard + IM）缺一不可**

---

## 二、群派发 4 步流程（v3.0.1 主线场景）

> **v3.1.0 补充**（2026-06-06）：大管家“私聊你发送任务”场景在原 4 步流程里不适用（无“群艾特”通道），看 [三、私聊派发场景](#三私聊派发场景) 处理。

### 步骤 1：明确任务 + 写 TODO（大管家）

回答三个问题：
- **任务目标**：一句话说清要干什么
- **指派对象**：哪个 agent（`writer` / `reviewer` / `psychologist` / ...）
- **优先级 + 标签**：`low/normal/high/urgent` + `labels`

TODO 7 字段：

```markdown
- [ ] **T-001.1** 子任务描述  [card={{card_id}}]
  - 👤 负责人：{agent}
  - 🎯 目标：...
  - 📌 约束：...
  - 📁 输入：{绝对路径}
  - 📄 产出：{绝对路径}
  - 📊 状态：⬜ 待认领
```

**文件路径规范（v3.0.1 硬要求）**：

| 目录 | 用途 | 示例 |
|------|------|------|
| `manuscripts/` | 最终交付物 | 全文整合稿.md、references.bib |
| `temp/` | **中间过程文件** | 心理家家产出的认知范式补充资料 |
| `knowledge/` | **知识沉淀**（长期保存）| 文献综述笔记、理论详解 |

### 步骤 2：建 workboard 卡（大管家 CLI，**只到 backlog**）

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
  --no-dup                    # v3.0.1 新增：避免重复建卡
# 不传 --status → 默认 backlog（v1.4.0 起的默认行为）
```

**关键约束**：
- **只到 backlog**——**禁止**手动 `move --status todo`（Dx 自动覆盖）
- **文件路径必须绝对**——如 `/data/disk/仓库/.../temp/认知范式补充资料.md`
- 传 `--no-dup`（v3.0.1）——建卡前查同 title + sessionKey 是否有活跃卡

### 步骤 3：IM 群里艾特代理（**必须**）

**IM 模板**：

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
- workboard 信息**在开头**
- 目标/约束/输入/产出**双轨**（群里可见 + 卡 notes）
- 进度反馈指引改为"通过 workboard 提交"
- **只一个模板**，不拆多个

### 步骤 4：代理自取 + 自动执行（大管家不介入）

代理收到 @ 后自动：

```
1. 看到 dashboard 有 backlog 卡 → workboard_claim（**自动**）
2. Dx 看到 claim → 卡 backlog → running（**自动**）
3. 代理执行任务
4. 代理 workboard_proof（附产出）
5. 代理 workboard_comment（留进度反馈）
6. Dx 看到 session 完成 → 卡 running → done（**自动**）
```

**大管家不需要**：
- ❌ 手动 `move --status todo`（Dx 自动）
- ❌ 手动 `move --status done`（Dx 自动）
- ❌ ~~手动 `manager workboard start`~~（v1.5.0 已删除子命令，代理认领后自己 `chat.send` 启 run）

**监控**：如果卡超过 30 分钟仍在 running，介入处理（看 attempt 状态 + 群消息）

---

## 三、私聊派发场景（v3.1.0 新增，2026-06-06）

> **背景**：用户私聊大管家发送任务（Feishu DM、聊人不在群里）。群派发 [二、群派发 4 步流程](#二群派发-4-步流程v301-主线场景) 不能用——没“群艾特”通道。

### 私聊 vs 群场景差异

| 维度 | 群派发（v3.0.1） | 私聊派发（v3.1.0） |
|------|------------------|-------------------|
| 触发 | 老板在群里交任务 | 老板在 DM 里交任务 |
| 派发通道 | IM 群 5 段模板艾特 | **大管家手动 `sessions_spawn`** |
| 代理收任务方式 | 群里被 @ + 看 workboard | 启新 session + 传任务 + 看 workboard |
| 进度反馈 | workboard（proof + comment） | **同群派发**（workboard 仍是进度反馈层）|
| 完成汇报 | 群里艾特大管家 | **不发群**（没群可发），大管家自己从 workboard 看 |
| 核验 | 大管家读卡 + workboard_comment + move done | **同群派发** |
| TODO 更新 | 核验后更新 | **同群派发** |

> **私聊派发的工作量 = 3 步**（建卡 + spawn + 验收），不写 TODO.md（TODO 是看板面向老板 + 多任务场景，私聊单人任务不必建 TODO）。

### 私聊派发 3 步流程

#### 步骤 1：建 workboard 卡（大管家 CLI，同群派发）

```bash
manager workboard create \
  --assignee {agent} \
  --priority {normal|high|urgent} \
  --no-session                     # v3.1.0 私聊不联 dashboard session，用 spawn 启新 session
  --task-desc "..." \
  --agent-role {agent} \
  --goal "..." \
  --constraints "..." \
  --feedback "在当前会话中向派发者反馈"
# 不传 --status → 默认 todo
```

**关键调整**：
- **`--no-session`**：不联动 dashboard session（私聊场景不需要绑到特定 session）
- **反馈措辞**：默认"在当前会话中向派发者反馈"（v1.5.0 动态反馈措辞，dashboard 场景适用）
- **不传 `--status`** → 默认 `todo`（不是 backlog，因为不需 Dx 同步）

#### 步骤 2：私聊 spawn 代理（大管家手动，不走 workboard CLI）

**workboard 不提供 spawn 派发能力**（v1.5.0 删了 start）。大管家在当前 DM session 里手动启子代理：

```python
# 示例（以 sessions_spawn 隔离模式启子代理）
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
    isolate=True,                # 隔离子代理
    model="minimax",              # 不指具体模型
)
```

**为什么手 sessions_spawn 而不靠 workboard CLI**：
- `manager workboard` **不**提供派发能力（v1.5.0 删除 start 后剩 16 个子命令都是“看板/管理”动作）
- 私聊派发没有“群艾特”通道，**必须**由大管家主动启 session
- 隔离 `isolate=True` 保证子代理不污染主 DM 会话上下文

**完整 spawn 参数**（参考 [sessions_spawn tool 文档]）：agentId / task / isolate / model / sandbox / light_context 等。

#### 步骤 3：代理自取 + 自动执行（与群派发一致）

子代理被 spawn 后，**自己读卡 + 走 workboard 工作流**（不需大管家介入）：

```
1. 子代理在隔离 session 里收到任务 → 读 card 看 goal/constraints/input/output
2. workboard_claim 认领卡
3. 子代理执行（调工具、写文件、读资料）
4. workboard_proof 附产出（status=passed）
5. workboard_comment 写进度
6. Dx 看到 session 完成 → 卡 running → review（自动）
7. 子代理在 DM 会话里回复"已完成 + 产出路径"（只在 spawn 时大管家传的 task 里要求）
```

**大管家不需要**：
- ❌ 任何 `manager workboard` 动作（create 完了就等）
- ❌ 手动 chat.send / move（Dx 自动）

**监控**：卡超过 30 分钟仍在 running，介入处理（看 attempt + DM session）

### 步骤 4：大管家核验 + 验收（与群派发一致）

```bash
# 1. 读卡看产出
manager workboard read --id <card_id>

# 2. 读文件核验
# /data/disk/仓库/.../manuscripts/{output_file}

# 3. workboard_comment 写核验结果
workboard_comment --id <card_id> --body "核验通过：..."

# 4. move to done
manager workboard move --id <card_id> --status done
```

**不更新 TODO.md**（私聊单人任务不必建 TODO）。

**不在群里发完成确认**（没群可发；DM 会话里大管家直接读 proof 就知道完成了）。

### 私聊派发常见问题

**Q1：私聊派发需要大管家会话清单吗？**
不需要。`sessions_spawn` 是隔离子代理，子代理会话**不**进大管家主会话的子任务列表。

**Q2：子代理能在 DM 里回消息吗？**
能——但默认**不**会调 `chat.send` 发到 DM 渠道（spawn 时 task 显式要求才回）。如需 DM 可见回复，在 spawn task 里明说“在 DM 里回一条完成消息”。

**Q3：能不能“多私聊任务”并行？**
能。每个私聊任务 = 独立卡 + 独立 spawn session，互不干扰。

**Q4：子代理出错了怎么办？**
看卡 attempt 状态 → Dx 会把 failed session 推卡到 `blocked` → 大管家读卡看错误 → 手动重派或改任务描述重新 spawn。

**Q5：私聊派发用 `im` 还是 `spawn`？**
用 `spawn`——v3.1.0 定型。`im` 是群派发专用（艾特群成员）。私聊没群，im 不能用。

---

## 四、代理反馈（走 workboard，不走群消息）

代理执行任务期间，通过 workboard 提交进度：

| 工具 | 用途 | 时机 |
|------|------|------|
| `workboard_comment` | 进度描述、遇到问题 | 执行过程中按需 |
| `workboard_proof` | 产出证明（artifact） | 任务完成时 |
| `workboard_heartbeat` | 续约 claim token | 每 10 分钟续约 |

**🚫 禁止**：群里发"进度更新"消息——群消息只用于派发通知 + 完成确认。
**✅ 必须**：任务完成后附 workboard_proof（status: passed）。

---

## 五、大管家核验 + TODO 更新

```bash
# 1. 读卡看产出
manager workboard read --id <card_id>

# 2. 读文件核验（手动）
```

**核验清单**：
- [ ] 产出文件是否存在（绝对路径）
- [ ] 中间文件放 temp/，最终产出放 manuscripts/
- [ ] 产出内容是否符合 4 必填（目标/约束/输入/产出）
- [ ] 引用格式是否规范
- [ ] 是否有 workboard_proof（status: passed）

**核验通过后**：
1. **workboard_comment** 写核验结果：`核验通过：4 范式齐全，300 字/段，APA 7 引用规范`
2. **更新 TODO.md**：
   ```markdown
   - [x] **T-001.1** 子任务描述  [card={{card_id}}] ✅
     - 👤 负责人：{agent}
     - 🎯 目标：...
     - 📌 约束：...
     - 📁 输入：...
     - 📄 产出：{{output_file}} ✅ 已完成
     - 📊 状态：✅ 已完成
     - **核验结果**：{{核验总结}}
   ```
3. **move to done**：`manager workboard move --id <card_id> --status done`
4. （可选）群里发简短确认消息（**不是模板**，大管家自己写）

---

## 六、任务状态映射

### workboard 状态机（Dx 自动）

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
```

**Dx 自动行为**：
- 卡有 sessionKey + session 开始 → backlog → running
- 卡有 sessionKey + session 完成 → running → review
- 卡有 sessionKey + session 失败 → running → blocked
- 卡无 sessionKey → 不动

### TODO ↔ workboard 状态对应

| workboard 状态 | TODO 标记 | 含义 |
|---------------|-------------|------|
| `backlog` | ⬜ 待开始 | 刚 create（Dx 自动推中）|
| `running` | 🔄 进行中 | 代理已 claim 在跑 |
| `review` | 👀 待核验 | 等待大管家核验 |
| `done` | ✅ 已完成 | 大管家核验通过 |
| `blocked` | ❌ 阻塞 | Dx 误判或执行失败 |

---

## 七、Dx 误判排查（v3.0.1 新增）

如果卡在 5 分钟内 blocked 3+ 次：

```bash
# 1. 读卡确认 attempt 状态
manager workboard read --id <card_id>

# 2. 如果 attempt 状态是 running（Dx 误判），unblock
workboard_unblock

# 3. 如果 attempt 状态是 blocked（真失败），retry
manager workboard retry --id <card_id>        # v3.0.1 新增 CLI
```

**预防**：代理 claim 后立即 `workboard_heartbeat` 续约，避免 claim token 过期被 Dx 误判。

---

## 八、禁止行为（v3.0.1 版）

1. **一个任务只艾特一个代理**——不得在同一条消息中艾特多个代理
2. **禁止私信汇报**——进度反馈走 workboard，不私聊
3. **禁止私信核验**——大管家核验在群里发简短确认，不私聊
4. **禁止用 Dashboard 的"开始"按钮**——必须用 CLI
5. **不要重复发 IM 模板**——只一个模板
6. **不要在 create 后手动 move 到 todo**——Dx 自动
7. **不要在 agent 执行中用群消息发进度**——走 workboard
8. **不要把 workboard 当 TODO 平替**——各管一段
9. **中间文件放 temp/，不放 knowledge/**——知识沉淀才放 knowledge/
10. **卡 notes / IM 模板的文件路径必须绝对路径**

---

## 九、版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 3.1.0 | 2026-06-06 00:55 | **新增私聊派发场景**（老板 2026-06-06 拍板）：用户 DM 交任务时，大管家走 “建卡 + sessions_spawn + 验收” 3 步（不写 TODO、不艾特群）；workboard 仍是任务进度控制面（建卡 + 验收），派发动作（IM 群艾特 / sessions_spawn）由大管家手动做，**不**走 workboard CLI |
| 3.0.1 | 2026-06-03 03:05 | **老板定型**：(1) IM 群艾特必须（纠正 v3.0.1 草案"可选"）；(2) 任务进度反馈走 workboard（proof+comment）；(3) start 保留但不主动调；(4) 中间文件放 temp/，不放 knowledge/；(5) 采纳 A/B/C/E 提议，撤回 D；(6) 新增 --no-dup 防重复建卡 |
| 3.0.0 | 2026-06-03 02:39 | 基于 T001.1 端到端测试定型：5+1 步 → 3 步派发；Dx 自动行为；代理汇报 |
| 2.3.0 | 2026-06-03 | TODO 7 字段定型 |
| 2.2.0 | 2026-06-03 | 5+1 步新流程 |
| 2.0.0 | 2026-05-21 | task-guide.md v2.0 |

*最后更新：2026-06-06 00:55*
*v3.1.0 新增者：大管家（steward）*
*v3.0.1 定稿者：老板（杨权）*
