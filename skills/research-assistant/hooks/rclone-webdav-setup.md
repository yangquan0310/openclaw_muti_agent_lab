# Hook: rclone / WebDAV 配置（首次接入坚果云）

> **触发场景**：第一次在 VM 上配置 rclone 同步坚果云 WebDAV（用于 Zotero PDF 附件）。

## 5 步

```bash
# 1. 装 rclone
apt install rclone
# 或最新版
curl https://rclone.org/install.sh | sudo bash

# 2. 建 WebDAV remote
rclone config create nutstore webdav \
  url=https://dav.jianguoyun.com/dav \
  vendor=other \
  user='<JIANGUOYUN_USER>' \
  pass='<应用密码>'

# 3. 测连通
rclone lsd nutstore:

# 4. rclone obscure 密码（避免明文存 rclone.conf）
rclone obscure '<明文应用密码>'

# 5. 收紧权限
chmod 600 ~/.config/rclone/rclone.conf
```

## 应用密码

在坚果云网页后台生成：账户安全 → 第三方应用管理 → 应用密码（**不是**登录密码）。

## 同步目录约定

```
坚果云 WebDAV/
└── quanquanzi/
    └── zotero/
        └── storage/  ← Zotero PDF 附件（自动同步，禁手动修改）
```

## 常见错误

| 错误 | 原因 | 修复 |
|---|---|---|
| `Failed to create file system` | rclone.conf 没 remote | 跑 Step 2 |
| `401 Unauthorized` | 用户名/应用密码错 | 重新生成应用密码 |
| `directory not found` | 路径不存在 | GUI 创建目录 |
| `hash unsupported` | WebDAV 不支持 md5 | 跳过 hash 检查 |
