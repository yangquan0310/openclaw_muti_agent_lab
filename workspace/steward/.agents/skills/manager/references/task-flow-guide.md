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

## 二、4 步派发流程

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
- ❌ 手动 `manager workboard start`（Dx 自动）
- ❌ 手动 `move --status done`（Dx 自动）

**start 保留但不主动调**（CLI 不删除）：
- Dx 现在自动 backlog → running → done，start 用不到
- 但**保留命令**——应对未来 Dx bug 修复或需要手动触发的新场景
- 用法（按需）：`manager workboard start --id <card_id>`

**监控**：如果卡超过 30 分钟仍在 running，介入处理（看 attempt 状态 + 群消息）

---

## 三、代理反馈（走 workboard，不走群消息）

代理执行任务期间，通过 workboard 提交进度：

| 工具 | 用途 | 时机 |
|------|------|------|
| `workboard_comment` | 进度描述、遇到问题 | 执行过程中按需 |
| `workboard_proof` | 产出证明（artifact） | 任务完成时 |
| `workboard_heartbeat` | 续约 claim token | 每 10 分钟续约 |

**🚫 禁止**：群里发"进度更新"消息——群消息只用于派发通知 + 完成确认。
**✅ 必须**：任务完成后附 workboard_proof（status: passed）。

---

## 四、大管家核验 + TODO 更新

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

## 五、任务状态映射

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

## 六、Dx 误判排查（v3.0.1 新增）

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

## 七、禁止行为（v3.0.1 版）

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

## 八、版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 3.0.1 | 2026-06-03 03:05 | **老板定型**：(1) IM 群艾特必须（纠正 v3.0.1 草案"可选"）；(2) 任务进度反馈走 workboard（proof+comment）；(3) start 保留但不主动调；(4) 中间文件放 temp/，不放 knowledge/；(5) 采纳 A/B/C/E 提议，撤回 D；(6) 新增 --no-dup 防重复建卡 |
| 3.0.0 | 2026-06-03 02:39 | 基于 T001.1 端到端测试定型：5+1 步 → 3 步派发；Dx 自动行为；代理汇报 |
| 2.3.0 | 2026-06-03 | TODO 7 字段定型 |
| 2.2.0 | 2026-06-03 | 5+1 步新流程 |
| 2.0.0 | 2026-05-21 | task-guide.md v2.0 |

*最后更新：2026-06-03 03:05*
*定稿者：老板（杨权）*
