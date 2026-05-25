# 如何建立 CLI

> 如何为技能建立命令行入口。

---

## 问题

### 为什么要给技能建 CLI？

CLI 让技能可以从终端直接调用，而不仅依赖 OpenClaw 的自然语言触发。当技能需要：
- 被 cron 定时调用
- 在脚本中被引用
- 被其他技能调用

就需要 CLI。

### 什么情况下不需要 CLI？

如果技能仅通过 OpenClaw 的自然语言触发（如"查看天气"），不需要 CLI。

### CLI 和 MCP 工具的区别？

| | CLI | MCP 工具 |
|---|---|---|
| **调用方式** | 终端命令 | OpenClaw 自然语言 |
| **入口** | `/usr/local/bin/{skill}` | `mcp/server.py` |
| **用途** | 脚本/cron/其他技能调用 | 用户对话触发 |
| **关系** | 独立建立，可与 MCP 共存 | 可独立存在 |

---

## 方法论

### 格式哲学：可预期 > 简洁

CLI 的核心价值不是最短命令，而是**结构可预期**：

```
{技能名} {模块} [{子模块}] [{方法}] [{参数}]
```

用户记住一个命令的结构，就能推断出其他命令的结构。

### 判断：单模块还是多模块？

| 判断条件 | 类型 | 分发方式 |
|----------|------|----------|
| 业务功能 ≥ 2 个独立模块 | 多模块 | 必须写 `main.py` 做子命令分发 |
| 业务功能只有 1 个 | 单模块 | wrapper 直接指向唯一脚本 |

---

## 工作流

### 流程概览

```
① 明确CLI结构 → ② 写模块 → ③ 写分发层 → ④ 暴露CLI → ⑤ SKILL.md声明
```

---

### 步骤 1：明确 CLI 结构

在动手前，先确定命令结构：

```
{技能名} {模块} [{子模块}] [{方法}] [{参数}]
```

**示例**：skill-developer 的结构
```
skill-developer init <name> <description> [path] [emoji]
skill-developer check <path>
```

### 步骤 2：写各模块（`scripts/{module}.py`）

每个模块一个文件，每个文件必须同时包含：

```python
#!/usr/bin/env python3
"""{模块描述}"""

class {模块名}:
    """业务逻辑封装"""
    def __init__(self):
        pass
    def do_something(self, param: str) -> dict:
        return {"success": True}

def main() -> int:
    """命令行入口"""
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
```

**规则**：
- 文件名 = 类名（单数名词）
- 函数名用动词（`search()`、`calculate()`）
- 禁止名词函数名（`searcher()`、`calculator()`）

### 步骤 3：写分发层

**多模块** → 必须写 `scripts/main.py`：

```python
#!/usr/bin/env python3
"""CLI 统一入口"""
import sys
from pathlib import Path

_SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SKILL_ROOT))

from scripts.bazi import main as bazi_main

def main() -> int:
    if len(sys.argv) < 2:
        print_help()
        return 0

    subcmd = sys.argv[1]
    del sys.argv[1]          # 关键：删掉子命令本身

    if subcmd == 'bazi':
        sys.argv[0] = '<skill> bazi'
        return bazi_main()

    print(f"Error: 未知子命令 '{subcmd}'")
    return 1

if __name__ == '__main__':
    raise SystemExit(main())
```

**关键规则**：`del sys.argv[1]` 必须执行，否则子模块的 argparse 会把子命令当位置参数。

**单模块** → `main.py` 做透传：

```python
#!/usr/bin/env python3
"""CLI 统一入口"""
import sys
from pathlib import Path

_SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SKILL_ROOT))

from scripts.唯一模块 import main as 模块_main

def main() -> int:
    return 模块_main()

if __name__ == '__main__':
    raise SystemExit(main())
```

### 步骤 4：暴露 CLI

**手动 wrapper**：
```bash
#!/bin/bash
exec python3 /path/to/skills/{skill}/scripts/main.py "$@"
```

**安装 wrapper**：
```bash
chmod +x /usr/local/bin/{skill}
```

**验证**：
```bash
{skill} --help
```

### 步骤 5：SKILL.md 声明

```markdown
## 快速调用

```bash
# 功能说明
{技能名} {模块} [参数...]

# 功能说明
{技能名} {模块} {子模块} [参数...]
```
```

---

## 执行标准

### 格式规范

| 规范项 | 要求 |
|--------|------|
| 命令数 | 一个技能不超过 **7 个**顶层命令 |
| 层次深度 | `{技能} {模块} {子模块}` 最多 **3 层** |
| 选项数 | 单个命令选项不超过 **5 个** |
| 布尔标志 | 优先 `--flag` 而非 `--flag true/false` |
| 选项名 | 全小写，禁止缩写歧义（如 `-t` 既是 `--type` 又是 `--title`） |

### 命名规范

```bash
# ❌ 大写技能名
FortuneTelling bazi 1990 5 15

# ❌ 驼峰/中划线子命令
fortunetelling calculateMatrix
fortunetelling lunar-convert

# ❌ 大写选项
fortunetelling bazi 1990 5 15 --Gender 男

# ✅ 全小写
fortunetelling bazi 1990 5 15 --gender 男
```

### 结构规范

```python
# ❌ 禁止：裸 argparse 在模块顶层
parser = argparse.ArgumentParser()
args = parser.parse_args()

# ✅ 正确：argparse 在 main() 函数内
def main() -> int:
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    return 0
```

### 分发规范

```python
# ❌ 禁止：缺少 del sys.argv[1]
subcmd = sys.argv[1]
# ... 但没有 del

# ✅ 正确：
subcmd = sys.argv[1]
del sys.argv[1]
```

---

*详见 [ch04_how-to-write-scripts.md](ch04_how-to-write-scripts.md)*
