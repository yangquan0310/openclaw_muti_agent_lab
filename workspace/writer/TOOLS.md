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
| 技能文件夹 | ~/.openclaw/workspace/skills/README.md | 存放了所有技能文件（公共技能） |
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
| Agent 个人记忆 | ~/.openclaw/workspace/writer/MEMORY.md | 写作助手独立维护 |
| Agent 个人技能 | ~/.openclaw/workspace/writer/skills/ | 写作助手专属技能存储目录 |
| Agent 临时文件 | ~/.openclaw/workspace/writer/temp/ | 写作助手专属临时文件存储目录 |
| 实验室仓库 | ~/实验室仓库/ | 实验室仓库 |
| 实验室项目 | ~/实验室仓库/项目文件/ | 实验室各个项目 |
| 工作日志 | ~/实验室仓库/日志文件/ | 任务执行记录 |
| 项目知识库 | ~/实验室仓库/项目文件/{项目名}/知识库/index.json | 项目专属文献知识库索引 |
---

## 实验室仓库结构
> 只同步给数学家、物理学家、心理学家、写作助手和审稿助手
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
└── YYYY-MM-DD_项目名/
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
| AI降重提示工程 | ~/实验室仓库/项目文件/AI降重提示工程/ | AI降重提示词工程和学习项目 |
| 2026-04-01_数字化存储与自传体记忆 | ~/实验室仓库/项目文件/数字化存储与自传体记忆/ | 研究数字化存储对自传体记忆的影响机制 |
| 2026-04-01_跨期选择的年龄差异 | ~/实验室仓库/项目文件/跨期选择的年龄差异/ | 研究不同年龄群体在跨期选择任务中的决策差异 |
| 2026-04-04_影响者营销中的自我扩展机制 | ~/实验室仓库/项目文件/影响者营销中的自我扩展机制/ | 研究影响者营销中自我扩展机制对消费意愿的影响 |
| 2026-04-05_Zotero文件管理 | ~/实验室仓库/项目文件/Zotero文件管理/ | Zotero文献管理和学习项目 |
| 2026-04-05_审稿学习 | ~/实验室仓库/项目文件/审稿学习/ | 审稿学习项目，包含各类审稿范文 |
| 2026-04-05_科研实验室搭建 | ~/实验室仓库/项目文件/科研实验室搭建/ | 基于心理学理论重构Agent配置体系，介绍实验室搭建方法 |
| 2026-04-05_范文学习 | ~/实验室仓库/项目文件/范文学习/ | 范文学习项目，包含各类论文范文和写作模板 |
| 2026-04-07_维护老板信息 | ~/实验室仓库/项目文件/维护老板信息/ | 老板的个人信息、学术成就和账户信息管理项目 |
| 2026-04-14_学生论文修改 | ~/实验室仓库/项目文件/学生论文修改/ | 学生论文修改和指导项目 |
| 2026-04-15_内卷感知与工作繁荣 | ~/实验室仓库/项目文件/内卷感知与工作繁荣/ | 研究内卷感知对工作繁荣的影响机制 |

---

## 索引
> 各个代理独立维护

### 公共技能索引
> 大管家统一维护
> 完整列表见: `/root/.openclaw/workspace/skills/README.md`

