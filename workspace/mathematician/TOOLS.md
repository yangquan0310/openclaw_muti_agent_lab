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
|教学助手仓库| ~/教研室仓库/备课资料/ |教学助手用来进行工作的文件夹、其他成员不可以写入，只能读取|
|教务助手仓库| ~/教研室仓库/教务归档/ |教务助手用来进行工作的文件夹、其他成员不可以写入，只能读取|
|学工助手仓库| ~/教研室仓库/学生工作/ |学工助手用来进行工作的文件夹、其他成员不可以写入，只能读取|

### 私人存储位置
> 大管家维护格式
> 内容由各代理独立维护
| 文件 | 存储路径 | 说明 |
|----------|----------|------|
| Agent 个人记忆 | ~/.openclaw/workspace/mathematician/MEMORY.md | 数学家独立维护 |
| Agent 个人技能 | ~/.openclaw/workspace/mathematician/skills/ | 个人技能存储目录 |
| Agent 临时文件 | ~/.openclaw/workspace/mathematician/temp/ | 临时文件存储目录 |
| 工作日志 | ~/实验室仓库/日志文件/ | 任务执行记录 |
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
> 大管家统一维护

| 技能名称 | 触发示例 | 描述 | 路径 |
|---------|---------|------|------|
| agent-browser | 浏览器自动化、网页抓取 | Headless browser automation CLI | /root/.openclaw/workspace/skills/agent-browser-clawdbot/SKILL.md |
| baidu-scholar-search | 百度学术搜索 | 中英文文献检索 | /root/.openclaw/workspace/skills/baidu-scholar-search/SKILL.md |
| cnki-advanced-search | 知网高级检索 | CSSCI/C刊论文检索 | /root/.openclaw/workspace/skills/cnki-advanced-search/SKILL.md |
| docx-cn | Word文档处理 | 创建、读取、编辑Word文档 | /root/.openclaw/workspace/skills/docx-cn/SKILL.md |
| docx-generator | Word文档生成 | 生成带AI页脚的Word文档 | /root/.openclaw/workspace/skills/docx-generator/SKILL.md |
| excel-xlsx | Excel处理 | 创建、编辑Excel工作簿 | /root/.openclaw/workspace/skills/excel-xlsx/SKILL.md |
| feishu-calendar-advanced | 飞书日历管理 | 日历和日程管理 | /root/.openclaw/workspace/skills/feishu-calendar-advanced/SKILL.md |
| find-skills | 查找技能 | 技能发现和安装 | /root/.openclaw/workspace/skills/find-skills/SKILL.md |
| github | GitHub交互 | 使用gh CLI操作GitHub | /root/.openclaw/workspace/skills/github/SKILL.md |
| ima-skills | IMA技能 | IMA相关技能 | /root/.openclaw/workspace/skills/ima-skills/SKILL.md |
| knowledge-manager | 检索文献、更新知识库 | 知识管理工具 | /root/.openclaw/workspace/skills/knowledge-manager/SKILL.md |
| mcp-adapter | MCP集成 | Model Context Protocol服务器 | /root/.openclaw/workspace/skills/mcp-adapter/SKILL.md |
| memory-hygiene | 记忆清理 | 向量记忆审计和优化 | /root/.openclaw/workspace/skills/memory-hygiene/SKILL.md |
| openclaw-tavily-search | Tavily搜索 | 网络搜索 | /root/.openclaw/workspace/skills/openclaw-tavily-search/SKILL.md |
| pdf | PDF处理 | PDF文本提取、创建、合并 | /root/.openclaw/workspace/skills/pdf/SKILL.md |
| pdf-generator | PDF生成 | 从Markdown生成PDF | /root/.openclaw/workspace/skills/pdf-generator/SKILL.md |
| pdf-processing | PDF处理 | PDF文本和表格提取 | /root/.openclaw/workspace/skills/pdf-processing/SKILL.md |
| pptx-2 | PPT处理 | PowerPoint文件处理 | /root/.openclaw/workspace/skills/pptx-2/SKILL.md |
| pptx-generator | PPT生成器 | 生成可编辑的PPT | /root/.openclaw/workspace/skills/pptx-generator/SKILL.md |
| scihub-paper-downloader | Sci-Hub下载 | 获取PDF链接 | /root/.openclaw/workspace/skills/scihub-paper-downloader/SKILL.md |
| skillhub-preference | SkillHub偏好 | 技能发现首选 | /root/.openclaw/workspace/skills/skillhub-preference/SKILL.md |
| Skill-developer | 技能开发 | 创建和改进技能 | /root/.openclaw/workspace/skills/Skill-developer/SKILL.md |
| Subagents-manager | 子代理管理 | 子代理创建和管理 | /root/.openclaw/workspace/skills/Subagents-manager/SKILL.md |
| summarize | 内容总结 | 总结URL或文件 | /root/.openclaw/workspace/skills/summarize/SKILL.md |
| tencentcloud-lighthouse-skill | 腾讯云轻量服务器 | Lighthouse管理 | /root/.openclaw/workspace/skills/tencentcloud-lighthouse-skill/SKILL.md |
| tencent-cos-skill | 腾讯云COS | 对象存储管理 | /root/.openclaw/workspace/skills/tencent-cos-skill/SKILL.md |
| tencent-docs | 腾讯文档 | 在线云文档平台 | /root/.openclaw/workspace/skills/tencent-docs/SKILL.md |
| tencent-meeting-skill | 腾讯会议 | 视频会议管理 | /root/.openclaw/workspace/skills/tencent-meeting-skill/SKILL.md |
| web-tools-guide | Web工具指南 | 搜索/抓取/浏览器策略 | /root/.openclaw/workspace/skills/web-tools-guide/SKILL.md |
| zotero | Zotero管理 | 文献管理 | /root/.openclaw/workspace/skills/zotero/SKILL.md |
| zotero-local-pdf-import | Zotero本地导入 | 本地PDF导入Zotero | /root/.openclaw/workspace/skills/zotero-local-pdf-import/SKILL.md |
| zotero-scholar | Zotero学术搜索 | Zotero学术搜索 | /root/.openclaw/workspace/skills/zotero-scholar/SKILL.md |
| zotero-vectorize | Zotero向量化 | Zotero语义索引 | /root/.openclaw/workspace/skills/zotero-vectorize/SKILL.md |
---

### 个人技能索引
> 大管家维护格式
> 内容由各代理独立维护
| 技能名称 | 触发示例 | 描述 | 路径 |
|---------|---------|------|------|
| daily_maintenance | 每日维护任务 | 执行数学家每日维护任务 | ~/.openclaw/workspace/mathematician/skills/daily_maintenance.sh |
| update_indexes | 更新索引、维护 TOOLS.md | 自动更新 TOOLS.md 中的技能索引和项目库 | ~/.openclaw/workspace/mathematician/skills/update_indexes/SKILL.md |

---
*最后重构: 2026-04-16*
*重构者: 数学家*
