"""八字排盘核心算法 (Bazi / Four Pillars of Destiny).

设计要点
--------
1. **节气切月**、**立春换年**、**子时换日** 全部委托给成熟中文历法库 `cnlunar`
   （0.2.x+）。我们不重新发明日历，避免重复 tkinter-test 那种"自己写推算
   然后漏掉闰月/节气/子时"的 bug。

2. **十神** 与 **五行** 完全在 Python 层从日主视角重算（不读 cnlunar 的
   ten_god 字段 —— 多数历法库对此字段定义不一致，且 cnlunar 本身
   `today5Elements` 只返回日柱五行，不返回十神）。

3. **十神查表** 按"我克/克我/我生/生我/同我" + 阴阳同性/异性 推，
   而不是反向查表（这是 tkinter-test `Input.py:__tianganshishen__`
   那个 bug 的修复）。

4. **地支十神**：取本气藏干与日干算十神（本气优先 —— 这是主流子平术
   的标准做法），不使用反向查表或硬编码错误的"卯 10 个值"表。

参考:
- 子平真诠（沈孝瞻）
- 滴天髓（京图）
- 穷通宝鉴
- cnlunar 文档: https://pypi.org/project/cnlunar/

Author: programmer agent (for 大管家)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

try:
    import cnlunar
except ImportError as e:  # pragma: no cover - 环境缺失
    raise ImportError(
        "未安装 cnlunar，请先运行: pip install cnlunar"
    ) from e


# ============================================================================
# 天干地支常量
# ============================================================================

# 十天干
TIANGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

# 阴阳（按天干顺序，甲丙戊庚壬 = 阳；乙丁己辛癸 = 阴）
YIN_YANG = ["阳", "阴", "阳", "阴", "阳", "阴", "阳", "阴", "阳", "阴"]

# 天干五行
GAN_WUXING = {
    "甲": "木", "乙": "木",
    "丙": "火", "丁": "火",
    "戊": "土", "己": "土",
    "庚": "金", "辛": "金",
    "壬": "水", "癸": "水",
}

# 十二地支
DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 地支五行（按地支本气五行）
ZHI_WUXING = {
    "子": "水", "亥": "水",
    "寅": "木", "卯": "木",
    "巳": "火", "午": "火",
    "申": "金", "酉": "金",
    "辰": "土", "戌": "土", "丑": "土", "未": "土",
}

# 地支藏干（本气 / 中气 / 余气）
# 来源：子平术主流藏干表
ZHI_CANGAN = {
    "子": ["癸"],
    "丑": ["己", "癸", "辛"],   # 本气己土，中气癸水，余气辛金
    "寅": ["甲", "丙", "戊"],
    "卯": ["乙"],
    "辰": ["戊", "乙", "癸"],
    "巳": ["丙", "戊", "庚"],
    "午": ["丁", "己"],
    "未": ["己", "丁", "乙"],
    "申": ["庚", "壬", "戊"],
    "酉": ["辛"],
    "戌": ["戊", "辛", "丁"],
    "亥": ["壬", "甲"],
}

# 时辰地支（按本地时间，23:00 起的子时换日由 cnlunar 处理）
# 子[23-01] 丑[01-03] 寅[03-05] ... 亥[21-23]
HOUR_TO_ZHI = [
    ("子", (23, 24)), ("子", (0, 1)),
    ("丑", (1, 3)), ("寅", (3, 5)),
    ("卯", (5, 7)), ("辰", (7, 9)),
    ("巳", (9, 11)), ("午", (11, 13)),
    ("未", (13, 15)), ("申", (15, 17)),
    ("酉", (17, 19)), ("戌", (19, 21)),
    ("亥", (21, 23)),
]

# 五行相生相克（用于十神判定）
SHENG = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}  # 我生
KE    = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}  # 我克
# 派生
SHENG_ME = {v: k for k, v in SHENG.items()}  # 生我的
KE_ME    = {v: k for k, v in KE.items()}     # 克我的
SAME     = lambda x: x                        # 同我的


# ============================================================================
# 工具函数
# ============================================================================

def wuxing_of_gan(g: str) -> str:
    return GAN_WUXING[g]


def wuxing_of_zhi(z: str) -> str:
    return ZHI_WUXING[z]


def yinyang_of_gan(g: str) -> str:
    return YIN_YANG[TIANGAN.index(g)]


def is_yang(g: str) -> bool:
    return yinyang_of_gan(g) == "阳"


def benqi_cangan(zhi: str) -> str:
    """地支本气藏干（十神判定的标准主气）."""
    return ZHI_CANGAN[zhi][0]


def ten_god(day_master: str, other: str) -> str:
    """十神判定 —— 从日主视角看 other 干（或本气藏干）.

    判定逻辑（正向，不反向查表）：
    1. 五行关系：
       - 同我         → 比肩/劫财（按阴阳同/异）
       - 我生         → 食神/伤官（按阴阳同/异）
       - 我克         → 偏财/正财（按阴阳同/异）
       - 生我         → 偏印/正印（按阴阳同/异）
       - 克我         → 七杀/正官（按阴阳同/异）
    2. 阴阳关系：
       - 同性（阳阳 / 阴阴）= 偏（劫/伤/偏/枭/杀）
       - 异性（阳阴 / 阴阳）= 正（肩/官/财/印/财）
       注意：比肩是"劫"对应的"正"位，但子平术中"比肩"专指同五行同阴阳，
       所以"同性同我"= 比肩，"异性同我"= 劫财。
    """
    me_wx = wuxing_of_gan(day_master)
    other_wx = wuxing_of_gan(other)
    me_yy = yinyang_of_gan(day_master)
    other_yy = yinyang_of_gan(other)
    same_yy = (me_yy == other_yy)

    if other_wx == me_wx:
        return "比肩" if same_yy else "劫财"
    if other_wx == SHENG[me_wx]:
        return "食神" if same_yy else "伤官"
    if other_wx == KE[me_wx]:
        return "偏财" if same_yy else "正财"
    if other_wx == SHENG_ME[me_wx]:
        return "偏印" if same_yy else "正印"
    if other_wx == KE_ME[me_wx]:
        return "七杀" if same_yy else "正官"
    raise ValueError(f"impossible wuxing relation: {me_wx} vs {other_wx}")


def ten_god_of_zhi(day_master: str, zhi: str) -> str:
    """地支十神（取本气藏干与日干算十神）."""
    return ten_god(day_master, benqi_cangan(zhi))


# ============================================================================
# 四柱数据类
# ============================================================================

@dataclass
class Pillar:
    """单柱（天干 + 地支 + 十神 + 五行）."""
    gan: str
    zhi: str
    gan_wuxing: str = ""
    zhi_wuxing: str = ""
    gan_shishen: str = ""        # 天干十神
    zhi_shishen: str = ""        # 地支本气十神
    canggan: list = field(default_factory=list)  # 地支全部藏干（信息用）

    def __post_init__(self):
        if not self.gan_wuxing:
            self.gan_wuxing = wuxing_of_gan(self.gan)
        if not self.zhi_wuxing:
            self.zhi_wuxing = wuxing_of_zhi(self.zhi)
        if not self.canggan:
            self.canggan = list(ZHI_CANGAN[self.zhi])

    def render(self, day_master: str = "") -> "Pillar":
        """填充十神（按日主视角）."""
        if day_master:
            self.gan_shishen = ten_god(day_master, self.gan)
            self.zhi_shishen = ten_god_of_zhi(day_master, self.zhi)
        return self


@dataclass
class Bazi:
    """完整八字（四柱 + 日主 + 农历信息）."""
    year: Pillar
    month: Pillar
    day: Pillar
    hour: Pillar
    day_master: str
    gender: str = ""           # 暂留位（后续大运/流年需用）
    solar: datetime = None     # type: ignore
    lunar_year_cn: str = ""    # 农历年（中文）
    lunar_month_cn: str = ""   # 农历月（中文）
    lunar_day_cn: str = ""     # 农历日（中文）
    shengxiao: str = ""        # 生肖
    jieqi: str = ""            # 当日所临近节气

    def four_pillars(self) -> list[Pillar]:
        return [self.year, self.month, self.day, self.hour]

    def pretty(self) -> str:
        """人类可读排盘（竖排）。"""
        lines = []
        lines.append(f"公历：{self.solar.strftime('%Y-%m-%d %H:%M')}")
        lines.append(
            f"农历：{self.lunar_year_cn}年 {self.lunar_month_cn} {self.lunar_day_cn}"
        )
        lines.append(f"生肖：{self.shengxiao}    节气：{self.jieqi or '无'}")
        lines.append("")

        header = ["年柱", "月柱", "日柱", "时柱"]
        gans   = [p.gan for p in self.four_pillars()]
        zhis   = [p.zhi for p in self.four_pillars()]
        gan_ss = [p.gan_shishen for p in self.four_pillars()]
        zhi_ss = [p.zhi_shishen for p in self.four_pillars()]

        lines.append("  " + "  ".join(f"{h:^6}" for h in header))
        lines.append(
            "  " + "  ".join(
                f"{g}（{gs}）".center(6) for g, gs in zip(gans, gan_ss)
            )
        )
        lines.append(
            "  " + "  ".join(
                f"{z}（{zs}）".center(6) for z, zs in zip(zhis, zhi_ss)
            )
        )
        lines.append("")
        lines.append(f"日主：{self.day_master}（{wuxing_of_gan(self.day_master)}）")
        # 藏干明细
        lines.append("")
        lines.append("地支藏干：")
        for h, p in zip(header, self.four_pillars()):
            if len(p.canggan) == 1:
                cg_str = p.canggan[0]
            else:
                cg_str = " ".join(p.canggan)
            lines.append(f"  {h} {p.zhi}: {cg_str}")
        return "\n".join(lines)


# ============================================================================
# 核心：build_bazi
# ============================================================================

def build_bazi(solar: datetime) -> Bazi:
    """根据公历时间构造完整八字.

    子时换日、立春换年、节气切月 —— 全部由 cnlunar 处理。
    """
    # cnlunar 已正确处理：
    #   - 子时（23:00-00:59）→ 取下一天日柱
    #   - 立春换年（在 02-04 当日用新干支）
    #   - 节气切月（month8Char 是按节气推的月柱）
    l = cnlunar.Lunar(solar)

    year_p  = Pillar(gan=l.year8Char[0],  zhi=l.year8Char[1])
    month_p = Pillar(gan=l.month8Char[0], zhi=l.month8Char[1])
    day_p   = Pillar(gan=l.day8Char[0],   zhi=l.day8Char[1])
    hour_p  = Pillar(gan=l.twohour8Char[0], zhi=l.twohour8Char[1])

    day_master = l.day8Char[0]
    year_p.render(day_master)
    month_p.render(day_master)
    day_p.render(day_master)
    hour_p.render(day_master)

    # 农历中文（cnlunar 返回 e.g. "正月大" "廿一"）
    # monthCN/daysCN: '一九九六一九九六', '正月小', '廿一'
    day_cn_tuple = l.get_lunarCn()
    lunar_year_cn = day_cn_tuple[0][4:] if day_cn_tuple[0] else ""
    lunar_month_cn = day_cn_tuple[1] if len(day_cn_tuple) > 1 else ""
    lunar_day_cn = day_cn_tuple[2] if len(day_cn_tuple) > 2 else ""

    # 生肖: cnlunar.get_chineseZodiacClash 返回 "马日冲鼠" 这种, 生肖 = 第一个字
    zodiac_full = l.get_chineseZodiacClash() or ""
    shengxiao = zodiac_full[:1] if zodiac_full else ""

    # 节气（当日可能为空 → 取近日）
    jieqi = l.get_todaySolarTerms() or ""

    return Bazi(
        year=year_p,
        month=month_p,
        day=day_p,
        hour=hour_p,
        day_master=day_master,
        solar=solar,
        lunar_year_cn=lunar_year_cn,
        lunar_month_cn=lunar_month_cn,
        lunar_day_cn=lunar_day_cn,
        shengxiao=shengxiao,
        jieqi=jieqi,
    )


def build_bazi_from_str(date_str: str, time_str: str = "12:00") -> Bazi:
    """便捷入口：`build_bazi_from_str("1996-03-10", "14:30")`."""
    y, m, d = date_str.split("-")
    hh, mm = time_str.split(":")
    solar = datetime(int(y), int(m), int(d), int(hh), int(mm))
    return build_bazi(solar)


# ============================================================================
# 流年 / 流月 / 流时 推算（扩展）
# ============================================================================
#
# 设计说明：
# - 直接复用 build_bazi() 得到目标时刻的 Bazi（节气切月 / 立春换年 /
#   子时换日 全部由 cnlunar 处理，与基础排盘一致）。
# - 流年：用 年中日期 (year, 6, 1, 12, 0) 作为参考点，确保取到 year
#   的年柱（避开立春日边界，6 月绝无歧义）。
# - 流月：用 (year, month, 15, 12, 0) 作为参考点（15 号必不跨节气）。
# - 流时：直接用目标 datetime（子时换日交给 cnlunar）。
# - 与命局的"关系"判定（六合 / 六冲 / 三合 / 天克地冲 等）全部委托给
#   `bazi_relations` 模块——不在 bazi.py 里硬编码 relation table。
# - 与命主日主的十神关系复用 `ten_god()`。

from bazi_relations import pillar_relation, zhi_relation, gan_relation


def _build_target_bazi(year: int, month: int = None, day: int = None,
                       hour: int = 12, minute: int = 0) -> Bazi:
    """构造目标时刻的 Bazi（内部 helper）.

    流年：month=6 day=1（保证年后半年，立春后）
    流月：day=15（保证月内，节气内）
    流时：传入真实 datetime
    """
    if day is None:
        if month is None:
            day = 1
            month = 6
        else:
            day = 15
    if month is None:
        month = 6
    return build_bazi(datetime(year, month, day, hour, minute))


def _shishen_str(day_master: str, pillar) -> str:
    """返回 '天干十神 | 地支本气十神' 字符串."""
    gan_ss = ten_god(day_master, pillar.gan)
    zhi_ss = ten_god_of_zhi(day_master, pillar.zhi)
    return f"{gan_ss} | 地支{pillar.zhi}({pillar.canggan[0]})={zhi_ss}"


def _render_section(title: str, lines: list) -> str:
    """render 一节标题 + 内容."""
    out = [f"━━━ {title} ━━━"]
    out.extend(lines)
    return "\n".join(out)


def _liuyun_text(birth: Bazi, target_year: Bazi, birth_pos: str,
                 target_pos: str, target_label: str,
                 target_value: str) -> str:
    """流年 / 流月 / 流时 共用的渲染逻辑.

    birth_pos: 命局对照柱（"年柱"/"月柱"/"日柱"/"时柱"）
    target_pos: 目标柱（"年柱"/"月柱"/"时柱"）
    """
    target_pillar = {
        "年柱": target_year.year,
        "月柱": target_year.month,
        "时柱": target_year.hour,
    }[target_pos]

    birth_pillar = {
        "年柱": birth.year,
        "月柱": birth.month,
        "日柱": birth.day,
        "时柱": birth.hour,
    }[birth_pos]

    rel = pillar_relation(target_pillar, birth_pillar)

    lines = []
    lines.append(f"目标{target_label}：{target_value}")
    lines.append(f"流{target_pos[:1]}柱：{target_pillar.gan}{target_pillar.zhi}")
    lines.append(f"  └ 干十神（vs 日主{birth.day_master}）：{ten_god(birth.day_master, target_pillar.gan)}")
    lines.append(f"  └ 支本气（{target_pillar.zhi} 本气 {target_pillar.canggan[0]}）十神：{ten_god_of_zhi(birth.day_master, target_pillar.zhi)}")
    lines.append("")
    lines.append(f"与命主{birth_pos}（{birth_pillar.gan}{birth_pillar.zhi}）的关系：")
    lines.append(f"  天干：{target_pillar.gan} vs {birth_pillar.gan} → {' | '.join(rel['gan_rels'])}")
    lines.append(f"  地支：{target_pillar.zhi} vs {birth_pillar.zhi} → {' | '.join(rel['zhi_rels'])}")
    lines.append(f"  综合：{' | '.join(rel['combined'])}")
    return "\n".join(lines)


def liunian(birth: Bazi, year: int) -> dict:
    """流年柱推算：给定公历年份 year，返回与命主的关系字典.

    返回 dict：
    - target_year_pillar:  {"gan": ..., "zhi": ...}
    - target_year:         cnlunar 推算的 year 年柱 Bazi（部分字段）
    - vs_day_master:       {"gan_shishen", "zhi_shishen"}  vs 命主日主
    - vs_birth_year:       pillar_relation 判定结果
    """
    target = _build_target_bazi(year)
    rel = pillar_relation(target.year, birth.year)
    return {
        "year": year,
        "target_year_pillar": {"gan": target.year.gan, "zhi": target.year.zhi},
        "vs_day_master": {
            "gan_shishen": ten_god(birth.day_master, target.year.gan),
            "zhi_shishen": ten_god_of_zhi(birth.day_master, target.year.zhi),
            "zhi_benqi": target.year.canggan[0],
        },
        "vs_birth_year": rel,
    }


def liunian_text(birth: Bazi, year: int) -> str:
    """流年的纯文本输出."""
    info = liunian(birth, year)
    target = _build_target_bazi(year)
    return _liuyun_text(
        birth, target,
        birth_pos="年柱",
        target_pos="年柱",
        target_label="流年",
        target_value=f"{year} 年",
    )


def liumonth(birth: Bazi, year: int, month: int) -> dict:
    """流月柱推算：给定公历 (year, month)，返回与命主的关系字典."""
    target = _build_target_bazi(year, month=month)
    rel = pillar_relation(target.month, birth.month)
    return {
        "year": year,
        "month": month,
        "target_month_pillar": {"gan": target.month.gan, "zhi": target.month.zhi},
        "vs_day_master": {
            "gan_shishen": ten_god(birth.day_master, target.month.gan),
            "zhi_shishen": ten_god_of_zhi(birth.day_master, target.month.zhi),
            "zhi_benqi": target.month.canggan[0],
        },
        "vs_birth_month": rel,
    }


def liumonth_text(birth: Bazi, year: int, month: int) -> str:
    """流月的纯文本输出."""
    info = liumonth(birth, year, month)
    target = _build_target_bazi(year, month=month)
    return _liuyun_text(
        birth, target,
        birth_pos="月柱",
        target_pos="月柱",
        target_label="流月",
        target_value=f"{year}-{month:02d} 月",
    )


def liushi(birth: Bazi, target_dt: datetime) -> dict:
    """流时柱推算：给定 datetime，返回与命主的关系字典."""
    target = build_bazi(target_dt)
    rel = pillar_relation(target.hour, birth.hour)
    return {
        "target_dt": target_dt.strftime("%Y-%m-%d %H:%M"),
        "target_hour_pillar": {"gan": target.hour.gan, "zhi": target.hour.zhi},
        "target_year_pillar": {"gan": target.year.gan, "zhi": target.year.zhi},
        "target_month_pillar": {"gan": target.month.gan, "zhi": target.month.zhi},
        "target_day_pillar": {"gan": target.day.gan, "zhi": target.day.zhi},
        "vs_day_master": {
            "gan_shishen": ten_god(birth.day_master, target.hour.gan),
            "zhi_shishen": ten_god_of_zhi(birth.day_master, target.hour.zhi),
            "zhi_benqi": target.hour.canggan[0],
        },
        "vs_birth_hour": rel,
        "target_solar": target.solar.strftime("%Y-%m-%d %H:%M"),
        "target_lunar": f"{target.lunar_year_cn}年 {target.lunar_month_cn} {target.lunar_day_cn}",
    }


def liushi_text(birth: Bazi, target_dt: datetime) -> str:
    """流时的纯文本输出."""
    info = liushi(birth, target_dt)
    target = build_bazi(target_dt)
    return _liuyun_text(
        birth, target,
        birth_pos="时柱",
        target_pos="时柱",
        target_label="流时",
        target_value=target_dt.strftime("%Y-%m-%d %H:%M"),
    )


# ============================================================================
# 自测入口
# ============================================================================

if __name__ == "__main__":  # pragma: no cover
    import sys
    if len(sys.argv) >= 3:
        solar = datetime.strptime(
            f"{sys.argv[1]} {sys.argv[2]}", "%Y-%m-%d %H:%M"
        )
    elif len(sys.argv) == 2:
        solar = datetime.strptime(sys.argv[1], "%Y-%m-%d")
    else:
        solar = datetime.now()
    print(build_bazi(solar).pretty())