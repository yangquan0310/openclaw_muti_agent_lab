# CLI 建立工作流

> 新技能需要CLI时的标准流程。重点是**决策顺序**和**文件生成顺序**，而非具体命令。

---

## 流程概览

```
① 明确CLI结构 → ② 写模块 → ③ 写分发层 → ④ 暴露CLI → ⑤ SKILL.md声明
```

---

## ① 明确CLI结构

在动手前，先在脑子里或草稿中确定：

```
{技能名} {模块} [{子模块}] [{方法}] [{参数}]
```

- **技能名**：`project.name`（pyproject.toml），全小写
- **模块**：顶层功能分组，1个或多个
- **子模块/方法**：按需追加，optional
- **参数**：位置参数在前，选项参数在后

### 判断：多模块还是单模块？

| 判断条件 | 类型 | 分发方式 |
|----------|------|----------|
| 业务功能 ≥ 2 个独立模块 | 多模块 | 必须写 `main.py` 做子命令分发 |
| 业务功能只有 1 个 | 单模块 | `main.py` 做统一入口（透传参数给子模块），wrapper 指向 `main.py` |

---

## ② 写各模块（`scripts/{module}.py`）

每个模块一个文件，每个文件必须同时包含：

1. **`class`**：业务逻辑封装（文件名 = 类名）
2. **`main()` 函数**：命令行解析 + 业务调用，返回 `int`（0=成功，1=失败）
3. **`if __name__ == '__main__':`**：入口，调用 `raise SystemExit(main())`

```python
# scripts/模块A.py
class 模块A:
    ...

def main() -> int:
    parser = argparse.ArgumentParser(...)
    # 解析参数
    # 调用业务逻辑
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
```

> 如果某模块内部还有子功能，用 `subparsers` 在模块内部处理，不单独拆文件。

---

## ③ 写分发层

### 多模块 → 必须写 `scripts/main.py`

```python
# scripts/main.py
# 导入所有模块的 main
# 在 main() 中解析 sys.argv[1] 得到 subcmd
# del sys.argv[1]（关键！删掉子命令本身）
# 按 subcmd 分发到对应模块的 main()
```

### 单模块 → main.py 做透传

`main.py` 导入子模块的 `main()` 并直接透传，wrapper 指向 `main.py`：

```python
# scripts/main.py（单模块透传）
from scripts.子模块 import main as 子模块_main

def main() -> int:
    return 子模块_main()
```

---

## ④ 暴露CLI

当前 `/usr/local/bin/` wrapper 是临时方案，后续应通过 `pyproject.toml` 的 `entry_points` 自动生成。

**临时方案**（手动建 wrapper）：
1. 创建 `/usr/local/bin/{技能名}`
2. 写入 `exec python3 {path}/scripts/main.py "$@"`（或多模块路径）
3. `chmod +x /usr/local/bin/{技能名}`

**正确方案**（future）：
```toml
# pyproject.toml
[project.scripts]
{技能名} = "scripts.main:main"
```
安装后自动生成 CLI。

---

## ⑤ SKILL.md 声明

在 `## 命令行（CLI）` 或 `## 快速调用` 章节中，按格式声明：

```markdown
## 命令行（CLI）

```bash
{技能名} {模块A} [参数...]
{技能名} {模块B} [参数...]
```
```

---

## 决策树

```
需要CLI？
  │
  ├── 业务模块 ≥ 2 个？
  │     ├── 是 → 写 scripts/main.py 做分发
  │     └── 否 → 直接 wrapper → 脚本
  │
  └── 暴露CLI（临时wrapper / 正式entry_points）
        │
        └── SKILL.md 声明
```

---

*详见 [cli-standards.md](cli-standards.md)*
