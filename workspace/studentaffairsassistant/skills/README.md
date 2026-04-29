# Skills 文件夹

> 学工助手（studentaffairsassistant）个人技能存储目录
> 遵循 Skill-developer 规范，每个技能包含代码实现、AI 规范文档和人类说明文档

---

## 功能说明

本文件夹用于存储学工助手的**个人技能**，每个技能是一个独立的程序模块或文档规范，可被主代理直接调用或委派给子代理执行。

技能分为两类：
- **结构化技能**：包含可执行代码（Python/Shell），可直接运行
- **非结构化技能**：纯 Markdown 描述的操作流程，作为 SOP 指导执行

所有技能均遵循 `Skill-developer` 规范进行创建和维护，支持面向对象的代码框架和统一的文档格式。

---

## 文件夹结构

```
skills/
├── {技能名}/                   # 技能目录（英文小写，横线分隔）
│   ├── SKILL.md                # AI 可读的技能规范（YAML front matter + Markdown）
│   ├── README.md               # 给人类看的技能说明
│   ├── _meta.json              # 技能元数据（名称、版本、触发词、依赖）
│   └── {功能模块}/              # 功能模块目录（英文小写，横线分隔）
│       ├── SKILL.md            # AI 可读的技能规范（YAML front matter + Markdown）
│       └── *.py / *.sh         # 核心代码实现（面向对象框架）
│
└── README.md                   # 本文件 - 技能目录总览
```

### 规范要求

| 文件 | 必需 | 说明 |
|------|------|------|
| `SKILL.md` | ✅ | AI 执行规范，必须包含 YAML front matter（name, description, version） |
| `README.md` | ✅ | 人类可读说明，包含功能、用法、示例 |
| `_meta.json` | ✅ | 机器可读元数据（triggers, dependencies, environment） |
| 代码文件 | 视类型 | 结构化技能必须有 `.py` 或 `.sh` |

---

## 技能索引

| 技能名称 | 触发示例 | 描述 | 路径 |
|---------|---------|------|------|
| student-record-management | 学生档案、创建学生、学生信息 | 学生档案管理技能 - 创建、分类、存储、检索学生档案 | skills/student-record-management/ |
| academic-counseling | 学业辅导、学习问题、辅导记录 | 学业辅导记录技能 - 记录学业问题、制定辅导计划、跟踪辅导效果 | skills/academic-counseling/ |
| club-activity-management | 社团活动、社团管理、活动记录 | 社团活动管理技能 - 记录社团活动计划、管理社团成员、生成活动总结 | skills/club-activity-management/ |

---

## 使用方式

1. **查看技能文档**：阅读对应技能文件夹中的 `SKILL.md`（AI 规范）或 `README.md`（人类说明）
2. **执行技能**：运行 `.sh` 脚本或调用 `.py` 模块
3. **了解元数据**：阅读 `_meta.json` 获取触发词、依赖和环境变量

---

*维护者：学工助手（studentaffairsassistant）*
*最后更新：2026-04-30*
