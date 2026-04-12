# update_indexes 使用说明

## 简介

自动扫描工作空间中的脚本和项目，更新 TOOLS.md 中的索引表格。

## 使用方法

```bash
# 进入技能目录
cd ~/.openclaw/workspace/mathematician/skills/update_indexes

# 执行更新脚本
bash update_indexes.sh
```

## 输出

脚本会自动更新 `~/.openclaw/workspace/mathematician/TOOLS.md` 中的：
- 脚本索引表格
- 项目库表格

## 注意事项

- 执行前会自动创建备份文件
- 更新后请检查 TOOLS.md 内容是否正确
