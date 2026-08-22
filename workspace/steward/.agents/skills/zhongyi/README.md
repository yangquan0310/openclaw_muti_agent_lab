# zhongyi · 中医辨证技能 v1

> 给一段文本症状 → 返回八纲 + 候选证型 + 经典方剂 + 强 disclaimer。
> 32 证型 · 31 方剂 · 基于《中医诊断学》《方剂学》《伤寒论》《金匮要略》整理。
> **仅学习参考，非医疗建议。**

## 快速开始

```bash
# 1) 直接调局部 CLI
cd ~/.openclaw/workspace/steward/.agents/skills/zhongyi/scripts
./tcm diagnose --symptoms "头痛3天，怕冷，无汗，鼻塞流清涕，脉浮紧"

# 2) 全局安装（推荐）
sudo ln -sf $(pwd)/scripts/tcm /usr/local/bin/zhongyi
tcm --help
```

## 安装

无外部依赖（纯 Python 3.8+）。

```bash
# 注册全局 `tcm` 命令
sudo ln -sf /root/.openclaw/workspace/steward/.agents/skills/zhongyi/scripts/tcm /usr/local/bin/zhongyi

# 验证
which tcm
tcm version
```

可选：加入 PATH 直接用：

```bash
export PATH=$PATH:/root/.openclaw/workspace/steward/.agents/skills/zhongyi/scripts
```

## 常用命令

```bash
tcm diagnose -s "发热，咽痛，咳嗽痰黄" --json       # JSON
tcm diagnose -s "腰膝酸软，潮热盗汗，舌红少苔"        # 人类可读
tcm diagnose -s "..." --top-n 5                      # 多返回几条候选
tcm self-test                                         # 跑全部用例
tcm self-test 风寒                                     # 跑指定用例（按标题模糊）
tcm list                                              # 列全部证型
tcm list-formulas                                     # 列全部方剂
tcm version                                           # 版本与统计
```

## Python 模块用法

```python
from tcm_diagnose import TCMDiagnose
from pathlib import Path

diag = TCMDiagnose(skill_root=Path("/root/.openclaw/workspace/steward/.agents/skills/zhongyi"))
out = diag.diagnose("心悸怔忡，失眠多梦，纳少腹胀，面色萎黄，舌淡嫩脉细弱", top_n=3)
print(out["zheng_candidates"][0]["name"])   # → "心脾两虚"
print(out["formulas"][0]["name"])           # → "归脾汤（丸）"
print(out["disclaimer"]["must_acknowledge"]) # True
```

## 知识库

- `references/tcm-zheng.md` —— 32 证型（外感/心/肝/脾/肺/肾/复合/杂病）
- `references/tcm-formulas.md` —— 31 方剂（无剂量）
- `references/tcm-disclaimer.md` —— 强免责，每次输出必带

## ⚠️ 重要边界

1. **本技能不构成任何医疗建议**。临床须执业中医师面诊。
2. **不给药物剂量**。原方遵《方剂学》教材/原典；服药前必须咨询医师。
3. **急症请拨 120 / 去医院**。
4. **症状文本 ≠ 完整辨证**。中医辨证需要"望闻问切"四诊合参，文本只覆盖"问诊"。

## 版本

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0.0 | 2026-07-24 | 初版：32 证型 + 31 方剂；规则匹配；强制 disclaimer；8 用例自测 |

## 来源

- 《中医诊断学》——中国中医药出版社（"十四五"规划教材）
- 《方剂学》——中国中医药出版社（"十四五"规划教材）
- 《伤寒论》——东汉·张仲景（明·赵开美校刻本）
- 《金匮要略》——东汉·张仲景（明·赵开美校刻本）
- 部分补益 / 理气 / 化痰 / 活血化瘀方出自《太平惠民和剂局方》《景岳全书》《医林改错》《温病条辨》《小儿药证直诀》《济生方》等经典。
