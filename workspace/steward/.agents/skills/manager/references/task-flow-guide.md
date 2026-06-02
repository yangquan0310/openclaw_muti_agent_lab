# 任务流指南 v2.2

> **合并自三件套**（2026-06-03 v2.2）：
> - `task-guide.md`（派发模板、找 open_id、IM 艾特）
> - `task-lifecycle-standards.md`（task.* 工具流程、调节清单）
> - `task-progression-standards.md`（文件传递、TODO 任务树规范）
>
> **v2.2 重大更新**：5+1 步新派发流程（IM 艾特 + workboard claim + start + 核验），三件套架构（TODO 纪律 + workboard 执行 + IM 可见）

---

## 一、心智模型（三件套架构）

```
老板交任务
    ↓
[纪律层] 大管家写 TODO.md（人可读看板）
    ↓
[执行层] 大管家建 workboard 卡（机器可执行）
    ↓
[可见层] 大管家 IM 群艾特代理（开模板，workboard 信息在开头）
    ↓
代理 claim（插件工具 workboard_claim）
    ↓
大管家 start（CLI，claim 之后才调）
    ↓
代理执行（run 触发）
    ↓
代理执行完 → 群里发完成消息
    ↓
大管家核验 → workboard move → done / blocked
```

| 层级 | 工具 | 角色 | 谁用 |
|------|------|------|------|
| **纪律层** | `TODO.md` | 看板、状态记录 | 大管家 |
| **执行层** | `workboard` 卡片 | `start` 派发、状态机、运行轨迹 | 大管家 CLI（create/start/move）+ 代理插件工具（claim/heartbeat/release/proof） |
| **可见层** | **IM 群艾特** | 1 个通知模板（开头带 workboard 信息） | 大管家 |

**关键洞察**：三件套**缺一不可**——TODO 没纪律会失控，workboard 没 IM 群里看不到，IM 没 workboard 没结构化数据。

---

## 二、5+1 步派发流程

### 步骤 1：明确任务

回答三个问题：
- **任务目标**：一句话说清要干什么
- **指派对象**：哪个 agent（`writer` / `reviewer` / `psychologist` / ...）
- **优先级 + 标签**：`low/normal/high/urgent` + `labels`

### 步骤 2：写 TODO（大管家）

```markdown
- [ ] **T-001**：ch10 writer 草稿  [card={{card_id_占位}}]
  - 📄 约束目标：在 oc_983c895 群写 v1.0 ch10 草稿
  - 📄 输入：ch9 v2.0 + ch10 大纲
  - 📄 产出：ch10_v1.0.md
  - 📄 派发：writer（claim → start）
  - 📄 状态：⬜ 待认领
```

`[card={{card_id}}]` 是 workboard 引用（步骤 3 拿到 ID 后回填）。

### 步骤 3：建 workboard 卡（大管家 CLI）

```bash
manager workboard create \
  --title "ch10 草稿 v1.0" \
  --assignee writer \
  --priority high \
  --session 'agent:writer:feishu:group:oc_983c895ba1ddedcebda690213926d1b2' \
  --task-desc "..." \
  --agent-role writer \
  --goal "..." \
  --constraints "..." \
  --feedback "..."
```

**关键选项**：
- `--session X`：指定关联 session
- **不传 `--status` 时**：有 `--session` → 默认 `backlog`；无 → 默认 `todo`
- 想手动进 `todo`：`manager workboard move --id X --status todo`
- `--engine {codex,claude}` / `--model` 控制 execution

### 步骤 4：IM 群里艾特代理（大管家）

**IM 群艾特模板**（老板 2026-06-03 定型——**用于认领，不包目标/约束/输入/产出**）：
（目标/约束/输入/产出在 workboard 卡 notes 字段，见 cli.py `TASK_NOTES_TEMPLATE`）

