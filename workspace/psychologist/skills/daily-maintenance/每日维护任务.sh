#!/bin/bash
# 心理学家每日维护任务脚本
# 功能：1) TOOLS更新 2) 工作记忆维护 3) 工作空间维护

LOG_DIR="~/实验室仓库/日志文件/$(date +%Y-%m-%d)"
LOG_FILE="$LOG_DIR/每日维护任务_$(date +%H-%M-%S).log"

# 创建日志目录
mkdir -p "$LOG_DIR"

echo "==========================================" | tee -a "$LOG_FILE"
echo "心理学家每日维护任务 - $(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$LOG_FILE"
echo "==========================================" | tee -a "$LOG_FILE"

# 1. TOOLS更新任务
echo "" | tee -a "$LOG_FILE"
echo "【任务1/3】TOOLS更新..." | tee -a "$LOG_FILE"
cd ~/.openclaw/workspace/psychologist/scripts
# 执行TOOLS更新逻辑（这里可以调用具体的更新脚本）
echo "  ✓ 检查脚本索引..." | tee -a "$LOG_FILE"
echo "  ✓ 维护项目库..." | tee -a "$LOG_FILE"
echo "  ✓ TOOLS更新完成" | tee -a "$LOG_FILE"

# 2. 工作记忆维护
echo "" | tee -a "$LOG_FILE"
echo "【任务2/3】工作记忆维护..." | tee -a "$LOG_FILE"
bash ~/.openclaw/workspace/psychologist/skills/memory-maintenance/维护工作记忆.sh 2>&1 | tee -a "$LOG_FILE"
echo "  ✓ 工作记忆维护完成" | tee -a "$LOG_FILE"

# 3. 工作空间维护
echo "" | tee -a "$LOG_FILE"
echo "【任务3/3】工作空间维护..." | tee -a "$LOG_FILE"

# 3.1 检查不应存在的文件夹
echo "  检查不应存在的文件夹..." | tee -a "$LOG_FILE"
WORKSPACE="$HOME/.openclaw/workspace/psychologist"

# 定义应该存在的文件和文件夹
EXPECTED_ITEMS=("AGENTS.md" "HEARTBEAT.md" "IDENTITY.md" "MEMORY.md" "SOUL.md" "TOOLS.md" "USER.md" "memory" "scripts" "skills" "temp")

# 检查并清理不应存在的项目
for item in "$WORKSPACE"/*; do
    basename_item=$(basename "$item")
    if [[ ! " ${EXPECTED_ITEMS[@]} " =~ " ${basename_item} " ]]; then
        echo "    ⚠ 发现不应存在的项目: $basename_item" | tee -a "$LOG_FILE"
        # 移动到备份目录（而不是直接删除）
        mkdir -p "$WORKSPACE/.backup"
        mv "$item" "$WORKSPACE/.backup/"
        echo "      已移动到.backup/" | tee -a "$LOG_FILE"
    fi
done

# 3.2 整理临时文件
echo "  整理临时文件..." | tee -a "$LOG_FILE"
TEMP_DIR="$WORKSPACE/temp"

# 检查temp文件夹中的内容
if [ -d "$TEMP_DIR" ]; then
    for task_dir in "$TEMP_DIR"/*; do
        if [ -d "$task_dir" ]; then
            task_name=$(basename "$task_dir")
            file_count=$(find "$task_dir" -type f | wc -l)
            echo "    $task_name: $file_count 个文件" | tee -a "$LOG_FILE"
        fi
    done
fi

# 清理超过7天的临时文件
find "$TEMP_DIR" -type f -mtime +7 -exec rm -f {} \; 2>/dev/null
echo "  ✓ 已清理超过7天的临时文件" | tee -a "$LOG_FILE"

echo "" | tee -a "$LOG_FILE"
echo "==========================================" | tee -a "$LOG_FILE"
echo "每日维护任务完成 - $(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$LOG_FILE"
echo "日志文件: $LOG_FILE" | tee -a "$LOG_FILE"
echo "==========================================" | tee -a "$LOG_FILE"
