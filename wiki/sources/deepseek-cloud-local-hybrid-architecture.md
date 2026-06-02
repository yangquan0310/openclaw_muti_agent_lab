---
pageType: source
id: source.deepseek-cloud-local-hybrid-architecture
createdAt: "2026-06-02T13:55:00+08:00"
updatedAt: "2026-06-02T13:55:00+08:00"
title: DeepSeek - 云端大模型+本地小模型+代理框架 工程化开发工作流
sourceIds: []
aliases:
  - 大B小B模型协作
  - 混合 AI 部署
  - DeepSeek 混合架构
provenance:
  type: web
  url: https://chat.deepseek.com/share/wth27xgnr7kztgb5rf
  accessedAt: "2026-06-02T13:51:00+08:00"
  retrievalMethod: tavily_extract (advanced JS rendering)
  accessedBy: steward
---

# DeepSeek 分享 - 云端大模型 + 本地小模型 + Docker 代理框架

> **来源**：DeepSeek 公开分享链接，由 杨权 转发给大管家
> **访问方式**：tavily_extract advanced 模式（普通 web_fetch 拿不到 JS 渲染的正文）
> **可信度**：中等（模型生成的工程建议，非一手文档）

## 原始内容要点

DeepSeek 上的一次对话，主题是**"云端大模型 + 本地小模型 + Docker 代理框架"的工程化开发工作流**。对话双方似乎是用户与 DeepSeek 共同探讨：

### 核心架构

- **大B模型**（云端 API，如 GPT-4/Qwen-Plus）= 架构师，**开发期**做知识库搭建、工作流梳理
- **小B模型**（本地，Ollama 跑 7B-13B）= 执行者，**运行期**按工作流做具体子任务（分类、抽取、本地推理）
- **代理框架** = 智能路由（本地/云端调度）+ 状态管理 + 成本监控
- **Docker** = 把小模型 + 代理框架打包为一键部署

### 两阶段工作流

1. **开发期**：人工 + 大B → 输出静态知识库（SQLite/FAISS）+ 工作流定义（YAML/JSON DAG）
2. **运行期**：纯本地执行，无云端调用 —— 用户请求进入代理框架 → 匹配 DAG 节点 → 调本地小B → 出回复

### 具体例子（原文摘）

> 新工单进来 → 代理框架启动流程 → 本地小模型分类为"退款问题" → 本地小模型判断情绪为"愤怒" → 代理框架触发大B模型API："用安抚语气生成退款指引回复"
> 最终回复由大B模型生成，但两个前置预处理由本地完成，省去了两次云端调用

## 杨权转发意图

待确认（推测）：
- 探索 AI Agent 工程化的最佳实践
- 对比 OpenClaw 现有的代理框架（gateway + 多 agent 协作）有无参考价值
- 寻找"本地小模型 + 云端大模型"混部方案的可能性

## Related
<!-- openclaw:wiki:related:start -->
### Referenced By

- [[syntheses/2026-06-02-13-55-00-云端大模型-本地小模型-混合架构-工程化实践|云端大模型+本地小模型 混合架构 工程化实践]]
<!-- openclaw:wiki:related:end -->
