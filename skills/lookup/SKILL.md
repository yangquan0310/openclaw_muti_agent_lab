---
name: lookup
description: >
  中央 References 搜索与索引工具。为所有技能提供统一的文档检索能力。
  当用户询问某个技能的使用方法、参数、示例时激活。
---

## 命令行（CLI）

```bash
# 构建索引
lookup index -r <references> [-m <manifest.json>] [-c <chunks.json>]
lookup index -r ./references                       # 默认输出到 ./index/
lookup index -r ./references -m /tmp/idx.json       # 指定 manifest 路径
lookup index -r ./references -c /tmp/chunks.json    # 指定 chunks 路径

# 搜索（需要 manifest.json 路径）
lookup search -i <manifest.json> <关键词>

# 列出已索引文件
lookup list   -i <manifest.json>
```

## 工作原理

- **索引构建**：扫描 `references/` 目录，提取每个 `.md` 的标题、描述、关键词、章节结构，分别输出到 `manifest.json` 和 `chunks.json`
- **搜索**：在索引中匹配关键词，结合词重叠率和关键词命中计算相关性分数

## 快速调用

```bash
# mathematician
lookup index -r ~/.openclaw/workspace/mathematician/skills/mathematician/references
lookup search -i ~/.openclaw/workspace/mathematician/skills/mathematician/index/manifest.json 工作流

# lark-base
lookup search -i ~/.openclaw/skills/lark-base/index/manifest.json 仪表盘
```

## 版本历史

| 版本 | 日期 | 更新 |
|------|------|------|
| 1.0.0 | 2026-05-24 | 初始版本，-r/-m/-c 三个独立参数 |
