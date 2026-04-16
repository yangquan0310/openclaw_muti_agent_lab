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
| 实验室仓库 | ~/实验室仓库/README.md | 实验室仓库 |
| 教研室仓库 | ~/教研室仓库/README.md | 教学研究、教务管理和学生工作相关文件存储 |

### 私人存储位置
> 大管家维护格式
> 内容由各代理独立维护
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

### 公共技能索引
| 技能名称 | 触发示例 | 描述 | 路径 |
|---------|---------|------|------|
| knowledge-manager | 文献检索、知识库管理 | 文献检索、总结、管理、综述撰写 | `~/.openclaw/workspace/skills/knowledge-manager/` |
| zotero | Zotero文献管理 | 管理Zotero文献库，支持DOI/ISBN/PMID添加、导出、PDF获取 | `~/.openclaw/workspace/skills/zotero/` |
| cnki-advanced-search | 知网检索 | 知网高级检索CSSCI论文，提取题录和摘要 | `~/.openclaw/workspace/skills/cnki-advanced-search/` |
| baidu-scholar-search | 百度学术搜索 | 中英文文献检索，覆盖期刊、会议、学位论文 | `~/.openclaw/workspace/skills/baidu-scholar-search/` |
| excel-xlsx | Excel处理 | 创建、编辑、检查Excel工作簿，支持公式、格式、模板 | `~/.openclaw/workspace/skills/excel-xlsx/` |
| pptx-2 | PPT处理 | 创建、编辑、读取PPT演示文稿，支持模板和设计 | `~/.openclaw/workspace/skills/pptx-2/` |
| pdf | PDF处理 | PDF文本提取、合并分割、创建、表单填写 | `~/.openclaw/workspace/skills/pdf/` |
| docx-cn | Word处理 | 创建、编辑Word文档，支持格式、表格、图片 | `~/.openclaw/workspace/skills/docx-cn/` |
| github | GitHub操作 | 使用gh CLI操作Issues、PRs、CI工作流 | `~/.openclaw/workspace/skills/github/` |
| summarize | 内容总结 | 总结URL、PDF、图片、音频、YouTube内容 | `~/.openclaw/workspace/skills/summarize/` |
| web-tools-guide | Web工具策略 | 搜索、抓取、浏览器自动化的策略指南 | `~/.openclaw/workspace/skills/web-tools-guide/` |

### 个人技能索引
| 技能名称 | 触发示例 | 描述 | 路径 |
|---------|---------|------|------|
| convert_syllabus | 转换课程大纲格式 | 将Word格式课程大纲转换为Markdown | `~/.openclaw/workspace/academicassistant/skills/convert_syllabus/` |
| update_index | 更新项目索引 | 更新教研室项目文件的索引 | `~/.openclaw/workspace/academicassistant/skills/update_index/` |
| update_syllabi | 批量更新课程大纲 | 批量处理课程大纲文件 | `~/.openclaw/workspace/academicassistant/skills/update_syllabi/` |
| update_tools_md | 自动更新工具索引文档 | 自动维护TOOLS.md文档内容 | `~/.openclaw/workspace/academicassistant/skills/update_tools_md/` |

---

*最后重构: 2026-04-16*
*重构者: 教务助手*
