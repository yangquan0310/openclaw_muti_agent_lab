# 八字技能 (Bazi Skill) v1.7.0

> **给定公历时间 → 输出完整四柱八字 + 流年 / 流月 / 流时推算 + 基于格局分析的解读框架**

---

## 一、核心能力

| # | 能力 | 说明 |
|---|---|---|
| 1 | **完整四柱** | 年柱 / 月柱 / 日柱 / 时柱 + 天干地支 + 五行 + 十神 + 藏干 |
| 2 | **节气切月** | 月柱按节气（非农历月）切 |
| 3 | **立春换年** | 年柱以立春为界（非正月初一）|
| 4 | **子时换日** | 23:00–00:59 出生 → 日柱取次日 |
| 5 | **流年 / 流月 / 流时** | 与命主日主 + 同位置柱的关系查表 |
| 6 | **三种分析并列**（v1.6.0）| 正格 + 势局 + 神煞 三层融合 |
| 7 | **用神融合**（v1.7.0 ★）| 基于正格 + 势局融合得出最终用神 |

---

## 二、文件结构

```
bazi/
├── README.md          ← 本文件（入口）
├── SKILL.md v1.7.0   ← 主技能文档（5+1 步流程）
│
├── references/         ← 8 个 reference 文档
│   ├── bazi-rules.md              [工具层]  工具规则
│   ├── bazi-zhengge.md  v1.0.1   [正格] = 骨
│   ├── bazi-shiju.md    v1.0.0   [势局] = 势
│   ├── bazi-shensha.md  v2.1.1   [神煞] = 助缘
│   ├── bazi-yongshen.md v1.0.0   [用神] = 融合产物  ★ 新
│   ├── bazi-style.md    v3.1.0   [输出风格 · 含排盘/合盘输出示例]
│   ├── bazi-paipan.md   v1.7.0   [排盘]  5+1 步流程  ★ 重命名
│   └── bazi-hehun.md    v1.3.0   [合盘]  5+1+1 步流程
│
└── scripts/            ← 5 个程序 + 1 个测试
    ├── bazi                       ← shell 入口
    ├── bazi_cli.py                ← CLI 参数解析
    ├── bazi.py                    ← 核心算法
    ├── bazi_relations.py          ← 干支关系查表
    └── test_cases.json            ← 测试用例
```

---

## 三、三层模型框架（v1.7.0 核心）

```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│      正格       │  │      势局       │  │      神煞       │
│   命局之"骨"   │  │  命局之"势"   │  │ 命局之"助缘"   │
│   (Layer 1)    │  │   (Layer 1)    │  │   (Layer 1)    │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         └──────────┐ ┌───────┘                  │
                    ↓ ↓                         │
         ┌──────────────────────────┐            │
         │  用神融合（Layer 2）    │            │
         │  （仅基于正格 + 势局）   │            │
         │  ⚠️ 神煞不进入          │            │
         └─────────┬───────────────┘            │
                   ↓                              ↓
         ┌────────────────────────────────┐
         │  五维判断（Layer 3）           │
         │  （用神 + 神煞）              │
         └────────────────────────────────┘
```

| 分析 | 文档 | 版本 | 主要用书 |
|---|---|---|---|
| **正格**（Layer 1）| `bazi-zhengge.md` | v1.0.1 | 渊海 / 三命 / 人伦 / 千里 |
| **势局**（Layer 1）| `bazi-shiju.md` | v1.0.0 | 滴天 / 子平 / 穷通 |
| **神煞**（Layer 1）| `bazi-shensha.md` | v2.1.1 | 渊海 / 三命 / 星平会海 |
| **用神**（Layer 2）★ 新 | `bazi-yongshen.md` | v1.0.0 | 渊海 / 子平 / 滴天 / 穷通 |

> **关键**：用神是**融合产物**（基于正格 + 势局），**不是第四种分析**。神煞**不进入用神判定**，但**进入五维判断**。

