# Quarto PPT vs python-pptx 对比

> 工具选型参考。SKILL.md 第 1.9 节只放评分，详细对比在此。

---

## 评分对比

| 维度 | Quarto (qmd) | python-pptx |
|------|--------------|-------------|
| **作者友好度** | ⭐⭐⭐⭐⭐ Markdown | ⭐⭐ Python API |
| **公式/代码/图表** | ⭐⭐⭐⭐⭐ 原生 | ⭐⭐ 需手动 |
| **可二次编辑** | ⭐⭐⭐（pptx）| ⭐⭐⭐⭐⭐ |
| **精确像素控制** | ⭐⭐（受限）| ⭐⭐⭐⭐⭐ |
| **自动化（数据驱动）** | ⭐⭐⭐⭐ 模板循环 | ⭐⭐⭐⭐⭐ |
| **主题复用** | ⭐⭐⭐⭐⭐ reference-doc | ⭐⭐ 复制代码 |
| **Git diff 友好** | ⭐⭐⭐⭐⭐ | ⭐ 代码 diff |
| **学习曲线** | 1 小时上手 | 1 天上手 |
| **跨平台** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **协作者数量** | ⭐⭐⭐⭐⭐ 任何会 Markdown 的人 | ⭐⭐ 会 Python 的人 |

---

## 什么时候用 Quarto

- ✅ 课程 / 培训 / 技术分享 / 答辩
- ✅ 需要"代码 + 公式 + 图"混合内容
- ✅ 内容来自 Markdown 源
- ✅ 多页、有大量重复版式
- ✅ 团队协作者不会 Python
- ✅ 想用 Git 跟踪 PPT 变更
- ✅ 想自动从数据生成图

---

## 什么时候用 python-pptx

- ❌ 需要逐像素控制（精确到 1px）
- ❌ 程序化拼装（如根据 Excel 自动生成 200 张不同内容的 PPT）
- ❌ 维护既有 .pptx 资产里嵌入的 VBA 宏
- ❌ 复杂动画/触发器（Quarto 不支持）
- ❌ 客户明确要求保留旧 .pptx 模板里某个特殊格式

---

## 决策流程

```
开始
  │
  ▼
是数据驱动的批量生成吗？
  ├─ 是 → python-pptx
  └─ 否 ↓
需要逐像素控制吗？
  ├─ 是 → python-pptx
  └─ 否 ↓
维护既有 .pptx 资产吗？
  ├─ 是 → python-pptx（继续维护）
  └─ 否 ↓
                ┌────────────────┐
                │   用 Quarto    │
                │   （默认）     │
                └────────────────┘
```

---

## 实际工作流对比

### 同一份课件：Quarto 方式

```bash
# 1. 复制模板
cp assets/templates/lesson-pptx.qmd deck.qmd

# 2. 编辑 Markdown
vim deck.qmd

# 3. 渲染
quarto render deck.qmd --to pptx

# 4. 提交
git add deck.qmd && git commit -m "update deck"
```

### 同一份课件：python-pptx 方式

```bash
# 1. 复制脚本模板
cp old-deck.py deck.py

# 2. 改 Python 代码（拼 XML）
vim deck.py

# 3. 编译
python deck.py

# 4. 提交
git add deck.py && git commit -m "update deck"
```

**Quarto 的优势**：
- 第 2 步是 Markdown（人友好）
- diff 干净（只看到内容变化，不是 XML 噪音）
- 不需要 Python 运行环境

---

## 性能对比

| 项 | Quarto | python-pptx |
|----|--------|-------------|
| 冷启动渲染 50 页 | ~3-5 秒 | ~2-3 秒 |
| 修改 1 页重渲染 | 整份重渲染（~5 秒）| 只改 1 页（~0.5 秒）|
| 依赖安装 | 1 个二进制（Quarto）| pip install python-pptx |

**Quarto 的劣势**：每次都要重渲染整份，但 Quarto 已经很快了。
