# SKILL.md - update_tools

## 技能元数据

| 属性 | 值 |
|------|-----|
| **技能名称** | update_tools |
| **技能类型** | 系统维护 |
| **版本** | 1.0.0 |
| **作者** | 审稿助手 (reviewer) |
| **创建时间** | 2026-04-11 |

## 触发条件

- 需要更新 TOOLS.md 时
- 每日维护任务执行时
- 项目列表发生变化时

## 输入

无直接输入，自动扫描文件系统。

## 输出

1. 更新后的 `TOOLS.md` 文件
2. 工作日志文件

## 执行方式

```bash
# 方式1：直接执行 Node.js 脚本
node skills/update_tools/update_tools.js

# 方式2：执行包装脚本
bash skills/update_tools/update_tools.sh
```

## 文件结构

```
skills/update_tools/
├── update_tools.js    # 主程序
├── update_tools.sh    # 包装脚本
├── SKILL.md          # 技能元数据
└── README.md         # 使用说明
```

## 注意事项

- 需要读取 `/root/实验室仓库/项目文件/` 目录
- 需要写入 `~/.openclaw/workspace/reviewer/TOOLS.md`
- 会自动创建日志文件到 `~/实验室仓库/日志文件/`
