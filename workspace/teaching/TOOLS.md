# TOOLS.md

> 配置档案

---

## 存储位置

### 公共存储位置

| 文件 | 存储路径 | 说明 |
|----------|----------|------|
| 技能文件夹 | ~/.openclaw/workspace/skills/README.md | 存放了所有技能文件（公共技能） |
| API密钥存储 | ~/.openclaw/.env | 安全存储所有API密钥 |
| 实验室仓库 | ~/实验室仓库/README.md | 实验室仓库 |
| 教研室仓库 | ~/教研室仓库/README.md | 教学研究、教务管理和学生工作相关文件存储 |

### 私人存储位置

| 文件 | 存储路径 | 说明 |
|----------|----------|------|
| Agent 个人记忆 | ~/.openclaw/workspace/teaching/MEMORY.md | 教学助手独立维护 |
| Agent 个人技能 | ~/.openclaw/workspace/teaching/skills/README.md | 教学助手专属技能存储目录 |
| Agent 临时文件 | ~/.openclaw/workspace/teaching/temp/README.md | 教学助手专属临时文件存储目录 |
| Agent 工作记忆 | ~/.openclaw/workspace/teaching/memory/ | OpenClaw核心记忆系统数据（由memory-core维护） |
| **Agent 发展日记** | ~/.openclaw/workspace/teaching/diary/YYYY-MM-DD.md | 每日自我发展总结（由agent-self-development维护） |
| **Agent 事件记录** | ~/.openclaw/workspace/teaching/events/YYYY-MM-DD/{HH-MM-SS-事件}.md | 详细事件记录（由agent-self-development维护） |
| 教学助手仓库 |	~/教研室仓库/备课资料/README.MD	|教学助手用来进行工作的文件夹、其他成员不可以写入，只能读取|
| 课程项目 |	~/教研室仓库/备课资料/项目文件/README.MD	|教学助手用来存储项目的文件夹、其他成员不可以写入，只能读取|
---

## 教研室仓库结构

```
~/教研室仓库/
├── 主任信息/                   # 教研室主任个人信息和学术资料
├── 备课资料/                   # 课程准备材料
├── 学生工作/                   # 学生管理和辅导
├── 教务归档/                   # 教学教务文件归档
└── 日程文件/                   # 教学日程安排
```

## 项目

### 项目结构
> 项目结构详见 ~/教研室仓库/备课资料/项目文件/README.md



### 项目库
> 项目索引详见 ~/教研室仓库/备课资料/项目文件/README.md
---

## 技能索引

### 公共技能索引
> 完整列表见: `/root/.openclaw/workspace/skills/README.md`

---

### 个人技能索引
> 完整列表见: `/root/.openclaw/workspace/teaching/skills/README.md`

---

*最后重构: 2026-04-17*
*重构者: 教学助手*