| 技能名称 | 触发示例 | 描述 | 路径 |
|---------|---------|------|------|
| agent-browser-clawdbot | 浏览器自动化 | 浏览器自动化工具 | ~/.openclaw/workspace/skills/agent-browser-clawdbot/SKILL.md |
| baidu-scholar-search | 百度学术搜索 | 百度学术文献检索 | ~/.openclaw/workspace/skills/baidu-scholar-search/SKILL.md |
| cnki-advanced-search | 知网高级检索 | 知网CSSCI论文检索 | ~/.openclaw/workspace/skills/cnki-advanced-search/SKILL.md |
| docx-cn | Word文档处理 | 创建、读取、编辑Word文档 | ~/.openclaw/workspace/skills/docx-cn/SKILL.md |
| docx-generator | Word文档生成 | 生成带AI页脚的Word文档 | ~/.openclaw/workspace/skills/docx-generator/SKILL.md |
| excel-xlsx | Excel处理 | 创建、编辑Excel工作簿 | ~/.openclaw/workspace/skills/excel-xlsx/SKILL.md |
| feishu-calendar-advanced | 飞书日历 | 飞书日历管理 | ~/.openclaw/workspace/skills/feishu-calendar-advanced/SKILL.md |
| find-skills | 查找技能 | 技能发现和安装 | ~/.openclaw/workspace/skills/find-skills/SKILL.md |
| github | GitHub操作 | GitHub CLI操作 | ~/.openclaw/workspace/skills/github/SKILL.md |
| ima-skills | IMA技能 | IMA相关技能 | ~/.openclaw/workspace/skills/ima-skills/SKILL.md |
| knowledge-manager | 知识管理 | 文献检索、知识库维护 | ~/.openclaw/workspace/skills/knowledge-manager/SKILL.md |
| mcp-adapter | MCP集成 | Model Context Protocol | ~/.openclaw/workspace/skills/mcp-adapter/SKILL.md |
| memory-hygiene | 记忆清理 | 向量记忆审计和优化 | ~/.openclaw/workspace/skills/memory-hygiene/SKILL.md |
| openclaw-tavily-search | Tavily搜索 | 网络搜索 | ~/.openclaw/workspace/skills/openclaw-tavily-search/SKILL.md |
| pdf | PDF处理 | PDF文本提取、合并、分割 | ~/.openclaw/workspace/skills/pdf/SKILL.md |
| pdf-generator | PDF生成 | 生成专业PDF文档 | ~/.openclaw/workspace/skills/pdf-generator/SKILL.md |
| pdf-processing | PDF处理(中文) | PDF文本和表格提取 | ~/.openclaw/workspace/skills/pdf-processing/SKILL.md |
| pptx-2 | PPT处理 | 读取、创建PPT | ~/.openclaw/workspace/skills/pptx-2/SKILL.md |
| pptx-generator | PPT生成器 | 生成可编辑PPT | ~/.openclaw/workspace/skills/pptx-generator/SKILL.md |
| scihub-paper-downloader | Sci-Hub下载 | 获取论文PDF链接 | ~/.openclaw/workspace/skills/scihub-paper-downloader/SKILL.md |
| Skill-developer | 技能开发 | 创建和改进技能 | ~/.openclaw/workspace/skills/Skill-developer/SKILL.md |
| skillhub-preference | SkillHub偏好 | 技能发现安装偏好 | ~/.openclaw/workspace/skills/skillhub-preference/SKILL.md |
| Subagents-manager | 子代理管理 | 子代理创建和管理 | ~/.openclaw/workspace/skills/Subagents-manager/SKILL.md |
| summarize | 摘要总结 | URL和文件摘要 | ~/.openclaw/workspace/skills/summarize/SKILL.md |
| tencentcloud-lighthouse-skill | 腾讯云轻量服务器 | 轻量服务器管理 | ~/.openclaw/workspace/skills/tencentcloud-lighthouse-skill/SKILL.md |
| tencent-cos-skill | 腾讯云COS | 对象存储和图片处理 | ~/.openclaw/workspace/skills/tencent-cos-skill/SKILL.md |
| tencent-docs | 腾讯文档 | 腾讯文档操作 | ~/.openclaw/workspace/skills/tencent-docs/SKILL.md |
| tencent-meeting-skill | 腾讯会议 | 腾讯会议管理 | ~/.openclaw/workspace/skills/tencent-meeting-skill/SKILL.md |
| web-tools-guide | Web工具指南 | 搜索抓取策略 | ~/.openclaw/workspace/skills/web-tools-guide/SKILL.md |
| zotero | Zotero管理 | 文献库管理 | ~/.openclaw/workspace/skills/zotero/SKILL.md |
| zotero-local-pdf-import | Zotero本地导入 | 本地PDF导入Zotero | ~/.openclaw/workspace/skills/zotero-local-pdf-import/SKILL.md |
| zotero-scholar | Zotero学术 | Zotero学术功能 | ~/.openclaw/workspace/skills/zotero-scholar/SKILL.md |
| zotero-vectorize | Zotero向量化 | 语义索引构建 | ~/.openclaw/workspace/skills/zotero-vectorize/SKILL.md |

### 个人技能索引
> 大管家维护格式
> 内容由各代理独立维护

| 技能名称 | 触发示例 | 描述 | 路径 |
|---------|---------|------|------|
| 学术句子撰写脚本 | 撰写学术句子 | 撰写符合学术规范的中英文句子 | ~/.openclaw/workspace/writer/skills/学术句子撰写脚本/SKILL.md |
| 学术段落撰写脚本 | 撰写学术段落 | 撰写独立学术段落，论证特定论点 | ~/.openclaw/workspace/writer/skills/学术段落撰写脚本/SKILL.md |
| 学术篇章撰写脚本 | 撰写学术篇章 | 撰写完整学术篇章，整合段落形成连贯论述 | ~/.openclaw/workspace/writer/skills/学术篇章撰写脚本/SKILL.md |

---

*最后重构: 2026-04-16*
*重构者: 写作助手*
