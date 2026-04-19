# diary_reader

> 同化与顺应 - 日记阅读器
> 读取事件日志，为日记生成提供素材

---

## 概述

日记阅读器负责扫描和读取 `events/` 目录下的事件日志文件，提取关键信息并按时间排序，为发展日记的生成提供结构化素材。

---

## 核心功能

### 1. 扫描事件日志

**扫描范围**:
- **目录**: `~/.openclaw/workspace/{agentId}/events/YYYY-MM-DD/`
- **模式**: `*.md` 文件
- **格式**: `HH-MM-SS-*.md`

**文件筛选**:
```
events/YYYY-MM-DD/HH-MM-SS-*.md 格式文件
    ↓
提取日期和时间戳
    ↓
按时间排序
```

### 2. 读取事件内容

**读取的章节**:
| 章节 | 用途 | 重要性 |
|------|------|--------|
| 基本信息 | 时间、类型、项目 | 高 |
| 事件描述 | 背景、触发条件 | 中 |
| 元认知阶段 | 计划/监控/调节信息 | 高 |
| 执行结果 | 结果状态、与预期对比 | 高 |
| 经验总结 | 成功经验、新发现 | 高 |
| 日记标记 | 同化/顺应标记 | 高 |

### 3. 信息提取

**提取字段**:
```json
{
  "filename": "HH-MM-SS-事件.md",
  "timestamp": "HH:MM:SS",
  "event_type": "创建/监控/调节/完成/终止",
  "project": "项目名称",
  "subagent_key": "子代理key",
  "result_status": "成功/失败/部分成功",
  "assimilation_marked": true/false,
  "accommodation_marked": true/false,
  "success_pattern": "成功模式描述",
  "failure_lesson": "失败教训描述",
  "new_discovery": "新发现描述"
}
```

### 4. 按日期筛选

**筛选逻辑**:
```
指定日期: YYYY-MM-DD
    ↓
计算前一天日期
    ↓
读取 events/YYYY-MM-DD/*.md
    ↓
按时间排序 (HH:MM:SS)
```

---

## 使用流程

### 定时任务流程 (每日 01:00)

```
触发定时任务
    ↓
[步骤1] 确定目标日期
    └── 前一天: YYYY-MM-DD
    ↓
[步骤2] 扫描 events/YYYY-MM-DD/ 目录
    └── 获取所有 *.md 文件
    ↓
[步骤3] 读取文件内容
    └── 提取关键章节和信息
    ↓
[步骤4] 结构化处理
    ├── 按时间排序
    ├── 分类统计
    └── 提取同化/顺应标记
    ↓
[步骤5] 输出给 diary 模块
    └── 生成发展日记
```

### 手动执行流程

```
需要回顾特定日期时
    ↓
[步骤1] 指定日期范围
    └── 开始日期 + 结束日期
    ↓
[步骤2] 扫描并筛选
    └── 读取 events/YYYY-MM-DD/*.md
    ↓
[步骤3] 读取并结构化
    ↓
[步骤4] 输出结果
```

---

## 输出格式

### 结构化事件列表

```json
{
  "date": "YYYY-MM-DD",
  "total_events": 5,
  "events": [
    {
      "time": "14:30:00",
      "type": "创建",
      "description": "创建文献检索子代理",
      "result": "成功",
      "assimilation": false,
      "accommodation": false
    },
    {
      "time": "15:45:00",
      "type": "监控",
      "description": "检测到进度偏差",
      "result": "部分成功",
      "assimilation": false,
      "accommodation": true,
      "lesson": "需要调整检索策略"
    }
  ],
  "statistics": {
    "success_count": 3,
    "failure_count": 1,
    "partial_count": 1,
    "assimilation_count": 2,
    "accommodation_count": 1
  }
}
```

---

## 与 diary 的关系

```
diary_reader (读取事件)
    ├── 扫描 events/YYYY-MM-DD/*.md
    ├── 读取文件内容
    ├── 提取关键信息
    └── 结构化处理
            ↓
    diary (生成日记)
        ├── 接收结构化事件列表
        ├── 分析模式
        ├── 判断同化/顺应
        └── 生成 diary/YYYY-MM-DD.md
```

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.1.0 | 2026-04-19 | 更新存储路径：memory/ → events/ |
| v1.0.0 | 2026-04-17 | 初始版本 |

---

*创建者: 大管家*  
*创建时间: 2026-04-17*  
*最后更新: 2026-04-19*
