#!/bin/bash
# 每日维护任务脚本
# 功能：维护 TOOLS.md、MEMORY.md 和工作空间

WORKSPACE="$HOME/.openclaw/workspace/mathematician"
MEMORY_FILE="$WORKSPACE/MEMORY.md"
TOOLS_FILE="$WORKSPACE/TOOLS.md"
LOG_FILE="$HOME/实验室仓库/日志文件/$(date +%Y-%m-%d)/04-00-00-mathematician-每日维护.md"

# 创建日志目录
mkdir -p "$(dirname $LOG_FILE)"

# 记录维护开始时间
echo "# 每日维护任务日志" > "$LOG_FILE"
echo "维护时间：$(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# ==================== 1. 维护 MEMORY.md ====================
echo "## 1. MEMORY.md 维护" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

if [ ! -f "$MEMORY_FILE" ]; then
    echo "❌ MEMORY.md 不存在" >> "$LOG_FILE"
else
    # 提取completed和killed状态的任务并归档到事件记忆
    completed_tasks=$(grep "|.*|.*|.*| completed |" "$MEMORY_FILE" || true)
    killed_tasks=$(grep "|.*|.*|.*| killed |" "$MEMORY_FILE" || true)

    if [ -z "$completed_tasks" ] && [ -z "$killed_tasks" ]; then
        echo "✅ 没有需要归档的任务" >> "$LOG_FILE"
    else
        # 处理completed任务
        if [ -n "$completed_tasks" ]; then
            echo "### 归档 completed 任务" >> "$LOG_FILE"
            echo "$completed_tasks" | while read line; do
                subagent_key=$(echo "$line" | awk -F'|' '{print $2}' | xargs)
                task=$(echo "$line" | awk -F'|' '{print $4}' | xargs)
                echo "- 归档：$subagent_key - $task" >> "$LOG_FILE"
            done
            echo "" >> "$LOG_FILE"
        fi
        
        # 处理killed任务
        if [ -n "$killed_tasks" ]; then
            echo "### 删除 killed 任务" >> "$LOG_FILE"
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
        
        echo "✅ 已清理 completed/killed 任务" >> "$LOG_FILE"
    fi
    
    # 验证程序性记忆脚本位置表
    echo "" >> "$LOG_FILE"
    echo "### 验证程序性记忆脚本位置" >> "$LOG_FILE"
    
    # 检查脚本索引中的路径是否存在
    while IFS= read -r line; do
        if echo "$line" | grep -q "|.*|.*|.*\`.*\`.*|"; then
            script_path=$(echo "$line" | grep -oP '`\K[^`]+' | head -1)
            if [ -n "$script_path" ]; then
                full_path="${script_path/#\~/$HOME}"
                if [ -f "$full_path" ]; then
                    echo "- ✅ $script_path" >> "$LOG_FILE"
                else
                    echo "- ❌ $script_path（文件不存在）" >> "$LOG_FILE"
                fi
            fi
        fi
    done < <(grep -A 100 "### 脚本索引" "$MEMORY_FILE" | grep "^|")
fi

echo "" >> "$LOG_FILE"

# ==================== 2. 维护 TOOLS.md ====================
echo "## 2. TOOLS.md 维护" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

if [ ! -f "$TOOLS_FILE" ]; then
    echo "❌ TOOLS.md 不存在" >> "$LOG_FILE"