```
{{task_desc}}

{{艾特代理}}

🔧 workboard 信息：
- card_id: {{card_id}}（短 8 位：{{card_short}}）
- session: {{sessionKey}}
- dashboard: {{card_url}}

📋 前置要求：
- 明确自己的角色：{{agent_role}}、找到对应的 .agents/agents/{{agent}}.md 阅读
- 查看并完善 TODO.md 中的 {{subtask}} 子任务

💬 反馈：任务领取后在群里艾特大管家汇报
```

**模板要点**（老板 2026-06-03 02:09 调整顺序）：
- **{{task_desc}} 抬头**——先说啥事
- workboard 信息**往下**——技术细节放后
- **只在认领阶段用**（代理认领后告知大管家）
- 目标/约束/输入/产出 → **不在群里发**，走 workboard 卡 notes 字段
- **只一个模板**（不拆派发/启动/完成多个）
- 后续状态变化由 workboard 自己管（Dx + dashboard），群里**不重复发**

### 步骤 5：等代理 claim

代理收到模板后：
1. 用 `workboard_claim` 插件工具认领
2. 群里回复 `已认领 card={{card_short}}`
3. 卡片 metadata.claim 写入

**大管家动作**：看到认领后，调 `manager workboard start`。

### 步骤 6：start（大管家 CLI，**只在 claim 之后**）

```bash
manager workboard start --id <card_id>
# 或强制指定 session：
manager workboard start --id <card_id> --session 'agent:writer:feishu:group:oc_xxx'
```

**start 内部做了什么**（v1.4.0+）：
1. 读卡 → 确认有 claim 或 --session 指定
2. 复用 session（不再新建）
3. **调 `chat.send` 触发新 run**（带 `idempotencyKey`）
4. 更新卡片：`status=running`, `execution.status=running`, `execution.runId=xxx`

**关键修复**：
- ❌ v1.4.0 之前：start 只改卡元数据，不触发 run（卡 = running 但 agent 一直不在群里）
- ✅ v1.4.0+：start 调 chat.send 真正触发 run

### 步骤 7：代理执行 + 完成反馈

代理在 session 里干活：
- `workboard_heartbeat` 续约
- `workboard_comment` 留评论
- 执行完用 `workboard_proof` 附产出
- **在群里发完成消息**（艾特大管家）

Dx 自动同步：run 完成后，卡从 `running` 移到 `review`。

### 步骤 8（核验）：大管家核验 + 归档

```bash
# 读卡看产出
manager workboard read --id <card_id>

# 核验通过：移到 done
manager workboard move --id <card_id> --status done

# 核验失败：移到 blocked
manager workboard move --id <card_id> --status blocked

# 归档（可选）
manager workboard archive --id <card_id>
```

**核验清单**：
- 产出文件是否存在（路径对照 task-desc 里的 output_file）
- 产出内容是否符合约束（goal + constraints）
- 是否有 proof 附件
- 完成后 TODO.md 对应行标注 ✅
- 群里发简短确认消息（不是模板，是大管家自己写）

---

## 三、任务状态映射（workboard ↔ TODO ↔ task 工具）

### workboard 状态机

```
   create
     ↓
   backlog   ← Dx 不会从 backlog 同步出去（推荐初始状态）
     ↓ (move to todo)
   todo       ← 已在群里艾特，等代理 claim
     ↓ (claim 写入 metadata)
   [claimed]  ← metadata 状态，不是卡片 status
     ↓ (start)
   running    ← chat.send 触发 run
     ↓ (run 完成)
   review     ← Dx 自动从 running 挪过来
     ↓
     ├─→ done      (大管家核验通过)
     ├─→ blocked   (大管家核验失败/超时)
     └─→ running   (重跑)
```

### TODO ↔ workboard 状态对应

| workboard 状态 | TODO 标记 | 含义 |
|---------------|-------------|------|
| `backlog` | ⬜ 待开始（未派发） | 刚 create，还没在群里艾特 |
| `todo` | ⬜ 待认领 | 已在群里艾特，等代理 claim |
| `running` | 🔄 进行中 | 代理已 start，run 触发 |
| `review` | 👀 待核验 | run 完成，大管家核验产出 |
| `done` | ✅ 已完成 | 大管家核验通过 |
| `blocked` | ❌ 阻塞 | 失败/超时，需人工介入 |

