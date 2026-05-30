# EasyScholar API 参考

> 使用 easyScholar API 获取期刊等级和 SCI 分区信息，集成在 `Summarizer.update_jcr()` 方法中

---

## 快速开始

### 1. 获取 API Key

1. 访问 [easyScholar](https://www.easyscholar.cc) 注册账号
2. 在 [API 页面](https://www.easyscholar.cc/console/user/open) 获取 API Key
3. 设置环境变量：
   ```bash
   export EASYSCHOLAR_API_KEY=***
   ```

### 2. 配置 API Key（两种方式）

**方式一：环境变量（推荐）**
```bash
export EASYSCHOLAR_API_KEY=***
```

**方式二：CLI 参数直接传入**
```bash
research-assistant summarize --kb-path knowledge/index.json --update-jcr --easyscholar-api-key YOUR_KEY
```

**方式三：Python API**
```python
from summarize.Summarizer import Summarizer
summarizer = Summarizer(kb_path="knowledge/index.json", easyscholar_api_key="YOUR_KEY")
stats = summarizer.update_jcr()
```

---

## API 端点

```
GET https://easyscholar.cc/open/getPublicationRank
```

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `secretKey` | string | ✓ | API 密钥 |
| `publicationName` | string | ✓ | 期刊名称 (URL 编码) |

### 返回字段

```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "customRank": {
      "rankInfo": [
        {
          "abbName": "JCRQ1Q2Q3Q4",
          "oneRankText": "Q1",
          "twoRankText": "Q2",
          "threeRankText": "Q3",
          "fourRankText": "Q4"
        },
        {
          "abbName": "SCI升级版2022",
          "oneRankText": "1区",
          "twoRankText": "2区",
          "threeRankText": "3区",
          "fourRankText": "4区"
        }
      ]
    }
  }
}
```

---

## 使用方式

### Python API

```python
from summarize.Summarizer import Summarizer

# 初始化
summarizer = Summarizer(kb_path="knowledge/index.json")

# 更新 JCR 分区（需设置 EASYSCHOLAR_API_KEY 环境变量）
stats = summarizer.update_jcr()
# {'total': 468, 'updated': 120, 'skipped': 348, 'errors': 0}

# 模拟运行（不保存）
stats = summarizer.update_jcr(dry_run=True)
```

### CLI 命令

```bash
# 更新知识库中论文的 JCR 分区
python3 scripts/summarize/Summarizer.py --kb-path knowledge/index.json --update-jcr

# 模拟运行（不保存）
python3 scripts/summarize/Summarizer.py --kb-path knowledge/index.json --update-jcr --dry-run
```

---

## 与 Summarizer 配合使用

`Summarizer.summarize()` 生成 `labels.type`（文献类型）和 `notes`（摘要分析），`Summarizer.update_jcr()` 补充 `labels.JCR`（期刊等级）。

**推荐工作流**：

```bash
# 1. 使用 summarize 生成文献类型和摘要
research-assistant summarize --kb-path knowledge/index.json

# 2. 使用 update_jcr 补充 JCR 分区
python3 scripts/summarize/Summarizer.py --kb-path knowledge/index.json --update-jcr
```

更新后的 `labels` 结构：

```json
{
  "type": "📊实证",
  "importance": "🔴奠基文献",
  "JCR": "Q1"
}
```

---

## 注意事项

1. **API Key 优先级**：实例变量 > 环境变量 > config.json
2. **API Key 安全**：不要将 API Key 直接写入代码或公开分享
3. **请求频率**：注意控制请求频率，避免触发限流
4. **数据更新**：期刊等级信息可能随年份变化，建议定期更新
5. **跳过已有数据**：`update_jcr()` 会跳过已有 JCR 值的文献
