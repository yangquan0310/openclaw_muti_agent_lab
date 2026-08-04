---
name: manager
description: >
  manager是大管家的**科研项目管理**技能（**唯一入口**，任务派发唯一路径）。
  当需要派发任务（群派发 IM 艾特 / dispatch 派发 `openclaw workboard dispatch` CLI）、推进任务、完善TODO、领取项目任务、协调子代理干活时激活（task-flow-guide.md）。
  当需要创建/管理**科研项目**（论文、程序、知识库/wiki、通用项目）时激活。
  当需要技能审计、核查技能质量时激活（skill-audit-workflow）。
  当需要.openclaw系统体检、日常维护、问题处理时激活（openclaw-maintenance-guide）。
  当需要定期清理wiki或同步规范时激活（cleaning-guide、sync-guide）。
  当需要发布 workboard 任务卡（多 Agent 协作跟踪）时激活（workboard-guide）。
  当需要决定 workboard 卡片粒度（**混合 L1 项目 / L2 阶段 / L3 任务**三层模式，老板 2026-08-04 拍板）时激活（card-granularity）。
  当需要 Quarto PDF 编译/排版/APA 7th 论文配置时激活（quarto-pdf-config）。
version: 5.15.0
author: Yang Quan
metadata:
  openclaw:
    emoji: 📋
    requires:
      bins: [python3]
---

# manager 管理技能

> **科研项目管理入口**：所有科研管理场景统一由此入口处理。**不**涵盖教学/课程管理（已 v8.52.0 教研→科研转型废弃）。

---

## 核心原则

1. **授权执行**：管方向、定边界、分配任务，不亲自执行
2. **约束目标前置**：领取任务先明确验收标准 + 边界条件
3. **子代理自主**：子任务由子代理自己拆解，大管家只定约束/输入/产出
4. **TODO.md 群场景强制，dispatch 派发不写**：
   - **群派发**：领取任务立即写 TODO.md（看板 + 状态记录）
   - **dispatch 派发**：单卡 workboard 即可，**不**写 TODO.md（单人任务不必建看板）
5. **派发永远只 2 动作**：**建卡（`openclaw workboard create` CLI）+ 触发**（IM 艾特 / `openclaw workboard dispatch` CLI）。验收权下放给 worker

---

## 边界条件

- **不做什么**：不撰写内容、不编写代码、不进行数据分析、不提供学术观点
- 模板只能存放在 `assets/`
- 不得在任务中指定模型、预算等权限外内容
- **汇报渠道按场景分**：
  - **群派发**：进度走 workboard，群里不发"进度更新"（只派发通知 + 完成确认）
  - **dispatch 派发**：大管家只 `workboard_read` 追踪 status，**status=done → 汇报老板**
  - ❌ 大管家**不调** `workboard_complete`（验收权下放）
  - ❌ 大管家**不调** `workboard_claim`（让代理/dispatch 调）
- **提纯后定位（v5.14.0）**：本技能**仅**管科研项目（论文/程序/知识库/wiki/通用），**不**管教学/课程项目（lesson-plan-guide / course-guide 已删除，CourseMaintainer 已删除，教学模板已删除）。如需教学管理，请老板新建独立 `lesson-manager` 技能（v8.52.0 之后如有需要）

---

## 快速调用

```bash
# === Workboard 任务发布（v5.13.0：CLI 主用） ===

# 群派发建卡
openclaw workboard create "title" --agent <agent> --board default \
  --status backlog --priority high --labels "..." --notes "任务四要素"

# 绑群 session（agent tool — CLI 无 comment）
workboard_comment({ id: cardId, body: "sessionKey=agent:<agent>:feishu:group:oc_xxx" })

# dispatch 派发建卡
openclaw workboard create "title" --agent <agent> --board default \
  --status ready --priority normal --labels "..." --notes "任务四要素"

# === 派发动作 ===
# 群场景：IM 5 段模板艾特（看 task-flow-guide.md §二）
# dispatch 派发场景：openclaw workboard dispatch --board default --expect-final --timeout 300000

# === 追踪（agent tool — CLI 无 read） ===
workboard_read({ id: cardId })
# status=done → 汇报老板
# ❌ 不调 workboard_complete（验收权下放，worker 自己）
# ❌ 不调 workboard_claim（让代理/dispatch 调）
```

```bash
# === plugin CLI 速查 ===
openclaw workboard create "title" --agent <id> --status <s> ...
openclaw workboard list [--board default] [--status <s>]
openclaw workboard show <id>
openclaw workboard dispatch --board default --expect-final --timeout 300000
```

**大管家 2 动作铁律**：**建卡（`openclaw workboard create` CLI）+ 触发**（IM 艾特 / `openclaw workboard dispatch` CLI）。验收权下放给 worker。

---

## 指南导航

