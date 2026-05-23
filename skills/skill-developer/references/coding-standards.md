# 代码规范

> scripts/ 如何组织代码，不写死结构，由代理根据目的决定

---

## 核心原则

**目的决定形式**：不是先定结构，而是先明确要做什么，再选择合适的代码组织方式。

---

## scripts/ 结构选择

### 选项 1：纯方法脚本

适用于：工具类、一次性脚本、简单操作

```
scripts/
└── {方法}.py          # 直接是方法脚本
```

### 选项 2：面向对象模块

适用于：需要状态管理、多个相关方法、类层次结构

```
scripts/
└── {模块}/
    ├── __init__.py
    └── {类}.py
```

### 选项 3：完整应用

适用于：复杂逻辑、多文件协同、CLI 入口

```
scripts/
└── {应用}/
    ├── __init__.py
    ├── main.py         # CLI 入口（可选）
    ├── {子模块}.py
    └── ...
```

---

## 命名规范

| 对象 | 规范 | 示例 |
|------|------|------|
| **类名** | 单数名词，PascalCase | `Searcher`, `Maintainer` |
| **方法名** | 动词/动宾短语，snake_case | `search()`, `archive_file()` |
| **文件名** | 与类名一致或描述性名称 | `Searcher.py`, `utils.py` |
| **私有方法** | `_` 前缀 | `_validate()`, `_build_path()` |

---

## MCP 暴露规范

scripts/ 中的方法通过 `mcp/server.py` 暴露：

```python
# mcp/server.py
EXPOSED_TOOLS = [
    {
        "name": "{skill_name}_{action}",
        "description": "执行某个操作",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["action1", "action2"],
                    "description": "要执行的操作"
                }
            },
            "required": ["action"]
        }
    }
]
```

**原则**：MCP server 只路由，不重复业务逻辑。业务逻辑在 scripts/ 中实现。

---

## 安全规范

- ❌ 不在脚本中硬编码 API Key（通过 env 或参数传入）
- ❌ 不在脚本中硬编码用户敏感数据
- ✅ 临时文件写入 `/tmp/` 或 `tempfile`，使用后清理
- ✅ 操作前验证路径存在，操作后验证结果

---

*详见 [索引](index.md)*
