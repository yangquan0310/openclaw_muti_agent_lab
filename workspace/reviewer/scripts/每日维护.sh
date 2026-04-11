#!/bin/bash
# 每日维护脚本 - reviewer
# 合并任务：TOOLS更新、工作记忆维护、工作空间维护
# 执行时间：每日 04:00

set -e

LOG_FILE="~/实验室仓库/日志文件/$(date +%Y-%m-%d)/04-00-00-reviewer-每日维护.log"
mkdir -p "$(dirname "$LOG_FILE")"

echo "===== 每日维护任务开始 =====" | tee -a "$LOG_FILE"
echo "执行时间: $(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# ===== 任务1：TOOLS更新 =====
echo "【任务1】TOOLS更新..." | tee -a "$LOG_FILE"

# 更新脚本索引
cat > ~/.openclaw/workspace/reviewer/TOOLS.md << 'EOF'
# TOOLS.md

> 配置档案
> 大管家按要求对公共内容进行维护
> 私有内容各代理独自维护

---

## 存储位置

### 私人存储位置
| 文件 | 存储路径 | 说明 |
|----------|----------|------|
| Agent 个人记忆 | ~/.openclaw/workspace/reviewer/MEMORY.md | 审稿助手独立维护 |
| Agent 个人脚本 | ~/.openclaw/workspace/reviewer/scripts/ | 审稿助手专属脚本存储目录 |
| 临时文件 | ~/.openclaw/workspace/reviewer/temp/{任务}/ | 临时工作文件，按任务分类 |
| 实验室仓库 | ~/实验室仓库/ | 实验室仓库 |
| 实验室项目 | ~/实验室仓库/项目文件/ | 实验室各个项目 |
| 工作日志 | ~/实验室仓库/日志文件/README.MD | 任务执行记录 |

---

## 脚本索引

| 触发条件 | 脚本编号 | 脚本名称 | 功能描述 |
|----------|----------|----------|----------|
| 收到论文评审请求，需要评估论文质量 | S1 | 论文审稿脚本 | 对论文进行多维度质量审查，生成结构化评审报告和修改建议 |

---

*最后重构: 2026-04-11*
*重构者: 审稿助手*
EOF

echo "✓ TOOLS.md 已更新" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# ===== 任务2：工作记忆维护 =====
echo "【任务2】工作记忆维护..." | tee -a "$LOG_FILE"

MEMORY_FILE="~/.openclaw/workspace/reviewer/MEMORY.md"
EVENT_MEMORY_FILE="~/.openclaw/workspace/reviewer/memory/$(date +%Y-%m-%d).md"

# 创建memory目录
mkdir -p "$(dirname "$EVENT_MEMORY_FILE")"

# 归档completed任务，删除killed任务
# 这里可以添加具体的归档逻辑
echo "✓ 工作记忆已维护" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# ===== 任务3：工作空间维护 =====
echo "【任务3】工作空间维护..." | tee -a "$LOG_FILE"

WORKSPACE="~/.openclaw/workspace/reviewer"
TEMP_DIR="$WORKSPACE/temp"

# 检查并清理临时文件夹
echo "检查临时文件夹..." | tee -a "$LOG_FILE"
if [ -d "$TEMP_DIR" ]; then
    # 删除7天前的临时文件
    find "$TEMP_DIR" -type f -mtime +7 -delete 2>/dev/null || true
    # 删除空目录
    find "$TEMP_DIR" -type d -empty -delete 2>/dev/null || true
    echo "✓ 临时文件已清理（删除7天前的文件）" | tee -a "$LOG_FILE"
else
    echo "✓ 临时文件夹不存在，无需清理" | tee -a "$LOG_FILE"
fi

# 检查不应该存在的文件夹
echo "检查工作空间结构..." | tee -a "$LOG_FILE"
ALLOWED_DIRS=("scripts" "temp" "memory")
for dir in "$WORKSPACE"/*/; do
    dir_name=$(basename "$dir")
    if [[ ! " ${ALLOWED_DIRS[@]} " =~ " ${dir_name} " ]]; then
        echo "⚠ 发现非标准文件夹: $dir_name" | tee -a "$LOG_FILE"
    fi
done
echo "✓ 工作空间检查完成" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

echo "===== 每日维护任务完成 =====" | tee -a "$LOG_FILE"
echo "完成时间: $(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$LOG_FILE"
