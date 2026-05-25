# 如何开发新技能

> 如何从零开发一个新技能，包括初始化、命名、设计、实现、自检、Git 提交全流程。

---

## 问题

### 什么时候需要开发新技能？

| 场景 | 判断 |
|------|------|
| 同一类任务做了两次以上 | 应考虑做成技能 |
| 用户明确要求"创建一个技能" | 直接开始 |
| 发现现有技能无法满足需求 | 新建或扩展 |

### 开发的核心理念

> **约束 > 流程**，**目的 > 形式**，**进化 > 固化**

不是"按步骤做"，而是明确：
1. **约束**：这个技能解决什么问题？边界在哪里？
2. **目的**：代理用这个技能要达成什么？
3. **迭代**：先跑通，再优化，不追求一步完美

---

## 方法论

### 六步成技

```
① 初始化项目
     ↓
② 明确约束
     ↓
③ 设计结构
     ↓
④ 实现业务逻辑
     ↓
⑤ 自检
     ↓
⑥ Git 提交
```

### 什么时候不需要六步？

| 场景 | 可以跳过 |
|------|----------|
| 用户明确说"简单查一下" | 跳过大部分步骤 |
| 第一次做某类任务 | 还没形成方法论，先试跑 |
| 已有成熟流程 | 简化流程 |

### 结构由目的决定

不是所有技能都需要完整结构：

| 需要的结构 | 对应的目的 |
|------------|------------|
| `SKILL.md` + `references/` | 需要代理理解何时使用 |
| `scripts/` 单模块 | 只需要一个业务功能 |
| `scripts/main.py` + 多模块 | 需要多个独立功能 |
| `mcp/server.py` | 需要 MCP 工具暴露 |
| `pyproject.toml` entry_points | 需要正式 CLI 发布 |

---

## 工作流

### 步骤 1：初始化项目

#### 什么时候需要初始化？

| 场景 | 是否初始化 |
|------|------------|
| 从零创建新技能 | ✅ 必须初始化 |
| 用户明确要求"创建一个技能" | ✅ 必须初始化 |
| 复制现有技能改写 | ❌ 可跳过，直接复制 |
| 仅修改现有技能 | ❌ 不需要初始化 |

#### skill-developer init 能做什么？

| 功能 | 说明 |
|------|------|
| 生成目录结构 | 按标准创建所有必要目录 |
| 生成必要文件 | SKILL.md、README.md、_meta.json 等 |
| 生成模板 | scripts/、mcp/、references/ 的基础文件 |
| 设置 entry_points | pyproject.toml 配置 |

#### 确定技能信息

```
skill-name = ?
description = ?
path = ?
emoji = ?
```

**skill-name 规范**：
| 标准 | 要求 |
|------|------|
| 字符 | 字母、数字、连字符 |
| 大小写 | 全部小写 |
| 分隔符 | 单词间用连字符 `-` |
| 长度 | 不超过 20 字符 |

| 好的名称 | 坏的名称 |
|----------|----------|
| `code-review` | `CodeReview`、`code_review`、`code review` |
| `weather-query` | `weather`、`get-weather`、`weather_query` |

**description 规范**：
| 标准 | 要求 |
|------|------|
| 内容 | 一句话说清解决什么问题 |
| 长度 | 不超过 50 字符 |

#### 执行初始化

```bash
skill-developer init <skill-name> <description> [path] [emoji]
```

**示例**：
```bash
skill-developer init my-skill "这是一个测试技能" ./my-skill 📦
```

**产出结构**：
```
{skill-name}/
├── SKILL.md
├── README.md
├── _meta.json
├── scripts/
│   └── .gitkeep
├── mcp/
│   └── server.py
└── references/
    ├── index.md
    └── guide.md
```

#### 检查生成结果

确认以下文件存在：
- [ ] SKILL.md
- [ ] README.md
- [ ] _meta.json
- [ ] scripts/
- [ ] mcp/server.py
- [ ] references/index.md
- [ ] references/guide.md

