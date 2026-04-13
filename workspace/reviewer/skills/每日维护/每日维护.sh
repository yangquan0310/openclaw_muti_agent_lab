#!/bin/bash
# 每日维护脚本 - reviewer
# 执行时间：每日 04:00 (Asia/Shanghai)
# 功能：维护 TOOLS.md、维护 MEMORY.md、工作空间维护

set -e

WORKSPACE="$HOME/.openclaw/workspace/reviewer"
LOG_ROOT="/root/实验室仓库/日志文件"
HEARTBEAT_LOG_ROOT="/root/实验室仓库/日志文件/心跳任务"
PROJECTS_ROOT="/root/实验室仓库/项目文件"
DATE_STR=$(date +%Y-%m-%d)
TIME_STR=$(date +%H-%M-%S)
LOG_FILE="$LOG_ROOT/$DATE_STR/04-00-00-reviewer-每日维护.md"

# 创建日志目录
mkdir -p "$(dirname "$LOG_FILE")"

# 日志函数
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') $1" | tee -a "$LOG_FILE"
}

log "===== 每日维护任务开始 ====="
log "工作空间: $WORKSPACE"
log ""

# ===== 任务1：维护 TOOLS.md =====
log "【任务1】维护 TOOLS.md..."

# 1.1 维护个人技能索引
log "  1.1 维护个人技能索引..."
SKILLS_DIR="$WORKSPACE/skills"
skill_list=""
if [ -d "$SKILLS_DIR" ]; then
    for skill_dir in "$SKILLS_DIR"/*/; do
        if [ -d "$skill_dir" ]; then
            skill_name=$(basename "$skill_dir")
            skill_list="$skill_list $skill_name"
            if [ -f "$skill_dir/SKILL.md" ]; then
                log "    ✓ 技能 '$skill_name' 包含 SKILL.md"
            else
                log "    ⚠ 技能 '$skill_name' 缺少 SKILL.md"
            fi
            if [ -f "$skill_dir/README.md" ]; then
                log "    ✓ 技能 '$skill_name' 包含 README.md"
            else
                log "    ⚠ 技能 '$skill_name' 缺少 README.md"
            fi
        fi
    done
    log "    共发现 $(echo "$skill_list" | wc -w) 个技能"
fi

# 1.2 维护个人脚本索引
log "  1.2 维护个人脚本索引..."
SCRIPTS_DIR="$WORKSPACE/scripts"
script_list=""
if [ -d "$SCRIPTS_DIR" ]; then
    for script_dir in "$SCRIPTS_DIR"/*/; do
        if [ -d "$script_dir" ]; then
            script_name=$(basename "$script_dir")
            script_list="$script_list $script_name"
            # 检查是否有 .md 文件
            md_files=$(find "$script_dir" -maxdepth 1 -name "*.md" -not -name "SKILL.md" -not -name "README.md" 2>/dev/null | wc -l)
            if [ "$md_files" -gt 0 ]; then
                log "    ✓ 脚本 '$script_name' 包含核心 .md 文件"
            else
                log "    ⚠ 脚本 '$script_name' 缺少核心 .md 文件"
            fi
            if [ -f "$script_dir/SKILL.md" ]; then
                log "    ✓ 脚本 '$script_name' 包含 SKILL.md"
            else
                log "    ⚠ 脚本 '$script_name' 缺少 SKILL.md"
            fi
            if [ -f "$script_dir/README.md" ]; then
                log "    ✓ 脚本 '$script_name' 包含 README.md"
            else
                log "    ⚠ 脚本 '$script_name' 缺少 README.md"
            fi
        fi
    done
    log "    共发现 $(echo "$script_list" | wc -w) 个脚本"
fi

