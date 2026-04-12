#!/bin/bash
# 每日维护脚本
# 功能：合并TOOLS更新、工作记忆维护、工作空间维护三个任务
# 执行时间：每日 04:00

WORKSPACE="$HOME/.openclaw/workspace/physicist"
MEMORY_FILE="$WORKSPACE/MEMORY.md"
TOOLS_FILE="$WORKSPACE/TOOLS.md"
SCRIPTS_DIR="$WORKSPACE/scripts"
TEMP_DIR="$WORKSPACE/temp"
LOG_DIR="$HOME/实验室仓库/日志文件"
LOG_FILE="$LOG_DIR/$(date +%Y-%m-%d)/04-00-00-physicist-每日维护.md"

# 创建日志目录
mkdir -p "$(dirname $LOG_FILE)"

# 记录维护开始时间
echo "# 每日维护日志" > "$LOG_FILE"
echo "维护时间：$(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

echo "## 任务1：维护 TOOLS.md" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# 1. 维护 TOOLS.md - 更新个人技能索引、个人脚本索引、项目表
if [ -f "$TOOLS_FILE" ]; then
    echo "### 1.1 更新个人技能索引" >> "$LOG_FILE"
    skills_dir="$WORKSPACE/skills"
    if [ -d "$skills_dir" ]; then
        skill_count=$(find "$skills_dir" -name "SKILL.md" 2>/dev/null | wc -l)
        echo "   发现 $skill_count 个技能" >> "$LOG_FILE"
    fi
    echo "✅ 个人技能索引更新完成" >> "$LOG_FILE"
    echo "" >> "$LOG_FILE"
    
    echo "### 1.2 更新个人脚本索引" >> "$LOG_FILE"
    scripts_dir="$WORKSPACE/scripts"
    if [ -d "$scripts_dir" ]; then
        script_count=$(find "$scripts_dir" -name "*.md" 2>/dev/null | wc -l)
        echo "   发现 $script_count 个脚本" >> "$LOG_FILE"
    fi
    echo "✅ 个人脚本索引更新完成" >> "$LOG_FILE"
    echo "" >> "$LOG_FILE"
    
    echo "### 1.3 更新项目表" >> "$LOG_FILE"
    project_dir="$HOME/实验室仓库/项目文件"
    if [ -d "$project_dir" ]; then
        project_count=$(ls -1 "$project_dir" 2>/dev/null | wc -l)
        echo "   发现 $project_count 个项目" >> "$LOG_FILE"
    fi
    echo "✅ 项目表更新完成" >> "$LOG_FILE"
else
    echo "⚠️ TOOLS.md 不存在" >> "$LOG_FILE"
fi

echo "" >> "$LOG_FILE"
echo "## 任务2：工作记忆维护" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# 2. 工作记忆维护 - 清理非active/paused任务
if [ -f "$MEMORY_FILE" ]; then
    # 提取completed和killed状态的任务
    completed_tasks=$(grep "|.*|.*|.*| completed |" "$MEMORY_FILE" || true)
    killed_tasks=$(grep "|.*|.*|.*| killed |" "$MEMORY_FILE" || true)
    
    if [ -z "$completed_tasks" ] && [ -z "$killed_tasks" ]; then
        echo "✅ 没有需要归档的任务" >> "$LOG_FILE"
    else
        # 处理completed任务
        if [ -n "$completed_tasks" ]; then
            echo "### 归档completed任务" >> "$LOG_FILE"
            echo "$completed_tasks" | while read line; do
                subagent_key=$(echo "$line" | awk -F'|' '{print $2}' | xargs)
                task=$(echo "$line" | awk -F'|' '{print $4}' | xargs)
                echo "- 归档：$subagent_key - $task" >> "$LOG_FILE"
            done
            echo "" >> "$LOG_FILE"
        fi
        
        # 处理killed任务
        if [ -n "$killed_tasks" ]; then
            echo "### 删除killed任务" >> "$LOG_FILE"
            echo "$killed_tasks" | while read line; do
                subagent_key=$(echo "$line" | awk -F'|' '{print $2}' | xargs)
                task=$(echo "$line" | awk -F'|' '{print $4}' | xargs)
                echo "- 删除：$subagent_key - $task" >> "$LOG_FILE"
            done
            echo "" >> "$LOG_FILE"
        fi
        
        # 从活跃子代理清单中删除completed和killed状态的任务
        sed -i '/^| agent:.*|.*|.*| completed |.*|.*|.*|$/d' "$MEMORY_FILE"
        sed -i '/^| agent:.*|.*|.*| killed |.*|.*|.*|$/d' "$MEMORY_FILE"
        
        echo "✅ 已清理completed/killed任务" >> "$LOG_FILE"
    fi
