# bazi 技能审查报告

> **审查版本**：SKILL.md v1.11.0（描述中混用 v1.8.0/v1.10.0/v2.0.0/v1.9.0/v2.1.0 等子版本）
> **审查日期**：2026-08-13
> **审查范围**：完整代码（scripts/*.py 4733 行）+ 10 个 references（4129 行）+ SKILL.md + README.md
> **审查方式**：只读 + 自测（`bazi --self-test` 实测 **46/46 PASS**）

---

## 总体评分（满分 10）

**[8.0 / 10]**

**结论**：技能整体可用性高，自测 46/46 全过，核心算法（节气切月、立春换年、子时换日）实现正确且与 cnlunar 对齐。前次 review-v1.8.0 报告里两个 P1（逆排大运 bug + 灾煞表错误）**均已修复**（commit `8269e588` + 后续）。但当前存在 **1 个 P0 文档缺漏**（v8.54.0 五虎遁起月法公式缺失）、**4 个 P1 一致性问题**（SKILL.md 版本号过期、CLI bug、文本输出缺信息、遗漏文件树节点）、**多 P2 改进项**。

---

## 严重问题（P0 · 必须修）

### P0-1：v8.54.0 五虎遁起月法 **公式表完全缺失**

- **位置**：`references/bazi-rules.md` §十一.3 表格第 5-6 行
- **症状**：MEMORY.md v8.54.0 明确要求"流月天干必须用五虎遁起月法"，并给出了完整口诀（甲己之年丙作首 / 乙庚之年戊为头 / 丙辛之年寻庚上 / 丁壬壬寅顺水流 / 戊癸之年何处起、甲寅之上好追求）。但 bazi-rules.md §十一.3 表格只写了"详见 v8.54.0 流月天干规则"，**没有把 5 组起月规则具体列出来**。`五鼠遁起时法`同理缺失。
- **影响**：(1) 任何新加入的协作者无法从 references 文档独立学会五虎遁；(2) 八字技能深层代码产生流月天干全部依赖 cnlunar，文档未记录 5 组口诀表 = 接口契约缺失；(3) 当未来需要切换历法库或自校验时无文档依据。
- **修复建议**：在 `references/bazi-rules.md` 新增 §十二"五虎遁起月口诀表"和 §十三"五鼠遁起时口诀表"，含：
  ```
  ## 十二、五虎遁起月口诀表（流月专用）

  | 年干 | 寅月 | 卯月 | 辰月 | 巳月 | 午月 | 未月 | 申月 | 酉月 | 戌月 | 亥月 | 子月 | 丑月 |
  |------|------|------|------|------|------|------|------|------|------|------|------|------|
  | 甲/己 | 丙寅 | 丁卯 | 戊辰 | 己巳 | 庚午 | 辛未 | 壬申 | 癸酉 | 甲戌 | 乙亥 | 丙子 | 丁丑 |
  | 乙/庚 | 戊寅 | 己卯 | 庚辰 | 辛巳 | 壬午 | 癸未 | 甲申 | 乙酉 | 丙戌 | 丁亥 | 戊子 | 己丑 |
  | 丙/辛 | 庚寅 | 辛卯 | 壬辰 | 癸巳 | 甲午 | 乙未 | 丙申 | 丁酉 | 戊戌 | 己亥 | 庚子 | 辛丑 |
  | 丁/壬 | 壬寅 | 癸卯 | 甲辰 | 乙巳 | 丙午 | 丁未 | 戊申 | 己酉 | 庚戌 | 辛亥 | 壬子 | 癸丑 |
  | 戊/癸 | 甲寅 | 乙卯 | 丙辰 | 丁巳 | 戊午 | 己未 | 庚申 | 辛酉 | 壬戌 | 癸亥 | 甲子 | 乙丑 |

  ## 十三、五鼠遁起时口诀表（流时专用）
  ...
  ```
  并在 §十一.3 表格"备注"列改为"详见 §十二 五虎遁起月口诀表 + §十三 五鼠遁起时口诀表"。

### P0-2：`bazi --liushi "YYYY-MM-DD HH:MM"` 单参数带引号时解析失败

- **位置**：`scripts/bazi_cli.py:84-99` `_parse_liushi_target()`
- **症状**：用户按 SKILL.md §调用的"流时推算"示例 `--liushi 2025-06-15 14:30`（两参数）能正常工作，但用 `--liushi "2024-02-04 22:30"`（单参数带引号）时返回 `ERROR: 无法解析 --liushi 参数`。
- **根因**：argparser 的 `nargs="+"` 行为 — 当 shell 把单引号参数传进来时，`args_value` 是 `["2024-02-04 22:30"]`（单元素 list）。`_parse_liushi_target` 走 `isinstance(args_value, str)` 分支失败 → 走 `parts = list(args_value)` = `["2024-02-04 22:30"]` → `time_part = "12:00"` 缺省 → `strptime("2024-02-04 22:30 12:00", "%Y-%m-%d %H:%M")` 失败。
- **影响**：用户在写 shell 脚本时容易踩坑（习惯性把 `YYYY-MM-DD HH:MM` 加引号）。
- **修复建议**：改 `_parse_liushi_target()`，先尝试把单个 element 内的空白分拆：

  ```python
  def _parse_liushi_target(args_value):
      if isinstance(args_value, str):
          parts = args_value.split()
      elif isinstance(args_value, list):
          parts = []
          for p in args_value:
              parts.extend(p.split())
      else:
          return None
      if not parts:
          return None
      date_part = parts[0]
      time_part = parts[1] if len(parts) > 1 else "12:00"
      try:
          return datetime.strptime(f"{date_part} {time_part}", "%Y-%m-%d %H:%M")
      except ValueError:
          return None
  ```

---

## 中等问题（P1 · 应该修）

### P1-1：SKILL.md 引用版本号严重过期

- **位置**：`SKILL.md:53`、`:54`、`:91`、`:220`、`:236` 等多处
- **症状（关键案例）**：
  - `SKILL.md:53` 引 `bazi-style.md` 为 **v3.1.0**，但该文档实际为 **v3.16.0**（按其版本历史末条 2026-08-12）
  - `SKILL.md:54` 引 `bazi-paipan.md` 为 **v1.7.0**，但该文档实际为 **v2.2.0**（按其版本历史末条 2026-08-10）
  - `README.md:34` 列 `bazi-shiju.md` 为 **v1.0.0**，但该文档实际为 **v2.0.0**（按其版本历史末条 2026-08-10）
  - README 实际统计也对不上：列 8 个 references（不含 `bazi-audit-principles.md` 和迟到日期），但目录里有 10 个 md 文件
- **影响**：协作者按 SKILL.md 指引去找文档，会拿到过期版本。
- **修复建议**：
  1. 在 SKILL.md、README.md 全文搜 `v[0-9]+\.[0-9]+\.[0-9]+` 对照各 references 元数据 `version:` 行
  2. 按 V2（核查方法 §二）规则补全：bazi-style.md → v3.16.0；bazi-paipan.md → v2.2.0；bazi-shiju.md → v2.0.0；bazi-yongshen.md 实际 v1.1.0（README 是 v1.0.0）；其它按实际 frontmatter

### P1-2：SKILL.md 描述中混用 5+ 版本号，README 文本混乱

- **位置**：`SKILL.md:4`（description 字段）
- **症状**：YAML description 一行内同时出现 `v1.8.0 三种分析并列` + `v1.10.0 流通独立` + `v1.8.0 用神融合（🆕 v2.0.0 含调候+扶抑完全移入用神）` + `v1.8.0 大运/八字反查` + `v2.0.0 大六壬排盘` + `v1.9.0 农历/四柱输入` — 5+ 旧版标识混用，HR 级别的"技能用书"读者无法快速定位当前主要版本号。
- **修复建议**：description 收敛到仅 `v1.11.0`（SKILL 自身版本）+ "v2.0.0 大六壬" + "v3.x 一段话范式（见 bazi-style.md v3.16.0）"，其他小版本演进细节挪到 SKILL.md 末尾"版本历史"章节。

### P1-3：SKILL.md 文件树缺 `bazi-audit-principles.md`

- **位置**：`SKILL.md:495-514` "## 文件结构" 代码块
- **症状**：列出 9 个 references（漏掉 `bazi-audit-principles.md`），但 `references/` 目录实际有 10 个 md 文件。README.md 的文件结构表则列了 10 个（包括该文件）。
- **影响**：协作者首次阅读 SKILL.md 会以为 audit-principles 不存在 → 错过 v1.0.0 核查原则。
- **修复建议**：在 SKILL.md 的 `references/` 代码块中加入 `bazi-audit-principles.md` 一行。

### P1-4：`_liuyun_text` 不显示 **目标日柱**（子时换日丢失关键信息）

- **位置**：`scripts/bazi.py:446-485` `_liuyun_text()`
- **症状**：SKILL.md §4c 流时推算（晚子时换日 · 决策 9）示例输出包含 `日柱同步变更为：丙辰` ——**但 `--liushi` 实际跑出来的文本不含此行**。只能从 JSON 的 `target_day_pillar` 字段看到。
- **影响**：决策 9（早子时/晚子时换日）的核心反馈信息在 `--liushi` CLI 输出中**对用户不可见**。
- **修复建议**：在 `_liuyun_text()` 函数渲染时增加（仅在 target.day != birth.day 时）：
  ```python
  birth_day_gz = f"{birth.day.gan}{birth.day.zhi}"
  target_day_gz = f"{target_year.day.gan}{target_year.day.zhi}"
  if birth_day_gz != target_day_gz:
      lines.append(f"  ⚠️ 日柱同步变更：{birth_day_gz} → {target_day_gz}（子时换日）")
  ```

### P1-5：SKILL.md 自测数写"45"但实测"46"

- **位置**：`SKILL.md:91` 和 `:518`
- **症状**：SKILL.md 描述 `45 用例（13 基础 + 10 流年/月/时 + 2 大六壬 + 17 v1.8.0 模块 + 3 v1.9.0 农历/四柱）` 和 `# 通过 45/45` ——但实际跑出来 46/46。**v1.8.0 模块实际只有 12 个**（3 zhengge + 2 shiju + 2 shensha + 2 yongshen + 3 dayun），缺口 = `zaisha`（1）和"逆排大运/反查月末边界"等用例分配错位。
- **修复建议**：在 SKILL.md:91 改为 `46 用例（13 基础 + 10 流年/月/时 + 2 大六壬 + 12 v1.8.0 模块 + 1 v1.8.0 zaisha 校验 + 7 v1.8.0 反查/组合/补全 + 3 v1.9.0 农历/四柱）`，更准确的分类。同样的，README §九版本历史最后一条仍是 v1.8.0 (2026-08-12)，但 README 自身 mtime 已 2026-08-12 21:56（晚于 SKILL.md）。

### P1-6：5 个 references 缺 frontmatter `version:` 行

- **位置**：`references/bazi-audit-principles.md`、`bazi-hehun.md`、`bazi-liutong.md`、`bazi-paipan.md`、`bazi-shiju.md`、`bazi-style.md`
- **症状**：仅 4/10 references 在文件头含 YAML `title:` + `version:` 前置元数据：
  - ✅ 有：bazi-rules.md (v1.1.0) / bazi-shensha.md (v2.1.1) / bazi-yongshen.md (v1.1.0) / bazi-zhengge.md (v1.0.1)
  - ❌ 缺：**bazi-audit-principles.md** (v1.0)、**bazi-hehun.md** (v1.3.0)、**bazi-liutong.md** (v1.0.0)、**bazi-paipan.md** (v2.2.0)、**bazi-shiju.md** (v2.0.0)、**bazi-style.md** (v3.16.0)
- **影响**：违反 `bazi-audit-principles.md` 自定的 §二 V1 规则 —— 与 audit-principles.md 自家定的核查原则不统一。
- **修复建议**：在 6 个文件顶加 YAML：
  ```yaml
  ---
  title: ...
  version: X.Y.Z
  ---
  ```
  其中 bazi-hehun.md = v1.3.0；bazi-liutong.md = v1.0.0；bazi-paipan.md = v2.2.0；bazi-shiju.md = v2.0.0；bazi-style.md = v3.16.0；bazi-audit-principles.md = v1.0（虽然 v1.0.0 header 已写，但应在 frontmatter 加版本字段以统一）。

### P1-7：`bazi-rules.md` §四立春精度说明 **与 SKILL.md 实际行为不完全对齐**

- **位置**：`references/bazi-rules.md:122` "⚠️ cnlunar 库局限"段
- **症状**：文档说"立春如果落在了'立春日'的几点几分，cnlunar 可能把整个立春日全侧子都判为同一侧"——这是简化描述，**实际 cnlunar 是"日级"边界（整日同侧）**，按实测 2000-02-04 11:32 立春 + 2000-02-04 全日都被判作己卯年，下一日 2000-02-05 才切到庚辰年。这意味着 2000-02-04 22:30 出生按 cnlunar 仍判己卯年，但**实际天文学应为庚辰年**。这段需要更精确描述"整日边界"，并补充 sxtwl 兜底案例。
- **修复建议**：在 §四增加：
  > 实测边界案例：2000-02-04 22:30 出生（立春已过近 11 小时），按 cnlunar = `己卯年戊寅月`（日级边界偏差），按 sxtwl = `庚辰年戊寅月`。
  > 涉及 `2000-02-04 11:32 ± 12h` 这个全日敏感边界的用例，强烈建议用 sxtwl 校验。

---

## 轻微问题（P2 · 可选修）

### P2-1：`KONGWANG` 6 旬首遍历可加缓存，但当前 6 次循环影响不大

- **位置**：`scripts/bazi.py:1247-1300`（空亡计算）
- **说明**：每次 `shensha()` 调用都会把 6 旬 × 10 干支遍历 60 次。当前实现正确（无 bug），但若命中空亡计算多次会浪费少量 CPU。属于不痛不痒。

### P2-2：`dayun()` 起运岁数 `days // 3` 余数未折算

- **位置**：`scripts/bazi.py:2151-2156`
- **症状**：源码注释写了"1 天≈4 个月、1 时辰≈10 天"，但实现仅 `qi_yun_age = days_diff // 3`，余数丢失。例如 38 天 → `38 // 3 = 12`，实际应 `12 岁 4 个月`。
- **影响**：精度低（约 4 个月粒度），但任务规模下可接受。CLI 输出已标注 `qi_yun_rule` 提示用户简化口径。
- **修复建议**：增强为 `years = days_diff // 3; months = (days_diff % 3) * 4`，输出 `12 岁 4 个月`，或留作可选细化。

### P2-3：`lunar_to_solar()` 闰月错误年份返回 `None` 无错误信息

- **位置**：`scripts/bazi.py:2486-2509`
- **症状**：`lunar_to_solar(2000, 4, 15, leap=True)` 返回 `None`（2000 年无闰四月），导致 `build_bazi_from_lunar_str()` 抛 `ValueError("农历日期无法转换到公历: ...")`。错误信息不直接指出"该年没有闰 X 月"。
- **修复建议**：在 lunar_to_solar 头部检查 cnlunar `getLunarMonthCN` 是否含"闰"，提前返回带清晰错误信息：
  ```python
  # 验证闰月存在性
  l_check = cnlunar.Lunar(datetime(year, 6, 15, 12, 0))
  if leap and l_check.getRunMonth(l_check.LunarMonth) != month:
      raise ValueError(f"{year} 年没有闰{['正','二','三','四','五','六','七','八','九','十','冬','腊'][month-1]}月")
  ```

### P2-4：性能优化 — `reverse_lookup()` 大范围 12×12×31×24 = 547,776 次最坏 cnlunar 调用

- **位置**：`scripts/bazi.py:2219-2300`
- **症状**：当前对每个 (年, 月, 日, 时) 都重新调用 `cnlunar.Lunar()` —— cnlunar 内部每次都做历法计算。1900-2100 范围最坏可调用 50+ 万次。实测 200 年扫描仅 0.13s（性能还 OK），但 24 小时 × 31 日 × 12 月 × 50 年 ≈ 446,400 次 cnlunar.Lunar 调用会造成延迟抖动。
- **可优化**：对单日内所有 24 小时共享 `day8Char`，只有边界小时（23:00 跨日）需要单独算。
- **修复建议**：当前性能对 200 年范围没问题，记录为待优化项，不阻塞发布。

### P2-5：`_zhengge_check_jiu_ying` 字符串拆解不完整

- **位置**：`scripts/bazi.py:752-790`
- **症状**：`_zhengge_check_jiu_ying()` 只硬编码了 6 个关键词（"印星"/"财"/"官杀"/"食伤"/"比劫"/"正印"）来拆分相神字符串，"财+官"或"食伤+正印"等多关键词组合可能被忽略。
- **修复建议**：扩展关键词字典覆盖 ZHENGGE_XIJI 中的所有 xiangshen 用词。

### P2-6：SKILL.md §4c（晚子时换日）**示例已不存在**

- **位置**：`SKILL.md:308-322`（早子时/晚子时/立春前夕示例段）
- **症状**：4c "晚子时" / 4d "立春前夕" 等示例标注的决策编号 "决策 9" 在文档其它地方找不到定义（可能是私人笔记追溯标记）。读者会困惑"决策 9"是什么。
- **修复建议**：把"决策 9"替换为更可读的"v2.0.0 决策表（子时换日）"，或在 SKILL.md 末尾加"决策编号索引表"。

### P2-7：README.md 顶部标题写 `v1.8.0` 但内容引用到 `v3.8.0-v3.16.0`

- **位置**：`README.md:1` "# 八字技能 (Bazi Skill) v1.8.0"
- **症状**：README 自身标题版本 v1.8.0，但内容拉到了 v3.16.0 风格规则。SKILL.md YAML v1.11.0 才更接近"当前主版本"。README 顶部标题应升级或加注释"README 锚定 SKILL.md v1.11.0 + 输出风格 v3.16.0 + 解读 v2.0.0+大六壬 v2.0.0"。

### P2-8：`SHENG_ME` 和 `KE_ME` 命名不规范（v10 style）

- **位置**：`scripts/bazi.py:50-52`
- **说明**：用了 `KE_ME`、`SHENG_ME` 缩写 ——略不直观，但风格统一，能理解。无需修。

### P2-9：`cnlunar.Lunar` 边界差异未文档化

- **症状**：测试用例 `2025-01-01 00:30` 标注"元旦 00:30 子时（换日后日柱）"，但 cnlunar 内部处理 早子时/晚子时存在"取次日"还是"取当日"的玄学差异（主流子平术：早子时 = 当日）。bazi skills 完全跟随 cnlunar 默认行为没有显式校验 vs 子平术主流。
- **修复建议**：在 §五 子时换日加明确备注："本技能跟随 cnlunar 默认行为（早子时/晚子时均取次日），与子平术主流'早子时=当日'有差异；如需严格依子平术，请在 CLI 提供真太阳时校正后再次跑"。

### P2-10：未实装的 5 项紫微/奇门/太乙/七政/纳甲技能**仅在 §十一.8 表格 + §十一.5 表格列出**

- **位置**：`bazi-rules.md:469-481`（§十一.8 未来扩展待建技能清单）
- **症状**：MEMORY.md 没把"5 个待建技能"列入 If-Then 规则，仅在 bazi-rules.md 文档内提到。5 个新技能对总范畴（古代天文历法术数）的扩展**没有强约束**。
- **修复建议**：把"5 个待建技能"作为 agenda 列入 MEMORY.md v8.55.x 待办项；或在 bazi-rules.md §十一.8 顶部加"commit 时同步建 workboard 卡"的提醒。

### P2-11：缺少 `references/index.md` 索引文件

- **症状**：`bazi-audit-principles.md` 自定原则 §四明确要求"新增内容必须更新入口文档引用（README / SKILL）"，但 references/ 没有标准索引文件。SKILL.md 用代码块做文件树，README.md 用表格 — 两种形式同时存在，不统一。
- **修复建议**：在 references/ 加 `index.md` 索引按职能（内容层 / 应用层 / 输出层）分类聚合，含每份文档的当前版本号和一句话简介。

### P2-12：`reports/` 目录只有旧 review-v1.8.0 没增量

- **症状**：`reports/review-v1.8.0-2026-08-10.md` 是上次的审查报告，本次完成审查后，应该追加 `review-v1.11.0-2026-08-13.md` （或本文件）落档。
- **修复建议**：把本报告保存到 `reports/` 后，下次审查可对照增量。

---

## 改进建议（按优先级）

### 建议 1：补全 v8.54.0 五虎遁/五鼠遁公式表 → **最高优先**

直接在 `bazi-rules.md` 新增 §十二（起月口诀表）+ §十三（起时口诀表）+ §十四（流月/流时推算自校验步骤"用 `bazi --liumonth YYYY-MM` 验证流月，与对照预期口诀"），并交叉引用 MEMORY.md v8.54.0。

### 建议 2：CLI 修 P0-2 之后的"流时/流月/流年 flag 全部支持单引号带空格"

同时把 `_liuyun_text` 修复为含目标日柱显示，补全 SKILL.md 中所有 `--liushi` 示例的可移植性。

### 建议 3：脚本化版本号同步

写一个 `scripts/check_versions.py` 脚本：
1. 读 SKILL.md YAML `version:` 
2. 读 10 个 references 的 frontmatter `version:` 
3. 全文 grep `v[0-9]+\.[0-9]+\.[0-9]+` 找到所有引用
4. 输出 mismatch 表 + 过期引用
5. 集成进 `bazi --self-test` 作为前置检查

后续每次发版前跑一遍，杜绝版本号漂移。

### 建议 4：补全 cases for 未覆盖边界

测试用例漏的 4 类边界场景：
1. **逆排大运起运**（前次 v1.8.0 P1 修复后没补用例）—— 加 `1998-07-16 09:00 女 → 逆排起运 2 岁`。
2. **灾煞精确值**（每 12 个日支分别断言）。
3. **大六壬"待人工判定"兜底** —— 例如 八专/伏吟/反吟触发场景。
4. **29–31 日反查边界** —— 已有 1988-07-31 / 1990-04-30 ✅ 算覆盖了。

### 建议 5：归档 `references/bazi-rules.md` §四 立春精度

按 §十一.6 表格 5（立春精确时刻）的规定，新增 `scripts/bazi_sxtwl_jieqi.py`：
- 用 sxtwl 计算 `立春精确时刻`
- 提供 `bazi --use-sxtwl-jieqi` flag（精确边界）
- 加对应测试用例（5 个立春同日不同时辰的日切对比）

### 建议 6：补 5 个待建技能（紫微/奇门/太乙/七政/纳甲）的 workboard 卡

按 MEMORY.md v5.15.x L1/L2/L3 模式立项：
- `L1`：1 个项目的"古代天文历法术数扩展"卡
- `L2`：5 张阶段卡（一个一张，对应 v2.0 大六壬已实现 + 4 个待建）
- `L3`：实际建模任务卡（按需）

### 建议 7：精简 `bazi-rules.md` §一-§十 与"内容层"内部文档交叉

按 audit-principles §一（职责边界），`bazi-rules.md` 大量内容（节气切月、立春换年、子时换日、十神查表表等）和 `bazi-shensha.md` / `bazi-zhengge.md` 等有交叉。建议：
- `bazi-rules.md` 只保留"工具表"（天干地支、五行、十神查表、节气表）
- 各应用文档（zhengge/shiju/shensha/yongshen）保留"应用口径"

### 建议 8：补五虎遁/真太阳时集成测试

按 P0-1 修复后，新增 5 个用例验证 cnlunar 五虎遁与 sxtwl 五虎遁结果一致（年份 = 戊/丙/丁 边界）。

---

## 亮点

- ✅ **核心算法忠于成熟历法库 cnlunar** — 杜绝自己写历法导致闰月/节气/子时 bug，整体 46/46 测试通过 + 真太阳时未做但已声明
- ✅ **三层模型（事实/分析/输出）职责清晰** — `bazi-paipan.md` v2.2.0 + `bazi-style.md` v3.16.0 配套完整
- ✅ **代码即文档**：每个函数都有完整 docstring 标算法依据（如 `@see references/bazi-rules.md §X`）—— 比大多数同级审稿对象做得好
- ✅ **CLI 组合分析单 JSON（v2.0.0）实现规范**：`_combined_json_output()` 保证 ≥2 模块时输出 `{chart, analysis}` 单 JSON，对外消费非常友好
- ✅ **数据/逻辑解耦**：`bazi_relations.py` 独立 relation tables，与算法模块完全解耦，按 `bazi-audit-principles.md` §一职责模型合规
- ✅ **P1 修复彻底**：上轮 review-v1.8.0 提的两个 P1（逆排大运、灾煞表）这次实测都过了，6.4 复核部分可信
- ✅ **v8.55.0 §十一 范畴定位** 已加入 bazi-rules.md（v1.1.0, 2026-08-13），把"五虎遁/五鼠遁/真太阳时/五行纳音"等都列在硬约束表，与 MEMORY.md v8.47.0 流派归属对齐
- ✅ **CLI 全局入口按 MEMORY.md v8.49.0 部署规范**:`/usr/local/bin/bazi → ~/.openclaw/workspace/steward/.agents/skills/bazi/scripts/bazi`，路径正确
- ✅ **46/46 自测全过**，覆盖 8 类边界场景（立春换年/子时换日/闰月/早子时/晚子时/立春前夕/节气前后/大运起运）
- ✅ **大六壬 v2.0.0 在声明边界内达标**：天地盘/四课/三传 4 宗门（贼克/比用/涉害/遥克）正确实现；简化项目（涉害取首位、末传=上神占位）已显式声明

---

## 与规范对齐度

| 规范 | 状态 | 备注 |
|------|------|------|
| **MEMORY.md v8.55.0 §十一 古代天文历法术数范畴规则** | ⚠️ **部分** | bazi-rules.md §十一已写入 v1.1.0 (2026-08-13)，但**五虎遁/五鼠遁公式表本身缺失**（仅引用 v8.54.0）—— P0-1 |
| **v8.54.0 五虎遁起月法** | ❌ **缺实现 + 缺文档** | 代码正确（依赖 cnlunar 的五虎遁规则），但**bazi-rules.md 没有口诀表** —— P0-1 |
| **v8.49.0 skill 部署路径** | ✅ | `.agents/skills/bazi/` 部署，CLI symlink 到位；不存在 `/root/.openclaw/skills/bazi` —— 严格合规 |
| **v5.15.x workboard L1/L2/L3 模式** | — | 本次审查未涉及派发流程；前次 review-v1.8.0 涉及，独立 |
| **v8.47.0 流派归属** | ✅ | bazi-paipan.md §一明示"基于格局分析的传统命理现代化"，与 MEMORY.md 完全一致 |
| **MEMORY.md `技能 CLI 必须有全局入口`** | ✅ | `/usr/local/bin/bazi` symlink → `scripts/bazi` → `scripts/bazi_cli.py` —— 标准三段式 |
| **bazi-audit-principles.md §一 职责三层模型**（自定） | ✅ | 内容层(bazi-rules/shensha/zhengge/shiju/yongshen) + 应用层(paipan/hehun) + 输出层(style) — 完全合规 |
| **bazi-audit-principles.md §二 V1-V4 版本一致性** | ❌ **违反** | 6/10 references 缺 frontmatter；SKILL.md/README.md 引用版本号过期严重 —— P1-1, P1-6 |
| **bazi-audit-principles.md §三 P1-P4 流程一致性** | ⚠️ **部分** | 流程编号未跳变；SKILL.md description 内多版本号混用，描述 v1.11.0 但描述字段列出 5+ 旧版号 —— P1-2 |
| **bazi-audit-principles.md §四 R1-R4 引用完整性** | ⚠️ **部分** | SKILL.md 文件树漏 bazi-audit-principles.md —— P1-3 |
| **bazi-audit-principles.md §五 N1-N4 残留与边界** | ✅ | 无旧文件名残留（"明牌实证派"改名已统一到"基于格局分析的传统命理现代化"） |

---

## 综合结论

- **是否可交付**：⚠️ **P0-1 (五虎遁公式表缺失) + P0-2 (CLI 单引号解析) 必修后即发 v1.12.0**；P1 全部建议在同次发版合并；P2 可下版本处理。
- **核心质量**：正面 — 46/46 测试覆盖 8 大类边界，前次 P1 全修了。
- **文档质量**：负面 — 版本号体系混乱 + 1 个 P0 缺漏需补。
- **代码质量**：正面 — 模块解耦好、docstring 完整、测试覆盖足。

---

## 审查元数据

- 审查文件数：17 个（含 10 个 references + 4 个 scripts + SKILL.md + README.md + test_cases.json）
- 代码总行数：4733 行（scripts）+ 4129 行（references）+ 535 行（SKILL.md）+ 201 行（README.md）= ~9,600 行
- 自测结果：**46/46 PASS**
- 实际耗时（reviewer 子代理运行约）：< 30 分钟
- 后续建议：在 root commit 上加 `BaziReviewerSubagent` tag 标明已完成审查

---

*审查人：reviewer 子代理（重派）*
*输出时间：2026-08-13 23:22 GMT+8*
*不要修改任何文件 — 本报告由大管家决定是否落档 reports/* (建议落档以备增量对照)*
