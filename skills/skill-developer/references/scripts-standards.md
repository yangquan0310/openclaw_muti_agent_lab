# scripts 规范

> 技能的 `scripts/` 目录是一个独立 CLI 应用集合，必须满足以下结构与编码规范。

---

## 目录结构

```
skills/<name>/
├── SKILL.md
├── scripts/
│   ├── main.py              # CLI 统一入口（可选，仅多子命令时必需）
│   └── {module}/            # 可选：模块内部子包
│       ├── __init__.py
│       └── {class}.py
├── references/
└── assets/
```

**单子命令技能**（如 `skill-developer` 的 `init`）：可省略 `main.py`，直接让唯一模块作为入口。

**多子命令技能**（如 `fortunetelling`/`research-assistant`）：必须有 `main.py` 做分发。

---

## `scripts/` 是独立应用目录

`scripts/` 是**独立 Python 应用集合**，不是包：

- **不需要** `__init__.py`
- **不需要** `sys.path` 操作
- 直接用 `python3 /path/to/scripts/main.py` 或 wrapper 调用

```python
import sys
from pathlib import Path

_SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SKILL_ROOT))

from scripts.bazi  import main as bazi_main
from scripts.lunar import main as lunar_main
```

---

## 模块文件规范（`{module}.py`）

每个模块文件（如 `bazi.py`）必须同时满足：

### 1. 文件名 = 类名（单数名词）

| 正确 | 错误 |
|------|------|
| `searcher.py`（含 `class Searcher`） | `searchers.py` |
| `calculator.py`（含 `class Calculator`） | `calculate.py` |

### 2. 函数名使用动词

```python
# ✅ 正确
def search(query: str) -> list[dict]:
def calculate(formula: str, vars: dict) -> float:
def validate(script_path: Path) -> bool:

# ❌ 错误
def searcher(query):          # searcher 是名词
def calculation(formula):     # calculation 是名词
```

### 3. 每个模块必须有 `main()` 函数

```python
def main() -> int:
    parser = argparse.ArgumentParser(description='八字排盘')
    parser.add_argument('year', type=int, help='年份')
    parser.add_argument('month', type=int, help='月份')
    args = parser.parse_args()
    # 业务逻辑...
    return 0
```

### 4. 每个模块必须有 `__main__` 入口

```python
if __name__ == '__main__':
    raise SystemExit(main())
```

**注意**：不使用 `sys.exit(main())` 在模块顶层，因为 `main.py` 会调用 `main()` 并自己处理返回值。

### 5. 完整示例

```python
#!/usr/bin/env python3
"""八字排盘模块。"""

import argparse
from pathlib import Path

class BaziReader:
    """读取并解析八字信息。"""

    def __init__(self, year: int, month: int, day: int):
        self.year = year
        self.month = month
        self.day = day

    def read(self) -> dict:
        # 读取逻辑
        return {}


def main() -> int:
    parser = argparse.ArgumentParser(description='八字排盘')
    parser.add_argument('year', type=int, help='年份')
    parser.add_argument('month', type=int, help='月份')
    parser.add_argument('day', type=int, help='日期')
    parser.add_argument('--gender', default='男', choices=['男', '女'])
    args = parser.parse_args()

    reader = BaziReader(args.year, args.month, args.day)
    result = reader.read()
    print(result)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
```

---

## main.py 分发规范（多子命令技能）

### 标准结构

```python
#!/usr/bin/env python3
"""CLI 统一入口。"""

import sys
from pathlib import Path

_SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SKILL_ROOT))

from scripts.bazi  import main as bazi_main
from scripts.lunar import main as lunar_main


def main() -> int:
    if len(sys.argv) < 2:
        print_help()
        return 0

    subcmd = sys.argv[1]
    del sys.argv[1]          # 让子模块看到干净的参数

    if subcmd == 'bazi':
        sys.argv[0] = '<skill> bazi'
        return bazi_main()

    elif subcmd == 'lunar':
        sys.argv[0] = '<skill> lunar'
        return lunar_main()

    else:
        print(f"Error: 未知子命令 '{subcmd}'")
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
```

### 关键规则

1. **`del sys.argv[1]`** — 必须删除子命令本身，否则子模块的 argparse 会把子命令当作成位置参数
2. **`sys.argv[0]` 重命名** — 保持错误信息的可读性（如 `fortunetelling bazi: error: ...`）
3. **`raise SystemExit(main())`** — 不在 `__main__` 层调用 `sys.exit()`

---

## 禁止形式

```python
# ❌ 禁止：裸 argparse 在模块顶层（与 main.py 分发冲突）
parser = argparse.ArgumentParser()   # 应在 main() 函数内
args = parser.parse_args()           # 应在 main() 函数内

# ❌ 禁止：sys.exit 在模块 __main__ 之外调用
if __name__ == '__main__':
    sys.exit(main())                # ✅ 正确：raise SystemExit(main())

# ❌ 禁止：模块文件名与类名不匹配
calculator.py  →  class Calculator   # ✅
calculators.py →  class Calculator   # ❌

# ❌ 禁止：函数名用名词
def reader(path): ...                # ❌
def parser(text): ...               # ❌
def searcher(query): ...            # ❌

# ❌ 禁止：多模块技能缺少 main.py
skills/fortunetelling/scripts/
  bazi.py     # ❌ 没有 main.py 无法统一调用
  lunar.py
  fate.py
```

---

*详见 [索引](index.md)*
