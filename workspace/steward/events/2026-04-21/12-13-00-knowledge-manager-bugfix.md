# 事件 - 2026-04-21 12:13

## 事件描述

排查并修复 knowledge-manager 技能包 Searcher.py 的严重 Bug

## 涉及文件

- `/root/.openclaw/workspace/skills/knowledge-manager/search/Searcher.py`
- `/root/.openclaw/workspace/skills/knowledge-manager/SKILL.md`
- `/root/.openclaw/workspace/skills/knowledge-manager/search/SKILL.md`
- `/root/.openclaw/workspace/skills/knowledge-manager/summarize/SKILL.md`
- `/root/.openclaw/workspace/skills/knowledge-manager/manage/SKILL.md`
- `/root/.openclaw/workspace/skills/knowledge-manager/synthesize/SKILL.md`

## Bug 详情

### 发现的 3 个问题

| 问题 | 严重程度 | 位置 | 影响 |
|------|---------|------|------|
| **主题覆盖** | 🔴 严重 | `search()` 第 97 行 | 已有文献的主题被新检索的主题覆盖 |
| **Labels 清空** | 🔴 严重 | `search()` 第 99 行 | Summarizer 已填充的 labels 被重置为空 |
| **主题不合并** | 🟡 中等 | `_deduplicate()` | 同一文献多主题时只保留一个主题 |

### 修复内容

```python
# 修复前（有 Bug）
for p in papers:
    p['topic'] = [topic]           # ← 直接覆盖，不检查是否已有
    p['labels'] = {"type": "", "importance": "", "JCR": ""}  # ← 清空已有 labels
all_new_papers.extend(papers)

# 修复后
for p in papers:
    pid = p.get('paperId')
    if pid and pid in existing_map:
        # 已有文献：合并主题，保留原有 labels
        existing_paper = existing_map[pid]
        existing_topics = set(existing_paper.get('topic', []))
        existing_topics.add(topic)
        existing_paper['topic'] = list(existing_topics)
        # 不覆盖 labels，保留已有值
    else:
        # 新文献：设置主题和空 labels
        p['topic'] = [topic]
        p['labels'] = {"type": "", "importance": "", "JCR": ""}
        all_new_papers.append(p)
```

### 修复效果

1. **主题合并**：已有文献会合并新主题（`["主题A"]` → `["主题A", "主题B"]`）
2. **Labels 保留**：已有文献的 labels 不会被清空
3. **新文献正常**：新检索的文献仍然设置主题和空 labels
4. **统计信息更新**：新增文献数量统计更准确（显示"新文献: X 篇"）

## 同时完成的修改

### 1. kb_path 参数位置调整
- 将 `kb_path` 从各方法参数移至 `__init__` 构造函数参数
- 修改文件：所有 5 个 SKILL.md 文档

### 2. 工作流顺序调整
- 原顺序：检索 → 总结 → 管理 → 综述
- 新顺序：检索 → 管理（筛选保存笔记）→ 总结（基于筛选后的笔记）→ 综述

## 执行结果

✅ Bug 已修复，所有 SKILL.md 文档已同步更新

---

*记录时间: 2026-04-21 12:13*
*记录者: 大管家 (Steward)*