---

### 步骤 2：明确约束

**必答问题**：
- 这个技能解决什么问题？
- 触发条件是什么？
- 技能的边界在哪里（能做什么/不能做什么）？

**输出**：
- SKILL.md 的触发条件
- _meta.json 的 description

**触发条件规范**：
| 好的触发条件 | 坏的触发条件 |
|--------------|--------------|
| "创建新技能" | "技能相关" |
| "修复 bug" | "代码问题" |
| "需要定时任务" | "自动化" |

---

### 步骤 3：设计结构

根据目的选择：

```
需要 CLI 入口？
├── 否 → 跳过 scripts/main.py
└── 是 → 多模块？→ 是 → scripts/main.py 做分发
                    └→ 否 → 单模块入口

需要 MCP 暴露？
└── 是 → mcp/server.py 注册工具

需要多模块？
├── 是 → scripts/main.py + {module-a}.py + {module-b}.py
└── 否 → scripts/{module}.py
```

详见：
- CLI 设计：[ch03_how-to-build-cli.md](ch03_how-to-build-cli.md)
- scripts 编写：[ch04_how-to-write-scripts.md](ch04_how-to-write-scripts.md)
- 命名规范：[ch05_how-to-apply-naming-conventions.md](ch05_how-to-apply-naming-conventions.md)

---

### 步骤 4：实现业务逻辑

详见 [ch04_how-to-write-scripts.md](ch04_how-to-write-scripts.md)

```python
#!/usr/bin/env python3
"""{方法描述}"""

class {模块名}:
    """业务逻辑封装"""

    def do_something(self, param: str) -> dict:
        return {"success": True}


def main() -> int:
    """命令行入口"""
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
```

---

### 步骤 5：自检

详见 [ch02_how-to-check-quality.md](ch02_how-to-check-quality.md)

```bash
python3 scripts/selfcheck.py /path/to/skill
```

**自检不通过？** → 修复 → 再次自检 → 通过后继续

---

### 步骤 6：Git 提交

```bash
git add .
git commit -m "feat: 新技能 {skill-name}"
```

---

## 执行标准

### SKILL.md 标准

| 标准 | 要求 |
|------|------|
| frontmatter | name/description/version 完整 |
| 触发条件 | 明确、有意义，不是占位符 |
| 章节结构 | 清晰、可读，行数 ≤ 200 |
| 版本历史 | 每次更新追加一条 |

### references 标准

| 标准 | 要求 |
|------|------|
| index.md | 导航链接正确 |
| 每章结构 | 问题→方法论→工作流→执行标准 |
| 内容质量 | 回答实际问题，不是空洞复述 |

### 代码标准

| 标准 | 要求 |
|------|------|
| 命名 | 见 [ch05_how-to-apply-naming-conventions.md](ch05_how-to-apply-naming-conventions.md) |
| 脚本 | 见 [ch04_how-to-write-scripts.md](ch04_how-to-write-scripts.md) |
| CLI | 见 [ch03_how-to-build-cli.md](ch03_how-to-build-cli.md) |

### 版本号规范

| 变更类型 | 版本号规则 |
|----------|------------|
| Bug 修复 | patch: 1.0.0 → 1.0.1 |
| 新增功能（向下兼容） | minor: 1.0.0 → 1.1.0 |
| 不兼容变更 | major: 1.0.0 → 2.0.0 |

---

## 检查清单

### 开发前

- [ ] 明确技能解决的问题
- [ ] 明确触发条件
- [ ] 明确技能边界

### 开发中

- [ ] 初始化项目结构
- [ ] 明确约束（触发条件、边界）
- [ ] 设计结构（CLI/MCP/多模块）
- [ ] 实现业务逻辑
- [ ] 自检通过

### 开发后

- [ ] SKILL.md frontmatter 完整
- [ ] 触发条件有意义
- [ ] Git 提交
