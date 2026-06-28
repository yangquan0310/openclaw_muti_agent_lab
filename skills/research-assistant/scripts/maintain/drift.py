"""drift.py - DriftChecker 类（wiki ↔ Zotero ↔ WebDAV 三方一致性检查）"""

from __future__ import annotations

import re
import json
import subprocess
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

from scripts.utils import config, WIKI_SOURCES, WIKI_REPORTS


class DriftChecker:
    """wiki ↔ Zotero ↔ WebDAV 三方一致性检查器"""

    def __init__(self, cfg: dict | None = None):
        self.cfg = cfg or config()
        # config 优先；兑底从 ~/.openclaw/.env 读
        import os
        from pathlib import Path as _P
        env_path = _P.home() / ".openclaw" / ".env"
        env = {}
        if env_path.exists():
            for line in env_path.read_text(encoding="utf-8").splitlines():
                if "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip().strip('"').strip("'")
        self.zotero_user_id = (
            self.cfg.get("zotero", {}).get("user_id", "")
            or env.get("ZOTERO_USER_ID", "")
        )
        self.zotero_api_key = (
            self.cfg.get("zotero", {}).get("api_key", "")
            or env.get("ZOTERO_API_KEY", "")
        )
        self.webdav_remote = self.cfg.get("jianguoyun", {}).get("remote_root", "nutstore:quanquanzi/zotero/")
        self.wiki_sources = WIKI_SOURCES
        self.reports_dir = WIKI_REPORTS
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    # === wiki 侧 ===

    def _list_sources(self) -> list[dict]:
        """列出所有 wiki source"""
        result = []
        if not self.wiki_sources.exists():
            return result
        for f in sorted(self.wiki_sources.glob("*.md")):
            if f.name.startswith("_") or f.name == "index.md":
                continue
            content = f.read_text(encoding="utf-8")
            has_zotero = bool(re.search(r"^zotero_item_key:\s*\S", content, re.MULTILINE))
            has_doi = bool(re.search(r"^zotero_doi:\s*\S", content, re.MULTILINE))
            result.append({
                "file": str(f),
                "name": f.name,
                "has_zotero_item_key": has_zotero,
                "has_doi": has_doi,
                "is_academic": has_zotero or has_doi,
            })
        return result

    def _extract_zotero_key(self, source_file: str) -> str | None:
        content = Path(source_file).read_text(encoding="utf-8")
        m = re.search(r"^zotero_item_key:\s*(\S+)", content, re.MULTILINE)
        return m.group(1) if m else None

    # === Zotero 侧 ===

    def _verify_zotero_item(self, item_key: str) -> dict:
        """验证 Zotero item 是否存在"""
        if not self.zotero_api_key or not self.zotero_user_id:
            return {"exists": False, "error": "no_credentials"}
        url = f"https://api.zotero.org/users/{self.zotero_user_id}/items/{item_key}"
        req = urllib.request.Request(url, headers={
            "Authorization": f"Bearer {self.zotero_api_key}",
            "Zotero-API-Version": "3",
        })
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                d = data.get("data", {})
                return {
                    "exists": True,
                    "title": d.get("title"),
                    "itemType": d.get("itemType"),
                    "version": data.get("version"),
                }
        except urllib.error.HTTPError as e:
            return {"exists": False, "error": f"HTTP {e.code}"}
        except Exception as e:
            return {"exists": False, "error": str(e)}

    # === WebDAV 侧 ===

    def _check_webdav_pdf(self, attachment_key: str) -> dict:
        """检查 WebDAV 上是否有 PDF（用 rclone lsf）"""
        rclone_conf = self.cfg.get("upload", {}).get("rclone_config", "~/.config/rclone/rclone.conf")
        try:
            result = subprocess.run(
                ["rclone", "lsf", f"{self.webdav_remote}",
                 "--files-only", "--config", rclone_conf],
                capture_output=True, text=True, timeout=30,
            )
            if result.returncode != 0:
                return {"exists": False, "error": "rclone failed"}
            target = f"{attachment_key}.zip"
            files = result.stdout.strip().split("\n")
            return {"exists": target in files, "found_files": len(files)}
        except Exception as e:
            return {"exists": False, "error": str(e)}

    # === 主入口 ===

    def check(self) -> dict:
        """主入口：扫所有 wiki sources，对每个 source 查 Zotero + WebDAV

        Returns:
            {
                ok: [...],
                missing_key: [...],          # 学术型 source 缺 zotero_item_key
                zotero_not_found: [...],     # Zotero 库无此 item
                webdav_missing: [...],       # WebDAV 缺 PDF
                non_academic: [...],         # 非文献型 source（豁免）
            }
        """
        sources = self._list_sources()
        drift = {
            "ok": [],
            "missing_key": [],
            "zotero_not_found": [],
            "webdav_missing": [],
            "non_academic": [],
        }

        for s in sources:
            if not s["is_academic"]:
                drift["non_academic"].append(s)
                continue
            if not s["has_zotero_item_key"]:
                drift["missing_key"].append(s)
                continue
            key = self._extract_zotero_key(s["file"])
            if not key:
                drift["missing_key"].append(s)
                continue
            result = self._verify_zotero_item(key)
            if not result["exists"]:
                drift["zotero_not_found"].append({**s, "itemKey": key, "error": result.get("error")})
                continue
            # 检查 attachment
            content = Path(s["file"]).read_text(encoding="utf-8")
            m = re.search(r"^zotero_attachment_key:\s*(\S+)", content, re.MULTILINE)
            if m:
                att_key = m.group(1)
                webdav = self._check_webdav_pdf(att_key)
                if not webdav["exists"]:
                    drift["webdav_missing"].append({**s, "attachmentKey": att_key})
                    continue
            drift["ok"].append({**s, "itemKey": key, "zoteroTitle": result.get("title")})

        return drift

    def missing(self) -> list[dict]:
        """缺 zotero_item_key 的 sources（学术型）"""
        return [s for s in self._list_sources() if s["is_academic"] and not s["has_zotero_item_key"]]

    def report(self, drift: dict | None = None, output_path: Path | None = None) -> str:
        """生成漂移报告 markdown → wiki/reports/wiki-zotero-drift-<date>.md"""
        drift = drift or self.check()
        date = datetime.now().strftime("%Y-%m-%d")
        if output_path is None:
            output_path = self.reports_dir / f"wiki-zotero-drift-{date}.md"
        else:
            output_path = Path(output_path)

        lines = [f"# 漂移报告 - {date}", "",
                 "> 自动生成 by DriftChecker (v7.0.0)", "",
                 f"## 🟢 OK ({len(drift['ok'])})", ""]
        for s in drift["ok"]:
            lines.append(f"- ✅ `{s['name']}` → {s.get('zoteroTitle', '?')[:60]}")
        lines += ["", f"## 🔴 缺 zotero_item_key ({len(drift['missing_key'])})", ""]
        for s in drift["missing_key"]:
            lines.append(f"- ❌ `{s['name']}`")
        lines += ["", f"## 🟡 Zotero 库无此 item ({len(drift['zotero_not_found'])})", ""]
        for s in drift["zotero_not_found"]:
            lines.append(f"- ⚠️ `{s['name']}` → key={s.get('itemKey')} ({s.get('error')})")
        lines += ["", f"## 🟠 WebDAV 缺 PDF ({len(drift['webdav_missing'])})", ""]
        for s in drift["webdav_missing"]:
            lines.append(f"- ⚠️ `{s['name']}` → attachment={s.get('attachmentKey')}")
        lines += ["", f"## 📂 非学术型 source（豁免，{len(drift['non_academic'])})", ""]
        lines.append("> 这些 source 不含 DOI 字段，不参与三方漂移检测。")
        for s in drift["non_academic"]:
            lines.append(f"- 📄 `{s['name']}`")
        lines.append("")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("\n".join(lines), encoding="utf-8")
        return str(output_path)

    def graph(self, mode: str = "light") -> str:
        """三方联动 ASCII 状态图

        Args:
            mode: "light"（秒级，仅统计 wiki）/ "full"（跑完整三方检查）
        """
        sources = self._list_sources()
        total = len(sources)
        academic = [s for s in sources if s["is_academic"]]
        missing = self.missing()
        has_key = len(academic) - len(missing)
        non_academic = total - len(academic)

        if mode == "full":
            drift = self.check()
            zotero_count = len(drift["ok"]) + len(drift["zotero_not_found"])
            webdav_count = len(drift["ok"])
            ok_count = len(drift["ok"])
            zotero_missing = len(drift["zotero_not_found"])
            webdav_missing = len(drift["webdav_missing"])
        else:
            zotero_count = webdav_count = "?"
            ok_count = has_key
            zotero_missing = webdav_missing = "?"
            drift = None

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        W = 67
        L = [
            "=" * W,
            " " * 18 + "research-assistant 三方联动状态",
            " " * 18 + f"跑于 {now} ({mode} mode)",
            "=" * W, "",
            "         ┌──────────┐         ┌──────────┐         ┌──────────┐",
            "         │   wiki   │  ←───→  │  Zotero  │  ←───→  │  WebDAV  │",
            "         │  (后端)  │         │  (条目)  │         │  (附件)  │",
            f"         │ {str(has_key):>4} src │         │ {str(zotero_count):>4} item│         │ {str(webdav_count):>4} PDF │",
            "         └────┬─────┘         └────┬─────┘         └────┬─────┘",
            "              │                    │                    │",
            "              └────────────────────┴────────────────────┘",
            "                                   │",
            "                       DriftChecker",
            "                         (drift 检测)",
            "",
            "-" * W,
            f" 漂移统计（{mode} mode）",
            "-" * W,
        ]
        if mode == "light":
            L += [
                f"  🟢  wiki 学术型 OK        : {has_key} / {total - non_academic} 学术型 source",
                f"  🔴  wiki 学术型缺 zotero_item_key : {len(missing)} / {total - non_academic} 学术型 source",
                "  🟡  Zotero 库无此 item       : (未检查，跑 full 模式获取)",
                "  🟠  WebDAV 缺 PDF            : (未检查，跑 full 模式获取)",
                f"  📂  非学术型 source（豁免）  : {non_academic} / {total}",
                "",
                "  💡 跑 `python3 scripts/main.py maintain graph --full` 拿完整三方数据",
            ]
        else:
            L += [
                f"  🟢  wiki 学术型 OK        : {ok_count} / {total - non_academic} 学术型 source",
                f"  🔴  wiki 学术型缺 zotero_item_key : {len(drift['missing_key'])} / {total - non_academic} 学术型 source",
                f"  🟡  Zotero 库无此 item       : {zotero_missing} / {total - non_academic} 学术型 source",
                f"  🟠  WebDAV 缺 PDF            : {webdav_missing} / {total - non_academic} 学术型 source",
                f"  📂  非学术型 source（豁免）  : {non_academic} / {total}",
            ]
        L.append("=" * W)
        return "\n".join(L)
