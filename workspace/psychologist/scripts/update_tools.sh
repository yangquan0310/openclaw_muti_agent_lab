#!/bin/bash
# TOOLS.md自动更新脚本
# 功能：每天自动更新TOOLS.md的项目列表和脚本索引
# 执行时间：每天6:00

# 配置绝对路径
TOOLS_MD="/root/.openclaw/workspace/psychologist/TOOLS.md"
MEMORY_MD="/root/.openclaw/workspace/psychologist/MEMORY.md"
PROJECT_DIR="/root/实验室仓库/项目文件/"
LOG_DIR="/root/实验室仓库/日志文件/$(date +%Y-%m-%d)"
LOG_FILE="${LOG_DIR}/$(date +%H-%M-%S)_TOOLS更新.log"

# 创建日志目录
mkdir -p "${LOG_DIR}"

# 日志函数
log() {
    echo "[$(date +"%Y-%m-%d %H:%M:%S")] $1" >> "${LOG_FILE}"
}

log "========== 开始执行TOOLS.md更新任务 =========="

# 备份原始文件
cp "${TOOLS_MD}" "${TOOLS_MD}.$(date +%Y%m%d%H%M%S).bak"
log "已创建TOOLS.md备份文件"

# 1. 更新项目列表
log "正在更新项目列表..."

# 获取当前所有项目文件夹
CURRENT_PROJECTS=($(ls -d "${PROJECT_DIR}"*/ 2>/dev/null | sort))

# 提取现有项目行（从"### 项目"到"### 项目结构"之间的内容）
PROJECT_START=$(grep -n "### 项目" "${TOOLS_MD}" | head -1 | cut -d: -f1)
PROJECT_END=$(grep -n "### 项目结构" "${TOOLS_MD}" | head -1 | cut -d: -f1)

# 提取表头和分隔线
HEADER_LINE=$(sed -n "$((PROJECT_START + 2))p" "${TOOLS_MD}")
SEPARATOR_LINE=$(sed -n "$((PROJECT_START + 3))p" "${TOOLS_MD}")

# 生成新的项目列表内容
NEW_PROJECT_CONTENT=""

# 遍历所有项目文件夹
for project_path in "${CURRENT_PROJECTS[@]}"; do
    project_name=$(basename "${project_path}")
    
    # 尝试从README.md获取描述
    description=""
    if [ -f "${project_path}README.md" ]; then
        # 提取第一行标题，去掉#和空格
        description=$(grep -m 1 "^# " "${project_path}README.md" | sed 's/^# //' | sed 's/^## //')
    fi
    
    # 如果没有README或描述为空，使用默认描述
    if [ -z "${description}" ]; then
        description="研究项目"
    fi
    
    # 添加到项目列表
    NEW_PROJECT_CONTENT+="| ${project_name} | ${project_path} | ${description} |
"
done

# 读取通用脚本项目（特殊处理）
GENERAL_SCRIPTS_PATH="/root/.openclaw/skills/general-scripts/"
NEW_PROJECT_CONTENT+="| 2026-04-07_通用脚本迁移 | ${GENERAL_SCRIPTS_PATH} | 通用脚本技能，提供文档管理、项目创建、日志记录等标准化操作流程 |
"

# 替换TOOLS.md中的项目部分
# 先提取项目部分之前的内容（包括表头）
head -n $((PROJECT_START + 3)) "${TOOLS_MD}" > "${TOOLS_MD}.tmp"
# 添加新的项目内容
echo -e "${NEW_PROJECT_CONTENT}" >> "${TOOLS_MD}.tmp"
# 添加项目部分之后的内容
tail -n +$((PROJECT_END)) "${TOOLS_MD}" >> "${TOOLS_MD}.tmp"
# 替换原文件
mv "${TOOLS_MD}.tmp" "${TOOLS_MD}"

log "项目列表更新完成，共发现 ${#CURRENT_PROJECTS[@]} 个项目文件夹"

# 2. 更新脚本索引
log "正在更新脚本索引..."

# 找到脚本索引部分
SCRIPT_START=$(grep -n "### 脚本索引" "${TOOLS_MD}" | head -1 | cut -d: -f1)
# 找到脚本索引后的下一个---
SCRIPT_END=$(awk 'NR>'"${SCRIPT_START}"' && /^---/ {print NR; exit}' "${TOOLS_MD}")

# 提取脚本索引表头和分隔线
SCRIPT_HEADER=$(sed -n "$((SCRIPT_START + 2))p" "${TOOLS_MD}")
SCRIPT_SEPARATOR=$(sed -n "$((SCRIPT_START + 3))p" "${TOOLS_MD}")

