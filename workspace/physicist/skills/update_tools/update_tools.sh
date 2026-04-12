#!/bin/bash
set -e

# 配置参数
WORKSPACE="/root/.openclaw/workspace/physicist"
TOOLS_FILE="$WORKSPACE/TOOLS.md"
MEMORY_FILE="$WORKSPACE/MEMORY.md"
PROJECTS_DIR="/root/实验室仓库/项目文件"
LOG_DIR_BASE="/root/实验室仓库/日志文件"
SCRIPTS_DIR="/root/.openclaw/workspace/physicist/scripts"
AGENT_NAME="physicist"
TASK_TYPE="TOOLS更新"

# 获取当前时间
CURRENT_DATE=$(date +"%Y-%m-%d")
CURRENT_TIME=$(date +"%H-%M-%S")
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# 创建日志目录
LOG_DIR="$LOG_DIR_BASE/$CURRENT_DATE"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/${CURRENT_TIME}-[${AGENT_NAME}]-[${TASK_TYPE}].md"

# 日志函数
log() {
    local level="$1"
    local message="$2"
    echo "[$TIMESTAMP] [$level] $message" >> "$LOG_FILE"
    echo "[$level] $message"
}

# 开始执行
log "INFO" "开始执行TOOLS.md更新任务"

# 备份原始TOOLS.md
BACKUP_FILE="$TOOLS_FILE.backup.$CURRENT_DATE"
cp "$TOOLS_FILE" "$BACKUP_FILE"
log "INFO" "已备份原始TOOLS.md到 $BACKUP_FILE"

# --------------------------
# 1. 更新存储位置表
# --------------------------
log "INFO" "步骤1: 更新存储位置表"

# 检查是否已存在脚本存储位置条目
if ! grep -q "脚本存储位置" "$TOOLS_FILE"; then
    # 找到存储位置表的结束位置（第一个 | 文件 | 存储路径 | 说明 | 之后的表结束）
    awk -v scripts_path="$SCRIPTS_DIR" '
        /^\| 文件 \| 存储路径 \| 说明 \|$/ {
            print
            print "| 脚本存储位置 | " scripts_path " | 物理学家Agent自定义脚本存储目录 |"
            next
        }
        1
    ' "$TOOLS_FILE" > "${TOOLS_FILE}.tmp" && mv "${TOOLS_FILE}.tmp" "$TOOLS_FILE"
    log "INFO" "已添加脚本存储位置到存储位置表"
else
    log "INFO" "脚本存储位置已存在，跳过添加"
fi

# --------------------------
# 2. 更新项目列表
# --------------------------
log "INFO" "步骤2: 更新项目列表"

# 获取现有项目列表
existing_projects=$(awk '/^\| 项目名 \| 存储位置 \| 描述 \|$/,/^---$/ {
    if ($0 ~ /^\| [^\|]+ \| [^\|]+ \| [^\|]+ \|$/ && $0 !~ /^\| 项目名 \| 存储位置 \| 描述 \|$/) {
        gsub(/^\| | \|$/, "", $0)
        split($0, parts, / *\| */)
        print parts[1] "|" parts[2]
    }
}' "$TOOLS_FILE")

# 获取实际存在的项目
actual_projects=()
for project_dir in "$PROJECTS_DIR"/20*; do
    if [ -d "$project_dir" ] && [[ $(basename "$project_dir") =~ ^20[0-9]{2}-[0-9]{2}-[0-9]{2}_ ]]; then
        project_name=$(basename "$project_dir")
        project_path="$project_dir"
        # 尝试读取README.md获取描述
        description=""
        if [ -f "$project_dir/README.md" ]; then
            description=$(head -n 3 "$project_dir/README.md" | grep -v "^#" | head -n 1 | sed 's/^[> ]*//' | tr -d '\n' | cut -c 1-100)
        fi
        if [ -z "$description" ]; then
            description="项目目录"
        fi
        actual_projects+=("$project_name|$project_path|$description")
    fi
done

# 生成新的项目列表
new_projects_section="### 项目

| 项目名 | 存储位置 | 描述 |
|--------|----------|------|"

for project in "${actual_projects[@]}"; do
    IFS='|' read -r name path desc <<< "$project"
    new_projects_section+="
| $name | $path | $desc |"
done

# 替换项目列表部分 - 先删除所有现有项目部分，再插入新的
awk '
    /^### 项目$/ {
        in_projects = 1
        next
    }
    in_projects && /^### / {
        in_projects = 0
    }
    !in_projects {
        print
    }
