---
name: assimilation_accommodation
description: >
  同化与顺应模块。基于皮亚杰认知发展理论，通过日记记录和经验反思实现 Agent 持续自我更新。
version: 1.1.0
author: 大管家
dependencies:
  - ../working_memory
exports:
  - diary_template
  - core_self_update_template
  - identity_update_template
  - belief_style_update_template
  - skills_update_template
routes:
  - diary/
  - core_self_update/
  - identity_update/
  - belief_style_update/
  - skills_update/
---

# assimilation_accommodation

> 同化与顺应模块 - 通过日记记录实现自我更新
> 基于皮亚杰认知发展理论

---

## 文件说明

| 文件 | 功能 | 说明 |
|------|------|------|
| `SKILL.md` | 模块路由 | 同化与顺应总览，索引子模块 |
| `diary/SKILL.md` | 发展日记 | 记录每日经验和反思 |
| `diary_reader/SKILL.md` | 日记阅读器 | 读取事件日志，为日记生成提供素材 |
| `core_self_update/SKILL.md` | 核心自我更新 | 更新核心身份和能力边界 |
| `identity_update/SKILL.md` | 身份更新 | 更新角色集和社会身份 |
| `belief_style_update/SKILL.md` | 信念与风格更新 | 更新工作信念和工作风格 |
| `skills_update/SKILL.md` | 技能更新 | 更新技能体系 |

---

## 定时任务配置

### 每日自我更新任务

| 属性 | 配置 |
|------|------|
| **任务ID** | 各代理独立配置（如：`757bffa8-bd05-4f27-b197-b4edfa3d3aef`） |
| **执行时间** | `0 0 * * *`（每日 00:00，Asia/Shanghai） |
| **执行方式** | 主代理执行 |
| **触发消息** | `[cron:每日自我更新]` |
| **超时时间** | 300秒 |
| **事件日志路径** | `events/YYYY-MM-DD/HH-MM-SS-self-update.md` |
| **日记路径** | `diary/YYYY-MM-DD.md` |

### 任务执行流程

```
[cron:每日自我更新] 触发
    ↓
1. 阅读当日事件记忆（events/YYYY-MM-DD/HH-MM-SS-{event}.md）
    ↓
2. 撰写/完善发展日记（diary/YYYY-MM-DD.md）
    ↓
3. 阅读核心自我与配置文件
   ├── MEMORY.md（核心自我认知）
   ├── SOUL.md（风格与信念）
   ├── IDENTITY.md（身份定义）
   └── skills/README.md（个人技能索引）
    ↓
4. 同化与顺应分析（对比日记与核心自我）
   ├── 同化：原有内容的细化
   └── 顺应：新结构的出现
    ↓
5. 检测更新触发信号
   ├── 自我认知变化 → core_self_update
   ├── 角色变化 → identity_update
   ├── 信念/风格调整 → belief_style_update
   └── 技能变化 → skills_update
    ↓
6. 执行相应更新
   ├── 更新 IDENTITY.md / SOUL.md / MEMORY.md
   ├── 固化个人 skills（创建/更新技能文件，更新 skills/README.md 索引）
   └── 同步到 lab_repository
    ↓
7. 记录更新日志
   ├── 更新 MEMORY.md 历史版本
   └── 生成 self-update 事件文件（events/YYYY-MM-DD/HH-MM-SS-self-update.md）
```

---

## 工作流

### 工作流1：任务工作流（六阶段闭环）

> 从接受用户需求到任务完成并归档的完整生命周期。
> 对应 `AGENTS.md` 六阶段规范，其中阶段6由本模块（assimilation_accommodation）主导。

```
接受用户需求
    ↓
阶段0：会话初始化
    ├── 载入 SOUL.md / IDENTITY.md / MEMORY.md / TOOLS.md
    └── 初始化工作记忆（读取当前活跃任务看板、活跃子代理清单）
    ↓
阶段1：任务决策
    ├── 快速查询 / Cron → 主代理直接执行（跳至阶段5）
    └── 复杂任务 → 进入元认知闭环
        ↓
阶段2：计划（Planning）→ metacognition/planning/SKILL.md
        ├── 目标澄清、约束识别
        ├── 任务层级拆解
        ├── 子代理与工具分配
        └── 在工作记忆创建任务记录（状态：active）
        ↓
阶段3：执行或监控（Monitoring）→ metacognition/monitoring/SKILL.md
        ├── 创建子代理并分配任务
        ├── 持续跟踪子代理状态
        ├── 更新工作记忆（最后活跃时间、进度）
        └── 偏差检测（>10% / >80% / >30min）
        ↓
阶段4：调节（Regulation）→ metacognition/regulation/SKILL.md（条件触发）
        ├── 根因分析
        ├── 生成调节方案
        ├── 执行调节（paused → active）
        └── 返回阶段3继续监控
        ↓
阶段5：任务完成与归档 → working_memory/memory_table/SKILL.md
        ├── 更新状态为 completed
        ├── 记录完成摘要到工作记忆
        ├── 归档到事件记忆：events/YYYY-MM-DD/HH-MM-SS-completed.md
        └── killed 任务：events/YYYY-MM-DD/HH-MM-SS-killed.md（后删除）
```

