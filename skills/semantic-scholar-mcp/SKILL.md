# Semantic Scholar MCP Skill

使用 Semantic Scholar API 进行学术论文搜索和检索。

## 功能说明

- **论文搜索**：根据关键词搜索相关学术论文
- **论文详情**：获取特定论文的详细信息
- **格式化显示**：将搜索结果格式化为易读的 Markdown 格式

## 使用方式

### 1. 搜索论文

```bash
python3 semantic_scholar_mcp.py search "<关键词>" [结果数量]
```

示例：
```bash
python3 semantic_scholar_mcp.py search "machine learning" 5
```

### 2. 获取论文详情

```bash
python3 semantic_scholar_mcp.py details "<论文ID>"
```

## 参数说明

| 参数 | 说明 | 必须 | 默认值 |
|------|------|------|--------|
| command | 命令类型：search 或 details | 是 | - |
| query | 搜索关键词 | search命令必须 | - |
| limit | 返回结果数量 | 否 | 10 |
| paper_id | Semantic Scholar 论文 ID | details命令必须 | - |

## 配置文件

配置文件位置：`semantic_scholar_config.json`

配置项：
- `api_key`：Semantic Scholar API 密钥
- `base_url`：API 基础 URL
- `default_limit`：默认返回结果数量
- `default_fields`：默认返回字段

## 依赖

- Python 3.7+
- httpx 或 requests

## 相关资源

- Semantic Scholar 官网：https://www.semanticscholar.org/
- API 文档：https://api.semanticscholar.org/