---

## 四、快速上手

### CLI（推荐）

```bash
# 基础排盘
bazi 1996-03-10 14:30

# 流月推算
bazi 1996-03-10 14:30 --liumonth 2026-08

# 流时推算
bazi 1996-03-10 14:30 --liushi 2026-08-08 14:30

# 完整三 flag 组合
bazi 1996-03-10 14:30 --liumonth 2026-08 --liushi 2026-08-08 14:30 --json

# 自检
bazi --self-test
```

### Python 模块

```python
from bazi import build_bazi_from_str

# 基础排盘
bz = build_bazi_from_str("1996-03-10", "14:30")
print(bz.pretty())
```

### 完整安装

```bash
# 必需
pip install cnlunar

# 可选（用于天文精确校验）
pip install sxtwl
```

---

## 五、关键文档入口

| 需求 | 看哪份文档 |
|---|---|
| **快速入门** | 本 README.md |
| **5+1 步流程摘要** | [`SKILL.md`](SKILL.md) v1.7.0 |
| **排盘技术规范** | [`references/bazi-paipan.md`](references/bazi-paipan.md) v1.7.0 |
| **合盘技术规范** | [`references/bazi-hehun.md`](references/bazi-hehun.md) v1.3.0 |
| **正格体系** | [`references/bazi-zhengge.md`](references/bazi-zhengge.md) v1.0.1 |
| **势局体系** | [`references/bazi-shiju.md`](references/bazi-shiju.md) v1.0.0 |
| **神煞体系** | [`references/bazi-shensha.md`](references/bazi-shensha.md) v2.1.1 |
| **用神体系** ★ 新 | [`references/bazi-yongshen.md`](references/bazi-yongshen.md) v1.0.0 |
| **输出风格** | [`references/bazi-style.md`](references/bazi-style.md) v3.1.0（含排盘/合盘输出示例 §六）|
| **工具层规则** | [`references/bazi-rules.md`](references/bazi-rules.md) |

---

## 六、核心立场（5 条 · 最高纲领）

[1] **每句话标依据** —— `[依据: 类别]` 标明来源
[2] **术语洁净** —— 暗合是暗合、相生是相生、合冲是合冲
[3] **用现代汉语** —— 基于工具数据 + 传统命理逻辑给**明确判断**，用大白话写
[4] **不仿古** —— 不编"古贤云"，不假托师承
[5] **综合** —— 天干地支同等看，不偏天派不偏地派

> 完整定义见 [`references/bazi-paipan.md`](references/bazi-paipan.md) §二

---

## 七、神煞核心原则（一体两面 · v2.1.0）

> **神煞从来都是一体两面的。好坏同体。**

- 每颗神煞同时具备 **阳面**（正向）+ **阴面**（负向）
- **禁止单面贴吉凶**（如"羊刃 = 大凶"）
- 吉凶取决于：激活条件 + 制化机制 + 命局组合
- 详细见 [`references/bazi-shensha.md`](references/bazi-shensha.md) §0.4

---

## 八、版本历史

| 版本 | 日期 | 关键变化 |
|---|---|---|
| v1.0.0 | 2026-07-24 | 初版（CLI + Python + 四柱排盘）|
| v1.6.0 | 2026-08-08 | 三种分析并列框架（正格 + 势局 + 神煞） + 一体两面神煞原则 |
| v3.0.0 | 2026-08-08 | README 重构（624B → 完整入口）|
| v1.7.0 | 2026-08-08 | **🆕 三层模型框架**（Layer1 三种分析 + Layer2 用神融合 + Layer3 五维）+ **bazi-yongshen.md 新建** + **bazi-single 重命名为 bazi-paipan（single → 排盘）** + 8 个 reference 文档矩阵 + SKILL.md YAML v1.7.0 同步 + README.md/SKILL.md 引用全部对齐 v1.7.0 状态 |

---

## License

MIT