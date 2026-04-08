# lab-backup-manager 使用说明

## 概述
`lab-backup-manager` 是一个用于OpenClaw实验室的轻量级备份管理工具，使用`backup_openclaw_config.sh`脚本自动备份核心配置文件到GitHub。

## 主要功能

### 1. 轻量级配置备份
- 基于`.gitignore`规则的智能备份
- 只备份核心配置文件，确保仓库轻量
- 自动排除敏感文件和临时文件

### 2. GitHub自动同步
- 自动检测并提交配置更改
- 支持GitHub推送
- 详细的日志记录和备份验证

## 安装与配置

### 脚本位置
```
/root/.openclaw/backup_openclaw_config.sh
```

### 权限设置
```bash
chmod +x /root/.openclaw/backup_openclaw_config.sh
```

## 使用方法

### 手动运行
```bash
# 运行完整备份
bash /root/.openclaw/backup_openclaw_config.sh
```

### 定时任务（推荐）
配置cron任务实现自动备份：

```bash
# 编辑cron任务
crontab -e

# 添加以下行（每天凌晨3点运行）
0 3 * * * /root/.openclaw/backup_openclaw_config.sh

# 或者每小时运行一次
0 * * * * /root/.openclaw/backup_openclaw_config.sh
```

## 配置说明

### 备份范围配置
备份脚本基于当前OpenClaw目录的Git配置，通过`.gitignore`控制备份范围：

**备份的核心文件**：
1. 根目录：`.gitignore`, `README.md`, `openclaw.json`
2. agents目录：各Agent的`models.json`
3. workspace目录：6个主要Agent的7个核心配置文件
   (AGENTS.md, HEARTBEAT.md, IDENTITY.md, MEMORY.md, SOUL.md, TOOLS.md, USER.md)

**排除的内容**（通过`.gitignore`）：
- 敏感文件（`.env`, `*.key`, `*.secret`等）
- 日志和缓存文件
- OpenClaw内部文件
- IDE配置文件

## 输出说明

### 日志输出位置
备份日志保存在实验室仓库的日志目录中：
```
/root/实验室仓库/日志/YYYY-MM-DD/openclaw_backup_HH-MM-SS.log
```

### 任务执行流程
```
=== OpenClaw核心配置备份任务 ===
执行时间: 2026-04-07 21:40:00

1. 检查当前Git状态...
2. 检查未提交的更改...
3. 备份核心配置文件...
4. 提交更改...
5. 推送到远程仓库...
6. 验证备份...

=== 备份完成 ===
备份完成，日志文件: /root/实验室仓库/日志/2026-04-07/openclaw_backup_21-40-00.log
✅ 备份任务执行完成
```

## 故障排除

### 常见问题

#### 1. GitHub推送失败
**症状**: 推送时出现权限错误
**解决方案**:
- 检查SSH密钥配置
- 验证GitHub仓库权限
- 检查网络连接
- 确认Git远程仓库配置

#### 2. 脚本执行权限问题
**症状**: `Permission denied`
**解决方案**:
```bash
chmod +x /root/.openclaw/backup_openclaw_config.sh
```

#### 3. 没有需要备份的更改
**症状**: 脚本显示没有需要提交的更改
**解决方案**:
- 检查是否有配置文件被修改
- 确认Git跟踪状态

#### 4. 脚本找不到
**症状**: `bash: /root/.openclaw/backup_openclaw_config.sh: No such file or directory`
**解决方案**:
- 确认脚本路径正确
- 检查脚本文件是否存在

## 安全注意事项

### 敏感文件保护
- 确保`.env`文件包含所有敏感信息
- 密钥文件使用`.key`、`.secret`等扩展名
- 这些文件通过`.gitignore`排除，不备份到GitHub

### 备份验证
- 定期检查GitHub仓库中的备份
- 验证备份只包含核心配置文件
- 检查备份日志确认执行状态

### 访问控制
- 限制对备份脚本的访问权限
- 使用SSH密钥而非密码进行GitHub认证

## 恢复备份

### 从Git历史恢复
```bash
# 查看提交历史
cd /root/.openclaw
git log --oneline

# 恢复特定文件
git checkout <commit-hash> -- <file-path>

# 恢复整个目录状态
git reset --hard <commit-hash>
```

### 从GitHub克隆恢复（完整恢复）
```bash
# 克隆GitHub仓库
git clone git@github.com:yangquan0310/openclaw_multi_agent_backup.git /tmp/openclaw_backup

# 复制配置文件
cp -r /tmp/openclaw_backup/* /root/.openclaw/

# 注意：需要手动恢复.env等敏感文件
```

## 更新日志

### 版本 3.0 (2026-04-07)
- 重构为轻量级备份策略，使用`backup_openclaw_config.sh`脚本
- 只备份核心配置文件，由`.gitignore`控制备份范围
- 删除Agent工作空间清理功能
- 简化配置要求，只需Git依赖

### 版本 2.0 (2026-04-07)
- 重构GitHub同步策略，基于`.openclaw`根目录
- 删除`workspace`目录中的`.github`目录清理
- 完善`.gitignore`配置
- 删除任务2（openclaw.json复制任务）

### 版本 1.0 (2026-04-06)
- 初始版本
- 包含Agent工作空间清理
- workspace-only GitHub同步
- openclaw.json复制功能

## 联系支持
如有问题，请参考：
1. SKILL.md - 技能详细文档
2. 脚本源码注释
3. 备份日志文件
4. TOOLS.md中的技能索引