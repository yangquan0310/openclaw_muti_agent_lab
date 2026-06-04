# 为什么只用 Quarto（不做 python-pptx 选型）

> 历史选型史证。2026-06-04 后**无回退路径**：`scripts/ppt/` 已全量删档，python-pptx 不再是合法选项。
>
> 此文件用于解释**为什么是这个选择**，不是"什么时候用哪个"。

---

## 一句话结论

**Quarto + .qmd + Pandoc reference-doc 覆盖 95% 的 PPT 制作需求**。剩下 5% 的逐像素控制 / 表格样式等，由 `scripts/build_brand_template.py` 和 `scripts/style_pptx_tables.py`（**纯 zipfile XML 后处理器**，**不是 python-pptx**）补完。

**没有"用 python-pptx 更合适"的合法场景**。如果有人提出，多半是工作流惯性——请重新评估。

---

## 为什么不是 python-pptx

| 维度 | Quarto (qmd) | python-pptx | 评分 |
|------|--------------|-------------|------|
| **作者友好度** | Markdown | Python API | Quarto ★★★★★ |
| **公式/代码/图表** | 原生 | 需手动 | Quarto ★★★★★ |
| **Git diff 友好** | 文本 diff | 代码 diff | Quarto ★★★★★ |
| **学习曲线** | 1 小时上手 | 1 天上手 | Quarto ★ |
| **协作者数量** | 任何会 Markdown 的人 | 会 Python 的人 | Quarto ★★★★★ |
| **跨平台** | 全平台 | 全平台 | 平 |
| **主题复用** | reference-doc 复用 PPT 母版 | 复制代码 | Quarto ★★★★★ |
| **可二次编辑** | 输出 .pptx 任何 Office 都能改 | 任何 Office 都能改 | 平 |
| **精确像素控制** | 受 Pandoc 限制 | ★★★★★ | python-pptx 胜（但本技能不需要） |
| **程序化拼装** | 模板循环够用 | ★★★★★ | python-pptx 胜（但本技能不需要） |
| **维护既有 VBA 宏** | 不支持 | 原生 | python-pptx 胜（但本技能没这个需求） |

**Quarto 输 9 维，python-pptx 输 11 维中的 3 维，且这 3 维对本技能工作流无关**。

---

## Quarto + 后处理怎么覆盖那 5%

| 需求 | Quarto 直接做 | 用 `build_brand_template.py` | 用 `style_pptx_tables.py` |
|------|--------------|------------------------------|---------------------------|
| 写内容（H2 分页、表格、代码、公式、图片）| ✅ | | |
| 改母版装饰（顶部色条 / 左侧装饰）| | ✅ 改 slide master XML | |
| 改主题色（accent1/2 → 品牌色）| | ✅ 改 theme1.xml | |
| 改 CJK 字体 | | ✅ Calibri/宋体 → Microsoft YaHei/微软雅黑 | |
| 改表格样式（teal 表头 / 隔行斑马纹 / 细边）| | | ✅ 注入 `<a:tcPr>` 到每个 cell |
| 输出 .pptx（Office 可二次编辑）| ✅ | | |
| 输出 .html（RevealJS，动画 / 投影）| ✅ | | |

**全部需求都有路径，无须回退**。

---

## 历史：为什么从 python-pptx 切到 Quarto

- **2026-05-11**：presenter 技能首次上线。PPT 生成用 python-pptx（`scripts/ppt/PptxCompiler.py`），从零拼装 XML。
- **2026-05-21**：v1.2.0 加脚本编写职责。出现"用 Markdown 写脚本 + Python 拼装 PPT"的痛点——脚本和 PPT 两份维护。
- **2026-06-04 v1.6.0**：**固化工具原则：PPT 一律用 Quarto**。`scripts/ppt/` 标 DEPRECATED。
- **2026-06-04 v1.11.0**：`scripts/ppt/` **全量删档**。理由：
  1. 没人再用——所有近期工作（ch06-ch14）都走 Quarto
  2. 维护成本 > 价值——Quarto 已经覆盖 95% 需求
  3. **杨权 2026-06-04 明确指令**："主要用 quarto 去把 md/qmd 编译为 pptx。**尽量只使用 quarto 去制作 pptx**"

---

## 后处理工具 vs python-pptx 的本质区别

| 类别 | `build_brand_template.py` / `style_pptx_tables.py` | `scripts/ppt/PptxCompiler.py`（已删） |
|------|---------------------------------------------------|--------------------------------------|
| 实现 | Python `zipfile` 直接操作 .pptx 内的 XML | `python-pptx` 库 API |
| 输入 | Quarto 已渲染的 .pptx | Markdown / JSON 脚本 |
| 输出 | 修改后的 .pptx | 从零生成的 .pptx |
| 角色 | **后处理器**（Quarto → 后处理 → 输出） | **生成器**（脚本 → 直接输出）|
| 是否 python-pptx | ❌ | ✅ |

**两者技术栈看似都用 Python，但定位完全不同**：
- 后处理 = "Quarto 输出的修补匠"（必需，因为 Quarto 有些细节做不了）
- python-pptx 生成 = "Quarto 的替代品"（已被 Quarto 替代）

**保留后处理，删除生成器** = 100% 走 Quarto 主线 + 5% 后处理补完。

---

## 例外：什么时候**真的**需要 python-pptx

如果以下需求**真的出现**，请示老板决定是否重启 python-pptx 路线：

- ⚠️ 嵌入式 VBA 宏 / COM 自动化（Quarto 不支持）
- ⚠️ 程序化拼装 200+ 张定制化幻灯片（Quarto 模板循环够用，但极端场景可能不够）
- ⚠️ 维护既有 .pptx 资产里的某段 VBA（但我们章节库 16 章全是 Quarto 生成的，没这个需求）

**截至 2026-06-04，这些需求一个都没出现**。

---

## 经验教训

> **工具锁定的代价是灵活性，但收益是可维护性**。
>
> 当一个工具覆盖 95% 需求 + 后处理覆盖剩下 5% 时，强行保留"第二个工具处理剩下的 5%"是反模式：
> - 增加学习成本（团队要会两个工具）
> - 增加维护成本（两份代码）
> - 引入不一致风险（不同章节不同工具渲出来不一样）
>
> 用 5% 的灵活性换 100% 的一致性，对长期项目（16 章统一视觉）是值得的。
