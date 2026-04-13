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
| 脚本存储位置 | /root/.openclaw/workspace/physicist/scripts | 物理学家Agent自定义脚本存储目录 |
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
| Agent 个人记忆 | ~/.openclaw/workspace/physicist/MEMORY.md | 物理学家独立维护 |
| Agent 个人脚本 | ~/.openclaw/workspace/physicist/scripts/README.md | 物理学家专属脚本存储目录 |
| Agent 个人技能 | ~/.openclaw/workspace/physicist/skills/README.md | 物理学家专属技能存储目录 |
| Agent 临时文件 | ~/.openclaw/workspace/physicist/temp/README.md | 物理学家专属临时文件存储目录 |
| 实验室仓库 | ~/实验室仓库/ | 实验室仓库 |
| 实验室项目 | ~/实验室仓库/项目文件/ | 实验室各个项目 |
| 工作日志 | ~/实验室仓库/日志文件/README.MD | 任务执行记录 |
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
| 2026-04-01_数字化存储与自传体记忆 | ~/实验室仓库/项目文件/2026-04-01_数字化存储与自传体记忆/ | 研究数字化存储对自传体记忆的影响机制 |
| 2026-04-01_跨期选择的年龄差异 | ~/实验室仓库/项目文件/2026-04-01_跨期选择的年龄差异/ | 研究不同年龄群体在跨期选择任务中的决策差异 |
| 2026-04-04_影响者营销中的自我扩展机制 | ~/实验室仓库/项目文件/2026-04-04_影响者营销中的自我扩展机制/ | 研究影响者营销中自我扩展机制对消费意愿的影响 |
| 2026-04-05_Zotero文件管理 | ~/实验室仓库/项目文件/2026-04-05_Zotero文件管理/ | Zotero文献管理和学习项目 |
| 2026-04-05_审稿学习 | ~/实验室仓库/项目文件/2026-04-05_审稿学习/ | 审稿学习项目，包含各类审稿范文 |
| 2026-04-05_科研实验室搭建 | ~/实验室仓库/项目文件/2026-04-05_科研实验室搭建/ | 基于心理学理论重构Agent配置体系，介绍实验室搭建方法 |
| 2026-04-05_范文学习 | ~/实验室仓库/项目文件/2026-04-05_范文学习/ | 范文学习项目，包含各类论文范文和写作模板 |
| 2026-04-07_维护老板信息 | ~/实验室仓库/项目文件/2026-04-07_维护老板信息/ | 老板的个人信息、学术成就和账户信息管理项目 |

---

## 索引

### 公共技能索引
> 大管家统一维护

| 技能名称 | 触发示例 | 描述 | 路径 |
|---------|---------|------|------|
| 修改文档 | 需要修改已存在的文档文件 | 修改文档文件，保存新版本并记录修改历史 | ~/.openclaw/scripts/修改文档/SKILL.md |
| 撰写脚本 | 需要创建新的操作脚本 | 按照五要素SOP规范撰写新脚本 | ~/.openclaw/scripts/撰写脚本/SKILL.md |
| 撰写技能 | 需要创建新的技能 | 创建新的技能（结构化或非结构化） | ~/.openclaw/scripts/撰写技能/SKILL.md |
| knowledge-manager | 检索文献、更新知识库、总结笔记、提取笔记 | 知识管理工具，支持文献检索、知识库维护、笔记处理等功能 | ~/.openclaw/skills/knowledge-manager/SKILL.md |
| 管理项目元数据 | 需要创建或维护项目 | 创建和维护项目元数据，管理云文档映射 | ~/.openclaw/scripts/管理项目元数据/SKILL.md |
| 记录工作日志 | 任务执行完成 | 记录任务执行日志 | ~/.openclaw/scripts/记录工作日志/SKILL.md |
| feishu-doc-manager | 上传飞书云文档 | Markdown 渲染、权限管理、长文档处理 | ~/.openclaw/skills/feishu-doc-manager/SKILL.md |
| tencent-docs | 上传腾讯云文档 | 使用 md 上传 | ~/.openclaw/skills/tencent-docs/SKILL.md |
| Zotero | 管理文献、搜索文献 | Zotero 文献管理 | ~/.openclaw/skills/zotero/SKILL.md |
---

