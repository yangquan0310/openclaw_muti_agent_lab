# OpenClaw 多Agent智能协作系统

![OpenClaw](https://img.shields.io/badge/OpenClaw-v2.0-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Agents](https://img.shields.io/badge/Agents-9%20个-orange.svg)
![Skills](https://img.shields.io/badge/Skills-20%2B-yellow.svg)

## 👥 团队成员

### 实验室成员（研究团队）
| 成员 | 角色 | 研究领域 |
|------|------|----------|
| 杨权 | 实验室负责人 | 心理学、认知科学、数字化记忆 |
| 数学家Agent | 科研助理 | 数学建模、统计分析、数据处理 |
| 物理学家Agent | 科研助理 | 物理建模、理论推导、量化分析 |
| 心理学家Agent | 科研助理 | 心理学理论、实验设计、数据分析 |
| 写作助手Agent | 科研助理 | 论文撰写、内容创作、文档编辑 |
| 审稿助手Agent | 科研助理 | 论文审查、质量控制、格式规范 |
| 大管家Agent | 系统管理员 | 文档管理、系统维护、协调调度 |

### 教研室成员（教学团队）
| 成员 | 角色 | 职责范围 |
|------|------|----------|
| 教学助手Agent | 教学助理 | 课程备课、课件制作、作业批改 |
| 教务助手Agent | 教务管理 | 排课安排、成绩管理、教务归档 |
| 学工助手Agent | 学生工作 | 学生管理、心理咨询、就业指导 |

## 🤖 Agent任务分工

### 核心科研Agent
| Agent | 主要任务 | 触发关键词 |
|-------|----------|------------|
| **数学家** | 统计分析、数学建模、算法实现 | 统计、建模、数据分析、计算、算法 |
| **物理学家** | 物理建模、理论推导、量化研究 | 建模、模拟、物理分析、理论推导 |
| **心理学家** | 理论审核、实验设计、结果解释 | 心理学、实验设计、理论分析、问卷设计 |
| **写作助手** | 论文撰写、内容创作、文档编辑 | 写作、编辑、翻译、润色、文档生成 |
| **审稿助手** | 质量审查、格式规范、投稿建议 | 审稿、检查、格式、投稿、审查 |
| **大管家** | 文档管理、系统维护、任务调度 | 管理、维护、备份、同步、调度 |

### 教学辅助Agent
| Agent | 主要任务 | 触发关键词 |
|-------|----------|------------|
| **教学助手** | 备课、课件制作、作业批改、教学资料整理 | 备课、课件、作业、教学、课程 |
| **教务助手** | 排课、成绩管理、教务系统维护、毕业审核 | 教务、排课、成绩、毕业、归档 |
| **学工助手** | 学生管理、心理咨询、就业指导、资助管理 | 学生、心理、就业、资助、学工 |

## 📁 仓库文件结构

```
.openclaw/
├── README.md                          # 本说明文件
├── .gitignore                         # Git忽略规则
├── openclaw.json                      # OpenClaw主配置文件
├── skills/                            # 公共技能库（所有Agent共享）
│   ├── knowledge-manager/             # 知识管理工具（文献检索+知识库管理+笔记生成+综述合成）
│   │   ├── search/                     # 文献检索模块
│   │   │   ├── Searcher.py             # 文献检索类：多主题多轮检索，支持每轮单独条件
│   │   │   └── SKILL.md               # 检索模块说明
│   │   ├── summarize/                  # 文献总结模块
│   │   │   ├── Summarizer.py           # 文献总结类：LLM分析，添加labels和notes
│   │   │   └── SKILL.md               # 总结模块说明
│   │   ├── manage/                     # 知识库管理模块
│   │   │   ├── Manager.py              # 知识库管理类：合并、筛选、链式调用
│   │   │   └── SKILL.md               # 管理模块说明
│   │   ├── synthesize/                 # 文献综述合成模块
│   │   │   └── SKILL.md               # 综述合成模块说明
│   │   ├── config.json                 # 统一配置文件：多LLM供应商、API参数、存储规则
│   │   ├── README.md                   # 工具使用说明
│   │   └── SKILL.md                    # 主技能说明（AI入口）
│   ├── feishu-doc-manager/            # 飞书文档管理
│   ├── tencent-docs/                  # 腾讯文档管理
│   ├── tencent-cos-skill/             # 腾讯云对象存储
│   ├── tencent-meeting-skill/         # 腾讯会议管理
│   ├── tencentcloud-lighthouse-skill/ # 腾讯轻量云管理
│   ├── github/                        # GitHub仓库管理
│   ├── zotero/                        # Zotero文献管理
│   └── .skills_store_lock.json        # 技能锁定配置
├── scripts/                           # 公共SOP脚本
│   ├── agents-sop/                    # Agent标准操作流程
│   ├── 修改文档/                       # 文档修改规范
│   ├── 撰写脚本/                       # 脚本创建规范
│   ├── 撰写技能/                       # 技能创建规范
│   └── 管理项目元数据/                 # 项目元数据管理
└── workspace/                         # 所有Agent工作空间
    ├── steward/                       # 大管家工作空间（系统配置中心）
    ├── mathematician/                 # 数学家工作空间
    ├── physicist/                     # 物理学家工作空间
    ├── psychologist/                  # 心理学家工作空间
    ├── reviewer/                      # 审稿助手工作空间
    ├── writer/                        # 写作助手工作空间
    ├── teaching/                      # 教学助手工作空间
    ├── academicassistant/              # 教务助手工作空间
    └── studentaffairsassistant/        # 学工助手工作空间
```

## 📂 实验室仓库结构（独立存储）

```
实验室仓库/
├── 日程管理/                           # 日程安排、会议记录、项目计划
├── 日志文件/                           # 任务执行日志、系统操作记录
├── 项目文件/                           # 科研项目文件
│   └── <项目名>/
│       ├── 文档/                      # 用户上传的原始文档
│       ├── 草稿/                      # 论文草稿、中间版本
│       ├── 终稿/                      # 最终版本、投稿版本
│       ├── 知识库/                     # 项目专属知识库
│       │   └── 索引.json              # 文献索引、知识图谱
│       ├── 元数据.json                 # 项目元数据配置
│       └── README.md                   # 项目说明文档
└── README.md                           # 仓库说明
```

## 🏫 教研室仓库结构（独立存储）

```
教研室仓库/
├── 备课资料/                           # 课程课件、教学大纲、教案
├── 学生工作/                           # 学生信息、心理咨询记录、就业数据
├── 教务归档/                           # 教务文件、成绩记录、毕业资料
├── 日志文件/                           # 教学、教务、学工操作日志
├── 日程文件/                           # 教学日程、会议安排、工作计划
└── README.md                           # 仓库说明
```

## 🧠 知识库管理系统（knowledge-manager v2.1.0）

### 项目专属知识库
每个科研项目有独立的知识库，位于`实验室仓库/项目文件/<项目名>/知识库/`，包含：
- 项目相关的文献集合
- 数据分析结果
- 实验记录
- 阶段性报告
- 知识图谱索引

### 知识管理工具（knowledge-manager）
系统内置强大的知识管理技能，采用面向对象的四模块架构，支持多主题多轮次文献检索、LLM智能总结、知识库管理和文献综述合成。

#### 核心架构
| 模块 | 目录 | 功能说明 | 对应类 |
|------|------|----------|--------|
| **文献检索** | `search/` | 从Semantic Scholar获取数据，支持多主题多轮检索 | Searcher |
| **文献总结** | `summarize/` | 使用LLM分析文献，添加labels和notes字段 | Summarizer |
| **知识库管理** | `manage/` | 合并、筛选、保存知识库，支持链式调用 | Manager |
| **文献综述合成** | `synthesize/` | 基于知识库生成文献综述和研究现状 | Synthesizer |

#### 核心功能
| 功能 | 描述 | 触发关键词 |
|------|------|------------|
| **文献检索** | 多主题多轮次学术文献检索，每轮可单独设置query、limit、year、minCitationCount等 | 检索、文献、查资料 |
| **笔记总结** | LLM自动分析文献内容，提取核心观点，生成结构化笔记，打标签，分类 | 总结、笔记、摘要 |
| **知识库维护** | 合并知识库、筛选知识库、提取知识库 | 知识库、维护、分类 |
| **文献综述** | 基于知识库生成文献综述和研究现状 | 综述、文献综述、研究现状 |

#### 知识库特性
✅ **分级分类**：按照研究领域、文献类型、重要程度多级分类
✅ **版本控制**：记录每一次修改和更新，支持历史版本回溯
✅ **全文检索**：支持关键词、作者、发表时间等多维度检索
✅ **关联分析**：自动识别文献之间的引用关系和研究脉络
✅ **导出功能**：支持导出为Markdown、JSON、BibTeX等多种格式
✅ **多主题多轮检索**：每个主题可设置多轮检索条件，每轮单独配置query、limit、year、minCitationCount、venue等
✅ **面向对象架构**：四个独立模块，职责清晰，易于扩展和维护

#### 快速开始示例
```python
from search.Searcher import Searcher
from summarize.Summarizer import Summarizer
from manage.Manager import Manager
from synthesize.Synthesizer import Synthesizer

# 1. 多主题多轮检索（每轮可单独设置条件）
searcher = Searcher()
queries = {
    "自传体记忆基础": [
        {"query": "autobiographical memory | personal memory", "limit": 30},
        {"query": "\"self-memory system\" Conway", "year": "2010-2025", "minCitationCount": 50}
    ],
    "数字记忆": [
        {"query": "digital memory | Google effect", "limit": 20, "year": "2020-2025"}
    ]
}
kb = searcher.search(queries, kb_path="my_project.json")

# 2. 总结文献
Summarizer().summarize(kb_path="my_project.json")

# 3. 筛选和保存
Manager("my_project.json").filter({
    "citations_min": 50,
    "types": ["📊实证", "📖综述"],
    "sort_by": "citationCount",
    "limit": 10
}).save("final_kb.json")

# 4. 合成文献综述
Synthesizer().synthesize(kb_path="final_kb.json", output_path="review.md")
```

## 🚀 部署指南

### 1. 环境要求
- 操作系统: Ubuntu 22.04 LTS / macOS 13+
- Python 版本: 3.10+
- Node.js 版本: 18+
- 内存要求: 最低4GB，推荐8GB以上
- 存储要求: 至少50GB可用空间

### 2. 安装步骤

#### 第一步: 克隆仓库
```bash
git clone git@github.com:yangquan0310/openclaw_muti_agent_lab.git
cd openclaw_muti_agent_lab
```

#### 第二步: 安装OpenClaw
```bash
# 安装OpenClaw CLI
npm install -g @openclaw/cli

# 初始化配置
openclaw init --config openclaw.json
```

#### 第三步: 恢复工作空间
```bash
# 恢复所有Agent工作空间
cp -r workspace/* /root/.openclaw/workspace/
```

#### 第四步: 安装依赖
```bash
# 安装Python依赖
pip install -r requirements.txt

# 安装Node.js依赖
npm install
```

#### 第五步: 配置环境变量
```bash
# 编辑.env文件，填入API密钥等信息
vim .env
```

#### 第六步: 启动服务
```bash
# 启动OpenClaw服务
openclaw start

# 验证服务状态
openclaw status
```

### 3. 初始化配置

#### 配置Git自动备份
```bash
# 设置Git用户信息
git config --global user.name "OpenClaw Backup"
git config --global user.email "openclaw@example.com"

# 测试Git推送
git push origin main
```

#### 配置定时任务
```bash
# 编辑crontab
crontab -e

# 添加以下内容（每日凌晨3点自动备份）
0 3 * * * /root/.openclaw/workspace/steward/skills/lab-backup-manager/backup.sh >> /var/log/openclaw_backup.log 2>&1
```

### 4. 验证部署
```bash
# 查看Agent列表
openclaw agents list

# 查看系统状态
openclaw status
```

## 🔧 常用操作

### 备份操作
```bash
# 手动执行备份
bash /root/.openclaw/workspace/steward/skills/lab-backup-manager/backup.sh

# 查看备份历史
cd /root/.openclaw
git log --oneline -20
```

### 技能管理
```bash
# 列出所有可用技能
openclaw skills list

# 查看技能详情
openclaw skills show <skill-name>
```

### Agent管理
```bash
# 查看Agent状态
openclaw agents status <agent-name>

# 重启Agent
openclaw agents restart <agent-name>
```

## 🔒 安全注意事项

1. **敏感信息保护**
   - 所有API密钥、密码存储在`.env`文件中，该文件不会被提交到Git
   - 禁止在代码和文档中硬编码敏感信息
   - 教研室仓库的日志和学生信息采用AES-256加密存储

2. **访问控制**
   - 实验室仓库仅对科研团队成员开放
   - 教研室仓库仅对教学团队成员开放
   - 不同Agent有不同的权限范围，禁止越权操作

3. **数据备份**
   - 每日自动备份到GitHub和私有备份服务器
   - 重要数据采用多副本存储，确保数据安全
   - 定期测试恢复流程，确保备份可用

## 📝 更新历史

### 版本 2.1 (2026-04-13)
- 重构日志系统，移除公共记录工作日志脚本
- 迁移知识管理工具，整合文献检索和知识库功能
- 完善技能锁定机制，新增.skills_store_lock.json
- 更新所有Agent的TOOLS.md配置
- 新增实验室和教研室独立日志系统

### 版本 2.0 (2026-04-07)
- 重构备份策略，基于.openclaw根目录同步
- 完善Agent分工和权限体系
- 新增多仓库管理机制（实验室+教研室）

### 版本 1.0 (2026-04-06)
- 初始版本，多Agent系统上线

## 📄 许可证

本项目遵循 MIT 许可证，详见 LICENSE 文件。

## 👨‍💻 维护者

- **杨权** - 系统架构、实验室负责人
- **大管家Agent** - 自动维护、系统监控

---

**最后更新**: 2026-04-13 19:37:00  
**系统版本**: v2.1.1  
**运行状态**: ✅ 正常运行  
**备份状态**: ✅ 自动执行中