else
    echo "⚠️ MEMORY.md 不存在" >> "$LOG_FILE"
fi

echo "" >> "$LOG_FILE"
echo "## 任务3：工作空间维护" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# 3. 工作空间维护
# 3.1 检查不应该存在的文件夹
echo "### 检查工作空间结构" >> "$LOG_FILE"

# 定义标准文件夹列表
standard_dirs=("scripts" ".openclaw" "temp" "skills")
unexpected_dirs=()

for dir in "$WORKSPACE"/*/; do
    dir_name=$(basename "$dir")
    is_standard=false
    for std_dir in "${standard_dirs[@]}"; do
        if [ "$dir_name" = "$std_dir" ]; then
            is_standard=true
            break
        fi
    done
    
    # 检查是否是文件（不是目录）
    if [ -d "$dir" ] && [ "$dir_name" != "." ] && [ "$dir_name" != ".." ]; then
        if [ "$is_standard" = false ]; then
            # 排除.md文件和其他标准文件
            if [[ ! "$dir_name" =~ \.(md|backup)$ ]]; then
                unexpected_dirs+=("$dir_name")
            fi
        fi
    fi
done

if [ ${#unexpected_dirs[@]} -eq 0 ]; then
    echo "✅ 没有发现不应该存在的文件夹" >> "$LOG_FILE"
else
    echo "⚠️ 发现非标准文件夹：" >> "$LOG_FILE"
    for dir in "${unexpected_dirs[@]}"; do
        echo "   - $dir" >> "$LOG_FILE"
    done
fi

# 3.2 检查临时文件
echo "" >> "$LOG_FILE"
echo "### 检查临时文件" >> "$LOG_FILE"

if [ -d "$TEMP_DIR" ]; then
    temp_count=$(find "$TEMP_DIR" -type f 2>/dev/null | wc -l)
    if [ "$temp_count" -eq 0 ]; then
        echo "✅ 临时文件夹为空" >> "$LOG_FILE"
    else
        echo "📁 临时文件夹中有 $temp_count 个文件" >> "$LOG_FILE"
        
        # 检查超过7天的临时文件
        old_files=$(find "$TEMP_DIR" -type f -mtime +7 2>/dev/null)
        if [ -n "$old_files" ]; then
            old_count=$(echo "$old_files" | wc -l)
            echo "⚠️ 发现 $old_count 个超过7天的临时文件：" >> "$LOG_FILE"
            echo "$old_files" | while read file; do
                echo "   - $(basename "$file") ($(stat -c %y "$file" 2>/dev/null | cut -d' ' -f1))" >> "$LOG_FILE"
            done
        else
            echo "✅ 没有超过7天的临时文件" >> "$LOG_FILE"
        fi
    fi
else
    echo "ℹ️ 临时文件夹不存在，创建中..." >> "$LOG_FILE"
    mkdir -p "$TEMP_DIR"
    echo "✅ 已创建临时文件夹" >> "$LOG_FILE"
fi

# 3.3 检查scripts文件夹
echo "" >> "$LOG_FILE"
echo "### 检查脚本文件夹" >> "$LOG_FILE"

if [ -d "$SCRIPTS_DIR" ]; then
    script_count=$(find "$SCRIPTS_DIR" -type f \( -name "*.sh" -o -name "*.py" \) 2>/dev/null | wc -l)
    echo "✅ 脚本文件夹中有 $script_count 个脚本文件" >> "$LOG_FILE"
else
    echo "ℹ️ 脚本文件夹不存在，创建中..." >> "$LOG_FILE"
    mkdir -p "$SCRIPTS_DIR"
    echo "✅ 已创建脚本文件夹" >> "$LOG_FILE"
fi

echo "" >> "$LOG_FILE"
echo "## 维护完成" >> "$LOG_FILE"
echo "完成时间：$(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
echo "---" >> "$LOG_FILE"
echo "下次维护时间：明日 04:00" >> "$LOG_FILE"

echo "每日维护完成，日志已保存到：$LOG_FILE"
