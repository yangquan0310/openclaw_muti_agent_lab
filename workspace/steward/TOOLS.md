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
| r-base | R 语言环境 (conda) | `conda activate r-base`, `R --version` |

### 文档处理模块（conda base 环境，Python 3.13）（PDF/Word/PPT/Excel/排版）

| 模块 | 版本 | 用途 |
|------|------|------|
| mineru | 3.1.15 | PDF 解析主模块 |
| pdfminer.six | 20260107 | PDF 文本提取 |
| pypdf | 6.12.1 | PDF 处理 |
| pypdfium2 | 4.30.0 | PDF 渲染 |
| pdftext | 0.6.3 | PDF 文本提取 |
| python-docx | 1.2.0 | Word 文档处理 |
| pypptx-with-oxml | 1.0.3 | PPT 处理 |
| openpyxl | 3.1.5 | Excel 处理 |
| beautifulsoup4 | 4.14.3 | HTML/XML 解析 |
| lxml | 6.1.1 | XML/HTML 处理 |
| markdown-it-py | 4.2.0 | Markdown 解析 |
| pandoc | (系统) | 文档格式转换 |
| weasyprint | (系统) | HTML 转 PDF |
| fonttools | 4.63.0 | 字体处理 |
| reportlab | 4.5.1 | PDF 生成 |
| pillow | 12.2.0 | 图像处理 |
| scikit-image | 0.26.0 | 图像处理 |
| onnxruntime | 1.26.0 | ONNX 推理 |
| nbformat | 5.10.4 | Jupyter 笔记处理 |
| jq | JSON 处理 | `jq '.' openclaw.json` |
| curl | HTTP 请求 | `curl -s https://...` |
| Vim / Nano | 文件编辑 | `vim file.md`, `nano file.md` |

#### mineru 使用方法

> minerU 可将 PDF 转换为 Markdown，适合复杂 PDF（表格、公式、图像）解析
> base 为默认 Python 环境，直接使用 `python` 命令即可。

**基本用法**：
```bash
python -m mineru.run --pdf /path/to/file.pdf --output /path/to/output/
```

**输出**：生成 `{文件名}.md` 文件，包含解析后的 Markdown 内容

**适用场景**：学术论文、含表格/公式的复杂文档、多栏排版 PDF

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

# 发送语音消息（需先转换格式，见下方说明）
lark-cli im +messages-send --user-id ou_xxx --audio ./voice.ogg

> ⚠️ **语音消息格式要求**：飞书语音消息需要 **OPUS in OGG** 格式，不支持 MP3。使用 `ffmpeg -i input.mp3 -acodec libopus -ac 1 -ar 16000 output.ogg` 转换。
>
> **自动化脚本**：`~/.openclaw/skills/feishu-voice/scripts/send_voice.py`
> ```bash
> python3 ~/.openclaw/skills/feishu-voice/scripts/send_voice.py <mp3_path> [open_id]
> ```

---

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

## 小米 MiMo 多模态理解（音频 / 视频）

> MiMo-V2-Omni 模型支持音频理解（语音转文字/分析）和视频理解（逐帧分析）
> API 接入点：`https://token-plan-cn.xiaomimimo.com/v1`
> Provider 配置参考（openclaw.json models.providers）：

```json
"mimo": {
  "label": "MiMo",
  "baseUrl": "https://token-plan-cn.xiaomimimo.com/v1",
  "apiKey": "<your_mimo_api_key>",
  "api": "openai-chat",
  "models": ["mimo-v2-omni"]
}
```

### 语音理解（Audio Understanding）

| 项目 | 说明 |
|------|------|
| **模型** | `mimo-v2-omni` |
| **输入方式** | Base64 编码音频（`input_audio` 类型） |
| **支持格式** | WAV、MP3、FLAC、OGG |
| **计费** | 按音频时长计费，时长越长 Token 越多 |

**消息格式示例**（SDK）：
```python
from openai import OpenAI
import base64

client = OpenAI(api_key="<your_mimo_api_key>", base_url="https://token-plan-cn.xiaomimimo.com/v1")

with open("audio.wav", "rb") as f:
    audio_data = base64.b64encode(f.read()).decode()

completion = client.chat.completions.create(
    model="mimo-v2-omni",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "这段音频说了什么？"},
            {
                "type": "input_audio",
                "input_audio": {"data": audio_data, "format": "wav"}
            }
        ]
    }]
)
```

**飞书语音消息处理流程**：
1. 接收飞书语音消息（格式为 OPUS in OGG）
2. 下载到本地（`feishu_im_bot_image`，message_id + file_key）
3. 转换为 WAV：`ffmpeg -i input.ogg -acodec pcm_s16le -ar 16000 output.wav`
4. Base64 编码后通过 MiMo API 发送

### 视频理解（Video Understanding）

| 项目 | 说明 |
|------|------|
| **模型** | `mimo-v2-omni` |
| **输入方式** | 视频 URL 或 Base64 编码视频（`video_url` 类型） |
| **支持格式** | MP4（URL 或 base64） |
| **计费** | 按视频时长、分辨率、帧率计费，消耗远高于图片/文本 |

**消息格式示例 — 视频 URL**：
```python
from openai import OpenAI

client = OpenAI(api_key="<your_mimo_api_key>", base_url="https://token-plan-cn.xiaomimimo.com/v1")

completion = client.chat.completions.create(
    model="mimo-v2-omni",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "这个视频里发生了什么？"},
            {"type": "video_url", "video_url": {"url": "https://example.com/video.mp4"}}
        ]
    }]
)
```

**消息格式示例 — Base64 编码视频**：
```python
from openai import OpenAI
import base64

with open("video.mp4", "rb") as f:
    video_data = base64.b64encode(f.read()).decode()

completion = client.chat.completions.create(
    model="mimo-v2-omni",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "描述这个视频中发生了什么"},
            {"type": "video_url", "video_url": {"url": f"data:video/mp4;base64,{video_data}"}}
        ]
    }]
)
```

**⚠️ 成本提示**：视频 Token 消耗远高于图片/文本，长视频建议：
- 提取关键帧作为图片输入，或
- 剪辑为较短片段再分析

### 参考链接

- [语音理解文档](https://www.mimo-v2.com/zh/docs/usage-guide/multimodal/audio)
- [视频理解文档](https://www.mimo-v2.com/zh/docs/usage-guide/multimodal/video)

---

*最后重构: 2026-05-27*
*重构者: 大管家*
