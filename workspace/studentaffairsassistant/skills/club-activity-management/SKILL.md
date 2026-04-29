---
name: club-activity-management
description: >
  社团活动管理技能。记录社团活动计划、管理社团成员信息、记录活动过程、生成活动总结报告。
  支持活动策划、成员管理、场地协调、活动评估等功能。
version: 1.0.0
author: studentaffairsassistant
dependencies:
  - student-record-management
exports:
  - create_activity_plan
  - manage_club_members
  - record_activity_process
  - generate_activity_summary
---

# club-activity-management

> 社团活动管理技能
> 学工助手核心技能之一，支撑「社团活动组织者」角色

---

## 功能说明

本技能用于管理社团活动，包括：
- 记录社团活动计划
- 管理社团成员信息
- 记录活动过程
- 生成活动总结报告
- 协调场地和资源

---

## 对象

### ActivityPlan（活动计划对象）

| 属性 | 类型 | 说明 |
|------|------|------|
| `plan_id` | string | 计划唯一标识 |
| `activity_name` | string | 活动名称 |
| `club_name` | string | 社团名称 |
| `activity_type` | string | 活动类型（学术/文体/公益/其他） |
| `description` | string | 活动描述 |
| `schedule` | object | 时间安排 |
| `location` | string | 活动地点 |
| `budget` | number | 预算 |
| `responsible` | string | 负责人 |
| `participants` | string[] | 参与人员 |
| `status` | string | 状态（策划中/进行中/已完成/已取消） |
| `created_at` | string | 创建时间 |

### ActivityRecord（活动记录对象）

| 属性 | 类型 | 说明 |
|------|------|------|
| `record_id` | string | 记录唯一标识 |
| `plan_id` | string | 关联的计划ID |
| `actual_date` | string | 实际活动日期 |
| `actual_location` | string | 实际活动地点 |
| `attendance` | object[] | 出席记录 |
| `process` | string | 活动过程记录 |
| `photos` | string[] | 活动照片 |
| `issues` | string[] | 遇到的问题 |
| `feedback` | string[] | 参与者反馈 |

---

## 工作流

### 工作流1：创建活动计划

**步骤**：
1. 收集活动基本信息（名称、社团、类型）
2. 制定活动方案（描述、目标）
3. 安排时间地点
4. 编制预算
5. 确定负责人和参与人员
6. 创建活动计划

**输出**：活动计划文件路径

### 工作流2：管理社团成员

**步骤**：
1. 收集成员基本信息
2. 记录成员角色和职责
3. 更新成员状态

**输出**：成员列表文件路径

### 工作流3：记录活动过程

**步骤**：
1. 活动前准备确认
2. 记录活动出席情况
3. 记录活动过程
4. 收集活动照片
5. 记录遇到的问题
6. 收集参与者反馈

**输出**：活动记录文件路径

### 工作流4：生成活动总结

**步骤**：
1. 收集活动记录
2. 统计参与情况
3. 分析活动效果
4. 总结经验教训
5. 生成总结报告

**输出**：活动总结报告

---

## 使用指南

### 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `activity_name` | string | ✅ | 活动名称 |
| `club_name` | string | ✅ | 社团名称 |
| `action` | string | ✅ | 操作类型（plan/member/record/summary） |

### 输出结果

| 输出项 | 格式 | 说明 |
|--------|------|------|
| `plan_path` | string | 计划文件路径 |
| `record_path` | string | 记录文件路径 |
| `summary_content` | Markdown | 总结报告 |

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0.0 | 2026-04-30 | 初始版本，创建社团活动管理技能 |

---

*创建者: studentaffairsassistant*
*创建时间: 2026-04-30*