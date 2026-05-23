# TOOLS.md

> 系统管理员工具配置

---

## 存储位置

### 系统级存储

| 文件 | 存储路径 | 说明 |
|----------|----------|------|
| 主配置 | ~/.openclaw/openclaw.json | OpenClaw 主配置文件 |
| 环境变量 | ~/.openclaw/.env | API密钥和环境变量 |
| 插件目录 | ~/.openclaw/extensions/ | 插件安装位置 |
| 日志目录 | ~/.openclaw/logs/ | 系统日志 |

### 工作空间存储

| 文件 | 存储路径 | 说明 |
|----------|----------|------|
| 工作空间根 | ~/.openclaw/workspace/ | 所有代理工作空间 |
| 公共技能 | ~/.openclaw/workspace/skills/ | 共享技能 |
| 代理工作空间 | ~/.openclaw/workspace/<agent>/ | 各代理目录 |
| 仓库默认位置 | `/root/data/disk/仓库` | 项目文件根目录 |

### 成员工作空间

| 称呼 | Agent ID | 工作空间 | Agent目录 |
|------|----------|----------|-----------|
| 大管家 | Steward | ~/.openclaw/workspace/steward | ~/.openclaw/agents/steward/agent |
| 数学家 | mathematician | ~/.openclaw/workspace/mathematician | ~/.openclaw/agents/mathematician/agent |
| 物理学家 | physicist | ~/.openclaw/workspace/physicist | ~/.openclaw/agents/physicist/agent |
| 心理学家 | psychologist | ~/.openclaw/workspace/psychologist | ~/.openclaw/agents/psychologist/agent |
| 写作助手 | writer | ~/.openclaw/workspace/writer | ~/.openclaw/agents/writer/agent |
| 审稿助手 | reviewer | ~/.openclaw/workspace/reviewer | ~/.openclaw/agents/reviewer/agent |
| 教学助手 | teaching | ~/.openclaw/workspace/teaching | ~/.openclaw/agents/teaching/agent |
| 教务助手 | academicassistant | ~/.openclaw/workspace/academicassistant | ~/.openclaw/agents/academicassistant/agent |
| 学工助手 | studentaffairsassistant | ~/.openclaw/workspace/studentaffairsassistant | ~/.openclaw/agents/studentaffairsassistant/agent |

---

## 系统管理命令

### 常用 CLI 命令

| 命令 | 用途 |
|------|------|
| `openclaw status` | 查看系统状态 |
| `openclaw doctor` | 诊断系统问题 |
| `openclaw gateway restart` | 重启网关 |
| `openclaw config get` | 查看配置 |
| `openclaw config set` | 设置配置项（首选） |
| `openclaw config patch` | 修补配置（备用） |
| `openclaw plugins list` | 列出插件 |
| `openclaw hooks list` | 列出钩子 |
| `openclaw memory status` | 查看记忆状态 |

---

## 索引

### 代理工作空间索引
> 完整列表见: `~/.openclaw/workspace/`

---

*最后重构: 2026-04-26*
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