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
| 实验室仓库 | ~/实验室仓库/README.md | 实验室仓库 |
| 实验室项目 | ~/实验室仓库/项目文件/README.md | 实验室各个项目 |
| 工作日志 | ~/实验室仓库/日志文件/README.md | 任务执行记录 |
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
├── 日志文件/                   # Agent工作日志
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
├── 日志文件/                   # 教学相关日志记录
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

| 技能名称 | 触发示例 | 描述 | 路径 |
|---------|---------|------|------|
| knowledge-manager | 检索文献、更新知识库、总结笔记、提取笔记 | 知识管理工具，支持文献检索、知识库维护、笔记处理等功能 | ~/.openclaw/workspace/skills/knowledge-manager/SKILL.md |
| tencent-docs | 上传腾讯云文档 | 使用 md 上传 | ~/.openclaw/workspace/skills/tencent-docs/SKILL.md |
| Zotero | 管理文献、搜索文献 | Zotero 文献管理 | ~/.openclaw/workspace/skills/zotero/SKILL.md |
| github | GitHub操作、代码同步 | 使用 gh CLI 进行 GitHub 交互、拉取/推送代码、管理 issues/PRs | ~/.openclaw/workspace/skills/github/SKILL.md |
| agent-browser-clawdbot | 浏览器自动化 | 浏览器自动化操作 | ~/.openclaw/workspace/skills/agent-browser-clawdbot/SKILL.md |
| baidu-scholar-search | 百度学术搜索 | 百度学术文献搜索 | ~/.openclaw/workspace/skills/baidu-scholar-search/SKILL.md |
| cnki-advanced-search | CNKI高级搜索 | 中国知网高级搜索 | ~/.openclaw/workspace/skills/cnki-advanced-search/SKILL.md |
| docx-cn | Word文档生成 | 生成中文Word文档 | ~/.openclaw/workspace/skills/docx-cn/SKILL.md |
| docx-generator | Word文档生成器 | Word文档生成工具 | ~/.openclaw/workspace/skills/docx-generator/SKILL.md |
| excel-xlsx | Excel处理 | Excel文件处理 | ~/.openclaw/workspace/skills/excel-xlsx/SKILL.md |
| feishu-calendar-advanced | 飞书日历高级 | 飞书日历高级功能 | ~/.openclaw/workspace/skills/feishu-calendar-advanced/SKILL.md |
| find-skills | 查找技能 | 技能查找工具 | ~/.openclaw/workspace/skills/find-skills/SKILL.md |
| ima-skills | IMA技能 | IMA知识库技能 | ~/.openclaw/workspace/skills/ima-skills/SKILL.md |
| mcp-adapter | MCP适配器 | MCP工具适配 | ~/.openclaw/workspace/skills/mcp-adapter/SKILL.md |
| memory-hygiene | 记忆清理 | 记忆清理工具 | ~/.openclaw/workspace/skills/memory-hygiene/SKILL.md |
| openclaw-tavily-search | Tavily搜索 | Tavily搜索引擎 | ~/.openclaw/workspace/skills/openclaw-tavily-search/SKILL.md |
| pdf-generator | PDF生成器 | 生成PDF文件 | ~/.openclaw/workspace/skills/pdf-generator/SKILL.md |
| pdf-processing | PDF处理 | PDF文件处理 | ~/.openclaw/workspace/skills/pdf-processing/SKILL.md |
| pdf | PDF工具 | PDF基础工具 | ~/.openclaw/workspace/skills/pdf/SKILL.md |
| pptx-2 | PPT生成 | 生成PowerPoint演示文稿 | ~/.openclaw/workspace/skills/pptx-2/SKILL.md |
| pptx-generator | PPT生成器 | PowerPoint生成工具 | ~/.openclaw/workspace/skills/pptx-generator/SKILL.md |
| scihub-paper-downloader | SciHub下载 | 从SciHub下载论文 | ~/.openclaw/workspace/skills/scihub-paper-downloader/SKILL.md |
| Skill-developer | 技能开发 | 开发新技能 | ~/.openclaw/workspace/skills/Skill-developer/SKILL.md |
| skillhub-preference | SkillHub偏好 | SkillHub偏好设置 | ~/.openclaw/workspace/skills/skillhub-preference/SKILL.md |
| Subagents-manager | 子代理管理 | 管理子代理 | ~/.openclaw/workspace/skills/Subagents-manager/SKILL.md |
| summarize | 总结 | 文本总结工具 | ~/.openclaw/workspace/skills/summarize/SKILL.md |
| tencentcloud-lighthouse-skill | 腾讯云轻量服务器 | 腾讯云轻量应用服务器管理 | ~/.openclaw/workspace/skills/tencentcloud-lighthouse-skill/SKILL.md |
| tencent-cos-skill | 腾讯云COS | 腾讯云对象存储 | ~/.openclaw/workspace/skills/tencent-cos-skill/SKILL.md |
| tencent-meeting-skill | 腾讯会议 | 腾讯会议管理 | ~/.openclaw/workspace/skills/tencent-meeting-skill/SKILL.md |
| web-tools-guide | Web工具指南 | Web工具使用指南 | ~/.openclaw/workspace/skills/web-tools-guide/SKILL.md |
| zotero-local-pdf-import | Zotero本地PDF导入 | 导入本地PDF到Zotero | ~/.openclaw/workspace/skills/zotero-local-pdf-import/SKILL.md |
| zotero-scholar | Zotero学术 | Zotero学术功能 | ~/.openclaw/workspace/skills/zotero-scholar/SKILL.md |
| zotero-vectorize | Zotero向量化 | Zotero文献向量化 | ~/.openclaw/workspace/skills/zotero-vectorize/SKILL.md |
---

### 个人技能索引

| 技能名称 | 触发示例 | 描述 | 路径 |
|---------|---------|------|------|
| 管理项目元数据 | 需要创建或维护项目 | 创建和维护项目元数据，管理云文档映射 | ~/.openclaw/workspace/steward/skills/管理项目元数据/SKILL.md |
| 维护配置文件 | 维护其他Agent的配置文件 | 维护其他Agent的配置文件，同步大管家更新的公共结构部分 | ~/.openclaw/workspace/steward/skills/维护配置文件/SKILL.md |

---

*最后重构: 2026-04-17*
*重构者: 大管家*