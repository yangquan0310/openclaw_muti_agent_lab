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
| 技能文件夹 | ~/.openclaw/skills/ | 存放了所有技能文件（公共技能） |
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
| Agent 个人记忆 | ~/.openclaw/workspace/teaching/MEMORY.md | 教学助手独立维护 |
| Agent 个人技能 | ~/.openclaw/workspace/teaching/skills/README.md | 教学助手专属技能存储目录 |
| Agent 临时文件 | ~/.openclaw/workspace/teaching/temp/README.md | 教学助手专属临时文件存储目录 |
| 工作日志 | ~/教研室仓库/日志文件/README.MD | 任务执行记录 |
| 课程项目文件 | ~/教研室仓库/备课资料/ | 教学助手课程项目文件存储位置 |
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
    ├── 课件/                   # 课件
    ├── 知识库/                 # 项目专属知识库
    │   └── 索引.json          # 文献索引
    ├── 元数据.json             # 项目元数据
    └── README.md               # 项目说明
```

### 项目库
> 大管家维护格式
> 内容由各代理独立维护
**教研室项目（私人项目库，存储于备课资料）：**
| 项目ID | 项目名 | 项目类型 | 状态 | 存储位置 | 描述 |
|--------|--------|----------|------|----------|------|
| JY001 | 教育科学研究方法 | 本科课程 | 进行中 | ~/教研室仓库/备课资料/教育科学研究方法/ | 教育科学研究方法本科课程教学资料，包含16章完整教学内容 |
| CY001 | 创新创业基础 | 本科课程 | 未开始 | ~/教研室仓库/备课资料/创新创业基础/ | 创新创业基础本科课程教学资料 |
| 索引 | - | - | - | ~/教研室仓库/备课资料/索引.json | 课程项目索引 |
| 项目库 | - | - | - | ~/教研室仓库/备课资料/项目库.json | 项目库信息 |

---
---

## 索引
> 各个代理独立维护

### 公共技能索引
> 大管家统一维护

| 技能名称 | 触发示例 | 描述 | 路径 |
|---------|---------|------|------|
| agent-browser-clawdbot | 浏览器自动化 | Headless browser automation CLI | ~/.openclaw/workspace/skills/agent-browser-clawdbot/SKILL.md |
| baidu-scholar-search | 百度学术检索 | 百度学术搜索工具 | ~/.openclaw/workspace/skills/baidu-scholar-search/SKILL.md |
| cnki-advanced-search | 知网高级检索 | 知网CSSCI论文自动化检索 | ~/.openclaw/workspace/skills/cnki-advanced-search/SKILL.md |
| docx-cn | Word文档处理 | 创建、读取、编辑Word文档 | ~/.openclaw/workspace/skills/docx-cn/SKILL.md |
| docx-generator | Word文档生成 | 创建包含AI生成页脚的Word文档 | ~/.openclaw/workspace/skills/docx-generator/SKILL.md |
| excel-xlsx | Excel处理 | 创建、编辑Excel工作簿 | ~/.openclaw/workspace/skills/excel-xlsx/SKILL.md |
| feishu-calendar-advanced | 飞书日历 | 飞书日历管理 | ~/.openclaw/workspace/skills/feishu-calendar-advanced/SKILL.md |
| find-skills | 技能发现 | 查找和安装技能 | ~/.openclaw/workspace/skills/find-skills/SKILL.md |
| github | GitHub交互 | 使用gh CLI与GitHub交互 | ~/.openclaw/workspace/skills/github/SKILL.md |
| ima-skills | IMA技能 | IMA相关技能 | ~/.openclaw/workspace/skills/ima-skills/SKILL.md |
| knowledge-manager | 知识管理 | 文献检索、知识库维护 | ~/.openclaw/workspace/skills/knowledge-manager/SKILL.md |
| mcp-adapter | MCP集成 | Model Context Protocol集成 | ~/.openclaw/workspace/skills/mcp-adapter/SKILL.md |
| memory-hygiene | 记忆清理 | 审计和优化向量内存 | ~/.openclaw/workspace/skills/memory-hygiene/SKILL.md |
| openclaw-tavily-search | Tavily搜索 | Web搜索 | ~/.openclaw/workspace/skills/openclaw-tavily-search/SKILL.md |
| pdf | PDF处理 | PDF文本提取、创建、合并 | ~/.openclaw/workspace/skills/pdf/SKILL.md |
| pdf-generator | PDF生成 | 从Markdown生成PDF | ~/.openclaw/workspace/skills/pdf-generator/SKILL.md |
| pdf-processing | PDF处理 | PDF文本和表格提取 | ~/.openclaw/workspace/skills/pdf-processing/SKILL.md |
| pptx-2 | PPT处理 | 读取、创建、编辑PPT | ~/.openclaw/workspace/skills/pptx-2/SKILL.md |
| pptx-generator | PPT生成器 | 专业PPT生成 | ~/.openclaw/workspace/skills/pptx-generator/SKILL.md |
| scihub-paper-downloader | Sci-Hub下载 | 从Sci-Hub获取PDF | ~/.openclaw/workspace/skills/scihub-paper-downloader/SKILL.md |
| Skill-developer | 技能开发 | 创建和改进技能 | ~/.openclaw/workspace/skills/Skill-developer/SKILL.md |
| skillhub-preference | Skillhub偏好 | 技能发现偏好设置 | ~/.openclaw/workspace/skills/skillhub-preference/SKILL.md |
| Subagents-manager | 子代理管理 | 子代理调度和管理 | ~/.openclaw/workspace/skills/Subagents-manager/SKILL.md |
| summarize | 摘要生成 | 摘要URL或文件 | ~/.openclaw/workspace/skills/summarize/SKILL.md |
| tencentcloud-lighthouse-skill | 腾讯云Lighthouse | 轻量应用服务器管理 | ~/.openclaw/workspace/skills/tencentcloud-lighthouse-skill/SKILL.md |
| tencent-cos-skill | 腾讯云COS | 对象存储管理 | ~/.openclaw/workspace/skills/tencent-cos-skill/SKILL.md |
| tencent-docs | 腾讯文档 | 腾讯文档管理 | ~/.openclaw/workspace/skills/tencent-docs/SKILL.md |
| tencent-meeting-skill | 腾讯会议 | 腾讯会议管理 | ~/.openclaw/workspace/skills/tencent-meeting-skill/SKILL.md |
| web-tools-guide | Web工具指南 | Web搜索和抓取策略 | ~/.openclaw/workspace/skills/web-tools-guide/SKILL.md |
| zotero | Zotero管理 | Zotero文献管理 | ~/.openclaw/workspace/skills/zotero/SKILL.md |
| zotero-local-pdf-import | Zotero本地导入 | 本地PDF导入Zotero | ~/.openclaw/workspace/skills/zotero-local-pdf-import/SKILL.md |
| zotero-scholar | Zotero学术 | Zotero学术功能 | ~/.openclaw/workspace/skills/zotero-scholar/SKILL.md |
| zotero-vectorize | Zotero向量化 | Zotero语义索引 | ~/.openclaw/workspace/skills/zotero-vectorize/SKILL.md |
| 修改文档 | 需要修改已存在的文档文件 | 修改文档文件，保存新版本并记录修改历史 | ~/.openclaw/workspace/skills/修改文档/SKILL.md |
| 撰写脚本 | 需要创建新的操作脚本 | 按照五要素SOP规范撰写新脚本 | ~/.openclaw/workspace/skills/撰写脚本/SKILL.md |
| 撰写技能 | 需要创建新的技能 | 创建新的技能（结构化或非结构化） | ~/.openclaw/workspace/skills/撰写技能/SKILL.md |
---

### 个人技能索引
> 大管家维护格式
> 内容由各代理独立维护
| 技能名称 | 触发示例 | 描述 | 路径 |
|---------|---------|------|------|
| download_papers | 需要下载论文 | 批量下载学术论文 | ~/.openclaw/workspace/teaching/skills/download_papers/SKILL.md |
| retrieve_papers | 需要检索论文 | 检索并获取论文信息 | ~/.openclaw/workspace/teaching/skills/retrieve_papers/SKILL.md |
| search_literature | 需要文献检索 | 综合文献检索工具 | ~/.openclaw/workspace/teaching/skills/search_literature/SKILL.md |

---

*最后重构: 2026-04-16*
*重构者: 教学助手*
