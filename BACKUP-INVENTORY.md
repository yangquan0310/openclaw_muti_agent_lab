# BACKUP-INVENTORY.md

> **gitignored 文件备份清单 + 复原路径**
>
> 记录所有**不进 git 的关键文件**及其备份位置。**OpenClaw 仓库根 .gitignore 默认排除所有文件（`/*`）+ 仅保留 `.gitallowed` 例外**，因此配置文件、SQLite 数据库、env 凭证等敏感数据都不入库。
>
> **最后更新：2026-08-04 (v8.52.0 综合整理)**

---

## 一、备份目录总览

| 备份目录 | 创建时间 | 内容 | 大小 |
|---|---|---|---|
| `/data/disk/.openclaw/agents-env-backup-20260804/` | 2026-08-04 | auditor/instructor agent .env（飞书 bot 凭证）| ~2KB |
| `/data/disk/.openclaw/sqlite-residue-backup-20260804/` | 2026-08-04 | SQLite 4 张核心表完整 dump（cron_run_logs / flow_runs / plugin_state_entries / task_runs）| ~11MB |
| `/data/disk/.openclaw/workboard-cleanup-20260804/` | 2026-08-04 | workboard.sqlite 归档前备份 | ~5MB |
| `/data/disk/.openclaw/openclaw.json.bak-20260804` | 2026-08-04 | OpenClaw 完整配置（含 v8.52.0 转型前状态）| ~22KB |
| `/data/disk/.openclaw/env.bak-20260804` | 2026-08-04 | 完整 .env（含 v8.52.0 转型前所有凭证）| ~2KB |
| `/data/disk/.openclaw/state-openclaw.sqlite.bak-20260804` | 2026-08-04 | state/openclaw.sqlite 完整备份（v8.52.0 转型前）| ~28MB |

---

## 二、gitignored 关键文件 + 当前状态 + 备份位置

### 2.1 配置文件类

| 文件 | 当前状态 | 备份位置 |
|---|---|---|
| `/root/.openclaw/openclaw.json` | 20950 bytes（v8.52.0 转型后，已删 auditor/instructor 引用）| `/data/disk/.openclaw/openclaw.json.bak-20260804` |
| `/root/.openclaw/.env` | 2091 bytes（v8.52.0 转型后，已删 ACADEMIC/TEACHING bot 凭证）| `/data/disk/.openclaw/env.bak-20260804` |

### 2.2 SQLite 数据库类

| 文件 | 当前状态 | 备份位置 |
|---|---|---|
| `/root/.openclaw/state/openclaw.sqlite` | 28MB（运行时状态，含 cron_run_logs / flow_runs / plugin_state_entries / task_runs）| `/data/disk/.openclaw/state-openclaw.sqlite.bak-20260804`（完整）+ `/data/disk/.openclaw/sqlite-residue-backup-20260804/*.sql`（4 张表 dump）|
| `/root/.openclaw/plugins/workboard/workboard.sqlite` | 1.1MB（workboard 卡片数据，含今天清理的 21 张 archive 卡）| `/data/disk/.openclaw/workboard-cleanup-20260804/workboard.sqlite.bak-20260804` |

### 2.3 Agent 工作区（v8.52.0 转型后）

| Agent 目录 | 状态 | 备份 |
|---|---|---|
| `/root/.openclaw/workspace/steward/` | ✅ 保留（大管家）| git tracked |
| `/root/.openclaw/workspace/programmer/` | ✅ 保留 | git tracked |
| `/root/.openclaw/workspace/psychologist/` | ✅ 保留 | git tracked |
| `/root/.openclaw/workspace/writer/` | ✅ 保留 | git tracked |
| `/root/.openclaw/workspace/reviewer/` | ✅ 保留（v8.52.0 替代 auditor）| git tracked |
| `/root/.openclaw/workspace/presenter/` | ✅ 保留（v8.52.0 转型可视化师）| git tracked |
| `/root/.openclaw/workspace/mathematician/` | ✅ 保留 | git tracked |
| `/root/.openclaw/workspace/physicist/` | ✅ 保留 | git tracked |
| `/root/.openclaw/workspace/auditor/` | ❌ **删除**（v8.52.0）| git snapshot `41acc6b8`（git history）|
| `/root/.openclaw/workspace/instructor/` | ❌ **删除**（v8.52.0）| git snapshot `41acc6b8`（git history）|

### 2.4 已删 agent 的凭证（v8.52.0 转型时备份）

| 凭证 | 备份位置 |
|---|---|
| auditor 飞书 bot appSecret | `/data/disk/.openclaw/agents-env-backup-20260804/auditor.env` |
| instructor 飞书 bot appSecret | `/data/disk/.openclaw/agents-env-backup-20260804/instructor.env` |

---

