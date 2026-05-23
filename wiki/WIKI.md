# Memory Wiki (全局共享)

This vault is maintained by the OpenClaw memory-wiki plugin.

- Vault mode: `isolated`
- Render mode: `native`
- Search corpus default: `wiki`
- **共享范围：所有代理（all agents）**

## Architecture
- Raw sources remain the evidence layer.
- Wiki pages are the human-readable synthesis layer.
- `.openclaw-wiki/cache/agent-digest.json` is the agent-facing compiled digest.
- **所有代理共享此知识库，任何代理的更新对所有代理可见。**

## Notes
<!-- openclaw:human:start -->
<!-- openclaw:human:end -->
