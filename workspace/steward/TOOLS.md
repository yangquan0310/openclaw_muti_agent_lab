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

## 消息发送（message）

> OpenClaw 内置渠道消息工具，通过 `message` 工具发送。支持文本、图片、文件、音视频、交互卡片等。

### 发送图片
```
{
  "action": "send",
  "target": "user:ou_xxx",
  "message": "图片说明",
  "media": "/path/image.png"
}
```

### 发送文件
```
{
  "action": "send",
  "target": "user:ou_xxx",
  "message": "文件说明",
  "attachments": [{"type": "file", "path": "/path/file.pdf"}]
}
```

### 发送音视频
```
{
  "action": "send",
  "target": "user:ou_xxx",
  "message": "语音",
  "media": "/path/audio.opus"
}
```
```
{
  "action": "send",
  "target": "user:ou_xxx",
  "message": "视频",
  "media": "/path/video.mp4"
}
```

### @提及用户
```
{
  "action": "send",
  "target": "chat:oc_xxx",
  "message": "<at user_id=\"ou_xxx\">姓名</at> 请回复",
  "text": "<at user_id=\"ou_xxx\">姓名</at> 请回复"
}
```

---

## lark-cli 常用命令

> `lark-cli` 是飞书官方 CLI 工具，命令结构：`lark-cli <command> [subcommand] [method] [options]`

### 消息发送（im）

```bash
# 发送文本消息
lark-cli im +messages-send --user-id ou_xxx --text "消息内容"

# 发送 Markdown（自动转换为 post 格式）
lark-cli im +messages-send --user-id ou_xxx --markdown $'**加粗** 和 *斜体*\n\n- 列表项'

# 发送图片
lark-cli im +messages-send --user-id ou_xxx --image ./photo.png

# 发送文件
lark-cli im +messages-send --user-id ou_xxx --file ./report.pdf

# 发送视频
lark-cli im +messages-send --user-id ou_xxx --video ./video.mp4 --video-cover ./cover.jpg

# 回复消息
lark-cli im +messages-reply --message-id om_xxx --text "回复内容"

# 搜索群聊
lark-cli im +chat-search --query "群名"

# 查看群聊消息列表
lark-cli im +chat-messages-list --chat-id oc_xxx

# 搜索消息
lark-cli im +messages-search --query "关键词"

# 下载消息中的文件
lark-cli im +messages-resources-download --message-id om_xxx --file-key file_xxx

# @提及用户
lark-cli im +messages-send --chat-id oc_xxx --text "<at user_id=\"ou_xxx\">姓名</at> 您好"

```

### 日历（calendar）

```bash
# 查看日历议程（默认今天）
lark-cli calendar +agenda

# 查看指定日期范围的日历
lark-cli calendar events instance_view \
  --params '{"start_time":"2026-05-23T00:00:00+08:00","end_time":"2026-05-24T00:00:00+08:00"}'

# 创建日程
lark-cli calendar +create \
  --summary "会议标题" \
  --start-time "2026-05-23T14:00:00+08:00" \
  --end-time "2026-05-23T15:00:00+08:00" \
  --user-ids ou_xxx

# 查询忙闲
lark-cli calendar +freebusy --user-ids ou_xxx,ou_yyy \
  --start-time "2026-05-23T00:00:00+08:00" \
  --end-time "2026-05-23T23:59:59+08:00"

# 查找会议室
lark-cli calendar +room-find \
  --start-time "2026-05-23T14:00:00+08:00" \
  --end-time "2026-05-23T15:00:00+08:00"

# 回复日程邀请
lark-cli calendar +rsvp --event-id oo_xxx --user-id ou_xxx --answer accept
```

### 通讯录（contact）

```bash
# 获取用户信息
lark-cli contact +get-user --user-id ou_xxx

# 搜索用户
lark-cli api GET /open-apis/contact/v3/users/search \
  --params '{"query":"姓名","page_size":10}'
```

### 通用 API 调用