else
    # 2.1 维护个人技能索引
    echo "### 维护个人技能索引" >> "$LOG_FILE"
    skills_dir="$WORKSPACE/skills"
    if [ -d "$skills_dir" ]; then
        skill_count=$(find "$skills_dir" -mindepth 1 -maxdepth 1 -type d | wc -l)
        echo "- 发现 $skill_count 个技能文件夹" >> "$LOG_FILE"
        
        # 检查每个技能的完整性
        for skill_dir in "$skills_dir"/*/; do
            skill_name=$(basename "$skill_dir")
            if [ -f "$skill_dir/SKILL.md" ] && [ -f "$skill_dir/README.md" ]; then
                echo "  - ✅ $skill_name（完整）" >> "$LOG_FILE"
            else
                echo "  - ⚠️ $skill_name（缺少 SKILL.md 或 README.md）" >> "$LOG_FILE"
            fi
        done
    else
        echo "- ❌ skills 文件夹不存在" >> "$LOG_FILE"
    fi
    
    echo "" >> "$LOG_FILE"
    
    # 2.2 维护个人脚本索引
    echo "### 维护个人脚本索引" >> "$LOG_FILE"
    scripts_dir="$WORKSPACE/scripts"
    if [ -d "$scripts_dir" ]; then
        script_count=$(find "$scripts_dir" -mindepth 1 -maxdepth 1 -type d | wc -l)
        echo "- 发现 $script_count 个脚本文件夹" >> "$LOG_FILE"
        
        # 检查每个脚本的完整性
        for script_dir in "$scripts_dir"/*/; do
            if [ -d "$script_dir" ]; then
                script_name=$(basename "$script_dir")
                if [ -f "$script_dir/SKILL.md" ] && [ -f "$script_dir/README.md" ]; then
                    echo "  - ✅ $script_name（完整）" >> "$LOG_FILE"
                else
                    echo "  - ⚠️ $script_name（缺少 SKILL.md 或 README.md）" >> "$LOG_FILE"
                fi
            fi
        done
    else
        echo "- ❌ scripts 文件夹不存在" >> "$LOG_FILE"
    fi
    
    echo "" >> "$LOG_FILE"
    
    # 2.3 维护项目表
    echo "### 维护项目表" >> "$LOG_FILE"
    projects_dir="$HOME/实验室仓库/项目文件"
    if [ -d "$projects_dir" ]; then
        project_count=$(find "$projects_dir" -mindepth 1 -maxdepth 1 -type d | wc -l)
        echo "- 发现 $project_count 个项目" >> "$LOG_FILE"
        
        # 检查每个项目的完整性
        for project_dir in "$projects_dir"/*/; do
            if [ -d "$project_dir" ]; then
                project_name=$(basename "$project_dir")
                has_readme=false
                has_metadata=false
                
                [ -f "$project_dir/README.md" ] && has_readme=true
                [ -f "$project_dir/元数据.json" ] && has_metadata=true
                
                if [ "$has_readme" = true ] && [ "$has_metadata" = true ]; then
                    echo "  - ✅ $project_name（完整）" >> "$LOG_FILE"
                else
                    missing=""
                    [ "$has_readme" = false ] && missing="$missing README.md"
                    [ "$has_metadata" = false ] && missing="$missing 元数据.json"
                    echo "  - ⚠️ $project_name（缺少$missing）" >> "$LOG_FILE"
                fi
            fi
        done
    else
        echo "- ❌ 项目文件夹不存在" >> "$LOG_FILE"
    fi
fi

echo "" >> "$LOG_FILE"

# ==================== 3. 工作空间维护 ====================
echo "## 3. 工作空间维护" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# 3.1 检查配置文件
echo "### 检查配置文件" >> "$LOG_FILE"
config_files=("AGENTS.md" "MEMORY.md" "TOOLS.md" "IDENTITY.md" "SOUL.md" "USER.md" "HEARTBEAT.md")
for file in "${config_files[@]}"; do
    if [ -f "$WORKSPACE/$file" ]; then
        echo "- ✅ $file" >> "$LOG_FILE"
    else
        echo "- ❌ $file（缺失）" >> "$LOG_FILE"
    fi
done

echo "" >> "$LOG_FILE"

# 3.2 维护临时文件夹
echo "### 维护临时文件夹" >> "$LOG_FILE"
temp_dir="$WORKSPACE/temp"
if [ -d "$temp_dir" ]; then
    # 删除超过24小时的文件
    find "$temp_dir" -type f -mtime +1 -delete 2>/dev/null
    find "$temp_dir" -type d -empty -delete 2>/dev/null
    echo "- ✅ 已清理超过24小时的临时文件" >> "$LOG_FILE"
else
    echo "- ⚠️ temp 文件夹不存在" >> "$LOG_FILE"
fi

echo "" >> "$LOG_FILE"

# 3.3 维护技能文件夹
echo "### 维护技能文件夹" >> "$LOG_FILE"
if [ -d "$skills_dir" ]; then
    # 确保每个技能都有 SKILL.md 和 README.md
    for skill_dir in "$skills_dir"/*/; do
        if [ -d "$skill_dir" ]; then
            skill_name=$(basename "$skill_dir")
            [ ! -f "$skill_dir/SKILL.md" ] && echo "- ⚠️ $skill_name 缺少 SKILL.md" >> "$LOG_FILE"
            [ ! -f "$skill_dir/README.md" ] && echo "- ⚠️ $skill_name 缺少 README.md" >> "$LOG_FILE"
        fi
    done
    echo "- ✅ 技能文件夹检查完成" >> "$LOG_FILE"
else
    echo "- ❌ skills 文件夹不存在" >> "$LOG_FILE"
fi

echo "" >> "$LOG_FILE"

# 3.4 维护脚本文件夹
echo "### 维护脚本文件夹" >> "$LOG_FILE"
if [ -d "$scripts_dir" ]; then
    echo "- ✅ 脚本文件夹存在" >> "$LOG_FILE"
else
    echo "- ⚠️ scripts 文件夹不存在" >> "$LOG_FILE"
fi

echo "" >> "$LOG_FILE"

# 3.5 删除多余文件（备份文件）
echo "### 清理多余文件" >> "$LOG_FILE"
backup_count=$(find "$WORKSPACE" -maxdepth 1 -name "*.bak.*" -type f | wc -l)
if [ "$backup_count" -gt 5 ]; then
    # 只保留最近5个备份
    ls -t "$WORKSPACE"/*.bak.* 2>/dev/null | tail -n +6 | xargs -r rm
    echo "- ✅ 已清理旧备份文件（保留最近5个）" >> "$LOG_FILE"
else
    echo "- ✅ 备份文件数量正常（$backup_count 个）" >> "$LOG_FILE"
fi

echo "" >> "$LOG_FILE"
echo "## 维护完成" >> "$LOG_FILE"
echo "完成时间：$(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"

echo "每日维护任务完成，日志已保存到：$LOG_FILE"
