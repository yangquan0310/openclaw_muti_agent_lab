---
name: "astrology"
description: "西方占星排盘+性欲/性风格/性功能占星解读（基于火星/金星/冥王星/8宫/5宫）。非医学建议。"
---

# 西方占星排盘（Western Astrology / Natal Chart）

> 给定一个公历出生时间，输出完整的西方占星星盘 + 九大行星位置 + 12 宫位 + 主要相位 + 10 大领域解读。
> 本技能是"占星"系列的基础模块，覆盖感情、事业、财富、健康、人际、学业、家庭、子女、灵性、性欲 10 大领域。

## 核心能力（10 大领域）

| # | 领域 | 核心宫位 | 核心星体 | 解读文件 |
|---|---|---|---|---|
| 1 | 感情/爱情 | 5、7、8 | 金星、火星 | love-analysis.md |
| 2 | 事业/工作 | 10、6、2 | 太阳、土星、木星 | career-analysis.md |
| 3 | 财富/金钱 | 2、8 | 木星、金星 | wealth-analysis.md |
| 4 | 健康/身体 | 1、6 | 太阳、火星、土星 | health-analysis.md |
| 5 | 人际/关系 | 7、11 | 金星、月亮 | relationship-analysis.md |
| 6 | 学业/学习 | 3、9 | 水星、木星 | study-analysis.md |
| 7 | 家庭/父母 | 4、10 | 月亮、太阳 | family-analysis.md |
| 8 | 子女/后代 | 5 | 木星 | children-analysis.md |
| 9 | 灵性/成长 | 9、12 | 木星、海王 | spirituality-analysis.md |
| 10 | 性欲/性功能 | 5、8 | 火星、冥王、金星 | sexual-analysis.md |

> 1-9 领域：**非医学、可文化/心理/学术解读**。
> 10 领域：**非医学（重点提醒）**。

## 流派归属

> **本技能归属于：现代心理占星 + 文化解读派（v0.3.0 起，与 bazi v8.48.0「用现代汉语」立场同步）**

> **核心立场（4 条）**：
> 1. **敢断 + 用现代汉语**（与 bazi v8.48.0 同源）—— 基于星象数据给明确判断，用大白话写，**不藏免责**
> 2. **心理学化**（用占星语言描述心理倾向，不替代心理评估）
> 3. **文化记录**（承认占星术在人类文化中的历史地位）
> 4. **文化相对**（尊重不同文化对性/性欲/家庭等的多元理解）

> **3 条硬底线（法律 / 伦理 / 医疗，不让步）**：
> - **不下医学诊断**（ED / PE / 激素 = 医疗诊断，不是免责）
> - **不开药 / 不治疗建议**（处方权 = 医师资格）
> - **不替代医学检查**（物理尺寸 / 激素指标 / 神经传导 = 需医学设备）
>
> **问「阴茎大小 / 是否 ED / PE」 → 100% 引导到医生。这不是藏，是真不能下。**

> **「能谈」与「不能谈」明确边界（v0.3.0 起）**：
>
> | 能谈（必须谈） | 不能谈（明确让出） |
> |---|---|
> | 性能量驱力强度（火星 / 金星 / 8 宫） | ED / PE / 激素水平诊断 |
> | 表达节奏（主动 / 被动 / 压抑-释放） | 吃药 / 治疗建议 |
> | 风格偏好（火 / 土 / 风 / 水 型） | 物理尺寸 / 生理指标 |
> | 亲密场域能量强度（7 / 8 宫） | 医学检查替代 |
> | 心理底色（占有 / 灵性 / 边界） | |

## 何时使用本技能

- 用户问"我的星座是什么 / 太阳/月亮/上升是什么"
- 用户问某领域解读（"我的事业怎么样"、"我的感情运")
- 上层算法（行运、合盘、推运）需要基础星盘
- 学术研究/文化研究/娱乐用途

## 何时 **不要** 使用

- 用户问中医/医学相关 → 用中医技能
- 用户问八字/紫微 → 用 bazi 技能
- 用户有具体的健康/性健康问题 → **引导到专业医生/性治疗师**

## 调用方式

### CLI

