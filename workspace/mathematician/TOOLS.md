# TOOLS.md

> 配置档案

---

## 存储位置

### 公共存储位置
> 条目由大管家统一维护
> 实验室仓库、实验室项目等实验室相关内容同步给实验室成员
> 教研室仓库、教学助手仓库、教务助手仓库、学工助手仓库等教研室相关内容同步给教研室成员
| 文件 | 存储路径 | 说明 |
|----------|----------|------|
| 技能文件夹 | ~/.openclaw/workspace/skills/README.md | 存放了所有技能文件（公共技能） |
| API密钥存储 | ~/.openclaw/.env | 安全存储所有API密钥 |
| 实验室仓库 | ~/实验室仓库/README.md | 实验室仓库 |
| 教研室仓库 | ~/教研室仓库/README.md | 教学研究、教务管理和学生工作相关文件存储 |

### 私人存储位置

| 文件 | 存储路径 | 说明 |
|----------|----------|------|
| Agent 个人记忆 | ~/.openclaw/workspace/mathematician/MEMORY.md | 数学家独立维护 |
| Agent 个人技能 | ~/.openclaw/workspace/mathematician/skills/ | 个人技能存储目录 |
| Agent 临时文件 | ~/.openclaw/workspace/mathematician/temp/ | 临时文件存储目录 |
| **Agent 发展日记** | ~/.openclaw/workspace/mathematician/diary/YYYY-MM-DD.md | 每日自我发展总结（由agent-self-development维护） |
| **Agent 事件记录** | ~/.openclaw/workspace/mathematician/events/YYYY-MM-DD/{HH-MM-SS-事件}.md | 详细事件记录（由agent-self-development维护） |
| Agent 工作记忆 | ~/.openclaw/workspace/mathematician/memory/ | OpenClaw核心记忆系统数据（由memory-core维护） |
| 实验室仓库 | ~/实验室仓库/README.md | 实验室仓库 |
| 实验室项目 | ~/实验室仓库/项目文件/README.md | 实验室各个项目 |
| 项目元数据 | ~/实验室仓库/项目文件/{项目名}/元数据.json | 项目信息 |
| 项目知识库 | ~/实验室仓库/项目文件/{项目名}/知识库/index.json | 项目专属文献知识库索引 |
---

## 实验室仓库结构

```
~/实验室仓库/
├── 日程管理/                   # 日程管理
├── 项目文件/                   # 研究项目
├── 心跳报告/                   # 心跳检查报告
└── README.md                   # 仓库说明
```

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
> 项目结构详见 ~/实验室仓库/项目文件/README.md

### 项目库
> 项目索引详见 ~/实验室仓库/项目文件/README.md

## 技能索引

### 公共技能索引
> 完整列表见: `/root/.openclaw/workspace/skills/README.md`
---

### 个人技能索引
> 完整列表见: `/root/.openclaw/workspace/mathematician/skills/README.md`


---
*最后重构: 2026-04-16*
*重构者: 数学家*
