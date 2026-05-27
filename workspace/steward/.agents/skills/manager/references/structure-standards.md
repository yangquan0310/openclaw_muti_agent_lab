# Wiki 结构规范

> 知识库目录结构及内容规范

---

## 一、目录结构

```
~/.openclaw/wiki/
├── concepts/     → 规范、标准、流程（AI 决策参考）
├── entities/     → 人物、系统、项目（AI 路由参考）
├── syntheses/    → 跨项目总结、经验提炼
├── sources/      → 工具/平台级文档（conda、openclaw-env等）
├── reports/      → 生成的仪表盘（按需）
├── _attachments/ → 附件
└── index.md      → 知识库首页
```

---

## 二、目录职责

| 目录 | 内容类型 | 示例 |
|------|----------|------|
| **concepts** | 概念/规范/流程 | project.md、thesis-project.md |
| **entities** | 人物/系统/项目实体 | steward.md、openclaw-gateway.md |
| **syntheses** | 跨项目综合总结 | 多agent协作案例 |
| **sources** | 工具/平台来源文档 | conda.md、openclaw-env.md |
| **reports** | 自动生成的仪表盘 | open-questions.md |
| **_attachments** | 附件（图片/文件） | — |

---

## 三、各目录内容规范

### concepts/

存放抽象概念、业务规范、工作流程。

| 类型 | 示例 | 标记 |
|------|------|------|
| 规范 | 项目规范、版本管理规范 | pageType: concept |
| 流程 | 任务推进流程、协作协议 | pageType: concept |
| 标准 | 命名规范、目录规范 | pageType: concept |

### entities/

存放具体实体（人/系统/项目）。

| 类型 | 示例 | 标记 |
|------|------|------|
| 人物 | steward、psychologist | entityType: person |
| 系统 | openclaw-gateway | entityType: system |
| 项目 | 具体项目名称 | entityType: project |

### syntheses/

存放跨项目总结、经验提炼。

| 类型 | 示例 |
|------|------|
| 协作案例 | 多agent协作案例 |
| 经验总结 | 项目管理经验 |

### sources/

存放工具/平台来源文档。

| 类型 | 示例 |
|------|------|
| 工具文档 | conda、git、python |
| 平台文档 | openclaw-env、openclaw-system |

**禁止**：项目级文件（应在仓库，不在 wiki）

---

## 四、命名规范

| 规范 | 示例 |
|------|------|
| 使用中文 | 项目管理.md |
| 避免特殊字符 | 不用 ? * / \ |
| 统一小写扩展名 | .md |

---

## 五、版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0.0 | 2026-05-19 | 初始版本 |

*最后更新：2026-05-22*
