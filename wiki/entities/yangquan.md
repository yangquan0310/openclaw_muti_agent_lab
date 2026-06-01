---
pageType: entity
entityType: user
id: entity.yangquan
createdAt: "2026-03-31T00:00:00+08:00"
updatedAt: "2026-05-23T19:15:00+08:00"
canonicalId: user.yangquan
aliases:
  - 杨权
  - 老板
  - 实验室负责人
sourceIds:
  - source.system-config
  - source.warehouse
  - source.yangquan-cv
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

## 基本信息

| 属性 | 值 |
|------|-----|
| **身份** | 心理学博士研究生（华中师范大学） |
| **出生年月** | 1996-03 |
| **性别** | 男 |
| **研究领域** | 数学、物理、心理学的交叉研究 |
| **电话** | 13657283452 |
| **邮箱** | yangquan0310@163.com |
| **个人主页** | [ORCID](https://orcid.org/0000-0001-6201-4174) · [GitHub](https://github.com/yangquan0310) |
| **时区** | Asia/Shanghai (UTC+8) |

## 教育背景

| 时间 | 学校 | 专业 | 学历 |
|------|------|------|------|
| 2014-09 ~ 2018-06 | — | — | 本科 |
| 2018-09 ~ 2021-06 | — | — | 硕士 |
| 2021-09 ~ 至今 | 华中师范大学 | 心理学 | 博士（在读） |

## 项目经历

| 项目 | 时间 | 角色 | 简介 |
|------|------|------|------|
| OpenClaw Multi-Agent Lab | 2026/03~至今 | 独立开发 | 基于管理学矩阵管理理论，构建 Agent 角色×项目双维度管理框架 |
| Agent Self-Development 插件 | 2026/03~至今 | 独立开发 | 基于博士论文交互式自传体记忆理论，增强 Agent 计划、监控与调节能力 |
| 回音室效应对中学生自我同一性发展的影响 | 2023/05~2024/05 | 主持 | 中国基础教育质量检测协同创新中心研究生自主课题 |
| 主观记忆减退老年人情节记忆研究 | 2017/01~2019/12 | 参与 | 国家自然科学基金青年项目（24万） |
| 青少年心理健康问题研究 | 2022~2025 | 参与 | 湖北省新型智库暨省社科基金重点项目 |

## 学术成果

### 期刊论文

| 年份 | 论文 | 期刊 | 备注 |
|------|------|------|------|
| 2024 | 不同自我同一性状态大学生的回音适应行为表现 | 心理与行为研究 | CSSCI, 第一作者 |
| 2020 | 跨期选择中的年龄差异及其机制 | 心理科学进展 | CSSCI, 第一作者 |
| 2021 | Time Unpacking Effect on Intertemporal Decision-Making | Frontiers in Psychology | SSCI, 第一作者 |
| 2020 | Social Support and the Incidence of Cognitive Impairment | Frontiers in Psychiatry | SSCI, 导师一作 |
| 2020 | Filial Expectations and Depressive Symptoms in Chinese Older Adults | Journal of Adult Development | SSCI, 共同一作 |
| 2024 | Age-Differential Role of Gaze Reinstatement in Recognition Memory | The Journals of Gerontology, Series B | SSCI/SCI 一区 top, 第一作者 |

### 博士论文
- **题目**：《数字化存储对自传体记忆的影响及其机制》
- **理论**：记忆系统研究 → 迁移至 Agent 记忆设计（分布式自传体记忆架构）

## 学术兼职

- 《Current Psychology》审稿人
- 《Frontiers in Psychology》审稿人

## 获奖经历

- 中国老年学和老年医学学会老年心理分会 2021 年度学术会议论文二等奖

## 偏好

- **称呼**："老板"或直接称呼用户名
- **回复风格**：简洁、条理清晰
- **格式偏好**：Markdown，便于复制和存档
- **确认习惯**：希望每次操作后有明确确认（文件路径、版本号）

## 管理范围

- 实验室科研方向与项目规划
- 论文写作项目的总体规划与调度（博士论文、学生论文修改）
- 教研团队的教学设计审核（《教育科学研究方法》课程）
- 所有 Agent 的最终任务分配与决策

## 相关实体

- 各 Agent 实体页面 — 所有 Agent 直接服务于杨权
- [[wangyaxin]] — 王雅欣（同事，武汉文理学院）

## Related

- [[entities/wangyaxin]]

## Related
<!-- openclaw:wiki:related:start -->
### Referenced By

- [[syntheses/2026-06-01-16-12-00-我的agent工程实践-harness与plugin双轮|我的 agent 工程实践：驾驭方法论]]
<!-- openclaw:wiki:related:end -->
