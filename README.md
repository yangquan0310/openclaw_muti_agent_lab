# OpenClaw 多Agent实验室备份仓库

## 概述

本仓库是 OpenClaw 多Agent实验室的完整备份，包含所有Agent配置、工作空间、技能和系统设置。

## 仓库结构

```
.openclaw/
├── README.md              # 本文件
├── .gitignore            # Git忽略规则
├── openclaw.json         # OpenClaw主配置文件
├── workspace/            # 所有Agent工作空间
│   ├── mathematician/    # 数学家Agent
│   ├── physicist/        # 物理学家Agent
│   ├── psychologist/     # 心理学家Agent
│   ├── reviewer/         # 审稿助手Agent
│   ├── writer/          # 写作助手Agent
│   └── steward/         # 大管家Agent
└── agents/              # Agent运行时配置
    ├── main/            # 主Agent配置
    ├── mathematician/   # 数学家Agent运行时
    ├── physicist/       # 物理学家Agent运行时
    ├── psychologist/    # 心理学家Agent运行时
    ├── reviewer/        # 审稿助手Agent运行时
    ├── writer/         # 写作助手Agent运行时
    └── steward/        # 大管家Agent运行时
```

## Agent配置

### 核心Agent（6个）

| Agent | 中文名 | 功能描述 |
|-------|--------|----------|
| `mathematician` | 数学家 | 数学建模、统计分析 |
| `physicist` | 物理学家 | 物理问题建模、理论推导 |
| `psychologist` | 心理学家 | 心理学理论审核、实验设计 |
| `reviewer` | 审稿助手 | 论文质量审查、格式规范 |
| `writer` | 写作助手 | 内容创作、论文撰写 |
| `steward` | 大管家 | 文档管理、日志记录、协调 |

### 辅助Agent

| Agent | 功能描述 |
|-------|----------|
| `main` | 主Agent配置 |
| `academicassistant` | 学术助手 |
| `studentaffairsassistant` | 学生事务助手 |
| `teachingassistant` | 教学助手 |

## 备份策略

### 同步内容
1. **workspace/** - 所有Agent的工作空间和配置文件
2. **agents/** - Agent运行时配置和会话历史
3. **openclaw.json** - 主配置文件

### 排除内容
- 敏感文件（`.env`, `*.key`, `*.secret`, `*.token`等）
- 日志和缓存文件
- 临时文件和备份文件
- OpenClaw内部文件

### 备份频率
- **自动备份**: 每日自动执行
- **手动备份**: 随时可执行

## 恢复方法

### 1. 完整恢复
```bash
# 克隆仓库
git clone git@github.com:yangquan0310/openclaw_muti_agent_lab.git

# 复制文件到正确位置
cp -r openclaw_muti_agent_lab/workspace /root/.openclaw/
cp -r openclaw_muti_agent_lab/agents /root/.openclaw/
cp openclaw_muti_agent_lab/openclaw.json /root/.openclaw/
```

### 2. 部分恢复
```bash
# 恢复单个Agent的工作空间
cp -r openclaw_muti_agent_lab/workspace/mathematician /root/.openclaw/workspace/

# 恢复特定配置
cp openclaw_muti_agent_lab/openclaw.json /root/.openclaw/
```

## 使用说明

### 手动执行备份
```bash
bash /root/.openclaw/workspace/skills/lab-backup-manager/backup.sh
```

### 定时备份（推荐）
```bash
# 每天凌晨3点执行
0 3 * * * /root/.openclaw/workspace/skills/lab-backup-manager/backup.sh
```

### 查看备份日志
```bash
# 查看最近的提交
cd /root/.openclaw
git log --oneline -10
```

## 文件说明

### 核心配置文件

| 文件 | 位置 | 说明 |
|------|------|------|
| `AGENTS.md` | workspace/<agent>/ | Agent行为规范 |
| `IDENTITY.md` | workspace/<agent>/ | Agent身份定义 |
| `SOUL.md` | workspace/<agent>/ | Agent风格和信念 |
| `TOOLS.md` | workspace/<agent>/ | 工具配置 |
| `USER.md` | workspace/<agent>/ | 用户偏好 |
| `MEMORY.md` | workspace/<agent>/ | Agent记忆 |
| `HEARTBEAT.md` | workspace/<agent>/ | 心跳检查 |

### 技能文件
- 位置: `workspace/skills/`
- 包含: 各种任务处理的技能脚本
- 数量: 约70个技能

### 会话历史
- 位置: `agents/<agent>/sessions/`
- 内容: Agent的交互会话记录
- 用途: 调试和追踪Agent行为

## 安全注意事项

### 🔒 保护敏感信息
- 所有API密钥、密码等敏感信息应存储在`.env`文件中
- `.env`文件已被`.gitignore`排除，不会被提交
- 请勿在代码中硬编码敏感信息

### 📋 版本控制最佳实践
1. **定期提交**: 每天自动备份
2. **描述性提交信息**: 包含时间戳和变更摘要
3. **分支管理**: 使用main分支作为主要备份

### 🛡️ 备份验证
1. **完整性检查**: 定期验证备份的完整性
2. **恢复测试**: 定期测试从备份恢复的能力
3. **监控**: 监控备份执行结果

## 故障排除

### 常见问题

#### 1. 备份失败
```bash
# 检查脚本权限
chmod +x /root/.openclaw/workspace/skills/lab-backup-manager/backup.sh

# 检查Git配置
cd /root/.openclaw
git config --list
```

#### 2. Git推送失败
```bash
# 检查SSH密钥
ssh -T git@github.com

# 检查远程仓库配置
git remote -v
```

#### 3. 磁盘空间不足
```bash
# 清理临时文件
rm -rf /root/.openclaw/workspace/**/node_modules/
rm -rf /root/.openclaw/workspace/**/.cache/
```

### 联系支持
如有问题，请参考：
1. 备份脚本: `/root/.openclaw/workspace/skills/lab-backup-manager/`
2. GitHub Issues: 仓库问题跟踪
3. 系统管理员: 杨权

## 更新历史

### 版本 2.0 (2026-04-07)
- 重构备份策略，基于`.openclaw`根目录同步
- 删除workspace中的`.gitignore`和`README.md`
- 新增根目录`README.md`文档
- 优化`.gitignore`配置

### 版本 1.0 (2026-04-06)
- 初始版本，基于workspace-only同步

## 许可证

本备份仓库遵循 MIT 许可证。

## 维护者

- **杨权** - 系统管理员
- **OpenClaw系统** - 自动备份

---

**最后更新**: 2026-04-07 17:16:00  
**仓库状态**: ✅ 活跃维护  
**备份状态**: ✅ 自动运行