---
name: mathematician
description: >
  mathematician 技能的参考资料索引。
---

## 命令行（CLI）

```bash
# 数值计算
mathematician calculate basic 1 2 add
mathematician calculate matrix --A '[[1,2],[3,4]]' --op inverse
mathematician calculate integrate --func 'x**2' --a 0 --b 1
mathematician calculate root --func 'x**2-2' --x0 0,2

# 统计分析
mathematician statistics describe --data 1,2,3,4,5
mathematician statistics ttest --a 5.0 --b 5.5 --n1 10 --n2 10
mathematician statistics regress --x 1,2,3 --y 2,4,6

# 数据可视化
mathematician visualize function --func 'x**2' --xmin -10 --xmax 10
mathematician visualize scatter --x 1,2,3 --y 2,4,6
mathematician visualize histogram --data 1,2,2,3,3,3,4,5

# 查看帮助
mathematician -h
mathematician calculate --help
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
