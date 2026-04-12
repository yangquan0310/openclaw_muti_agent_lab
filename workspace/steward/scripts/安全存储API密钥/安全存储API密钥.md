# 安全存储API密钥

## 触发条件
需要安全存储新的API密钥

## 依赖
无

## 输入
- API密钥内容
- 服务名称(Zotero/Semantic Scholar/Baidu Scholar/其他)

## 步骤
1. **传递完整上下文给子代理**
   - 提供API密钥内容和服务名称
   - 明确目标文件路径:~/.openclaw/.env
   - 规定输出格式:确认存储成功或错误信息

2. **监控子代理执行任务**
   - 确定API Key类型(Zotero/Semantic Scholar/Baidu Scholar/其他)
   - 检查 ~/.openclaw/.env 文件是否存在,不存在则创建
   - 在文件末尾添加新的API密钥变量,格式:SERVICE_NAME_API_KEY=your_api_key_here
   - 设置文件权限 chmod 600 ~/.openclaw/.env
   - 验证密钥格式和可读性

3. **接收和验证子代理结果**
   - 确认子代理返回存储成功确认
   - 验证文件权限是否正确设置

4. **记录到工作日志**

## 输出
API密钥已安全存储,文件权限设置为600
