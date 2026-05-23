# 如何撰写标准

> 本章讲述如何撰写 references 中的标准类文章（`*-standards.md`）。

---

## 标准的定位

标准回答：**交付物要满足什么条件？**

不是教程，不是解释原理，而是**检查清单**。

---

## 写作要点

### 1. 检查项原子化

每个检查项只检查**一个条件**。

```
❌ 不好：
| 文件存在且非空 | 文件存在 且 行数>0 |

✅ 好：
| 文件存在 | 文件存在 |
| 文件非空 | 行数 > 0 |
```

### 2. 给出通过标准

每个检查项都要有明确的"怎样算通过"。

```
❌ 不好：
| SKILL.md 存在 | 要存在 |

✅ 好：
| SKILL.md 存在 | 文件存在 |
| YAML 格式正确 | JSON 有效 |
```

### 3. 不解释原因

标准就是标准，不需要解释"为什么"。

```
❌ 不好：
| 文件名小写 | 因为 Unix 系统对大小写敏感，所以要小写 |

✅ 好：
| 文件名小写 | 全部小写 |
```

### 4. 使用表格呈现

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 1 | 文件存在 | 文件存在 |
| 2 | 命名规范 | 全部小写、单词间横线分隔 |

---

## 文件命名规范

### references 文章命名

| 类型 | 命名规则 | 示例 |
|------|----------|------|
| **方法论** | `*-guide` | `guide-writing-guide.md` |
| **标准** | `*-standards` | `coding-standards.md` |
| **工作流** | `*-workflow` | `development-workflow.md` |

### 目录命名

| 目录 | 命名规则 | 示例 |
|------|----------|------|
| **技能根目录** | 小写、单词间横线分隔 | `my-skill` |
| **子目录** | 小写、单词间横线分隔 | `assets/templates`, `scripts` |

### 文件命名

| 文件类型 | 命名规则 | 示例 |
|----------|----------|------|
| **SKILL.md** | 固定大写 | `SKILL.md` |
| **README.md** | 固定大写 | `README.md` |
| **_meta.json** | 下划线开头 | `_meta.json` |
| **模板文件** | `{原名}.template` | `SKILL.md.template` |

---

## 代码命名规范

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

## 质量检查清单示例

### 必选结构检查

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 1 | SKILL.md 存在 | 文件存在 |
| 2 | README.md 存在 | 文件存在 |
| 3 | _meta.json 存在 | 文件存在 |
| 4 | scripts/ 目录存在 | 目录存在 |
| 5 | references/ 目录存在 | 目录存在 |
| 6 | references/index.md 存在 | 文件存在 |
| 7 | references/guide.md 存在 | 文件存在 |

### 文档检查

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 8 | SKILL.md 有 YAML frontmatter | name/description/version |
| 9 | SKILL.md 正文不超过 200 行 | 行数合理 |
| 10 | 触发条件已填写 | 非空、有意义 |
| 11 | 指南回答实际问题 | 不是占位符或空洞复述 |

### 代码检查

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 12 | 方法名有具体含义 | 非 `main`/`do_something` |
| 13 | 无 API Key 明文 | 通过 env 或参数传入 |
| 14 | Python 脚本可独立运行 | `if __name__ == "__main__"` |

### MCP 检查

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 15 | mcp/server.py 存在 | 文件存在 |
| 16 | mcp/server.py 可运行 | `python3 mcp/server.py` 不报错 |
| 17 | EXPOSED_TOOLS 结构正确 | JSON 格式、必填字段存在 |

---

## 自检命令

```bash
python3 scripts/selfcheck.py /path/to/skill
```

---

## 本章小结

1. **原子化**：每个检查项只检查一个条件
2. **通过标准明确**：怎样算通过要写清楚
3. **不解释原因**：标准就是标准
4. **表格呈现**：清晰易查

---

*详见 [索引](index.md)*