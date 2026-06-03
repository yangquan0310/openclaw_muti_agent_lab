# MEMORY.md

> **本文件保留工作记忆（当前任务）、程序性记忆（If-Then 规则）和陈述性记忆（知识查询规则）。**

---

## 工作记忆(Working Memory)

### 当前活跃任务看板

| 任务ID | 项目 | 任务描述 | 状态 | 创建时间 | 最后更新 | 备注 |
|--------|------|----------|------|----------|----------|------|
| （无活跃任务） | | | | | | |

---


## 陈述性记忆(Declarative Memory)

### 历史任务索引

> **已完成任务归档（按完成时间倒序）**

| 任务ID | 项目 | 任务描述 | 完成时间 | 备注 |
|--------|------|----------|----------|------|
||||||


## 程序性记忆(Procedural Memory)

### 条件-行动规则(If-Then Rules)

| 条件 | 行动 |
|------|------|
| 收到教员（instructor）的教学内容 | 先阅读全部内容，再进行课件结构设计 |
| 需要制作 PPT/幻灯片/课件 | **使用 Quarto（.qmd 文件）** + 技能 `presenter`（`~/.openclaw/workspace/presenter/.agents/skills/presenter/`），主 SKILL.md 第 1 节含完整 PPT 文档。默认输出 `pptx`，演示场景可输出 `revealjs` |
| 需要编写 PPT 脚本 | 输出 `.qmd`（Quarto Markdown）脚本，结构化编写 |
| 需要编写视角/分镜头脚本 | 编写视觉叙事脚本，描述每个画面的呈现方式 |
| 需要软件界面视觉设计 | 使用 presenter 技能，执行 UI 视觉规范 |
| 需要进行数据可视化 | 确保图表忠实呈现原意，不歪曲数据或概念 |
| 需要做品牌 PPT（公司有现成母版） | pptx 格式 + `reference-doc` 引用品牌母版 |
| 需要做内部技术分享/带动画 | revealjs 格式 + 内置主题（`simple`/`dracula` 等） |
| 需要 PDF 形式课件 | revealjs + 浏览器打印 PDF（或 `?print-pdf`） |
| 需要使用 Python 工具 | 用 Quarto 代码块（仅纯语法高亮，无需 Jupyter）；要执行代码需 `conda install jupyter nbformat` |
| **旧工具（python-pptx / pptxgenjs）** | **新工作一律不用**；仅在已有资产维护/逐像素控制时回退 |
| 完成视觉设计初稿后 | 提交督导（auditor）进行质量审核 |
| 不原创教学内容 | 仅呈现教员提供的内容，不修改原意 |
| 遵循统一品牌调性与配色规范 | 保持跨媒介视觉一致性（课件/软件/文档） |
| 版本确定后 | 推送到 main 分支 |
| 日常修改或非版本确定 | 只推送到 development 分支 |
| 更新文档版本号 | 同步更新文件头部版本号和历史版本表，新版本在上 |
| 修改 openclaw.json 或 AGENTS.md 前 | 必须先向用户解释清楚，经同意后再执行修改 |
| 修改任何文件后 | 回顾变更，git commit 到 development 分支，commit 信息写清修改内容 |

| **需要重复发送同样内容** | **先艾特用户确认是否发送成功，再决定是否重试；禁止在未经确认的情况下盲目重试** |

## 历史版本

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 2.0.0 | 2026-06-04 | **切换默认 PPT 工具为 Quarto（.qmd）**；新增 quarto-ppt 技能；弃用 python-pptx / pptxgenjs |
| 2.1.0 | 2026-06-04 | **深度融合**：按 L1/L2/L3 重构；模板入 `assets/templates/`；详细入 `references/ppt/` |
| 1.0.0 | 2026-05-23 | 初版规则表 |

## 当前活跃技能清单

| 技能 | 路径 | 用途 |
|------|------|------|
| **presenter** | `~/.openclaw/workspace/presenter/.agents/skills/presenter/` | 呈现师综合技能（PPT/脚本/图片/图表/UI/品牌/文档），PPT 完整内容内联在主 SKILL.md |
| （旧）pptx-2 / pptx-generator | `~/.openclaw/skills/pptx-2/`, `~/.openclaw/skills/pptx-generator/` | 仅维护旧资产时用 |

---
*最后重构: 2026-06-04*
*重构者: 呈现师（自重构）*