```bash
# GET 请求
lark-cli api GET /open-apis/calendar/v4/calendars

# POST 请求
lark-cli api POST /open-apis/im/v1/messages \
  --data '{"receive_id":"ou_xxx","msg_type":"text","content":"{\"text\":\"内容\"}"}'

# 带参数查询
lark-cli api GET /open-apis/drive/v1/files \
  --params '{"page_size":20}'

# 格式化输出
lark-cli api GET /open-apis/calendar/v4/calendars --format pretty

# 自动翻页获取所有数据
lark-cli api GET /open-apis/im/v1/chats --page-all

# 试运行（不实际发送）
lark-cli api POST /open-apis/im/v1/messages --dry-run
```

### 全局参数

| 参数 | 说明 |
|------|------|
| `--as <type>` | 身份类型：`user` 或 `bot`（默认） |
| `--format <fmt>` | 输出格式：`json`（默认）、`ndjson`、`table`、`csv`、`pretty` |
| `--page-all` | 自动翻页获取所有数据 |
| `--page-size <N>` | 每页数量 |
| `--page-limit <N>` | 最大页数限制（默认 10，0 为无限制） |
| `--page-delay <MS>` | 翻页间隔毫秒数（默认 200） |
| `-o, --output <path>` | 输出文件路径（用于二进制响应） |
| `--dry-run` | 试运行，不实际发送请求 |
| `-q <expr>` | jq 表达式过滤 JSON 输出 |

### 飞书语音消息发送（feishu-voice）

> 将 TTS 生成的 MP3 转换为飞书原生语音消息气泡（非文件附件）

**脚本路径**：`~/.openclaw/workspace/steward/skills/feishu-voice/scripts/send_voice.py`

**依赖**：ffmpeg, python3 标准库（urllib, json, subprocess）

**工作流程**：
```
MP3 → ffmpeg 转换(OGG/Opus) → 上传飞书 → 获取 file_key → 发送 msg_type=audio → 语音气泡
```

**命令格式**：
```bash
python3 ~/.openclaw/workspace/steward/skills/feishu-voice/scripts/send_voice.py <mp3_path> [open_id] [--duration MS]
```

**示例**：
```bash
# 发送 TTS 生成的 MP3（自动使用老板 open_id）
python3 ~/.openclaw/workspace/steward/skills/feishu-voice/scripts/send_voice.py \
  /root/.openclaw/media/outbound/voice-1779549735396---0f659d43-a6dc-4f69-9141-48ed8846ab41.mp3

# 指定接收者
python3 ~/.openclaw/workspace/steward/skills/feishu-voice/scripts/send_voice.py \
  /path/to/audio.mp3 ou_25cf20a1973aecc51f73d8e2800d7f7e

# 指定时长
python3 ~/.openclaw/workspace/steward/skills/feishu-voice/scripts/send_voice.py \
  /path/to/audio.mp3 --duration 10000
```

**Python 调用**：
```python
import sys
sys.path.insert(0, '~/.openclaw/workspace/steward/skills/feishu-voice/scripts')
from send_voice import send_feishu_voice

result = send_feishu_voice(
    audio_path="/root/.openclaw/media/outbound/tts.mp3",
    open_id="ou_25cf20a1973aecc51f73d8e2800d7f7e"
)
```

**飞书 API 端点**：
| 步骤 | 端点 | 方法 |
|------|------|------|
| 获取 token | `https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal` | POST |
| 上传文件 | `https://open.feishu.cn/open-apis/im/v1/files?file_type=opus` | POST |
| 发送语音 | `https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id` | POST |

**注意事项**：
- 飞书要求音频格式：**OPUS in OGG**，必须用 `ffmpeg -acodec libopus -ac 1 -ar 16000` 转换
- `duration` 参数单位：**毫秒**
- 凭证自动从 `~/.openclaw/openclaw.json` 和 `~/.openclaw/.env` 读取

---

*最后重构: 2026-05-23*
*重构者: 大管家*
