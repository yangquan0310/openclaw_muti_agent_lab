# fortunetelling技能 - 分析报告模板

本目录包含八字命理各类分析报告的模板文件。

---

## 模板列表

| 模板文件 | 用途 | 说明 |
|----------|------|------|
| bazi_template.md | 八字排盘报告 | 综合八字分析 |
| dayun_template.md | 大运分析报告 | 十年大运走势 |
| liunian_template.md | 流年分析报告 | 年度运势分析 |
| xueye_template.md | 学业运势报告 | 读书考试运势 |
| hanyin_template.md | 婚姻情感报告 | 姻缘感情分析 |
| shiye_template.md | 事业运势报告 | 工作创业运势 |

---

## 模板变量说明

### 基本信息
- `{name}` - 姓名
- `{gender}` - 性别
- `{birth_date}` - 出生日期
- `{birth_time}` - 出生时间
- `{timestamp}` - 报告生成时间

### 八字四柱
- `{year_gan}` - 年干
- `{year_zhi}` - 年支
- `{year_wuxing}` - 年柱五行
- `{month_gan}` - 月干
- `{month_zhi}` - 月支
- `{month_wuxing}` - 月柱五行
- `{day_gan}` - 日干
- `{day_zhi}` - 日支
- `{day_wuxing}` - 日柱五行
- `{hour_gan}` - 时干
- `{hour_zhi}` - 时支
- `{hour_wuxing}` - 时柱五行

### 日主分析
- `{rizhu}` - 日主天干
- `{rizhu_wuxing}` - 日主五行
- `{wood_count}` - 木的数量
- `{fire_count}` - 火的数量
- `{earth_count}` - 土的数量
- `{metal_count}` - 金的数量
- `{water_count}` - 水的数量

### 大运流年
- `{dayun_ganzhi}` - 大运干支
- `{dayun_wuxing}` - 大运五行
- `{dayun_shishen}` - 大运十神
- `{liunian_ganzhi}` - 流年干支
- `{liunian_wuxing}` - 流年五行
- `{jixiong}` - 吉凶判定

---

## 使用方式

这些模板由 `scripts/` 目录下的 Python 脚本调用，填充实际数据后输出最终报告。

---

*最后更新：2026-05-20*
