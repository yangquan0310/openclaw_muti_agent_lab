# SKILL.md - memory_maintenance

## 技能元数据

| 属性 | 值 |
|------|-----|
| **技能名称** | memory_maintenance |
| **技能类型** | 系统维护 |
| **版本** | 1.0.0 |
| **作者** | 审稿助手 (reviewer) |
| **创建时间** | 2026-04-10 |

## 触发条件

- 每日维护任务执行时
- 需要手动清理工作记忆时

## 输入

- `~/.openclaw/workspace/reviewer/MEMORY.md`

## 输出

1. 更新后的 MEMORY.md（删除已归档任务）
2. 维护日志文件

## 执行方式

```bash
bash skills/memory_maintenance/维护工作记忆.sh
```

## 处理逻辑

| 任务状态 | 处理方式 | 是否归档 |
|----------|----------|----------|
| completed | 从活跃清单删除 | ✅ 是 |
| killed | 从活跃清单删除 | ❌ 否 |
| active | 保留在清单中 | - |
| paused | 保留在清单中 | - |

## 文件结构

```
skills/memory_maintenance/
├── 维护工作记忆.sh    # 主脚本
├── SKILL.md          # 技能元数据
└── README.md         # 使用说明
```

## 注意事项

- 只归档 completed 状态的任务
- killed 状态的任务直接删除，不进入历史记录
- 保留 active 和 paused 状态的任务在清单中
