# LEARNINGS

## 2026-06-28 04:08（research-assistant v6.0.7 SciHub 整合）

**发生了什么**：老板 2026-06-28 04:08 升级 research-assistant 技能到 v6.0.7，原独立技能 `scihub-paper-downloader` (v1.0.3) 合并进 `scripts/download/scihub.py` 的 `SciHubDownloader` 类；CLI 新增 `--source {zotero,scihub}` 选项（默认 `zotero`）。

**关键设计原则**：
- `--source scihub` 仅落 `wiki/raw/papers`，**不动老板坚果云**（保留 Zotero 数据保护逻辑）
- 零外部依赖（纯 Python stdlib）+ ALTCHA 验证码自动解 + 6 镜像 fallback（`sci-hub.st/.ru/.se/.ren/.box/.workflow`，可由 `SCIHUB_MIRRORS` 环境变量覆盖）
- 4 状态语义：`FOUND` / `NOT_FOUND+OA_LINK` / `MIRROR_ERROR` / `INVALID_INPUT`
- `--source zotero` 行为完全不变（老板坚果云保护逻辑保留）——纯增量升级

**新调用方式**（取代原独立技能）：
```bash
python3 ~/.openclaw/skills/research-assistant/scripts/main.py download --doi <DOI> --source scihub
```

**对心理学家的应用场景**：
- 心理科学家身份（学术文献评述 / Meta 分析 / 文献综述）核心受益
- TASK-012 类 CFPPS 文献综述场景：Zotero 库里没有的"临时要读全文"论文用 `--source scihub` 兜底
- 已入 Zotero 的论文继续走默认 `--source zotero` 三联动（Zotero + 坚果云 + wiki raw）

**已同步**：
- `paper-reading.md` §8.4 检索 API 速查表已有 `--source scihub` 命令（无需再改）
- module-download.md（v7.0.0，含 v6.0.7 SciHub 整合）、SKILL.md、README.md、ARCHITECTURE.md、index.md 5 份文档均已升级

**教训/注意**：
- 引用 SciHub 兜底命令时使用完整路径 `~/.openclaw/skills/research-assistant/scripts/main.py download --doi <DOI> --source scihub`，不要用旧的独立技能调用方式（原 `scihub-paper-downloader` 已删除）
- 心理活动策划审核、心理咨询督导等不涉及文献下载的场景不受影响

