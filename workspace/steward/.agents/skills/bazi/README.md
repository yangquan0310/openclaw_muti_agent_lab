# 八字排盘技能 (Bazi Skill)

按公历时间输出完整四柱八字 + 十神 + 五行。

## 安装

```bash
pip install cnlunar
```

可选（用于天文精确校验）：

```bash
pip install sxtwl
```

## 快速上手

```bash
# CLI
bazi 1996-03-10 14:30
bazi --self-test

# Python
from bazi import build_bazi_from_str
bz = build_bazi_from_str("1996-03-10", "14:30")
print(bz.pretty())
```

## 详细文档

见 [`SKILL.md`](SKILL.md)。

## 规则速查

见 [`references/bazi-rules.md`](references/bazi-rules.md)。

## 测试

```bash
cd scripts
python3 bazi_cli.py --self-test
```

## License

MIT（待定）