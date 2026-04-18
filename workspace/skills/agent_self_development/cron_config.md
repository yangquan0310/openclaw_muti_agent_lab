# agent_self_development 定时任务配置

> 定时任务配置文件
> 基于元认知理论和同化顺应理论设计

---

## 定时任务列表

| 执行时间 | 任务名称 | 功能描述 | 执行方式 | 所属模块 |
|----------|----------|----------|----------|----------|
| 每日 01:00 | 日记生成任务 | 读取前一天事件日志，生成发展日记 | 子代理执行 | assimilation_accommodation/diary_reader + diary |
| 每日 02:00 | 自我更新任务 | 阅读日记，执行同化/顺应，更新自我 | 子代理执行 | assimilation_accommodation/* |
| 每日 04:00 | 工作记忆清理 | 归档 completed 任务，删除 killed 任务 | 子代理执行 | working_memory/memory_table |

---

## 任务详细说明

### 任务1: 日记生成任务 (01:00)

**执行流程**:
```
01:00 触发
    ↓
[步骤1] diary_reader 扫描 memory/ 目录
    └── 读取前一天 (YYYY-MM-DD) 的所有事件日志
    ↓
[步骤2] 提取关键信息
    ├── 事件类型统计
    ├── 成功/失败统计
    └── 同化/顺应标记
    ↓
[步骤3] diary 生成发展日记
    └── 创建 diary/YYYY-MM-DD.md
    ↓
[步骤4] 记录执行日志
```

**输出文件**: `~/.openclaw/workspace/{agentId}/memory/diary/YYYY-MM-DD.md`

---

### 任务2: 自我更新任务 (02:00)

**执行流程**:
```
02:00 触发
    ↓
[步骤1] 读取当日发展日记
    └── diary/YYYY-MM-DD.md
    ↓
[步骤2] 分析同化/顺应清单
    ├── 统计同化事件数量和类型
    ├── 统计顺应事件数量和类型
    └── 评估认知结构变化需求
    ↓
[步骤3] 判断更新层次
    ├── 同化为主 → 更新程序性记忆
    │   └── 添加条件-行动规则到 MEMORY.md
    └── 顺应为主 → 执行相应更新
        ├── 第0层: personal_skills_update
        ├── 第1层: core_self_update
        ├── 第2层: belief_style_update
        ├── 第3层: identity_update
        └── 第4层: self_identity_update
    ↓
[步骤4] 记录更新日志
```

**更新目标**:
- `SOUL.md` - 信念和风格
- `IDENTITY.md` - 身份和角色
- `MEMORY.md` - 程序性记忆和事件记忆
- `skills/` - 个人技能

---

### 任务3: 工作记忆清理 (04:00)

**执行流程**:
```
04:00 触发
    ↓
[步骤1] 读取 MEMORY.md 工作记忆章节
    ↓
[步骤2] 扫描活跃子代理清单
    ↓
[步骤3] 处理 completed 任务
    ├── 归档到「事件记忆」表格
    └── 从清单中删除
    ↓
[步骤4] 处理 killed 任务
    ├── 直接删除（不归档）
    └── 从清单中删除
    ↓
[步骤5] 更新 MEMORY.md
    ↓
[步骤6] 记录清理日志
```

---

## 任务依赖关系

```
日记生成任务 (01:00)
        ↓
自我更新任务 (02:00) 依赖 日记生成任务完成
        ↓
工作记忆清理 (04:00) 独立执行
```

---

## 错误处理

| 错误场景 | 处理方式 |
|----------|----------|
| 无事件日志 | 生成空日记，记录"今日无事件" |
| 日记生成失败 | 记录错误，次日重试 |
| 自我更新失败 | 记录错误，标记待处理 |
| 文件读写错误 | 记录错误，通知用户 |

---

## 配置示例

```json
{
  "cron_tasks": [
    {
      "id": "diary-generation",
      "name": "日记生成任务",
      "schedule": "0 1 * * *",
      "timezone": "Asia/Shanghai",
      "skill_path": "agent_self_development/assimilation_accommodation/diary_reader",
      "enabled": true
    },
    {
      "id": "self-update",
      "name": "自我更新任务",
      "schedule": "0 2 * * *",
      "timezone": "Asia/Shanghai",
      "skill_path": "agent_self_development/assimilation_accommodation",
      "enabled": true
    },
    {
      "id": "working-memory-cleanup",
      "name": "工作记忆清理",
      "schedule": "0 4 * * *",
      "timezone": "Asia/Shanghai",
      "skill_path": "agent_self_development/working_memory/memory_table",
      "enabled": true
    }
  ]
}
```

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0.0 | 2026-04-17 | 初始版本 |

---

*创建者: 大管家*
*创建时间: 2026-04-17*
