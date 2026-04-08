#!/bin/bash
# 每日自动更新TOOLS.md脚本
# 功能：自动更新项目列表和脚本索引

TOOLS_PATH="/root/.openclaw/workspace/steward/TOOLS.md"
MEMORY_PATH="/root/.openclaw/workspace/steward/MEMORY.md"
PROJECTS_DIR="/root/实验室仓库/项目文件/"
LOG_DIR="/root/实验室仓库/日志文件/$(date +%Y-%m-%d)"
LOG_FILE="${LOG_DIR}/$(date +%H-%M-%S)-steward-TOOLS更新.md"

# 创建日志目录
mkdir -p "${LOG_DIR}"

# 记录开始时间
echo "### TOOLS.md自动更新日志" > "${LOG_FILE}"
echo "更新时间: $(date '+%Y-%m-%d %H:%M:%S')" >> "${LOG_FILE}"
echo "" >> "${LOG_FILE}"

# 步骤1：更新项目列表
echo "#### 步骤1：更新项目列表" >> "${LOG_FILE}"
echo "扫描项目目录: ${PROJECTS_DIR}" >> "${LOG_FILE}"

# 获取现有项目列表（保留格式）
EXISTING_PROJECTS=$(sed -n '/### 项目/,/### 项目结构/p' "${TOOLS_PATH}" | grep -E "^|.*|" | grep -v "项目名\|----")
echo "现有项目数量: $(echo "${EXISTING_PROJECTS}" | grep -v "^$" | wc -l)" >> "${LOG_FILE}"

# 扫描实际存在的项目
ACTUAL_PROJECTS=$(find "${PROJECTS_DIR}" -maxdepth 1 -type d -name "202[0-9]-[01][0-9]-[0-3][0-9]_*" | sort)
echo "实际项目数量: $(echo "${ACTUAL_PROJECTS}" | grep -v "^$" | wc -l)" >> "${LOG_FILE}"

# 生成新的项目列表
NEW_PROJECTS="| 项目名 | 存储位置 | 描述 |
|--------|----------|------|"

for proj_path in ${ACTUAL_PROJECTS}; do
    proj_name=$(basename "${proj_path}")
    # 尝试读取README.md获取描述
    desc=""
    if [ -f "${proj_path}/README.md" ]; then
        desc=$(head -n 10 "${proj_path}/README.md" | grep -E "^#|^## " | head -1 | sed 's/^#* //' | sed 's/项目：//' | sed 's/描述：//')
    fi
    NEW_PROJECTS="${NEW_PROJECTS}
| ${proj_name} | ~/实验室仓库/项目文件/${proj_name}/ | ${desc} |"
done

# 替换TOOLS.md中的项目列表
sed -i '/### 项目/,/### 项目结构/{
  /### 项目/!{/### 项目结构/!d;}
}' "${TOOLS_PATH}"

# 插入新的项目列表
sed -i "/### 项目/a\\
${NEW_PROJECTS}
" "${TOOLS_PATH}"

echo "项目列表已更新" >> "${LOG_FILE}"
echo "" >> "${LOG_FILE}"

# 步骤2：更新脚本索引
echo "#### 步骤2：更新脚本索引" >> "${LOG_FILE}"

# 从MEMORY.md提取程序性记忆中的脚本
SCRIPTS=$(sed -n '/#### S[0-9]/,/```/p' "${MEMORY_PATH}" | grep -E "^#### S[0-9]" | sed 's/#### //')
echo "从MEMORY.md提取到脚本数量: $(echo "${SCRIPTS}" | grep -v "^$" | wc -l)" >> "${LOG_FILE}"

# 生成新的脚本索引
NEW_SCRIPT_INDEX="| 触发条件 | 脚本编号 | 脚本名称 | 功能描述 |
|----------|----------|----------|----------|"

while IFS= read -r line; do
    if [[ "${line}" =~ ^S([0-9]+)\ (.*)$ ]]; then
        script_num="S${BASH_REMATCH[1]}"
        script_name="${BASH_REMATCH[2]}"
        # 尝试提取功能描述
        desc=$(sed -n "/#### ${script_num} ${script_name}/,/触发条件:/p" "${MEMORY_PATH}" | grep "功能描述:" | head -1 | sed 's/功能描述://' | sed 's/^ *//')
        NEW_SCRIPT_INDEX="${NEW_SCRIPT_INDEX}
|  | **${script_num}** | ${script_name} | ${desc} |"
    fi
done <<< "${SCRIPTS}"

# 替换TOOLS.md中的脚本索引
sed -i '/### 脚本索引/,/*最后重构/p' "${TOOLS_PATH}" | grep -v "### 脚本索引" | grep -v "|----------" | grep -v "触发条件" | head -n -3 > /tmp/old_scripts.txt
echo "原有脚本数量: $(cat /tmp/old_scripts.txt | grep -v "^$" | wc -l)" >> "${LOG_FILE}"

# 删除旧的脚本索引
sed -i '/### 脚本索引/,/*最后重构/{
  /### 脚本索引/!{/*最后重构/!d;}
}' "${TOOLS_PATH}"

# 插入新的脚本索引
sed -i "/### 脚本索引/a\\
${NEW_SCRIPT_INDEX}
" "${TOOLS_PATH}"

echo "脚本索引已更新" >> "${LOG_FILE}"
echo "" >> "${LOG_FILE}"

# 步骤3：完成
echo "#### 更新完成" >> "${LOG_FILE}"
echo "TOOLS.md已成功更新" >> "${LOG_FILE}"
echo "日志文件: ${LOG_FILE}" >> "${LOG_FILE}"

# 更新最后重构时间
sed -i "s/*最后重构:.*/\*最后重构: $(date '+%Y-%m-%d')\n\*重构者: 大管家/" "${TOOLS_PATH}"

exit 0
