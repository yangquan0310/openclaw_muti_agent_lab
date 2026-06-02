# TODO ↔ 任务工具 ↔ workboard 同步规则 v2.0

> 大管家追踪、TODO 看板、workboard 卡片之间的双向同步规则。
> 合并自 `sync-guide.md` + `sync-standards.md`（2026-06-03 v2.0），新增 TODO ↔ workboard 章节。

---

## 一、同步的本质

不同层各管一段，**真相只有一份**：
- `TODO.md`：人可读看板，老板快速看
- `workboard` 卡片：机器可执行，子代理追踪
- `task.*` 工具：workboard 不可用时的 fallback

三者的同步是**双向引用**，不是数据复制。每层都标注对其它层的引用 ID。

---

## 二、TODO.md ↔ workboard 同步（主用）

### 状态对应

| workboard 状态 | TODO 标记 | 含义 |
|---------------|-------------|------|
| `backlog` | ⬜ 待开始（未派发） | 刚 create，还没在群里艾特 |
| `todo` | ⬜ 待认领 | 已在群里艾特，等代理 claim |
| `running` | 🔄 进行中 | 代理已 start，run 触发 |
| `review` | 👀 待核验 | run 完成，大管家核验产出 |
| `done` | ✅ 已完成 | 大管家核验通过 |
| `blocked` | ❌ 阻塞 | 失败/超时，需人工介入 |

### 同步时序

| 场景 | TODO.md | workboard 卡片 |
|------|---------|-----------------|
| 大管家领取时 | 添加主任务行，备注 `card={{card_id}}` | `manager workboard create --session X` |
| 群里艾特代理 | 标记 ⬜ → 派发通知已发 | 状态保持 todo，等代理 claim |
| 代理 claim | 标记 ⬜ → ⏳ 已认领 | 卡片 metadata.claim 写入 |
| 大管家 start | 标记 ⏳ → 🔄 | `manager workboard start` |
| 代理执行中 | 保持 🔄 | execution.status=running |
| 代理完成 | 保持 🔄（等核验） | Dx 自动 todo → review |
| 大管家核验 | 标记 🔄 → ✅ | `manager workboard move --status done` |
| 出错 | 标记 🔄 → ❌ | `manager workboard move --status blocked` |

### TODO 行格式（带 workboard 引用）

```markdown
- [ ] **T-001**：ch10 writer 草稿  [card=2a967a38-47e1-4182-98f3-698a14c84a80]
  - 📄 约束目标：在 oc_983c895 群写 v1.0 ch10 草稿
  - 📄 输入：ch9 v2.0 + ch10 大纲
  - 📄 产出：ch10_v1.0.md
  - 📄 派发：writer（claim → start）
  - 📄 状态：⬜ 待认领
```

`[card={{card_id}}]` 是 workboard 引用，便于从 TODO 跳到 Dashboard 查完整状态。

---

## 三、TODO.md ↔ task 工具同步（fallback）

> workboard 不可用时使用。

| task 工具状态 | TODO 标记 | 说明 |
|--------------|-------------|------|
| draft | ⬜ 待开始 | 刚创建 |
| active | 🔄 进行中 | 执行中 |
| completed | ✅ 已完成 | 任务完成 |

| 场景 | TODO.md | task 工具 |
|------|---------|-----------|
| 大管家领取时 | 添加主任务行 | `task.create` |
| 子代理领取时 | 添加子任务行 | `task.create` |
| 执行中 | 标记进度 | `task.advance` |
| 完成时 | 标记 ✅ | `task.update → event.report → task.archive` |

---

## 四、Wiki 同步（按需）

### 同步的本质

同步不是复制，而是**更新引用**。wiki 中的页面应该指向原始规范文件，而不是替代它。原始文件才是真相来源，wiki 只是索引。

### 同步时机

| 场景 | 是否同步 | 说明 |
|------|----------|------|
| 新增 SKILL 技能 | ✅ | 添加到 sources/ |
| 更新规范文档 | ✅ | 更新对应 wiki 页面 |
| 新增管理规范 | ✅ | 添加到 concepts/ |
| 项目结构变更 | ⚠️ | 只更新引用，不复制项目文件 |
| 临时文件 | ❌ | 不同步 |

### 同步操作

**新增 SKILL 技能**：
```
来源：~/.openclaw/workspace/steward/skills/<skill-name>/
目标：~/.openclaw/wiki/sources/<skill-name>.md
```
1. 提取 HANDBOOK.md 核心内容
2. 保留引用路径指向原技能
3. 添加到 sources/index.md

**更新规范文档**：
```
来源：~/.openclaw/workspace/steward/AGENTS.md
目标：~/.openclaw/wiki/concepts/agents.md
```
1. 同步关键规范变更
2. 更新版本历史
3. 保留引用指向原文件

**新增管理规范**：
```
来源：skills/manager/references/<guide>.md
目标：~/.openclaw/wiki/concepts/<guide>.md
```
1. 判断是否需要升级为 wiki 页面
2. AI 专用规范 → 保持在技能目录
3. 人机共用规范 → 同步到 wiki

### 同步检查

```bash
openclaw wiki lint
openclaw wiki status
```

### 禁止行为

| 禁止 | 原因 |
|------|------|
| 复制项目文件到 wiki | 项目文件应在仓库 |
| 同步临时文件 | wiki 是知识库，非存储库 |
| 创建重复页面 | 先检查是否已存在 |

---

## 五、目录结构

```
项目/
├── .agents
│   ├── tasks/              # task 工具的 JSON（fallback 用）
│   │   └── {runId}.json
│   └── events/            # 事件报告
│       └── {日期}/
│           └── {runId}.md
├── README.md
├── HANDBOOK.md
└── TODO.md
```

---

## 六、关键参数

| 参数 | 说明 |
|------|------|
| `card_id` | workboard 卡片 UUID（短 8 位即可） |
| `sessionKey` | agent session（如 `agent:writer:feishu:group:oc_xxx`） |
| `baseDir` | 项目根目录，task/event 生成到 `项目/.agents` |
| `runId` | task 工具任务唯一 ID（fallback 用） |

---

## 七、版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 2.0.0 | 2026-06-03 | 合并 `sync-guide.md` + `sync-standards.md`；新增 TODO ↔ workboard 同步章节 |
| 1.0.0 | 2026-05-19 | 初始版本（两份独立文件） |

*最后更新：2026-06-03*
