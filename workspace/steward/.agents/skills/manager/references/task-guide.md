# 任务派发指南

> 当需要给团队中的其他 AI 代理分配任务时，使用本指南。
> **v2.0 重大更新**：派发机制从 IM（飞书艾特）转向 Workboard（看板）。IM 派发仅保留为轻量场景的备选方案。

---

## 一、任务派发的本质

任务派发不是"转发消息"，而是**传递清晰的约束、输入和产出**。子代理根据这些信息自主决定执行方式。

大管家在派发任务时只做三件事：
- 说明使用什么技能
- 说明输入什么文件、输出什么文件
- 说明任务目标是什么

具体怎么执行，由子代理自行判断。

---

## 二、派发机制选择

| 场景 | 推荐机制 | 工具 |
|------|---------|------|
| **长任务**（>1 小时）/ **多代理接力** / **需要状态跟踪 + 证据沉淀** | ✅ **Workboard**（默认） | `manager workboard create` |
| **轻量短期任务**（<30 分钟、单代理、不需要后续跟踪） | IM 飞书艾特 | 飞书 @ 消息 |
| **老板临时一句话**（"看下 X"/"查下 Y"） | IM 飞书直接回答 | — |

**原则**：能用 Workboard 就不用 IM。Workboard 是结构化、留痕、可追责的；IM 是流式、易丢失、难聚合的。

---

## 三、Workboard 派发（默认流程）

### 1. 派发前准备

- 目标代理的角色定义文件（`.agents/agents/{{assignee}}.md`）是否存在
- 输入文件是否就位
- 任务边界条件（验收标准 + 禁止事项）是否明确

### 2. 建卡（manager 创建任务卡）

**`manager workboard create` 三段式调用**：

```bash
manager workboard create \
  --title "{{task_title}}" \
  --notes "{{task_notes}}" \
  --priority {{priority}} \
  --labels "{{labels}}" \
  --assignee {{assignee}}
```

| 占位符 | 说明 | 必填 | 例子 |
|--------|------|------|------|
| `{{task_title}}` | 任务标题（一句话） | ✅ | `ch12 个案研究法 - 文献检索` |
| `{{task_notes}}` | 任务描述（背景 + 范围） | ❌ | `检索近5年核心中英文文献，整理到 wiki/sources/ch12-literature.md` |
| `{{priority}}` | `low` / `normal` / `high` / `urgent` | ❌ | `high` |
| `{{labels}}` | 逗号分隔的标签 | ❌ | `ch12,psychologist,文献检索` |
| `{{assignee}}` | 目标代理名（agentId） | ❌ | `psychologist` |

**返回值**：卡片 ID，记为 `{{task_id}}`。

### 3. 通知目标代理（飞书 IM 同步）

```text
📋 新任务已派发到 Workboard

@{{艾特代理}}

请打开 Workboard 认领并开始：
- 任务 ID: {{task_id}}
- 标题: {{task_title}}
- 优先级: {{priority}}

认领命令（你自己用 agent 工具或 CLI 跑）：
  manager workboard claim --id {{task_id}} --owner {{assignee}} --ttl 120
```

### 4. 子代理执行（认领 → 续约 → 评论 → 释放）

子代理（目标 agent）使用 **agent 原生工具**（无需 CLI）：

```python
# 1. 认领（独占此卡）
workboard_claim(id="{{task_id}}", ttlSeconds=120)
# → 返回 token: {{token}}

# 2. 续约（每 60-90s 一次，防 claim 过期）
workboard_heartbeat(id="{{task_id}}", token="{{token}}", note="进度说明")

# 3. 评论（重要节点、问题求助、阶段汇报）
workboard_comment(id="{{task_id}}", body="{{comment_body}}")

# 4. 释放（任务完成 / 阻塞 / 终止）
workboard_release(id="{{task_id}}", token="{{token}}", status="done")
#   状态选项: done / blocked / todo（释放回 backlog）
```

**证明**（重要产出 / 测试结果）：

```python
workboard_proof(
    id="{{task_id}}",
    status="passed",            # passed / failed / skipped / unknown
    label="v7 终稿审核通过",
    command="manager workboard audit ./",
    url="http://10.0.0.9:18098/estqvr/card/{{task_id}}",
    note="沉淀到 wiki/sources/..."
)
```

### 5. 大管家闭环（跟踪 + 汇报老板）