## 三、复原 SOP（按场景）

### 场景 1：完整复原 v8.52.0 转型前状态（紧急回滚）

```bash
# 1. 还原 git 工作区（删除前 snapshot commit 41acc6b8）
cd /root/.openclaw
git checkout 41acc6b8 -- workspace/auditor/ workspace/instructor/

# 2. 重建运行时数据目录
mkdir -p /data/disk/.openclaw/agents/{auditor,instructor}

# 3. 重建符号链接
ln -s /data/disk/.openclaw/agents/auditor /root/.openclaw/agents/auditor
ln -s /data/disk/.openclaw/agents/instructor /root/.openclaw/agents/instructor

# 4. 还原凭证
cp /data/disk/.openclaw/agents-env-backup-20260804/auditor.env /root/.openclaw/workspace/auditor/.openclaw/
cp /data/disk/.openclaw/agents-env-backup-20260804/instructor.env /root/.openclaw/workspace/instructor/.openclaw/

# 5. 还原 openclaw.json + .env
cp /data/disk/.openclaw/openclaw.json.bak-20260804 /root/.openclaw/openclaw.json
cp /data/disk/.openclaw/env.bak-20260804 /root/.openclaw/.env

# 6. 还原 SQLite
cp /data/disk/.openclaw/state-openclaw.sqlite.bak-20260804 /root/.openclaw/state/openclaw.sqlite

# 7. 重新注册到 OpenClaw
openclaw agents sync
```

### 场景 2：还原 workboard 卡片数据（误操作回滚）

```bash
# 停止 OpenClaw（防止覆盖备份）
openclaw gateway stop

# 还原 workboard SQLite
cp /data/disk/.openclaw/workboard-cleanup-20260804/workboard.sqlite.bak-20260804 /root/.openclaw/plugins/workboard/workboard.sqlite
cp /data/disk/.openclaw/workboard-cleanup-20260804/workboard.sqlite-wal.bak-20260804 /root/.openclaw/plugins/workboard/workboard.sqlite-wal 2>/dev/null || true
cp /data/disk/.openclaw/workboard-cleanup-20260804/workboard.sqlite-shm.bak-20260804 /root/.openclaw/plugins/workboard/workboard.sqlite-shm 2>/dev/null || true

# 重启 OpenClaw
openclaw gateway restart
```

### 场景 3：还原 SQLite 单张表数据

```bash
# 查看 dump 文件
ls /data/disk/.openclaw/sqlite-residue-backup-20260804/

# 还原 task_runs 表（示例）
sqlite3 /root/.openclaw/state/openclaw.sqlite < /data/disk/.openclaw/sqlite-residue-backup-20260804/task_runs-full.sql
```

---

## 四、新增备份策略

### 4.1 备份触发时机

| 触发场景 | 备份内容 | 备份位置命名 |
|---|---|---|
| 重大配置变更前（删除 agent / 改 openclaw.json）| openclaw.json + .env | `*.bak-YYYYMMDD` |
| SQLite 数据批量修改前 | state/openclaw.sqlite + workboard.sqlite | `*-bak-YYYYMMDD` |
| 新工作区删除前 | 整个工作区目录 | git snapshot commit |
| 凭证轮换前 | .env | `env.bak-YYYYMMDD` |

### 4.2 备份文件保留策略

- 备份文件**永久保留**（除非磁盘空间告急）
- 每个备份目录**记录**：
  - 创建时间（YYYYMMDD）
  - 创建原因（如「v8.52.0 转型前」「workboard cleanup 2026-08-04」）
  - 关联 commit（如有）
- 备份文件**不被** git track（除非 git history 需要）

### 4.3 备份位置选择

| 类型 | 推荐位置 | 原因 |
|---|---|---|
| SQLite 大文件 | `/data/disk/.openclaw/state-*-bak-YYYYMMDD` | 与运行时分离，避免污染主仓 |
| 配置文件 | `/data/disk/.openclaw/*.bak-YYYYMMDD` | 同上 |
| 工作区删除前 | git commit `*snapshot` 前缀 | git history 是永久备份 |
| Agent .env 凭证 | `/data/disk/.openclaw/agents-env-backup-YYYYMMDD/` | 独立目录，避免与其他备份混 |

---

## 五、备份验证 checklist

每次重大操作后必须验证：

- [ ] 备份文件大小 > 0
- [ ] 备份文件 mtime 在操作时间附近
- [ ] 备份文件可解压 / 可读（JSON 有效 / SQLite 有效）
- [ ] 备份位置命名清晰（含日期 + 原因）
- [ ] BACKUP-INVENTORY.md 已更新

---

*最后更新：2026-08-04*
*更新者：大管家*
*关联 commit：v8.52.0 转型（41acc6b8 snapshot） + workboard cleanup 2026-08-04*
