# 如何应用命名规范

> 如何为技能及其内部元素命名。

---

## 问题

### 为什么要专门讲命名？

命名不是随意取的。好的命名让代理看到文件名就知道：
1. 这个文件是关于什么的
2. 应该用什么类型的内容来填充
3. 和其他文件有什么区别

### references 文章命名的问题

每个 references 文章都解决一个实际问题。文件名应该是**动宾短语**，格式为 `how-to-do-something`：

```
how-to-initialize-new-skill     ✅
how-to-develop-new-skill       ✅
how-to-check-quality           ✅
how-to-build-cli              ✅

quality-checklist              ❌ 名词短语，不是动宾
development-workflow          ❌ 工作流后缀，不符合新框架
```

### 命名格式：ch{num}_{title}.md

```
ch{章节号}_{how-to-做什么}.md
```

- **ch{num}**：章节号，从 01 开始顺序编号
- **how-to-{做什么}**：动宾短语，用横线分隔
- **全部小写**

**示例**：
| 文件名 | 含义 |
|--------|------|
| `ch01_how-to-develop-new-skill.md` | 如何开发新技能 |
| `ch02_how-to-check-quality.md` | 如何检查质量 |
| `ch03_how-to-build-cli.md` | 如何建立 CLI |
| `ch06_how-to-update-skill.md` | 如何更新技能 |

### 标题要求

**标题必须是动宾短语**：`how-to-{动词}-{宾语}`

| 正确 | 错误 |
|------|------|
| `how-to-initialize-new-skill` | `initialization` |
| `how-to-check-quality` | `quality-checklist` |
| `how-to-build-cli` | `cli-development` |
| `how-to-write-scripts` | `scripts-guide` |

---

## 方法论

### 命名的三层价值

| 层次 | 价值 | 示例 |
|------|------|------|
| **可预期** | 用户能从命名推断出内容类型 | `naming-standards.md` 一定是检查清单 |
| **可搜索** | 代理能用关键词快速定位 | 搜索"cli"能找到 `ch03_how-to-build-cli.md` |
| **可维护** | 新增文件时不会与现有冲突 | 不会新建一个 `cli-guide.md` 再加 `cli-standards.md` |

### 命名的核心原则

1. **动宾短语优先** — 文件名 = how-to + 动词 + 宾语
2. **章节编号连续** — ch01, ch02, ch03... 不跳号
3. **固定名称优先** — `index.md`、`SKILL.md` 不适用此规则

---

## 工作流

### references 文章命名

新建一个 references 文章时：

```
① 确定文章要解决的实际问题
     ↓
② 写成一个动宾短语：how-to-{动词}-{宾语}
     ↓
③ 分配章节号（按顺序，不跳号）
     ↓
④ 检查是否与现有重复
```

**检查清单**：
- [ ] 标题是动宾短语（how-to-开头）？
- [ ] 章节号连续？
- [ ] 文件名不与现有重复？

### 技能内部命名

| 对象 | 命名规则 | 示例 |
|------|----------|------|
| **技能根目录** | 小写、单词间横线分隔 | `my-skill`, `skill-developer` |
| **子目录** | 小写、单词间横线分隔 | `assets/templates`, `scripts` |
| **SKILL.md** | 固定大写 | `SKILL.md` |
| **README.md** | 固定大写 | `README.md` |
| **_meta.json** | 下划线开头 | `_meta.json` |
| **模板文件** | `{原名}.template` | `SKILL.md.template` |
| **私有文件** | `_` 前缀 | `_internal.md` |
| **模块文件** | PascalCase 或 snake_case | `Searcher.py`, `utils.py` |

---

## 执行标准

### references 文章命名规范

**格式**：`ch{章节号}_{how-to-做什么}.md`

| 规则 | 要求 |
|------|------|
| 章节号 | 两位数字，从 01 开始 |
| 分隔符 | 下划线 `_` 连接章节号和标题 |
| 标题 | 动宾短语，how-to- 开头，全小写 |
| 单词分隔 | 横线 `-` |

**示例**：
```
ch01_how-to-develop-new-skill.md
ch02_how-to-check-quality.md
ch03_how-to-build-cli.md
```

**固定文件名**（不适用上述规则）：
- `index.md` — 书籍索引
- `SKILL.md` — 技能定义（根目录）

### 代码命名规范

| 对象 | 命名规则 | 示例 |
|------|----------|------|
| **类名** | PascalCase，单数名词 | `Searcher`, `Maintainer` |
| **方法名** | snake_case，**动词/动宾** | `search()`, `archive_file()` |
| **私有方法** | `_` 前缀 | `_validate()`, `_build_path()` |
| **常量** | UPPER_SNAKE_CASE | `MAX_RETRIES`, `DEFAULT_PATH` |
| **私有常量** | `_` 前缀 | `_CACHE_DIR` |

**方法名动词清单**：
```
search, find, get, fetch, calculate, compute,
validate, check, verify, build, create, generate,
update, patch, delete, remove, archive, export
```

**禁止使用**：
```
searcher, finder, calculator, validator  # 名词
```

### MCP 工具命名

| 对象 | 命名规则 | 示例 |
|------|----------|------|
| **工具名** | `{skill}_{action}` | `skill_dev_create` |
| **参数名** | snake_case | `skill_name`, `with_mcp` |

---

## 检查清单

### 新建 references 文章时

- [ ] 标题是动宾短语（how-to-开头）
- [ ] 章节号连续
- [ ] 文件名不与现有重复

### 代码命名检查

- [ ] 类名是 PascalCase 单数名词
- [ ] 方法名是 snake_case 动词/动宾
- [ ] 常量是 UPPER_SNAKE_CASE
- [ ] 文件名与类名一致（模块文件）
