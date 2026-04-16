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
| Agent 个人记忆 | ~/.openclaw/workspace/reviewer/MEMORY.md | 审稿助手独立维护 |
| Agent 个人技能 | ~/.openclaw/workspace/reviewer/skills/README.md | 审稿助手专属技能存储目录（含原脚本内容） |
| Agent 临时文件 | ~/.openclaw/workspace/reviewer/temp/README.md | 审稿助手专属临时文件存储目录 |
| 实验室仓库 | ~/实验室仓库/README.md | 实验室仓库 |
| 实验室项目 | ~/实验室仓库/项目文件/README.md | 实验室各个项目 |
| 工作日志 | ~/实验室仓库/日志文件/README.md | 任务执行记录 |
| 项目知识库 | ~/实验室仓库/项目文件/{项目名}/知识库/index.json | 项目专属文献知识库索引 |

## 项目
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
### 项目表
| 项目名称 | 路径 | 状态 |
|----------|------|------|
| AI降重提示工程 | ~/实验室仓库/项目文件/AI降重提示工程 | 活跃 |
| Zotero文件管理 | ~/实验室仓库/项目文件/Zotero文件管理 | 活跃 |
| 内卷感知与工作繁荣 | ~/实验室仓库/项目文件/内卷感知与工作繁荣 | 活跃 |
| 学生论文修改 | ~/实验室仓库/项目文件/学生论文修改 | 活跃 |
| 审稿学习 | ~/实验室仓库/项目文件/审稿学习 | 活跃 |
| 影响者营销中的自我扩展机制 | ~/实验室仓库/项目文件/影响者营销中的自我扩展机制 | 活跃 |
| 数字化存储与自传体记忆 | ~/实验室仓库/项目文件/数字化存储与自传体记忆 | 活跃 |
| 科研实验室搭建 | ~/实验室仓库/项目文件/科研实验室搭建 | 活跃 |
| 维护老板信息 | ~/实验室仓库/项目文件/维护老板信息 | 活跃 |
| 范文学习 | ~/实验室仓库/项目文件/范文学习 | 活跃 |
| 跨期选择的年龄差异 | ~/实验室仓库/项目文件/跨期选择的年龄差异 | 活跃 |
---

## 索引
### 公共技能索引
> 大管家统一维护，索引文件位于 `~/.openclaw/workspace/skills/README.md`

