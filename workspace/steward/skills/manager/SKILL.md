---
name: manager
description: >
  manager的实践技能。
  当需要推进任务、完善TODO、领取项目任务、派发任务时激活。
  大管家唯一管理技能入口，负责论文、课程、程序、知识库、通用项目的管理。
version: 5.0.0
author: Yang Quan
metadata:
  openclaw:
    emoji: 📋
    requires:
      bins: [python3]
---

# manager 管理技能

> **唯一入口**：所有管理场景统一由此入口处理。

---

## 核心原则

1. **授权执行**：管方向、定边界、分配任务，不亲自执行
2. **约束目标前置**：领取任务先明确验收标准 + 边界条件
3. **子代理自主**：子任务由子代理自己拆解，大管家只定约束/输入/产出
4. **TODO.md 强制**：领取任务立即录入，记录任务链路和当前阶段

---

## 场景索引

| 场景 | guide |
|------|-------|
| 任务推进/派发 | task-guide.md |
| 论文项目 | thesis-guide.md |
| 课程项目 | course-guide.md |
| 程序项目 | program-guide.md |
| 知识库管理 | knowledge-guide.md |
| 项目整理 | organize-workflow.md |
| 通用项目 | project-guide.md |

---

## 核心流程

```
领取任务 → 明确约束 → 更新TODO.md → 派发子代理 → 追踪进度 → 汇报老板
```

---

## 边界条件

- 模板只能存放在 `assets/`
- 不得在任务中指定模型、预算等权限外内容
- 汇报必须通过群聊，禁止私聊

---

## 快速调用

```bash
# 项目整理
python3 scripts/maintainer/Maintainer.py --help

# 搜索 guide
lookup search --skill manager <关键词>
```

---

## 版本历史

| 版本 | 日期 | 更新 |
|------|------|------|
| 5.0.0 | 2026-05-22 | 精简：详细工作流下沉到 references/ 各 guide |
| 4.0.0 | 2026-05-21 | 唯一入口，整合所有子技能 |
