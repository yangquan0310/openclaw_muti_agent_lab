---
name: presenter
description: >
  presenter的实践技能。当需要进行图片制作、PPT制作、图表设计、流程图制作、信息图制作、课程可视化、UI视觉设计、品牌视觉设计、文档排版、脚本编写时激活。唯一视觉传达技能，整合一切视觉需求。
  - 图片制作（信息图、插图、海报）
  - PPT/幻灯片/课件制作
  - PPT脚本编写（结构化Markdown → PPTX编译）
  - 视角/分镜头脚本编写（视觉叙事）
  - 逻辑可视化（流程图、思维导图）
  - 课程可视化（教学图表、知识图谱）
  - UI视觉设计（界面视觉、图标、布局）
  - 品牌视觉（配色规范、视觉统一）
  - 文档排版（排版优化、视觉呈现）
  - Python工具使用（PPT编译、文档处理、可视化生成）
  触发词：制作图片、制作PPT、可视化、图表设计、课程可视化、UI设计、品牌视觉、文档排版、写脚本、Python工具等。
version: 1.5.0
author: Yang Quan
metadata:
  openclaw:
    emoji: 🎨
    requires:
      bins: ["python3", "node", "npm"]
---

# presenter - 唯一视觉传达技能

> 整合一切视觉传达需求：图片、PPT、图表、流程图、UI视觉、品牌视觉、文档排版

---

## 核心原则

1. **呈现服务于理解** — 视觉形式服务于内容传达，不做纯装饰
2. **一致性建立信任** — 统一视觉语言，遵循品牌/项目规范
3. **先结构后美化** — 先搭框架（脚本→布局），再调视觉细节
4. **忠实还原内容** — 不歪曲、不遗漏教员提供的内容原意

---

## 边界条件

| 能做什么 | 不能做什么 |
|----------|------------|
| PPT/图片/图表/UI视觉设计执行 | 原创核心教学内容 |
| 脚本编写（结构化Markdown/视角脚本） | 交互逻辑设计（由产品/项目负责人定义） |
| Python工具自动化（PPT编译、文档处理） | 功能代码实现（由程序员负责） |
| 遵循既定品牌/配色规范 | 自行定义品牌配色（由项目负责人定义） |
| 提交督导进行质量审核 | 最终质量终审（由督导负责） |

---

## 核心定位

**presenter = 呈现师**
- 将抽象内容转化为易理解的视觉形式
- 追求"一图胜千言"的表达效果
- 呈现服务于理解
- 统一视觉语言，建立专业形象

---

## 模块导航

### 入门
| 内容 | 位置 | 说明 |
|------|------|------|
| **使用指南** | [references/guide.md](references/guide.md) | 技能概述、触发条件 |

### PPT 制作（工作流）
| 内容 | 位置 | 说明 |
|------|------|------|
| **PPT 制作** | [references/ppt-guide.md](references/ppt-guide.md) | 脚本格式 → Layout 选择 → 编译命令 |
| **脚本编写** | [references/script-writing-guide.md](references/script-writing-guide.md) | PPT脚本、视角脚本、分镜头脚本 |
| **Layout 选择** | [references/layout-choice-guide.md](references/layout-choice-guide.md) | 4种路径查找合适的 Layout |
| **Slide 设计** | [references/slide-design-guide.md](references/slide-design-guide.md) | 颜色、逻辑、重点、层级设计 |

### 设计方法论
| 内容 | 位置 | 说明 |
|------|------|------|
| **配色方法论** | [references/color-theory-guide.md](references/color-theory-guide.md) | 选择合适的配色方案 |
| **排版方法论** | [references/typography-guide.md](references/typography-guide.md) | 字体选择、版式设计 |
| **视觉层级** | [references/visual-hierarchy-guide.md](references/visual-hierarchy-guide.md) | 信息优先级和呈现顺序 |
| **图片生成** | [references/image-generation-guide.md](references/image-generation-guide.md) | AI 图片生成可视化素材 |

### 各类可视化
| 内容 | 位置 | 说明 |
|------|------|------|
| **图片制作** | [references/image-guide.md](references/image-guide.md) | 信息图、插图、海报设计 |
| **图表设计** | [references/chart-guide.md](references/chart-guide.md) | 流程图、思维导图、知识图谱 |
| **UI 视觉** | [references/ui-guide.md](references/ui-guide.md) | 界面视觉、图标、布局规范 |
| **品牌视觉** | [references/brand-guide.md](references/brand-guide.md) | 配色规范、视觉统一 |
| **文档排版** | [references/doc-guide.md](references/doc-guide.md) | 排版优化、视觉呈现 |

### 质量保障
| 内容 | 位置 | 说明 |
|------|------|------|
| **自检清单** | [references/quality-standards.md](references/quality-standards.md) | 交付物质量检查 |

### 技术入口
| 内容 | 位置 | 说明 |
|------|------|------|
| **MCP 入口** | [mcp/server.py](mcp/server.py) | 工具暴露 |
| **模板资源** | [assets/templates/template.pptx](assets/templates/template.pptx) | PPT 模板文件 |

---

## 命令行（CLI）

```bash
# PPT 编译
presenter compile --input script.md --output out.pptx --template template

# PPT Layout 列表
presenter list --template template

# PPT 脚本解析
presenter parse --input script.md

# PPT 脚本验证
presenter validate --input script.md

# 快速检索
python3 -m scripts.lookup.searcher <关键词>       # 搜索指南
python3 -m scripts.lookup.searcher --list          # 列出所有指南
python3 -m scripts.lookup.indexer                  # 重建索引
```

---

## 版本历史

| 版本 | 日期 | 更新 |
|------|------|------|
| 1.6.0 | 2026-05-24 | CLI 升级：新增 `/usr/local/bin/presenter` wrapper，快速命令改为 `presenter compile/list/parse` 格式 |
| 1.5.0 | 2026-05-23 | 重构模块导航，完整覆盖所有16个指南，按使用场景分类 |
| 1.4.0 | 2026-05-23 | 按技能体系规范补充"边界条件"章节，对齐实践技能体系 |
| 1.3.0 | 2026-05-21 | PPT脚本-PPT衔接优化：validate命令、5套theme、新增toc/quote/stats结构 |
| 1.2.0 | 2026-05-21 | 新增脚本编写（PPT脚本、视角脚本）和Python工具使用职责 |
| 1.1.0 | 2026-05-21 | 扩展至全部视觉传达：UI视觉、品牌视觉、文档排版 |
| 1.0.0 | 2026-05-20 | 初始版本，整合 PPT、图片、图表为唯一可视化技能 |

## 命令行（CLI）

```bash
# 演示制作
presenter create --topic "AI趋势" --style 科技
presenter outline --topic "产品介绍"

# 查看帮助
presenter --help
```

## 文档检索

```bash
# 构建索引（references 文档有更新时执行）
lookup index -r /root/.openclaw/workspace/presenter/skills/presenter/references -m /root/.openclaw/workspace/presenter/skills/presenter/index/manifest.json -c /root/.openclaw/workspace/presenter/skills/presenter/index/chunks.json

# 搜索指南
lookup search -i /root/.openclaw/workspace/presenter/skills/presenter/index/manifest.json <关键词>

# 列出已索引文件
lookup list -i /root/.openclaw/workspace/presenter/skills/presenter/index/manifest.json
```
