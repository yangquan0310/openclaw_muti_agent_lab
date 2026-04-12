# daily_maintenance 技能

## 功能描述

每日维护任务，合并执行 TOOLS.md 维护、MEMORY.md 维护、工作空间维护。

## 使用方式

```bash
bash skills/daily_maintenance/每日维护.sh
```

## 文件说明

- `每日维护.sh` - 主脚本
- `SKILL.md` - 技能说明文档
- `README.md` - 使用说明文档

## 维护内容

### 1. 维护 TOOLS.md
- 维护个人技能索引（检查 skills/ 文件夹结构）
- 维护个人脚本索引（检查 scripts/ 文件夹结构）

### 2. 维护 MEMORY.md
- 维护任务看板（检查 completed 任务待归档）
- 维护活跃子代理清单（统计 active/paused 任务）
- 维护程序性记忆脚本位置表（检查脚本索引完整性）

### 3. 工作空间维护
- 检查配置文件（AGENTS.md, SOUL.md, TOOLS.md, MEMORY.md, HEARTBEAT.md, USER.md, IDENTITY.md）
- 维护临时文件夹（删除7天前的文件）
- 维护技能文件夹（检查每个技能的结构完整性）
- 维护脚本文件夹（检查每个脚本的结构完整性）
- 删除多余文件（检查根目录下的非标准文件）

## 执行时间

每日 04:00 (Asia/Shanghai)

## 日志位置

`~/实验室仓库/日志文件/YYYY-MM-DD/04-00-00-reviewer-每日维护.log`

## 作者

审稿助手 (reviewer)
