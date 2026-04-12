# scripts 文件夹说明

> 数学家的非结构化脚本存储目录

## 文件夹用途

本文件夹用于存放**非结构化 Markdown 脚本**，即：
- 纯 `.md` 格式的文档
- 不包含 `.py` 或 `.sh` 等可执行代码
- 配合 `SKILL.md` 和 `README.md` 组成完整脚本说明

## 文件夹结构

```
scripts/
└── {脚本名}/
    ├── xxx.md      # 脚本内容（Markdown格式）
    ├── SKILL.md    # 技能说明文档
    └── README.md   # 使用说明文档
```

## 与 skills 的区别

| 特性 | scripts | skills |
|------|---------|--------|
| 文件类型 | `.md` 文档 | `.py` + `.sh` 代码 |
| 结构化程度 | 非结构化 | 结构化程序 |
| 执行方式 | 阅读参考 | 直接执行 |
| 组成 | `.md` + `SKILL.md` + `README.md` | `.py` + `.sh` + `SKILL.md` + `README.md` |

## 当前内容

当前为空，等待添加非结构化 Markdown 脚本。

## 使用规范

1. 每个脚本创建一个独立子文件夹
2. 子文件夹内必须包含：`xxx.md`、`SKILL.md`、`README.md`
3. 脚本内容使用 Markdown 格式编写
4. 在 TOOLS.md 中注册脚本索引
