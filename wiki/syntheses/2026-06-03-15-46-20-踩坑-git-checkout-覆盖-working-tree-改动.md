---
pageType: synthesis
id: lesson.git-checkout-overwrite
title: 踩坑：git checkout 覆盖 working tree 改动
createdAt: "2026-06-03T15:46:20+08:00"
updatedAt: "2026-06-03T15:46:20+08:00"
sourceIds:
  - source.workspace-steward
tags:
  - 教训
  - git
  - working-tree
  - stash
  - 跨分支操作
---

# 踩坑：git checkout 覆盖 working tree 改动

> **事故日期**：2026-06-03
> **严重程度**：🟡 中（关键配置丢失，需重写）
> **踩坑人**：大管家（steward）
> **场景**：合并 development → main 时，steward.subagents.allowAgents 9 个专家配置丢失

---

## 一、事故现场

合并 development 到 main 时，我之前配置好的 9 个专家调用权限（`subagents.allowAgents`）**完全丢失**。

### 现象

- `openclaw.json` 的 `agents.list[0].subagents` = `null`
- `agents_list` 运行时工具只返回 steward 自己
- 无法 spawn 任何专家（writer / mathematician / physicist / ...）
- 须重新执行 `openclaw config set` 才能恢复

### 影响

- 9 个专家可调用能力完全丢失
- 合并到 main 后，`origin/main` 上的 `openclaw.json` 也是 `null`——**远程也是错的**
- 必须重新写入并 commit + push 修复（commit `8e8a8ed7`）

---

## 二、时间线

| # | 操作 | 状态 |
|---|------|------|
| 1 | `openclaw config set agents.list.0.subagents.allowAgents '["writer",...]'` | ✅ working tree 有改动 |
| 2 | `git stash` 暂存 4 个 modified | ✅ 暂存成功 |
| 3 | `git checkout main` | ⚠️ 看似 OK |
| 4 | `git merge development`（fast-forward） | ✅ |
| 5 | `git push origin main` | ✅ |
| 6 | `git checkout development` | ✅ |
| 7 | `git stash pop` | ❌ 失败：`cron/jobs-state.json` 与 development HEAD 冲突 |
| 8 | `git stash drop` | ⚠️ **整个 stash 被丢弃**——`openclaw.json` 改动彻底丢失 |
| 9 | 验证 working tree | ⚠️ 只剩 `cron/jobs-state.json` 一个 modified |
| 10 | 重新 `openclaw config set` 写入 | ✅ 恢复成功（commit `8e8a8ed7`） |

**关键节点**：第 7 步 stash pop 失败 → 第 8 步 drop stash → **openclaw.json 改动瞬间归零**。

---

## 三、根因（3 个叠加）

### 根因 1：对 `git checkout <branch>` 行为误解

- `git checkout <branch>` **会用目标分支 HEAD 覆盖** working tree 的同名文件
- 即使有 stash 也不保留——stash 不会自动同步到不同分支
- 我误以为"stash 起来就安全"——其实 stash 只对**当前分支**有效

### 根因 2：stash pop 失败 + drop 的"双重暴击"

- `git stash pop` 失败时**所有改动都没被应用**——不只是冲突的那个
- `git stash drop` 会**整体删除** stash——没有"部分保留"机制
- 这两步组合 = 改动**彻底归零**（除非有备份）

### 根因 3：跨分支操作未先 commit

- `openclaw.json` 涉及 agent 行为（9 个专家可调用性）——**关键配置**
- 关键配置应该**先 commit 到当前分支**，再跨分支操作
- 依赖 stash 保护关键改动 = 把安全寄托在"stash 一定能恢复"上——**违反最小依赖原则**

---

## 四、教训（应该怎么做）

### ✅ 正确做法

1. **关键配置先 commit，再跨分支**：
   ```bash
   git add openclaw.json
   git commit -m "checkpoint: 跨分支前保存 subagents 配置"
   ```