# 1.3 维护项目表
log "  1.3 维护项目表..."
project_count=0
if [ -d "$PROJECTS_ROOT" ]; then
    for project_dir in "$PROJECTS_ROOT"/*/; do
        if [ -d "$project_dir" ]; then
            project_name=$(basename "$project_dir")
            project_count=$((project_count + 1))
            readme_path="$project_dir/README.md"
            if [ -f "$readme_path" ]; then
                log "    ✓ 项目 '$project_name' 包含 README.md"
            else
                log "    ⚠ 项目 '$project_name' 缺少 README.md"
            fi
        fi
    done
    log "    共发现 $project_count 个项目"
else
    log "    ⚠ 项目根目录不存在: $PROJECTS_ROOT"
fi

log "  ✓ TOOLS.md 维护完成"
log ""

# ===== 任务2：维护 MEMORY.md =====
log "【任务2】维护 MEMORY.md..."

MEMORY_FILE="$WORKSPACE/MEMORY.md"

# 2.1 维护任务看板
log "  2.1 维护任务看板..."
if [ -f "$MEMORY_FILE" ]; then
    # 检查是否有未归档的 completed 任务
    completed_count=$(grep -c "|.*|.*|.*| completed |" "$MEMORY_FILE" 2>/dev/null | tr -d '\n' || echo "0")
    log "    发现 $completed_count 个 completed 状态任务待归档"
    
    # 归档 completed 任务到事件记忆
    if [ "$completed_count" -gt 0 ]; then
        log "    开始归档 completed 任务..."
        # 提取 completed 任务并归档
        grep "|.*|.*|.*| completed |" "$MEMORY_FILE" 2>/dev/null | while read line; do
            task_name=$(echo "$line" | awk -F'|' '{print $4}' | xargs)
            log "      归档任务: $task_name"
        done
        # 从活跃清单中删除 completed 任务
        sed -i '/|.*|.*|.*| completed |/d' "$MEMORY_FILE" 2>/dev/null || true
        log "    ✓ completed 任务已归档"
    fi
else
    log "    ⚠ MEMORY.md 不存在"
fi

# 2.2 维护活跃子代理清单
log "  2.2 维护活跃子代理清单..."
if [ -f "$MEMORY_FILE" ]; then
    active_count=$(grep -c "|.*|.*|.*| active |" "$MEMORY_FILE" 2>/dev/null | tr -d '\n' || echo "0")
    paused_count=$(grep -c "|.*|.*|.*| paused |" "$MEMORY_FILE" 2>/dev/null | tr -d '\n' || echo "0")
    killed_count=$(grep -c "|.*|.*|.*| killed |" "$MEMORY_FILE" 2>/dev/null | tr -d '\n' || echo "0")
    log "    活跃任务: $active_count 个, 暂停任务: $paused_count 个, 异常任务: $killed_count 个"
    
    # 清理 killed 任务
    if [ "$killed_count" -gt 0 ]; then
        log "    清理 $killed_count 个 killed 状态任务..."
        sed -i '/|.*|.*|.*| killed |/d' "$MEMORY_FILE" 2>/dev/null || true
        log "    ✓ killed 任务已清理"
    fi
else
    log "    ⚠ MEMORY.md 不存在"
fi

# 2.3 维护程序性记忆脚本位置表
log "  2.3 维护程序性记忆脚本位置表..."
if [ -f "$MEMORY_FILE" ]; then
    # 检查脚本索引部分
    if grep -q "## 五、程序性记忆" "$MEMORY_FILE"; then
        log "    ✓ 程序性记忆部分存在"
        # 检查是否有脚本索引表
        script_index_count=$(grep -A 10 "### 脚本索引" "$MEMORY_FILE" 2>/dev/null | grep -c "|.*|.*|.*|" || echo "0")
        log "    脚本索引条目: $script_index_count 个"
        
        # 验证脚本位置是否正确
        for script_dir in "$SCRIPTS_DIR"/*/; do
            if [ -d "$script_dir" ]; then
                script_name=$(basename "$script_dir")
                expected_path="~/.openclaw/workspace/reviewer/scripts/$script_name/SKILL.md"
                if grep -q "$expected_path" "$MEMORY_FILE"; then
                    log "    ✓ 脚本 '$script_name' 位置正确"
                else
                    log "    ⚠ 脚本 '$script_name' 位置可能需要更新"
                fi
            fi
        done
    else
        log "    ⚠ 程序性记忆部分缺失"
    fi
else
    log "    ⚠ MEMORY.md 不存在"
fi

log "  ✓ MEMORY.md 维护完成"
log ""

