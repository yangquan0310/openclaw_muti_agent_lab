---
name: fortunetelling
description: >
  fortunetelling 技能的参考资料索引。
---

## 命令行（CLI）

```bash
# 八字排盘
fortunetelling bazi 1990 5 15 10 --gender 男

# 阴历转公历
fortunetelling lunar 1990 4 15 10

# 运势分析
fortunetelling fate 1990 5 15 10 --gender 男 --type timing

# 查看帮助
fortunetelling -h
fortunetelling bazi --help
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
