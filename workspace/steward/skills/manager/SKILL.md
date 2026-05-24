---
name: manager
description: >
  manager 技能的参考资料索引。
---

## 命令行（CLI）

```bash
# 构建索引（references 文档有更新时执行）
lookup index -r /root/.openclaw/workspace/steward/skills/manager/references -m /root/.openclaw/workspace/steward/skills/manager/index/manifest.json -c /root/.openclaw/workspace/steward/skills/manager/index/chunks.json

# 搜索
lookup search -i /root/.openclaw/workspace/steward/skills/manager/index/manifest.json <关键词>

# 列出已索引文件
lookup list -i /root/.openclaw/workspace/steward/skills/manager/index/manifest.json
```

## 索引文件

- manifest: `/root/.openclaw/workspace/steward/skills/manager/index/manifest.json`
- chunks: `/root/.openclaw/workspace/steward/skills/manager/index/chunks.json`

## 版本历史

| 版本 | 日期 | 更新 |
|------|------|------|
| 1.0.0 | 2026-05-24 | 初始版本 |
