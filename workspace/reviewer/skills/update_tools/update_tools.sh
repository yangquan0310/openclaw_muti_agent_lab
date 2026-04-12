#!/bin/bash
# 自动更新TOOLS.md脚本
cd /root/.openclaw/workspace/reviewer
mkdir -p logs
node scripts/update_tools.js >> logs/update_tools.log 2>&1