' "$TOOLS_FILE" > "${TOOLS_FILE}.tmp" && mv "${TOOLS_FILE}.tmp" "$TOOLS_FILE"

# 找到仓库结构结束的位置，插入项目部分
awk -v new_section="$new_projects_section" '
    /^```$/ && in_warehouse == 1 {
        in_warehouse = 0
        print
        print ""
        print new_section
        next
    }
    /^### 仓库结构$/ {
        in_warehouse = 1
    }
    1
' "$TOOLS_FILE" > "${TOOLS_FILE}.tmp" && mv "${TOOLS_FILE}.tmp" "$TOOLS_FILE"

log "INFO" "已更新项目列表，共 ${#actual_projects[@]} 个项目"

# --------------------------
# 3. 更新脚本索引
# --------------------------
log "INFO" "步骤3: 更新脚本索引"

# 从MEMORY.md提取脚本
scripts=$(awk 'BEGIN { in_script = 0; buffer = "" }
/^#### P[0-9]+: / {
    if (in_script) {
        # 处理前一个脚本
        split(buffer, lines, "\n")
        trigger = ""
        desc = ""
        for (i in lines) {
            if (lines[i] ~ /触发条件: /) {
                trigger = lines[i]
                sub(/触发条件: /, "", trigger)
            } else if (lines[i] ~ /功能描述: /) {
                desc = lines[i]
                sub(/功能描述: /, "", desc)
            } else if (lines[i] ~ /输入: / && desc == "") {
                # 没有功能描述时从输入推断
                desc = lines[i]
                sub(/输入: /, "", desc)
                # 简化描述
                if (desc ~ /物理问题描述、建模目标、约束条件/) desc = "构建物理模型、理论分析、物理解释"
                else if (desc ~ /理论问题、已知条件、推导目标/) desc = "数学推导、物理意义阐释、结果分析"
                else if (desc ~ /物理问题描述/) desc = "问题类型判断、分析框架确定、方法选择"
            }
        }
        if (trigger != "" && id != "" && name != "") {
            print trigger "|" id "|" name "|" desc
        }
    }
    # 开始新脚本
    in_script = 1
    buffer = ""
    sub(/^#### /, "", $0)
    id = substr($0, 1, 2)
    name = substr($0, 4)
    gsub(/^ +| +$/, "", name)
    next
}
in_script && /^#### P[0-9]+: / {
    # 下一个脚本开始，先处理当前
    split(buffer, lines, "\n")
    trigger = ""
    desc = ""
    for (i in lines) {
        if (lines[i] ~ /触发条件: /) {
            trigger = lines[i]
            sub(/触发条件: /, "", trigger)
        } else if (lines[i] ~ /功能描述: /) {
            desc = lines[i]
            sub(/功能描述: /, "", desc)
        } else if (lines[i] ~ /输入: / && desc == "") {
            # 没有功能描述时从输入推断
            desc = lines[i]
            sub(/输入: /, "", desc)
            # 简化描述
            if (desc ~ /物理问题描述、建模目标、约束条件/) desc = "构建物理模型、理论分析、物理解释"
            else if (desc ~ /理论问题、已知条件、推导目标/) desc = "数学推导、物理意义阐释、结果分析"
            else if (desc ~ /物理问题描述/) desc = "问题类型判断、分析框架确定、方法选择"
        }
    }
    if (trigger != "" && id != "" && name != "") {
        print trigger "|" id "|" name "|" desc
    }
    # 重置新脚本
    buffer = ""
    sub(/^#### /, "", $0)
    id = substr($0, 1, 2)
    name = substr($0, 4)
    gsub(/^ +| +$/, "", name)
    next
}
in_script {
    buffer = buffer $0 "\n"
}
END {
    # 处理最后一个脚本
    if (in_script) {
        split(buffer, lines, "\n")
        trigger = ""
        desc = ""
        for (i in lines) {
            if (lines[i] ~ /触发条件: /) {
                trigger = lines[i]
                sub(/触发条件: /, "", trigger)
            } else if (lines[i] ~ /功能描述: /) {
                desc = lines[i]
                sub(/功能描述: /, "", desc)
            } else if (lines[i] ~ /输入: / && desc == "") {
                # 没有功能描述时从输入推断
                desc = lines[i]
                sub(/输入: /, "", desc)
                # 简化描述
                if (desc ~ /物理问题描述、建模目标、约束条件/) desc = "构建物理模型、理论分析、物理解释"
                else if (desc ~ /理论问题、已知条件、推导目标/) desc = "数学推导、物理意义阐释、结果分析"
                else if (desc ~ /物理问题描述/) desc = "问题类型判断、分析框架确定、方法选择"
            }
        }
        if (trigger != "" && id != "" && name != "") {
            print trigger "|" id "|" name "|" desc
        }
    }
}' "$MEMORY_FILE" | sort | uniq)

# 生成新的脚本索引部分
new_scripts_section="### 脚本索引

| 触发条件 | 脚本编号 | 脚本名称 | 功能描述 |
|----------|----------|----------|----------|"

if [ -n "$scripts" ]; then
    while IFS='|' read -r trigger id name desc; do
        new_scripts_section+="
| $trigger | **$id** | $name | $desc |"
    done <<< "$scripts"
else
    new_scripts_section+="
|  |  |  | |"
fi

# 替换脚本索引部分 - 直接在技能索引后插入新的脚本索引，覆盖原有
awk -v new_section="$new_scripts_section" '
    /^---$/ && in_skills == 1 {
        in_skills = 0
        print
        print new_section
        print ""
        print "---"
        next
    }
    /^### 技能索引$/ {
        in_skills = 1
        in_old_scripts = 0
    }
    /^### 脚本索引$/ {
        in_old_scripts = 1
        next
    }
    in_old_scripts && /^---$/ {
        in_old_scripts = 0
        next
    }
    !in_old_scripts {
        print
    }
' "$TOOLS_FILE" > "${TOOLS_FILE}.tmp" && mv "${TOOLS_FILE}.tmp" "$TOOLS_FILE"

script_count=$(echo "$scripts" | wc -l)
log "INFO" "已更新脚本索引，共 $script_count 个脚本"

# --------------------------
# 4. 验证更新结果
# --------------------------
log "INFO" "步骤4: 验证更新结果"

# 检查存储位置表
if grep -q "脚本存储位置" "$TOOLS_FILE"; then
    log "INFO" "✓ 脚本存储位置已成功添加"
else
    log "ERROR" "✗ 脚本存储位置添加失败"
    exit 1
fi

# 检查项目列表
project_count=$(awk '/^\| 项目名 \| 存储位置 \| 描述 \|$/,/^---$/ {
    if ($0 ~ /^\| [^\|]+ \| [^\|]+ \| [^\|]+ \|$/ && $0 !~ /^\| 项目名 \| 存储位置 \| 描述 \|$/) count++
} END {print count}' "$TOOLS_FILE")
log "INFO" "✓ 项目列表包含 $project_count 个项目"

# 检查脚本索引
script_count_final=$(awk '/^\| 触发条件 \| 脚本编号 \| 脚本名称 \| 功能描述 \|$/,/^---$/ {
    if ($0 ~ /^\| [^\|]+ \| [^\|]+ \| [^\|]+ \| [^\|]+ \|$/ && $0 !~ /^\| 触发条件 \| 脚本编号 \| 脚本名称 \| 功能描述 \|$/) count++
} END {print count}' "$TOOLS_FILE")
log "INFO" "✓ 脚本索引包含 $script_count_final 个脚本"

# --------------------------
# 5. 完成
# --------------------------
log "INFO" "TOOLS.md更新任务执行完成"

# 获取TOOLS.md版本
TOOLS_VERSION=$(grep -E "^[*] 版本|^版本：" "$TOOLS_FILE" | head -n 1 | sed 's/^.*版本[：: ]*//' | tr -d ' 
')
if [ -z "$TOOLS_VERSION" ]; then
    TOOLS_VERSION="未知"
fi

echo -e "\n## 更新日志" >> "$LOG_FILE"
echo -e "| 字段 | 值 |" >> "$LOG_FILE"
echo -e "|------|-----|" >> "$LOG_FILE"
echo -e "| 时间戳 | $TIMESTAMP |" >> "$LOG_FILE"
echo -e "| 更新内容摘要 | 1. 更新项目列表（共${project_count}个项目）\n2. 更新脚本索引（共${script_count_final}个脚本）\n3. 确保脚本存储位置正确 |" >> "$LOG_FILE"
echo -e "| TOOLS.md版本 | $TOOLS_VERSION |" >> "$LOG_FILE"
echo -e "| 执行结果状态 | 成功 |" >> "$LOG_FILE"

echo "✅ TOOLS.md更新成功"
echo "📝 日志文件: $LOG_FILE"
echo "📋 更新摘要:"
echo "  - 项目数量: $project_count"
echo "  - 脚本数量: $script_count_final"
echo "  - 备份文件: $BACKUP_FILE"
