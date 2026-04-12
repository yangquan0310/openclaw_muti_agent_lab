# SKILL.md - daily-maintenance

## 技能信息

| 属性 | 值 |
|------|-----|
| 技能名称 | daily-maintenance |
| 技能类型 | 定时任务 |
| 触发条件 | 每日自动执行 |
| 作者 | 心理学家 |

## 功能描述

本技能用于执行心理学家的每日维护任务，确保工作空间和文档的整洁有序。

## 任务清单

### 1. TOOLS维护
- [ ] 维护个人技能索引
- [ ] 维护个人脚本索引

### 2. MEMORY维护
- [ ] 维护任务看板
- [ ] 维护活跃子代理清单
- [ ] 维护程序性记忆脚本位置表
- [ ] 归档completed任务
- [ ] 清理killed任务

### 3. 工作空间维护
- [ ] 检查配置文件
- [ ] 维护临时文件夹
- [ ] 维护技能文件夹
- [ ] 维护脚本文件夹
- [ ] 删除多余文件

## Cron配置

```cron
0 4 * * * cd /root/.openclaw/workspace/psychologist && /usr/bin/openclaw sessions spawn --agent-id psychologist --label "psychologist-cron-daily-maintenance" --mode run --runtime subagent --task "执行心理学家每日维护任务"
```

## 日志位置

`~/实验室仓库/日志文件/cron_psychologist_*.log`
