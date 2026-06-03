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
  当需要 Quarto PDF 编译/排版/APA 7th 论文配置时激活（quarto-pdf-config，2026-06-04 新增）。
  **不做什么**：不撰写内容、不编写代码、不进行数据分析、不提供学术观点。
version: 5.11.0
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

## 边界条件

- **不做什么**：不撰写内容、不编写代码、不进行数据分析、不提供学术观点
- 模板只能存放在 `assets/`
- 不得在任务中指定模型、预算等权限外内容
- 汇报必须通过群聊，禁止私聊

---

## 快速调用

```bash
# Workboard 任务发布（v3.0.1）
manager workboard create --assignee writer --session 'agent:writer:...' --title '...' --no-dup
manager workboard move --id <card_id> --status done
# start 保留但不主动调（Dx 已自动覆盖）

# 项目整理
manager maintainer organize <project_path> [--dry-run]

# 同步模板
manager maintainer sync <project_path> [--dry-run]

# 检查更新
manager maintainer check-updates <project_path>

# 查看帮助
manager workboard --help
manager maintainer --help
```
---

## 指南导航

| 章节 | 文件 |
|------|------|
| manager 概述 | manager-overview.md |
| Workboard 任务发布 | workboard-guide.md v1.4.0 |
| 任务流（三件套派发） | task-flow-guide.md v3.0.1 |
| 论文项目 | thesis-guide.md |
| 课程项目 | course-guide.md |
| 程序项目 | program-guide.md |
| 知识库管理 | knowledge-guide.md v2.0 |
| 项目整理 | organize-workflow.md |
| 通用项目 | project-guide.md |
| 课程备课 | lesson-plan-guide.md |
| 技能审核 | skill-audit-workflow.md |
| 定期清理 | cleaning-guide.md |
| 系统维护 | openclaw-maintenance-guide.md |
| **Quarto PDF 编译/排版** | **quarto-pdf-config.md v1.1**（含 authblk 作者单位渲染模式）|

---
## 版本历史

| 版本 | 日期 | 更新 |
|------|------|------|
| **5.11.0** | **2026-06-04** | **Quarto 作者单位渲染模式固化**：(1) references/quarto-pdf-config.md 升 v1.1（~11KB），新增「八、作者 + 单位 + 联系方式 PDF 渲染（authblk 模式）」章节（源自记忆机制论文实战），含四件套配置（header.tex + title.tex partial + YAML 字段 + LaTeX 通讯作者块）+ 6 条坑速查 + 替代方案对比 + wiki 实体作为元数据源；(2) references/index.md 同步；(3) 导航表加 v1.1 标注 |
| **5.10.0** | **2026-06-04** | **新增 Quarto PDF 编译/排版场景**：(1) 新增 references/quarto-pdf-config.md（v1.0，~7.7KB），覆盖 3 范式 + CJK 字体（AR PL SungtiL GB 避 Noto TTC 坑）+ APA 7th + header-includes vs header.tex；(2) references/index.md 加"排版/编译"段；(3) description 加触发条件；(4) 导航表加新条目 |
| 5.9.0 | 2026-06-03 | **任务流指南 v3.0.1 老板定型**：(1) IM 群艾特必须（纠正"可选"歧义）；(2) 任务进度反馈走 workboard（proof+comment）；(3) 中间文件放 temp/ 不放 knowledge/；(4) start 保留但不主动调；(5) 新增 --no-dup 防重复建卡；(6) 指南导航 task-flow-guide 指向 v3.0.1 |
| 5.8.0 | 2026-06-03 | **任务流指南 v2.2 → v3.0 同步**：(1) 5+1 步 → 3 步派发（Dx 自动覆盖 move→todo / start）；(2) 明确"代理必须群里汇报"硬要求；(3) 文件路径硬性绝对化；(4) 指南导航 task-flow-guide 指向 v3.0 |
| 5.7.0 | 2026-06-03 | **skill-developer 规范对齐**：删 `_meta.json`、`references/README.md`（v5.5.0 移除）；`guide.md`→`manager-overview.md`（noun phrase 命名）；references 清理冗余（-3个文件）；版本历史全量修复 |
| 5.6.0 | 2026-06-02 | **修复 UX bug**：`claim --auto-start` 选项。claim 后自动用 update RPC 设置 `execution.status=running`，避免 dashboard 仍显示「开始」按钮（claim 只改 board.status，不改 execution.status） |
| 5.5.0 | 2026-06-02 | **Python 迁移**：workboard 模块从 Node.js (wb-rpc.mjs) 迁移至 Python 包 (`scripts/workboard/`)，集成到 manager CLI 统一入口（`manager workboard <子命令>`）。修复设备身份签名时间差 bug |
| 5.4.0 | 2026-06-02 | 新增场景：**Workboard 任务发布**（workboard-guide.md）。建/改/移/删/批量/归档走 gateway RPC + 设备身份认证 |
| 5.3.0 | 2026-05-28 | description 合并触发条件（删除 body 触发条件章节），覆盖全部12场景 |
| 5.2.0 | 2026-05-28 | 修复：CLI与实际不符、版本号统一、补充触发边界、同步 index.md 内容 |
| 5.1.0 | 2026-05-24 | CLI 精简：6子命令→4（init/organize/sync/check-updates），ABC 架构凝练 |
| 5.0.0 | 2026-05-22 | 精简：详细工作流下沉到 references/ 各 guide |
| 4.0.0 | 2026-05-21 | 唯一入口，整合所有子技能 |
