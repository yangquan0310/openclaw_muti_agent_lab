# CLI 规范

> 所有技能必须提供命令行入口，格式统一为 `{技能名} {模块} {方法} {参数}`。

---

## 格式规范

### 标准格式

```
{技能名} {模块} [子模块] [方法] [参数...]
```

| 组成部分 | 规范 | 示例 |
|----------|------|------|
| **技能名** | 必须与 `project.name` 完全一致，全小写，禁止大写/驼峰 | `fortunetelling` |
| **模块** | 顶层功能分组，全小写 | `bazi`、`calculate`、`maintainer` |
| **子模块** | 可选，模块内的子功能 | `basic`（在 calculate 下） |
| **方法** | 可选，具体操作或算法 | `add`、`inverse` |
| **参数** | 位置参数在前，选项参数在后 | `1990 5 15 10 --gender 男` |

### 错误示例

```bash
# ❌ 技能名大写
FortuneTelling bazi 1990 5 15

# ❌ 子命令大写
fortunetelling Bazi 1990 5 15

# ❌ 驼峰子命令
fortunetelling calculateMatrix

# ❌ 中划线（shell 会报错）
fortunetelling lunar-convert
```

---

## CLI 实现方式

当前有 **3 种实现方式**，优先级顺序：

### 方式 1：Shell Wrapper → main.py（推荐）

通过 `/usr/local/bin/{技能名}` wrapper 调用 `scripts/main.py`，由 main.py 分发到各模块。

```
/usr/local/bin/fortunetelling  →  scripts/main.py  →  bazi / lunar / fate
/usr/local/bin/physicist       →  scripts/main.py  →  calculate / visualize
/usr/local/bin/mathematician   →  scripts/main.py  →  calculate / statistics / visualize
```

wrapper 写法：
```bash
#!/bin/bash
exec python3 /path/to/skills/{skill}/scripts/main.py "$@"
```

### 方式 2：Shell Wrapper → 独立脚本（单模块技能）

wrapper 直接指向单模块脚本（无 main.py 分发）。

```
/usr/local/bin/reviewer  →  scripts/review_checklist.py
/usr/local/bin/writer     →  scripts/selfcheck.py
```

### 方式 3：带子包的 main.py

presenter 的 main.py 在 `scripts/ppt/main.py`，wrapper 指向它。

```
/usr/local/bin/presenter  →  scripts/ppt/main.py  →  list / extend / compile
```

---

## entry_points 声明（TODO）

所有技能应在 `pyproject.toml` 中声明 `entry_points`，实现 `skill-developer init` 后可自动生成：

```toml
[project.scripts]
fortunetelling = "scripts.main:main"
mathematician = "scripts.main:main"
physicist = "scripts.main:main"
reviewer = "scripts.main:review_checklist_main"
writer = "scripts.main:selfcheck_main"
manager = "scripts.main:main"
presenter = "scripts.ppt.main:main"
```

> 当前状态：均未配置 pyproject.toml，依赖 /usr/local/bin/ wrapper 临时解决。

---

## CLI 声明（SKILL.md）

每个技能的 SKILL.md 必须在 `## 命令行（CLI）` 或 `## 快速调用` 章节中声明 CLI，格式如下：

```markdown
## 命令行（CLI）

```bash
# 技能说明
{技能名} {模块} [参数...]
{技能名} {模块} {子模块} [参数...]
```
```

---

## 技能名 模块 方法 参数（参考表）

> 用于快速查阅各技能的 CLI 结构。空格分隔，`<>` 包裹必选参数，`[]` 包裹可选。

### fortunetelling

| 技能名 | 模块 | 方法 | 参数 |
|--------|------|------|------|
| fortunetelling | bazi | — | `<year> <month> <day> <hour> [--gender 男\|女]` |
| fortunetelling | lunar | — | `<year> <month> <day> <hour>` |
| fortunetelling | fate | — | `<year> <month> <day> <hour> [--gender 男\|女] [--type timing]` |

```bash
fortunetelling bazi 1990 5 15 10 --gender 男
fortunetelling lunar 1990 4 15 10
fortunetelling fate 1990 5 15 10 --gender 男 --type timing
```

### mathematician

| 技能名 | 模块 | 子模块 | 方法 | 参数 |
|--------|------|--------|------|------|
| mathematician | calculate | basic | — | `<a> <b> <add\|sub\|mul\|div\|pow\|mod>` |
| mathematician | calculate | matrix | — | `--A <json> [--B <json>] --op <transpose\|inverse\|det\|eigen\|multiply\|add\|subtract>` |
| mathematician | calculate | integrate | — | `--func <expr> --a <float> --b <float> [--method quad\|simpson\|trapezoid]` |
| mathematician | calculate | ode | — | `--func <expr> --y0 <json> --t0 <float> --t1 <float> [--method RK45]` |
| mathematician | calculate | root | — | `--func <expr> --x0 <json> [--method bisection\|newton\|brentq\|fsolve]` |
| mathematician | calculate | interp | — | `--x <floats> --y <floats> --xe <floats> [--method linear\|cubic]` |
| mathematician | statistics | describe | — | `--data <floats>` |
| mathematician | visualize | function | — | `--func <expr> --xmin <float> --xmax <float>` |

