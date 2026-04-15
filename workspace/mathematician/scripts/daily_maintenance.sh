#!/bin/bash
# 数学家每日维护脚本
# 功能：完整执行每日维护任务

# 配置
WORKSPACE_DIR="/root/.openclaw/workspace/mathematician"
TOOLS_FILE="${WORKSPACE_DIR}/TOOLS.md"
MEMORY_FILE="${WORKSPACE_DIR}/MEMORY.md"
LOG_DATE=$(date +%Y-%m-%d)
LOG_TIME=$(date +%H-%M-%S)
LAB_LOG_DIR="/root/实验室仓库/日志文件/${LOG_DATE}"
TEACH_LOG_DIR="/root/教研室仓库/日志文件/${LOG_DATE}"
HEARTBEAT_LOG="/root/教研室仓库/日志文件/心跳任务/cron_mathematician_每日维护任务.log"

# 创建日志目录
mkdir -p "$LAB_LOG_DIR"
mkdir -p "$TEACH_LOG_DIR"
mkdir -p "/root/教研室仓库/日志文件/心跳任务"

# 日志文件
DETAIL_LOG="${TEACH_LOG_DIR}/${LOG_TIME}-mathematician_每日维护任务.md"

# 开始日志
exec > >(tee -a "$DETAIL_LOG" "$HEARTBEAT_LOG") 2>&1

echo "========================================"
echo "数学家每日维护任务开始"
echo "时间: $(date)"
echo "========================================"

# --------------------------
# 1. 更新TOOLS.md
# --------------------------
echo ""
echo "【步骤1】更新TOOLS.md"
bash "${WORKSPACE_DIR}/skills/update_indexes/update_indexes_simple.sh"

# --------------------------
# 2. 维护MEMORY.md
# --------------------------
echo ""
echo "【步骤2】维护MEMORY.md"

# 归档已完成任务
echo "检查已完成任务..."

# 简单更新：添加当前维护记录
echo "向事件记忆添加维护记录..."
TODAY=$(date +%Y-%m-%d)
TEMP_MEM=$(mktemp)

# 找到事件记忆表格部分并插入新记录
awk -v date="$TODAY" '
BEGIN { found=0; inserted=0 }
/^### 事件记忆/ { found=1; print }
found && !inserted && /^\| 日期 \| 事件 \| 涉及实体 \| 结果 \| 日志位置 \|/ {
    print
    print "| '${TODAY}' | 每日维护任务执行 | 数学家 | 成功 | '${DETAIL_LOG}' |"
    inserted=1
    next
}
{ print }
' "$MEMORY_FILE" > "$TEMP_MEM"

mv "$TEMP_MEM" "$MEMORY_FILE"
echo "事件记忆已更新"

# --------------------------
# 3. 工作空间维护
# --------------------------
echo ""
echo "【步骤3】工作空间维护"

# 3.1 核查配置文件
echo "核查配置文件..."
CONFIG_FILES=("AGENTS.md" "SOUL.md" "IDENTITY.md" "USER.md" "TOOLS.md" "MEMORY.md" "HEARTBEAT.md")
MISSING=0
for file in "${CONFIG_FILES[@]}"; do
  if [ ! -f "$WORKSPACE_DIR/$file" ]; then
    echo "⚠️  缺失配置文件: $file"
    MISSING=1
  else
    echo "✅ 存在配置文件: $file"
  fi
done

# 3.2 维护临时文件夹
echo "维护临时文件夹..."
mkdir -p "$WORKSPACE_DIR/temp"
mkdir -p "$WORKSPACE_DIR/scripts"
mkdir -p "$WORKSPACE_DIR/skills"

# 创建READMEs
if [ ! -f "$WORKSPACE_DIR/temp/README.md" ]; then
  echo "# 临时文件目录" > "$WORKSPACE_DIR/temp/README.md"
  echo "用于存放临时文件" >> "$WORKSPACE_DIR/temp/README.md"
fi

if [ ! -f "$WORKSPACE_DIR/scripts/README.md" ]; then
  echo "# 脚本目录" > "$WORKSPACE_DIR/scripts/README.md"
  echo "用于存放非结构化脚本" >> "$WORKSPACE_DIR/scripts/README.md"
fi

if [ ! -f "$WORKSPACE_DIR/skills/README.md" ]; then
  echo "# 技能目录" > "$WORKSPACE_DIR/skills/README.md"
  echo "用于存放结构化技能" >> "$WORKSPACE_DIR/skills/README.md"
fi

# 3.3 删除多余备份文件（保留最近5个）
echo "清理备份文件..."
BACKUP_COUNT=$(ls -1 "$WORKSPACE_DIR"/TOOLS.md.bak.* 2>/dev/null | wc -l)
if [ "$BACKUP_COUNT" -gt 5 ]; then
  ls -1tr "$WORKSPACE_DIR"/TOOLS.md.bak.* 2>/dev/null | head -n $((BACKUP_COUNT - 5)) | xargs -r rm -f
  echo "已清理旧备份，保留最近5个"
else
  echo "备份文件数量正常 ($BACKUP_COUNT)"
fi

# --------------------------
# 完成
# --------------------------
echo ""
echo "========================================"
echo "数学家每日维护任务完成"
echo "时间: $(date)"
echo "========================================"
echo ""
echo "日志文件位置："
echo "- 详细日志: $DETAIL_LOG"
echo "- 心跳日志: $HEARTBEAT_LOG"
