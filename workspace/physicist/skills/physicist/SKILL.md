---
name: physicist
description: >
  physicist 技能的参考资料索引。
---

## 命令行（CLI）

```bash
# 数值计算
physicist calculate basic 1 2 add
physicist calculate matrix --A '[[1,2],[3,4]]' --op inverse
physicist calculate integrate --func 'x**2' --a 0 --b 1
physicist calculate ode --func 't,y' --y0 1 --t0 0 --t1 10

# 物理可视化
physicist visualize function --func 'sin(x)' --xmin 0 --xmax 3.14
physicist visualize phase --func 'y,-x' --y0 1 --t0 0 --t1 20
physicist visualize field --func 'x,y' --xmin -5 --xmax 5
physicist visualize surface --func 'sin(sqrt(x**2+y**2))' --xmin -5 --xmax 5

# 查看帮助
physicist -h
physicist calculate --help
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
