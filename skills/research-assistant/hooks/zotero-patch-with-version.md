# Hook: Zotero web API PATCH/PUT 用 If-Unmodified-Since-Version 头

> **触发**：用 web API 修改 Zotero item 字段（title / tags / creators 等）。
> **v5.15.0 实战修正**（2026-06-21 Al-Kari 案例）：Zotero API **不**用 HTTP 标准 `If-Match` 头，而用**自定义** `If-Unmodified-Since-Version` 头。

---

## 错误信息对照

| 错误 | 原因 | 修复 |
|---|---|---|
| `HTTP 428: Either If-Unmodified-Since-Version or object version property must be provided` | 用了 `If-Match`（Zotero 不认） | 改用 `If-Unmodified-Since-Version` |
| `HTTP 412: Item has been modified since specified version` | version 过期（Zotero sync 在改 item） | 重新 GET 拿最新 version 重试 |

---

## 正确 PATCH/PUT 模板

```python
import urllib.request
import json

# 1. GET 拿最新 version
get_url = f'https://api.zotero.org/users/{USER_ID}/items/{ITEM_KEY}'
req = urllib.request.Request(get_url, headers={
    'Authorization': f'Bearer {API_KEY}',
    'Zotero-API-Version': '3',
})
with urllib.request.urlopen(req, timeout=15) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    version = data['version']  # 最新 version
    full_data = data['data']

# 2. 改字段
full_data['title'] = 'New Title'  # 或其它字段

# 3. PUT 整个 item 替换
req = urllib.request.Request(
    get_url,
    data=json.dumps(full_data).encode('utf-8'),
    headers={
        'Authorization': f'Bearer {API_KEY}',
        'Zotero-API-Version': '3',
        'Content-Type': 'application/json',
        'If-Unmodified-Since-Version': str(version),  # 关键：自定义头
    },
    method='PUT',
)
with urllib.request.urlopen(req, timeout=15) as resp:
    result = json.loads(resp.read().decode('utf-8'))
    new_version = result['version']  # version +1
```

## PATCH 局部更新

```python
# PATCH 只改 title
req = urllib.request.Request(
    get_url,
    data=json.dumps({'title': 'New Title'}).encode('utf-8'),
    headers={...同上, 'If-Unmodified-Since-Version': str(version)},
    method='PATCH',
)
```

## 重试策略（412 race condition）

Zotero 库常因 sync 进程持续修改 item，导致 version 频繁过期：

```python
import time
for attempt in range(5):
    # GET 拿最新 version
    ...
    try:
        # PUT/PATCH with If-Unmodified-Since-Version
        ...
        break
    except urllib.error.HTTPError as e:
        if e.code == 412:
            time.sleep(2)  # 等 2 秒避开 sync
        else:
            break
```

## 实际案例（v5.15.0 实战）

Al-Kari (JBGDN6ZI) title 修正：
- 旧 title: `arXiv Query: search_query=&id_list=...`（v5.13.3 误入库）
- 新 title: `The Cognitive Categorical Transformer: Category-Theoretic Inductive Biases for Language Modeling`
- 用 `If-Unmodified-Since-Version: <version>` 头 + PUT，第一次就成功

## 相关 hook

- `manual-add-item.md` — 添加 item 时就用正确字段，避免后期 PATCH
- `arxiv-title-parse.md` — 解析 arXiv API 时用 `<entry>` 内 title，避免 query string
