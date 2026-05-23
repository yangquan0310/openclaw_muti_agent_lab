# 任务生命流程

---

## 一、子任务完整生命流程

```
子任务创建
    ↓
明确计划（向用户明确）
    ↓
申请审批（用户确认）
    ↓
task.advance（分步执行）
    ↓
task.update（更新状态）
    ↓
分析归因（deviation / attribution）
    ↓
event.report（事件记录）
    ↓
调节（更新 SOUL/IDENTITY/MEMORY/SKILL/AGENTS）
    ↓
task.archive（归档）
```

---

## 二、主任务更新（大管家）

```
所有子任务完成
    ↓
大管家更新主 task.json
    ↓
event.report
    ↓
task.archive
```

---

## 三、调节说明

任务完成后，如果过程中有值得记住的反思，需要调节到对应的文件中：

| 维度 | 文件 | 时机 |
|------|------|------|
| 自我认知/风格/信念 | SOUL.md | 有变化时 |
| 身份 | IDENTITY.md | 职责边界变化时 |
| 程序性记忆 | MEMORY.md | 新 If-Then 规则时 |
| 技能 | HANDBOOK.md | 流程规范更新时 |
| 协作规则 | AGENTS.md | 多代理规则变化时 |

详见 event-management 技能的「事件生成后的人格调节」章节。
