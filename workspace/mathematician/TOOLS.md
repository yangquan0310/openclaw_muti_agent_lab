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
| Agent 工作日志 | ~/.openclaw/workspace/mathematician/memory/README.md | 任务执行记录 |
| 实验室仓库 | ~/实验室仓库/README.md | 实验室仓库 |
| 实验室项目 | ~/实验室仓库/项目文件/README.md | 实验室各个项目 |
| 工作日志 | ~/实验室仓库/日志文件/README.md | 任务执行记录 |
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
| AI降重提示工程 | ~/实验室仓库/项目文件/AI降重提示工程/ | AI降重提示工程 |
| Zotero文件管理 | ~/实验室仓库/项目文件/Zotero文件管理/ | Zotero文件管理 |
| 内卷感知与工作繁荣 | ~/实验室仓库/项目文件/内卷感知与工作繁荣/ | 内卷感知与工作繁荣 |
| 学生论文修改 | ~/实验室仓库/项目文件/学生论文修改/ | 学生论文修改 |
| 审稿学习 | ~/实验室仓库/项目文件/审稿学习/ | 审稿学习 |
| 影响者营销中的自我扩展机制 | ~/实验室仓库/项目文件/影响者营销中的自我扩展机制/ | 影响者营销中的自我扩展机制 |
| 数字化存储与自传体记忆 | ~/实验室仓库/项目文件/数字化存储与自传体记忆/ | 数字化存储与自传体记忆 |
| 科研实验室搭建 | ~/实验室仓库/项目文件/科研实验室搭建/ | 科研实验室搭建 |
| 维护老板信息 | ~/实验室仓库/项目文件/维护老板信息/ | 维护老板信息 |
| 范文学习 | ~/实验室仓库/项目文件/范文学习/ | 范文学习 |
| 跨期选择的年龄差异 | ~/实验室仓库/项目文件/跨期选择的年龄差异/ | 跨期选择的年龄差异 |

## 技能索引

### 公共技能索引
> 完整列表见: `/root/.openclaw/workspace/skills/README.md`

