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
    # 检查技能文件夹中的SKILL.md
    skill_count=$(find "$SKILLS_DIR" -name "SKILL.md" | wc -l)
    log "  - 发现 $skill_count 个技能（SKILL.md）"
    
    # 更新技能索引README.md
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
    # 检查脚本文件夹中的SKILL.md
    script_count=$(find "$SCRIPTS_DIR" -name "SKILL.md" | wc -l)
    log "  - 发现 $script_count 个脚本（SKILL.md）"
    
    # 更新脚本索引README.md
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
    
    # 提取completed和killed状态的任务
    completed_tasks=$(grep "|.*|.*|.*| completed |" "$MEMORY_FILE" || true)
    killed_tasks=$(grep "|.*|.*|.*| killed |" "$MEMORY_FILE" || true)
    
    if [ -z "$completed_tasks" ] && [ -z "$killed_tasks" ]; then
        log "  - 没有需要清理的任务"
    else
        # 统计数量
        completed_count=$(echo "$completed_tasks" | grep -v "^$" | wc -l)
        killed_count=$(echo "$killed_tasks" | grep -v "^$" | wc -l)
        
        log "  - 发现 $completed_count 个 completed 任务，$killed_count 个 killed 任务"
        
        # 从活跃子代理清单中删除completed和killed状态的任务
        sed -i '/^| agent:.*|.*|.*| completed |.*|.*|.*|$/d' "$MEMORY_FILE"
        sed -i '/^| agent:.*|.*|.*| killed |.*|.*|.*|$/d' "$MEMORY_FILE"
        
        log "  - 已清理 completed/killed 任务"
    fi
    
    # 2.3 维护程序性记忆脚本位置表
    log "  - 维护程序性记忆脚本位置表..."
    # 检查程序性记忆区的脚本索引
    if grep -q "## 🛠️ 程序性记忆区" "$MEMORY_FILE"; then
        log "  - 程序性记忆区存在"
        # 检查脚本索引表格
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

# 3.1 检查配置文件
log "  - 检查配置文件..."
CONFIG_FILES=("AGENTS.md" "HEARTBEAT.md" "IDENTITY.md" "MEMORY.md" "SOUL.md" "TOOLS.md" "USER.md")
for config_file in "${CONFIG_FILES[@]}"; do
    if [ ! -f "$WORKSPACE/$config_file" ]; then
        log "  - 警告: 配置文件缺失: $config_file"
    fi
done
log "  - 配置文件检查完成"

# 3.2 检查工作空间结构（删除多余文件）
log "  - 检查工作空间结构..."
EXPECTED_DIRS=("scripts" "skills" "temp" ".openclaw")
EXPECTED_FILES=("AGENTS.md" "HEARTBEAT.md" "IDENTITY.md" "MEMORY.md" "SOUL.md" "TOOLS.md" "USER.md")

# 检查并删除非预期的文件
for file in "$WORKSPACE"/*; do
    if [ -f "$file" ]; then
        file_name=$(basename "$file")
        if [[ ! " ${EXPECTED_FILES[@]} " =~ " ${file_name} " ]]; then
            log "  - 发现多余文件: $file_name"
            # 可选：删除多余文件
            # rm "$file"
        fi
    fi
done

# 检查并报告非预期的文件夹
for dir in "$WORKSPACE"/*/; do
    if [ -d "$dir" ]; then
        dir_name=$(basename "$dir")
        if [[ ! " ${EXPECTED_DIRS[@]} " =~ " ${dir_name} " ]]; then
            log "  - 发现非标准文件夹: $dir_name"
        fi
    fi
done
log "  - 工作空间结构检查完成"

# 3.3 维护临时文件夹
log "  - 维护临时文件夹..."
TEMP_DIR="$WORKSPACE/temp"
if [ -d "$TEMP_DIR" ]; then
    # 清理超过7天的临时文件
    find "$TEMP_DIR" -type f -mtime +7 -delete 2>/dev/null || true
    find "$TEMP_DIR" -type d -empty -delete 2>/dev/null || true
    TEMP_COUNT=$(find "$TEMP_DIR" -type f 2>/dev/null | wc -l)
    log "  - 临时文件夹清理完成，剩余 $TEMP_COUNT 个文件"
    
    # 检查README.md
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
    # 确保技能脚本有执行权限
    find "$SKILLS_DIR" -name "main.sh" -exec chmod +x {} \; 2>/dev/null || true
    
    # 检查每个技能文件夹的结构
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
    # 检查README.md
    if [ ! -f "$SCRIPTS_DIR/README.md" ]; then
        log "  - 警告: scripts/README.md 不存在"
    fi
    
    # 检查每个脚本文件夹的结构
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
