# 质量检查清单

> 技能交付前的必检项，确保质量和一致性

---

## 必选检查项

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 1 | SKILL.md 存在 | 文件存在 |
| 2 | README.md 存在 | 文件存在 |
| 3 | _meta.json 存在 | 文件存在 |
| 4 | scripts/ 目录存在 | 目录存在 |
| 5 | mcp/server.py 存在 | 文件存在 |
| 6 | references/ 目录存在 | 目录存在 |
| 7 | references/index.md 存在 | 文件存在 |
| 8 | references/guide.md 存在 | 文件存在 |
| 9 | _meta.json 格式正确 | JSON 有效 |
| 10 | entry_point 指向 mcp/server.py | 配置正确 |

---

## 结构检查

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 11 | 目录命名小写 + 横线分隔 | 如 `my-skill` |
| 12 | 类文件在 scripts/（若有） | 命名与类名一致 |
| 13 | Python 脚本可独立运行 | `if __name__ == "__main__"` |

---

## 文档检查

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 14 | SKILL.md 有 YAML frontmatter | name/description/version |
| 15 | SKILL.md 正文不超过 200 行 | 行数合理 |
| 16 | 触发条件已填写 | 非空、有意义 |
| 17 | 指南回答实际问题 | 不是占位符或空洞复述 |

---

## 代码检查

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 18 | 方法名有具体含义 | 非 `main`/`do_something` |
| 19 | 无 API Key 明文 | 通过 env 或参数传入 |
| 20 | 无用户敏感数据硬编码 | 无 phone/email/id 等 |

---

## MCP 检查

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 21 | mcp/server.py 可运行 | `python3 mcp/server.py` 不报错 |
| 22 | EXPOSED_TOOLS 结构正确 | JSON 格式、必填字段存在 |

---

## 自检命令

```bash
python3 scripts/selfcheck.py /path/to/skill
```

---

*详见 [索引](index.md)*
