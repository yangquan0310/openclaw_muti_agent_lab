# CLI 规范

> 所有技能必须提供命令行入口，格式统一，结构可预期。

---

## 一、格式规范

### 标准格式

```
{技能名} {模块} [子模块] [方法] [参数...]
```

| 组成部分 | 要求 | 说明 |
|----------|------|------|
| **技能名** | 必须与 `project.name` 完全一致，**全小写** | 大写/驼峰违反 Shell 命令规范 |
| **模块** | 顶层功能分组，**全小写**，一个技能 1-5 个模块 | 按功能自然划分，非堆砌 |
| **子模块** | 可选，模块内再细分，**全小写** | 层次过深（>2层）说明模块划分有问题 |
| **方法** | 可选，具体操作，**全小写** | 无方法时模块即操作 |
| **参数** | 位置参数在前，选项参数在后，`--` 引导 | 选项名**全小写** |

### 命名禁令

```bash
# ❌ 大写技能名
FortuneTelling bazi 1990 5 15

# ❌ 驼峰/中划线子命令
fortunetelling calculateMatrix
fortunetelling lunar-convert

# ❌ 大写选项
fortunetelling bazi 1990 5 15 --Gender 男
```

### 选项设计原则

- 布尔标志用 `--flag`（无值），状态用 `--key value`
- 选项名尽量**短**（1-2词），全小写
- **禁止**缩写歧义选项（如 `-t` 既 `--type` 又 `--title`）

---

## 二、实现方式

所有技能统一使用 **Shell Wrapper** 方式，wrapper 在 `/usr/local/bin/{技能名}`：

```
/usr/local/bin/{技能名}  →  scripts/main.py  →  各模块
```

### wrapper 写法

```bash
#!/bin/bash
exec python3 /path/to/skills/{skill}/scripts/main.py "$@"
```

### main.py 路由格式

```python
def main() -> int:
    subcmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    del sys.argv[1]

    if subcmd == "模块A":
        return 模块A_main()
    elif subcmd == "模块B":
        return 模块B_main()
    else:
        print_help()
        return 1
```

---

## 三、SKILL.md 声明规范

每个技能的 SKILL.md 必须包含 `## 快速调用` 章节，格式：

```markdown
## 快速调用

```bash
# 功能说明
{技能名} {模块} [参数...]

# 功能说明
{技能名} {模块} {子模块} [参数...]
```
```

**原则**：
- 必选参数用具体值示例，可选参数用 `[...]` 包裹
- 每个命令前应有简短说明
- 只写**常用命令**，不堆砌所有变体

---

## 四、CLI 表格式（规范说明，非命令堆砌）

| 规范项 | 要求 |
|--------|------|
| 命令数 | 一个技能不超过 **7 个**顶层命令（含子模块命令） |
| 层次深度 | `{技能} {模块} {子模块}` 最多 **3 层**，超过说明设计有问题 |
| 选项数 | 单个命令选项不超过 **5 个**，超过说明命令职责不清 |
| 布尔标志 | 优先使用 `--flag` 而非 `--flag true/false` |

---

---

## 六、lookup 命令

`lookup` 是 OpenClaw 内置工具，不在 `scripts/` 中实现。

SKILL.md 中的 lookup 索引写法：
```bash
# 构建索引
lookup index -r <references_path> -m <manifest_path> -c <chunks_path>

# 搜索
lookup search -i <manifest_path> <关键词>

# 列出
lookup list -i <manifest_path>
```

---

*详见 [scripts-standards.md](scripts-standards.md)*
