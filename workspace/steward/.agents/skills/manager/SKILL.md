---
name: manager
description: >
  manager的实践技能。
  当需要推进任务、完善TODO、领取项目任务、派发任务时激活。
  当需要创建/整理/管理项目（论文、课程、程序、知识库/wiki、通用项目）时激活。
  当需要备课时激活（lesson-plan-guide）。
  当需要技能审计、核查技能质量时激活（skill-audit-workflow）。
  当需要.openclaw系统体检、日常维护、问题处理时激活（openclaw-maintenance-guide）。
  当需要定期清理wiki或同步规范时激活（cleaning-guide、sync-guide）。
  当需要发布 workboard 任务卡（多 Agent 协作跟踪）时激活（workboard-guide）。
  **不做什么**：不撰写内容、不编写代码、不进行数据分析、不提供学术观点。
version: 5.5.0
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
| 课程备课 | lesson-plan-guide.md |
| 技能审核 | skill-audit-workflow.md |
| 定期清理 | cleaning-guide.md |
| 规范同步 | sync-guide.md |
| 系统维护 | openclaw-maintenance-guide.md |
| Workboard 任务发布 | workboard-guide.md |

---

## 核心流程

```
领取任务 → 明确约束 → 更新TODO.md → 派发子代理 → 追踪进度 → 汇报老板
```

---

## 边界条件

- **不做什么**：不撰写内容、不编写代码、不进行数据分析、不提供学术观点
- 模板只能存放在 `assets/`
- 不得在任务中指定模型、预算等权限外内容
- 汇报必须通过群聊，禁止私聊

---

## 快速调用

```bash
# 项目整理
manager maintainer organize <project_path> [--dry-run]

# 同步模板
manager maintainer sync <project_path> [--dry-run]

# 检查更新
manager maintainer check-updates <project_path>

# 查看帮助
manager maintainer --help
manager maintainer <子命令> --help
```

## 版本历史

| 版本 | 日期 | 更新 |
|------|------|------|
| 5.5.0 | 2026-06-02 | **Python 迁移**：workboard 模块从 Node.js (wb-rpc.mjs) 迁移至 Python 包 (`scripts/workboard/`)，集成到 manager CLI 统一入口（`manager workboard <子命令>`）。修复设备身份签名时间差 bug（signedAt 只计算一次） |
| 5.4.0 | 2026-06-02 | 新增场景：**Workboard 任务发布**（workboard-guide.md）。建/改/移/删/批量/归档走 gateway RPC + 设备身份认证，详见 references/workboard-guide.md |
| 5.3.0 | 2026-05-28 | description合并触发条件（删除body触发条件章节），覆盖全部12场景 |
| 5.2.0 | 2026-05-28 | 修复：CLI与实际不符、版本号统一、补充触发边界、同步index.md内容 |
| 5.1.0 | 2026-05-24 | CLI 精简：6子命令→4（init/organize/sync/check-updates），ABC 架构凝练 |
| 5.0.0 | 2026-05-22 | 精简：详细工作流下沉到 references/ 各 guide |
| 4.0.0 | 2026-05-21 | 唯一入口，整合所有子技能 |