| 技能名称 | 触发示例 | 描述 | 路径 |
|---------|---------|------|------|
| agent-browser | 浏览器自动化 | Headless browser automation CLI | ~/.openclaw/workspace/skills/agent-browser-clawdbot/SKILL.md |
| baidu-scholar | 百度学术搜索 | 百度学术文献检索 | ~/.openclaw/workspace/skills/baidu-scholar-search/SKILL.md |
| cnki-search | 知网高级检索 | CNKI高级检索自动化 | ~/.openclaw/workspace/skills/cnki-advanced-search/SKILL.md |
| docx | Word文档处理 | 创建、读取、编辑Word文档 | ~/.openclaw/workspace/skills/docx-cn/SKILL.md |
| docx-generator | Word文档生成 | 创建含AI生成页脚的Word文档 | ~/.openclaw/workspace/skills/docx-generator/SKILL.md |
| excel | Excel处理 | 创建、编辑Excel工作簿 | ~/.openclaw/workspace/skills/excel-xlsx/SKILL.md |
| feishu-calendar | 飞书日历 | 飞书日历高级管理 | ~/.openclaw/workspace/skills/feishu-calendar-advanced/SKILL.md |
| find-skills | 技能发现 | 查找和安装技能 | ~/.openclaw/workspace/skills/find-skills/SKILL.md |
| github | GitHub交互 | 使用gh CLI操作GitHub | ~/.openclaw/workspace/skills/github/SKILL.md |
| ima-skills | IMA技能 | IMA相关技能集合 | ~/.openclaw/workspace/skills/ima-skills/SKILL.md |
| knowledge-manager | 知识管理 | 文献检索、知识库维护 | ~/.openclaw/workspace/skills/knowledge-manager/SKILL.md |
| mcp-adapter | MCP集成 | Model Context Protocol服务器 | ~/.openclaw/workspace/skills/mcp-adapter/SKILL.md |
| memory-hygiene | 记忆清理 | 审计和优化向量记忆 | ~/.openclaw/workspace/skills/memory-hygiene/SKILL.md |
| pdf | PDF处理 | PDF操作工具包 | ~/.openclaw/workspace/skills/pdf/SKILL.md |
| pdf-generator | PDF生成 | 从Markdown/HTML生成PDF | ~/.openclaw/workspace/skills/pdf-generator/SKILL.md |
| pdf-processing | PDF处理(中文) | 提取文本和表格、填写表单 | ~/.openclaw/workspace/skills/pdf-processing/SKILL.md |
| pptx | PPT处理 | 读取、创建、编辑PPT | ~/.openclaw/workspace/skills/pptx-2/SKILL.md |
| pptx-generator | PPT生成 | 专业PPT生成器 | ~/.openclaw/workspace/skills/pptx-generator/SKILL.md |
| scihub | Sci-Hub下载 | 获取Sci-Hub PDF链接 | ~/.openclaw/workspace/skills/scihub-paper-downloader/SKILL.md |
| skill-developer | 技能开发 | 创建和编辑Agent技能 | ~/.openclaw/workspace/skills/Skill-developer/SKILL.md |
| skillhub | 技能中心 | 技能发现与安装偏好 | ~/.openclaw/workspace/skills/skillhub-preference/SKILL.md |
| subagents | 子代理管理 | 子代理创建与管理 | ~/.openclaw/workspace/skills/Subagents-manager/SKILL.md |
| summarize | 内容总结 | 总结URL或文件 | ~/.openclaw/workspace/skills/summarize/SKILL.md |
| tavily | Tavily搜索 | 网络搜索 | ~/.openclaw/workspace/skills/openclaw-tavily-search/SKILL.md |
| tencent-cloud | 腾讯云COS | 腾讯云对象存储 | ~/.openclaw/workspace/skills/tencent-cos-skill/SKILL.md |
| tencent-docs | 腾讯文档 | 腾讯文档管理 | ~/.openclaw/workspace/skills/tencent-docs/SKILL.md |
| tencent-lighthouse | 轻量服务器 | 腾讯云Lighthouse管理 | ~/.openclaw/workspace/skills/tencentcloud-lighthouse-skill/SKILL.md |
| tencent-meeting | 腾讯会议 | 腾讯会议管理 | ~/.openclaw/workspace/skills/tencent-meeting-skill/SKILL.md |
| web-tools | Web工具 | 搜索/抓取/浏览器策略 | ~/.openclaw/workspace/skills/web-tools-guide/SKILL.md |
| zotero | Zotero管理 | 文献库管理 | ~/.openclaw/workspace/skills/zotero/SKILL.md |
| zotero-import | Zotero导入 | 本地PDF导入Zotero | ~/.openclaw/workspace/skills/zotero-local-pdf-import/SKILL.md |
| zotero-scholar | Zotero学术 | Zotero学术文献管理 | ~/.openclaw/workspace/skills/zotero-scholar/SKILL.md |
| zotero-vectorize | Zotero向量化 | 语义索引构建 | ~/.openclaw/workspace/skills/zotero-vectorize/SKILL.md |

### 个人技能索引
> 当前个人技能文件夹为空，仅保留 README.md

| 触发条件 | 技能名称 | 功能描述 | SKILL.md |
|----------|----------|----------|----------|
| - | - | - | - |

---
*最后更新: 2026-04-16*
*更新者: 审稿助手*
*更新说明: 统一技能路径格式，新增ima-skills/zotero-scholar技能，添加项目表*
