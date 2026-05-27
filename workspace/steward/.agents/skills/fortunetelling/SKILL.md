---
name: fortunetelling
description: >
  当用户提到「算命」、「八字」、「排盘」、「大运」、「流年」、「命理」、「算卦」时触发。
  提供阴历转八字、大运流年排盘、命理分析等命理计算服务。
version: 1.0.0
author: Yang Quan
metadata:
  openclaw:
    emoji: 🔮
    requires:
      bins: [python3]
---

# fortunetelling - 命理排盘技能

> 根据八字推算大运、流年、学业、婚姻、事业等人生运势。

---

## 触发条件

当用户提到以下场景时触发：

| 场景 | 触发关键词 |
|------|------------|
| 八字排盘 | 八字、排盘、算八字、批八字 |
| 大运流年 | 大运、流年、今年运势、明年运势 |
| 命理分析 | 命理、算命、命势、人生运势 |
| 婚姻事业 | 姻缘、婚姻、事业、工作运势 |
| 学业 | 学业、考试、学业运势 |

---

## 核心功能

| 功能 | 说明 |
|------|------|
| 八字排盘 | 输出年柱、月柱、日柱、时柱 |
| 大运排盘 | 计算10年一大运的运势 |
| 流年排盘 | 计算每年的具体运势 |
| 流年流月 | 计算流年+流月的干支十神 |
| 流年流月流日 | 计算流年+流月+流日的干支十神 |
| 流年流月流日流时 | 计算完整四柱流年干支十神 |
| 十神分析 | 分析八字中的十神关系 |
| 五行分析 | 分析八字中的五行强弱 |

### 技术实现

- **八字计算**：使用 `lunar_python` 库，精确处理节气和闰月
- **大运方向**：修复顺逆规则（阳干男顺/阴干男逆/阳干女逆/阴干女顺）
- **十神判断**：基于日主天干，自动计算六亲关系
- **流月/流日/流时**：根据日期时间推算干支

---

## 目录结构

```
fortunetelling/
├── SKILL.md           # 本文件
├── README.md          # 说明文档
├── _meta.json         # 元数据
├── references/        # 命理知识指南
│   ├── index.md       # 书籍索引
│   ├── guide.md       # 使用指南
│   └── bazi-theory.md # 八字理论基础
├── scripts/           # 计算脚本
│   ├── lunar.py       # 阴历转公历
│   ├── bazi.py        # 八字排盘
│   └── fate.py        # 大运流年计算
└── assets/            # 排盘模板
    └── templates/      # 分析报告模板
```

---

## 快速调用

```bash
# 八字排盘
fortunetelling bazi 1990 5 15 10 --gender 男

# 阴历转公历
fortunetelling lunar 1990 4 15 10

# 运势分析
fortunetelling fate 1990 5 15 10 --gender 男 --type timing

# 构建索引
lookup! index -r /root/.openclaw/workspace/steward/skills/fortunetelling/references \
  -m /root/.openclaw/workspace/steward/skills/fortunetelling/index/manifest.json \
  -c /root/.openclaw/workspace/steward/skills/fortunetelling/index/chunks.json

# 搜索指南
lookup! search -i /root/.openclaw/workspace/steward/skills/fortunetelling/index/manifest.json <关键词>

# 查看帮助
fortunetelling -h
```

## 版本历史

| 版本 | 日期 | 更新 |
|------|------|------|
| 1.0.0 | 2026-05-20 | 初始版本 |
