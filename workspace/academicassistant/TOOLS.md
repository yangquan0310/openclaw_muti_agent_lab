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
| 技能文件夹 | ~/.openclaw/skills/ | 存放了所有技能文件 |
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
| Agent 个人记忆 | ~/.openclaw/workspace/academicassistant/MEMORY.md | 教务助手独立维护 |
| Agent 个人脚本 | ~/.openclaw/workspace/academicassistant/scripts/ | 教务助手专属脚本存储目录 |
| Agent 个人技能 | ~/.openclaw/workspace/academicassistant/skills/ | 教务助手专属技能存储目录 |
| Agent 临时文件 | ~/.openclaw/workspace/academicassistant/temp/ | 教务助手专属临时文件存储目录 |
| 工作日志 | ~/教研室仓库/日志文件/README.MD | 任务执行记录 |
| 教研室项目文件 | ~/教研室仓库/项目文件/ | 教研室科研项目文件存储位置 |
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
    ├── 课程大纲/                   # 课程大纲
    ├── 知识库/                 # 项目专属知识库
    │   └── 索引.json          # 文献索引
    ├── 元数据.json             # 项目元数据
    └── README.md               # 项目说明
```

### 项目库
> 大管家维护格式
> 内容由各代理独立维护

**教研室项目（私人项目库）：**
| 项目名 | 存储位置 | 描述 |
|--------|----------|------|
| 2026-04-08_课程大纲审核 | ~/教研室仓库/项目文件/2026-04-08_课程大纲审核/ | 课程大纲审核与整理项目，包含以学生为中心的课程教学大纲核查表 |

---

## 索引
> 各个代理独立维护

### 公共技能索引
> 大管家统一维护

| 技能名称 | 触发示例 | 描述 | 路径 |
|---------|---------|------|------|
| general-scripts | 管理文档生命流程、写入项目元数据、创建工作日志、创建新项目、撰写脚本、创建文件、修改文件、映射云文档、控制版本、管理知识库、检索文献 | 提供标准化通用操作脚本 | ~/.openclaw/skills/general-scripts/SKILL.md |
| feishu-doc-manager | 上传飞书云文档 | Markdown 渲染、权限管理、长文档处理 | ~/.openclaw/skills/feishu-doc-manager/SKILL.md |
| tencent-docs | 上传腾讯云文档 | 使用 md 上传 | ~/.openclaw/skills/tencent-docs/SKILL.md |
| tencent-docs-upload-by-sections | 分段上传腾讯云文档 | 文件太大，上传腾讯云文档无法使用时，分段上传 | ~/.openclaw/skills/tencent-docs-upload-by-sections/SKILL.md |
| Zotero | 管理文献、搜索文献 | Zotero 文献管理 | ~/.openclaw/skills/zotero/SKILL.md |
| 检索文献 | 检索学术文献存入项目知识库 | 使用Semantic Scholar和Zotero检索文献并更新项目知识库 | ~/.openclaw/skills/general-scripts/检索文献.md |

### 私人技能索引
> 大管家维护格式
> 内容由各代理独立维护
| 技能名称 | 触发示例 | 描述 | 路径 |
|---------|---------|------|------|
| docx-cn | Word 文档处理 | 创建、读取、编辑 Word 文档（.docx 格式） | ~/.openclaw/skills/docx-cn/SKILL.md |
| docx-generator | Word 文档生成 | 从 Markdown 创建 Microsoft Word (.docx) 文档 | ~/.openclaw/skills/docx-generator/SKILL.md |
| pdf | PDF 综合工具包 | 提取文本、表格，创建、合并、拆分 PDF 文档 | ~/.openclaw/skills/pdf/SKILL.md |
| pdf-generator | PDF 生成器 | 从 Markdown/HTML 生成专业 PDF 文档（报告、发票等） | ~/.openclaw/skills/pdf-generator/SKILL.md |
| pdf-processing | PDF 处理 | 从 PDF 提取文本和表格，填写表单，合并文档 | ~/.openclaw/skills/pdf-processing/SKILL.md |
| baidu-scholar-search | 百度学术搜索 | 检索中英文文献、学术期刊、会议论文、学位论文 | ~/.openclaw/skills/baidu-scholar-search/SKILL.md |
| cnki-advanced-search | 知网高级检索 | 检索知网CSSCI/C刊论文、下载题录和摘要 | ~/.openclaw/skills/cnki-advanced-search/SKILL.md |
| excel-xlsx | Excel文件处理 | 创建、编辑、操作Excel工作簿和XLSX文件 | ~/.openclaw/skills/excel-xlsx/SKILL.md |
| feishu-calendar-advanced | 飞书日历管理 | 查看日历、列出事件、创建和删除日历事件 | ~/.openclaw/skills/feishu-calendar-advanced/SKILL.md |
| find-skills | 查找技能 | 搜索、发现、安装新的Agent技能 | ~/.openclaw/skills/find-skills/SKILL.md |
| github | GitHub操作 | 使用gh CLI管理GitHub issues、PR、CI运行等 | ~/.openclaw/skills/github/SKILL.md |
| lab-backup-manager | 实验室仓库备份 | 自动备份OpenClaw核心配置文件到GitHub | ~/.openclaw/skills/lab-backup-manager/SKILL.md |
| mcp-adapter | MCP服务器集成 | 访问MCP服务器提供的外部工具和数据源 | ~/.openclaw/skills/mcp-adapter/SKILL.md |
| memory-hygiene | 记忆库优化 | 审计、清理、优化Clawdbot的向量记忆 | ~/.openclaw/skills/memory-hygiene/SKILL.md |
| tavily-search | Tavily网络搜索 | 网络搜索、查找来源和链接 | ~/.openclaw/skills/openclaw-tavily-search/SKILL.md |
| pptx-2 | PPT文件处理 | 创建、读取、编辑PowerPoint演示文稿 | ~/.openclaw/skills/pptx-2/SKILL.md |
| pptx-generator | PPT生成器 | 创建专业可编辑的PowerPoint演示文稿 | ~/.openclaw/skills/pptx-generator/SKILL.md |
| scihub-paper-downloader | Sci-Hub文献下载 | 根据DOI从Sci-Hub获取PDF文献 | ~/.openclaw/skills/scihub-paper-downloader/SKILL.md |
| semantic-scholar-mcp | Semantic Scholar检索 | 检索Semantic Scholar学术文献 | ~/.openclaw/skills/semantic-scholar-mcp/SKILL.md |
| skillhub-preference | Skillhub优先 | 优先使用Skillhub进行技能发现和安装 | ~/.openclaw/skills/skillhub-preference/SKILL.md |
| summarize | 内容摘要 | 总结URL、文件、PDF、音频、视频、YouTube内容 | ~/.openclaw/skills/summarize/SKILL.md |
| tencentcloud-lighthouse-skill | 腾讯云轻量应用服务器管理 | 管理腾讯云Lighthouse实例、监控、防火墙等 | ~/.openclaw/skills/tencentcloud-lighthouse-skill/SKILL.md |
| tencent-cos-skill | 腾讯云对象存储管理 | 上传、下载、管理腾讯云COS文件，进行图片处理 | ~/.openclaw/skills/tencent-cos-skill/SKILL.md |
| tencent-docs | 腾讯云文档操作 | 创建、编辑、管理腾讯云文档 | ~/.openclaw/skills/tencent-docs/SKILL.md |
| tencent-docs-upload-by-sections | 腾讯云文档分段上传 | 长文档分段上传到腾讯云文档，避免内容截断 | ~/.openclaw/skills/tencent-docs-upload-by-sections/SKILL.md |
| tencent-meeting-skill | 腾讯会议管理 | 预约、修改、查询腾讯会议，管理录制和转写 | ~/.openclaw/skills/tencent-meeting-skill/SKILL.md |
| zotero | Zotero文献管理 | 管理Zotero参考文献库、搜索、导出引文 | ~/.openclaw/skills/zotero/SKILL.md |
| zotero-local-pdf-import | Zotero本地PDF导入 | 将本地PDF文件导入Zotero文献库 | ~/.openclaw/skills/zotero-local-pdf-import/SKILL.md |
| zotero-scholar | Zotero学术检索 | Zotero学术文献检索和管理 | ~/.openclaw/skills/zotero-scholar/SKILL.md |
| zotero-vectorize | Zotero语义索引 | 构建和维护Zotero文献库的语义索引 | ~/.openclaw/skills/zotero-vectorize/SKILL.md |
---
### 脚本索引
> 各个代理独立维护，这里显示教务助手特有脚本

| 触发条件 | 脚本编号 | 脚本名称 | 功能描述 |
|----------|----------|----------|----------|
| 批量更新课程大纲 | S001 | update_syllabi.py | 批量更新课程大纲文件 |
| 转换大纲格式 | S002 | convert_syllabus.py | 将课程大纲转换为标准格式 |
| 更新TOOLS.md | S003 | update_tools_md.sh | 自动更新工具索引文档 |
| 更新索引 | S004 | update_index.sh | 更新项目索引文件 |
| 维护工作记忆 | S005 | 维护工作记忆.sh | 每日维护工作记忆和清理任务 |

---

*最后重构: 2026-04-12*
*重构者: 教务助手*
