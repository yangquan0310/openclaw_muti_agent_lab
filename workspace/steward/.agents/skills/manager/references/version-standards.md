# 版本管理指南

> 管理项目文件模板版本与技能模板版本的对齐

---

## 一、版本类型的本质

版本管理解决的是：**技能模板更新后，如何让所有项目文件同步更新？**

有三个不同维度的版本：

| 类型 | 存储位置 | 含义 |
|------|----------|------|
| **技能模板版本** | `skills/*/AGENTS.md` frontmatter `version` | 模板格式规范版本，定义项目文件应达到的标准 |
| **项目文件模板版本** | `项目/AGENTS.md` frontmatter `version` | 判断该项目文件是否与技能模板对齐 |
| **项目版本** | `项目/metadata.json` `version` | 项目自身内容进度，与模板版本无关 |

---

## 二、版本对比规则

| 条件 | 动作 |
|------|------|
| 项目文件 version < 技能模板 version | 需要更新 |
| 项目文件 version ≥ 技能模板 version | 已对齐，跳过 |
| 项目文件无 version | 需要添加 |

---

## 三、更新触发条件

当技能模板内容变更导致版本号变化时：

```
技能模板版本变化（如 v2.0.0 → v3.0.0）
    ↓
扫描所有项目文件（AGENTS.md, README.md, TODO.md）
    ↓
对比项目文件 version vs 技能模板 version
    ↓
version < 技能模板 version → 更新文件格式到新模板
version ≥ 技能模板 version → 跳过
```

---

## 四、项目文件结构

```
项目根目录/
├── AGENTS.md              # 模板版本（frontmatter version）
├── README.md             # 模板版本（frontmatter version）
├── TODO.md              # 模板版本（frontmatter version）
├── metadata.json        # 项目版本（独立维护）
├── uploads/
├── manuscripts/
└── .agents/
```

---

## 五、frontmatter 格式

项目文件必须包含 frontmatter：

```yaml
---
name: 项目名
version: 2.0.0  # 模板版本，与技能模板对齐
author: Yang Quan
---
```

---

## 六、版本历史

| 日期 | 版本 | 说明 |
|------|------|------|
| 2026-05-18 | v2.0.0 | 初始版本 |

*最后更新：2026-05-22*