| 章节 | 文件 |
|------|------|
| manager 概述 | manager-overview.md |
| Workboard 任务发布 | workboard-guide.md v1.12.0 |
| 任务流（两种协调方式）| task-flow-guide.md v3.8.0（§二、群派发 / §三、dispatch 派发） |
| 论文项目 | thesis-guide.md |
| ~~课程项目~~ | ~~course-guide.md~~（v5.14.0 已删除）|
| 程序项目 | program-guide.md |
| 知识库管理 | knowledge-guide.md v2.0 |
| 项目整理 | organize-workflow.md |
| 通用项目 | project-guide.md |
| **workboard 卡片粒度** | **card-granularity.md v1.0.0**（**混合 L1/L2/L3 模式**）|
| ~~课程备课~~ | ~~lesson-plan-guide.md~~（v5.14.0 已删除）|
| 技能审核 | skill-audit-workflow.md |
| 定期清理 | cleaning-guide.md |
| 系统维护 | openclaw-maintenance-guide.md |
| **Quarto PDF 编译/排版** | **quarto-pdf-config.md v1.1**（含 authblk 作者单位渲染模式）|

---
## 版本历史

| 版本 | 日期 | 更新 |
|------|------|------|
| **5.15.0** | **2026-08-04** | **🆕 workboard 卡片粒度 = 混合模式**（老板 2026-08-04 11:32 拍板"workboard 卡片粒度改为混合，你落实到管理技能"）。**新增 `references/card-granularity.md` v1.0.0**（~5.3KB）：(1) 三层架构 = L1 项目卡（1张/项目，老板视角）+ L2 阶段卡（3-5张/项目，大管家追踪）+ L3 任务卡（按需，worker 执行）；(2) 每层建卡时机 + 必填字段 + 何时关卡；(3) 派发与混合模式关系：L1/L2 不直接派发，L3 才是真正派发对象（群派发 IM 5段艾特 / dispatch 派发 `openclaw workboard dispatch` CLI）；(4) 判断标准速查表；(5) 已有项目迁移建议。**SKILL.md 改动**：(a) description 加触发条件"当需要决定 workboard 卡片粒度（混合 L1/L2/L3 三层模式）时激活"；(b) 指南导航表加 card-granularity.md v1.0.0 行；(c) 版本号 5.14.0 → 5.15.0。**配套**：MEMORY.md If-Then 表加 1 条 v5.15.0 规则（"workboard 卡片粒度 = 混合 L1/L2/L3 模式，参考 card-granularity.md"）。**commit**：待 v5.15.0 commit。 |
| **5.14.0** | **2026-08-04** | **🆕 教研→科研转型：manager 技能提纯**（老板 2026-08-04 11:04 拍板）。**删除 12 个混杂文件**：(1) `references/lesson-plan-guide.md`（202 行，课程备课 v1-v7 SOP，v8.13.0/v8.40.0 已沉淀教训：项目 README/HANDBOOK 才是规范源）；(2) `references/course-guide.md`（112 行，课程项目指南）；(3) `scripts/maintainer/CourseMaintainer.py`（382 行，课程维护器）；(4) `assets/templates/终稿教案模板.md`；(5) `assets/templates/课件脚本模板.md`；(6) `assets/templates/内容框架模板.md`；(7) `assets/templates/学术前沿补充模板.md`；(8) `assets/templates/审校意见模板.md`；(9) `assets/templates/需求分析模板.md`；(10) `assets/chapter-metadata-template.json`；(11) `assets/agents/auditor.md`（agent 已删，v8.52.0）；(12) `assets/agents/instructor.md`（agent 已删，v8.52.0）。**清理缓存**：`scripts/maintainer/__pycache__/`（5 个 .pyc 文件）。**SKILL.md 重构**：(a) description 移除「当需要备课时激活（lesson-plan-guide）」触发词 + 「课程」从项目类型列表移除；(b) 章节标题从「所有管理场景统一由此入口处理」→「科研项目管理入口」；(c) 边界条件加「提纯后定位」段落（v5.14.0 明确：本技能**仅**管科研项目，不管教学/课程项目）；(d) 指南导航表删除 course-guide / lesson-plan-guide 行（用 ~~删除线~~ 标注）；(e) 版本号 5.13.0 → 5.14.0。**提纯后定位**：manager 技能**仅**管科研项目（论文/程序/知识库/wiki/通用）；如需教学管理，老板后续可新建独立 `lesson-manager` 技能。**配套**：(1) MEMORY.md v8.52.0 职责边界更新（删除 auditor/instructor）+ (2) README.md v3.3.4 badge 10→8 + (3) presentor v2.0.0 转型可视化师 + (4) HEARTBEAT.md v1.14.0 + (5) AGENTS.md v2026.8.4 仓库整理 + (6) `.archive/` 归档 10 个教学/AI 项目。**commit**：待 v5.14.0 commit。 |
| **5.13.0** | **2026-07-02** | (1) 派发从 3 模式 → 2 模式：群派发（IM）/ dispatch 派发（CLI）；(2) description 加 dispatch 触发词；(3) 核心原则 4 改 TODO.md 分场景；(4) 核心原则 5 改 2 动作铁律 + 验收权下放；(5) 边界条件加 2 条不调项；(6) 快速调用重写；(7) 导航表升 v3.8.0 / v1.12.0 |
| **5.12.0** | **2026-06-06** | (1) description 加"两种协调方式"必查触发；(2) 核心原则修分场景；(3) 边界条件撤销禁止私聊汇报；(4) 快速调用升 v1.5.0；(5) 导航表升 v3.2.0 / v1.5.0 |
| **5.11.0** | **2026-06-04** | **Quarto 作者单位渲染模式固化**：(1) references/quarto-pdf-config.md 升 v1.1（~11KB），新增「八、作者 + 单位 + 联系方式 PDF 渲染（authblk 模式）」章节（源自记忆机制论文实战），含四件套配置（header.tex + title.tex partial + YAML 字段 + LaTeX 通讯作者块）+ 6 条坑速查 + 替代方案对比 + wiki 实体作为元数据源；(2) references/index.md 同步；(3) 导航表加 v1.1 标注 |
| **5.10.0** | **2026-06-04** | **新增 Quarto PDF 编译/排版场景**：(1) 新增 references/quarto-pdf-config.md（v1.0，~7.7KB），覆盖 3 范式 + CJK 字体（AR PL SungtiL GB 避 Noto TTC 坑）+ APA 7th + header-includes vs header.tex；(2) references/index.md 加"排版/编译"段；(3) description 加触发条件；(4) 导航表加新条目 |
| 5.9.0 | 2026-06-03 | **任务流指南 v3.0.1 老板定型**：(1) IM 群艾特必须（纠正"可选"歧义）；(2) 任务进度反馈走 workboard（proof+comment）；(3) 中间文件放 temp/ 不放 knowledge/；(4) start 保留但不主动调；(5) 新增 --no-dup 防重复建卡；(6) 指南导航 task-flow-guide 指向 v3.0.1 |
| 5.8.0 | 2026-06-03 | **任务流指南 v2.2 → v3.0 同步**：(1) 5+1 步 → 3 步派发（Dx 自动覆盖 move→todo / start）；(2) 明确"代理必须群里汇报"硬要求；(3) 文件路径硬性绝对化；(4) 指南导航 task-flow-guide 指向 v3.0 |
| 5.7.0 | 2026-06-03 | **skill-developer 规范对齐**：删 `_meta.json`、`references/README.md`（v5.5.0 移除）；`guide.md`→`manager-overview.md`（noun phrase 命名）；references 清理冗余（-3个文件）；版本历史全量修复 |
| 5.6.0 | 2026-06-02 | **修复 UX bug**：`claim --auto-start` 选项。claim 后自动用 update RPC 设置 `execution.status=running`，避免 dashboard 仍显示「开始」按钮（claim 只改 board.status，不改 execution.status） |
| 5.5.0 | 2026-06-02 | **Python 迁移**：workboard 模块从 Node.js (wb-rpc.mjs) 迁移至 Python 包 (`scripts/workboard/`)，集成到 manager CLI 统一入口（`manager workboard <子命令>`）。修复设备身份签名时间差 bug |
| 5.13.0 | 2026-06-06 | **重大修复（老板纠错）**：删除 `scripts/workboard/` 整个目录（932 行 Python）。`manager workboard <子命令>` CLI 整段移除（main.py:49-50）。建卡/验收全部走 `workboard_*` agent tool（plugin contract tools 一直就有），shell 备选用 `openclaw workboard` plugin CLI。修复 v8.25.0 沉淀错误认知（漏看 `workboard_create` tool）。workboard-guide.md v1.6.0 → v1.7.0；task-flow-guide.md v3.2.0 → v3.3.0 |
| 5.4.0 | 2026-06-02 | 新增场景：**Workboard 任务发布**（workboard-guide.md）。建/改/移/删/批量/归档走 gateway RPC + 设备身份认证 |
| 5.3.0 | 2026-05-28 | description 合并触发条件（删除 body 触发条件章节），覆盖全部12场景 |
| 5.2.0 | 2026-05-28 | 修复：CLI与实际不符、版本号统一、补充触发边界、同步 index.md 内容 |
| 5.1.0 | 2026-05-24 | CLI 精简：6子命令→4（init/organize/sync/check-updates），ABC 架构凝练 |
| 5.0.0 | 2026-05-22 | 精简：详细工作流下沉到 references/ 各 guide |
| 4.0.0 | 2026-05-21 | 唯一入口，整合所有子技能 |
