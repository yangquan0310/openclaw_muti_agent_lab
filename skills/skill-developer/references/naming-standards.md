# 命名规范

> references 中的文件名和目录命名标准

---

## references 文章命名

| 类型 | 命名规则 | 示例 |
|------|----------|------|
| **方法论** | `*-guide` | `guide-writing-guide.md` |
| **标准** | `*-standards` | `coding-standards.md` |
| **工作流** | `*-workflow` | `development-workflow.md` |

**固定文件名**（不适用上述规则）：
- `index.md` — 书籍索引
- `guide.md` — 使用指南

---

## 目录命名

| 目录 | 命名规则 | 示例 |
|------|----------|------|
| **技能根目录** | 小写、单词间横线分隔 | `my-skill`, `skill-developer` |
| **子目录** | 小写、单词间横线分隔 | `assets/templates`, `scripts` |
| **脚本目录** | 小写、单词间横线分隔 | `selfcheck.py`, `init.py` |

---

## 文件命名

| 文件类型 | 命名规则 | 示例 |
|----------|----------|------|
| **SKILL.md** | 固定大写 | `SKILL.md` |
| **README.md** | 固定大写 | `README.md` |
| **_meta.json** | 下划线开头 | `_meta.json` |
| **模板文件** | `{原名}.template` | `SKILL.md.template` |
| **私有文件** | `_` 前缀 | `_internal.md` |

---

## 代码命名

| 对象 | 命名规则 | 示例 |
|------|----------|------|
| **类名** | PascalCase，单数名词 | `Searcher`, `Maintainer` |
| **方法名** | snake_case，动词/动宾 | `search()`, `archive_file()` |
| **文件名** | 与类名一致，或描述性小写 | `Searcher.py`, `utils.py` |
| **私有方法** | `_` 前缀 | `_validate()`, `_build_path()` |
| **常量** | UPPER_SNAKE_CASE | `MAX_RETRIES`, `DEFAULT_PATH` |

---

## MCP 工具命名

| 对象 | 命名规则 | 示例 |
|------|----------|------|
| **工具名** | `{skill}_{action}` | `skill_dev_create`, `thesis_search` |
| **参数名** | snake_case | `skill_name`, `with_mcp` |

---

*详见 [索引](index.md)*
