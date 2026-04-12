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
| 文件 | 存储路径 | 说明 |
|----------|----------|------|
| Agent 个人记忆 | ~/.openclaw/workspace/reviewer/MEMORY.md | 审稿助手独立维护 |
| Agent 个人脚本 | ~/.openclaw/workspace/reviewer/scripts/README.md | 审稿助手专属脚本存储目录 |
| Agent 个人技能 | ~/.openclaw/workspace/reviewer/skills/README.md | 审稿助手专属技能存储目录 |
| Agent 临时文件 | ~/.openclaw/workspace/reviewer/temp/README.md | 审稿助手专属临时文件存储目录 |
| 实验室仓库 | ~/实验室仓库/ | 实验室仓库 |
| 实验室项目 | ~/实验室仓库/项目文件/ | 实验室各个项目 |
| 工作日志 | ~/实验室仓库/日志文件/README.MD | 任务执行记录 |

---

## 索引
### 公共技能索引
> 大管家统一维护

| 技能名称 | 触发示例 | 描述 | 路径 |
|---------|---------|------|------|
| 修改文档 | 需要修改已存在的文档文件 | 修改文档文件，保存新版本并记录修改历史 | ~/.openclaw/scripts/修改文档/SKILL.md |
| 撰写脚本 | 需要创建新的操作脚本 | 按照五要素SOP规范撰写新脚本 | ~/.openclaw/scripts/撰写脚本/SKILL.md |
| 撰写技能 | 需要创建新的技能 | 创建新的技能（结构化或非结构化） | ~/.openclaw/scripts/撰写技能/SKILL.md |
| 检索文献 | 需要检索学术文献 | 使用Zotero和Semantic Scholar检索学术文献 | ~/.openclaw/scripts/检索文献/SKILL.md |
| 管理项目元数据 | 需要创建或维护项目 | 创建和维护项目元数据，管理云文档映射 | ~/.openclaw/scripts/管理项目元数据/SKILL.md |
| 记录工作日志 | 任务执行完成 | 记录任务执行日志 | ~/.openclaw/scripts/记录工作日志/SKILL.md |
| feishu-doc-manager | 上传飞书云文档 | Markdown 渲染、权限管理、长文档处理 | ~/.openclaw/skills/feishu-doc-manager/SKILL.md |
| tencent-docs | 上传腾讯云文档 | 使用 md 上传 | ~/.openclaw/skills/tencent-docs/SKILL.md |
| Zotero | 管理文献、搜索文献 | Zotero 文献管理 | ~/.openclaw/skills/zotero/SKILL.md |

### 个人技能索引
| 触发条件 | 技能名称 | 功能描述 | SKILL.md |
|----------|----------|----------|----------|
| 需要自动更新 TOOLS.md 文件 | update_tools | 扫描项目文件夹，更新项目列表和脚本索引 | [SKILL.md](skills/update_tools/SKILL.md) |
| 每日定时执行维护任务 | daily_maintenance | 合并执行 TOOLS 更新、工作记忆维护、工作空间维护 | [SKILL.md](skills/daily_maintenance/SKILL.md) |
| 需要清理工作记忆 | memory_maintenance | 清理非活跃任务，归档 completed 任务 | [SKILL.md](skills/memory_maintenance/SKILL.md) |
---

### 个人脚本索引

| 触发条件 | 脚本编号 | 脚本名称 | 功能描述 | SKILL.md |
|----------|----------|----------|----------|----------|
| 收到论文评审请求，需要评估论文质量 | S1 | 论文审稿脚本 | 对论文进行多维度质量审查，生成结构化评审报告和修改建议 | [SKILL.md](scripts/paper_review/SKILL.md) |

---

*最后重构: 2026-04-11*
*重构者: 审稿助手*
