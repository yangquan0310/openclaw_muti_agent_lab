#!/bin/bash
# 工作记忆维护脚本
# 功能：清理非active/paused任务，归档到事件记忆

WORKSPACE="$HOME/.openclaw/workspace/academicassistant"
MEMORY_FILE="$WORKSPACE/MEMORY.md"
LOG_FILE="$HOME/教研室仓库/日志文件/$(date +%Y-%m-%d)/$(date +%H-%M-%S)-academicassistant-每日维护.md"

# 创建日志目录
mkdir -p "$(dirname $LOG_FILE)"

# 记录维护开始时间
echo "# 工作记忆维护日志" > "$LOG_FILE"
echo "维护时间：$(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# 检查MEMORY.md是否存在
if [ ! -f "$MEMORY_FILE" ]; then
    echo "❌ MEMORY.md不存在" >> "$LOG_FILE"
    exit 1
fi

# 提取completed和killed状态的任务并归档到事件记忆
echo "## 归档任务" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# 读取活跃子代理清单，提取completed和killed状态的任务
completed_tasks=$(grep "|.*|.*|.*| completed |" "$MEMORY_FILE" || true)
killed_tasks=$(grep "|.*|.*|.*| killed |" "$MEMORY_FILE" || true)

if [ -z "$completed_tasks" ] && [ -z "$killed_tasks" ]; then
    echo "✅ 没有需要归档的任务" >> "$LOG_FILE"
else
    # 归档到事件记忆
    today=$(date +%Y-%m-%d)
    
    # 处理completed任务
    if [ -n "$completed_tasks" ]; then
        echo "### 归档completed任务" >> "$LOG_FILE"
        echo "$completed_tasks" | while read line; do
            # 提取任务信息
            subagent_key=$(echo "$line" | awk -F'|' '{print $2}' | xargs)
            task=$(echo "$line" | awk -F'|' '{print $4}' | xargs)
            echo "- 归档：$subagent_key - $task" >> "$LOG_FILE"
        done
        echo "" >> "$LOG_FILE"
    fi
    
    # 处理killed任务
    if [ -n "$killed_tasks" ]; then
        echo "### 归档killed任务" >> "$LOG_FILE"
        echo "$killed_tasks" | while read line; do
            # 提取任务信息
            subagent_key=$(echo "$line" | awk -F'|' '{print $2}' | xargs)
            task=$(echo "$line" | awk -F'|' '{print $4}' | xargs)
            echo "- 归档：$subagent_key - $task" >> "$LOG_FILE"
        done
        echo "" >> "$LOG_FILE"
    fi
    
    # 从活跃子代理清单中删除completed和killed状态的任务
    # 使用sed删除包含"| completed |"或"| killed |"的行（保留表头）
    sed -i '/^| agent:.*|.*|.*| completed |.*|.*|.*|$/d' "$MEMORY_FILE"
    sed -i '/^| agent:.*|.*|.*| killed |.*|.*|.*|$/d' "$MEMORY_FILE"
    
    echo "✅ 已清理completed/killed任务" >> "$LOG_FILE"
fi

echo "" >> "$LOG_FILE"
echo "## 维护完成" >> "$LOG_FILE"
echo "完成时间：$(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"

echo "工作记忆维护完成，日志已保存到：$LOG_FILE"
