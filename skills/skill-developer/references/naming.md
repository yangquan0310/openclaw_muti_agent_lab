# 命名规范

> 技能、文件、CLI 命令的命名约定。

---

## 技能名称

| 标准 | 要求 |
|------|------|
| 字符 | 字母、数字、连字符 |
| 大小写 | 全部小写 |
| 分隔符 | 单词间用连字符 `-` |
| 长度 | 不超过 20 字符 |
| 风格 | 名词短语或动名词 |

**好的名称**：`code-review`、`weather-query`、`skill-creation`

**坏的名称**：`CodeReview`、`code_review`、`code review`、`codeReview`

---

## 文件名称

| 类型 | 规范 |
|------|------|
| references/ | `xxx.md`，名词短语，如 `skill-creation.md` |
| scripts/ | `xxx.py`，如 `skill/init.py` |
| assets/ | 描述性名称，如 `skill-template.md` |

**references/ 文件禁止**：
- `how-to-xxx.md`（提示词风格）
- `guide.md`、`tutorial.md`（太通用）

---

## CLI 命令

格式：`{技能名} {子命令} [参数]`

| 规范 | 要求 |
|------|------|
| 子命令 | 动词或动词+名词 |
| 参数 | 尽量少，每个参数有明确用途 |
| 帮助 | `-h/--help` 提供简洁说明 |

**好的例子**：`skill-developer init my-skill "描述"`

**坏的例子**：`skill-developer create-new-skill-with-options`

---

## 命名优先级

1. **清晰优先于简短**：可以稍长但必须清晰
2. **一致性优先于个性**：和现有命名保持一致
3. **目的优先于结构**：名字反映目的，不反映实现
