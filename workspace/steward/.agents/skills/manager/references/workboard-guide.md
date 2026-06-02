# Workboard 任务发布指南

> 当需要把任务发布到 OpenClaw Workboard 看板时使用本指南。
> 适用于**多 Agent 协作、跨会话跟踪、长期任务管理**等场景。

---

## 一、Workboard 是什么

OpenClaw Workboard 是 Dashboard 看板系统（http://10.0.0.9:18098/estqvr/），提供：

- **结构化任务卡片**（id / status / priority / labels / assignee / claim / proof）
- **认领 + 心跳 + 释放** 机制（防抢任务、防崩、防僵死）
- **SQLite 持久化**（重启不丢）
- **状态机**：`backlog → todo → running → review / blocked → done → archived`

**与 MEMORY.md 任务看板的区别**：

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

### ❌ 不必用

- 单 Agent 短期任务（一句话能说完的）
- 临时讨论、IM 问询
- 简单进度跟踪（MEMORY.md 够用）

---

## 三、能力边界（重要）

### Agent 工具集（我直接可用）

| 工具 | 用途 |
|------|------|
| `workboard_list` | 列卡 |
| `workboard_read` | 读卡 |
| `workboard_claim` | 认领（独占）|
| `workboard_heartbeat` | 续约（防 claim 过期）|
| `workboard_release` | 释放（指定下一状态）|
| `workboard_comment` | 评论 |
| `workboard_proof` | 附证据（artifact）|
| `workboard_unblock` | 解阻塞卡 |

### Gateway RPC（需走脚本）

| RPC 方法 | 用途 |
|---------|------|
| `workboard.cards.create` | 建卡 |
| `workboard.cards.update` | 改卡 |
| `workboard.cards.move` | 移动（看板拖拽）|
| `workboard.cards.delete` | 删卡 |
| `workboard.cards.archive` | 归档 |
| `workboard.cards.bulk` | 批量操作 |
| `workboard.cards.export` | 导出 |

**关键限制**：建/改/移/删/批量/归档 **不暴露为 agent 工具**，必须走 gateway RPC。

---

## 四、发布任务的标准流程

### 步骤 1：明确要发的任务

回答三个问题：
- **任务目标**：一句话说清要干什么
- **指派对象**：哪个 agent（`steward` / `psychologist` / `writer` / ...）
- **优先级 + 标签**：`low/normal/high/urgent` + `labels`

### 步骤 2：调用 CLI

```bash
# 通过 manager 统一入口
cd /root/.openclaw/workspace/steward/.agents/skills/manager/scripts
manager workboard <子命令> [选项]
```

**支持的子命令**：

```bash
# 建卡
manager workboard create \
  --title "ch12 个案研究法 - 文献检索" \
  --notes "检索近 5 年中英文核心文献" \
  --priority high \
  --labels "ch12,文献检索" \
  --assignee psychologist

# 列卡
manager workboard list --assignee psychologist
manager workboard list --status todo --limit 10

# 读卡
manager workboard read --id <card_id>

# 认领
manager workboard claim --id <card_id> --owner steward --ttl 120

# 认领 + 自动触发 execution（推荐）
# 修复合卡后 dashboard 仍显示「开始」按钮的 UX bug：
#   claim 只改 board.status（todo→running），不改 execution.status（仍 idle）
#   → dashboard 渲染时仍把 execution.idle 的卡当作「未开始」，所以还显示「开始」按钮
#   --auto-start 会用 update RPC 同步设置 execution.status=running
manager workboard claim --id <card_id> --owner steward --ttl 120 --auto-start

# 续约（带 token）
manager workboard heartbeat --id <card_id> --owner steward --token *** --note "进度说明"

# 评论
manager workboard comment --id <card_id> --body "评论内容"

# 释放（带 token）
manager workboard release --id <card_id> --owner steward --token *** --status done

# 归档
manager workboard archive --id <card_id>
```

**查看完整帮助**：
```bash
manager workboard --help
manager workboard create --help
```

### 步骤 3：跟踪卡片状态

```bash
# 通过 agent 工具跟踪
workboard_list --assignee psychologist
workboard_read <card_id>
```

### 步骤 4：完成后归档

```bash
# 任务完成 → 移到 done → 归档
wb-rpc.mjs move --id <card_id> --status done
wb-rpc.mjs archive --id <card_id>
```

---

## 五、设备身份认证（首次使用）

首次调用 `manager workboard` 时会自动触发 **device pairing flow**：

1. Python 脚本自动生成 Ed25519 密钥对
2. 用私钥签名 connect 握手
3. gateway **自动批准** CLI 设备配对（无需手动操作）
4. scopes 自动获取 `operator.admin`

**配对过程全自动**。CLI 模式下 gateway 自动批准设备，无需在 Dashboard 手动操作。

---

## 六、常见错误与排查

| 错误 | 原因 | 解决 |
|------|------|------|
| `missing scope: operator.admin` | 设备未配对 / scopes 不足 | 批准设备配对 |
| `claim ownerId is required` | 调 claim 没传 ownerId | 必传 `ownerId` 参数 |
| `card already claimed by X` | 已被其他 agent 认领 | 等释放或换一张卡 |
| `claim token does not match` | 续约/释放的 token 错了 | 用 claim 返回的 token |

---

## 七、与其他工具的协作

### 与 TODO.md 配合

```markdown
## 当前活跃任务看板

| T042 | OpenClaw 版本检查 | ... | 状态：active |
```

**Workboard 卡片**是 TODO.md 的**结构化延伸**：
- TODO.md：轻量记事（人看）
- Workboard：结构化跟踪（系统看）

**规则**：重要任务在两边都登记。TODO.md 写摘要，Workboard 写详情和 proof。

### 与 IM 派发配合

派发任务的两种方式：

| 方式 | 适用场景 |
|------|----------|
| IM 艾特（轻量）| 单次短任务、不需要跟踪 |
| Workboard 卡片（重量）| 多人协作、长任务、需要留痕 |

**不要重复**：要么 IM 派，要么建卡派，不要同时发两边。

---

## 八、版本历史

| 版本 | 日期 | 更新 |
|------|------|------|
| 1.1.0 | 2026-06-02 | **Python 迁移**：脚本从 Node.js (wb-rpc.mjs) 迁移至 Python 包 (`scripts/workboard/`)，CLI 统一入口 `manager workboard <子命令>`。设备身份配对改为自动批准。 |
| 1.2.0 | 2026-06-02 | **修复 UX bug**：新增 `claim --auto-start` 选项，claim 后自动设置 `execution.status=running`（避免 dashboard 仍显示「开始」按钮）。烟测验证：execution.status 从 idle 成功改为 running |
| 1.0.0 | 2026-06-02 | 初始版本：明确 workboard 任务发布的标准流程（基于烟测验证） |
