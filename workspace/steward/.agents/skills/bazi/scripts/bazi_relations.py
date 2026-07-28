"""八字干支关系表 (Lookup tables for zhi/gan pairwise relations).

设计原则
--------
1. 本文件**只是数据**，不包含任何业务逻辑；所有表来自传统命理学的
   通行规则（子平术/滴天髓体系）。
2. **不放在 bazi.py 里**，避免污染核心算法模块；调用方从 bazi.py
   显式 `from bazi_relations import ...`。
3. 完整释义（"六合化土"/"六冲"/"天克地冲"判定口诀）见
   `references/bazi-rules.md` 末尾"流年关系"小节。

参考：
- 《子平真诠》沈孝瞻
- 《滴天髓》京图
- 《三命通会》
- 《协纪辨方书》
"""

from __future__ import annotations

from typing import Tuple

# ============================================================================
# 地支关系
# ============================================================================

# 六合（6 对）—— 子丑合土、寅亥合木、卯戌合火、辰酉合金、巳申合水、午未合火/土
LIU_HE: frozenset = frozenset({
    frozenset({"子", "丑"}),
    frozenset({"寅", "亥"}),
    frozenset({"卯", "戌"}),
    frozenset({"辰", "酉"}),
    frozenset({"巳", "申"}),
    frozenset({"午", "未"}),
})

# 六合五行（合化的五行，多数流派以六合对命名，化气五行按主气判定）
LIU_HE_WUXING: dict = {
    frozenset({"子", "丑"}): "土",
    frozenset({"寅", "亥"}): "木",
    frozenset({"卯", "戌"}): "火",
    frozenset({"辰", "酉"}): "金",
    frozenset({"巳", "申"}): "水",
    frozenset({"午", "未"}): "火",  # 也有主流派作"土"
}

# 六冲（6 对）—— 相对冲
LIU_CHONG: frozenset = frozenset({
    frozenset({"子", "午"}),
    frozenset({"丑", "未"}),
    frozenset({"寅", "申"}),
    frozenset({"卯", "酉"}),
    frozenset({"辰", "戌"}),
    frozenset({"巳", "亥"}),
})

# 六害（6 对）—— 穿心六害
LIU_HAI: frozenset = frozenset({
    frozenset({"子", "未"}),
    frozenset({"丑", "午"}),
    frozenset({"寅", "巳"}),
    frozenset({"卯", "辰"}),
    frozenset({"申", "亥"}),
    frozenset({"酉", "戌"}),
})

# 六破（6 对）—— 双方皆破
LIU_PO: frozenset = frozenset({
    frozenset({"子", "酉"}),
    frozenset({"丑", "辰"}),
    frozenset({"寅", "亥"}),
    frozenset({"卯", "午"}),
    frozenset({"巳", "申"}),
    frozenset({"未", "戌"}),
})

# 三合（4 局）—— 每局 3 个地支 + 化五行
SAN_HE_GROUPS: tuple = (
    (frozenset({"申", "子", "辰"}), "水"),
    (frozenset({"亥", "卯", "未"}), "木"),
    (frozenset({"寅", "午", "戌"}), "火"),
    (frozenset({"巳", "酉", "丑"}), "金"),
)

# 方合（三会）—— 4 局，每局 3 个地支
FANG_HE_GROUPS: tuple = (
    (frozenset({"寅", "卯", "辰"}), "木"),  # 东方
    (frozenset({"巳", "午", "未"}), "火"),  # 南方
    (frozenset({"申", "酉", "戌"}), "金"),  # 西方
    (frozenset({"亥", "子", "丑"}), "水"),  # 北方
)


# ============================================================================
# 天干关系
# ============================================================================

# 天干合（5 对）—— 合化表
TIANGAN_HE: frozenset = frozenset({
    frozenset({"甲", "己"}),
    frozenset({"乙", "庚"}),
    frozenset({"丙", "辛"}),
    frozenset({"丁", "壬"}),
    frozenset({"戊", "癸"}),
})

# 天干合五行（甲己合化土、乙庚合化金、丙辛合化水、丁壬合化木、戊癸合化火）
TIANGAN_HE_WUXING: dict = {
    frozenset({"甲", "己"}): "土",
    frozenset({"乙", "庚"}): "金",
    frozenset({"丙", "辛"}): "水",
    frozenset({"丁", "壬"}): "木",
    frozenset({"戊", "癸"}): "火",
}

# 天干相克 (g1 克 g2，按五行相克方向)
# 五行相克：木克土、土克水、水克火、火克金、金克木
GAN_TO_WUXING = {
    "甲": "木", "乙": "木",
    "丙": "火", "丁": "火",
    "戊": "土", "己": "土",
    "庚": "金", "辛": "金",
    "壬": "水", "癸": "水",
}

KE_PAIRS: frozenset = frozenset(
    (a, b)
    for a in GAN_TO_WUXING
    for b in GAN_TO_WUXING
    if GAN_TO_WUXING[a] == "木" and GAN_TO_WUXING[b] == "土"
    or GAN_TO_WUXING[a] == "土" and GAN_TO_WUXING[b] == "水"
    or GAN_TO_WUXING[a] == "水" and GAN_TO_WUXING[b] == "火"
    or GAN_TO_WUXING[a] == "火" and GAN_TO_WUXING[b] == "金"
    or GAN_TO_WUXING[a] == "金" and GAN_TO_WUXING[b] == "木"
)