### task 工具 ↔ workboard（fallback）

workboard 不可用时回退到 task 工具：

| task 工具状态 | TODO 标记 | 说明 |
|--------------|-------------|------|
| draft | ⬜ 待开始 | 刚创建 |
| active | 🔄 进行中 | 执行中 |
| completed | ✅ 已完成 | 任务完成 |

**同步时序**：

| 场景 | TODO.md | workboard | task 工具 |
|------|---------|-----------|-----------|
| 大管家领取 | 添加主任务行 | `create --session X` | `task.create`（fallback） |
| 群里艾特 | 标记 ⬜ → 派发通知已发 | 状态保持 todo，等代理 claim | — |
| 代理 claim | 标记 ⬜ → ⏳ 已认领 | metadata.claim 写入 | — |
| 大管家 start | 标记 ⏳ → 🔄 | `manager workboard start` | `task.advance`（fallback） |
| 执行中 | 保持 🔄 | execution.status=running | `task.update` |
| 完成 | 保持 🔄（等核验） | Dx 自动 → review | `task.update → event.report → task.archive` |
| 核验 | 标记 🔄 → ✅ | `move --status done` | `task.update` |
| 出错 | 标记 🔄 → ❌ | `move --status blocked` | `task.update` |

完整同步规则见 [`sync-standards.md`](./sync-standards.md) v2.0。

---

## 四、TODO 任务树规范

### 任务格式（7 字段，老板 2026-06-03 定型）

**总字段数：7**（主任务和子任务都这 7 个；子任务额外有"负责人"为必填）。

| 字段 | 主任务 | 子任务 | 性质 |
|------|--------|--------|------|
| 任务 ID | ✅ | ✅ | 元数据 |
| 任务描述 | ✅ | ✅ | 元数据 |
| 负责人 | — | ✅ 必填 | 元数据（子任务专属） |
| **目标** | ✅ 必填 | ✅ 必填 | **4 必填内容字段** |
| **约束** | ✅ 必填 | ✅ 必填 | **4 必填内容字段** |
| **输入** | ✅ 必填 | ✅ 必填 | **4 必填内容字段** |
| **产出** | ✅ 必填 | ✅ 必填 | **4 必填内容字段** |
| 状态 | ✅ | ✅ | 元数据（从 workboard 同步） |
| workboard 引用 | 可选 | 可选 | 跨层引用（`[card=...]`） |

**核心原则（老板 2026-06-03 明确）**：
- 4 必填（目标/约束/输入/产出）= 子代理**必须**遵守的内容
- 其他字段 = 协调+追踪元数据，**不是子代理的具体任务流程**
- **TODO 不规定子代理 HOW，只规定 WHAT**——子代理收到"目标/约束/输入/产出"后，**自行决定执行方式**（文件传递/多步推进/工具选择等都不在 TODO 里规定）

### 主任务模板（大管家）

```markdown
- [ ] **T-001** 主任务描述  [card={{card_id}}]
  - 🎯 目标：...
  - 📌 约束：...
  - 📁 输入：...
  - 📄 产出：...
  - 📊 状态：⬜ 待开始
  - 📌 子代理分配：子代理 A、子代理 B（**不写子任务细节**，子代理自拆）
```

### 子任务模板（子代理自拆）

```markdown
- [ ] **T-001.1** 子任务描述  [card={{card_id}}]
  - 👤 负责人：writer
  - 🎯 目标：...
  - 📌 约束：...
  - 📁 输入：...
  - 📄 产出：...
  - 📊 状态：⬜ 待认领
  - （具体执行方式由子代理**自行决定**——TODO 不规定）
```

### 文件传递标注

```markdown
[T001] 任务描述          → /path/to/output.md
[T002] 任务描述          → /path/to/output2.md
```

完成后在 TODO 中标注：
```markdown
[T001] ✅ 已完成 → /path/to/output.md
```

---

## 五、文件传递机制

### 核心原则

