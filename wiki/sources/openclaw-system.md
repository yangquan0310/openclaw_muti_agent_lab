---
pageType: source
id: source.openclaw-system
createdAt: "2026-05-12T10:22:00+08:00"
updatedAt: "2026-05-12T10:22:00+08:00"
title: openclaw-system
sourceIds:
  - source.system-config
aliases:
  - OpenClaw系统目录
---

# OpenClaw 系统目录

> OpenClaw 根目录结构。
> 来源：`~/.openclaw/`

---

## 路径

```
~/.openclaw/
```

## 结构

```
~/.openclaw/
├── wiki/                  # 本 wiki 目录
│   ├── concepts/          # 概念定义
│   ├── entities/          # 实体页面
│   ├── sources/           # 来源页面
│   ├── syntheses/         # 合成分析
│   ├── reports/           # 自动生成报告
│   └── index.md           # wiki 总索引
│
├── workspace/             # Agent 工作空间
│   └── {agent_id}/        # 各 Agent 目录
│
├── extensions/            # 插件目录
│   └── agent-self-development/
│
├── config/                # 系统配置
│   └── ...
│
├── .env                   # 敏感配置（密钥、Token）
│                          # ⚠️ 绝不可暴露
│
└── ...                    # 其他系统文件
```

## 核心目录

| 目录 | 说明 |
|------|------|
| `wiki/` | 实验室知识库（本 wiki） |
| `workspace/` | Agent 工作空间 |
| `extensions/` | OpenClaw 插件 |
| `config/` | 系统配置 |
| `.env` | 敏感配置（**不可暴露**） |

---

## 相关

- [[sources/openclaw-workspace]] — Agent 工作空间

-  — Agent 初始化流程

---

*最后更新：2026-05-12*

## Related
<!-- openclaw:wiki:related:start -->
### Referenced By

- [[sources/openclaw-env|openclaw-env]]
- [[sources/openclaw-workspace|openclaw-workspace]]
<!-- openclaw:wiki:related:end -->