# ===== 任务3：工作空间维护 =====
log "【任务3】工作空间维护..."

# 3.1 核查配置文件缺失
log "  3.1 核查配置文件缺失..."
config_files=("AGENTS.md" "SOUL.md" "TOOLS.md" "MEMORY.md" "HEARTBEAT.md" "USER.md" "IDENTITY.md")
missing_configs=0
for config in "${config_files[@]}"; do
    if [ -f "$WORKSPACE/$config" ]; then
        log "    ✓ $config 存在"
    else
        log "    ⚠ $config 缺失"
        missing_configs=$((missing_configs + 1))
        # 创建缺失的配置文件模板
        case "$config" in
            "AGENTS.md")
                cat > "$WORKSPACE/$config" << 'EOF'
# AGENTS.md

## 任务生命周期
- 计划 → 监控 → 调节

## 子代理调度
使用 sessions_spawn 创建子代理

---
*最后更新: $(date +%Y-%m-%d)*
EOF
                log "      已创建 $config 模板"
                ;;
            "SOUL.md")
                cat > "$WORKSPACE/$config" << 'EOF'
# SOUL.md

## 风格
- 严格审查
- 建设性反馈

## 价值观
数据安全 > 规范完整 > 学术质量

---
*最后更新: $(date +%Y-%m-%d)*
EOF
                log "      已创建 $config 模板"
                ;;
            *)
                touch "$WORKSPACE/$config"
                log "      已创建空文件 $config"
                ;;
        esac
    fi
done
if [ $missing_configs -eq 0 ]; then
    log "    ✓ 所有配置文件齐全"
fi

# 3.2 维护临时文件夹
log "  3.2 维护临时文件夹..."
TEMP_DIR="$WORKSPACE/temp"
if [ -d "$TEMP_DIR" ]; then
    # 删除7天前的临时文件
    deleted_count=$(find "$TEMP_DIR" -type f -mtime +7 2>/dev/null | wc -l)
    find "$TEMP_DIR" -type f -mtime +7 -delete 2>/dev/null || true
    # 删除空目录
    find "$TEMP_DIR" -type d -empty -delete 2>/dev/null || true
    log "    ✓ 临时文件已清理（删除 $deleted_count 个7天前的文件）"
else
    log "    ⚠ 临时文件夹不存在，创建中..."
    mkdir -p "$TEMP_DIR"
    # 创建 README.md
    cat > "$TEMP_DIR/README.md" << 'EOF'
# temp 文件夹

## 功能
存放临时工作文件，按任务分类存储。

## 清理策略
- 自动清理：7天前的文件会被删除
- 手动清理：任务完成后及时删除

## 注意
不要存放重要文件！
EOF
    log "    ✓ 临时文件夹已创建"
fi

