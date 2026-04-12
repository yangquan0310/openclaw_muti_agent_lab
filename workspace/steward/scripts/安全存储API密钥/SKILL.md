---
name: 安全存储API密钥
description: >
  安全存储API密钥到 ~/.openclaw/.env 文件，并设置正确的文件权限。
metadata:
  openclaw:
    emoji: "🔐"
    requires:
      bins: []
---

# 安全存储API密钥

## 触发条件
需要安全存储新的API密钥

## 执行方式
子代理执行

## 依赖
无

## 输入
- API密钥内容
- 服务名称(Zotero/Semantic Scholar/Baidu Scholar/其他)

## 步骤
1. 确定API Key类型
2. 检查 ~/.openclaw/.env 文件是否存在
3. 添加新的API密钥变量
4. 设置文件权限 chmod 600
5. 验证密钥格式

## 输出
API密钥已安全存储，文件权限设置为600
