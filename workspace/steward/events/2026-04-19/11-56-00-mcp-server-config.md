# 事件记忆: MCP 技能服务器配置

## 时间
2026-04-19 11:56

## 事件描述
完成 MCP 技能服务器配置，将知识库管理、Agent 自我发展、技能开发等技能包注册为 MCP 服务器。

## 涉及实体
- knowledge-manager 技能包
- agent_self_development 技能包  
- Skill-developer 技能包
- openclaw.json MCP 配置

## 操作内容

### 1. 创建 MCP 服务器

为以下技能创建了 MCP 服务器：

| 技能 | MCP 路径 | 暴露工具 |
|------|----------|----------|
| knowledge-manager | `mcp/server.py` | km_root, km_search, km_summarize, km_manage, km_synthesize |
| agent_self_development | `mcp/server.py` | asd_root, asd_metacognition, asd_working_memory, asd_assimilation |
| Skill-developer | `mcp/server.py` | skill_dev_create, skill_dev_mcp, skill_dev_extend |

### 2. 注册到 OpenClaw MCP

在 `openclaw.json` 中注册了 3 个新的 MCP 服务器：
- `knowledge-manager`
- `agent-self-development`
- `skill-developer`

### 3. 删除旧配置

- 删除了 `semantic-scholar` MCP 服务器（已被 knowledge-manager 取代）
- 删除了 `workspace-skills` 临时 MCP 服务器
- 删除了 `semantic-scholar-mcp` 技能目录

### 4. 更新文档

- 修改 `Skill-developer/SKILL.md`，添加 MCP 支持章节
- 明确区分：公共技能添加 MCP，私有技能不添加 MCP

## 结果

当前 MCP 服务器列表：
- tencent-docs
- tencent-docengine
- tencent-sheetengine
- knowledge-manager ✅
- agent-self-development ✅
- skill-developer ✅

## 相关文件路径

- `/root/.openclaw/workspace/skills/knowledge-manager/mcp/server.py`
- `/root/.openclaw/workspace/skills/agent_self_development/mcp/server.py`
- `/root/.openclaw/workspace/skills/Skill-developer/mcp/server.py`
- `/root/.openclaw/openclaw.json`