```bash
# 大管家查看进度
manager workboard list --assignee {{assignee}}
manager workboard read --id {{task_id}}

# 任务完成后归档
manager workboard archive --id {{task_id}}
```

大管家收到子代理的 proof 后：
1. 在群聊中向老板汇报（带 task_id 链接）
2. 更新 TODO.md（任务状态 → done）
3. 归档卡片（保持 Dashboard 干净）

---

## 四、IM 派发（备选方案，仅限轻量场景）

**适用**：单代理短任务（<30 分钟）、不需要后续跟踪、不需要证据沉淀。

在飞书群聊中直接艾特目标代理发送（一个任务只艾特一个代理）：

```
{{task_desc}}

{{艾特代理}}

📋 前置要求：
- 明确自己的角色：{{agent_role}}，找到对应的 .agents/agents/{{agent}}.md 阅读
- 查看 TODO.md 中的 {{subtask}} 子任务

🎯 任务目标：
- {{任务目标}}

📌 任务约束：
- {{任务约束}}

📁 输入文件：
- {{input_file}}

📄 输出文件：
- {{output_file}}

💬 反馈：
- 完成后在群聊中艾特大管家汇报
- 汇报内容：完成的是什么任务
- 汇报内容：产出是什么（文件路径）
```

| 参数 | 说明 |
|------|------|
| `{{task_desc}}` | 任务描述，一句话说明要做什么 |
| `{{agent_role}}` | 目标代理的角色名称 |
| `{{subtask}}` | TODO.md 中的子任务名称 |
| `{{任务目标}}` | 任务要达成的具体目标 |
| `{{任务约束}}` | 边界条件、禁止事项 |
| `{{input_file}}` | 输入文件路径 |
| `{{output_file}}` | 输出文件路径 |

---

## 五、禁止行为

| 禁止 | 原因 |
|------|------|
| ❌ 同一条消息艾特多个代理 | 任务责任不清 |
| ❌ 私聊汇报任务完成 | 必须群聊留痕 |
| ❌ 用 IM 派发长任务/多代理/需要证据的任务 | 应该用 Workboard |
| ❌ 跳过 Workboard 直接让子代理干 | 没有卡片 → 没有跟踪 → 没有证据 |
| ❌ 任务完成后不归档 | Dashboard 会越来越乱 |
| ❌ 任务不写 `--notes` | 子代理无法理解边界 |
| ❌ 任务不写 `--labels` | 后续无法按项目/类型聚合 |

---

## 六、任务完成后的闭环

子代理的 proof 或 IM 汇报必须包含：
1. **完成的是什么任务**（引用 task_id 或任务标题）
2. **产出是什么**（文件路径 / 链接 / commit hash）

大管家收到后：
1. 更新 TODO.md（状态 → done 或 blocked）
2. 在群聊向老板汇报（带可验证的链接）
3. Workboard 卡片归档（`manager workboard archive`）
4. 重要产出 push 到 git（development 或 main 分支）

---

## 七、Workboard 卡片状态机

```
backlog ──→ todo ──→ running ──→ done ──→ archived
                 ↑      │
                 │      ↓
                 │   blocked ──→ unblocked → running
                 ↓
              (claim 自动 todo → running)
```

| 状态 | 含义 | 进入方式 |
|------|------|----------|
| `backlog` | 储备池，未启动 | `create --status backlog` |
| `todo` | 待办 | `create`（默认） |
| `running` | 进行中 | `claim`（自动）/ `move --status running` |
| `blocked` | 阻塞（等待依赖） | `move --status blocked` |
| `done` | 完成 | `release --status done` |
| `archived` | 归档（不显示在主面板） | `archive` |

---

## 八、占位符约定

本文档所有 `{{xxx}}` 占位符在使用时**必须替换**为实际值。已固定的 8 个占位符（沿用 v1.0）：

`{{task_desc}}` / `{{艾特代理}}` / `{{agent_role}}` / `{{subtask}}` / `{{任务目标}}` / `{{任务约束}}` / `{{input_file}}` / `{{output_file}}`

新增的 8 个占位符（Workboard 派发）：

`{{task_title}}` / `{{task_notes}}` / `{{priority}}` / `{{labels}}` / `{{assignee}}` / `{{task_id}}` / `{{token}}` / `{{comment_body}}`

---

*详见 [Workboard 详细指南](workboard-guide.md)*

*版本：v2.0 - 2026-06-02 - 派发机制从 IM 转向 Workboard*
