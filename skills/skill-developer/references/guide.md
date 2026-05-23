# 使用指南

> skill-developer 技能开发完整使用说明

---

## 触发条件

当用户提到以下场景时触发：
- "创建一个技能"
- "新建一个 OpenClaw 技能"
- "教我如何开发技能"

---

## 初始化

```bash
python3 scripts/init.py <skill-name> <description> [path] [emoji]
```

**示例**：
```bash
python3 scripts/init.py my-skill "这是一个测试技能" ./my-skill 📦
```

**产出结构**：
```
{skill-name}/
├── SKILL.md
├── README.md
├── _meta.json
├── assets/templates/
├── scripts/
├── mcp/
│   └── server.py
└── references/
```

---

## 编写 SKILL.md

SKILL.md 是技能的导航首页，包含：
- 触发条件
- 模块导航
- 快速调用
- 版本历史

详见 [如何写指南](how-to-write-guide.md)

---

## MCP 工具暴露

scripts/ 下的方法通过 mcp/server.py 暴露为 MCP 工具。

```python
# mcp/server.py
EXPOSED_TOOLS = [
    {
        "name": "{skill_name}_do_something",
        "description": "执行某个操作",
        "parameters": {...}
    }
]
```

---

## 质量检查

完成开发后，使用自检脚本检查：

**自检脚本**：`scripts/selfcheck.py`（来自 skill-developer）

**自检清单**：`skill-developer/assets/templates/selfcheck-checklist.md`

```bash
python3 scripts/selfcheck.py /path/to/skill
```

详见 [质量标准](quality-standards.md)

---

## 发布

1. 更新 `_meta.json` 版本号
2. 更新 `SKILL.md` 版本历史
3. Git commit

---

*详见 [索引](index.md) 导航全部指南*
