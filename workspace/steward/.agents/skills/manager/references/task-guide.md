# 任务派发指南

> 当需要给团队中的其他 AI 代理分配任务时，使用本指南。
> **v2.1 重大修正**：IM 不是"备选"而是与 Workboard **并行的可见层**。Workboard 是数据层，IM 群是给老板看流程的窗口，艾特是后台交互的进度播报。

---

## 一、任务派发的本质

任务派发不是"转发消息"，而是**传递清晰的约束、输入和产出**。子代理根据这些信息自主决定执行方式。

大管家在派发任务时只做三件事：
- 说明使用什么技能
- 说明输入什么文件、输出什么文件
- 说明任务目标是什么

具体怎么执行，由子代理自行判断。

---

## 二、双层架构：数据层 + 可见层

任务派发由**两个并行层**组成，缺一不可：

| 层 | 职责 | 工具 | 谁看 |
|----|------|------|------|
| **数据层** | 结构化跟踪、状态机、证据沉淀、claim/heartbeat 互斥 | Workboard（看板） | 大管家、子代理 |
| **可见层** | 让老板在群里看到流程进度和后台交互 | 飞书 IM 群消息 | 老板、群友 |

**数据层是真相源**（老板不点 Dashboard 也行），**可见层是信息流**（老板不读 Workboard 也行）。两个层必须保持同步。

### 双层分工

| 场景 | 数据层（Workboard） | 可见层（IM 群） |
|------|---------------------|----------------|
| 派发新任务 | `manager workboard create` 建卡 | 群里 @ 目标代理，告知 task_id |
| 子代理认领 | `workboard_claim`（自动 `todo → running`） | 群里 @ 目标代理 播报"已认领" |
| 进度更新 | `workboard_heartbeat` + `workboard_comment` | 重要节点在群里同步（如"卡在 X 依赖上"） |
| 任务完成 | `workboard_release --status done` | 群里 @ 大管家 汇报产出 + proof |
| 阻塞 | `move --status blocked` | 群里 @ 大管家 求助 |
| 归档 | `manager workboard archive` | 群里简短确认"已归档 task_id" |

**原则**：数据层有动作 → 可见层必有同步。**老板不看 Dashboard 也必须在 IM 流里看到全部进度。**

---

## 三、IM 群消息规范

### 1. 艾特格式（@ 代理）

飞书消息中 @ 代理必须使用 **user_id + user_name** 双字段，且**严禁 \n 换行**：

```xml
<at user_id="ou_xxx">代理姓名</at>
```

✅ 正确：
```
<at user_id="ou_a4bc01a3736e458817235a94124d340c">programmer</at> 请认领任务
```

❌ 错误（缺 user_name）：
```
<at user_id="ou_a4bc01a3736e458817235a94124d340c"></at> 请认领任务
```

❌ 错误（缺 user_id 或在 user_id 字段中夹换行）：
```
<at user_id="ou_xxx
">name</at> 请认领
```

**@ 提及只能用于群通知**（让老板/群友看到进度）。任务派发本身可以在私聊，但**群通知不可省**。

### 2. 群通知模板（每个 Workboard 事件）

#### 2.1 派发新任务时

```text
📋 新任务派发 [{{task_id}}]

<at user_id="{{assignee_open_id}}">{{assignee}}</at>

任务：{{task_title}}
优先级：{{priority}}
标签：{{labels}}

请认领：
  manager workboard claim --id {{task_id}} --owner {{assignee}} --ttl 120
```

#### 2.2 子代理认领时（@ 老板可见）

```text
<at user_id="{{assignee_open_id}}">{{assignee}}</at> 已认领 [{{task_id}}]
- TTL: 120s
- 开始时间: {{ts}}
```

#### 2.3 重要节点 / 续约失败 / 阻塞

```text
⚠️ [{{task_id}}] {{assignee}} 续约失败 / claim 过期
- 原因: {{reason}}
- 当前状态: {{status}}
- 处理: {{action}}
```

#### 2.4 任务完成

