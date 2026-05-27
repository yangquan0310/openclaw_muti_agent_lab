# 渐进式披露

> 技能架构的核心原则：让代理只在需要时加载需要的信息。

---

## 核心思想

渐进式披露（Progressive Disclosure）借鉴自 UI/UX 领域，旨在通过分阶段加载信息来解决**上下文容量有限**与**技能数量持续增长**之间的矛盾。

即使安装了 20 个技能，初始加载也仅消耗约 1000-2000 tokens；相比之下，单体式提示词会将所有内容一次性塞入上下文，造成约 90% 的浪费。

---

## 三层加载模型

### L1 · 元数据层（启动时加载）

| 项目 | 内容 |
|------|------|
| **时机** | 代理启动时，所有技能的 `name + description` 被提取并注入 System Prompt |
| **Token 消耗** | 约 50-100 tokens / 技能 |
| **内容来源** | `SKILL.md` 的 YAML frontmatter 中的 `name` 和 `description` |

```xml
<available_skills>
  <skill>
    <name>pdf-processing</name>
    <description>Extract PDF text, fill forms, merge files. Use when handling PDFs.</description>
  </skill>
</available_skills>
```

**代理此时只知道**：有哪些技能可用、每个技能大致做什么。尚未加载任何指令或资源。

---

### L2 · 指令层（触发时加载）

| 项目 | 内容 |
|------|------|
| **时机** | LLM 判断用户任务与某技能 description 匹配后，读取完整 SKILL.md body |
| **Token 消耗** | 建议 < 5000 tokens |
| **内容来源** | `SKILL.md` 的 Markdown 正文部分 |

加载方式为一次 `Read` 工具调用，而非直接注入。LLM 做决策，代理执行读取，结果作为 tool_result 返回。

**代理此时**：获得该技能的工作流程、判断框架、边界约束和执行指南。

---

### L3 · 资源层（按需加载）

| 项目 | 内容 |
|------|------|
| **时机** | L2 层的指令显式引用外部文件时 |
| **Token 消耗** | 视文件大小而定 |
| **内容来源** | `scripts/`、`references/`、`assets/` 中的文件 |

关键是**告诉代理何时加载**。例如：

> 当 API 返回非 200 状态码时，读取 `references/api-errors.md`

---

## 三层对比总览

| 层级 | 加载时机 | Token 成本 | 内容 | 加载方式 |
|------|---------|-----------|------|---------|
| **L1 元数据** | 启动时 | ~100 tokens/技能 | name + description | 注入 System Prompt |
| **L2 指令** | 触发判断后 | 建议 <5000 tokens | 完整 SKILL.md body | Read 工具调用 |
| **L3 资源** | 指令引用时 | 视文件大小 | scripts / references / assets | Read 工具调用 |

---

## 模型驱动触发（Model-driven Activation）

### 核心原则

> 技能的筛选和激活由 **LLM 自主判断**，而非关键词硬编码匹配。

- 代理不做关键词匹配来决定用哪个技能
- LLM 将"技能目录"和用户消息一起考量，自主决策
- 决策体现为一次工具调用：读取对应 SKILL.md

### description 写作对触发的影响

| 写法 | 触发效果 |
|------|---------|
| `Helps with PDFs.` | ❌ 太模糊，LLM 难以判断激活时机 |
| `Extract text and tables from PDF files. Use when the user has a PDF and wants to extract content.` | ✅ 明确动作和场景，LLM 可准确判断 |
| `当用户要求创建一个新技能时触发` | ✅ 祈使句 + 明确动作 |
| `更新技能` | ⚠️ 无宾语，依赖上下文补充 |

### 好的 description 写作要点

- 使用祈使语气：「Use this skill when...」「当用户要求...时触发」
- 聚焦用户**意图**，而非技能内部机制
- 适当「强势」，覆盖用户可能的多种表述
- 包含关键触发词，帮助 LLM 快速识别
- 说明**何时不使用**，防止误激活

---

## 对技能设计的要求

### L1 层设计原则

- `name`：简短、小写、连字符分隔，不超过 64 字符
- `description`：1-1024 字符，包含触发场景关键词，说清楚**何时用、何时不用**

### L2 层设计原则

- SKILL.md 正文控制在 500 行以内
- 结构服务于目的，不为完整而完整
- 深度内容放到 `references/`，正文只放执行必需的指令

### L3 层设计原则

- 每个 reference 文件保持聚焦（文件越小，上下文消耗越少）
- 引用路径相对于技能根目录
- 在 L2 层指令中**明确标注何时加载** L3 文件

---

## 常见错误

### L1 层错误

- `description` 过于笼统（如「帮助处理文件」）
- `description` 缺少触发场景描述，只有功能罗列
- 多个技能的 description 高度重叠

### L2 层错误

- SKILL.md 正文过长（超过 500 行），把 references 内容直接塞入
- 正文缺少判断框架，只有步骤罗列
- 不告诉代理何时加载 L3 资源

### L3 层错误

- 将应该在 L2 的内容放到 L3（代理不知道何时加载）
- 引用路径不明确（未说明相对于哪个目录）
- 深层嵌套的引用链（超过一层深度）

---

## 与 MCP Tool 的本质区别

| 维度 | MCP Tool | Agent Skill |
|------|---------|-------------|
| **本质** | 提供**能力**（做某件事） | 提供**指令**（教会怎么做） |
| **信息注入位置** | 工具定义随 tools 参数发送 | 技能目录注入 System Prompt |
| **触发结果** | 返回数据（API 响应） | 返回指令（工作流程） |
| **LLM 行为变化** | 获得新的数据源 | 获得新的行为指南 |

**强力组合**：MCP 提供调用能力（如 BigQuery），Skill 教会公司规范（如表结构、查询规范）。两者互补，缺一不可。
