---
pageType: report
id: report.person-agent-directory
title: Person Agent Directory
status: active
updatedAt: 2026-05-12T14:07:31.761Z
---

# Person Agent Directory

> 实验室 Agent 飞书路由目录 — 记录各 Agent 的飞书 open_id，用于群聊 @mention 和私聊路由。

## Agent 路由表

| Agent | 显示名称 | 飞书 open_id | 实体页面 |
|-------|----------|-------------|----------|
| psychologist | 心理学家 | `ou_a0a0e824aa1959a64231872dce5cc775` | [entities/psychologist.md](entities/psychologist.md) |
| reviewer | 审稿助手 | `ou_1fe1fb30adbe8c90838ba3b8dbaee7f9` | [entities/reviewer.md](entities/reviewer.md) |
| writer | 写作助手 | `ou_6286830776f65067c096418e0c42bc57` | [entities/writer.md](entities/writer.md) |
| mathematician | 数学家 | `ou_0eb36c377d0f7375180335f2d57064f4` | [entities/mathematician.md](entities/mathematician.md) |
| physicist | 物理学家 | `ou_c79429d460ce49d501aafe602ed7ce54` | [entities/physicist.md](entities/physicist.md) |
| programmer | 程序员 | `ou_79c548c8fa4c886428dc9a817be2622e` | [entities/programmer.md](entities/programmer.md) |

## 使用方式

在飞书群聊中 @mention 格式：
```
<at user_id="ou_xxx">名称</at>
```

示例：
```
<at user_id="ou_a0a0e824aa1959a64231872dce5cc775">心理学家</at> 请审核这份实验设计
```

## 更新记录

| 日期 | 更新内容 |
|------|----------|
| 2026-05-12 | 初始创建，收录 6 个 Agent 的飞书 open_id |

## Generated
<!-- openclaw:wiki:person-agent-directory:start -->
- No person-like entity pages with agent cards yet.
<!-- openclaw:wiki:person-agent-directory:end -->
