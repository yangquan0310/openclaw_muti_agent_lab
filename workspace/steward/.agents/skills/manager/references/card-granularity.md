---
name: card-granularity
description: workboard 卡片粒度规范 — 混合 L1/L2/L3 三层模式
version: 1.0.0
author: Yang Quan
created: 2026-08-04
---

# workboard 卡片粒度规范（混合 L1/L2/L3 模式）

> **老板 2026-08-04 11:32 拍板**：以后 workboard 卡片粒度 = **混合模式**（一项目一卡 + 阶段/任务子卡按需），**不**用单一粗粒度（一项目一卡）或单一细粒度（一任务一卡）。

---

## 一、三层架构概览

| 层级 | 名称 | 粒度 | 建卡时机 | 谁看 |
|---|---|---|---|---|
| **L1** | **项目卡** | 1 张 / 项目 | 立项时 | 老板 / 大管家 |
| **L2** | **阶段卡** | 3-5 张 / 项目 | 立项后立即 | 大管家 |
| **L3** | **任务卡** | 按需（任务太长或子代理边界模糊时拆）| 派发时 | worker / 大管家 |

---

## 二、每层详细规范

### L1 项目卡（1 张 / 项目）

**作用**：项目级"看板主卡"，老板一眼看到所有项目状态。

**必填字段**：
- `title`：项目名（如「博士论文 - 跨期选择的年龄差异」）
- `notes`：项目背景 + 项目目标 + 验收标准
- `status`：`active`（立项）/ `done`（完结）/ `archived`（长期搁置）
- `priority`：`high` / `normal` / `low`
- `agentId`：`steward`（项目卡是元数据卡，不分派具体代理）
- `labels`：项目类型标签（如 `thesis` / `manuscript-polish` / `recruitment` / `audit`）
- `boardId`：默认 `default`，项目专项看板可独立建（如 `thesis-intertemporal-age`）
- `skills`：项目用到的技能（如 `["research-assistant", "apaquarto-pdf"]`）

**何时关卡**：项目整体完结 → `status=done` + 写 `summary`。

**示例**：
```json
{
  "title": "博士论文 - 跨期选择的年龄差异",
  "notes": "立项于 2026-05；目标：完成 ch1-ch19 + Quarto 范式 ④ apaquarto 排版。\n验收：19 章 + docs/记忆机制的认知推断.pdf + 答辩通过。",
  "status": "active",
  "priority": "high",
  "agentId": "steward",
  "labels": ["thesis", "apaquarto-pdf", "long-term"],
  "boardId": "thesis-intertemporal-age",
  "skills": ["research-assistant", "apaquarto-pdf"]
}
```

---

### L2 阶段卡（3-5 张 / 项目）

**作用**：项目内的主要阶段拆分（如文献综述 / 数据收集 / 数据分析 / 论文撰写 / 投稿修改），大管家追踪子阶段进度。

**必填字段**：
- `title`：阶段名（如「文献综述 v4」「数据收集」）
- `notes`：阶段目标 + 输入路径 + 输出路径 + 验收标准
- `status`：`todo` / `ready` / `running` / `done` / `blocked`
- `priority`：继承项目卡 / 按需调整
- `agentId`：阶段主负责代理（如 `psychologist` 做综述 / `programmer` 做数据收集）
- `parents`：**L1 项目卡 ID**（关键！建立层级关系）
- `labels`：阶段标签 + 父项目标签
- `boardId`：继承项目卡

**何时建卡**：立项后**立即**建好所有 L2 卡（先全部 `status=todo`，避免后期漏建）。

**何时关卡**：阶段完成 → `status=done` + 写 `summary`，**不**关闭项目卡。

**示例**：
```json
{
  "title": "文献综述 v4",
  "notes": "基于 research-assistant/SKILL.md v5.x 重新做综述。\n输入：knowledge/review/跨期选择的年龄差异_v3.md（v3 基础）\n输出：knowledge/review/跨期选择的年龄差异_v4.md（≥30KB / 295 行）\n验收：v4 ≥ 30KB + 含跨期选择 5 流派对比表 + 引文 ≥ 50 篇。",
  "status": "done",
  "priority": "high",
  "agentId": "psychologist",
  "parents": ["<L1_项目卡_ID>"],
  "labels": ["thesis", "literature-review", "manuscript-polish"],
  "boardId": "thesis-intertemporal-age"
}
```

---

### L3 任务卡（按需）

**作用**：当 L2 阶段卡**单卡过重**（如"论文撰写"涵盖 19 章）或**子代理边界模糊**时，按需拆为 L3 任务卡。

**触发条件**（满足任一即建 L3）：
1. L2 卡 `notes` 里同时涵盖 3+ 个独立子任务
2. 派发时子代理明确要求拆分（如"这个太大了，先做 ch5"）
3. 阶段需要分批派发（如 v1→v7 严格串行的 7 阶段流水线）
4. 大管家**自己**感觉到追踪粒度不够

