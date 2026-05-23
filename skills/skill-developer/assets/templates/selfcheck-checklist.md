# {skill-name} 自检清单

> 技能开发完成后使用。执行 `python3 scripts/main.py selfcheck` 进行自动检查。

---

## ✅ 必选检查项

| # | 检查项 | 通过标准 | 自检命令 |
|---|--------|----------|----------|
| 1 | SKILL.md 存在 | 文件存在 | `ls SKILL.md` |
| 2 | README.md 存在 | 文件存在 | `ls README.md` |
| 3 | _meta.json 存在 | 文件存在 | `ls _meta.json` |
| 4 | scripts/ 目录存在 | 目录存在 | `ls scripts/` |
| 5 | references/ 目录存在 | 目录存在 | `ls references/` |
| 6 | _meta.json 格式正确 | JSON 有效 | `python3 -c "import json; json.load(open('_meta.json'))"` |
| 7 | SKILL.md ≤ 200 行 | 行数合理 | `wc -l SKILL.md` |
| 8 | 触发条件已填写 | 非空描述 | 检查 SKILL.md 的 description |

---

## ⚠️ 建议检查项

| # | 检查项 | 说明 |
|---|--------|------|
| 1 | assets/templates/ 模板完整 | 初始化所需模板齐全 |
| 2 | references/guide.md 已撰写 | 使用指南非空 |
| 3 | 命名符合规范 | 类名 PascalCase，方法名 snake_case |

---

## 🚫 不允许项

| # | 检查项 | 错误示例 |
|---|--------|----------|
| 1 | SKILL.md 包含完整代码 | 业务逻辑应放在 scripts/ |
| 2 | 模板文件含占位符 `{xxx}` | 初始化时由 main.py 替换 |
| 3 | references/ 嵌套子目录 | 应扁平化 |

---

*自检命令：`python3 scripts/main.py selfcheck`*
