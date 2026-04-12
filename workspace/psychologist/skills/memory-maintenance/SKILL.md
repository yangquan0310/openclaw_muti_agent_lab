# SKILL.md - memory-maintenance

## 技能信息

| 属性 | 值 |
|------|-----|
| 技能名称 | memory-maintenance |
| 技能类型 | 记忆管理 |
| 触发条件 | 需要维护工作记忆 |
| 作者 | 心理学家 |

## 功能描述

本技能用于维护心理学家的长期记忆文件（MEMORY.md），确保工作记忆的准确性和时效性。

## 维护内容

### 工作记忆清理
1. 扫描「活跃子代理清单」
2. 将`completed`状态任务归档到「事件记忆」
3. 直接删除`killed`状态任务
4. 从清单中移除已处理任务

### 归档规则
- 只归档`completed`状态的任务
- `killed`状态的任务直接删除，不入历史记录
- 保留`active`和`paused`状态的任务

## 使用示例

```bash
bash memory-maintenance.sh
```

## 注意事项

- 执行前建议备份MEMORY.md
- 清理操作不可逆
