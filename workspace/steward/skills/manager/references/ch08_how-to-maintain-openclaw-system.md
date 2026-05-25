# 如何维护 .openclaw 系统？

> 对 .openclaw 目录进行体检、日常维护、问题处理和标准管理的完整指南。
> 版本：v1.0.0 | 更新：2026-05-25 | 引用规范：ch07 如何写 references 章节

---

## 一、问题

### 1.1 为什么要知道这个？

.openclaw 是整个多 Agent 系统的"地基"——配置文件、记忆数据库、定时任务、凭证、插件全部在此。一旦地基出问题，所有 Agent 都会受影响。

常见场景：
- 版本更新后 Gateway 无响应
- 记忆数据库膨胀到 100MB+
- 插件突然加载失败
- 磁盘空间耗尽
- 备份混乱，不知道哪个配置是正常的

### 1.2 常见困惑

| 困惑 | 答案 |
|------|------|
| 多久体检一次？ | 每周一次 + 版本更新后立即检查 + 重要任务前提前一天 |
| 哪些是核心文件？ | openclaw.json、.env、credentials/、memory/*.sqlite |
| 数据库多大算正常？ | steward 约 40-50MB，超过 100MB 需要 VACUUM |
| 哪些文件禁止提交 git？ | .env、credentials/、memory/、logs/、media/ 等（见 .gitignore） |

### 1.3 和项目维护的区别

.openclaw 维护和项目仓库维护是**两件不同的事**：

| | .openclaw 系统维护 | 项目仓库维护 |
|--|-------------------|-------------|
| 对象 | OpenClaw 自身配置和运行时数据 | 论文/课程/程序等项目文件 |
| 频率 | 每周体检 + 按需处理 | 每次任务完成后 |
| 工具 | openclaw status/config/cron | thesis-manager/course-manager 技能 |
| 备份 | openclaw.json + credentials/ | 项目终稿归档 |

---

## 二、方法论

### 2.1 维护分层框架

.openclaw 维护分为四个优先级，**按顺序处理，高优先级出问题才看低优先级**：

```
P0 核心层 ─── 不可跳过
  ├── 服务状态（Gateway 是否运行）
  ├── 配置文件完整性（openclaw.json + 备份）
  └── 定时任务状态

P1 运行数据层 ─── 每周检查
  ├── 记忆数据库大小 + WAL 状态
  ├── 磁盘空间占用
  └── 日志健康（ERROR 数量）

P2 功能插件层 ─── 每月检查
  ├── 插件可用性
  ├── 技能完整性
  └── 新增插件审查

P3 安全备份层 ─── 每月检查
  ├── Git 提交状态
  ├── 凭证文件完整性
  └── API Key 有效性（按需）
```

### 2.2 问题分类与响应

| 症状 | 分类 | 响应时间 |
|------|------|----------|
| Gateway stopped | P0 | 立即 |
| openclaw.json 损坏 | P0 | 立即 |
| 数据库 > 100MB | P1 | 当天 |
| 磁盘 > 80% | P1 | 当天 |
| 日志有 ERROR | P1 | 当天 |
| 插件突增/消失 | P2 | 3 天内 |
| Git 有未提交 | P3 | 7 天内 |
| 凭证文件丢失 | P0 | 立即 |

---

## 三、工作流

### 3.1 每周体检流程

```
预计耗时：10 分钟
触发：每周一 09:00 或手动
```

**步骤 1：服务状态（2 分钟）**

```bash
# 检查 Gateway 是否运行
openclaw status

# 检查 systemd 服务（如果部署了 systemd）
systemctl status openclaw

# 检查项：running 正常 / stopped 需要重启
```

**步骤 2：配置文件（1 分钟）**

```bash
# 核心配置文件存在性
ls -la ~/.openclaw/openclaw.json
ls -la ~/.openclaw/openclaw.json.bak*

# 验证备份数量（应 ≤ 5 个）
# 验证 .env 存在性（不查看内容，只验证存在）
ls -la ~/.openclaw/.env
```

**步骤 3：数据库与磁盘（2 分钟）**

```bash
# 检查各数据库大小
ls -lh ~/.openclaw/memory/*.sqlite

# 检查 WAL 是否堆积（正常应无 -wal 文件持续存在）
ls ~/.openclaw/memory/*.sqlite-wal 2>/dev/null | wc -l

# 磁盘空间
df -h /root/.openclaw
```

**步骤 4：日志审查（1 分钟）**

```bash
# 检查最近 ERROR
tail -100 ~/.openclaw/logs/main.jsonl | grep -i "error" | tail -10

# Gateway 重启记录
tail -20 ~/.openclaw/logs/gateway-restart.log 2>/dev/null
```

**步骤 5：Git + 凭证（1 分钟）**

```bash
cd ~/.openclaw && git status --short
ls -la ~/.openclaw/credentials/
```

**步骤 6：体检记录**

体检完成后，在 `~/.openclaw/workspace/steward/memory/` 下创建体检报告。

---

### 3.2 版本更新流程

```
触发：openclaw update 可用时
预计耗时：20 分钟
风险：中高
```

```
[1] 更新前备份（必须）
    cp openclaw.json openclaw.json.bak.$(date +%m%d)
    cp openclaw.json openclaw.json.last-good
    openclaw --version  # 记录当前版本

[2] 执行更新
    openclaw update

[3] 更新后检查
    openclaw status
    openclaw plugins list | grep enabled
    openclaw gateway restart

[4] 功能验证
    → 向飞书发送测试消息
    → 检查记忆系统
    → 验证定时任务

[5] 确认正常后
    → 更新 README.md 版本号
    → git add + commit + push
```

---

### 3.3 配置文件修改流程

```
风险：高
```

```
[1] 修改前备份
    cp openclaw.json openclaw.json.bak.$(date +%m%d)

[2] 使用官方工具修改
    openclaw config get <key>
    openclaw config set <key> <value>
    openclaw config patch <json>
    ⚠️ 禁止用 exec/cat/echo 直接修改配置文件

[3] 验证配置
    openclaw config list | grep <key>

[4] 测试功能
    openclaw gateway restart

[5] 提交
    git add openclaw.json && git commit -m "config: <描述>"
```

---

### 3.4 数据库异常处理

```
症状：sqlite 文件过大 / WAL 堆积 / 查询超时
```

```bash
# Step 1: 诊断
ls -lh memory/*.sqlite
ls memory/*.sqlite-wal

# Step 2: WAL 检查点（不丢失数据）
for db in memory/*.sqlite; do
    sqlite3 "$db" "PRAGMA wal_checkpoint(TRUNCATE);"
done

# Step 3: 压缩（仅文件过大时）
for db in memory/*.sqlite; do
    sqlite3 "$db" "VACUUM;"
done

# Step 4: 验证
ls -lh memory/*.sqlite
```

---

### 3.5 磁盘空间不足处理

```
触发：df 显示任一分区 > 85%
清理优先级从高到低：
```

| 优先级 | 目录 | 清理方式 | 风险 |
|--------|------|----------|------|
| 1 | `media/` | 删除超过 30 天的缓存文件 | 低 |
| 2 | `npm/` | `pnpm store prune` | 低 |
| 3 | `memory/` | VACUUM 压缩 | 低 |
| 4 | `logs/` | 删除 30 天前日志 | 低 |
| 5 | `agents/` | 归档超过 60 天会话 | 中 |
| 6 | `browser-existing-session/` | 清理旧会话 | 中 |

---

### 3.6 服务异常处理

```
症状：Gateway 无响应 / 报 Error / 插件加载失败
```

```
Step 1: 收集信息（2 分钟）
    openclaw status
    tail -50 logs/main.jsonl | grep ERROR
    tail -20 logs/gateway-restart.log

Step 2: 分类处理

    情况A：Gateway 进程停止
        → openclaw restart
        → 验证：openclaw status

    情况B：插件加载失败
        → openclaw plugins list | grep -i error
        → 单独禁用/启用该插件
        → openclaw gateway restart

    情况C：配置文件损坏
        → cp openclaw.json.bak openclaw.json
        → openclaw gateway restart
        → 或回退到 last-good

Step 3: 确认恢复
    → 向飞书发送测试消息
    → 确认各 Agent 正常响应
```

---

## 四、执行标准

### 4.1 数据库大小标准

| 数据库 | 正常范围 | 告警阈值 | 处理方式 |
|--------|----------|----------|----------|
| steward.sqlite | 40-50 MB | > 100 MB | VACUUM |
| programmer.sqlite | 30-40 MB | > 80 MB | VACUUM |
| psychologist.sqlite | 35-40 MB | > 80 MB | VACUUM |
| instructor.sqlite | 20-22 MB | > 45 MB | VACUUM |
| mathematician.sqlite | 18-20 MB | > 40 MB | VACUUM |
| physicist.sqlite | 14-16 MB | > 35 MB | VACUUM |

### 4.2 配置文件标准

| 检查项 | 通过标准 |
|--------|----------|
| openclaw.json 存在 | 文件存在且 ≥ 15KB |
| 备份文件数量 | ≤ 5 个（超出立即清理） |
| .env 存在 | 文件存在且包含 DEEPSEEK/MINIMAX 等变量 |
| 备份命名 | `openclaw.json.bak.N` 或 `openclaw.json.bak.YYYYMMDD` |

### 4.3 敏感文件标准

| 文件类型 | 权限要求 | Git 状态 |
|----------|----------|----------|
| openclaw.json | `600` | ✅ 可提交（不含 secrets） |
| .env | `600` | ❌ 禁止提交 |
| credentials/*.json | `600` | ❌ 禁止提交 |
| memory/*.sqlite | `600` | ❌ 禁止提交 |
| logs/*.jsonl | `640` | ❌ 禁止提交 |
| README.md | `644` | ✅ 可提交 |

### 4.4 Git 提交标准

**提交类型：**

| type | 说明 | 示例 |
|------|------|------|
| `config` | 配置文件变更 | `config: 更新 openclaw.json 模型配置` |
| `feat` | 新增功能 | `feat: 添加飞书日历技能` |
| `fix` | 问题修复 | `fix: 修复记忆数据库 VACUUM 脚本` |
| `doc` | 文档更新 | `doc: 更新 README.md Agent 列表` |
| `cleanup` | 清理工作 | `cleanup: 删除过期备份文件` |
| `backup` | 备份操作 | `backup: 手动备份 openclaw.json` |

**提交前检查清单：**

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 1 | .env 不在 git add 列表 | `git status` 无 .env |
| 2 | credentials/ 不在 git add 列表 | `git status` 无 credentials/ |
| 3 | 无大于 10MB 的文件在暂存区 | `git status` 文件均 < 10MB |
| 4 | 分支正确 | 仅推送 development，main 仅合并 |

### 4.5 插件启用标准

| 插件 | 状态 | 原因 |
|------|------|------|
| active-memory | ✅ 必须启用 | 核心记忆功能 |
| browser | ✅ 必须启用 | 浏览器自动化 |
| deepseek | ✅ 必须启用 | 默认模型之一 |
| document-extract | ✅ 必须启用 | 文档处理 |
| exa | ✅ 必须启用 | 搜索功能 |
| tavily | ✅ 必须启用 | 搜索备用 |
| memory-core | ✅ 必须启用 | 记忆核心 |
| 其他 | 按需启用 | 禁用不用的插件节省资源 |

---

## 五、体检报告模板

每次体检后，在 `~/.openclaw/workspace/steward/memory/` 下创建记录：

```markdown
# 体检报告 YYYY-MM-DD

## 执行摘要
- 整体状态：🟢 健康 / 🟡 需关注 / 🔴 异常
- 体检时间：HH:MM
- 体检人：大管家

## P0 核心层
- [ ] Gateway: 运行中 / 已停止
- [ ] openclaw.json: 正常 / 异常
- [ ] 定时任务: X 个活跃

## P1 运行数据层
- [ ] steward.sqlite: XX MB（正常/异常）
- [ ] 磁盘使用率: XX%（正常/告警）
- [ ] 日志 ERROR 数: X

## P2 功能插件层
- [ ] 启用插件: X 个
- [ ] 系统技能: X 个

## P3 安全备份层
- [ ] Git: 已同步 / 有未提交
- [ ] 凭证文件: 完整 / 缺失

## 问题清单
| # | 问题 | 严重度 | 处理状态 |
|---|------|--------|----------|
| 1 |      | P0/P1/P2 | 待处理/已修复 |

## 下次体检计划
YYYY-MM-DD
```

---

## 六、快速命令参考

```bash
# 服务状态
openclaw status
openclaw --version

# 配置
openclaw config list
openclaw config get agents.defaults.model

# 插件
openclaw plugins list

# 定时任务
openclaw cron list

# 数据库
ls -lh ~/.openclaw/memory/*.sqlite
for db in ~/.openclaw/memory/*.sqlite; do sqlite3 "$db" "PRAGMA wal_checkpoint(TRUNCATE);" done

# Git
cd ~/.openclaw && git status --short

# 磁盘
df -h /root/.openclaw
du -sh ~/.openclaw/*/ | sort -rh | head -5
```

---

## 检查清单

撰写完成后检查：

- [x] 文件名是否对应一个实际问题？（如何维护 .openclaw 系统？）
- [x] 「问题」章节是否解释为什么要知道这个？
- [x] 「方法论」章节是否给出 P0-P3 分层框架？
- [x] 「工作流」章节是否每步都有具体命令？
- [x] 「执行标准」章节是否原子化、无歧义？
- [x] 是否覆盖了体检、日常维护、问题处理三大场景？
- [x] 代理遇到实际问题是否能直接找到答案？

---

*最后更新：2026-05-25*
*维护者：大管家*
