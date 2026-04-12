# 维护工作记忆

> 物理学家专属技能

---

## 功能描述

清理 MEMORY.md 中的非 active/paused 状态任务，将 completed 任务归档到事件记忆，删除 killed 任务。

## 使用方法

```bash
bash ~/.openclaw/workspace/physicist/skills/维护工作记忆/维护工作记忆.sh
```

## 触发条件

- 每日维护任务的一部分
- 工作记忆需要清理时

## 输入

- MEMORY.md：工作记忆文件

## 输出

- 日志文件：~/实验室仓库/日志文件/YYYY-MM-DD/04-00-00-physicist-工作记忆维护.md
- 更新后的 MEMORY.md（删除 completed/killed 任务）

## 处理逻辑

1. 提取 completed 状态任务 → 归档到事件记忆
2. 提取 killed 状态任务 → 记录后删除
3. 从活跃子代理清单中删除 completed/killed 任务

## 依赖

- bash
- awk
- sed
- date

---

*最后更新：2026-04-12*
