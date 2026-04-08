---
name: lab-backup-manager
description: >
  实验室仓库备份管理技能。使用轻量级备份脚本自动备份OpenClaw核心配置文件到GitHub。
  只备份由.gitignore控制的必要文件，确保仓库清洁、轻量。支持按计划或手动执行备份任务。
metadata: { "openclaw": { "emoji": "🔄", "requires": { "bins": ["git"] } } }
---

# 实验室仓库备份管理技能

使用轻量级备份脚本自动执行OpenClaw核心配置文件的备份和同步任务。

## 功能特性

- ✅ **轻量级备份**：只备份核心配置文件，由.gitignore控制备份范围
- ✅ **GitHub同步**：自动将核心配置更改提交并推送到GitHub仓库
- ✅ **详细日志**：彩色日志输出，清晰显示执行进度和结果
- ✅ **安全备份**：基于Git版本控制，支持历史版本恢复
- ✅ **自动执行**：支持定时任务，无需人工干预

## 核心任务

### 任务1: 检查Git状态

检查当前OpenClaw目录的Git仓库状态，确保配置正确。

**检查内容**：
- 当前分支状态
- 远程仓库配置
- 未提交的更改

**执行流程**：
1. 切换到工作目录
2. 显示当前分支
3. 显示远程仓库信息
4. 检查未提交的更改

### 任务2: 备份核心配置文件

根据.gitignore规则，只备份核心配置文件到Git仓库。

**备份范围**：
- 根目录：.gitignore, README.md, openclaw.json
- agents目录：各Agent的models.json
- workspace目录：6个主要Agent的7个核心配置文件
  (AGENTS.md, HEARTBEAT.md, IDENTITY.md, MEMORY.md, SOUL.md, TOOLS.md, USER.md)

**执行流程**：
1. 显示当前跟踪的文件列表
2. 统计跟踪的文件数量
3. 确保只包含必要的核心配置文件

### 任务3: 提交并推送到GitHub

自动将更改提交并推送到GitHub仓库。

**GitHub仓库**：
- 基于当前OpenClaw目录配置
- 分支：main

**执行流程**：
1. 添加所有更改到暂存区
2. 检查是否有需要提交的更改
3. 提交更改（带时间戳）
4. 推送到GitHub远程仓库

### 任务4: 验证备份

验证备份是否成功，并显示备份结果。

**验证内容**：
- 当前跟踪的文件列表
- 总文件数量
- 备份的完成状态

## 使用方式

### 基本使用

```bash
bash /root/.openclaw/backup.sh
```

### 定时执行

可添加到cron任务，例如每天凌晨2点执行：

```bash
0 2 * * * bash /root/.openclaw/backup.sh
```

### 日志查看

备份日志保存在实验室仓库日志目录中：

```bash
ls -la /root/实验室仓库/工作日志/$(date +%Y-%m-%d)/
```

## 输出示例

```
=== OpenClaw核心配置备份任务 ===
执行时间: 2026-04-07 21:40:00

1. 检查当前Git状态...
当前分支: main
远程仓库: origin git@github.com:yangquan0310/openclaw_multi_agent_backup.git (fetch)

2. 检查未提交的更改...
M  workspace/steward/MEMORY.md

3. 备份核心配置文件...
跟踪的文件列表:
.gitignore
README.md
openclaw.json
agents/mathematician/agent/models.json
agents/physicist/agent/models.json
agents/psychologist/agent/models.json
agents/reviewer/agent/models.json
agents/steward/agent/models.json
agents/writer/agent/models.json
workspace/mathematician/AGENTS.md
workspace/mathematician/HEARTBEAT.md
workspace/mathematician/IDENTITY.md
workspace/mathematician/MEMORY.md
workspace/mathematician/SOUL.md
workspace/mathematician/TOOLS.md
workspace/mathematician/USER.md
...

跟踪的文件数量: 72

4. 提交更改...
✅ 提交成功

5. 推送到远程仓库...
✅ 推送成功

6. 验证备份...
当前跟踪的文件:
.gitignore
README.md
openclaw.json
...
总文件数: 72 个文件

=== 备份完成 ===
只同步核心配置文件，确保Git仓库轻量、清洁
同步的文件包括:
  - 根目录: .gitignore, README.md, openclaw.json
  - agents目录: 各Agent的models.json
  - workspace目录: 6个主要Agent的7个核心配置文件
    (AGENTS.md, HEARTBEAT.md, IDENTITY.md, MEMORY.md, SOUL.md, TOOLS.md, USER.md)

备份完成，日志文件: /root/实验室仓库/日志/2026-04-07/openclaw_backup_21-40-00.log
✅ 备份任务执行完成
```

