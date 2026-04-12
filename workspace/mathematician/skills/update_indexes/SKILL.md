# update_indexes

> 自动更新 TOOLS.md 中的脚本索引和项目库

## 功能描述

该技能用于自动维护 TOOLS.md 文件中的索引信息，包括：
- 更新个人脚本索引
- 更新个人项目库
- 保持文档结构的同步

## 使用方法

```bash
# 执行更新
bash ~/.openclaw/workspace/mathematician/skills/update_indexes/update_indexes.sh

# 或使用固定版本
bash ~/.openclaw/workspace/mathematician/skills/update_indexes/update_indexes_fixed.sh
```

## 文件说明

| 文件 | 说明 |
|------|------|
| update_indexes.sh | 主更新脚本 |
| update_indexes_fixed.sh | 修复版本 |
| SKILL.md | 技能说明文档 |
| README.md | 使用说明 |

## 触发条件

- 需要更新 TOOLS.md 索引时
- 每日维护任务执行时
