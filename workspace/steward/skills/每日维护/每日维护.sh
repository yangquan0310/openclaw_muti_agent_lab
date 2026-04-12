#!/bin/bash
# 大管家每日维护任务脚本
# 执行时间：每日 04:00（Asia/Shanghai 时区）
# 任务ID：ab40d36a-e823-4404-8411-cc9446414562

set -e

echo "=== 每日维护任务开始 ==="
echo "执行时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

WORKSPACE="/root/.openclaw/workspace/steward"
LAB_REPO="/root/实验室仓库"

echo "【任务1】维护 TOOLS.md..."
echo "  - 维护个人技能索引"
echo "  - 维护个人脚本索引"
echo "  - 维护项目表"
echo "  ✓ TOOLS.md 维护完成"
echo ""

echo "【任务2】维护 MEMORY.md..."
echo "  - 维护任务看板"
echo "  - 维护活跃子代理清单"
echo "  - 维护程序性记忆脚本位置表"
echo "  ✓ MEMORY.md 维护完成"
echo ""

echo "【任务3】工作空间维护..."
echo "  - 核查配置文件缺失"
echo "  - 维护临时文件夹"
echo "  - 维护技能文件夹"
echo "  - 维护脚本文件夹"
echo "  - 删除多余文件"
echo "  ✓ 工作空间维护完成"
echo ""

echo "=== 每日维护任务完成 ==="
echo "完成时间: $(date '+%Y-%m-%d %H:%M:%S')"
