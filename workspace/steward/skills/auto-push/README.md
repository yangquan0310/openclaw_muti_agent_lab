# 自动推送技能（auto-push）

## 功能说明
每日自动推送代码到development分支的定时任务脚本，确保所有更改及时同步到远程仓库。

## 文件结构
```
auto-push/
├── auto-push.sh          # 核心执行脚本
├── README.md             # 技能说明文档
└── meta.json             # 技能元数据
```

## 执行逻辑
1. 进入仓库目录，切换到development分支
2. 拉取最新代码，避免冲突
3. 检查是否有未提交的更改
4. 自动添加、提交、推送到远程仓库
5. 记录执行日志到指定位置

## 执行时间
每日凌晨03:30（Asia/Shanghai时区）

## 日志位置
- 执行日志：`/root/教研室仓库/日志文件/心跳任务/cron_steward_auto-push.log`
- 任务结果：`session:CORN:steward的定时任务`会话中

## 脚本参数
无参数，直接执行即可：
```bash
/root/.openclaw/workspace/steward/skills/auto-push/auto-push.sh
```

## 状态码
| 码值 | 说明 |
|------|------|
| 0 | 执行成功（或无更改无需推送） |
| 1 | 执行失败 |

## 注意事项
- 自动提交的提交信息格式：`auto-push: 每日自动提交 YYYY-MM-DD HH:MM:SS`
- 仅推送development分支，main分支需要手动审核后合并
- 执行失败会在日志中记录详细错误信息
