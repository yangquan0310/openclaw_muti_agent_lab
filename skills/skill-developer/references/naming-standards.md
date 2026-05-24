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

## 命令行（CLI）命名

> 所有技能的 CLI 命令统一格式。

### 格式规范

```
{技能名} {方法名} {参数}
```

| 组成部分 | 命名规则 | 示例 |
|----------|----------|------|
| **技能名** | 与 `pyproject.toml` 中 `[project.name]` 一致，全小写、单词间横线 | `research-assistant` |
| **方法名** | 与 CLI subcommand 一致，小写单词 | `search`, `scholar`, `summarize` |
| **参数** | 遵循 GNU 标准风格（`--long-option`，可选值用 `[]`） | `--keyword "深度学习" --limit 10` |

### 完整示例

```bash
# research-assistant 技能
research-assistant search --queries queries.json --kb-path knowledge/index.json
research-assistant cnki --queries queries.json --kb-path knowledge/index.json
research-assistant scholar --keyword "deep learning" --limit 20 --year-min 2020
research-assistant summarize --kb-path knowledge/index.json
research-assistant manage info --kb-path knowledge/index.json

# skill-developer 技能
skill-developer init my-skill "我的新技能" --emoji 📦

# lark 系列技能（飞书官方 CLI）
lark-cli im +messages-send --user-id ou_xxx --text "hello"
```

### 入口方式：shell wrapper（推荐）

由于多个技能可能有同名 `scripts` 包，pip 的 `project.scripts` entry_points 会导致包名冲突。
**推荐在 /usr/local/bin/ 创建 shell wrapper**：

```bash
#!/bin/bash
# /usr/local/bin/{技能名}
exec python3 /root/.openclaw/skills/{skill-name}/scripts/main.py "$@"
```

创建后：

```bash
chmod +x /usr/local/bin/{技能名}
# 之后全局可用
{技能名} --help
{技能名} {子命令} --arg value
```

每次技能更新入口文件 `scripts/main.py` 后无需重新安装，shell wrapper 自动生效。

### scripts/ 目录结构规范

详见 [scripts-standards.md](scripts-standards.md)（模块文件规范、main.py 分发模式、__init__.py 规范）。

### 禁止形式

```bash
# ❌ 禁止：不带技能名前缀
search --keyword "xxx"          # 缺少技能名

# ❌ 禁止：驼峰/大写
ResearchAssistant search ...     # 技能名必须全小写

# ❌ 禁止：非子命令形式
research-assistant --search --keyword "xxx"   # search 应为子命令，非选项
```

---

*详见 [索引](index.md)*
