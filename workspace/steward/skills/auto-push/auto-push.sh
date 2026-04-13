#!/bin/bash
# 自动推送代码到development分支脚本
# 执行时间：每日凌晨03:30，由Cron定时任务调用

set -e

# 配置项
REPO_DIR="/root/.openclaw"
BRANCH_NAME="development"
LOG_FILE="/root/教研室仓库/日志文件/心跳任务/cron_steward_auto-push.log"
DATE=$(date "+%Y-%m-%d %H:%M:%S")

# 日志函数
log() {
    echo "[$DATE] $1" >> $LOG_FILE
}

log "=== 开始自动推送任务 ==="

# 进入仓库目录
cd $REPO_DIR || {
    log "❌ 仓库目录不存在: $REPO_DIR"
    exit 1
}

# 检查Git状态
if ! git status > /dev/null 2>&1; then
    log "❌ 当前目录不是Git仓库"
    exit 1
fi

# 切换到目标分支
if ! git checkout $BRANCH_NAME > /dev/null 2>&1; then
    log "❌ 切换分支失败: $BRANCH_NAME"
    exit 1
fi
log "✅ 切换到分支: $BRANCH_NAME"

# 拉取最新代码
if ! git pull origin $BRANCH_NAME > /dev/null 2>&1; then
    log "❌ 拉取最新代码失败"
    exit 1
fi
log "✅ 拉取最新代码成功"

# 检查是否有未提交的更改
if git status | grep -q "nothing to commit, working tree clean"; then
    log "ℹ️ 没有未提交的更改，无需推送"
    exit 0
fi

# 添加所有更改
if ! git add . > /dev/null 2>&1; then
    log "❌ 添加文件到暂存区失败"
    exit 1
fi
log "✅ 添加所有更改到暂存区"

# 提交更改
COMMIT_MSG="auto-push: 每日自动提交 $DATE"
if ! git commit -m "$COMMIT_MSG" > /dev/null 2>&1; then
    log "❌ 提交更改失败"
    exit 1
fi
log "✅ 提交更改成功: $COMMIT_MSG"

# 推送到远程仓库
if ! git push origin $BRANCH_NAME > /dev/null 2>&1; then
    log "❌ 推送到远程仓库失败"
    exit 1
fi
log "✅ 推送到远程仓库成功"

log "=== 自动推送任务完成 ==="
exit 0