### 个人技能索引
> 大管家维护格式
> 内容由各代理独立维护
| 技能名称 | 触发示例 | 描述 | 路径 |
|---------|---------|------|------|
| 每日维护 | 每日维护任务、工作空间维护 | 执行每日维护：TOOLS.md更新、工作记忆清理、工作空间检查 | ~/.openclaw/workspace/physicist/skills/每日维护/SKILL.md |
| 维护工作记忆 | 工作记忆清理、任务归档 | 清理MEMORY.md中的completed/killed任务，归档到事件记忆 | ~/.openclaw/workspace/physicist/skills/维护工作记忆/SKILL.md |
| update_tools | TOOLS.md更新 | 自动更新TOOLS.md：存储位置、项目列表、脚本索引 | ~/.openclaw/workspace/physicist/skills/update_tools/SKILL.md |
| github | GitHub操作、代码同步 | 使用 gh CLI 进行 GitHub 交互、拉取/推送代码、管理 issues/PRs | ~/.openclaw/skills/github/SKILL.md |
| lab-backup-manager | 备份 | 使用backup_openclaw_config.sh脚本自动备份OpenClaw核心配置文件到GitHub，轻量级备份策略 | ~/.openclaw/skills/lab-backup-manager/SKILL.md |
| docx-cn | Word文档处理 | 创建、读取、编辑Word文档，支持格式化、表格、图片 | ~/.openclaw/skills/docx-cn/SKILL.md |
| docx-generator | Word文档生成 | 编程方式生成包含页脚的Microsoft Word文档 | ~/.openclaw/skills/docx-generator/SKILL.md |
| excel-xlsx | Excel文件处理 | 创建、编辑Excel工作簿，支持公式、格式化、模板 | ~/.openclaw/skills/excel-xlsx/SKILL.md |
| pdf | PDF处理 | 提取PDF文本和表格、创建PDF、合并拆分文档 | ~/.openclaw/skills/pdf/SKILL.md |
| pdf-generator | PDF生成 | 从Markdown、HTML、数据生成专业PDF文档 | ~/.openclaw/skills/pdf-generator/SKILL.md |
| pdf-processing | PDF高级处理 | 填写PDF表单、合并文档、提取内容 | ~/.openclaw/skills/pdf-processing/SKILL.md |
| pptx | PPT文件处理 | 创建、读取、编辑PPT演示文稿，支持模板、布局 | ~/.openclaw/skills/pptx-2/SKILL.md |
| pptx-generator | PPT生成 | 创建专业可编辑PowerPoint演示文稿，支持多种样式 | ~/.openclaw/skills/pptx-generator/SKILL.md |
| summarize | 内容总结 | 总结URL、文件（网页、PDF、图片、音频、YouTube） | ~/.openclaw/skills/summarize/SKILL.md |
| tencent-meeting-skill | 腾讯会议管理 | 预约/修改/取消会议、查询参会人、获取会议录制 | ~/.openclaw/skills/tencent-meeting-skill/SKILL.md |
| tencent-cos-skill | 腾讯云COS管理 | 上传/下载/管理云存储文件，图片处理、文档转PDF | ~/.openclaw/skills/tencent-cos-skill/SKILL.md |
| tencentcloud-lighthouse-skill | 腾讯云轻量服务器管理 | 查询实例、监控告警、防火墙管理、远程命令执行 | ~/.openclaw/skills/tencentcloud-lighthouse-skill/SKILL.md |
| find-skills | 技能查找与安装 | 查找、安装、更新Agent技能，优先使用skillhub | ~/.openclaw/skills/find-skills/SKILL.md |
| skillhub-preference | 技能源配置 | 优先使用skillhub进行技能发现/安装/更新 | ~/.openclaw/skills/skillhub-preference/SKILL.md |
| memory-hygiene | 记忆优化 | 审计、清理、优化向量记忆，降低token使用 | ~/.openclaw/skills/memory-hygiene/SKILL.md |
| mcp-adapter | MCP服务器集成 | 访问外部工具和数据源，扩展Agent能力 | ~/.openclaw/skills/mcp-adapter/SKILL.md |

---

### 个人脚本索引
> 大管家维护格式
> 内容由各代理独立维护
| 脚本名称 | 触发示例 | 描述 | 路径 |
|----------|----------|----------|----------|------|
||||||
*最后重构: 2026-04-09*
*重构者: 大管家*
