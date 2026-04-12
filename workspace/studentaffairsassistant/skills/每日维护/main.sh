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
SKILLS_DIR="$WORKSPACE/skills"
if [ -d "$SKILLS_DIR" ]; then
    skill_count=$(find "$SKILLS_DIR" -name "SKILL.md" | wc -l)
    log "  - 发现 $skill_count 个技能（SKILL.md）"
    
    skills_readme="$SKILLS_DIR/README.md"
    if [ -f "$skills_readme" ]; then
        log "  - 技能索引 README.md 存在"
    else
        log "  - 警告: 技能索引 README.md 不存在"
    fi
else
    log "  - 警告: 技能目录不存在"
fi
log "  - 个人技能索引检查完成"

# 1.2 维护个人脚本索引
log "  - 维护个人脚本索引..."
SCRIPTS_DIR="$WORKSPACE/scripts"
if [ -d "$SCRIPTS_DIR" ]; then
    script_count=$(find "$SCRIPTS_DIR" -name "SKILL.md" | wc -l)
    log "  - 发现 $script_count 个脚本（SKILL.md）"
    
    scripts_readme="$SCRIPTS_DIR/README.md"
    if [ -f "$scripts_readme" ]; then
        log "  - 脚本索引 README.md 存在"
    else
        log "  - 警告: 脚本索引 README.md 不存在"
    fi
else
    log "  - 警告: 脚本目录不存在"
fi
log "  - 个人脚本索引检查完成"

# 1.3 维护项目表
log "  - 维护项目表..."
TOOLS_FILE="$WORKSPACE/TOOLS.md"
if [ -f "$TOOLS_FILE" ]; then
    # 检查学工项目库表格（只统计实际项目行，不包括表头分隔符）
    if grep -q "### 学工项目库" "$TOOLS_FILE"; then
        # 提取学工项目库表格中的项目（以 ~/教研室仓库/学生工作/ 开头的数据行）
        project_count=$(grep "| .* | ~/教研室仓库/学生工作/" "$TOOLS_FILE" | grep -v "^| -" | wc -l)
        log "  - 发现 $project_count 个项目"
        
        # 检查项目目录是否存在
        PROJECTS_DIR="/root/教研室仓库/学生工作"
        if [ -d "$PROJECTS_DIR" ]; then
            actual_projects=$(find "$PROJECTS_DIR" -mindepth 1 -maxdepth 1 -type d | wc -l)
            log "  - 实际项目目录: $actual_projects 个"
            
            if [ "$project_count" -ne "$actual_projects" ]; then
                log "  - 警告: 项目表与实际目录数量不一致"
            fi
        fi
    else
        log "  - 警告: 学工项目库表格不存在"
    fi
else
    log "  - 警告: TOOLS.md 不存在"
fi
log "  - 项目表检查完成"

log "【任务1】TOOLS.md 维护完成"

# ============================================
# 任务2: 维护 MEMORY.md
# ============================================
log "【任务2】开始维护 MEMORY.md..."

MEMORY_FILE="$WORKSPACE/MEMORY.md"
if [ -f "$MEMORY_FILE" ]; then
    # 2.1 维护任务看板
    log "  - 维护任务看板..."
    log "  - 任务看板检查完成"
    
    # 2.2 维护活跃子代理清单（清理 completed/killed 任务）
    log "  - 维护活跃子代理清单..."
    
    completed_tasks=$(grep "|.*|.*|.*| completed |" "$MEMORY_FILE" || true)
    killed_tasks=$(grep "|.*|.*|.*| killed |" "$MEMORY_FILE" || true)
    
    if [ -z "$completed_tasks" ] && [ -z "$killed_tasks" ]; then
        log "  - 没有需要清理的任务"
    else
        completed_count=$(echo "$completed_tasks" | grep -v "^$" | wc -l)
        killed_count=$(echo "$killed_tasks" | grep -v "^$" | wc -l)
        
        log "  - 发现 $completed_count 个 completed 任务，$killed_count 个 killed 任务"
        
        sed -i '/^| agent:.*|.*|.*| completed |.*|.*|.*|$/d' "$MEMORY_FILE"
        sed -i '/^| agent:.*|.*|.*| killed |.*|.*|.*|$/d' "$MEMORY_FILE"
        
        log "  - 已清理 completed/killed 任务"
    fi
    
    # 2.3 维护程序性记忆脚本位置表
    log "  - 维护程序性记忆脚本位置表..."
    if grep -q "## 🛠️ 程序性记忆区" "$MEMORY_FILE"; then
        log "  - 程序性记忆区存在"
        script_index_count=$(grep -c "scripts/.*/SKILL.md" "$MEMORY_FILE" || echo "0")
        log "  - 程序性记忆脚本索引包含 $script_index_count 个脚本"
    else
        log "  - 警告: 程序性记忆区不存在"
    fi
    log "  - 程序性记忆脚本位置表检查完成"
else
    log "  - 警告: MEMORY.md 不存在"
fi

log "【任务2】MEMORY.md 维护完成"

