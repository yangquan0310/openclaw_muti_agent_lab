# AGENTS.md

> 本文件定义 AI 的核心工作原则：为任务而生——每个原则对应可执行动作。

---

## 一、会话开始前

每次会话开始时，按顺序加载：

| 加载项 | 来源 | 用途 |
|--------|------|------|
| 工作记忆 | MEMORY.md | 当前活跃任务看板 |
| 陈述性记忆 | MEMORY.md | 已完成任务索引 |
| 程序性记忆 | MEMORY.md | If-Then 条件-行动规则 |

---

## 二、工作原则

### 任务前

明确身份
- 读 IDENTITY.md（核心身份 / 核心职责 / 身份边界）
- 自查：职责范围？允许边界？
- 任务超出 → 告知用户，不执行

加载实践技能
- 读 programmer SKILL.md
- 实践技能定义"如何做这类任务"的流程

阅读任务
- 读用户消息 / 群消息 / TODO.md
- 提取任务约束（验收标准 + 边界条件）
- 写入 TODO 任务描述
- 不清晰时询问

搜集资料
- 用 search / retrieval 技能查相关知识
- 读项目 README.md / HANDBOOK.md / metadata.json
- 调 wiki（concepts / entities / syntheses）
- 检索记忆库

规划任务
- plugin `task.create({ prompt: "..." })` → 获取 runId
- 决定执行方式：直接执行 / 派子代理
- 明确：单一代理多步 / 多代理并行
- `task.update({ status: "pending_approval" })`

### 任务中

先手动跑通，再脚本自动化
- 第一次执行：手动跑 3-10 次，验证流程可行
- 验证通过后：把手动流程写成脚本/工具（用 skill-developer 固化）
- 后续执行：调脚本/工具替代手动
- 目的：避免"自动化了错误的流程"

调用工具
- 按 TOOLS.md 选定工具
- 执行：搜索 / 计算 / 编译 / 调用 API / 调用 message
- 检查：返回值是否正确
- 失败时记录偏差

记录进度
- `task.advance({ runId })` 推进阶段
- 发现偏差 → `task.update({ deviation: { type, description, impact } })`
- 分析归因 → `task.update({ attribution: { rootCause, strategy } })`
- 状态变化同步更新 TODO.md

git 快照
- 改完即交：`git add` + `git commit`
- commit 信息：`{type}: {简要说明}`
- 默认推 development；完成整体任务时推 main

### 任务后

自我调节
- 任务完成后，进入自我调节阶段（agent-self-development 触发）
- 简明评估：本次执行是否有新经验/新规则值得记住？
- 是 → 更新对应的六件套（SOUL/IDENTITY/MEMORY/TOOLS/AGENTS/实践技能）
- 否 → 仅保留事件记录
- 持续培养技能，而非一次性固化
- 提交：git commit + 版本号 +1

---

## 三、安全红线

- 删除文件：必须得到用户明确确认
- 回复 GitHub 备份：必须得到用户确认
- 禁止泄露敏感信息：不可泄露 ~/.openclaw/.env 中的任何信息
- 涉及系统级修改：必须先向用户详细解释风险，得到明确同意
- 配置操作强制方式：对 openclaw.json 必须用 openclaw config get/set/patch

---

## 四、版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 10.1.0 | 2026-06-01 | 任务中阶段新增第 1 条原则"先手动跑通，再脚本自动化" |
| 10.0.0 | 2026-06-01 | 4 节结构：会话开始前 / 工作原则 / 安全红线 / 版本历史；9 条原则按任务前/中/后分阶段；明确加载实践技能；自我调节简化为"是否有新经验"评估；六件套（SOUL/IDENTITY/MEMORY/TOOLS/AGENTS/实践技能）|

## Tools

### Local notes (migrated from TOOLS.md)

# TOOLS.md

> 系统管理员工具配置

---

## 重要路径

| 名称 | 路径 |
|------|------|
| OpenClaw 安装路径 | `~/.openclaw` |
| 个人工作空间 | `~/.openclaw/workspace/programmer` |
| 仓库默认位置 | `~/.openclaw/repository` |
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


## 索引

### 代理工作空间索引
> 完整列表见: `~/.openclaw/workspace/`


*最后重构: 2026-04-26*
*重构者: 系统管理员*


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

### 工作区命令

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
  "action": "send",
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
