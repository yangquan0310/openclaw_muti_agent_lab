# GitHub同步策略文档

## 概述
本文档描述了OpenClaw实验室的GitHub备份同步策略。该策略基于`.openclaw`根目录进行同步，确保只同步必要且安全的文件。

## 同步范围

### ✅ 允许同步的内容
1. **workspace/** - 所有Agent的工作空间
2. **agents/** - Agent配置目录
3. **openclaw.json** - 主配置文件
4. **.gitignore** - Git忽略规则文件

### ❌ 禁止同步的内容
1. **敏感文件**：
   - `.env`文件
   - 各种密钥文件（`.key`, `.secret`, `.token`, `.pem`, `.crt`, `.pfx`, `.p12`）
   
2. **日志和缓存文件**：
   - 各种日志文件（`*.log`）
   - 缓存目录（`node_modules/`, `__pycache__/`, `*.pyc`）
   - 备份文件（`*.bak`, `*.backup`）
   - 临时文件（`*.tmp`, `*.temp`, `*.swp`, `*~`）
   
3. **OpenClaw内部文件**：
   - `config/openclaw.json.bak*` - 配置文件备份
   - `memory-tdai/` - 临时记忆存储
   - `tasks/` - 任务队列
   - `subagents/` - 子代理管理
   - `delivery-queue/` - 消息队列
   - `state/` - 状态文件
   - `cron/` - 定时任务

4. **IDE配置文件**：
   - `.vscode/`
   - `.idea/`

## Git仓库配置

### 仓库位置
- **根目录**: `/root/.openclaw/`
- **远程仓库**: `git@github.com:yangquan0310/openclaw_multi_agent_backup.git`

### Git配置
- **用户名**: OpenClaw Backup
- **邮箱**: backup@openclaw.local
- **分支**: main

## 备份脚本功能

### 任务0：清理Agent工作空间
- 仅保留8个核心配置MD文件：
  - `AGENTS.md`, `BOOTSTRAP.md`, `HEARTBEAT.md`, `IDENTITY.md`
  - `MEMORY.md`, `SOUL.md`, `TOOLS.md`, `USER.md`
- 删除其他临时文件和目录
- 影响的核心Agent：`mathematician`, `physicist`, `psychologist`, `reviewer`, `writer`, `steward`

### 任务1：GitHub同步
1. **配置检查**：
   - 确保在`.openclaw`根目录初始化Git仓库
   - 配置远程GitHub仓库
   - 创建/更新`.gitignore`文件

2. **清理旧配置**：
   - 删除`workspace/.github`目录（如果存在）
   - 清空Git暂存区

3. **选择性添加**：
   - 只添加允许同步的目录和文件
   - 使用`.gitignore`确保敏感文件不被跟踪

4. **提交和推送**：
   - 自动提交更改
   - 推送到GitHub远程仓库
   - 支持强制推送（当需要时）

## 安全注意事项

### 数据保护
1. **敏感信息隔离**：
   - 所有API密钥、密码等敏感信息必须存储在`.env`文件中
   - `.env`文件已被`.gitignore`排除

2. **隐私保护**：
   - 用户个人数据不应存储在同步目录中
   - 临时文件应定期清理

### 备份验证
1. **完整性检查**：
   - 定期验证备份的完整性
   - 确保可以成功从备份恢复

2. **版本控制**：
   - 每次备份都创建新的提交
   - 提交信息包含时间戳，便于追溯

## 使用说明

### 手动运行备份
```bash
bash ~/.openclaw/workspace/skills/lab-backup-manager/backup.sh
```

### 自动定时备份（推荐）
建议配置cron任务定期运行备份：
```bash
# 每天凌晨3点运行备份
0 3 * * * /root/.openclaw/workspace/skills/lab-backup-manager/backup.sh
```

### 恢复备份
1. 克隆GitHub仓库到本地
2. 将文件复制到相应位置
3. 注意恢复`.env`等敏感文件（需要手动配置）

## 故障排除

### 常见问题
1. **GitHub推送失败**：
   - 检查网络连接
   - 验证SSH密钥配置
   - 检查GitHub仓库权限

2. **权限问题**：
   - 确保脚本有执行权限
   - 检查文件所有权

3. **磁盘空间不足**：
   - 清理临时文件
   - 扩展磁盘空间

### 日志查看
备份脚本会输出详细的日志信息，包括：
- 任务开始时间
- 每个步骤的执行状态
- 错误信息（如果有）

## 更新历史
- **2026-04-07**: 创建基于`.openclaw`根目录的同步策略，删除旧的workspace-only同步

## 联系信息
如有问题，请联系系统管理员。