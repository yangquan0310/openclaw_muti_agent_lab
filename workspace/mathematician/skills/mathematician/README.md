# Mathematician: 数学分析与统计建模技能

> 数学不说谎。数学推导是最终的真理检验。

---

## 概述

Mathematician 是实验室的数学家角色，专注于数学分析与统计建模。

## 核心能力

- **数学建模**：微分方程、优化问题、统计模型
- **统计分析**：假设检验、回归分析、时间序列
- **算法设计**：复杂度分析、数值算法
- **数值计算**：精确数值模拟和计算
- **证明验证**：数学定理和推导验证
- **数据可视化**：统计图表和数学图形

---

## 目录结构

```
mathematician/
├── SKILL.md                      # 技能导航
├── README.md                     # 本文件
├── _meta.json                    # 元数据
├── assets/templates/             # 模板文件
│   ├── report_template.md        # 分析报告模板
│   └── formula_template.md       # 公式模板
├── scripts/                      # 工具脚本
│   ├── lookup.py                 # 命令行工具索引
│   ├── calculate.py              # 数值计算工具
│   └── visualize.py              # 数据可视化工具
├── references/                   # 指南文档
│   ├── index.md                 # 索引
│   ├── guide.md                 # 使用指南
│   ├── math-tools.md            # 数学工具指南
│   └── statistics.md            # 统计分析指南
└── mcp/                         # MCP 暴露
    └── server.py                # MCP 入口
```

---

## 快速开始

1. 查看技能索引：`python3 scripts/lookup.py --list`
2. 搜索工具：`python3 scripts/lookup.py --search optimization`
3. 查看工具详情：`python3 scripts/lookup.py --info calculate`

---

## 工具使用

### 命令行工具

```bash
# 列出所有工具
python3 scripts/lookup.py --list

# 搜索相关工具
python3 scripts/lookup.py --search regression

# 查看工具帮助
python3 scripts/lookup.py --info calculate
```

### 数值计算

```bash
python3 scripts/calculate.py --help
```

### 数据可视化

```bash
python3 scripts/visualize.py --help
```

---

## 文档

- [使用指南](references/guide.md) - 详细使用说明
- [数学工具指南](references/math-tools.md) - 常用数学工具
- [统计分析指南](references/statistics.md) - 统计分析方法

---

## 版本历史

| 版本 | 日期 | 更新 |
|------|------|------|
| 1.0.0 | 2026-05-23 | 初始版本 |

---

*作者：杨权*
