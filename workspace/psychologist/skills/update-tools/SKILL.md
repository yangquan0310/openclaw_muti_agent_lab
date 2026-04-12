# SKILL.md - update-tools

## 技能信息

| 属性 | 值 |
|------|-----|
| 技能名称 | update-tools |
| 技能类型 | 文档维护 |
| 触发条件 | 需要更新TOOLS.md索引 |
| 作者 | 心理学家 |

## 功能描述

本技能用于自动更新TOOLS.md文件中的脚本索引和项目列表。

## 执行流程

1. 扫描scripts目录，生成脚本索引
2. 扫描skills目录，生成技能索引
3. 扫描项目文件目录，更新项目列表
4. 更新TOOLS.md文件

## 定时执行

建议每日凌晨执行，保持索引最新。

## 使用示例

```bash
bash update_tools.sh
```
