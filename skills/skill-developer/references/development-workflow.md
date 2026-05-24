# 开发工作流

> 技能开发不是按流程执行，而是围绕约束、目的、迭代展开

:::tip 配套参考
开发前先阅读 [开发原则](development-guide.md)，理解"先手动跑通"、"六步成技"等核心准则。
:::

---

## 核心理念

> **约束 > 流程**，**目的 > 形式**，**进化 > 固化**

开发不是"按步骤做"，而是明确：
1. **约束**：这个技能解决什么问题？边界在哪里？
2. **目的**：代理用这个技能要达成什么？
3. **迭代**：先跑通，再优化，不追求一步完美

---

## 开发阶段

### 阶段 1：明确约束

**必答问题**：
- 这个技能解决什么问题？
- 触发条件是什么？
- 技能的边界在哪里（能做什么/不能做什么）？

**输出**：
- SKILL.md 的触发条件
- _meta.json 的 description 和 triggers

---

### 阶段 2：设计结构

**根据目的选择**：
- 需要 CLI 入口吗？→ 需要 scripts/main.py
- 需要面向对象吗？→ 创建 scripts/{模块}/
- 需要 MCP 暴露吗？→ 创建 mcp/server.py

**原则**：结构由目的决定，不写死。

---

### 阶段 3：实现方法

在 scripts/ 中实现具体方法：

```python
#!/usr/bin/env python3
"""
{方法描述}
"""

def do_something(param: str) -> dict:
    """执行某个操作"""
    return {"success": True, "result": param}
```

---

### 阶段 4：MCP 暴露

在 `mcp/server.py` 中注册工具：

```python
EXPOSED_TOOLS = [
    {
        "name": "{skill}_do_something",
        "description": "执行某个操作",
        "parameters": {...}
    }
]
```

---

### 阶段 5：撰写指南

在 `references/` 中撰写指南：
- `guide.md` — 使用指南
- `index.md` — 索引

**原则**：指南回答问题，不是复述结构。

---

### 阶段 6：自检与迭代

**自检脚本**：`skill-developer/scripts/selfcheck.py`

**自检清单**：`skill-developer/assets/templates/selfcheck-checklist.md`

```bash
python3 scripts/selfcheck.py /path/to/skill
```

**自检不通过？** → 修复 → 再次自检 → 通过后 Git 提交

---

## 版本管理

| 变更类型 | 版本号规则 |
|----------|------------|
| Bug 修复 | patch: 1.0.0 → 1.0.1 |
| 新增功能（向下兼容） | minor: 1.0.0 → 1.1.0 |
| 不兼容变更 | major: 1.0.0 → 2.0.0 |

---

*详见 [索引](index.md)*