**必填字段**：
- `title`：具体任务名（如「ch14 量的研究与质的研究的整合 v2 内容框架」）
- `notes`：任务四要素（目标/约束/输入/输出）
- `status`：`backlog` / `ready` / `running` / `done` / `blocked`
- `priority`：继承阶段卡
- `agentId`：派发的具体代理
- `parents`：**L2 阶段卡 ID**（关键！）
- `labels`：继承 + 任务类型
- `boardId`：继承

**何时建卡**：派发时建（**不**像 L2 提前批量建）。

**示例**：
```json
{
  "title": "ch14 v2 内容框架（instructor）",
  "notes": "任务目标：完成 ch14 量的研究与质的研究的整合 v2 内容框架\n任务约束：按 HANDBOOK v1.0.5 7 阶段流水线 v2 模板\n输入路径：/root/.openclaw/repository/教育科学研究方法/HANDBOOK.md\n输出路径：/root/.openclaw/repository/教育科学研究方法/ch14/v2_内容框架.md\n验收标准：含 6 节骨架 + 各节 ≥ 200 字 + 与 v1 需求分析对应。",
  "status": "ready",
  "priority": "high",
  "agentId": "instructor",
  "parents": ["<L2_阶段卡_ID>"],
  "labels": ["thesis", "course-prep", "ch14", "v2"],
  "boardId": "course-jiaoyu-keyan"
}
```

---

## 三、workboard 工具使用

### 建卡（统一用 `workboard_create` agent tool）

```javascript
// L1 项目卡
workboard_create({
  title: "...",
  notes: "...",
  status: "active",
  agentId: "steward",
  labels: ["..."],
  boardId: "..."
})

// L2 阶段卡（关键：parents 指向 L1）
workboard_create({
  title: "...",
  notes: "...",
  status: "todo",
  agentId: "psychologist",
  parents: ["<L1_项目卡_ID>"],
  labels: ["..."],
  boardId: "..."
})

// L3 任务卡（关键：parents 指向 L2）
workboard_create({
  title: "...",
  notes: "...",
  status: "ready",
  agentId: "instructor",
  parents: ["<L2_阶段卡_ID>"],
  labels: ["..."],
  boardId: "..."
})
```

### 追踪

```javascript
// 看单个项目全貌
workboard_read({ id: "<L1_项目卡_ID>" })

// 看项目所有阶段
workboard_list({ boardId: "<项目看板>" })

// 看阶段所有任务
workboard_read({ id: "<L2_阶段卡_ID>" })  // 详情里有 childCardIds
```

---

## 四、判断标准速查（建卡前自检）

| 情况 | 选哪层 |
|---|---|
| 老板布置了一个新项目 | **L1 项目卡**（1 张）|
| 项目立项，需要拆主要阶段 | **L2 阶段卡**（3-5 张，全部建好 `todo`）|
| L2 阶段卡涵盖 3+ 子任务 | 拆 **L3 任务卡** |
| 派发时子代理明确说"这个太大" | 拆 **L3 任务卡** |
| 项目需要分批严格串行（如 v1→v7）| 拆 **L3 任务卡**（每轮 1 卡）|
| 大管家自己觉得追踪粒度不够 | 拆 **L3 任务卡** |
| 1 次性 1 个小任务（如"读 30 篇论文"）| **L3 任务卡**（不需要 L2）|

---

## 五、派发与混合模式关系

| 派发模式 | 适用于 | 与 L1/L2/L3 关系 |
|---|---|---|
| **群派发**（IM 5 段艾特）| 群里代理需看到/知道 | 通常对应 L3 任务卡 |
| **dispatch 派发**（`openclaw workboard dispatch` CLI）| 机器自动启动 + 不需要人看 | 通常对应 L3 任务卡 |
| L1 / L2 卡 | **不**直接派发 | 只做元数据 + 追踪（status/done 反映进度）|

**L3 任务卡**才是真正派发的对象；L1/L2 是追踪层级。

---

## 六、迁移建议（已有卡片的项目）

**对老板已有项目**（如博士论文 1 个项目 + 13 张零散卡）：

1. **盘点现有卡片**：`workboard_list({ boardId: "<项目看板>" })`
2. **建 L1 项目卡**（如还没有）
3. **对现有卡片分组**（按阶段），把每组第一张卡的 `parents` 设为 L1（或建 L2 阶段卡作为中转）
4. **建 L2 阶段卡**（每阶段 1 张，notes 里列本阶段所有 L3 子卡的 ID）
5. **现有 L3 任务卡**的 `parents` 从「无」或「L1」改为「L2」

**迁移是可选的**——已有项目**不**强制迁移到三层；只在**新项目**严格执行。

---

## 七、变更历史

| 版本 | 日期 | 更新内容 |
|---|---|---|
| v1.0.0 | 2026-08-04 | 初版。老板拍板混合模式（L1 项目卡 + L2 阶段卡 + L3 任务卡按需）。|
