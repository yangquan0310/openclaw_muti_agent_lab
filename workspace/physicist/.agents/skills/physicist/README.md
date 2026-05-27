# Physicist: 物理建模与理论分析技能

> 物理理论必须符合实验。无法被实验验证的理论没有意义。

---

## 概述

Physicist 是实验室的物理学家角色，专注于物理建模与理论分析。

## 核心能力

- **物理建模**：构建描述物理现象的理论模型
- **理论分析**：严谨的数学推导和物理分析
- **公式推导**：使用 LaTeX 进行数学表达
- **交叉研究**：连接物理与数学、心理学等学科
- **模型验证**：设计实验或模拟验证理论预测
- **物理可视化**：物理图景、场分布、轨迹绘制

---

## 目录结构

```
physicist/
├── SKILL.md                      # 技能导航
├── README.md                     # 本文件
├── _meta.json                    # 元数据
├── assets/templates/             # 模板文件
│   ├── report_template.md        # 分析报告模板
│   └── formula_template.md       # 公式推导模板
├── scripts/                      # 工具脚本
│   ├── lookup.py                 # 命令行工具索引
│   ├── calculate.py              # 数值计算工具
│   └── visualize.py              # 物理可视化工具
├── references/                   # 指南文档
│   ├── index.md                 # 索引
│   ├── guide.md                 # 使用指南
│   ├── physics-tools.md         # 物理工具指南
│   └── formula.md               # 公式推导指南
└── mcp/                         # MCP 暴露
    └── server.py                # MCP 入口
```

---

## 快速开始

1. 构建索引：`python3 -m scripts.lookup.indexer`
2. 搜索指南：`python3 -m scripts.lookup.searcher <关键词>`
3. 列出文件：`python3 -m scripts.lookup.searcher --list`

---

## 工具使用

### 搜索工具

```bash
# 构建索引（首次使用或更新文档后）
python3 -m scripts.lookup.indexer

# 搜索指南
python3 -m scripts.lookup.searcher 量纲分析
python3 -m scripts.lookup.searcher 量子力学

# 列出已索引的文件
python3 -m scripts.lookup.searcher --list

# 只显示文件匹配
python3 -m scripts.lookup.searcher <关键词> --files-only
```

### 数值计算

```bash
python3 scripts/calculate.py --help
```

### 物理可视化

```bash
python3 scripts/visualize.py --help
```

---

## 文档

- [使用指南](references/guide.md) - 详细使用说明
- [物理工具指南](references/physics-tools.md) - 常用物理工具
- [公式推导指南](references/formula.md) - 物理公式推导方法

---

## 版本历史

| 版本 | 日期 | 更新 |
|------|------|------|
| 1.0.0 | 2026-05-23 | 初始版本 |

---

*作者：杨权*
