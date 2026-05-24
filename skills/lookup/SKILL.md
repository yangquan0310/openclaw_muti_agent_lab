---
name: lookup
description: >
  中央 References 搜索与索引工具。为所有技能提供统一的文档检索能力。
  当用户询问某个技能的使用方法、参数、示例时激活。
  自动支持 OpenClaw 内置技能（~/.openclaw/skills/<name>/）和 Workspace 技能（~/.openclaw/workspace/<name>/skills/<name>/）两种路径。
---

## 命令行（CLI）

```bash
# 搜索指南
lookup search --skill <技能名> <关键词>

# 列出已索引文件
lookup list --skill <技能名>

# 构建/更新索引
lookup index --skill <技能名>

# 示例
lookup search --skill lark-base 仪表盘
lookup search --skill programmer 设计模式
lookup index --skill skill-developer
lookup list --skill lark-calendar
```

## 工作原理

- **索引构建**：`lookup index` 扫描技能的 `references/` 目录，提取每个 `.md` 文件的标题、描述、关键词、章节结构，输出到技能的 `index/` 目录
- **搜索**：`lookup search` 在已构建的索引中匹配关键词，结合词重叠率和关键词命中计算相关性分数
- **路径解析**：自动尝试 `~/.openclaw/skills/<name>/` 和 `~/.openclaw/workspace/<name>/skills/<name>/` 两条路径

## 索引维护

索引文件位于各技能的 `index/` 目录（与 `references/` 同级）：

```
~/.openclaw/skills/<技能名>/
├── references/          # 源文档（人工维护）
│   ├── guide.md
│   └── *.md
└── index/               # 索引数据（自动生成）
    ├── manifest.json     # 文件元数据
    └── chunks.json       # 内容块索引
```

## 快速调用

```bash
lookup search --skill lark-base 仪表盘
lookup search --skill skill-developer 命名规范
lookup index --skill research-assistant
```

## 版本历史

| 版本 | 日期 | 更新 |
|------|------|------|
| 1.0.0 | 2026-05-24 | 初始版本，中央 lookup 库 |