```bash
mathematician calculate basic 1 2 add
mathematician calculate matrix --A '[[1,2],[3,4]]' --op inverse
mathematician calculate integrate --func 'x**2' --a 0 --b 1
mathematician statistics describe --data 1,2,3,4,5
mathematician visualize function --func 'x**2' --xmin -10 --xmax 10
```

### physicist

| 技能名 | 模块 | 子模块 | 方法 | 参数 |
|--------|------|--------|------|------|
| physicist | calculate | basic | — | `<a> <b> <add\|sub\|mul\|div\|pow>` |
| physicist | calculate | matrix | — | `--A <json> --op <det\|inv\|eig\|trace\|norm>` |
| physicist | calculate | integrate | — | `--func <expr> --a <float> --b <float> [--method quad\|trapz]` |
| physicist | calculate | ode | — | `--func <expr> --y0 <json> --t0 <float> --t1 <float> [--method RK45]` |
| physicist | visualize | function | — | `--func <expr> --x0 <float> --x1 <expr> [--title <str>]` |
| physicist | visualize | phase | — | `--func <expr> --y0 <json> --t0 <float> --t1 <float>` |
| physicist | visualize | field | — | `--potential <expr> --x-range <json> --y-range <json>` |
| physicist | visualize | surface | — | `--func <expr> --x-range <json> --y-range <json>` |

```bash
physicist calculate basic 10 5 add
physicist calculate matrix --A '[[1,2],[3,4]]' --op det
physicist calculate integrate --func 'x**2' --a 0 --b 1
physicist visualize function --func 'np.sin(x)' --x0 0 --x1 '2*np.pi'
physicist visualize phase --func '[y[1],-y[0]]' --y0 '[[0,1],[0,2]]' --t0 0 --t1 20
physicist visualize field --potential '1/np.sqrt(x**2+y**2)' --x-range '[-3,3]' --y-range '[-3,3]'
```

### reviewer

| 技能名 | 模块 | 方法 | 参数 |
|--------|------|------|------|
| reviewer | review | — | `--type <thesis\|journal\|opensource\|course\|proposal> [--output <path>] [paper]` |

```bash
reviewer review --type thesis paper.pdf
reviewer review -t journal paper.pdf --output review.md
```

### writer

| 技能名 | 模块 | 方法 | 参数 |
|--------|------|------|------|
| writer | selfcheck | — | `--file <path> [--level <sentence\|paragraph\|chapter\|all>]` |

```bash
writer selfcheck --file essay.md
writer selfcheck --file essay.md --level sentence
```

### manager

| 技能名 | 模块 | 子模块 | 方法 | 参数 |
|--------|------|--------|------|------|
| manager | init | — | — | `<path> --type thesis\|course\|program` |
| manager | organize | — | — | `[<project_path>] [--dry-run]` |
| manager | sync | — | — | `[<project_path>] [--dry-run]` |
| manager | check-updates | — | — | `[<project_path>]` |

```bash
# 初始化新项目
manager init /root/data/disk/仓库/my-project --type thesis

# 整理项目文件
manager organize /root/data/disk/仓库/my-project
manager organize --dry-run

# 同步模板
manager sync /root/data/disk/仓库/my-project

# 检查更新
manager check-updates /root/data/disk/仓库/my-project
```

### presenter

| 技能名 | 模块 | 方法 | 参数 |
|--------|------|------|------|
| presenter | list | — | `--template <name>` |
| presenter | extend | — | `--template <name> --add <layout1> <layout2>...` |
| presenter | compile | — | `--input <script.md> --output <out.pptx> --template <name>` |

```bash
presenter list --template template
presenter extend --template template --add timeline flowchart
presenter compile --input script.md --output out.pptx --template template
```

---

## lookup 命令规范（lookup!）

`lookup` 是 OpenClaw 内置工具，通过 `SKILL.md` 引用时使用 `lookup!` 标记。

```markdown
### lookup! 搜索

\`\`\`bash
lookup index -r <references_path> -m <manifest_path> -c <chunks_path>
lookup search -i <manifest_path> <关键词>
lookup list -i <manifest_path>
\`\`\`
```

**注意**：`lookup` 不是技能脚本，不需要在 `scripts/` 中实现。

---

## 子命令路由规范（main.py）

多模块技能必须使用 `main.py` 统一分发：

```python
#!/usr/bin/env python3
"""技能名 CLI 统一入口。"""

import sys
from pathlib import Path

_SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SKILL_ROOT))

from scripts.模块A import main as 模块A_main
from scripts.模块B import main as 模块B_main


def main() -> int:
    if len(sys.argv) < 2:
        print_help()
        return 0

    subcmd = sys.argv[1]
    del sys.argv[1]          # 必须删除子命令本身

    if subcmd == "模块A":
        sys.argv[0] = "<技能名> 模块A"
        return 模块A_main()
    elif subcmd == "模块B":
        sys.argv[0] = "<技能名> 模块B"
        return 模块B_main()
    else:
        print(f"Error: 未知子命令 '{subcmd}'")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
```

---

*详见 [scripts-standards.md](scripts-standards.md)*