```bash
astrology 1990-05-15 14:30 --location "纽约"           # 完整排盘
astrology 1990-05-15 14:30 --json                       # JSON 输出
astrology 1990-05-15 14:30 --focus love career          # 聚焦 2 个领域
astrology 1990-05-15 14:30 --focus all                  # 全部 10 领域
astrology 1990-05-15 14:30 --compatibility 1992-08-22   # 合盘
astrology --self-test                                   # 跑全部测试
```

### Python

```python
from astrology import build_chart_from_str

chart = build_chart_from_str("1990-05-15", "14:30", location="纽约")
print(chart.pretty())
print(chart.profile("love"))      # 单领域
print(chart.profile("all"))       # 全领域
```

### JSON

```json
{
  "solar": "1990-05-15 14:30",
  "location": "纽约",
  "sun":   {"sign": "金牛", "degree": 24, "house": 10},
  "moon":  {"sign": "狮子", "degree": 12, "house": 1},
  "rising": "处女 8°",
  "planets": {...},
  "aspects": [...],
  "profile": {
    "love":         {"intensity": 4, "keywords": [...]},
    "career":       {...},
    "wealth":       {...},
    "health":       {...},
    "relationship": {...},
    "study":        {...},
    "family":       {...},
    "children":     {...},
    "spirituality": {...},
    "sexuality":    {...}
  }
}
```

## 输出示例

### 基础排盘

```
公历：1990-05-15 14:30
地点：纽约

太阳：金牛座 24°（10 宫）
月亮：狮子座 12°（1 宫）
上升：处女座 8°

行星位置：
  太阳 ♉ 金牛 24°    10 宫
  月亮 ♌ 狮子 12°     1 宫
  水星 ♉ 金牛 18°    10 宫
  金星 ♊ 双子 3°     11 宫
  火星 ♌ 狮子 28°     1 宫
  木星 ♋ 巨蟹 15°    11 宫
  土星 ♑ 摩羯 27°     4 宫
  天王 ♑ 摩羯 4°      4 宫
  海王 ♑ 摩羯 11°     4 宫
  冥王 ♏ 天蝎 16°     2 宫

主要相位：
  太阳 ☌ 水星（光芒型）
  火星 ☌ 月亮（情感-行动一致）
  火星 □ 土星（压抑-爆发）
  ...
```

### 10 领域解读摘要

```
1. 感情/爱情：⭐⭐⭐⭐
   - 关键词：外显、主动、戏剧性
   - 主导：金星双子 + 火星狮子
2. 事业/工作：⭐⭐⭐⭐⭐
   - 关键词：权威、领导、稳定
   - 主导：10 宫主星 + 土星摩羯
3. 财富/金钱：⭐⭐⭐
   - 关键词：稳健、保守、长期
   - 主导：2 宫主星金星
4. 健康/身体：⭐⭐⭐
   - 关键词：注意呼吸系统（仅文化参考）
   - 主导：6 宫主星土星
5. 人际/关系：⭐⭐⭐⭐
   - 关键词：魅力、外交、平衡
   - 主导：7 宫主星金星
6. 学业/学习：⭐⭐⭐⭐
   - 关键词：智识、好奇心
   - 主导：水星金牛
7. 家庭/父母：⭐⭐⭐
   - 关键词：传统、责任
   - 主导：4 宫主星月亮
8. 子女/后代：⭐⭐⭐⭐
   - 关键词：创造力、玩乐
   - 主导：5 宫主星太阳
9. 灵性/成长：⭐⭐⭐
   - 关键词：哲学、扩展
   - 主导：9 宫主星木星
10. 性欲/性功能：⭐⭐⭐⭐
    - 关键词：主动、戏剧、表演（仅文化参考）
    - 主导：火星狮子
```

## 文件结构

```
astrology/
├── SKILL.md                    # 入口（本文件）
├── references/
│   ├── astrology-rules.md      # 占星规则速查（10 领域宫位/星体）
│   ├── love-analysis.md        # 感情/爱情解读
│   ├── career-analysis.md      # 事业/工作解读
│   ├── wealth-analysis.md      # 财富/金钱解读
│   ├── health-analysis.md      # 健康/身体解读（非医学）
│   ├── relationship-analysis.md # 人际/关系解读
│   ├── study-analysis.md       # 学业/学习解读
│   ├── family-analysis.md      # 家庭/父母解读
│   ├── children-analysis.md    # 子女/后代解读
│   ├── spirituality-analysis.md # 灵性/成长解读
│   └── sexual-analysis.md      # 性欲/性功能解读（非医学）
├── scripts/
│   ├── astrology.py            # 核心算法（待 programmer 实现）
│   ├── astrology_cli.py        # CLI 入口（待 programmer 实现）
│   └── astrology               # 全局命令包装
└── test_cases.json             # 测试用例
```

