修复完成！所有 12 个项目的元数据已按照 `数据结构.md` 标准更新：

---

## 修复内容总结

### 1. **删除了旧字段**
- `cloud_doc_mappings` - 已删除
- `manuscripts` - 已删除

### 2. **添加了标准字段**
- `markdown` - 扫描手稿目录自动填充
- `notes` - 扫描笔记目录自动填充（对象格式）
- `reviews` - 扫描综述目录自动填充
- `updated_at` - 自动更新时间戳

### 3. **修复了数据结构**
- `directories` - 使用标准键名（文档/手稿/知识库/笔记/综述/临时数据/草稿/检索条件/临时笔记）
- `documents` - 使用标准数组格式
- `notes` - 从数组格式改为对象格式

### 4. **修复了 Maintainer.py**
- 添加了 `markdown` 字段的自动扫描
- 添加了 `notes` 和 `reviews` 字段的自动扫描
- 删除了旧的 `manuscripts` 和 `cloud_doc_mappings` 处理
- 修复了 `notes` 使用对象格式而非数组格式
- 添加了 `_migrate_old_format()` 方法自动迁移旧数据

---

## 修复后的标准结构示例

```json
{
  "project_id": "项目名称",
  "title": "项目标题",
  "created_date": "2026-04-15",
  "status": "active",
  "version": "v1",
  "description": "项目描述",
  "directories": {
    "文档": "文档/",
    "手稿": "手稿/",
    "知识库": "知识库/",
    "笔记": "知识库/笔记/",
    "综述": "知识库/综述/",
    "临时数据": "临时数据/",
    "草稿": "临时数据/草稿/",
    "检索条件": "临时数据/检索条件/",
    "临时笔记": "临时数据/笔记/"
  },
  "documents": [
    {
      "title": "文档标题",
      "version": "v1",
      "path": "文档/文档标题.docx",
      "type": "user_uploaded"
    }
  ],
  "markdown": {
    "手稿标题.md": {
      "local_path": "手稿/手稿标题.md",
      "cloud": [
        {
          "platform": "feishu",
          "cloud_url": "https://xxx.feishu.cn/docx/xxx",
          "cloud_id": "doccnxxx",
          "created_at": "2026-04-15T10:00:00",
          "updated_at": "2026-04-15T10:00:00"
        }
      ]
    }
  },
  "notes": {
    "笔记.json": {
      "local_path": "知识库/笔记/笔记.json",
      "created_at": "2026-04-15",
      "description": "笔记描述"
    }
  },
  "reviews": {
    "综述.md": {
      "local_path": "知识库/综述/综述.md"
    }
  },
  "tags": [],
  "knowledge_base": {
    "index_file": "知识库/index.json",
    "description": "知识库描述",
    "updated_at": "2026-04-15"
  },
  "updated_at": "2026-04-26T10:04:00"
}
```

---

## 验证结果

所有 12 个项目均已修复：
1. ✅ AI降重提示工程
2. ✅ Zotero文件管理
3. ✅ 内卷感知与工作繁荣
4. ✅ 学生论文修改
5. ✅ 审稿学习
6. ✅ 影响者营销中的自我扩展机制
7. ✅ 数字化存储与自传体记忆
8. ✅ 科研实验室搭建
9. ✅ 维护老板信息
10. ✅ 范文学习
11. ✅ 跨期选择的年龄差异
12. ✅ 量表编制

---

## 后续使用建议

1. **使用 `Maintainer.py` 管理项目**：
   ```python
   from maintainer import Maintainer
   
   maintainer = Maintainer("~/实验室仓库/项目文件/项目名称")
   maintainer.organize()  # 自动整理文件
   maintainer.update_metadata()  # 更新元数据
   ```

2. **使用 `MetadataManager` 管理元数据**：
   ```python
   from maintainer import MetadataManager
   
   manager = MetadataManager("~/实验室仓库/项目文件/项目名称")
   manager.set_title("新标题").set_description("新描述").save()
   ```

3. **定期运行整理**：建议每周运行一次 `organize()` 保持项目整洁。