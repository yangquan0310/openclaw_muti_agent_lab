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
| Agent 个人记忆 | ~/.openclaw/workspace/steward/MEMORY.md | 大管家独立维护 |
| Agent 个人技能 | ~/.openclaw/workspace/steward/skills/README.md | 技能存储目录说明 |
| Agent 临时文件 | ~/.openclaw/workspace/steward/temp/README.md | 临时文件存储目录说明 |
| Agent 工作日志 | ~/.openclaw/workspace/steward/memory/ | 发展日记与事件记忆存储目录，按 YYYY-MM-DD/ 归档 |
| 实验室仓库 | ~/实验室仓库/README.md | 实验室仓库 |
| 实验室项目 | ~/实验室仓库/项目文件/README.md | 实验室各个项目 |
| 项目知识库 | ~/实验室仓库/项目文件/{项目名}/知识库/index.json | 项目专属文献知识库索引 |

---

## 成员工作空间

| 称呼 | Agent ID | 工作空间 | Agent目录 |
|------|----------|----------|-----------|
| 大管家 | Steward | /root/.openclaw/workspace/steward | /root/.openclaw/agents/steward/agent |
| 数学家 | mathematician | /root/.openclaw/workspace/mathematician | /root/.openclaw/agents/mathematician/agent |
| 物理学家 | physicist | /root/.openclaw/workspace/physicist | /root/.openclaw/agents/physicist/agent |
| 心理学家 | psychologist | /root/.openclaw/workspace/psychologist | /root/.openclaw/agents/psychologist/agent |
| 写作助手 | writer | /root/.openclaw/workspace/writer | /root/.openclaw/agents/writer/agent |
| 审稿助手 | reviewer | /root/.openclaw/workspace/reviewer | /root/.openclaw/agents/reviewer/agent |
| 教学助手 | teaching | /root/.openclaw/workspace/teaching | /root/.openclaw/agents/teaching/agent |
| 教务助手 | academicassistant | /root/.openclaw/workspace/academicassistant | /root/.openclaw/agents/academicassistant/agent |
| 学工助手 | studentaffairsassistant | /root/.openclaw/workspace/studentaffairsassistant | /root/.openclaw/agents/studentaffairsassistant/agent |

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
```
项目文件/
└── 项目名/
    ├── 文档/                  # 用户上传的文档
    ├── 草稿/                   # 论文草稿
    ├── 终稿/                   # 最终版本
    ├── 知识库/                 # 项目专属知识库
    │   └── 索引.json          # 文献索引
    ├── 元数据.json             # 项目元数据
    └── README.md               # 项目说明
```

### 项目库

| 项目名 | 存储位置 | 描述 |
|--------|----------|------|
| AI降重提示工程 | ~/实验室仓库/项目文件/AI降重提示工程/ | 研究AI降重提示工程的方法和技巧 |
| 数字化存储与自传体记忆 | ~/实验室仓库/项目文件/数字化存储与自传体记忆/ | 研究数字化存储对自传体记忆的影响机制 |
| 跨期选择的年龄差异 | ~/实验室仓库/项目文件/跨期选择的年龄差异/ | 研究不同年龄群体在跨期选择任务中的决策差异 |
| 影响者营销中的自我扩展机制 | ~/实验室仓库/项目文件/影响者营销中的自我扩展机制/ | 研究影响者营销中自我扩展机制对消费意愿的影响 |
| Zotero文件管理 | ~/实验室仓库/项目文件/Zotero文件管理/ | Zotero文献管理和学习项目 |
| 审稿学习 | ~/实验室仓库/项目文件/审稿学习/ | 审稿学习项目，包含各类审稿范文 |
| 科研实验室搭建 | ~/实验室仓库/项目文件/科研实验室搭建/ | 基于心理学理论重构Agent配置体系，介绍实验室搭建方法 |
| 范文学习 | ~/实验室仓库/项目文件/范文学习/ | 范文学习项目，包含各类论文范文和写作模板 |
| 维护老板信息 | ~/实验室仓库/项目文件/维护老板信息/ | 老板的个人信息、学术成就和账户信息管理项目 |
| 学生论文修改 | ~/实验室仓库/项目文件/学生论文修改/ | 学生论文修改指导项目，包含论文原始版本和修改记录 |
| 内卷感知与工作繁荣 | ~/实验室仓库/项目文件/内卷感知与工作繁荣/ | 研究内卷感知对工作繁荣的影响机制 |
| AI降重提示工程 | ~/实验室仓库/项目文件/AI降重提示工程/ | 研究AI降重提示工程的方法和技巧 |
---

## 索引

### 公共技能索引
> 完整列表见: `/root/.openclaw/workspace/skills/README.md`

---

### 个人技能索引
> 完整列表见: `/root/.openclaw/workspace/steward/skills/README.md`

---

*最后重构: 2026-04-19*
*重构者: 大管家*