# 每日维护

> 教务助手（academicassistant）的每日定时维护任务
> 执行时间：每日 04:00（Asia/Shanghai）
> 任务ID：`31db3717-398c-432b-800b-58b74e52a840`

---

## 功能概述

本技能负责教务助手工作空间的每日维护工作，包括：

### 1. 维护 TOOLS.md
- **维护个人技能索引**
  - 扫描 `~/.openclaw/workspace/academicassistant/skills/` 目录
  - 更新技能列表，路径指向各技能的 `SKILL.md`
  
- **维护个人脚本索引**
  - 扫描 `~/.openclaw/workspace/academicassistant/scripts/` 目录
  - 更新脚本列表，路径指向各脚本的 `SKILL.md`

- **维护项目表**
  - 检查「项目库」表格完整性
  - 更新项目列表和存储位置

### 2. 维护 MEMORY.md
- **维护任务看板**
  - 检查「当前活跃任务看板」状态
  - 清理已完成（completed）和已终止（killed）的任务
  
- **维护活跃子代理清单**
  - 检查子代理状态
  - 清理已完成的子代理记录
  
- **维护程序性记忆脚本位置表**
  - 扫描技能文件夹中的脚本
  - 更新脚本索引表（脚本名|功能|位置）
  - 确保位置指向 `SKILL.md`

### 3. 工作空间维护
- **检查配置文件**
  - 检查 `AGENTS.md`、`MEMORY.md`、`TOOLS.md` 等核心文件完整性
  
- **维护临时文件夹**
  - 清理 `~/.openclaw/workspace/academicassistant/temp/` 中超过7天的文件
  
- **维护技能文件夹**
  - 确保每个技能文件夹包含：`.py/.sh` + `SKILL.md` + `README.md`
  - 检查 `skills/README.md` 是否存在
  
- **维护脚本文件夹**
  - 确保脚本文件夹只包含 `.md` 文件
  - 检查 `scripts/README.md` 是否存在
  
- **删除多余文件**
  - 清理工作空间根目录下的非配置文件

---

## 触发条件

- **定时触发**：每日 04:00 自动执行
- **手动触发**：通过子代理调度执行

---

## 执行方式

```bash
# 手动执行
bash ~/.openclaw/workspace/academicassistant/skills/每日维护/每日维护.sh
```

---

## 输出

- **日志文件**：`~/教研室仓库/日志文件/YYYY-MM-DD/04-00-00-每日维护.md`
- **更新文件**：
  - `~/.openclaw/workspace/academicassistant/TOOLS.md`
  - `~/.openclaw/workspace/academicassistant/MEMORY.md`

---

## 依赖

- `MEMORY.md` 必须存在
- `TOOLS.md` 必须存在
- 工作空间目录结构完整

---

## 版本历史

- **v1.0.0** (2026-04-12)：初始版本，整合每日维护任务

---
*最后更新：2026-04-12*
