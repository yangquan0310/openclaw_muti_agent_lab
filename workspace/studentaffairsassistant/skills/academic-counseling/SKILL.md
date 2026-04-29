---
name: academic-counseling
description: >
  学业辅导记录技能。记录学生学业问题、制定辅导计划、跟踪辅导效果、生成学业分析报告。
  支持学业困难识别、辅导资源协调、效果评估等功能。
version: 1.0.0
author: studentaffairsassistant
dependencies:
  - student-record-management
exports:
  - record_academic_issue
  - create_counseling_plan
  - track_counseling_progress
  - generate_academic_report
---

# academic-counseling

> 学业辅导记录技能
> 学工助手核心技能之一，支撑「学业辅导协调员」角色

---

## 功能说明

本技能用于管理学业辅导工作，包括：
- 记录学生学业问题
- 制定辅导计划
- 跟踪辅导效果
- 生成学业分析报告
- 协调辅导资源

---

## 对象

### CounselingRecord（辅导记录对象）

| 属性 | 类型 | 说明 |
|------|------|------|
| `record_id` | string | 记录唯一标识 |
| `student_id` | string | 学生学号 |
| `issue_type` | string | 问题类型（学习困难/方法不当/态度问题/其他） |
| `issue_description` | string | 问题描述 |
| `severity` | string | 严重程度（高/中/低） |
| `counseling_plan` | object | 辅导计划 |
| `progress_records` | object[] | 进度记录 |
| `status` | string | 状态（进行中/已完成/已转介） |
| `created_at` | string | 记录创建时间 |
| `updated_at` | string | 记录最后更新时间 |

### CounselingPlan（辅导计划对象）

| 属性 | 类型 | 说明 |
|------|------|------|
| `plan_id` | string | 计划唯一标识 |
| `goals` | string[] | 辅导目标 |
| `methods` | string[] | 辅导方法 |
| `resources` | string[] | 所需资源 |
| `timeline` | string | 时间计划 |
| `responsible` | string | 负责人 |

---

## 工作流

### 工作流1：记录学业问题

**步骤**：
1. 收集学生基本信息（学号、姓名）
2. 收集问题描述（类型、具体表现、持续时间）
3. 评估严重程度
4. 创建问题记录
5. 存储到指定目录

**输出**：问题记录文件路径

### 工作流2：制定辅导计划

**步骤**：
1. 分析问题记录
2. 确定辅导目标
3. 选择辅导方法
4. 协调所需资源
5. 制定时间计划
6. 指定负责人
7. 创建辅导计划

**输出**：辅导计划文件路径

### 工作流3：跟踪辅导进度

**步骤**：
1. 根据记录ID检索辅导记录
2. 记录辅导进展
3. 更新辅导状态
4. 记录辅导效果

**输出**：更新后的辅导记录

### 工作流4：生成学业分析报告

**步骤**：
1. 收集学生学业数据
2. 分析问题模式
3. 生成分析报告
4. 提供改进建议

**输出**：学业分析报告

---

## 使用指南

### 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `student_id` | string | ✅ | 学生学号 |
| `issue_type` | string | ✅ | 问题类型 |
| `action` | string | ✅ | 操作类型（record/plan/track/report） |

### 输出结果

| 输出项 | 格式 | 说明 |
|--------|------|------|
| `record_path` | string | 记录文件路径 |
| `record_content` | Markdown | 记录内容 |

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0.0 | 2026-04-30 | 初始版本，创建学业辅导记录技能 |

---

*创建者: studentaffairsassistant*
*创建时间: 2026-04-30*
