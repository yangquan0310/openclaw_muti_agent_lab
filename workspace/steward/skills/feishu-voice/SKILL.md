---
name: feishu-voice
description: >
  飞书原生语音消息发送技能。当用户要求「发送语音消息」「用语音回复」「语音回复」，
  或 TTS 生成的音频需要作为语音气泡发送时触发。
  支持：MP3 → OGG/Opus 转换 → 上传飞书 → 发送原生语音消息。
version: 1.0.0
author: Yang Quan
metadata:
  openclaw:
    emoji: 🔊
    requires:
      bins: [ffmpeg, curl, python3]
---

# feishu-voice（飞书语音消息发送）

> 将 TTS 或本地音频文件转换为飞书原生语音消息气泡（非文件附件）。

## 功能说明

| 功能 | 说明 |
|------|------|
| 格式转换 | MP3/WAV → OGG/Opus（ffmpeg） |
| 原生发送 | 通过飞书 `msg_type=audio` 发送语音气泡 |
| 命令行 | `python3 send_voice.py <mp3_path> [open_id]` |
| 自动化 | 支持从 OpenClaw TTS 输出自动触发 |

## 工作流程

```
MP3 → ffmpeg 转换 → OGG/Opus → 上传飞书 → 获取 file_key → 发送 audio 消息 → 语音气泡
```

## 依赖检查

```bash
# 依赖工具
which ffmpeg   # 音频格式转换
which curl     # HTTP 请求
python3 -c "import json, subprocess"  # Python 标准库
```

## 使用示例

### 命令行发送

```bash
# 基本用法
python3 scripts/send_voice.py /path/to/audio.mp3 ou_25cf20a1973aecc51f73d8e2800d7f7e

# 指定目标（默认使用老板的 open_id）
python3 scripts/send_voice.py /path/to/audio.mp3

# 查看帮助
python3 scripts/send_voice.py --help
```

### Python 调用

```python
from send_voice import send_feishu_voice

# 发送语音消息
result = send_feishu_voice(
    audio_path="/root/.openclaw/media/outbound/tts.mp3",
    open_id="ou_25cf20a1973aecc51f73d8e2800d7f7e"  # 默认：老板
)
print(result)
```

## 飞书 API 凭证

| 凭证 | 来源 | 说明 |
|------|------|------|
| app_id | `openclaw.json` → `channels.feishu.accounts.*.appId` | 应用标识 |
| app_secret | `~/.openclaw/.env` → `FEISHU_STEWARD_APP_SECRET` | 应用密钥 |
| tenant_token | 通过 `app_id + app_secret` 调用 `/auth/v3/tenant_access_token` 获取 | 临时凭证 |

## 飞书 API 端点

| 步骤 | 端点 | 方法 |
|------|------|------|
| 获取 token | `https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal` | POST |
| 上传文件 | `https://open.feishu.cn/open-apis/im/v1/files?file_type=opus` | POST |
| 发送语音 | `https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id` | POST |

## 注意事项

- 飞书语音消息格式：**OPUS in OGG**，必须用 `ffmpeg -acodec libopus -ac 1 -ar 16000` 转换
- `duration` 参数单位：**毫秒**
- `file_type=opus` 对所有音频格式都适用，不只是 .opus 文件

## 已知限制

- OpenClaw `message` 工具当前不支持 `msg_type=audio`，只能通过本技能手动调用 API
- 语音消息最长支持约 5 分钟（受限于飞书 API）

## 版本历史

| 版本 | 日期 | 更新 |
|------|------|------|
| 1.0.0 | 2026-05-23 | 初始版本，支持 MP3→OGG/Opus→飞书语音消息 |

---
*创建者：杨权*