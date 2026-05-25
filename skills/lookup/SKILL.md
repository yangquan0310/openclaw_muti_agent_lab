---
name: lookup
description: >
  中央 References 搜索与索引工具。为所有技能提供统一的文档检索能力。
version: 2.0.0
---

# lookup（文档检索工具）

> 中央 References 搜索与索引工具

---

## 问题

### 什么是 lookup？

lookup 是**文档检索工具**，用于：
- 为技能构建索引（manifest.json + chunks.json）
- 在索引中搜索关键词
- 列出已索引的文件

### 什么时候用 lookup？

| 场景 | 操作 |
|------|------|
| 技能有新的 references | 先 `lookup index` 构建索引 |
| 需要搜索技能文档 | `lookup search` |
| 忘记索引包含哪些文件 | `lookup list` |

---

## 方法论

### 工作原理

```
references/*.md → Indexer → manifest.json + chunks.json
                                    ↓
                            Searcher ← 关键词
                                    ↓
                               排序结果
```

| 文件 | 内容 |
|------|------|
| manifest.json | 索引清单：文件路径、标题、描述、关键词 |
| chunks.json | 内容块：每个文件的章节结构 |

### 索引路径规则

| 参数 | 说明 |
|------|------|
| `-r <references>` | references 目录路径 |
| `-m <manifest>` | manifest.json 输出路径（默认：`<references>/../index/manifest.json`）|
| `-c <chunks>` | chunks.json 输出路径（默认：与 manifest 同目录）|

---

## 工作流

### 步骤 1：构建索引

```bash
lookup index -r <references> [-m <manifest.json>] [-c <chunks.json>]
```

**示例**：
```bash
# 默认输出到 references/../index/
lookup index -r ~/.openclaw/skills/research-assistant/references

# 指定输出路径
lookup index -r ./references -m /tmp/manifest.json -c /tmp/chunks.json
```

### 步骤 2：搜索

```bash
lookup search -i <manifest.json> <关键词> [-k <结果数>]
```

**示例**：
```bash
lookup search -i ~/.openclaw/skills/research-assistant/index/manifest.json 文献检索

# 只显示文件匹配
lookup search -i manifest.json 检索 -f
```

### 步骤 3：列出已索引文件

```bash
lookup list -i <manifest.json>
```

---

## 执行标准

### 索引质量检查

| 检查项 | 标准 |
|--------|------|
| manifest.json 存在 | 文件非空 |
| chunks.json 存在 | 文件非空 |
| 关键词命中 | 搜索结果 > 0 |

### CLI 格式规范

| 命令 | 格式 |
|------|------|
| index | `lookup index -r <references> [-m <manifest>] [-c <chunks>]` |
| search | `lookup search -i <manifest> <query> [-k <top>]` |
| list | `lookup list -i <manifest>` |

---

## 快速命令

```bash
# 构建索引
lookup index -r ~/.openclaw/skills/xxx/references

# 搜索
lookup search -i ~/.openclaw/skills/xxx/index/manifest.json <关键词>

# 列出文件
lookup list -i ~/.openclaw/skills/xxx/index/manifest.json
```

---

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 2.0.0 | 2026-05-25 | 新框架适配：SKILL.md 重构 |
| 1.0.0 | 2026-05-24 | 初始版本 |
