# SKILL.md - daily_maintenance

## 技能元数据

| 属性 | 值 |
|------|-----|
| **技能名称** | daily_maintenance |
| **技能类型** | 定时任务 |
| **版本** | 1.0.0 |
| **作者** | 审稿助手 (reviewer) |
| **创建时间** | 2026-04-12 |
| **定时任务ID** | `a1b2c3d4-e5f6-7890-abcd-ef1234567890` |
| **执行时间** | 每日 04:00 (Asia/Shanghai) |
| **cron表达式** | `0 4 * * *` |

## 触发条件

- 每日定时执行（04:00）
- 手动执行维护任务时

## 输入

无直接输入。

## 输出

1. 更新后的配置文件
2. 维护日志文件

## 执行方式

```bash
bash skills/daily_maintenance/每日维护.sh
```

## 任务详情

### 任务1：维护 TOOLS.md
- **维护个人技能索引** - 扫描 skills/ 文件夹，检查每个技能的 SKILL.md 和 README.md
- **维护个人脚本索引** - 扫描 scripts/ 文件夹，检查每个脚本的 .md 文件、SKILL.md 和 README.md
- **维护项目表** - 扫描 ~/实验室仓库/项目文件/，检查每个项目的 README.md

### 任务2：维护 MEMORY.md
- **维护任务看板** - 检查并归档 completed 状态任务到事件记忆
- **维护活跃子代理清单** - 统计 active/paused/killed 任务，清理 killed 任务
- **维护程序性记忆脚本位置表** - 检查脚本索引完整性，验证脚本位置正确性

### 任务3：工作空间维护
- **核查配置文件缺失** - 检查 AGENTS.md, SOUL.md, TOOLS.md, MEMORY.md, HEARTBEAT.md, USER.md, IDENTITY.md，自动创建缺失文件
- **维护临时文件夹** - 删除7天前的临时文件，删除空目录
- **维护技能文件夹** - 检查每个技能文件夹包含 SKILL.md 和 README.md
- **维护脚本文件夹** - 检查每个脚本文件夹包含核心 .md 文件、SKILL.md 和 README.md
- **删除多余文件** - 检查并自动删除根目录下的非标准文件/目录

## 文件结构

```
skills/daily_maintenance/
├── 每日维护.sh       # 主脚本
├── SKILL.md          # 技能元数据
└── README.md         # 使用说明
```

## 定时配置

cron 表达式：`0 4 * * *`

## 注意事项

- 需要写入多个目录的权限
- 日志会自动按日期归档
