# state

本目录用于存储插件运行时的状态数据，替代 `~/.openclaw/plugin-state/` 的集中式 JSON 存储。

## 设计原则

- **对象命名空间**：每个机制（metacognition / working_memory / personality）拥有独立的子目录
- **日期分片**：事件和记忆表按日期（YYYY-MM-DD）分片存储，便于归档和清理
- **纯 JSON**：状态文件为 JSON 格式，可直接读写

## 目录结构

```
state/
├── metacognition/
│   └── plans.json              # Plan 对象（runId 为键）
├── working_memory/
│   ├── sessions.json           # Session 对象（runId 为键的数组）
│   ├── events/
│   │   └── 2026-04-28.json     # Event 对象（按日聚合）
│   └── memory_tables/
│       └── 2026-04-28.json     # Archive 记录（按日聚合）
└── personality/
    ├── diary/
    │   └── 2026-04-28.md       # Diary 日记文件
    ├── belief/
    │   └── SOUL.md.patch       # Belief 更新补丁
    ├── self/
    │   └── MEMORY.md.patch     # Self 更新补丁
    ├── identity/
    │   └── IDENTITY.md.patch   # Identity 更新补丁
    └── skills/
        └── index.json          # Skills 索引
```

## 与 PluginState 的关系

| 存储位置 | 用途 |
|----------|------|
| `~/.openclaw/plugin-state/agent-self-development.json` | 旧位置（扁平 JSON，兼容保留） |
| `state/` | 新位置（按对象/日期分片，开发友好） |

迁移方式：启动时若 `state/` 存在则优先使用，否则回退到旧位置。
