# 如何编写 scripts

> 如何编写技能的 scripts/ 目录。

---

## 问题

### scripts/ 是什么？

`scripts/` 是技能的**业务逻辑目录**，包含所有可执行的方法。它是一个独立 Python 应用集合，不依赖 OpenClaw。

### scripts/ 和 mcp/ 的区别？

| | scripts/ | mcp/ |
|---|---|---|
| **定位** | 业务逻辑 | MCP 工具暴露 |
| **入口** | CLI 命令或被 import | OpenClaw 自然语言触发 |
| **关系** | 被 mcp/server.py 调用 | 调用 scripts/ 中的方法 |

### scripts/ 和 SKILL.md 的关系？

SKILL.md 声明技能的触发条件，scripts/ 实现具体的业务逻辑。SKILL.md 告诉代理"什么时候用"，scripts/ 告诉代理"具体怎么做"。

---

## 方法论

### 目录结构哲学

`scripts/` 的结构由**目的决定**，不写死：

| 需要的结构 | 对应的场景 |
|------------|------------|
| 单文件 `scripts/xxx.py` | 只有一个业务功能 |
| `scripts/main.py` + 多模块 | 多个独立业务功能 |
| `scripts/xxx/` 子包 | 复杂业务需要模块内部再拆分 |

### 单模块 vs 多模块的判断

| 判断条件 | 类型 | 结构 |
|----------|------|------|
| 业务功能只有 1 个 | 单模块 | 唯一模块文件作为入口 |
| 业务功能 ≥ 2 个独立模块 | 多模块 | `main.py` 做分发 |

### 文件组织原则

1. **一个文件 = 一个类 = 一个业务概念**
2. **文件名 = 类名（单数名词）**
3. **类内方法用动词，公共方法暴露给外部调用**

---

## 工作流

### 步骤 1：确定 scripts/ 结构

```
业务功能数量 = 1？
├── 是 → 单模块结构
│        scripts/
│        └── {module}.py
│
└── 否 → 多模块结构
         scripts/
         ├── main.py
         ├── {module-a}.py
         └── {module-b}.py
```

### 步骤 2：写单模块文件

```python
#!/usr/bin/env python3
"""{模块描述}"""

class {模块名}:
    """业务逻辑封装"""

    def __init__(self):
        self._internal_state = None

    def do_something(self, param: str) -> dict:
        """执行某个操作"""
        return {"success": True, "result": param}


def main() -> int:
    """命令行入口"""
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
```

### 步骤 3：写多模块分发（main.py）

```python
#!/usr/bin/env python3
"""CLI 统一入口"""
import sys
from pathlib import Path

_SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SKILL_ROOT))

from scripts.bazi import main as bazi_main
from scripts.lunar import main as lunar_main


def main() -> int:
    if len(sys.argv) < 2:
        print_help()
        return 0

    subcmd = sys.argv[1]
    del sys.argv[1]  # 关键：删除子命令本身

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

### 步骤 4：关联 MCP 工具

在 `mcp/server.py` 中注册：

```python
EXPOSED_TOOLS = [
    {
        "name": "{skill}_do_something",
        "description": "执行某个操作",
        "parameters": {
            "type": "object",
            "properties": {
                "param": {"type": "string", "description": "参数说明"}
            },
            "required": ["param"]
        }
    }
]
```

---

## 执行标准

### 结构标准

| 标准 | 要求 |
|------|------|
| 目录存在 | `scripts/` 目录存在 |
| 模块文件命名 | PascalCase 或 snake_case，与类名一致 |
| 单模块入口 | 唯一模块文件包含 `main()` 函数 |
| 多模块入口 | `main.py` 包含 `main()` 函数做分发 |

### 文件标准

```python
# ❌ 文件名与类名不匹配
calculator.py  →  class Calculator      # ✅
calculators.py →  class Calculator      # ❌

# ❌ 函数名用名词
def reader(path): ...                    # ❌
def parser(text): ...                   # ❌
def searcher(query): ...               # ❌

# ✅ 函数名用动词
def read(path: str) -> dict:
def parse(text: str) -> dict:
def search(query: str) -> list:
```

### 函数签名标准

```python
# ❌ 没有类型注解
def do_something(param):
    return {"success": True}

# ✅ 有类型注解
def do_something(param: str) -> dict:
    return {"success": True, "result": param}

# ❌ 裸 argparse 在模块顶层
parser = argparse.ArgumentParser()  # ❌
args = parser.parse_args()

# ✅ argparse 在 main() 函数内
def main() -> int:
    parser = argparse.ArgumentParser(description='...')
    args = parser.parse_args()
    return 0
```

### 入口标准

```python
# ❌ 使用 sys.exit
if __name__ == '__main__':
    sys.exit(main())

# ✅ 使用 raise SystemExit
if __name__ == '__main__':
    raise SystemExit(main())
```

### 路径导入标准

```python
# ❌ sys.path 操作在函数外部
import sys
sys.path.insert(0, '/path/to/skill')

# ✅ 动态计算路径
from pathlib import Path
_SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SKILL_ROOT))
```

---

## 检查清单

### 文件检查

- [ ] `scripts/` 目录存在
- [ ] 模块文件命名与类名一致
- [ ] 每个模块文件包含 `main()` 函数
- [ ] 每个模块文件包含 `if __name__ == '__main__'` 入口

### 函数检查

- [ ] 函数名使用动词/动宾
- [ ] 公共方法有类型注解
- [ ] `main()` 返回 `int`（0=成功，1=失败）
- [ ] argparse 在 `main()` 函数内，不在模块顶层

### CLI 检查

- [ ] 多模块技能有 `main.py` 做分发
- [ ] `main.py` 中有 `del sys.argv[1]`
- [ ] `main.py` 中有 `sys.argv[0]` 重命名
- [ ] MCP 工具在 `mcp/server.py` 中注册
