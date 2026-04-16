# TOOLS.md

> 配置档案

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
| 实验室仓库 | ~/实验室仓库/README.md | 实验室仓库 |
| 教研室仓库 | ~/教研室仓库/README.md | 教学研究、教务管理和学生工作相关文件存储 |

### 私人存储位置

| 文件 | 存储路径 | 说明 |
|----------|----------|------|
| Agent 个人记忆 | ~/.openclaw/workspace/academicassistant/MEMORY.md | 教务助手独立维护 |
| Agent 个人技能 | ~/.openclaw/workspace/academicassistant/skills/README.md | 教务助手专属技能存储目录 |
| Agent 临时文件 | ~/.openclaw/workspace/academicassistant/temp/README.md | 教务助手专属临时文件存储目录 |
| 工作日志 | ~/教研室仓库/日志文件/README.MD | 任务执行记录 |
| 教务助手仓库 |	~/教研室仓库/教务归档/README.MD	|教务助手用来进行工作的文件夹、其他成员不可以写入，只能读取|
| 教务助手项目 |	~/教研室仓库/教务归档/项目文件/README.MD	|教务助手用来存储项目的文件夹、其他成员不可以写入，只能读取|
---

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

## 项目

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

**教研室项目（私人项目库）：**
| 项目名 | 存储位置 | 描述 |
|--------|----------|------|
| *当前无项目* | - | - |

---
## 索引

### 公共技能索引
| 技能名称 | 触发示例 | 描述 | 路径 |
|---------|---------|------|------|
| agent-browser-clawdbot | 浏览器自动化 | Headless浏览器自动化CLI，支持可访问性树快照 | `~/.openclaw/workspace/skills/agent-browser-clawdbot/` |
| baidu-scholar-search | 百度学术搜索 | 中英文文献检索，覆盖期刊、会议、学位论文 | `~/.openclaw/workspace/skills/baidu-scholar-search/` |
| cnki-advanced-search | 知网检索 | 知网高级检索CSSCI论文，提取题录和摘要 | `~/.openclaw/workspace/skills/cnki-advanced-search/` |
| docx-cn | Word处理 | 创建、编辑Word文档，支持格式、表格、图片 | `~/.openclaw/workspace/skills/docx-cn/` |
| docx-generator | Word生成器 | AI生成页脚的Microsoft Word文档 | `~/.openclaw/workspace/skills/docx-generator/` |
| excel-xlsx | Excel处理 | 创建、编辑、检查Excel工作簿，支持公式、格式、模板 | `~/.openclaw/workspace/skills/excel-xlsx/` |
| feishu-calendar-advanced | 飞书日历 | 飞书日历管理，查看、创建、删除日程 | `~/.openclaw/workspace/skills/feishu-calendar-advanced/` |
| github | GitHub操作 | 使用gh CLI操作Issues、PRs、CI工作流 | `~/.openclaw/workspace/skills/github/` |
| knowledge-manager | 文献检索、知识库管理 | 文献检索、总结、管理、综述撰写 | `~/.openclaw/workspace/skills/knowledge-manager/` |
| mcp-adapter | MCP集成 | 使用Model Context Protocol访问外部工具和数据源 | `~/.openclaw/workspace/skills/mcp-adapter/` |
| memory-hygiene | 内存清理 | 审计、清理和优化Clawdbot的向量内存 | `~/.openclaw/workspace/skills/memory-hygiene/` |
| openclaw-tavily-search | Tavily搜索 | 使用Tavily API进行网络搜索 | `~/.openclaw/workspace/skills/openclaw-tavily-search/` |
| pdf | PDF处理 | PDF文本提取、合并分割、创建、表单填写 | `~/.openclaw/workspace/skills/pdf/` |
| pdf-generator | PDF生成器 | 从Markdown、HTML、数据生成专业PDF文档 | `~/.openclaw/workspace/skills/pdf-generator/` |
| pdf-processing | PDF处理 | PDF文本和表格提取、表单填写、合并文档 | `~/.openclaw/workspace/skills/pdf-processing/` |
| pptx-2 | PPT处理 | 创建、编辑、读取PPT演示文稿，支持模板和设计 | `~/.openclaw/workspace/skills/pptx-2/` |
| pptx-generator | PPT生成器 | 专业PPT生成器，支持多种风格和布局 | `~/.openclaw/workspace/skills/pptx-generator/` |
| scihub-paper-downloader | Sci-Hub下载 | 从Sci-Hub获取PDF链接 | `~/.openclaw/workspace/skills/scihub-paper-downloader/` |
| Skill-developer | 技能开发 | 技能开发和维护工具 | `~/.openclaw/workspace/skills/Skill-developer/` |
| Subagents-manager | 子代理管理 | 子代理创建、监控和管理 | `~/.openclaw/workspace/skills/Subagents-manager/` |
| summarize | 内容总结 | 总结URL、PDF、图片、音频、YouTube内容 | `~/.openclaw/workspace/skills/summarize/` |
| tencentcloud-lighthouse-skill | 腾讯云轻量服务器 | 管理腾讯云Lighthouse实例 | `~/.openclaw/workspace/skills/tencentcloud-lighthouse-skill/` |
| tencent-cos-skill | 腾讯云COS | 腾讯云对象存储管理和图片处理 | `~/.openclaw/workspace/skills/tencent-cos-skill/` |
| tencent-docs | 腾讯文档 | 腾讯文档创建、编辑、管理 | `~/.openclaw/workspace/skills/tencent-docs/` |
| tencent-meeting-skill | 腾讯会议 | 腾讯会议预约、管理、录制 | `~/.openclaw/workspace/skills/tencent-meeting-skill/` |
| web-tools-guide | Web工具策略 | 搜索、抓取、浏览器自动化的策略指南 | `~/.openclaw/workspace/skills/web-tools-guide/` |
| zotero | Zotero文献管理 | 管理Zotero文献库，支持DOI/ISBN/PMID添加、导出、PDF获取 | `~/.openclaw/workspace/skills/zotero/` |
| zotero-local-pdf-import | Zotero本地导入 | 通过本地连接器导入PDF到Zotero | `~/.openclaw/workspace/skills/zotero-local-pdf-import/` |
| zotero-scholar | Zotero学术搜索 | Zotero学术文献搜索 | `~/.openclaw/workspace/skills/zotero-scholar/` |
| zotero-vectorize | Zotero向量化 | 构建Zotero语义索引 | `~/.openclaw/workspace/skills/zotero-vectorize/` |

### 个人技能索引

| 技能名称 | 触发示例 | 描述 | 路径 |
|---------|---------|------|------|
| *当前无个人技能* | - | - | - |

---

*最后重构: 2026-04-16*
*重构者: 教务助手*
