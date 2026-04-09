#!/bin/bash
# 数学家索引更新脚本
# 功能：自动更新TOOLS.md中的脚本索引和项目库

# 配置
WORKSPACE_DIR="/root/.openclaw/workspace/mathematician"
TOOLS_FILE="${WORKSPACE_DIR}/TOOLS.md"
SCRIPTS_DIR="${WORKSPACE_DIR}/scripts"
PROJECTS_DIR="/root/实验室仓库/项目文件"
MEMORY_FILE="${WORKSPACE_DIR}/MEMORY.md"

# 创建备份
cp "$TOOLS_FILE" "$TOOLS_FILE.bak.$(date +%Y%m%d%H%M%S)"

# --------------------------
# 1. 更新脚本索引
# --------------------------
echo "更新脚本索引..."

# 提取现有脚本索引部分
SCRIPT_INDEX_START=$(grep -n "### 脚本索引" "$TOOLS_FILE" | head -n1 | cut -d: -f1)
SCRIPT_INDEX_END=$(grep -n "^---" "$TOOLS_FILE" | awk -v start="$SCRIPT_INDEX_START" 'NR > start {print NR; exit}')
if [ -z "$SCRIPT_INDEX_END" ]; then
  SCRIPT_INDEX_END=$(wc -l < "$TOOLS_FILE")
fi

# 读取程序性记忆中的脚本
declare -A PROCEDURAL_SCRIPTS
# 从MEMORY.md中提取脚本信息
while IFS= read -r line || [[ -n "$line" ]]; do
  # 匹配脚本定义行，支持中文冒号
  if [[ "${line}" =~ ^####[[:space:]]+S([0-9]+)[：:](.*)$ ]]; then
    SCRIPT_ID="S${BASH_REMATCH[1]}"
    SCRIPT_NAME="${BASH_REMATCH[2]}"
    SCRIPT_NAME=$(echo "$SCRIPT_NAME" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    # 读取触发条件
    IFS= read -r trigger_line || true
    TRIGGER_CONDITION=""
    if [[ "${trigger_line}" =~ 触发条件[：:][[:space:]]*(.*)$ ]]; then
      TRIGGER_CONDITION="${BASH_REMATCH[1]}"
    fi
    # 使用脚本名称作为功能描述
    FUNCTION_DESC="${SCRIPT_NAME}"
    PROCEDURAL_SCRIPTS["${SCRIPT_ID}"]="${TRIGGER_CONDITION}|${SCRIPT_NAME}|${FUNCTION_DESC}"
  fi
done < "${MEMORY_FILE}"

# 读取实际存在的脚本文件
declare -A FILE_SCRIPTS
for script_file in "${SCRIPTS_DIR}"/*.sh; do
  if [ -f "${script_file}" ]; then
    script_name=$(basename "${script_file}" .sh)
    # 尝试从脚本中提取描述
    description=$(grep -m1 "^# 功能" "${script_file}" | sed 's/^# 功能[：:][[:space:]]*//')
    if [ -z "${description}" ]; then
      description="自定义脚本 ${script_name}"
    fi
    FILE_SCRIPTS["${script_name}"]="脚本文件执行|${script_name}|${description}"
  fi
done

# 合并脚本列表
declare -A ALL_SCRIPTS
for id in "${!PROCEDURAL_SCRIPTS[@]}"; do
  ALL_SCRIPTS["${id}"]="${PROCEDURAL_SCRIPTS[${id}]}"
done
for name in "${!FILE_SCRIPTS[@]}"; do
  ALL_SCRIPTS["${name}"]="${FILE_SCRIPTS[${name}]}"
done

# 生成新的脚本索引内容
NEW_SCRIPT_INDEX="### 脚本索引
> 各个代理独立维护，这里显示数学家特有脚本

| 触发条件 | 脚本编号 | 脚本名称 | 功能描述 |
|----------|----------|----------|----------|
"

# 按脚本编号排序
for key in $(printf "%s\n" "${!ALL_SCRIPTS[@]}" | sort); do
  IFS='|' read -r trigger name desc <<< "${ALL_SCRIPTS[${key}]}"
  NEW_SCRIPT_INDEX+="| ${trigger} | ${key} | ${name} | ${desc} |
"
done

# 替换TOOLS.md中的脚本索引部分
head -n $((SCRIPT_INDEX_START - 1)) "${TOOLS_FILE}" > "${TOOLS_FILE}.tmp"
echo "${NEW_SCRIPT_INDEX}" >> "${TOOLS_FILE}.tmp"
tail -n +$((SCRIPT_INDEX_END + 1)) "${TOOLS_FILE}" >> "${TOOLS_FILE}.tmp"
mv "${TOOLS_FILE}.tmp" "${TOOLS_FILE}"

# --------------------------
# 2. 更新项目库
# --------------------------
echo "更新项目库..."

# 提取现有项目库部分
PROJECT_INDEX_START=$(grep -n "### 项目库" "${TOOLS_FILE}" | head -n1 | cut -d: -f1)
PROJECT_INDEX_END=$(grep -n "^---" "${TOOLS_FILE}" | awk -v start="$PROJECT_INDEX_START" 'NR > start {print NR; exit}')
if [ -z "$PROJECT_INDEX_END" ]; then
  PROJECT_INDEX_END=$(grep -n "## 索引" "${TOOLS_FILE}" | head -n1 | cut -d: -f1)
  PROJECT_INDEX_END=$((PROJECT_INDEX_END - 1))
fi

# 读取实际存在的项目目录
declare -A PROJECTS
for project_dir in "${PROJECTS_DIR}"/*/; do
  if [ -d "${project_dir}" ]; then
    project_name=$(basename "${project_dir}")
    # 尝试从README.md中提取描述
    description=""
    if [ -f "${project_dir}/README.md" ]; then
      description=$(grep -m1 "^#" "${project_dir}/README.md" | sed 's/^#*[[:space:]]*//')
    fi
    if [ -z "${description}" ]; then
      # 从目录名推断描述
      description=$(echo "${project_name}" | sed 's/^[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}_//' | sed 's/_/ /g')
    fi
    PROJECTS["${project_name}"]="${description}"
  fi
done

# 生成新的项目库内容
NEW_PROJECT_INDEX="### 项目库
> 大管家维护格式
> 内容由各代理独立维护
| 项目名 | 存储位置 | 描述 |
|--------|----------|------|
"

# 按项目名称排序（按日期降序）
for project in $(printf "%s\n" "${!PROJECTS[@]}" | sort -r); do
  NEW_PROJECT_INDEX+="| ${project} | ~/实验室仓库/项目文件/${project}/ | ${PROJECTS[${project}]} |
"
done

# 替换TOOLS.md中的项目库部分
head -n $((PROJECT_INDEX_START - 1)) "${TOOLS_FILE}" > "${TOOLS_FILE}.tmp"
echo "${NEW_PROJECT_INDEX}" >> "${TOOLS_FILE}.tmp"
tail -n +$((PROJECT_INDEX_END + 1)) "${TOOLS_FILE}" >> "${TOOLS_FILE}.tmp"
mv "${TOOLS_FILE}.tmp" "${TOOLS_FILE}"

echo "索引更新完成！"
echo "脚本数量: ${#ALL_SCRIPTS[@]}"
echo "项目数量: ${#PROJECTS[@]}"
