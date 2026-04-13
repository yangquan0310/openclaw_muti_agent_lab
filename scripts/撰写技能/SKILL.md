---
name: 撰写技能
description: >
  创建新技能的标准操作流程，支持结构化（代码）和非结构化（脚本）两种类型技能的封装
metadata:
  openclaw:
    emoji: "🔧"
    requires:
      bins: []
---

## 文件说明

| 文件 | 功能 | 说明 |
|------|------|------|
| `撰写技能.md` | 技能SOP | 完整的技能创建流程文档，包含Step 1-5详细步骤 |
| `SKILL.md` | 技能规范 | 给AI看的技能使用说明，结构化格式便于解析 |
| `README.md` | 技能说明 | 给人类看的技能说明，自然语言描述 |

---

## 完整方法文档

### 核心功能
- 支持两种技能类型创建：结构化技能（含可执行代码）、非结构化脚本（纯Markdown流程）
- 自动生成标准文件结构，确保符合OpenClaw技能规范
- 统一SKILL.md和README.md内容，保持一致性
- 提供YAML元数据模板和文件结构模板

### 输入参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| 技能名称 | string | ✅ | 技能的唯一标识名称，英文小写，用横线分隔 |
| 技能功能描述 | string | ✅ | 详细说明技能的用途和能力 |
| 触发场景 | list | ✅ | 触发该技能的关键词或场景列表 |
| 技能类型 | string | ✅ | `structured`（结构化/含代码）或 `unstructured`（非结构化/纯脚本） |

### 输出结果
| 输出项 | 格式 | 说明 |
|--------|------|------|
| 核心技能文件 | code/Markdown | Python/Shell脚本或Markdown流程文档 |
| README.md | Markdown | 给人类阅读的技能说明文档 |
| SKILL.md | Markdown | 给AI解析的结构化技能规范文档 |

---

## 工作流示例

### 工作流1：创建结构化技能（含Python代码）
```
Step 1: 确认技能需求
  名称: semantic-scholar-search
  功能: 调用Semantic Scholar API检索学术文献
  触发: ["检索文献", "学术搜索", "Semantic Scholar检索"]
  类型: structured

Step 2: 创建文件结构
  skills/semantic-scholar-search/
  ├── semantic_scholar.py  # 核心Python脚本
  ├── README.md            # 人类说明
  └── SKILL.md             # AI规范

Step 3: 编写核心脚本
  实现API调用、参数处理、结果返回等功能

Step 4: 撰写README.md
  技能概述、功能描述、使用示例、版本历史

Step 5: 撰写SKILL.md
  YAML元数据、触发条件、执行步骤、输入输出说明
```

### 工作流2：创建非结构化脚本（纯流程）
```
Step 1: 确认技能需求
  名称: 文献检索流程
  功能: 手动文献检索的标准操作流程
  触发: ["文献检索", "检索流程", "手动检索"]
  类型: unstructured

Step 2: 创建文件结构
  scripts/文献检索流程/
  ├── 检索流程.md  # 核心SOP文档
  ├── README.md    # 人类说明
  └── SKILL.md     # AI规范

Step 3: 编写SOP文档
  详细描述检索的每一步操作、注意事项、标准模板

Step 4: 撰写README.md
  流程概述、适用场景、操作步骤说明

Step 5: 撰写SKILL.md
  YAML元数据、触发条件、执行步骤、输出说明
```

### 工作流3：快速创建最小化技能
```
Step 1: 提供基础信息（名称、描述、1个触发词）
Step 2: 自动生成标准文件结构
Step 3: 填充核心内容
Step 4: 自动生成SKILL.md和README.md模板
Step 5: 检查完整性后输出
```

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 1.0.0 | 2026-04-13 | 初始版本，包含完整的技能创建流程和模板 |
| 0.9.0 | 2026-04-12 | 新增两种技能类型支持，完善文件结构规范 |
| 0.8.0 | 2026-04-10 | 添加YAML元数据模板和README/SKILL内容区分标准 |