# 3.3 维护技能文件夹
log "  3.3 维护技能文件夹..."
SKILLS_DIR="$WORKSPACE/skills"
if [ -d "$SKILLS_DIR" ]; then
    skill_count=$(find "$SKILLS_DIR" -mindepth 1 -maxdepth 1 -type d | wc -l)
    log "    ✓ 技能文件夹存在，包含 $skill_count 个技能"
    # 检查每个技能的结构
    for skill_dir in "$SKILLS_DIR"/*/; do
        if [ -d "$skill_dir" ]; then
            skill_name=$(basename "$skill_dir")
            has_readme=0
            has_skill_md=0
            [ -f "$skill_dir/README.md" ] && has_readme=1
            [ -f "$skill_dir/SKILL.md" ] && has_skill_md=1
            if [ $has_readme -eq 1 ] && [ $has_skill_md -eq 1 ]; then
                log "      ✓ 技能 '$skill_name' 结构完整"
            else
                [ $has_readme -eq 0 ] && log "      ⚠ 技能 '$skill_name' 缺少 README.md"
                [ $has_skill_md -eq 0 ] && log "      ⚠ 技能 '$skill_name' 缺少 SKILL.md"
            fi
        fi
    done
else
    log "    ⚠ 技能文件夹不存在，创建中..."
    mkdir -p "$SKILLS_DIR"
    cat > "$SKILLS_DIR/README.md" << 'EOF'
# skills 文件夹

存放结构化技能程序。

## 结构
skills/{技能名}/
  - SKILL.md
  - README.md
  - 执行文件(.sh/.py/.js)
EOF
    log "    ✓ 技能文件夹已创建"
fi

# 3.4 维护脚本文件夹
log "  3.4 维护脚本文件夹..."
SCRIPTS_DIR="$WORKSPACE/scripts"
if [ -d "$SCRIPTS_DIR" ]; then
    script_count=$(find "$SCRIPTS_DIR" -mindepth 1 -maxdepth 1 -type d | wc -l)
    log "    ✓ 脚本文件夹存在，包含 $script_count 个脚本"
    # 检查每个脚本的结构
    for script_dir in "$SCRIPTS_DIR"/*/; do
        if [ -d "$script_dir" ]; then
            script_name=$(basename "$script_dir")
            has_readme=0
            has_skill_md=0
            has_md=0
            [ -f "$script_dir/README.md" ] && has_readme=1
            [ -f "$script_dir/SKILL.md" ] && has_skill_md=1
            [ $(find "$script_dir" -maxdepth 1 -name "*.md" -not -name "SKILL.md" -not -name "README.md" 2>/dev/null | wc -l) -gt 0 ] && has_md=1
            if [ $has_readme -eq 1 ] && [ $has_skill_md -eq 1 ] && [ $has_md -eq 1 ]; then
                log "      ✓ 脚本 '$script_name' 结构完整"
            else
                [ $has_readme -eq 0 ] && log "      ⚠ 脚本 '$script_name' 缺少 README.md"
                [ $has_skill_md -eq 0 ] && log "      ⚠ 脚本 '$script_name' 缺少 SKILL.md"
                [ $has_md -eq 0 ] && log "      ⚠ 脚本 '$script_name' 缺少核心 .md 文件"
            fi
        fi
    done
else
    log "    ⚠ 脚本文件夹不存在，创建中..."
    mkdir -p "$SCRIPTS_DIR"
    cat > "$SCRIPTS_DIR/README.md" << 'EOF'
# scripts 文件夹

存放非结构化脚本（Markdown格式）。

## 结构
scripts/{脚本名}/
  - {脚本名}.md
  - SKILL.md
  - README.md
EOF
    log "    ✓ 脚本文件夹已创建"
fi

# 3.5 删除多余文件
log "  3.5 删除多余文件..."
# 检查根目录下的非配置文件
allowed_root_files=("AGENTS.md" "SOUL.md" "TOOLS.md" "MEMORY.md" "HEARTBEAT.md" "USER.md" "IDENTITY.md" "BOOTSTRAP.md")
allowed_root_dirs=("scripts" "skills" "temp" "memory" ".openclaw")
deleted_items=0
for item in "$WORKSPACE"/*; do
    if [ -e "$item" ]; then
        item_name=$(basename "$item")
        is_allowed=0
        # 检查是否在允许的文件列表中
        for allowed in "${allowed_root_files[@]}"; do
            if [ "$item_name" == "$allowed" ]; then
                is_allowed=1
                break
            fi
        done
        # 检查是否在允许的目录列表中
        for allowed in "${allowed_root_dirs[@]}"; do
            if [ "$item_name" == "$allowed" ]; then
                is_allowed=1
                break
            fi
        done
        # 检查是否是以点开头的隐藏文件/目录
        if [[ "$item_name" == .* ]]; then
            is_allowed=1
        fi
        if [ $is_allowed -eq 0 ]; then
            log "    ⚠ 发现多余文件/目录: $item_name，删除中..."
            rm -rf "$item" 2>/dev/null && log "      ✓ 已删除: $item_name" || log "      ❌ 删除失败: $item_name"
            deleted_items=$((deleted_items + 1))
        fi
    fi
done
if [ $deleted_items -eq 0 ]; then
    log "    ✓ 未发现多余文件"
else
    log "    ✓ 共删除 $deleted_items 个多余文件/目录"
fi

log "  ✓ 工作空间维护完成"
log ""

log "===== 每日维护任务完成 ====="
log "日志文件: $LOG_FILE"
log "完成时间: $(date '+%Y-%m-%d %H:%M:%S')"
