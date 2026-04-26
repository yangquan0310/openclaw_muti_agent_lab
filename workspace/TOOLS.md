# TOOLS.md

> 系统管理员工具配置

---

## 存储位置

### 系统级存储

| 文件 | 存储路径 | 说明 |
|----------|----------|------|
| 主配置 | ~/.openclaw/openclaw.json | OpenClaw 主配置文件 |
| 环境变量 | ~/.openclaw/.env | API密钥和环境变量 |
| 插件目录 | ~/.openclaw/extensions/ | 插件安装位置 |
| 日志目录 | ~/.openclaw/logs/ | 系统日志 |

### 工作空间存储

| 文件 | 存储路径 | 说明 |
|----------|----------|------|
| 工作空间根 | ~/.openclaw/workspace/ | 所有代理工作空间 |
| 公共技能 | ~/.openclaw/workspace/skills/ | 共享技能 |
| 代理工作空间 | ~/.openclaw/workspace/<agent>/ | 各代理目录 |

---

## 系统管理命令

### 常用 CLI 命令

| 命令 | 用途 |
|------|------|
| `openclaw status` | 查看系统状态 |
| `openclaw doctor` | 诊断系统问题 |
| `openclaw gateway restart` | 重启网关 |
| `openclaw config get` | 查看配置 |
| `openclaw config patch` | 修改配置 |
| `openclaw plugins list` | 列出插件 |
| `openclaw hooks list` | 列出钩子 |
| `openclaw memory status` | 查看记忆状态 |

---

## 索引

### 代理工作空间索引
> 完整列表见: `~/.openclaw/workspace/`

---

*最后重构: 2026-04-26*
*重构者: 系统管理员*
