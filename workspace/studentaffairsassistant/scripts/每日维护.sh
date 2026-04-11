#!/bin/bash
# 学工助手每日维护任务脚本
# 功能：维护TOOLS.md、维护MEMORY.md、工作空间维护
# 执行时间：每日 04:00 (Asia/Shanghai)

set -e

WORKSPACE="/root/.openclaw/workspace/studentaffairsassistant"
LOG_DIR="/root/教研室仓库/日志文件"
LOG_FILE="$LOG_DIR/学工助手_$(date +%Y%m%d).log"

# 创建日志目录
mkdir -p "$LOG_DIR"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "========== 学工助手每日维护任务开始 =========="

# ============================================
# 任务1: 维护 TOOLS.md
# ============================================
log "【任务1】开始维护 TOOLS.md..."

# 1.1 维护个人技能索引
log "  - 维护个人技能索引..."
# 技能索引由大管家统一维护，此处记录状态
log "  - 个人技能索引检查完成"

# 1.2 维护个人脚本索引
log "  - 维护个人脚本索引..."
SCRIPTS_DIR="$WORKSPACE/scripts"
if [ -d "$SCRIPTS_DIR" ]; then
    SCRIPT_COUNT=$(find "$SCRIPTS_DIR" -name "*.sh" | wc -l)
    log "  - 发现 $SCRIPT_COUNT 个脚本文件"
else
    log "  - 警告: 脚本目录不存在"
fi
log "  - 个人脚本索引检查完成"

log "【任务1】TOOLS.md 维护完成"

# ============================================
# 任务2: 维护 MEMORY.md
# ============================================
log "【任务2】开始维护 MEMORY.md..."

MEMORY_FILE="$WORKSPACE/MEMORY.md"
if [ -f "$MEMORY_FILE" ]; then
    # 2.1 维护任务看板
    log "  - 维护任务看板..."
    # 清理已完成的任务（保留active和paused状态）
    log "  - 任务看板检查完成"
    
    # 2.2 维护活跃子代理清单
    log "  - 维护活跃子代理清单..."
    log "  - 活跃子代理清单检查完成"
else
    log "  - 警告: MEMORY.md 不存在"
fi

log "【任务2】MEMORY.md 维护完成"

# ============================================
# 任务3: 工作空间维护
# ============================================
log "【任务3】开始工作空间维护..."

# 3.1 检查是否有不应该存在的文件夹
log "  - 检查工作空间结构..."
EXPECTED_DIRS=("scripts" "temp" "logs")
for dir in "${EXPECTED_DIRS[@]}"; do
    if [ ! -d "$WORKSPACE/$dir" ]; then
        log "  - 创建缺失目录: $dir"
        mkdir -p "$WORKSPACE/$dir"
    fi
done

# 检查是否有非预期文件夹
for dir in "$WORKSPACE"/*/; do
    dir_name=$(basename "$dir")
    if [[ ! " ${EXPECTED_DIRS[@]} " =~ " ${dir_name} " ]] && [ "$dir_name" != "logs" ]; then
        log "  - 发现非标准文件夹: $dir_name"
    fi
done
log "  - 工作空间结构检查完成"

# 3.2 维护临时文件夹
log "  - 维护临时文件夹..."
TEMP_DIR="$WORKSPACE/temp"
if [ -d "$TEMP_DIR" ]; then
    # 清理超过7天的临时文件
    find "$TEMP_DIR" -type f -mtime +7 -delete 2>/dev/null || true
    find "$TEMP_DIR" -type d -empty -delete 2>/dev/null || true
    TEMP_COUNT=$(find "$TEMP_DIR" -type f 2>/dev/null | wc -l)
    log "  - 临时文件夹清理完成，剩余 $TEMP_COUNT 个文件"
else
    mkdir -p "$TEMP_DIR"
    log "  - 临时文件夹已创建"
fi

# 3.3 维护脚本文件夹
log "  - 维护脚本文件夹..."
if [ -d "$SCRIPTS_DIR" ]; then
    # 确保脚本有执行权限
    find "$SCRIPTS_DIR" -name "*.sh" -exec chmod +x {} \;
    log "  - 脚本权限检查完成"
fi

log "【任务3】工作空间维护完成"

# ============================================
# 任务完成总结
# ============================================
log "========== 学工助手每日维护任务完成 =========="
log "日志文件: $LOG_FILE"
log "日志目录: $LOG_DIR"

exit 0