| 技能名称 | 触发示例 | 描述 | 路径 |
|---------|---------|------|------|
| agent-browser-clawdbot | 浏览器自动化、网页抓取 | 基于 Clawdbot 的浏览器自动化工具 | `workspace/skills/agent-browser-clawdbot/SKILL.md` |
| **agent_self_development** | **Agent自我发展** | **基于认知发展理论的Agent自我进化系统** | **`workspace/skills/agent_self_development/SKILL.md`** |
| baidu-scholar-search | 百度学术搜索 | 百度学术文献检索工具 | `workspace/skills/baidu-scholar-search/SKILL.md` |
| cnki-advanced-search | CNKI高级检索 | 中国知网高级检索工具 | `workspace/skills/cnki-advanced-search/SKILL.md` |
| docx-cn | Word文档处理 | 中文Word文档处理技能 | `workspace/skills/docx-cn/SKILL.md` |
| docx-generator | Word文档生成 | Word文档自动生成工具 | `workspace/skills/docx-generator/SKILL.md` |
| excel-xlsx | Excel表格处理 | Excel文件处理技能 | `workspace/skills/excel-xlsx/SKILL.md` |
| feishu-calendar-advanced | 飞书日历高级功能 | 飞书日历高级管理功能 | `workspace/skills/feishu-calendar-advanced/SKILL.md` |
| find-skills | 查找技能 | 技能发现和安装工具 | `workspace/skills/find-skills/SKILL.md` |
| github | GitHub操作 | GitHub代码托管操作技能 | `workspace/skills/github/SKILL.md` |
| ima-skills | IMA知识管理 | IMA知识库管理技能 | `workspace/skills/ima-skills/SKILL.md` |
| knowledge-manager | 知识管理 | 文献检索、知识库维护、笔记处理 | `workspace/skills/knowledge-manager/SKILL.md` |
| mcp-adapter | MCP适配器 | MCP协议适配工具 | `workspace/skills/mcp-adapter/SKILL.md` |
| memory-hygiene | 记忆清理 | 工作记忆清理和维护工具 | `workspace/skills/memory-hygiene/SKILL.md` |
| openclaw-tavily-search | Tavily搜索 | 使用Tavily API进行网络搜索 | `workspace/skills/openclaw-tavily-search/SKILL.md` |
| pdf | PDF工具 | PDF基础操作工具 | `workspace/skills/pdf/SKILL.md` |
| pdf-generator | PDF生成 | PDF文档生成工具 | `workspace/skills/pdf-generator/SKILL.md` |
| pdf-processing | PDF处理 | PDF文件处理技能 | `workspace/skills/pdf-processing/SKILL.md` |
| pptx-2 | PPT处理 | PowerPoint文档处理技能 | `workspace/skills/pptx-2/SKILL.md` |
| pptx-generator | PPT生成 | PowerPoint自动生成工具 | `workspace/skills/pptx-generator/SKILL.md` |
| scihub-paper-downloader | SciHub下载 | 学术论文下载工具 | `workspace/skills/scihub-paper-downloader/SKILL.md` |
| skillhub-preference | 技能偏好 | 技能发现和安装偏好设置 | `workspace/skills/skillhub-preference/SKILL.md` |
| Skill-developer | 技能开发 | 技能包开发工具 | `workspace/skills/Skill-developer/SKILL.md` |
| Subagents-manager | 子代理管理 | 子代理创建、监控、调节管理 | `workspace/skills/Subagents-manager/SKILL.md` |
| summarize | 文本摘要 | 文本自动摘要工具 | `workspace/skills/summarize/SKILL.md` |
| tencent-cos-skill | 腾讯云COS | 腾讯云对象存储操作技能 | `workspace/skills/tencent-cos-skill/SKILL.md` |
| tencent-docs | 腾讯文档 | 腾讯文档操作和管理技能 | `workspace/skills/tencent-docs/SKILL.md` |
| tencent-meeting-skill | 腾讯会议 | 腾讯会议管理技能 | `workspace/skills/tencent-meeting-skill/SKILL.md` |
| tencentcloud-lighthouse-skill | 腾讯云轻量服务器 | 腾讯云轻量应用服务器管理 | `workspace/skills/tencentcloud-lighthouse-skill/SKILL.md` |
| web-tools-guide | Web工具指南 | 网络工具使用指南 | `workspace/skills/web-tools-guide/SKILL.md` |
| zotero | Zotero文献管理 | Zotero文献管理工具 | `workspace/skills/zotero/SKILL.md` |
| zotero-local-pdf-import | Zotero本地PDF导入 | Zotero本地PDF文件导入工具 | `workspace/skills/zotero-local-pdf-import/SKILL.md` |
| zotero-scholar | Zotero学术搜索 | Zotero学术文献检索工具 | `workspace/skills/zotero-scholar/SKILL.md` |
| zotero-vectorize | Zotero向量化 | Zotero文献向量化处理工具 | `workspace/skills/zotero-vectorize/SKILL.md` |

---

### 个人技能索引
> 完整列表见: `/root/.openclaw/workspace/mathematician/skills/README.md`

| 技能名称 | 触发示例 | 描述 | 路径 |
|---------|---------|------|------|
| auto-push | `自动推送`、`推送代码`、`git push` | 每日自动推送代码到 development 分支的定时任务技能 | `skills/auto-push/` |
| update_tools | `更新工具`、`更新 TOOLS` | 每日自动更新 TOOLS.md，扫描项目列表和脚本索引 | `skills/update_tools/` |
| 维护工作记忆 | `清理工作记忆`、`归档任务` | 清理 completed/killed 任务，归档到事件记忆，维护活跃子代理清单 | `skills/维护工作记忆/` |
| 管理项目元数据 | `创建项目元数据`、`维护云文档映射` | 创建新项目元数据，维护本地文档与飞书/腾讯文档的映射关系 | `skills/管理项目元数据/` |
| 维护配置文件 | `同步 AGENTS.md`、`维护配置` | 维护其他 Agent 的配置文件，同步大管家更新的公共结构部分 | `skills/维护配置文件/` |
| 腾讯文档分段上传 | `分段上传腾讯文档`、`长文档上传` | 长文档切分成多个段落，逐段上传到腾讯文档智能文档 | `skills/腾讯文档分段上传/` |

---
*最后重构: 2026-04-16*
*重构者: 数学家*