```text
✅ [{{task_id}}] {{assignee}} 任务完成
- 产出: {{output}}
- proof: {{proof_url}}
- 状态: done
```

#### 2.5 归档

```text
📦 [{{task_id}}] 已归档
```

### 3. 占位符表（群通知）

| 占位符 | 说明 | 例子 |
|--------|------|------|
| `{{task_id}}` | Workboard 卡片 ID | `2337ee4b-...` |
| `{{task_title}}` | 任务标题 | `ch12 文献检索` |
| `{{assignee}}` | 目标代理名 | `psychologist` |
| `{{assignee_open_id}}` | 代理的飞书 open_id | `ou_c1a8fc008307a0385a2fcd3c0ca6b71b` |
| `{{priority}}` | 优先级 | `high` |
| `{{labels}}` | 标签 | `ch12,文献检索` |
| `{{ts}}` | ISO 时间戳 | `2026-06-02 13:45:00` |
| `{{reason}}` / `{{action}}` | 错误原因 / 后续动作 | `claim 过期` / `等待重新认领` |
| `{{output}}` | 产出文件路径 | `wiki/sources/ch12-literature.md` |
| `{{proof_url}}` | 证明链接 | Dashboard URL |

---

## 四、Workboard 派发流程（数据层）

### 1. 派发前准备

- 目标代理的角色定义文件（`.agents/agents/{{assignee}}.md`）是否存在
- 输入文件是否就位
- 任务边界条件（验收标准 + 禁止事项）是否明确
- **目标代理的飞书 open_id**（在群消息中搜索历史消息提取）

### 2. 建卡（manager 创建任务卡）

```bash
manager workboard create \
  --title "{{task_title}}" \
  --notes "{{task_notes}}" \
  --priority {{priority}} \
  --labels "{{labels}}" \
  --assignee {{assignee}}
```

| 占位符 | 必填 | 例子 |
|--------|------|------|
| `{{task_title}}` | ✅ | `ch12 个案研究法 - 文献检索` |
| `{{task_notes}}` | ❌ | `检索近5年核心中英文文献，整理到 wiki/sources/ch12-literature.md` |
| `{{priority}}` | ❌ | `low` / `normal` / `high` / `urgent`（默认 normal） |
| `{{labels}}` | ❌ | `ch12,psychologist,文献检索`（逗号分隔） |
| `{{assignee}}` | ❌ | `psychologist` |

**返回值**：卡片 ID，记为 `{{task_id}}`。

### 3. 同步到群（IM 通知）

按 **2.1 派发新任务时** 的模板发给目标群。

### 4. 子代理执行（认领 → 续约 → 评论 → 释放）

子代理使用 **agent 原生工具**（无需 CLI）：

```python
# 1. 认领（独占此卡，状态自动 todo → running）
workboard_claim(id="{{task_id}}", ttlSeconds=120)
# → 返回 token: {{token}}

# 2. 续约（每 60-90s 一次，防 claim 过期）
workboard_heartbeat(id="{{task_id}}", token=*** note="{{heartbeat_note}}")

# 3. 评论（重要节点、问题求助、阶段汇报）
workboard_comment(id="{{task_id}}", body="{{comment_body}}")

# 4. 释放（任务完成 / 阻塞 / 终止）
workboard_release(id="{{task_id}}", token=*** status="{{final_status}}")
#   状态选项: done / blocked / todo（释放回 backlog）
```

**证明**（重要产出 / 测试结果）：

```python
workboard_proof(
    id="{{task_id}}",
    status="passed",            # passed / failed / skipped / unknown
    label="{{proof_label}}",
    command="{{proof_command}}",
    url="{{proof_url}}",
    note="{{proof_note}}",
)
```

### 5. 大管家闭环（跟踪 + 群同步 + 归档）

```bash
# 数据层
manager workboard list --assignee {{assignee}}
manager workboard read --id {{task_id}}
manager workboard archive --id {{task_id}}
```

**可见层同步**：每一步操作都要在群里有对应消息（按 §三 模板）。

---

## 五、IM 派发（仅私聊，不在群）

