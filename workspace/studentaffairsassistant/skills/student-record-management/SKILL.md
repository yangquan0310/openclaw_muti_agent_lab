---
name: student-record-management
description: >
  学生档案管理技能。创建、分类、存储、检索学生档案，确保学生信息完整、准确、安全。
  支持学生基本信息、学业记录、社团活动等多维度档案管理。
version: 1.0.0
author: studentaffairsassistant
dependencies: []
exports:
  - create_student_record
  - update_student_record
  - query_student_record
  - list_student_records
---

# student-record-management

> 学生档案管理技能
> 学工助手核心技能之一，支撑「学生信息管理员」角色

---

## 功能说明

本技能用于管理学生档案，包括：
- 创建学生档案（基本信息、学业记录、社团活动）
- 更新学生档案信息
- 检索和查询学生档案
- 列出所有学生档案
- 数据完整性检查

---

## 对象

### StudentRecord（学生档案对象）

| 属性 | 类型 | 说明 |
|------|------|------|
| `student_id` | string | 学生唯一标识（学号） |
| `name` | string | 学生姓名 |
| `gender` | string | 性别 |
| `major` | string | 专业 |
| `grade` | string | 年级 |
| `class` | string | 班级 |
| `contact` | object | 联系方式（电话、邮箱） |
| `academic_records` | object[] | 学业记录 |
| `club_activities` | object[] | 社团活动记录 |
| `created_at` | string | 档案创建时间 |
| `updated_at` | string | 档案最后更新时间 |

---

## 工作流

### 工作流1：创建学生档案

**步骤**：
1. 收集学生基本信息（学号、姓名、性别、专业、年级、班级）
2. 收集联系方式（电话、邮箱）
3. 创建档案文件（Markdown格式）
4. 存储到指定目录
5. 记录创建日志

**输出**：学生档案文件路径

### 工作流2：更新学生档案

**步骤**：
1. 根据学号检索档案
2. 更新指定字段
3. 记录更新时间
4. 保存更新

**输出**：更新后的档案文件路径

### 工作流3：查询学生档案

**步骤**：
1. 根据学号或姓名检索
2. 返回档案内容

**输出**：学生档案内容

### 工作流4：列出所有学生档案

**步骤**：
1. 扫描档案目录
2. 列出所有档案摘要

**输出**：学生档案列表

---

## 使用指南

### 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `student_id` | string | ✅ | 学生学号 |
| `name` | string | ✅ | 学生姓名 |
| `action` | string | ✅ | 操作类型（create/update/query/list） |

### 输出结果

| 输出项 | 格式 | 说明 |
|--------|------|------|
| `record_path` | string | 档案文件路径 |
| `record_content` | Markdown | 档案内容 |

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0.0 | 2026-04-30 | 初始版本，创建学生档案管理技能 |

---

*创建者: studentaffairsassistant*
*创建时间: 2026-04-30*