# 天干相生 (a 生 b，按五行相生方向)
SHENG_PAIRS: frozenset = frozenset(
    (a, b)
    for a in GAN_TO_WUXING
    for b in GAN_TO_WUXING
    if GAN_TO_WUXING[a] == "木" and GAN_TO_WUXING[b] == "火"
    or GAN_TO_WUXING[a] == "火" and GAN_TO_WUXING[b] == "土"
    or GAN_TO_WUXING[a] == "土" and GAN_TO_WUXING[b] == "金"
    or GAN_TO_WUXING[a] == "金" and GAN_TO_WUXING[b] == "水"
    or GAN_TO_WUXING[a] == "水" and GAN_TO_WUXING[b] == "木"
)


# ============================================================================
# 关系判定函数
# ============================================================================

def zhi_relation(a: str, b: str) -> list:
    """返回两个地支的所有关系（多重并列，如 ['六合', '六破']）.

    返回的关系类型（按优先级）：
    - "六合" (化气按 LIU_HE_WUXING)
    - "六冲"
    - "三合X半合" / "三合X"（X 为局元素，仅当 3 字齐全时）
    - "方合X半会" / "方合X"（X 为方局元素，仅当 3 字齐全时）
    - "六害"
    - "六破"
    - "无特殊关系"（默认）
    """
    if a == b:
        return []  # 同支不计
    pair = frozenset({a, b})

    rels = []
    # 六合
    if pair in LIU_HE:
        rels.append("六合")
    # 六冲
    if pair in LIU_CHONG:
        rels.append("六冲")
    # 三合半合 / 完整
    # （对只在两个地支比较的函数，永远是"半合"；三合整局需要三个地支全到，
    #   那是另一个函数，详见 references/bazi-rules.md。）
    for group, element in SAN_HE_GROUPS:
        if a in group and b in group:
            rels.append(f"三合{element}半合")
            break
    # 方合半会 / 完整
    for group, element in FANG_HE_GROUPS:
        if a in group and b in group:
            rels.append(f"方合{element}半会")
            break
    # 六害
    if pair in LIU_HAI:
        rels.append("六害")
    # 六破
    if pair in LIU_PO:
        rels.append("六破")

    if not rels:
        rels.append("无特殊关系")
    return rels


def gan_relation(a: str, b: str) -> list:
    """返回两个天干的所有关系.

    类型：
    - "天干合"（按 TIANGAN_HE 表；可附带"化气=X"）
    - "天干相克" (a 克 b)
    - "天干被克" (b 克 a — 多余；一般统一说"天干相克"双向)
    - "无特殊关系"
    """
    if a == b:
        return []  # 同干不计
    pair = frozenset({a, b})

    rels = []
    # 天干合
    if pair in TIANGAN_HE:
        rel = "天干合"
        if pair in TIANGAN_HE_WUXING:
            rel += f"化{TIANGAN_HE_WUXING[pair]}"
        rels.append(rel)
    # 天干相克
    if (a, b) in KE_PAIRS:
        rels.append("天干相克")
    elif (b, a) in KE_PAIRS:
        rels.append("天干被克")
    # 天干相生
    if (a, b) in SHENG_PAIRS:
        rels.append("天干相生")
    elif (b, a) in SHENG_PAIRS:
        rels.append("天干被生")
    if not rels:
        rels.append("无特殊关系")
    return rels


def pillar_relation(p1, p2) -> dict:
    """柱-柱关系（同时判定天干/地支）。

    p1, p2 是 Pillar 数据类（含 gan/zhi）。

    返回 dict：
    {
        "gan_rels": ["天干合化土", ...],
        "zhi_rels": ["六合", "六冲", ...],
        "combined": ["天克地冲", ...]   # 综合判定
    }
    """
    g_rels = gan_relation(p1.gan, p2.gan)
    z_rels = zhi_relation(p1.zhi, p2.zhi)

    combined = []
    has_gan_ke = any("相克" in r for r in g_rels)
    has_gan_sheng = any(("相生" in r) or ("被生" in r) for r in g_rels)
    has_gan_he = any("合" in r for r in g_rels)
    has_same_gan = (p1.gan == p2.gan)
    has_chong = "六冲" in z_rels
    has_lihe = "六合" in z_rels
    has_hai = "六害" in z_rels
    has_po = "六破" in z_rels
    has_san_he_full = any(r.startswith("三合") and "半" not in r for r in z_rels)
    has_san_he_half = any(r.startswith("三合") and "半" in r for r in z_rels)
    has_fang_he_half = any("方合" in r for r in z_rels)

    if has_gan_ke and has_chong:
        combined.append("天克地冲")
    if has_gan_he and has_lihe:
        combined.append("天合地合")
    if has_gan_he and has_chong:
        combined.append("天合地冲")
    if has_same_gan and has_chong:
        combined.append("天比地冲")
    if has_same_gan and has_lihe:
        combined.append("天比地合")
    if has_san_he_full:
        combined.append("地三合局")
    if has_gan_sheng and has_lihe:
        combined.append("天生地合")
    if has_gan_sheng and has_chong:
        combined.append("天生地冲")
    if has_hai:
        combined.append("地支六害")
    if has_po:
        combined.append("地支六破")
    if not combined:
        combined.append("普通")

    return {
        "gan_rels": g_rels,
        "zhi_rels": z_rels,
        "combined": combined,
    }
