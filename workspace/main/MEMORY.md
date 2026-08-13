# Long-Term Memory


## Promoted From Short-Term Memory (2026-08-14)

<!-- openclaw-memory-promotion:memory:memory/2026-08-09-1251.md:29:30 -->
- 方案 A：让所有未绑渠道默认走 steward（推荐）: "id": "steward", "name": "steward", [score=0.803 recalls=0 avg=0.620 source=memory/2026-08-09-1251.md:29-30]
<!-- openclaw-memory-promotion:memory:memory/2026-08-09-1251.md:31:31 -->
- 方案 A：让所有未绑渠道默认走 steward（推荐）: "default": true, [score=0.803 recalls=0 avg=0.620 source=memory/2026-08-09-1251.md:31-31]
<!-- openclaw-memory-promotion:memory:memory/2026-08-09-1251.md:32:32 -->
- 方案 A：让所有未绑渠道默认走 steward（推荐）: "workspace": "/root/.openclaw/workspace/steward", [score=0.803 recalls=0 avg=0.620 source=memory/2026-08-09-1251.md:32-32]
<!-- openclaw-memory-promotion:memory:memory/2026-08-09-1251.md:35:38 -->
- 方案 B：只把 lightclawbot 这个账号绑到 steward: "lightclawbot": { "accounts": { "100047136354": { "apiKey": "***", [score=0.803 recalls=0 avg=0.620 source=memory/2026-08-09-1251.md:35-38]
<!-- openclaw-memory-promotion:memory:memory/2026-08-09-1251.md:39:39 -->
- 方案 B：只把 lightclawbot 这个账号绑到 steward: "agentId": "steward" [score=0.803 recalls=0 avg=0.620 source=memory/2026-08-09-1251.md:39-39]
<!-- openclaw-memory-promotion:memory:memory/2026-08-09-1251.md:42:42 -->
- 方案 B：只把 lightclawbot 这个账号绑到 steward: "enabled": true [score=0.803 recalls=0 avg=0.620 source=memory/2026-08-09-1251.md:42-42]
<!-- openclaw-memory-promotion:memory:memory/2026-08-09-1251.md:46:46 -->
- 方案 B：只把 lightclawbot 这个账号绑到 steward: **注意**：改完要 `gateway restart` 重启，并且**这次会话是粘性的**——它已经绑死到 `agent:main` 了，不会自动迁到 steward。要在 lightclawbot 里以 steward 身份继续，得先发 `/new` 或 `/reset` 开新会话才会走新路由。 [score=0.803 recalls=0 avg=0.620 source=memory/2026-08-09-1251.md:46-46]
<!-- openclaw-memory-promotion:memory:memory/2026-08-09-1251.md:48:51 -->
- 方案 B：只把 lightclawbot 这个账号绑到 steward: 要我直接帮你改吗？哪个方案？ user: A+B assistant: 好，A+B 都上。先用 `config.patch` 加两个补丁。 assistant: raw 要的是对象，不是 JSON Patch 数组。换成分部文档： [score=0.803 recalls=0 avg=0.620 source=memory/2026-08-09-1251.md:48-51]
