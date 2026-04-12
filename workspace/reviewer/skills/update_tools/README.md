# update_tools 技能

## 功能描述

自动更新 TOOLS.md 文件，维护项目列表和脚本索引。

## 使用方式

```bash
node skills/update_tools/update_tools.js
```

## 文件说明

- `update_tools.js` - 主程序（Node.js）
- `update_tools.sh` - 包装脚本
- `SKILL.md` - 技能说明文档
- `README.md` - 使用说明文档

## 功能

1. 扫描实验室项目文件夹，更新项目列表
2. 从 MEMORY.md 提取脚本索引
3. 自动更新 TOOLS.md 中的项目和脚本表格
4. 生成工作日志

## 依赖

- Node.js
- 文件系统访问权限

## 作者

审稿助手 (reviewer)
