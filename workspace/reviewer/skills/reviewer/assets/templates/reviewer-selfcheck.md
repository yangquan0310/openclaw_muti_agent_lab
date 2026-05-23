# reviewer 技能自检清单

> 创建/更新技能后使用此清单进行自检

---

## 1. 文件结构检查

```bash
# 检查目录结构
reviewer/
├── SKILL.md                    ✅ 存在
├── README.md                   ✅ 存在
├── _meta.json                  ✅ 存在
├── scripts/
│   └── review_checklist.py    ✅ 存在
├── references/
│   ├── index.md               ✅ 存在
│   ├── guide.md               ✅ 存在
│   ├── thesis-review-guide.md ✅ 存在
│   ├── journal-review-guide.md ✅ 存在
│   ├── opensource-review-guide.md ✅ 存在
│   ├── course-paper-review-guide.md ✅ 存在
│   └── proposal-review-guide.md ✅ 存在
└── assets/
    └── templates/
        └── reviewer-selfcheck.md ✅ 本文件
```

---

## 2. SKILL.md 前matter 验证

- [ ] 顶行是 `---`
- [ ] 包含 `name` 字段
- [ ] 包含 `description` 字段（触发条件）
- [ ] `description` 使用触发条件导向
- [ ] YAML 格式正确（无语法错误）

```bash
# 验证命令
python3 -c "import yaml; yaml.safe_load(open('SKILL.md').read().split('---')[1])"
```

---

## 3. description 触发条件检查

**有效触发示例：**
```yaml
description: >
  当用户要求「审稿」「审查论文」「审阅文稿」时触发。
```

**无效触发示例：**
```yaml
# ❌ 描述性而非触发条件
description: "这是一个审稿技能"

# ❌ 触发条件不明确
description: "用于审稿工作"
```

---

## 4. references/ 引用检查

- [ ] index.md 存在且包含所有指南索引
- [ ] guide.md 存在（通用指南）
- [ ] 各类型指南齐全：
  - [ ] thesis-review-guide.md
  - [ ] journal-review-guide.md
  - [ ] opensource-review-guide.md
  - [ ] course-paper-review-guide.md
  - [ ] proposal-review-guide.md

---

## 5. scripts/ 检查

- [ ] review_checklist.py 存在
- [ ] 可执行（`chmod +x`）
- [ ] 无语法错误

```bash
# 测试命令
python3 scripts/review_checklist.py --type thesis
python3 scripts/review_checklist.py --type journal
```

---

## 6. _meta.json 检查

- [ ] 包含 `name`
- [ ] 包含 `version`
- [ ] 包含 `description`
- [ ] 包含 `created`
- [ ] JSON 格式正确

```bash
# 验证命令
python3 -c "import json; json.load(open('_meta.json'))"
```

---

## 7. 功能测试

### 7.1 清单生成测试

```bash
# 学位论文清单
python3 scripts/review_checklist.py --type thesis --output /tmp/checklist_thesis.md

# 期刊论文清单
python3 scripts/review_checklist.py --type journal --output /tmp/checklist_journal.md
```

### 7.2 审稿维度覆盖测试

检查清单是否覆盖八大维度：
- [ ] 选题的重要性
- [ ] 文献综述质量
- [ ] 问题提出
- [ ] 研究方法
- [ ] 数据分析和结果
- [ ] 讨论和结论
- [ ] 文稿呈现
- [ ] 研究贡献

---

## 8. 审稿意见输出格式测试

验证输出包含：
- [ ] 总体评价
- [ ] 详细意见（按维度）
- [ ] 优先级标注（🔴🟡🟢🔵）
- [ ] 修改建议总结
- [ ] 审稿结论

---

## 9. 触发条件测试

在技能未加载时，使用以下短语测试是否能触发：
- 「审稿」
- 「审查论文」
- 「审阅文稿」
- 「检查论文」

---

## 10. git 提交检查

- [ ] 已添加到 git
- [ ] 已 commit
- [ ] commit 信息符合规范

```bash
git log -1 --oneline
```

---

## 快速自检命令

```bash
cd ~/.openclaw/workspace/reviewer/skills/reviewer

# 1. 结构检查
find . -type f | grep -v __pycache__ | sort

# 2. YAML 验证
python3 -c "import yaml; yaml.safe_load(open('SKILL.md').read().split('---')[1])" && echo "SKILL.md YAML OK"

# 3. JSON 验证
python3 -c "import json; json.load(open('_meta.json'))" && echo "_meta.json OK"

# 4. 清单脚本测试
python3 scripts/review_checklist.py --type thesis > /dev/null && echo "review_checklist.py OK"
```

---

*创建时间：2026-05-20*
