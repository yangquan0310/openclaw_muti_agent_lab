#!/bin/bash
# OpenClaw配置备份脚本
# 只备份核心配置文件，确保Git仓库保持清洁

set -e

echo "=== OpenClaw核心配置备份任务 ==="
echo "执行时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 工作目录
WORKDIR="/root/.openclaw"
BACKUP_LOG="/root/实验室仓库/工作日志/$(date +%Y-%m-%d)/$(date +%H-%M-%S)-大管家-上传GitHub.md"

# 创建日志目录
mkdir -p "$(dirname "$BACKUP_LOG")"

# 记录到日志文件
{
echo "=== OpenClaw核心配置备份任务 ==="
echo "执行时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "工作目录: $WORKDIR"
echo ""

# 1. 检查当前Git状态
echo "1. 检查当前Git状态..."
cd "$WORKDIR"
echo "当前分支: $(git branch --show-current)"
echo "远程仓库: $(git remote -v | grep origin | head -1)"
echo ""

# 2. 检查未提交的更改
echo "2. 检查未提交的更改..."
git status --short
echo ""

# 3. 备份核心配置文件
echo "3. 备份核心配置文件..."
# 只添加已跟踪的文件，避免添加未跟踪的临时文件
git add -u
echo "跟踪的文件列表:"
git ls-files

echo ""
echo "跟踪的文件数量: $(git ls-files | wc -l)"
echo ""

# 4. 提交更改
echo "4. 提交更改..."
if git diff --cached --quiet; then
    echo "没有需要提交的更改"
else
    git commit -m "备份: OpenClaw核心配置文件 - $(date '+%Y-%m-%d %H:%M:%S')"
    echo "✅ 提交成功"
fi
echo ""

# 5. 推送到远程仓库
echo "5. 推送到远程仓库..."
CURRENT_BRANCH=$(git branch --show-current)
if git push origin $CURRENT_BRANCH; then
    echo "✅ 推送成功"
else
    echo "❌ 推送失败，请检查网络连接或权限"
    exit 1
fi
echo ""

# 6. 验证备份
echo "6. 验证备份..."
echo "当前跟踪的文件:"
git ls-files | head -20
echo "..."
echo ""
echo "总文件数: $(git ls-files | wc -l) 个文件"
echo ""

echo "=== 备份完成 ==="
echo "只同步核心配置文件，确保Git仓库轻量、清洁"
echo "同步的文件包括:"
echo "  - 根目录: .gitignore, README.md, openclaw.json"
echo "  - agents目录: 各Agent的models.json"
echo "  - workspace目录: 10个主要Agent的7个核心配置文件"
echo "    (AGENTS.md, HEARTBEAT.md, IDENTITY.md, MEMORY.md, SOUL.md, TOOLS.md, USER.md)"
echo "  - 技能目录: skills/lab-backup-manager/ 备份脚本和文档"
echo ""

} >> "$BACKUP_LOG" 2>&1

echo "备份完成，日志文件: $BACKUP_LOG"
echo "✅ 备份任务执行完成"