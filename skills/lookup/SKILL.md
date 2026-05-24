---
name: lookup
description: >
  中央 References 搜索与索引工具。为所有技能提供统一的文档检索能力。
  当用户询问某个技能的使用方法、参数、示例时激活。
---

## 命令行（CLI）

```bash
# 构建索引
lookup index  -r <references目录> [-i <输出索引目录>]
lookup index  -r ./skill/references                  # 输出到 <references>/../index/
lookup index  -r ./skill/references -i /tmp/my-index

# 搜索
lookup search -i <manifest.json路径> <关键词>

# 列出已索引文件
lookup list   -i <manifest.json路径>
```

## 工作原理

- **索引构建**：`lookup index -r` 扫描 `references/` 目录，提取每个 `.md` 的标题、描述、关键词、章节结构，输出到 `index/` 目录（manifest.json + chunks.json）
- **搜索**：`lookup search -i` 在已构建的索引中匹配关键词，结合词重叠率和关键词命中计算相关性分数
- **路径**：`--index` 必须指向 `manifest.json` 文件本身

## 快速调用

```bash
# mathematician
lookup index  -r ~/.openclaw/workspace/mathematician/skills/mathematician/references
lookup search -i ~/.openclaw/workspace/mathematician/skills/mathematician/index/manifest.json 工作流

# lark-base
lookup search -i ~/.openclaw/skills/lark-base/index/manifest.json 仪表盘
```

## 版本历史

| 版本 | 日期 | 更新 |
|------|------|------|
| 1.0.0 | 2026-05-24 | 初始版本，--index 指向 manifest.json 文件 |
