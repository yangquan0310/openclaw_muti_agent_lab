#!/bin/bash
# TOOLS.md 自动更新脚本
# 功能：
# 1. 扫描最新项目并更新TOOLS.md
# 2. 移除不存在的项目
# 3. 从MEMORY.md提取程序性记忆中的脚本索引并更新
# 4. 删除不存在的脚本索引
# 5. 自动生成更新日志

# 配置变量
TOOLS_MD_PATH="/root/.openclaw/workspace/academicassistant/TOOLS.md"
MEMORY_MD_PATH="/root/.openclaw/workspace/academicassistant/MEMORY.md"
PROJECTS_DIR="/root/教研室仓库/项目文件/"
LOG_DIR="/root/实验室仓库/日志文件/$(date +%Y-%m-%d)/"
LOG_FILE="${LOG_DIR}/$(date +%H-%M-%S)-academicassistant-TOOLS更新.md"

# 确保日志目录存在
mkdir -p "${LOG_DIR}"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "${LOG_FILE}"
}

# 开始执行
log "=== TOOLS.md 更新任务开始 ==="

# 备份原文件
BACKUP_FILE="${TOOLS_MD_PATH}.bak.$(date +%Y%m%d%H%M%S)"
cp "${TOOLS_MD_PATH}" "${BACKUP_FILE}"
log "已备份原文件到: ${BACKUP_FILE}"

# 1. 提取现有内容
# 提取索引之前的内容
CONTENT_BEFORE=$(awk '/## 索引/{exit}1' "${BACKUP_FILE}")

# 提取技能索引部分 - 保留原始技能列表（使用原始备份文件）
log "正在提取现有技能索引"
SKILLS_SECTION=$(grep -A 20 "### 技能索引"  | grep -E "^\|" | grep -v "技能名称" | grep -v "-------")
log "提取到技能: $(echo "${SKILLS_SECTION}" | grep -v "^$" | wc -l) 个"

# 2. 获取最新项目列表
log "正在扫描项目目录: ${PROJECTS_DIR}"
PROJECTS_LIST=$(find "${PROJECTS_DIR}" -maxdepth 1 -type d -name "20*" | sort -r | head -20)
log "找到最新项目: $(echo "${PROJECTS_LIST}" | grep -v "^$" | wc -l) 个"

# 3. 从MEMORY.md提取脚本索引
log "正在从MEMORY.md提取程序性记忆脚本"
# 逐个提取每个脚本的信息
SCRIPTS_CONTENT=""
SCRIPT_NUM=1
while true; do
    # 提取脚本块
    SCRIPT_BLOCK=$(awk '/### 脚本'${SCRIPT_NUM}'：/,/^$/' "${MEMORY_MD_PATH}")
    if [ -z "${SCRIPT_BLOCK}" ]; then
        break
    fi
    
    # 提取脚本名称
    SCRIPT_NAME=$(echo "${SCRIPT_BLOCK}" | grep "### 脚本${SCRIPT_NUM}：" | sed 's/### 脚本[0-9]*：//' | sed 's/^ *//')
    # 提取触发条件
    TRIGGER=$(echo "${SCRIPT_BLOCK}" | awk '/触发条件/,/^$/' | grep -v "触发条件" | grep -v "^$" | head -n1 | sed 's/^ *- //' | sed 's/^ *//')
    # 提取功能描述
    DESC=$(echo "${SCRIPT_BLOCK}" | awk '/功能描述/,/^$/' | grep -v "功能描述" | grep -v "^$" | head -n1 | sed 's/^ *- //' | sed 's/^ *//')
    
    if [ -n "${SCRIPT_NAME}" ] && [ -n "${TRIGGER}" ] && [ -n "${DESC}" ]; then
        SCRIPTS_CONTENT+="| ${TRIGGER} | 脚本${SCRIPT_NUM} | ${SCRIPT_NAME} | ${DESC} |
"
    fi
    
    SCRIPT_NUM=$((SCRIPT_NUM + 1))
done
log "提取到脚本: $((SCRIPT_NUM - 1)) 个"

# 4. 构建新的TOOLS.md内容
NEW_CONTENT="${CONTENT_BEFORE}
## 索引

### 技能索引
| 技能名称 | 触发示例 | 描述 | 路径 |
|---------|---------|------|------|
${SKILLS_SECTION}

---
### 脚本索引

| 触发条件 | 脚本编号 | 脚本名称 | 功能描述 |
|----------|----------|----------|----------|
${SCRIPTS_CONTENT}

---

*最后重构: $(date +%Y-%m-%d)*
*重构者: 大管家*
"

# 写入新内容
echo "${NEW_CONTENT}" > "${TOOLS_MD_PATH}"
log "已写入新的TOOLS.md内容"

# 验证文件大小
OLD_SIZE=$(stat -c%s "${BACKUP_FILE}")
NEW_SIZE=$(stat -c%s "${TOOLS_MD_PATH}")
log "文件大小变化: ${OLD_SIZE}字节 -> ${NEW_SIZE}字节"

# 完成
log "=== TOOLS.md 更新任务完成 ==="
echo "更新完成，日志已保存到: ${LOG_FILE}"