# 生成新的脚本索引内容
NEW_SCRIPT_CONTENT=""

# 从MEMORY.md提取所有脚本
# 匹配"#### S[0-9]+-"开头的脚本标题
scripts=$(grep -E "^#### S[0-9]+-" "${MEMORY_MD}")

while IFS= read -r line; do
    if [[ $line =~ ^####\ (S[0-9]+)-(.*) ]]; then
        script_id="${BASH_REMATCH[1]}"
        script_name="${BASH_REMATCH[2]}"
        
        # 提取触发条件：查找"触发条件:"行
        trigger=$(grep -A 20 "#### ${script_id}-${script_name}" "${MEMORY_MD}" | grep -m 1 "触发条件:" | sed 's/^触发条件: //')
        
        # 提取功能描述：查找"功能描述:"或从开头描述提取
        description=""
        # 先找功能描述行
        desc_line=$(grep -A 20 "#### ${script_id}-${script_name}" "${MEMORY_MD}" | grep -m 1 "功能描述:")
        if [ -n "${desc_line}" ]; then
            description=$(echo "${desc_line}" | sed 's/^功能描述: //')
        else
            # 没有功能描述行，使用默认
            description="执行${script_name}相关任务"
        fi
        
        # 添加到脚本索引
        NEW_SCRIPT_CONTENT+="| ${trigger} | **${script_id}** | ${script_name} | ${description} |
"
    fi
done <<< "$scripts"

# 替换TOOLS.md中的脚本索引部分
# 提取脚本索引之前的内容（包括表头）
head -n $((SCRIPT_START + 3)) "${TOOLS_MD}" > "${TOOLS_MD}.tmp"
# 添加新的脚本内容
echo -e "${NEW_SCRIPT_CONTENT}" >> "${TOOLS_MD}.tmp"
# 添加脚本索引之后的内容
tail -n +$((SCRIPT_END)) "${TOOLS_MD}" >> "${TOOLS_MD}.tmp"
# 替换原文件
mv "${TOOLS_MD}.tmp" "${TOOLS_MD}"

log "脚本索引更新完成，共提取 $(echo "${scripts}" | wc -l) 个脚本"

# 3. 更新最后重构时间
log "正在更新最后重构时间..."
current_date=$(date +%Y-%m-%d)
sed -i "s/*最后重构: .*/\*最后重构: ${current_date}/" "${TOOLS_MD}"
sed -i "s/*重构者: .*/\*重构者: 自动更新脚本/" "${TOOLS_MD}"

# 4. 验证更新结果
log "正在验证更新结果..."
validation_passed=1

# 检查项目数量是否一致
project_count_in_tools=$(grep -E "^\| [0-9]{4}-[0-9]{2}-[0-9]{2}_" "${TOOLS_MD}" | wc -l)
expected_count=$((${#CURRENT_PROJECTS[@]} + 1)) # 加1是通用脚本项目

if [ "${project_count_in_tools}" -ne "${expected_count}" ]; then
    log "⚠️  项目数量警告：TOOLS.md中项目数 ${project_count_in_tools}，实际项目数 ${#CURRENT_PROJECTS[@]}"
    # 只警告，不失败，因为可能有其他不在项目文件夹的项目
else
    log "✅ 项目数量验证通过：共 ${project_count_in_tools} 个项目"
fi

# 检查脚本数量是否一致
script_count_in_tools=$(grep -E "^\|.*\*\*S[0-9]+\*\*" "${TOOLS_MD}" | wc -l)
expected_script_count=$(echo "${scripts}" | wc -l)

if [ "${script_count_in_tools}" -ne "${expected_script_count}" ]; then
    log "❌ 脚本数量验证失败：TOOLS.md中脚本数 ${script_count_in_tools}，MEMORY.md中脚本数 ${expected_script_count}"
    validation_passed=0
else
    log "✅ 脚本数量验证通过：共 ${script_count_in_tools} 个脚本"
fi

# 检查文件格式是否正确
if grep -q "### 项目" "${TOOLS_MD}" && grep -q "### 脚本索引" "${TOOLS_MD}"; then
    log "✅ 文件格式验证通过"
else
    log "❌ 文件格式验证失败：缺少必要的章节标题"
    validation_passed=0
fi

if [ "${validation_passed}" -eq 1 ]; then
    log "========== TOOLS.md更新成功完成 =========="
    echo "更新成功！日志文件：${LOG_FILE}"
else
    log "========== TOOLS.md更新失败，存在验证错误 =========="
    echo "更新失败！请检查日志：${LOG_FILE}"
    exit 1
fi
