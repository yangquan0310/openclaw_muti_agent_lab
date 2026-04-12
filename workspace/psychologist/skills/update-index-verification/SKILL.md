# SKILL.md - update-index-verification

## 技能信息

| 属性 | 值 |
|------|-----|
| 技能名称 | update-index-verification |
| 技能类型 | 数据验证 |
| 触发条件 | 需要更新索引并验证 |
| 作者 | 心理学家 |

## 功能描述

本技能用于更新项目知识库索引文件并验证数据完整性。

## 输入

- 项目路径
- index.json文件

## 输出

- 更新后的index.json
- 验证报告

## 验证内容

1. 文献ID唯一性
2. 必填字段完整性
3. 引用量数据类型
4. 年份格式正确性

## 使用示例

```bash
python update_index_with_verification.py /path/to/project
```
