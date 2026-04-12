# 安全存储API密钥

> 大管家（Steward）脚本
> 用于安全存储API密钥到 ~/.openclaw/.env 文件

---

## 功能说明

本脚本用于安全存储各种API密钥（Zotero、Semantic Scholar、Baidu Scholar等）到统一的.env文件中，并设置正确的文件权限。

## 文件结构

```
安全存储API密钥/
├── 安全存储API密钥.md    # 脚本详细说明
├── SKILL.md              # 技能规范文档
└── README.md             # 本文件
```

## 使用方法

1. 查看 SKILL.md 了解触发条件和使用方法
2. 按照 安全存储API密钥.md 中的步骤执行

## 输入

- API密钥内容
- 服务名称（Zotero/Semantic Scholar/Baidu Scholar/其他）

## 输出

- API密钥安全存储到 ~/.openclaw/.env
- 文件权限设置为 600

---

*维护者：大管家（Steward）*
*最后更新：2026-04-12*
