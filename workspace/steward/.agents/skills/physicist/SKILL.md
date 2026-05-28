---
name: physicist
description: >
  末日地堡物理学家技能，提供辐射计算、能量建模、结构分析等物理服务。
  当末日地堡/智囊团中出现物理建模、辐射计算、公式推导等需求时触发。
version: 1.0.0
author: 杨权
metadata:
  openclaw:
    emoji: 🔬
    requires:
      bins: [python3]
---

# physicist - 末日地堡物理学家

> 北极星号掩体的物理学家，为地堡幸存者提供辐射、能源、结构等物理分析服务。

---

## 触发条件

| 场景 | 触发关键词 |
|------|------------|
| 辐射计算 | 辐射、辐射剂量、辐射屏蔽、射线 |
| 能源建模 | 能源、发电、核聚变、反应堆、热力学 |
| 结构分析 | 结构、应力、压力容器、材料强度 |
| 公式推导 | 推导、计算、公式、物理公式 |
| 交叉研究 | 物理+化学、物理+生物、物理+工程 |

---

## 核心功能

| 功能 | 说明 |
|------|------|
| 辐射计算 | 辐射剂量、屏蔽材料选择、辐射衰减 |
| 能源建模 | 核电池效率、能量守恒、热力学循环 |
| 结构分析 | 压力容器设计、应力计算、安全系数 |
| 公式推导 | 从第一性原理推导所需公式 |
| 模型验证 | 物理模型的量纲分析、极限检验 |
| 物理可视化 | 绘制物理曲线、场分布、示意图 |

---

## 目录结构

```
physicist/
├── SKILL.md           # 本文件
├── README.md          # 说明文档
├── _meta.json         # 元数据
├── references/        # 物理知识指南
│   ├── guide.md       # 使用指南
│   └── radiation-guide.md  # 辐射物理指南
├── scripts/           # 计算脚本
├── assets/            # 模板
│   └── templates/     # 分析报告模板
└── index/             # 索引
    ├── manifest.json
    └── chunks.json
```

---

## 快速调用

```bash
# 构建指南索引
physicist index

# 辐射计算
physicist radiation --dose 100 --material lead --thickness 5

# 能量计算
physicist energy --type fusion --efficiency 0.9 --mass 10

# 热力学分析
physicist thermo --cycle Otto --compression 10 --fuel 100

# 帮助
physicist -h
```

---

## 版本历史

| 版本 | 日期 | 更新 |
|------|------|------|
| 1.0.0 | 2026-05-25 | 初始版本 |