| 原则 | 说明 |
|------|------|
| **任务即文件** | TODO 中每个任务对应一个文件 |
| **完成即文件完成** | 任务完成 = 文件编写完成 |
| **传递即推进** | 文件传给下一个代理 = 任务交接 |

### 推进流程

```
领取用户任务
    ↓
阅读项目 README 了解分工
    ↓
完善 TODO 任务树（每个任务对应一个文件）
    ↓
用户审核 TODO 任务树
    ↓
按文件传递推进任务
```

每步详解：
1. **领取任务**：用户提出需求 → 识别为项目任务 → 明确任务范围、交付物、截止时间 → 确认执行方式（直接执行 / 派发子代理）
2. **阅读项目文档**：README.md（了解目标、角色、当前状态）→ HANDBOOK.md（流水线、目录规范）→ metadata.json（确认版本）
3. **完善 TODO 任务树**：检查 TODO 完整性，有缺失任务或状态不准确时更新
4. **审核 TODO 任务树**（关键环节）：向用户展示更新后的 TODO，等待确认。用户提出修改则返回步骤 3
5. **按文件传递推进**：每个任务对应输出文件，代理完成任务 → 写入文件 → 更新 TODO 状态（标注文件路径）→ 通知下一个代理。循环直到所有任务完成

---

## 六、任务完成后的调节清单

任务完成后，如果过程中有值得记住的反思，需要调节到对应的文件中：

| 维度 | 文件 | 时机 |
|------|------|------|
| 自我认知/风格/信念 | SOUL.md | 有变化时 |
| 身份 | IDENTITY.md | 职责边界变化时 |
| 程序性记忆 | MEMORY.md | 新 If-Then 规则时 |
| 技能 | HANDBOOK.md | 流程规范更新时 |
| 协作规则 | AGENTS.md | 多代理规则变化时 |

**主任务更新**（大管家）：
1. 所有子任务完成
2. 大管家用 `task.update` 标记主任务状态
3. `event.report` 写事件报告
4. `task.archive` 归档

> ✅ 老板 2026-06-03 确认：`agent-self-development` 插件可用，`task.*` 工具**不退役**

详见 event-management 技能的「事件生成后的人格调节」章节。

---

## 七、禁止行为

1. **一个任务只艾特一个代理**，不得在同一条消息中艾特多个代理
2. **禁止私信汇报**：任务完成后，子代理必须在群聊中艾特大管家汇报，禁止私聊
3. **禁止用 Dashboard 的"开始"按钮**（v1.4.0 限制）：点"开始"会强制 `sessions.create` 覆盖卡上 sessionKey，必须用 CLI `manager workboard start`
4. **不要重复发 IM 模板**：状态变化由 workboard Dx 自动同步到 Dashboard，群里不重复通知
5. **不要新建多个 IM 通知模板**：只一个模板（开头带 workboard 信息），状态变化都靠它
6. **不要在 claim 之前 start**：先等代理 claim，再 start 触发 run（否则浪费一次会话）
7. **不要把 workboard 当 TODO 平替**：两者各管一段，TODO 纪律 + workboard 执行

---

## 八、版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 2.3.0 | 2026-06-03 | **审计修复**：(1) TODO 7 字段定型（4 必填内容字段 + 3 协调元数据 + 1 workboard 引用）；(2) 明确"TODO 不规定子代理 HOW，只规定 WHAT"；(3) task 工具确认可用（agent-self-development 插件，**不退役**） |
| 2.2.0 | 2026-06-03 | **重大升级**：合并三件套 → task-flow-guide.md；5+1 步新流程（IM 艾特 + workboard claim + start + 核验）；三件套架构（TODO + workboard + IM）；IM 模板（开头带 workboard） |
| 2.0.0 | 2026-05-21 | task-guide.md v2.0（派发模板、找 open_id、IM 艾特） |
| 3.0.0 | 2026-05-18 | task-progression-standards.md v3.0（TODO 任务树用户审核 + 文件传递） |
| 3.1.0 | 2026-05-18 | task-progression-standards.md v3.1（基于文件传递） |

*最后更新：2026-06-03*
