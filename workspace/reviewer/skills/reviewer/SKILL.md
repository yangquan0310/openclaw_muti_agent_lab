---
name: reviewer
description: >
  reviewer 技能的参考资料索引。
---

## 命令行（CLI）

```bash
# 审稿清单
reviewer --type thesis paper.pdf
reviewer -t journal paper.pdf --output review.md
reviewer --type opensource --output review.md

# 查看帮助
reviewer --help
```

## 索引

```bash
lookup index -r $SKILL_REFS -m $SKILL_INDEX/manifest.json -c $SKILL_INDEX/chunks.json
lookup search -i $SKILL_INDEX/manifest.json <关键词>
lookup list -i $SKILL_INDEX/manifest.json
```

## 索引文件

- manifest: `$SKILL_INDEX/manifest.json`
- chunks: `$SKILL_INDEX/chunks.json`

## 版本历史

| 版本 | 日期 | 更新 |
|------|------|------|
| 1.0.0 | 2026-05-24 | 初始版本 |