## 前置条件

- Git已配置并可访问GitHub仓库
- SSH密钥已配置，可推送代码
- OpenClaw目录已初始化为Git仓库
- .gitignore文件正确配置，排除敏感文件

## 安装与配置

### 1. 安装脚本

将备份脚本复制到OpenClaw根目录：

```bash
cp /root/.openclaw/skills/lab-backup-manager/backup.sh /root/.openclaw/backup.sh
chmod +x /root/.openclaw/backup.sh
```

### 2. 配置.gitignore

确保`.gitignore`文件已正确配置（已自动生成）：

```gitignore
# 排除敏感文件
.env
*.key
*.secret
*.pem
*.env*
credentials.json
tokens.json

# 排除日志和缓存文件
*.log
*.cache
*.tmp
*.temp
*.swp
*.swo
*~

# 排除OpenClaw内部文件
node_modules/
.cache/
*.db
sessions/
memory/
devices/
openclaw-*/
subagents/
exec-approvals.json
identity/
venv/
*/venv/
*/sessions/
*/memory/
*.db-journal
*.pyc
__pycache__/
.pytest_cache/

# 排除IDE配置文件
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# 排除备份文件
*.backup
*.bak
*.old
*.tmp.md
*.backup.*

# 排除临时文件
ppt_temp/
```

### 3. 配置Git远程仓库

确保OpenClaw目录已正确配置Git远程仓库：

```bash
cd /root/.openclaw
git remote -v  # 查看远程仓库配置
# 如果未配置，执行：
# git remote add origin git@github.com:<username>/<repo>.git
```

### 4. 配置SSH密钥

确保SSH密钥已添加到GitHub账户：

```bash
ssh -T git@github.com  # 测试连接
# 显示 "Hi <username>! You've successfully authenticated..." 表示配置成功
```

### 脚本位置

备份脚本位于：
```bash
/root/.openclaw/skills/lab-backup-manager/backup.sh
/root/.openclaw/backup.sh  # 运行位置
```

## 快速开始

### 手动执行备份

```bash
# 方法1: 直接执行
/root/.openclaw/backup.sh

# 方法2: 使用技能路径
bash /root/.openclaw/skills/lab-backup-manager/backup.sh
```

### 定时自动备份

添加到cron任务，例如每天凌晨2点执行：

```bash
# 编辑crontab
crontab -e

# 添加以下行
0 2 * * * /root/.openclaw/backup.sh >> /var/log/openclaw_backup.log 2>&1
```

### 查看备份日志

备份日志保存在实验室仓库日志目录中：

```bash
# 查看今日日志
ls -la /root/实验室仓库/工作日志/$(date +%Y-%m-%d)/

# 查看所有日志
find /root/实验室仓库/工作日志/ -name "*-大管家-上传GitHub.md" | sort
```

## 常见问题

### Q: 如何只备份核心配置文件？

A: 备份脚本基于`.gitignore`规则，只备份已跟踪的核心配置文件，确保仓库轻量。

### Q: 推送GitHub失败怎么办？

A: 检查：
1. SSH密钥是否正确配置
2. GitHub仓库访问权限
3. 网络连接是否正常
4. Git远程仓库配置是否正确

### Q: 如何恢复备份的文件？

A: 通过Git历史恢复：
```bash
cd /root/.openclaw
git log --oneline  # 查看提交历史
git checkout <commit-hash> -- <file>  # 恢复特定文件
```

### Q: 备份脚本在哪里？

A: 脚本有两个位置：
- 技能目录: `/root/.openclaw/skills/lab-backup-manager/backup.sh`
- 运行位置: `/root/.openclaw/backup.sh`

### Q: 如何检查备份是否正常工作？

A: 执行以下步骤验证：
1. 手动执行备份: `/root/.openclaw/backup.sh`
2. 查看日志文件: 检查是否有错误信息
3. 访问GitHub仓库: 确认最新提交已同步
4. 验证文件完整性: 对比本地和GitHub上的文件内容

### Q: 如何添加新的文件到备份范围？

A: 修改`.gitignore`文件，添加要跟踪的文件或目录：
```bash
# 取消注释或添加新的规则
!path/to/file
!path/to/directory/
```

### Q: 如何排除不需要备份的文件？

A: 在`.gitignore`文件中添加排除规则：
```bash
# 添加需要排除的文件或目录
path/to/file
path/to/directory/
```

## 依赖

- Git
- Bash
- OpenSSH（用于GitHub推送）

## 安全提示

- 确保只有授权用户可以执行此脚本
- 定期检查备份日志
- 通过`.gitignore`排除所有敏感文件
- Git仓库不包含API密钥、密码等敏感信息
