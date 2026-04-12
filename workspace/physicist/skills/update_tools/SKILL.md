# update_tools

> 物理学家专属技能

---

## 功能描述

自动更新 TOOLS.md 文件，包括：
1. 更新存储位置表（添加脚本存储位置）
2. 更新项目列表（扫描项目文件夹）
3. 更新脚本索引（从 MEMORY.md 提取）

## 使用方法

```bash
bash ~/.openclaw/workspace/physicist/skills/update_tools/update_tools.sh
```

## 触发条件

- 每日维护任务的一部分
- TOOLS.md 需要更新时

## 输入

- TOOLS.md：工具配置文件
- MEMORY.md：工作记忆文件（提取脚本索引）
- ~/实验室仓库/项目文件/：项目目录

## 输出

- 更新后的 TOOLS.md
- 备份文件：TOOLS.md.backup.YYYY-MM-DD
- 日志文件：~/实验室仓库/日志文件/YYYY-MM-DD/HH-MM-SS-[physicist]-[TOOLS更新].md

## 更新内容

1. **存储位置表**：确保脚本存储位置条目存在
2. **项目列表**：扫描项目文件夹，更新项目库
3. **脚本索引**：从 MEMORY.md 提取脚本信息

## 依赖

- bash
- awk
- grep
- date

---

*最后更新：2026-04-12*
