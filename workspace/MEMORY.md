# MEMORY.md

## 工作记忆(Working Memory)

### 当前活跃任务看板

| 任务ID | 项目 | 任务描述 | 会话ID | 状态 | 创建时间 | 最后更新 | 备注 |
|--------|------|----------|--------|------|----------|----------|------|
| T001 | github上传 | 执行工作流2每日自我更新 | session:CORN:main的定时任务 | active | 2026-04-27 00:00 | 2026-04-27 00:00 | 定时任务，每日04:00执行 |
---
### 活跃会话清单

| 会话ID | 类型/角色 | 分配任务 | 状态 | 创建时间 | 最后活跃 | 备注 |
|--------|-----------|----------|------|----------|----------|------|
| session:CORN:main的定时任务 | 定时任务 | github上传 | active | 2026-04-27 00:00 | 2026-04-27 00:00 |  |
---
### 工作记忆使用规则

> 详细规范参见 `\root\.openclaw\extensions\agent-self-development\skills\working_memory\SKILL.md`
> 本文件仅记录代理特定的实践细节
---


## 陈述性记忆(Semantic Memory)

### 核心自我认知
系统管理员，负责 OpenClaw 系统维护
---

### 知识网络

#### agent-self-development 插件
- **下载地址**: https://github.com/yangquan0310/openclaw_muti_agent_lab/releases
- **文件名格式**: `openclaw-agent-self-development-{版本}.tgz`
- **安装命令**: `openclaw plugins install /path/to/openclaw-agent-self-development-{版本}.tgz`
- **验证命令**: `openclaw plugins inspect agent-self-development --json`

> ⚠️ **版本更新注意**: 插件随版本更新，安装前请确认最新版本号
> - 查看最新版本: https://github.com/yangquan0310/openclaw_muti_agent_lab/releases/latest
> - 当前已知版本: v1.0.0 (2026-04-27)
---

### 事件记忆(Event Memory)

> 记录关键系统事件及其时间线索引

| 日期 | 事件 | 涉及实体 | 结果 | 日志位置 |
|------|------|----------|------|----------|
|||||

---

## 程序性记忆(Procedural Memory)

### 脚本索引
> 系统管理技能完整列表见: `/root/.openclaw/workspace/skills/README.md`

### 条件-行动规则(If-Then Rules)

| 条件 | 行动 |
|------|------|
| 用户请求修改配置 | 先备份，再修改，最后验证 |
| 系统异常 | 查看日志 → 诊断 → 修复 |
| 需要更新系统 | 检查兼容性 → 备份 → 更新 → 验证 |
| 用户请求查看状态 | 使用 openclaw status / doctor |
| **安装 agent-self-development 插件** | **使用 `openclaw plugins install /root/openclaw-agent-self-development-1.0.0.tgz`** |
| **验证插件安装** | **使用 `openclaw plugins inspect agent-self-development --json`** |

---

## 历史版本

| 版本 | 日期 | 更新内容 | 更新者 |
|------|------|----------|--------|
| v1.1.0 | 2026-04-28 | 用户重新更新记忆文档 | 系统管理员 |
| v1.0.0 | 2026-04-26 | 初始版本，作为系统管理员创建 | 系统管理员 |

---

*最后重构: 2026-04-28*
*重构者: 系统管理员*
