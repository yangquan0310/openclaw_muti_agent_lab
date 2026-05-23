# TOOLS.md

> 大管家专属工具配置
---

## 个人存储位置

| 文件 | 存储路径 | 说明 |
|------|----------|------|
| Agent 个人记忆 | `~/.openclaw/workspace/steward/MEMORY.md` | 大管家独立维护 |
| Agent 个人技能 | `~/.openclaw/workspace/steward/skills/README.md` | 技能存储目录说明 |
| Agent 临时文件 | `~/.openclaw/workspace/steward/temp/README.md` | 临时文件存储目录说明 |
| Agent 工作记忆 | `~/.openclaw/workspace/steward/memory/` | OpenClaw 核心记忆系统 |
| 仓库默认位置 | `/root/data/disk/仓库` | 项目文件根目录 |

---

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

> 示例：`openclaw plugins install git:github.com/openclaw/plugin-github`

### 技能管理

| 命令 | 用途 |
|------|------|
| `openclaw skills check` | 检查技能目录结构 |
| `openclaw skills list` | 列出所有技能 |

### 配置管理

| 命令 | 用途 |
|------|------|
| `openclaw config get <key>` | 获取配置项（如 `openclaw config get agents.defaults.model`） |
| `openclaw config set <key> <value>` | 设置配置项 |
| `openclaw config list` | 列出所有配置 |

### 工作区命令

| 命令 | 用途 |
|------|------|
| `openclaw workspace list` | 列出工作区 |
| `openclaw update` | 更新 OpenClaw 版本 |

### 网络代理（mihomo）

> mihomo 代理服务，已配置 systemd 开机自启
> 订阅配置路径：`/etc/mihomo/config.yaml`
> 监听端口：9981（HTTP/SOCKS5 混合）

| 命令 | 用途 |
|------|------|
| `systemctl status mihomo` | 查看 mihomo 运行状态 |
| `systemctl start mihomo` | 启动 mihomo |
| `systemctl stop mihomo` | 停止 mihomo |
| `systemctl restart mihomo` | 重启 mihomo |
| `tail -f /var/log/mihomo.log` | 实时查看 mihomo 日志 |
| `curl -x http://127.0.0.1:9981 https://example.com` | 通过代理测试连通性 |

**手动重启 mihomo**（systemd 未生效时）：
```bash
pkill mihomo && nohup mihomo -d /etc/mihomo > /var/log/mihomo.log 2>&1 &
```

### 记忆与向量搜索

| 命令 | 用途 |
|------|------|
| `openclaw memory status` | 查看记忆系统状态（含 provider/dims） |
| `openclaw memory status --deep` | 深度检测（探测向量存储可用性） |
| `openclaw memory index --force --agent steward` | 强制重建向量索引 |
| `openclaw memory search "关键词"` | 命令行搜索记忆 |
| `openclaw memory promote` | 预览记忆晋升候选 |
| `openclaw memory promote --apply` | 应用记忆晋升到 MEMORY.md |
| `openclaw memory rem-harness` | 预览 REM 反思结果 |

---

*最后重构: 2026-05-23*
*重构者: 大管家*
