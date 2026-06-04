# reference-doc/

Quarto 编译 PPTX 时用的母版。通过 YAML 引用：

```yaml
format:
  pptx:
    reference-doc: assets/reference-doc/brand-template.pptx
```

## 必备布局（Pandoc 按名字匹配）

`reference-doc` 必须包含以下 7 个布局名：

- `Title Slide`
- `Title and Content`
- `Section Header`
- `Two Content`
- `Comparison`
- `Content with Caption`
- `Blank`

缺失的布局 Pandoc 会告警并兜底。

**本目录的 6 份 .pptx 已通过合规性检查**（2026-06-04 验证：7 个英文 layout 全有）。

## 在 PowerPoint 里改母版

1. 打开 `.pptx`（用 PowerPoint）
2. View → Slide Master
3. 改背景色、字体、页脚
4. 保存回原位

## 文件清单

| 文件 | 用途 |
|------|------|
| `brand-template.pptx` | 通用品牌母版（默认，Quarto 默认 reference.pptx 导出）|
| `lora_hu_2021.pptx` | 参考·设计风 |
| `building_effective_agents.pptx` | 参考·技术风 |
| `kubernetes_blueprint_2026.pptx` | 参考·技术风 |
| `swiss_grid_systems.pptx` | 参考·极简风 |
| `kimsoong_loyalty_programme.pptx` | 参考·品牌风 |

## 生成新母版

```bash
# 导出默认母版做起点
quarto pandoc -o new-template.pptx --print-default-data-file reference.pptx
# 用 PowerPoint 打开 new-template.pptx → 修改 Slide Master → 保存
```

## 合规性检查脚本

```python
import zipfile, re, glob, os

REQUIRED = ['Title Slide', 'Title and Content', 'Section Header',
            'Two Content', 'Comparison', 'Content with Caption', 'Blank']

for f in sorted(glob.glob('*.pptx')):
    with zipfile.ZipFile(f) as z:
        names = []
        for l in z.namelist():
            if l.startswith('ppt/slideLayouts/') and l.endswith('.xml'):
                m = re.search(r'<p:cSld\s+name="([^"]*)"', z.read(l).decode('utf-8', errors='ignore'))
                if m: names.append(m.group(1))
        missing = [r for r in REQUIRED if r not in names]
        status = '✅' if not missing else '❌'
        print(f"{status} {f}: {len(names)} layouts, missing: {missing}")
```
