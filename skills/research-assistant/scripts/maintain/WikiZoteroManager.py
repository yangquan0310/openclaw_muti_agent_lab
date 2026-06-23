#!/usr/bin/env python3
"""
WikiZoteroManager.py - wiki-zotero-webdav 三联动批量维护器
v5.15.0 实现：替代旧 MetadataManager/VersionController
"""

import os
import re
import json
import subprocess
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime


class WikiZoteroManager:
    """wiki-zotero-webdav 三联动维护器（v5.15.0）"""

    def __init__(self, wiki_path='~/.openclaw/wiki',
                 zotero_api_key=None, zotero_user_id=None,
                 webdav_remote='nutstore:',
                 rclone_conf='~/.config/rclone/rclone.conf'):
        self.wiki_path = Path(os.path.expanduser(wiki_path))
        self.webdav_remote = webdav_remote
        self.rclone_conf = os.path.expanduser(rclone_conf)

        # 从 .env 读 Zotero 凭据
        env = {}
        env_path = Path.home() / '.openclaw' / '.env'
        if env_path.exists():
            for line in env_path.read_text(encoding='utf-8').splitlines():
                if '=' in line and not line.startswith('#'):
                    k, v = line.split('=', 1)
                    env[k.strip()] = v.strip().strip('"').strip("'")
        self.zotero_api_key = zotero_api_key or env.get('ZOTERO_API_KEY')
        self.zotero_user_id = zotero_user_id or env.get('ZOTERO_USER_ID')

    # === wiki 侧 ===

    def list_wiki_sources(self):
        """列出所有 wiki source 页（排除模板和 index）

        v6.0.1 新增字段：has_doi, is_academic
          - is_academic = has_doi（含 DOI 字段的 source 视为学术型）
          - 非学术型 source（系统笔记 / 工具笔记 / 网页分享）由 check_drift 豁免
        """
        sources_dir = self.wiki_path / 'sources'
        result = []
        if not sources_dir.exists():
            return result
        for f in sorted(sources_dir.glob('*.md')):
            if f.name.startswith('_') or f.name == 'index.md':
                continue
            content = f.read_text(encoding='utf-8')
            has_zotero = bool(re.search(r'^zotero_item_key:\s*\S', content, re.MULTILINE))
            has_doi = bool(re.search(r'^zotero_doi:\s*\S', content, re.MULTILINE))
            # v6.0.1：学术型 = 含 zotero_item_key 或 zotero_doi 字段
            # （兼容 arXiv 论文等没 DOI 但有 Zotero key 的情况）
            result.append({
                'file': str(f),
                'name': f.name,
                'has_zotero_item_key': has_zotero,
                'has_doi': has_doi,
                'is_academic': has_zotero or has_doi,
            })
        return result

    def find_missing_zotero_keys(self):
        """列出学术型 source 缺 zotero_item_key 的（v6.0.1 排除非文献型）"""
        return [s for s in self.list_wiki_sources() if s['is_academic'] and not s['has_zotero_item_key']]

    def extract_zotero_key(self, source_file):
        """从 wiki source YAML 提取 zotero_item_key"""
        content = Path(source_file).read_text(encoding='utf-8')
        m = re.search(r'^zotero_item_key:\s*(\S+)', content, re.MULTILINE)
        return m.group(1) if m else None

    # === Zotero 侧 ===

    def verify_zotero_item(self, item_key):
        """验证 Zotero item 是否存在 + 拿元数据"""
        if not self.zotero_api_key or not self.zotero_user_id:
            return {'exists': False, 'error': 'no_credentials'}
        url = f'https://api.zotero.org/users/{self.zotero_user_id}/items/{item_key}'
        req = urllib.request.Request(url, headers={
            'Authorization': f'Bearer {self.zotero_api_key}',
            'Zotero-API-Version': '3',
        })
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                d = data.get('data', {})
                return {
                    'exists': True,
                    'title': d.get('title'),
                    'itemType': d.get('itemType'),
                    'version': data.get('version'),
                    'tags': [t['tag'] for t in d.get('tags', [])],
                }
        except urllib.error.HTTPError as e:
            return {'exists': False, 'error': f'HTTP {e.code}'}
        except Exception as e:
            return {'exists': False, 'error': str(e)}

    def add_wiki_tag(self, item_key, wiki_source_id):
        """给 Zotero item 加 wiki:source.<id> tag"""
        zotero_script = Path.home() / '.openclaw/skills/zotero/scripts/zotero.py'
        result = subprocess.run(
            ['python3', str(zotero_script), 'update', item_key,
             '--add-tags', f'wiki:{wiki_source_id}'],
            capture_output=True, text=True, timeout=30
        )
        return 'Updated successfully' in result.stdout

    # === WebDAV 侧 ===

    def check_webdav_pdf(self, attachment_key):
        """检查 WebDAV 上是否有 PDF"""
        result = subprocess.run(
            ['rclone', 'lsf', f'{self.webdav_remote}quanquanzi/zotero/',
             '--files-only', '--config', self.rclone_conf],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            return {'exists': False, 'error': 'rclone failed'}
        files = result.stdout.strip().split('\n')
        target = f'{attachment_key}.zip'
        return {'exists': target in files, 'found_files': len(files)}

    # === 漂移检测（核心） ===

    def check_drift(self):
        """检查学术型 wiki source ↔ Zotero ↔ WebDAV 一致性（v6.0.1 排除非文献型）

        非文献型 source（如系统笔记、工具笔记、网页分享）不参与三方对比，
        单独列在 'non_academic' 类别，由 generate_drift_graph 可视化展示。

        返回：
        {
          'ok': [...],                  # 三方同步正常（仅学术型）
          'missing_key': [...],         # 学术型 source 缺 zotero_item_key
          'zotero_not_found': [...],    # Zotero 库无此 item
          'webdav_missing': [...],      # WebDAV 缺 PDF
          'non_academic': [...],        # v6.0.1 新增：非文献型 source（豁免）
        }
        """
        sources = self.list_wiki_sources()
        drift = {
            'ok': [],
            'missing_key': [],
            'zotero_not_found': [],
            'webdav_missing': [],
            'non_academic': [],
        }

        for s in sources:
            # v6.0.1：非文献型 source 单独列出，不参与漂移检测
            if not s['is_academic']:
                drift['non_academic'].append(s)
                continue
            if not s['has_zotero_item_key']:
                drift['missing_key'].append(s)
                continue
            key = self.extract_zotero_key(s['file'])
            if not key:
                drift['missing_key'].append(s)
                continue
            result = self.verify_zotero_item(key)
            if not result['exists']:
                drift['zotero_not_found'].append({**s, 'itemKey': key, 'error': result.get('error')})
                continue
            # 提取 attachment_key（如果有）
            content = Path(s['file']).read_text(encoding='utf-8')
            m = re.search(r'^zotero_attachment_key:\s*(\S+)', content, re.MULTILINE)
            if m:
                att_key = m.group(1)
                webdav = self.check_webdav_pdf(att_key)
                if not webdav['exists']:
                    drift['webdav_missing'].append({**s, 'attachmentKey': att_key})
                    continue
            drift['ok'].append({**s, 'itemKey': key, 'zoteroTitle': result.get('title')})

        return drift

    def generate_drift_report(self, output_path=None):
        """生成漂移报告 markdown"""
        drift = self.check_drift()
        date = datetime.now().strftime('%Y-%m-%d')
        if output_path is None:
            output_path = self.wiki_path / 'reports' / f'wiki-zotero-drift-{date}.md'
        else:
            output_path = Path(output_path)

        lines = [f'# 漂移报告 - {date}', '',
                 f'> 自动生成 by WikiZoteroManager v6.0.1',
                 '',
                 f'## 🟢 OK ({len(drift["ok"])})', '']
        for s in drift['ok']:
            lines.append(f'- ✅ `{s["name"]}` → {s.get("zoteroTitle", "?")[:60]}')
        lines.append('')
        lines.append(f'## 🔴 缺 zotero_item_key ({len(drift["missing_key"])})')
        lines.append('')
        for s in drift['missing_key']:
            lines.append(f'- ❌ `{s["name"]}`')
        lines.append('')
        lines.append(f'## 🟡 Zotero 库无此 item ({len(drift["zotero_not_found"])})')
        lines.append('')
        for s in drift['zotero_not_found']:
            lines.append(f'- ⚠️ `{s["name"]}` → key={s.get("itemKey")} ({s.get("error")})')
        lines.append('')
        lines.append(f'## 🟠 WebDAV 缺 PDF ({len(drift["webdav_missing"])})')
        lines.append('')
        for s in drift['webdav_missing']:
            lines.append(f'- ⚠️ `{s["name"]}` → attachment={s.get("attachmentKey")}')
        lines.append('')
        lines.append(f'## 📂 非学术型 source（豁免，{len(drift["non_academic"])}）')
        lines.append('')
        lines.append('> 这些 source 不含 DOI 字段，不是文献条目（如系统笔记、工具笔记、网页分享），不参与三方漂移检测。')
        lines.append('')
        for s in drift['non_academic']:
            lines.append(f'- 📄 `{s["name"]}`')
        lines.append('')

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text('\n'.join(lines), encoding='utf-8')
        return str(output_path)


    def generate_drift_graph(self, mode='light'):
        """生成三方联动 ASCII 状态图（v6.0.0 新增）

        mode:
          - 'light': 仅统计 wiki source 侧（不查 Zotero API / WebDAV），秒级完成
          - 'full':  完整三方检查（耗时 1-5 分钟，依赖 source 数量）

        返回: ASCII 图字符串
        """
        sources = self.list_wiki_sources()
        total = len(sources)
        academic_sources = [s for s in sources if s['is_academic']]
        non_academic_count = total - len(academic_sources)
        academic_total = len(academic_sources)
        missing_key = self.find_missing_zotero_keys()  # 已过滤非学术型
        has_key_count = academic_total - len(missing_key)

        if mode == 'full':
            drift = self.check_drift()
            zotero_count = len(drift['ok']) + len(drift['zotero_not_found'])
            zotero_not_found_count = len(drift['zotero_not_found'])
            webdav_count = len(drift['ok'])
            webdav_missing_count = len(drift['webdav_missing'])
            ok_count = len(drift['ok'])
        else:
            zotero_count = zotero_not_found_count = '?'
            webdav_count = webdav_missing_count = '?'
            ok_count = has_key_count
            drift = None

        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        W = 67
        L = []
        L.append('═' * W)
        L.append(' ' * 18 + 'research-assistant 三方联动状态')
        L.append(' ' * 18 + f'跑于 {now} ({mode} mode)')
        L.append('═' * W)
        L.append('')
        L.append('         ┌──────────┐         ┌──────────┐         ┌──────────┐')
        L.append('         │   wiki   │  ←───→  │  Zotero  │  ←───→  │  WebDAV  │')
        L.append('         │  (后端)  │         │  (条目)  │         │  (附件)  │')
        L.append(f'         │ {str(has_key_count):>4} src │         │ {str(zotero_count):>4} item│         │ {str(webdav_count):>4} PDF │')
        L.append('         └────┬─────┘         └────┬─────┘         └────┬─────┘')
        L.append('              │                    │                    │')
        L.append('              └────────────────────┴────────────────────┘')
        L.append('                                   │')
        L.append('                       WikiZoteroManager')
        L.append('                         (drift 检测)')
        L.append('')
        L.append('─' * W)
        L.append(f' 漂移统计（{mode} mode）')
        L.append('─' * W)
        if mode == 'light':
            L.append(f'  🟢  wiki 学术型 OK        : {has_key_count} / {total - non_academic_count} 学术型 source')
            L.append(f'  🔴  wiki 学术型缺 zotero_item_key : {len(missing_key)} / {total - non_academic_count} 学术型 source')
            L.append(f'  🟡  Zotero 库无此 item       : (未检查，跑 full 模式获取)')
            L.append(f'  🟠  WebDAV 缺 PDF            : (未检查，跑 full 模式获取)')
            L.append(f'  📂  非学术型 source（豁免）  : {non_academic_count} / {total}（系统笔记 / 工具笔记 / 网页分享）')
            L.append('')
            L.append('  💡 跑 `python3 scripts/main.py maintain drift-graph --full` 拿完整三方数据')
        else:
            academic_total = total - non_academic_count
            L.append(f'  🟢  wiki 学术型 OK        : {ok_count} / {academic_total} 学术型 source')
            L.append(f'  🔴  wiki 学术型缺 zotero_item_key : {len(drift["missing_key"])} / {academic_total} 学术型 source')
            L.append(f'  🟡  Zotero 库无此 item       : {zotero_not_found_count} / {academic_total} 学术型 source')
            L.append(f'  🟠  WebDAV 缺 PDF            : {webdav_missing_count} / {academic_total} 学术型 source')
            L.append(f'  📂  非学术型 source（豁免）  : {non_academic_count} / {total}（系统笔记 / 工具笔记 / 网页分享）')
            L.append('')
            L.append('  💡 修复建议（仅针对学术型 source）：')
            if len(drift['missing_key']) > 0:
                L.append(f'     - {len(drift["missing_key"])} 缺 key：跑 `download --doi` 或手工 add-doi')
            if zotero_not_found_count > 0:
                L.append(f'     - {zotero_not_found_count} Zotero 找不到：跑 `list-missing` 看清单')
            if webdav_missing_count > 0:
                L.append(f'     - {webdav_missing_count} WebDAV 缺 PDF：跑 `download` 重新拉')
            if ok_count == academic_total and not zotero_not_found_count and not webdav_missing_count:
                L.append('     - ✅ 三方同步良好，无需操作')
        L.append('═' * W)
        return '\n'.join(L)


if __name__ == '__main__':
    import sys
    mgr = WikiZoteroManager()

    if len(sys.argv) < 2:
        print('用法: python3 WikiZoteroManager.py <命令>')
        print('  list-sources          列出所有 wiki source')
        print('  missing-keys          缺 zotero_item_key 的')
        print('  check-drift           漂移检测')
        print('  generate-report       生成 reports/wiki-zotero-drift-<date>.md')
        print('  drift-graph [--full]  三方联动 ASCII 状态图（默认 light）')
        print('  verify <KEY>          验证单个 Zotero item')
        print('  add-tag <KEY> <WIKI_ID>  加 wiki:source.<id> tag')
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == 'list-sources':
        for s in mgr.list_wiki_sources():
            mark = '✅' if s['has_zotero_item_key'] else '❌'
            print(f'{mark} {s["name"]}')
    elif cmd == 'missing-keys':
        for s in mgr.find_missing_zotero_keys():
            print(f'❌ {s["name"]}')
    elif cmd == 'check-drift':
        drift = mgr.check_drift()
        print(f'🟢 OK: {len(drift["ok"])}')
        print(f'🔴 缺 zotero_item_key: {len(drift["missing_key"])}')
        print(f'🟡 Zotero 库无此 item: {len(drift["zotero_not_found"])}')
        print(f'🟠 WebDAV 缺 PDF: {len(drift["webdav_missing"])}')
    elif cmd == 'generate-report':
        path = mgr.generate_drift_report()
        print(f'✅ 报告写入: {path}')
    elif cmd == 'verify' and len(sys.argv) > 2:
        print(json.dumps(mgr.verify_zotero_item(sys.argv[2]), indent=2, ensure_ascii=False))
    elif cmd == 'add-tag' and len(sys.argv) > 3:
        ok = mgr.add_wiki_tag(sys.argv[2], sys.argv[3])
        print('✅' if ok else '❌')
    elif cmd == 'drift-graph':
        mode = 'full' if len(sys.argv) > 2 and sys.argv[2] == '--full' else 'light'
        print(mgr.generate_drift_graph(mode=mode))
    else:
        print(f'未知命令: {cmd}')
        sys.exit(1)
