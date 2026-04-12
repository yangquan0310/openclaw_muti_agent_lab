# skills 文件夹说明

> 数学家的结构化技能存储目录

## 文件夹用途

本文件夹用于存放**结构化程序技能**，即：
- 包含 `.py` 或 `.sh` 等可执行代码
- 配合 `SKILL.md` 和 `README.md` 组成完整技能说明
- 可直接被调用执行的程序

## 文件夹结构

```
skills/
└── {技能名}/
    ├── xxx.py      # Python 脚本（可选）
    ├── xxx.sh      # Shell 脚本（可选）
    ├── SKILL.md    # 技能说明文档
    └── README.md   # 使用说明文档
```

## 与 scripts 的区别

| 特性 | skills | scripts |
|------|--------|---------|
| 文件类型 | `.py` + `.sh` 代码 | `.md` 文档 |
| 结构化程度 | 结构化程序 | 非结构化 |
| 执行方式 | 直接执行 | 阅读参考 |
| 组成 | `.py` + `.sh` + `SKILL.md` + `README.md` | `.md` + `SKILL.md` + `README.md` |

## 当前技能列表

| 技能名称 | 路径 | 功能描述 |
|----------|------|----------|
| update_indexes | `skills/update_indexes/` | 自动更新 TOOLS.md 中的脚本索引和项目库 |
| 维护工作记忆 | `skills/维护工作记忆/` | 清理非 active/paused 任务，归档到事件记忆 |

## 使用规范

1. 每个技能创建一个独立子文件夹
2. 子文件夹内必须包含：`SKILL.md`、`README.md`
3. 至少包含一个可执行文件（`.py` 或 `.sh`）
4. 在 TOOLS.md 中注册技能索引
5. SKILL.md 路径用于 HEARTBEAT.md 中的定时任务引用