当任务内容**不适合在群聊公开**（涉密、敏感、私人请求）时，**私聊**目标代理派发。但群通知仍需发出（脱敏版）：

```text
📋 任务派发（私聊进行中）

任务 ID: {{task_id}}
已私聊 @{{艾特代理}} 同步详情
```

---

## 六、禁止行为

| 禁止 | 原因 |
|------|------|
| ❌ 只在 Workboard 操作、不在群里同步 | 老板看不到流程 |
| ❌ 只在群里喊、不建 Workboard 卡片 | 没有结构化跟踪 |
| ❌ @ 代理时只写 user_name 不写 user_id | 飞书解析失败 |
| ❌ @ 代理的 user_id 字段里夹 \n | 飞书解析失败 |
| ❌ 用 IM 派发长任务/多代理/需要证据的任务（同时没用 Workboard） | 流式消息易丢 |
| ❌ 同一条消息艾特多个代理 | 责任不清 |
| ❌ 私聊汇报任务完成 | 必须群聊留痕 |
| ❌ 任务完成后不归档 | Dashboard 越来越乱 |
| ❌ 任务不写 `--notes` / `--labels` | 子代理无法理解边界 |

---

## 七、占位符约定

本文档所有 `{{xxx}}` 占位符在使用时**必须替换**为实际值。

### 数据层占位符（Workboard 派发）

| 占位符 | 含义 |
|--------|------|
| `{{task_title}}` | 卡片标题 |
| `{{task_notes}}` | 卡片描述 |
| `{{priority}}` | low / normal / high / urgent |
| `{{labels}}` | 标签（逗号分隔） |
| `{{assignee}}` | agentId |
| `{{task_id}}` | 卡片 ID（建卡后获得） |
| `{{token}}` | claim 返回的 token |
| `{{heartbeat_note}}` | 续约时的进度备注 |
| `{{comment_body}}` | 评论正文 |
| `{{final_status}}` | 释放时的目标状态 |
| `{{proof_label}}` / `{{proof_command}}` / `{{proof_url}}` / `{{proof_note}}` | proof 字段 |

### 可见层占位符（IM 群消息）

| 占位符 | 含义 |
|--------|------|
| `{{assignee_open_id}}` | 目标代理的飞书 open_id（**@ 提及必须用**） |
| `{{艾特代理}}` | 同上，旧名保留兼容 |
| `{{ts}}` | ISO 时间戳 |
| `{{output}}` | 产出文件路径 |
| `{{reason}}` / `{{action}}` | 错误上下文 |

### 旧占位符（v1.0 IM 派发，保留兼容）

`{{task_desc}}` / `{{agent_role}}` / `{{subtask}}` / `{{任务目标}}` / `{{任务约束}}` / `{{input_file}}` / `{{output_file}}`

---

## 八、状态机

```
backlog ──→ todo ──→ running ──→ done ──→ archived
                 ↑      │
                 │      ↓
                 │   blocked ──→ unblocked → running
```

| 状态 | 含义 | 进入方式 |
|------|------|----------|
| `backlog` | 储备池 | `create --status backlog` |
| `todo` | 待办 | `create`（默认） |
| `running` | 进行中 | `claim`（自动）/ `move --status running` |
| `blocked` | 阻塞 | `move --status blocked` |
| `done` | 完成 | `release --status done` |
| `archived` | 归档 | `archive` |

---

## 九、任务完成后的闭环

子代理的 proof 或 IM 汇报必须包含：
1. **完成的是什么任务**（引用 task_id 或任务标题）
2. **产出是什么**（文件路径 / 链接 / commit hash）

大管家收到后：
1. 更新 TODO.md（状态 → done 或 blocked）
2. 在群聊向老板汇报（带可验证的链接 + 群通知模板 §三.2.4）
3. Workboard 卡片归档（`manager workboard archive`）
4. 重要产出 push 到 git（development 或 main 分支）

---

*详见 [Workboard 详细指南](workboard-guide.md)*

*版本：v2.1 - 2026-06-02 - 修正双层架构（Workboard 数据层 + IM 可见层）*
