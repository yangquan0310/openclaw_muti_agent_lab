---
name: writer
description: >
  writer 技能的参考资料索引。
---

## 命令行（CLI）

```bash
# 自检文章
writer --file essay.md
writer --file essay.md --level sentence
writer --file essay.md --level paragraph
writer --file essay.md --level chapter

# 查看帮助
writer --help
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
