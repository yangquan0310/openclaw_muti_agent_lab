# 公共技能目录

本目录存放实验室成员共享的公共技能。

## 目录位置

`/root/.openclaw/workspace/skills/`

## 公共技能索引表

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
| github | GitHub操作 | GitHub代码托管操作技能 | `workspace/skills/github/SKILL.md` |
| ima-skills | IMA知识管理 | IMA知识库管理技能 | `workspace/skills/ima-skills/SKILL.md` |
| knowledge-manager | 知识管理 | 文献检索、知识库维护、笔记处理 | `workspace/skills/knowledge-manager/SKILL.md` |
| mcp-adapter | MCP适配器 | MCP协议适配工具 | `workspace/skills/mcp-adapter/SKILL.md` |
| memory-hygiene | 记忆清理 | 工作记忆清理和维护工具 | `workspace/skills/memory-hygiene/SKILL.md` |
| pdf-generator | PDF生成 | PDF文档生成工具 | `workspace/skills/pdf-generator/SKILL.md` |
| pdf-processing | PDF处理 | PDF文件处理技能 | `workspace/skills/pdf-processing/SKILL.md` |
| pdf | PDF工具 | PDF基础操作工具 | `workspace/skills/pdf/SKILL.md` |
| pptx-2 | PPT处理 | PowerPoint文档处理技能 | `workspace/skills/pptx-2/SKILL.md` |
| pptx-generator | PPT生成 | PowerPoint自动生成工具 | `workspace/skills/pptx-generator/SKILL.md` |
| scihub-paper-downloader | SciHub下载 | 学术论文下载工具 | `workspace/skills/scihub-paper-downloader/SKILL.md` |
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

## 技能列表

### agent_self_development 子模块

| 子模块 | 路径 | 功能描述 |
|--------|------|----------|
| **metacognition** | `agent_self_development/metacognition/SKILL.md` | 元认知模块（计划/监控/调节） |
| ├─ planning | `metacognition/planning/SKILL.md` | 计划阶段 - 任务拆解与计划制定 |
| ├─ monitoring | `metacognition/monitoring/SKILL.md` | 监控阶段 - 进度跟踪与偏差检测 |
| └─ regulation | `metacognition/regulation/SKILL.md` | 调节阶段 - 策略调整与计划修正 |
| **working_memory** | `agent_self_development/working_memory/SKILL.md` | 工作记忆模块（任务/子代理管理） |
| ├─ memory_table | `working_memory/memory_table/SKILL.md` | 记忆表管理 |
| └─ subagent_tracker | `working_memory/subagent_tracker/SKILL.md` | 子代理追踪 |
| **assimilation_accommodation** | `agent_self_development/assimilation_accommodation/SKILL.md` | 同化与顺应模块（自我更新） |
| ├─ diary | `assimilation_accommodation/diary/SKILL.md` | 发展日记 |
| ├─ core_self_update | `assimilation_accommodation/core_self_update/SKILL.md` | 核心自我更新 |
| ├─ identity_update | `assimilation_accommodation/identity_update/SKILL.md` | 身份更新 |
| ├─ belief_style_update | `assimilation_accommodation/belief_style_update/SKILL.md` | 信念与风格更新 |
| └─ self_identity_update | `assimilation_accommodation/self_identity_update/SKILL.md` | 自我认同更新 |

各代理可通过 `~/.openclaw/workspace/skills/README.md` 查看完整的公共技能索引。
