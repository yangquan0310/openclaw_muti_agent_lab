# memory_maintenance 技能

## 功能描述

工作记忆维护脚本，清理非活跃任务，归档到事件记忆。

## 使用方式

```bash
bash skills/memory_maintenance/维护工作记忆.sh
```

## 文件说明

- `维护工作记忆.sh` - 主脚本
- `SKILL.md` - 技能说明文档
- `README.md` - 使用说明文档

## 功能

1. 扫描 MEMORY.md 中的活跃子代理清单
2. 提取 completed 和 killed 状态的任务
3. 归档 completed 任务到事件记忆
4. 删除 killed 任务（不归档）
5. 生成维护日志

## 日志位置

`~/实验室仓库/日志文件/YYYY-MM-DD/04-00-00-reviewer-工作记忆维护.md`

## 作者

审稿助手 (reviewer)
