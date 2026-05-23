# TOOLS.md

> 物理学家专属工具配置

---

## 个人存储位置

| 文件 | 存储路径 | 说明 |
|------|----------|------|
| Agent 个人记忆 | `~/.openclaw/workspace/physicist/MEMORY.md` | 物理学家独立维护 |
| Agent 个人技能 | `~/.openclaw/workspace/physicist/skills/` | 物理学家专属技能存储目录 |
| Agent 临时文件 | `~/.openclaw/workspace/physicist/temp/` | 临时文件存储目录 |
| Agent 工作记忆 | `~/.openclaw/workspace/physicist/memory/` | OpenClaw 核心记忆系统 |
| 仓库默认位置 | `/root/data/disk/仓库` | 项目文件根目录 |

---

## 个人技能索引

> 完整列表见: `~/.openclaw/workspace/physicist/skills/README.md`

| 技能名称 | 路径 |
|---------|------|
| （暂无个人技能） | - |

---

*最后重构: 2026-05-08*
*重构者: 系统管理员*


## 系统常用工具

| 工具 | 用途 | 常用命令 |
|------|------|----------|
| git | 版本控制 | `git add .`, `git commit -m "..."`, `git push origin development` |
| pnpm | Node.js 包管理 | `pnpm add -g <pkg>`, `pnpm list -g` |
| conda | Python 环境管理 | `conda env list`, `conda install <pkg>` |
| py311 | Python 3.11 环境 (conda) | `conda activate py311`, `python --version` |
| r-base | R 语言环境 (conda) | `conda activate r-base`, `R --version` |
| docproc | 文档处理环境 (conda) | `conda activate docproc` |

### docproc 环境模块（PDF/Word/PPT/Excel/排版）

| 模块 | 版本 | 用途 |
|------|------|------|
| mineru | 3.1.15 | PDF 解析主模块 |
| markitdown | 0.1.5 | 文档转 Markdown |
| pdfplumber | 0.11.9 | PDF 表格/文本提取 |
| pdfminer.six | 20251230 | PDF 文本提取 |
| pypdf | 6.11.0 | PDF 处理 |
| pypdfium2 | 4.30.0 | PDF 渲染 |
| pdftext | 0.6.3 | PDF 文本提取 |
| python-docx | 1.2.0 | Word 文档处理 |
| pypptx-with-oxml | 1.0.3 | PPT 处理 |
| openpyxl | 3.1.5 | Excel 处理 |
| beautifulsoup4 | 4.14.3 | HTML/XML 解析 |
| lxml | 6.1.1 | XML/HTML 处理 |
| markdown-it-py | 4.2.0 | Markdown 解析 |
| markdownify | 1.2.2 | Markdown 转换 |
| pandoc | (系统) | 文档格式转换 |
| weasyprint | (系统) | HTML 转 PDF |
| jinja2 | 3.1.6 | 模板引擎 |
| fonttools | 4.63.0 | 字体处理 |
| reportlab | 4.5.1 | PDF 生成 |
| pillow | 12.2.0 | 图像处理 |
| scikit-image | 0.25.2 | 图像处理 |
| onnxruntime | 1.23.2 | ONNX 推理 |
| nbformat | 5.10.4 | Jupyter 笔记处理 |
| jq | JSON 处理 | `jq '.' openclaw.json` |
| curl | HTTP 请求 | `curl -s https://...` |
| Vim / Nano | 文件编辑 | `vim file.md`, `nano file.md` |


## OpenClaw 常用命令

### 服务管理

| 命令 | 用途 |
|------|------|
| `openclaw status` | 查看 OpenClaw 运行状态 |
| `openclaw gateway status` | 查看 Gateway 状态 |
| `openclaw restart` | 重启 OpenClaw 服务 |
| `openclaw gateway restart` | 重启 Gateway |
| `openclaw start` | 启动服务 |
| `openclaw stop` | 停止服务 |

### 插件管理

| 命令 | 用途 |
|------|------|
| `openclaw plugins list` | 列出已安装插件 |
| `openclaw plugins install git:github.com/<owner>/<repo>` | 从 GitHub 安装插件 |
| `openclaw plugins install <plugin-name>` | 安装指定插件 |
| `openclaw plugins uninstall <plugin-name>` | 卸载插件 |
| `openclaw plugins update` | 更新插件 |

### 技能管理

| 命令 | 用途 |
|------|------|
| `openclaw skills check` | 检查技能目录结构 |
| `openclaw skills list` | 列出所有技能 |

### 配置管理

| 命令 | 用途 |
|------|------|
| `openclaw config get <key>` | 获取配置项 |
| `openclaw config set <key> <value>` | 设置配置项 |
| `openclaw config list` | 列出所有配置 |

### 工作区命令

| 命令 | 用途 |
|------|------|
| `openclaw workspace list` | 列出工作区 |
| `openclaw update` | 更新 OpenClaw 版本 |