2. **跨分支前手动备份**（比 stash 保险）：
   ```bash
   cp openclaw.json openclaw.json.bak.$(date +%Y%m%d-%H%M%S)
   ```

3. **stash pop 失败时逐个恢复**，不要直接 drop：
   ```bash
   # pop 失败后
   git checkout stash@{0} -- <不冲突的文件>
   # 验证关键文件
   jq '.agents.list[0].subagents' openclaw.json
   # 确认无问题再 drop
   git stash drop
   ```

4. **切回原分支后立即验证关键字段**：
   ```bash
   jq '.agents.list[0].subagents.allowAgents | length' openclaw.json
   # 应返回 9；若返回 0/null = 配置丢失
   ```

### ❌ 错误做法

- 只靠 stash 保护关键配置改动
- `git stash pop` 失败就 `git stash drop`（**所有改动都没了**）
- 跨分支操作前不验证 working tree 状态
- 假设 `git checkout` 不会覆盖 working tree
- 假设"stash 一定能在 pop 时完整恢复"

---

## 五、防御措施（建议落地）

### 1. 跨分支操作 SOP（推荐流程）

```bash
# 1. 关键配置先 commit
git add <关键文件> && git commit -m "checkpoint: pre branch switch"

# 2. 备份
cp <关键文件> <关键文件>.bak.$(date +%Y%m%d-%H%M%S)

# 3. 再 stash 其他临时改动
git stash push -m "<context>"

# 4. 跨分支
git checkout <branch>
# ... 操作 ...

# 5. 切回后，先 checkout stash 部分恢复
git checkout stash@{0} -- <不冲突的文件>

# 6. 验证关键文件
jq '.agents.list[0].subagents' openclaw.json  # 期望非 null

# 7. 全部确认后再 drop
git stash drop
```

### 2. 关键配置检查清单（每次跨分支前）

| 检查项 | 命令 | 期望值 |
|--------|------|--------|
| `subagents.allowAgents` 数量 | `jq '.agents.list[0].subagents.allowAgents \| length' openclaw.json` | 9（按需） |
| `subagents.delegationMode` | `jq -r '.agents.list[0].subagents.delegationMode' openclaw.json` | `"suggest"` / `"prefer"` |
| `subagents.requireAgentId` | `jq -r '.agents.list[0].subagents.requireAgentId' openclaw.json` | `true` / `false` |

### 3. 自动化检查脚本（待加）

写一个 `pre-branch-checkout.sh`：
- 检测 `openclaw.json` 等关键文件是否有未提交改动
- 提示先 commit 或备份

### 4. MEMORY 规则沉淀

把这条踩坑记入 MEMORY.md If-Then 规则：

> **跨分支操作前** | (1) 关键配置先 commit，不依赖 stash 保护；(2) stash pop 失败时**用 `git checkout stash@{0} -- <file>` 逐个恢复**，不要直接 `git stash drop`；(3) 切回原分支后**用 `jq` 验证关键字段**（如 `subagents.allowAgents`）。

---

## 六、相关参考

- **MEMORY.md**：合并 main 分支前先更新 README.md 版本历史
- **manager 技能**：`task-flow-guide.md` v3.0.1 三件套派发
- **OpenClaw 配置**：`agents.list[*].subagents` 字段 schema（`openclaw config schema lookup agents.list`）
- **本次事故修复 commit**：`8e8a8ed7 chore: 同步 working tree 4 个改动（2026-06-03）`

---

*事故归档人：大管家（steward）*
*归档时间：2026-06-03 15:46:20+08:00*
*状态：教训已学，防御措施待落地*

## Related
<!-- openclaw:wiki:related:start -->
### Related Pages

- [[syntheses/2026-05-19-18-25-37-如何攥写if-then规则|If-Then 规则修改标准]]
<!-- openclaw:wiki:related:end -->
