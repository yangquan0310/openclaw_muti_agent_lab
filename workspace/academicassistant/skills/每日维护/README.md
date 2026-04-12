# 每日维护

教务助手（academicassistant）的每日定时维护脚本。

## 功能

### 维护 TOOLS.md
- 维护个人技能索引（扫描 skills/ 目录，路径指向 SKILL.md）
- 维护个人脚本索引（扫描 scripts/ 目录，路径指向 SKILL.md）

### 维护 MEMORY.md
- 维护任务看板（清理 completed/killed 任务）
- 维护活跃子代理清单（清理已完成子代理）
- 维护程序性记忆脚本位置表（脚本名|功能|位置）

### 工作空间维护
- 检查配置文件完整性
- 维护临时文件夹（清理超过7天的文件）
- 维护技能文件夹（确保 .py/.sh + SKILL.md + README.md）
- 维护脚本文件夹（确保只包含 .md 文件）
- 删除多余文件

## 使用

```bash
bash ~/.openclaw/workspace/academicassistant/skills/每日维护/每日维护.sh
```

## 定时任务

- **执行时间**：每日 04:00
- **时区**：Asia/Shanghai
- **任务ID**：`31db3717-398c-432b-800b-58b74e52a840`

## 日志

日志保存在：`~/教研室仓库/日志文件/YYYY-MM-DD/04-00-00-每日维护.md`
