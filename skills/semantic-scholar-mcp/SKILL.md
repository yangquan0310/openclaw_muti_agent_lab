# Semantic Scholar MCP Skill

使用 Semantic Scholar API 进行学术论文搜索和检索，符合 Model Context Protocol 标准。

## 功能说明

- **论文搜索**：根据关键词搜索相关学术论文
- **论文详情**：获取特定论文的详细信息
- **MCP 标准接口**：支持通过 mcporter 统一调用
- **向后兼容**：保留命令行接口
- **环境变量配置**：从 `.env` 统一读取 API 密钥

## MCP 使用方式

### 1. 查看可用工具

```bash
mcporter list semantic-scholar
```

### 2. 搜索论文

```bash
mcporter call semantic-scholar.semantic_scholar_search query="photo-taking effect" limit=10
```

### 3. 获取论文详情

```bash
mcporter call semantic-scholar.semantic_scholar_get_details paper_id="CorpusID:1234567"
```

## 命令行兼容方式

### 搜索论文
```bash
python3 semantic_scholar_mcp.py search "<关键词>" [结果数量]
```

示例：
```bash
python3 semantic_scholar_mcp.py search "machine learning" 5
```

### 获取论文详情
```bash
python3 semantic_scholar_mcp.py details "<论文ID>"
```

## 参数说明

### MCP 工具参数
| 工具名 | 参数 | 说明 | 必须 |
|--------|------|------|------|
| semantic_scholar_search | query | 搜索关键词 | 是 |
| | limit | 返回结果数量 | 否（默认10） |
| semantic_scholar_get_details | paper_id | Semantic Scholar 论文ID | 是 |

### 命令行参数
| 参数 | 说明 | 必须 | 默认值 |
|------|------|------|--------|
| command | 命令类型：search 或 details | 是 | - |
| query | 搜索关键词 | search命令必须 | - |
| limit | 返回结果数量 | 否 | 10 |
| paper_id | Semantic Scholar 论文 ID | details命令必须 | - |

## 环境变量

API Key 存储在环境变量中：
- `SEMANTIC_SCHOLAR_API_KEY=KpNolzKwWrMhKMZW0XHq5jBhmBfOfNg3Q0sErPdi`

文件位置：`~/.openclaw/.env`

## 依赖

- Python 3.7+
- httpx 或 requests
- MCP 客户端（mcporter）

## 配置过程与问题解决

### 初始问题
1. **原始脚本仅支持命令行**，未实现 MCP 协议标准
2. **无法通过 mcporter 调用**，`mcporter list semantic-scholar-mcp` 返回未知服务器
3. **配置文件路径错误**：脚本从 `~/.openclaw/config/mcp/semantic_scholar_config.json` 读取配置，但实际使用环境变量

### 解决方案
1. **重写脚本实现 MCP 协议**：添加 JSON-RPC 标准接口
2. **统一密钥管理**：从 `.env` 环境变量读取 `SEMANTIC_SCHOLAR_API_KEY`
3. **注册到 mcporter**：在 `~/.mcporter/mcporter.json` 中添加配置
4. **修复字段问题**：移除不支持的 `doi` 字段，改用标准字段

### 配置步骤

**1. 检查 mcporter 配置**
```json
// ~/.mcporter/mcporter.json
{
  "mcpServers": {
    "semantic-scholar": {
      "command": "python3",
      "args": ["/root/.openclaw/skills/semantic-scholar-mcp/semantic_scholar_mcp.py"]
    }
  }
}
```

**2. 验证配置**
```bash
# 查看可用工具
mcporter list semantic-scholar

# 测试搜索
mcporter call semantic-scholar.semantic_scholar_search query="photo-taking effect" limit=3
```

**3. 环境变量配置**
```bash
# ~/.openclaw/.env
SEMANTIC_SCHOLAR_API_KEY=KpNolzKwWrMhKMZW0XHq5jBhmBfOfNg3Q0sErPdi
```

## 相关资源

- Semantic Scholar 官网：https://www.semanticscholar.org/
- API 文档：https://api.semanticscholar.org/
- MCP 协议：https://spec.modelcontextprotocol.io/

## 版本历史

- **v2.0.0** (2026-04-08)：重写为 MCP 标准服务，支持 mcporter 调用
- **v1.0.0** (原始)：仅支持命令行调用，无 MCP 接口
