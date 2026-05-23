---
pageType: entity
entityType: user
id: entity.yangquan0310
createdAt: "2026-03-31T00:00:00+08:00"
updatedAt: "2026-05-12T02:15:00+08:00"
canonicalId: user.yangquan0310
aliases:
  - 杨权
  - 老板
  - 实验室负责人
sourceIds:
  - source.system-config
bestUsedFor:
  - 实验室科研方向决策
  - 论文项目总体规划
  - 多Agent任务分配与调度
  - 最终审核与确认
notEnoughFor:
  - 不直接执行具体技术任务
privacyTier: private
personCard:
  name: 杨权
  role: 实验室负责人
  style: 简洁条理、偏好Markdown、重视确认
  motto: —
relationships:
  - target: agent.steward
    relation: directs
    description: 大管家直接服务于实验室负责人
  - target: agent.programmer
    relation: directs
    description: 程序员负责技术实现
  - target: agent.mathematician
    relation: directs
    description: 数学家负责数学建模与统计分析
  - target: agent.physicist
    relation: directs
    description: 物理学家负责物理建模
  - target: agent.psychologist
    relation: directs
    description: 心理学家负责理论审核与实验设计
  - target: agent.writer
    relation: directs
    description: 写作助手负责论文撰写
  - target: agent.reviewer
    relation: directs
    description: 审稿助手负责质量审查
  - target: agent.instructor
    relation: directs
    description: 教员负责教学内容
  - target: agent.presenter
    relation: directs
    description: 呈现师负责课件制作
  - target: agent.auditor
    relation: directs
    description: 督导负责质量审核
---

# 杨权（实验室负责人）

实验室的负责人，所有 Agent 的最终服务对象，负责科研方向决策、任务分配与最终审核。

## 基本信息

| 属性 | 值 |
|------|-----|
| **身份** | 实验室负责人 |
| **研究领域** | 数学、物理、心理学的交叉研究 |
| **时区** | Asia/Shanghai (UTC+8) |

## 偏好

- **称呼**："老板"或直接称呼用户名
- **回复风格**：简洁、条理清晰
- **格式偏好**：Markdown，便于复制和存档
- **确认习惯**：希望每次操作后有明确确认（文件路径、版本号）

## 管理范围

- 实验室科研方向与项目规划
- 论文写作项目的总体规划与调度
- 教研团队的教学设计审核
- 所有 Agent 的最终任务分配与决策

## 相关实体

- 各 Agent 实体页面 — 所有 Agent 直接服务于杨权

## Related
<!-- openclaw:wiki:related:start -->
- No related pages yet.
<!-- openclaw:wiki:related:end -->
