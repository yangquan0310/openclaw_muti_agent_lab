# 公共技能目录

本目录存放实验室成员共享的公共技能。

## 目录位置

`/root/.openclaw/workspace/skills/`

---

## 代理发展机制（agent_self_development）

> 基于皮亚杰认知发展理论 + Baddeley 工作记忆模型构建的 Agent 自我进化系统

### 核心工作流

```
每日 00:00 定时触发
    ↓
1. 阅读当日事件记忆（memory/YYYY-MM-DD/HH-MM-SS-{event}.md）
    ↓
2. 撰写/完善发展日记（memory/YYYY-MM-DD/diary.md）
    ↓
3. 阅读核心自我（MEMORY.md/SOUL.md/IDENTITY.md/skills/README.md）
    ↓
4. 同化与顺应分析
    ↓
5. 检测更新触发信号（自我认知/角色/风格-信念/技能）
    ↓
6. 执行相应更新
    ↓
7. 记录更新日志
```

### 更新类型

| 更新维度 | 触发条件 | 目标文件 |
|----------|----------|----------|
| **核心自我** | 能力边界变化 | MEMORY.md（核心自我认知） |
| **身份** | 角色变化 | IDENTITY.md（角色集、社会身份） |
| **风格-信念** | 价值观/工作方式变化 | SOUL.md（工作信念、风格） |
| **技能** | 习得/细化/淘汰 | skills/README.md（个人技能索引） |

### 详细文档

- [agent_self_development/README.md](agent_self_development/README.md) - 完整概述
- [agent_self_development/SKILL.md](agent_self_development/SKILL.md) - 根路由
- [agent_self_development/assimilation_accommodation/SKILL.md](agent_self_development/assimilation_accommodation/SKILL.md) - 同化顺应模块
- [agent_self_development/working_memory/SKILL.md](agent_self_development/working_memory/SKILL.md) - 工作记忆模块

---

## MCP 服务器支持

以下公共技能已添加 MCP 服务器支持，可通过 OpenClaw MCP 接口调用：

| 技能名称 | MCP 工具 | 描述 |
|---------|---------|------|
| **knowledge-manager** | km_root, km_search, km_summarize, km_manage, km_synthesize | 知识库管理 MCP 工具 |
| **agent_self_development** | asd_root, asd_metacognition, asd_working_memory, asd_assimilation | Agent 自我发展 MCP 工具 |
| **Skill-developer** | skill_dev_create, skill_dev_mcp, skill_dev_extend | 技能开发 MCP 工具 |

> 注：MCP 服务器文件位于各技能的 `mcp/server.py`，注册配置在 `openclaw.json` 的 `mcp.servers` 中。

---
## 公共技能索引表

| 技能名称 | 触发示例 | 描述 | 路径 |
|---------|---------|------|------|
| agent-browser-clawdbot | 浏览器自动化、网页抓取 | 基于 Clawdbot 的浏览器自动化工具 | `workspace/skills/agent-browser-clawdbot/SKILL.md` |
| **agent_self_development** | **Agent自我发展** | **基于认知发展理论的Agent自我进化系统**<br>• 定时任务：每日00:00执行自我更新<br>• 工作流：记录日记→同化顺应分析→执行更新<br>• 更新类型：核心自我/身份/风格-信念/技能 | **`workspace/skills/agent_self_development/SKILL.md`** |
| docx-cn | Word文档处理 | 中文Word文档处理技能 | `workspace/skills/docx-cn/SKILL.md` |
| docx-generator | Word文档生成 | Word文档自动生成工具 | `workspace/skills/docx-generator/SKILL.md` |
| excel-xlsx | Excel表格处理 | Excel文件处理技能 | `workspace/skills/excel-xlsx/SKILL.md` |
| find-skills | 查找技能 | 技能发现和安装工具 | `workspace/skills/find-skills/SKILL.md` |
| github | GitHub操作 | GitHub代码托管操作技能 | `workspace/skills/github/SKILL.md` |
| ima-skills | IMA知识管理 | IMA知识库管理技能 | `workspace/skills/ima-skills/SKILL.md` |
| knowledge-manager | 知识管理 | 文献检索、知识库维护、笔记处理 | `workspace/skills/knowledge-manager/SKILL.md` |
| memory-hygiene | 记忆清理 | 工作记忆清理和维护工具 | `workspace/skills/memory-hygiene/SKILL.md` |
| openclaw-tavily-search | Tavily搜索 | 使用Tavily API进行网络搜索 | `workspace/skills/openclaw-tavily-search/SKILL.md` |
| pdf-generator | PDF生成 | PDF文档生成工具 | `workspace/skills/pdf-generator/SKILL.md` |
| pdf-processing | PDF处理 | PDF文件处理技能 | `workspace/skills/pdf-processing/SKILL.md` |
| pdf | PDF工具 | PDF基础操作工具 | `workspace/skills/pdf/SKILL.md` |
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

