# TOOLS.md

> 心理学家专属工具配置

---

## 重要路径

| 名称 | 路径 |
|------|------|
| OpenClaw 安装路径 | `~/.openclaw` |
| 个人工作空间 | `~/.openclaw/workspace/psychologist` |
| 仓库默认位置 | `~/.openclaw/repository` |
## 系统常用工具

| 工具 | 用途 | 常用命令 |
|------|------|----------|
| git | 版本控制 | `git add .`, `git commit -m "..."`, `git push origin development` |
| pnpm | Node.js 包管理 | `pnpm add -g <pkg>`, `pnpm list -g` |
| conda | Python 环境管理 | `conda env list`, `conda install <pkg>` |
| r-base | R 语言环境 (conda) | `conda activate r-base`, `R --version` |

| `openclaw skills check` | 检查技能目录结构 |
| `openclaw skills list` | 列出所有技能 |

### 配置管理

| 命令 | 用途 |
|------|------|
| `openclaw config get <key>` | 获取配置项 |
| `openclaw config set <key> <value>` | 设置配置项 |
| `openclaw config list` | 列出所有配置 |


| 命令 | 用途 |
|------|------|
| `openclaw workspace list` | 列出工作区 |
| `openclaw update` | 更新 OpenClaw 版本 |

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
  "target": "chat:oc_xxx",
  "message": "<at user_id=\"ou_xxx\">姓名</at> 请回复",
  "text": "<at user_id=\"ou_xxx\">姓名</at> 请回复"
}
```


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
---
*最后重构: 2026-05-23*
*重构者: 大管家*
