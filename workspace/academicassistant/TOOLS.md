# TOOLS.md

> 配置档案

---

## 存储位置

>技能文件夹、API密钥存储所有代理都有
>实验室仓库、实验室项目同步给实验室成员
>教研室仓库、教学助手仓库、教务助手仓库、学工助手仓库同步给教研室成员

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
| Agent 个人记忆 | ~/.openclaw/workspace/academicassistant/MEMORY.md | 教务助手独立维护 |
| Agent 个人技能 | ~/.openclaw/workspace/academicassistant/skills/README.md | 教务助手专属技能存储目录 |
| Agent 临时文件 | ~/.openclaw/workspace/academicassistant/temp/README.md | 教务助手专属临时文件存储目录 |
| Agent 工作记忆 | ~/.openclaw/workspace/academicassistant/memory/ | OpenClaw核心记忆系统数据（由memory-core维护） |
| **Agent 发展日记** | ~/.openclaw/workspace/academicassistant/diary/YYYY-MM-DD.md | 每日自我发展总结（由agent-self-development维护） |
| **Agent 事件记录** | ~/.openclaw/workspace/academicassistant/events/YYYY-MM-DD/{HH-MM-SS-事件}.md | 详细事件记录（由agent-self-development维护） |
| 教务助手仓库 |	~/教研室仓库/教务归档/README.MD	|教务助手用来进行工作的文件夹、其他成员不可以写入，只能读取|
| 教务助手项目 |	~/教研室仓库/教务归档/项目文件/README.MD	|教务助手用来存储项目的文件夹、其他成员不可以写入，只能读取|
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

## 项目

### 项目结构
> 项目结构详见 ~/教研室仓库/教务归档/项目文件/README.md
```
项目文件/
└── YYYY-MM-DD_项目名/
    ├── 文档/                  # 用户上传的文档
    ├── 草稿/                   # 论文草稿
    ├── 终稿/                   # 最终版本
    ├── 课程大纲/                   # 课程大纲
    ├── 知识库/                 # 项目专属知识库
    │   └── 索引.json          # 文献索引
    ├── 元数据.json             # 项目元数据
    └── README.md               # 项目说明
```



### 项目库
> 项目索引详见 ~/教研室仓库/教务归档/项目文件/README.md

---
## 索引

### 公共技能索引
> 完整列表见: `/root/.openclaw/workspace/skills/README.md`

---

### 个人技能索引
> 完整列表见: `/root/.openclaw/workspace/academicassistant/skills/README.md`


---

*最后重构: 2026-04-19
*重构者: 教务助手*
