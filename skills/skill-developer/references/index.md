# skill-developer 参考手册

> 技能开发的完整参考指南。

---

## 书籍目录

| 章节 | 文件 | 对应的问题 |
|------|------|------------|
| 01 | [ch01_how-to-develop-new-skill.md](ch01_how-to-develop-new-skill.md) | 如何开发新技能？ |
| 02 | [ch02_how-to-check-quality.md](ch02_how-to-check-quality.md) | 如何检查技能质量？ |
| 03 | [ch03_how-to-build-cli.md](ch03_how-to-build-cli.md) | 如何建立命令行入口？ |
| 04 | [ch04_how-to-write-scripts.md](ch04_how-to-write-scripts.md) | 如何编写 scripts？ |
| 05 | [ch05_how-to-apply-naming-conventions.md](ch05_how-to-apply-naming-conventions.md) | 如何应用命名规范？ |
| 06 | [ch06_how-to-update-skill.md](ch06_how-to-update-skill.md) | 如何更新技能？ |
| 07 | [ch07_how-to-write-references-chapter.md](ch07_how-to-write-references-chapter.md) | 如何撰写 references 章节？ |

---

## 按阶段查找

### 开发技能

| 问题 | 章节 |
|------|------|
| 如何开发？ | ch01 |
| 如何检查质量？ | ch02 |
| 如何命名？ | ch05 |
| 如何写 scripts？ | ch04 |
| 如何建立 CLI？ | ch03 |

### 维护技能

| 问题 | 章节 |
|------|------|
| 如何更新？ | ch06 |

### 元技能

| 问题 | 章节 |
|------|------|
| references 怎么写？ | ch07 |

---

## 章节结构

每章统一包含四个层次：

| 层次 | 回答的问题 |
|------|------------|
| **问题** | 为什么要知道这个？ |
| **方法论** | 怎么思考这个问题？ |
| **工作流** | 具体怎么执行？ |
| **执行标准** | 做到什么程度算合格？ |

---

## 快速命令

```bash
# 初始化新技能
skill-developer init <name> <description> [path] [emoji]

# 自检技能
python3 scripts/selfcheck.py /path/to/skill
```