### 工作流2：每日同化与顺应（每日定时执行）

> 每日 00:00 定时执行，完成系统性反思与自我更新

**步骤**：

1. **阅读当日事件记忆**
   - 读取 `events/YYYY-MM-DD/` 下所有 `HH-MM-SS-{event}.md` 文件
   - 梳理 completed / killed / regulation 事件的完整脉络

2. **撰写/完善发展日记**
   - 在 `diary/YYYY-MM-DD.md` 中整合全天任务回顾
   - 提取跨任务的成功经验与失败教训（去重、归类）
   - 评估可复用性（高/中/低），标记需固化的技能点

3. **阅读核心自我与配置文件**
   - 读取 `MEMORY.md` 中的「核心自我认知」
   - 读取 `SOUL.md`（风格与信念）
   - 读取 `IDENTITY.md`（身份定义）
   - 读取 `skills/README.md`（个人技能索引）

4. **同化与顺应分析**
   - **同化**：原有内容的细化（如将"细心"操作化为检查清单）
   - **顺应**：新结构的出现（如用户提出全新约束、新角色分配）
   - 对比日记与核心自我 → 识别需要更新的信号

5. **检测更新触发信号**
   - [ ] 自我认知变化 → 调用 `core_self_update`
   - [ ] 角色变化 → 调用 `identity_update`
   - [ ] 信念/风格调整 → 调用 `belief_style_update`
   - [ ] 技能变化 → 调用 `skills_update`

6. **执行相应更新**
   - 调用对应子模块 SKILL.md
   - 更新 `IDENTITY.md` / `SOUL.md` / `MEMORY.md`
   - 固化个人 skills（创建/更新技能文件，更新 `skills/README.md` 索引）
   - 同步到 `lab_repository`

7. **记录更新日志**
   - 将变更记录到 `MEMORY.md` 历史版本
   - 生成 `events/YYYY-MM-DD/HH-MM-SS-self-update.md` 事件文件

---

## 使用指南

### 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `daily_events` | list | ✅ | 今日执行任务清单 |
| `memory_archive` | object | ❌ | 从 working_memory 归档的事件 |
| `current_identity` | object | ✅ | 当前身份定义（IDENTITY.md 内容） |

### 输出结果

| 输出项 | 格式 | 说明 |
|--------|------|------|
| `diary_entry` | Markdown | 发展日记条目（存储在 diary/YYYY-MM-DD.md） |
| `update_log` | Markdown | 自我更新日志 |
| `identity_patch` | Markdown | 身份/信念/技能更新补丁 |

### 同化与顺应判定

| 类型 | 判定标准 | 处理方式 |
|------|----------|----------|
| **同化** | 原有内容的细化 | 更新现有流程、细化标准操作 |
| **顺应** | 新结构的出现 | 新增模块、新增约束、新增角色 |

**示例**：
- 同化：工作风格有"细心"，将"细心"操作化为具体流程
- 顺应：用户提出全新风格要求（如"不要过度扩展"），需新增约束规则

---

## 与 working_memory 的关系

```
working_memory
    └── 任务完成 (completed)
            ↓ 归档
assimilation_accommodation
    ├── 事件记忆（events/ 目录，陈述性记忆）
    └── 发展日记（diary/ 目录，经验积累）
            ↓ 反思
    自我更新（核心自我/身份/信念/技能）
```

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.2.0 | 2026-04-19 | 更新存储路径：memory/ → events/ 和 diary/ |
| v1.1.0 | 2026-04-19 | 添加定时任务配置章节，规范每日自我更新流程 |
| v1.0.0 | 2026-04-17 | 初始版本，标准化文档规范 |

---

*创建者: 大管家*  
*创建时间: 2026-04-17*  
*最后更新: 2026-04-19*
