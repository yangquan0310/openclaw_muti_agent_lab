---
pageType: source
id: source.repository
createdAt: "2026-05-08T12:00:00+08:00"
updatedAt: "2026-05-12T10:17:00+08:00"
sourceIds:
  - source.system-config
aliases:
  - 仓库
---

# 仓库

> 实验室统一项目仓库。
> 来源：`/data/disk/OneDrive/Applications/openclaw repository/`

---

## 路径

```
/data/disk/OneDrive/Applications/openclaw repository/
```

## 结构

```
/data/disk/OneDrive/Applications/openclaw repository/
├── README.md              # 仓库总览（项目索引）
│
├── 项目A/                 # 每个项目一个文件夹
│   ├── README.md          # 项目总览
│   ├── metadata.json      # 项目元数据
│   ├── SKILL.md           # 项目级操作手册
│   ├── TODO.md            # 进度看板
│   └── ...                # 项目具体内容
│
├── 项目B/
│   └── ...
│
└── ...
```

## 核心文件

| 文件 | 说明 |
|------|------|
| `README.md` | 仓库总览，含项目索引表 |
| `项目/README.md` | 项目定位、目录结构、关键文件索引 |
| `项目/metadata.json` | 机器可读的项目元数据 |
| `项目/SKILL.md` | 项目级操作手册 |
| `项目/TODO.md` | 进度看板 |

## 管理技能

| 项目类型 | 管理技能 |
|----------|----------|
| 论文项目 | thesis-manager |
| 课程项目 | course-manager |
| 程序项目 | program-manager |

---

## 相关

-  — 仓库概念
-  — 项目规范

---

*最后更新：2026-05-12*

## Related
<!-- openclaw:wiki:related:start -->
### Referenced By

- [[syntheses/2026-05-19-18-25-37-如何配置仓库|仓库]]
- [[syntheses/2026-06-01-16-12-00-我的agent工程实践-harness与plugin双轮|我的 agent 工程实践：驾驭方法论]]
- [[syntheses/2026-05-19-22-53-22-如何管理项目|项目]]
<!-- openclaw:wiki:related:end -->