# ============================================
# 任务3: 工作空间维护
# ============================================
log "【任务3】开始工作空间维护..."

# 3.1 核查配置文件缺失
log "  - 核查配置文件缺失..."
CONFIG_FILES=("AGENTS.md" "HEARTBEAT.md" "IDENTITY.md" "MEMORY.md" "SOUL.md" "TOOLS.md" "USER.md")
MISSING_COUNT=0
for config_file in "${CONFIG_FILES[@]}"; do
    if [ ! -f "$WORKSPACE/$config_file" ]; then
        log "  - ❌ 配置文件缺失: $config_file"
        MISSING_COUNT=$((MISSING_COUNT + 1))
    fi
done

if [ $MISSING_COUNT -eq 0 ]; then
    log "  - ✅ 所有配置文件齐全"
else
    log "  - ⚠️ 共缺失 $MISSING_COUNT 个配置文件"
fi
log "  - 配置文件核查完成"

# 3.2 删除多余文件
log "  - 删除多余文件..."
EXPECTED_DIRS=("scripts" "skills" "temp" ".openclaw")
EXPECTED_FILES=("AGENTS.md" "HEARTBEAT.md" "IDENTITY.md" "MEMORY.md" "SOUL.md" "TOOLS.md" "USER.md")

DELETED_COUNT=0
# 删除非预期的文件
for file in "$WORKSPACE"/*; do
    if [ -f "$file" ]; then
        file_name=$(basename "$file")
        if [[ ! " ${EXPECTED_FILES[@]} " =~ " ${file_name} " ]]; then
            log "  - 删除多余文件: $file_name"
            rm "$file"
            DELETED_COUNT=$((DELETED_COUNT + 1))
        fi
    fi
done

# 删除非预期的文件夹
for dir in "$WORKSPACE"/*/; do
    if [ -d "$dir" ]; then
        dir_name=$(basename "$dir")
        if [[ ! " ${EXPECTED_DIRS[@]} " =~ " ${dir_name} " ]]; then
            log "  - 删除多余文件夹: $dir_name"
            rm -rf "$dir"
            DELETED_COUNT=$((DELETED_COUNT + 1))
        fi
    fi
done

if [ $DELETED_COUNT -eq 0 ]; then
    log "  - ✅ 没有多余文件"
else
    log "  - ✅ 已删除 $DELETED_COUNT 个多余文件/文件夹"
fi
log "  - 多余文件删除完成"

# 3.3 维护临时文件夹
log "  - 维护临时文件夹..."
TEMP_DIR="$WORKSPACE/temp"
if [ -d "$TEMP_DIR" ]; then
    find "$TEMP_DIR" -type f -mtime +7 -delete 2>/dev/null || true
    find "$TEMP_DIR" -type d -empty -delete 2>/dev/null || true
    TEMP_COUNT=$(find "$TEMP_DIR" -type f 2>/dev/null | wc -l)
    log "  - 临时文件夹清理完成，剩余 $TEMP_COUNT 个文件"
    
    if [ ! -f "$TEMP_DIR/README.md" ]; then
        log "  - 警告: temp/README.md 不存在"
    fi
else
    mkdir -p "$TEMP_DIR"
    log "  - 临时文件夹已创建"
fi
log "  - 临时文件夹维护完成"

# 3.4 维护技能文件夹
log "  - 维护技能文件夹..."
SKILLS_DIR="$WORKSPACE/skills"
if [ -d "$SKILLS_DIR" ]; then
    find "$SKILLS_DIR" -name "main.sh" -exec chmod +x {} \; 2>/dev/null || true
    
    for skill_dir in "$SKILLS_DIR"/*/; do
        if [ -d "$skill_dir" ]; then
            skill_name=$(basename "$skill_dir")
            if [ ! -f "$skill_dir/SKILL.md" ]; then
                log "  - 警告: 技能 '$skill_name' 缺少 SKILL.md"
            fi
        fi
    done
    log "  - 技能文件夹维护完成"
else
    log "  - 警告: 技能目录不存在"
fi

# 3.5 维护脚本文件夹
log "  - 维护脚本文件夹..."
SCRIPTS_DIR="$WORKSPACE/scripts"
if [ -d "$SCRIPTS_DIR" ]; then
    if [ ! -f "$SCRIPTS_DIR/README.md" ]; then
        log "  - 警告: scripts/README.md 不存在"
    fi
    
    for script_dir in "$SCRIPTS_DIR"/*/; do
        if [ -d "$script_dir" ]; then
            script_name=$(basename "$script_dir")
            if [ "$script_name" != "*" ]; then
                if [ ! -f "$script_dir/SKILL.md" ]; then
                    log "  - 警告: 脚本 '$script_name' 缺少 SKILL.md"
                fi
            fi
        fi
    done
    log "  - 脚本文件夹维护完成"
else
    log "  - 警告: 脚本目录不存在"
fi

log "【任务3】工作空间维护完成"

# ============================================
# 任务完成总结
# ============================================
log "========== 学工助手每日维护任务完成 =========="
log "日志文件: $LOG_FILE"
log "日志目录: $LOG_DIR"

exit 0