## 依赖

```
pyswisseph >= 2.10   # 瑞士星历表
pytz >= 2024.1
```

## 测试

```bash
cd scripts
astrology --self-test
```

## 关联技能

- `bazi` —— 八字排盘（东方命理）
- `bazi-hehun` —— 八字合婚（东方合盘）

## v0.2.0 changelog

- ✅ 范围扩展：从"性"扩展到"全 10 维度"
- ✅ 新增 8 个 references（career/wealth/health/relationship/study/family/children/spirituality）
- ✅ 扩展 astrology-rules.md 增加 10 领域宫位/星体映射
- ✅ 完善 SKILL.md 增加 10 领域表格
- 🔄 实际 astrology.py 算法仍待 programmer 代理实现（v0.2.1 修正：算法已实装，下面描述）

## v0.2.1 changelog（2026-07-29 老板测试触发）

- ✅ **CITY_DB 扩充**：新增 21 城市（+42 条目含 Pinyin 别名）—— 山西省全部 11 地级市 + 周边高频省会 10 个
- ✅ **算法已实装**：`astrology.py` 核心算法 + `astrology_cli.py` CLI 完整可用（pyswisseph 20230604 + pytz 2026.2 实时天文计算）
- ✅ **33/33 自测全过**：覆盖 5 基础排盘 + 10 focus 模式 + 2 合盘 + 1 JSON + 其他边界用例
- ✅ **老板排盘验证**：1996-03-10 18:00 / 山西太原 / 太阳双鱼 20.1° 7宫 / 月亮天蝎 20.6° 3宫 / 上升处女 14.5°

### v0.2.1 新增城市明细

| 类别 | 城市数 | 列表 |
|---|---|---|
| 山西 | 11 | 太原 / 大同 / 阳泉 / 长治 / 晋城 / 朔州 / 晋中 / 运城 / 忻州 / 临汾 / 吕梁 |
| 周边省会 | 10 | 石家庄 / 呼和浩特 / 兰州 / 银川 / 西宁 / 贵阳 / 南宁 / 福州 / 合肥 / 南昌 |
| Pinyin 别名 | 21 | Taiyuan / Datong / Yangquan / Changzhi / Jincheng / Shuozhou / Jinzhong / Yuncheng / Xinzhou / Linfen / Lvliang / Shijiazhuang / Hohhot / Lanzhou / Yinchuan / Xining / Guiyang / Nanning / Fuzhou / Hefei / Nanchang |

### v0.2.1 调用示例（带城市名）

```bash
# 中文
astrology 1996-03-10 18:00 --location "太原"

# Pinyin 别名
astrology 1996-03-10 18:00 --location "Taiyuan"

# 详细领域
astrology 1996-03-10 18:00 --location "太原" --focus love career

# 经纬度直传（不受 CITY_DB 限制）
astrology 1996-03-10 18:00 --location "37.87,112.55,Asia/Shanghai"
```

## 待办

- [x] 实际 `astrology.py` 核心算法（v0.2.1 已实装）
- [x] `astrology_cli.py` CLI 实现（v0.2.1 已实装）
- [x] `--focus` 模式的解读模板引擎（v0.2.1 已实装，10 领域框架）
- [ ] 行运（transit）模块
- [ ] 12 宫位详细解读库
- [ ] CITY_DB 二期：补全江苏/浙江/广东/河北地级市（约 40 个高频城市）
- [ ] Pinyin 别名补全：给现有 27 个中文城市加 Pinyin（北京→Beijing、上海→Shanghai 等）

## 版权与免责

本技能仅供学术研究与文化记录使用。占星推演不构成任何人生决策建议。
**所有健康/性健康相关解读不构成医学建议**——任何健康/性问题请咨询专业医生/性治疗师。
