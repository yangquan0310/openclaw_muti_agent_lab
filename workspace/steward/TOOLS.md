# TOOLS.md

> 配置档案
> 大管家按要求对公共内容进行维护
> 私有内容各代理独自维护

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
| 技能文件夹 | ~/.openclaw/skills/ | 存放了所有技能文件（结构化程序） |
| 脚本文件夹 | ~/.openclaw/scripts/ | 存放了所有脚本文件（非结构化Markdown） |
| API密钥存储 | ~/.openclaw/.env | 安全存储所有API密钥 |
| 实验室仓库 | ~/实验室仓库/ | 实验室仓库 |
| 实验室项目 |~/实验室仓库/项目文件/|实验室各个项目|
| 教研室仓库 | ~/教研室仓库/ | 教学研究、教务管理和学生工作相关文件存储 |
|教学助手仓库|	~/教研室仓库/备课资料/	|教学助手用来进行工作的文件夹、其他成员不可以写入，只能读取|
|教务助手仓库|	~/教研室仓库/教务归档/	|教务助手用来进行工作的文件夹、其他成员不可以写入，只能读取|
|学工助手仓库|	~/教研室仓库/学生工作/	|学工助手用来进行工作的文件夹、其他成员不可以写入，只能读取|

### 私人存储位置
> 大管家维护格式
> 内容由各代理独立维护
| 文件 | 存储路径 | 说明 |
|----------|----------|------|
| Agent 个人记忆 | ~/.openclaw/workspace/steward/MEMORY.md | 大管家独立维护 |
| Agent 个人脚本 | ~/.openclaw/workspace/steward/scripts/README.md | 非结构化脚本存储目录说明 |
| Agent 个人技能 | ~/.openclaw/workspace/steward/skills/README.md | 结构化技能存储目录说明 |
| Agent 临时文件 | ~/.openclaw/workspace/steward/temp/README.md | 临时文件存储目录说明 |
| 工作日志 | ~/实验室仓库/日志文件/README.MD | 任务执行记录 |
---

## 成员工作空间
> 仅大管家需要知道
> 不要同步给其他代理

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
> 只同步给数学家、物理学家、心理学家、写作助手和审稿助手
> 不同步给教学助手、教务助手和学工助手
```
~/实验室仓库/
├── 日程管理/                   # 日程管理
├── 日志文件/                   # Agent工作日志
├── 项目文件/                   # 研究项目
├── 心跳报告/                   # 心跳检查报告
└── README.md                   # 仓库说明
```
---

## 教研室仓库结构
> 只同步给教学助手、教务助手和学工助手
> 不同步给数学家、物理学家、心理学家、写作助手和审稿助手
```
~/教研室仓库/
├── 主任信息/                   # 教研室主任个人信息和学术资料
├── 备课资料/                   # 课程准备材料
├── 学生工作/                   # 学生管理和辅导
├── 教务归档/                   # 教学教务文件归档
├── 日志文件/                   # 教学相关日志记录
└── 日程文件/                   # 教学日程安排
```

## 项目
> 各个代理独立维护

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
> 大管家维护格式
> 内容由各代理独立维护

| 项目名 | 存储位置 | 描述 |
|--------|----------|------|
| AI降重提示工程 | ~/实验室仓库/项目文件/AI降重提示工程/ | AI降重提示工程 |
| Zotero文件管理 | ~/实验室仓库/项目文件/Zotero文件管理/ | Zotero文件管理 |
| 内卷感知与工作繁荣 | ~/实验室仓库/项目文件/内卷感知与工作繁荣/ | |
| 学生论文修改 | ~/实验室仓库/项目文件/学生论文修改/ | 学生论文修改 |
| 审稿学习 | ~/实验室仓库/项目文件/审稿学习/ | 审稿学习 |
| 影响者营销中的自我扩展机制 | ~/实验室仓库/项目文件/影响者营销中的自我扩展机制/ | 影响者营销中的自我扩展机制 |
| 数字化存储与自传体记忆 | ~/实验室仓库/项目文件/数字化存储与自传体记忆/ | 数字化存储与自传体记忆 |
| 科研实验室搭建 | ~/实验室仓库/项目文件/科研实验室搭建/ | 科研实验室搭建 |
| 维护老板信息 | ~/实验室仓库/项目文件/维护老板信息/ | 维护老板信息 |
| 范文学习 | ~/实验室仓库/项目文件/范文学习/ | 范文学习 |
| 跨期选择的年龄差异 | ~/实验室仓库/项目文件/跨期选择的年龄差异/ | 跨期选择的年龄差异 |
