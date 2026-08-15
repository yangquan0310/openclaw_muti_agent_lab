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

import re
import calendar
from dataclasses import dataclass, field
from datetime import datetime
from functools import lru_cache
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

# 地支 → 生肖（生肖 = 年支，**不是**日支）
# 修复说明：旧代码错用 cnlunar.get_chineseZodiacClash() 返回 "马日冲鼠"
# （日冲信息），截第一个字当成生肖，导致输出日支"马"而不是年支"子"对应的"鼠"。
SHENGXIAO_MAP = {
    "子": "鼠", "丑": "牛", "寅": "虎", "卯": "兔",
    "辰": "龙", "巳": "蛇", "午": "马", "未": "羊",
    "申": "猴", "酉": "鸡", "戌": "狗", "亥": "猪",
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
        if self.solar is not None:
            lines.append(f"公历：{self.solar.strftime('%Y-%m-%d %H:%M')}")
            lines.append(
                f"农历：{self.lunar_year_cn}年 {self.lunar_month_cn} {self.lunar_day_cn}"
            )
        else:
            # 四柱直接输入：无公历/农历日期，按四柱展示
            pillars_str = " ".join(
                f"{p.gan}{p.zhi}" for p in self.four_pillars()
            )
            lines.append(f"公历：四柱输入（{pillars_str}，公历日期未知）")
            lines.append("农历：四柱输入（无对应农历日期）")
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

    # 生肖 = 年支对应的生肖（不是日支，不是日冲信息）
    shengxiao = SHENGXIAO_MAP.get(year_p.zhi, "")

    # 节气：当天显示节气名（如"立夏"）；非当天显示"上一节气后 N 天"（如"惊蛰后 5 天"）
    jieqi = jieqi_text(l, solar)

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


def _previous_jieqi(l, solar: datetime):
    """找出生日之前最近的节气（含日期）.

    cnlunar 的 `thisYearSolarTermsDic` 按公历年组织（{节气名: (月,日)}）：
    - 常规情况：取今年节气表中日期 <= 出生日 的最近一个；
    - 年初边界（小寒之前）：上一节气在上一年（冬至），
      需用上一年 12 月中旬的 Lunar 对象取上一年节气表。
    """
    this_year = solar.year
    try:
        items = []
        for name, (m, d) in l.thisYearSolarTermsDic.items():
            try:
                items.append((datetime(this_year, m, d, 12, 0), name))
            except ValueError:
                continue
        items.sort()
        prev = None
        for dt, name in items:
            if dt.date() <= solar.date():
                prev = (dt, name)
            else:
                break
        if prev is None:
            # 年初边界：取上一年最后一个节气（冬至）
            prev_l = cnlunar.Lunar(datetime(this_year - 1, 12, 15, 12, 0))
            p_items = []
            for name, (m, d) in prev_l.thisYearSolarTermsDic.items():
                try:
                    p_items.append((datetime(this_year - 1, m, d, 12, 0), name))
                except ValueError:
                    continue
            if p_items:
                prev = max(p_items)
        return prev
    except Exception:
        return None


def jieqi_text(l, solar: datetime) -> str:
    """节气显示文本（日级精度，cnlunar 限制，节气当天 ±1 天边界可能偏差）.

    - 节气当天 → 节气名（如"立夏"）；
    - 非节气当天 → "上一节气后 N 天"（如"惊蛰后 5 天"）；
    - 无节气信息 → ""（显示为"无"）。
    """
    today_term = l.get_todaySolarTerms()
    if today_term and today_term != "无":
        return today_term
    prev = _previous_jieqi(l, solar)
    if prev is None:
        return ""
    prev_dt, prev_name = prev
    days = (solar.date() - prev_dt.date()).days
    if days <= 0:
        return prev_name
    return f"{prev_name}后 {days} 天"


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

    # v1.12.0 修复：子时换日时显示日柱同步变更
    birth_day_gz = f"{birth.day.gan}{birth.day.zhi}"
    target_day_gz = f"{target_year.day.gan}{target_year.day.zhi}"
    if birth_day_gz != target_day_gz:
        lines.append(f"  └ ⚠️ 日柱同步变更：{birth_day_gz} → {target_day_gz}（子时换日）")

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
# v1.8.0 模块 1：正格（zhengge）—— 月令定格 + 透干 + 用神方向
# ============================================================================
#
# 设计依据：`references/bazi-zhengge.md` v1.0.1
# 核心问题：月令是否透干成标准八格？用神方向是什么？
#
# 算法概要：
# 1. 月支查表 → 月令本气（按主流子平术）
# 2. 月令本气 vs 日主 → 十神
# 3. 月令本气是否在天干透出？
#    - 是 → 标准八格（按十神命名）
#    - 否 → 变格 / 走旺衰（返回 ge_type=null + 透干位）
# 4. 喜忌按 `bazi-zhengge.md` §三.1 总则查表
# 5. 破格 / 救应 自动检测（基于四柱关系）

# 八格喜忌总则（按 bazi-zhengge.md §三.1）
# 键：格名（与 ge_type 返回一致）
# 值：(yongshen_direction 五行串, xiangshen, jishen, choushen, po_ge_check)
ZHENGGE_XIJI = {
    "正官格": {
        "yongshen_dir": "金水（财+官）",
        "yongshen_wuxing": "金水",
        "xiangshen": "财星",
        "jishen": "伤官",
        "choushen": "食神",
        "po_ge_check": "伤官见官",
        "po_ge_target_ten": ["伤官"],
    },
    "七杀格": {
        "yongshen_dir": "火土（食神制杀）",
        "yongshen_wuxing": "火土",
        "xiangshen": "印星",
        "jishen": "财星",
        "choushen": "官杀混杂",
        "po_ge_check": "财生杀旺",
        "po_ge_target_ten": ["偏财", "正财"],
    },
    "正印格": {
        "yongshen_dir": "金水（财+官）",
        "yongshen_wuxing": "金水",
        "xiangshen": "财星",
        "jishen": "木火",
        "choushen": "水",
        "po_ge_check": "印太旺无制",
        "po_ge_target_ten": ["比肩", "劫财"],
    },
    "偏印格": {
        "yongshen_dir": "金水（财制枭）",
        "yongshen_wuxing": "金水",
        "xiangshen": "财星",
        "jishen": "食神",
        "choushen": "枭神夺食",
        "po_ge_check": "偏印夺食",
        "po_ge_target_ten": ["食神"],
    },
    "正财格": {
        "yongshen_dir": "火金（食伤+官）",
        "yongshen_wuxing": "火金",
        "xiangshen": "官杀、食伤",
        "jishen": "比劫",
        "choushen": "劫财",
        "po_ge_check": "比劫夺财",
        "po_ge_target_ten": ["比肩", "劫财"],
    },
    "偏财格": {
        "yongshen_dir": "火土金（食伤生财）",
        "yongshen_wuxing": "火土金",
        "xiangshen": "食伤、正财",
        "jishen": "比劫",
        "choushen": "比劫",
        "po_ge_check": "比劫夺财",
        "po_ge_target_ten": ["比肩", "劫财"],
    },
    "食神格": {
        "yongshen_dir": "金水（财泄食）",
        "yongshen_wuxing": "金水",
        "xiangshen": "官杀",
        "jishen": "偏印",
        "choushen": "枭神夺食",
        "po_ge_check": "枭神夺食",
        "po_ge_target_ten": ["偏印"],
    },
    "伤官格": {
        "yongshen_dir": "金水木（财+正印）",
        "yongshen_wuxing": "金水木",
        "xiangshen": "财、正印",
        "jishen": "官杀",
        "choushen": "伤官见官",
        "po_ge_check": "伤官见官",
        "po_ge_target_ten": ["正官", "七杀"],
    },
    # 特殊格：建禄/羊刃（主流承认）
    "建禄格": {
        "yongshen_dir": "财官（克泄）",
        "yongshen_wuxing": "金水",
        "xiangshen": "财、官",
        "jishen": "比劫",
        "choushen": "印星",
        "po_ge_check": "比劫太旺",
        "po_ge_target_ten": ["比肩"],
    },
    "羊刃格": {
        "yongshen_dir": "官杀（制刃）",
        "yongshen_wuxing": "金水",
        "xiangshen": "官杀",
        "jishen": "财星",
        "choushen": "印星",
        "po_ge_check": "羊刃倒戈",
        "po_ge_target_ten": ["偏印"],
    },
}

# 月支 → 本气（用于月令查表）
YUELING_BENQI = {
    "子": "癸", "丑": "己", "寅": "甲", "卯": "乙",
    "辰": "戊", "巳": "丙", "午": "丁", "未": "己",
    "申": "庚", "酉": "辛", "戌": "戊", "亥": "壬",
}

# 月支 → 中气（用于变格判定）
YUELING_ZHONGQI = {
    "丑": "癸", "寅": "丙", "辰": "乙", "巳": "戊",
    "午": "己", "未": "丁", "申": "壬", "戌": "辛", "亥": "甲",
}

# 月支 → 余气（用于小变格判定）
YUELING_YUQI = {
    "丑": "辛", "寅": "戊", "辰": "癸", "巳": "庚",
    "未": "乙", "申": "戊", "戌": "丁",
}

# 十神 → 格名（反向）
SHISHEN_TO_GE = {
    "正官": "正官格",
    "七杀": "七杀格",
    "正印": "正印格",
    "偏印": "偏印格",
    "正财": "正财格",
    "偏财": "偏财格",
    "食神": "食神格",
    "伤官": "伤官格",
    "比肩": "建禄格",   # 特殊
    "劫财": "羊刃格",   # 特殊
}

# 天干集合
ALL_GANS = set(TIANGAN)


def _zhengge_check_po_ge(bz: Bazi, ge_type: str) -> str | None:
    """检查破格.

    按 `bazi-zhengge.md` §四.2 破格类型 + 喜忌总则：
    - 命中是否出现 po_ge_target_ten 的十神？
    - 若是，则可能破格（仅标注，不下死结论——给大管家整合层判断）
    """
    if ge_type not in ZHENGGE_XIJI:
        return None
    cfg = ZHENGGE_XIJI[ge_type]
    targets = cfg.get("po_ge_target_ten", [])

    for p in bz.four_pillars():
        if p.gan_shishen in targets:
            return f"命中{p.gan}{p.zhi}={p.gan_shishen} → {cfg['po_ge_check']}"
    return None


def _zhengge_check_jiu_ying(bz: Bazi, ge_type: str) -> str | None:
    """检查救应.

    简化的救应检测：
    - 命中是否有 xiangshen 中提到的十神？
    - 若是 → 标注救应成立
    """
    if ge_type not in ZHENGGE_XIJI:
        return None
    cfg = ZHENGGE_XIJI[ge_type]

    # 把 xiangshen 字符串解析成十神列表（中文拆词）
    # v1.13.0 优化（P2-5）：扩展关键词字典覆盖全部 10 神 + 阴阳两面
    xiangshen_text = cfg["xiangshen"]
    found_any = []
    for keyword, label in [
        # 印（阳面 + 阴面）
        ("印星", "印星"),
        ("正印", "正印"),
        ("偏印", "偏印"),
        ("枭神", "偏印"),
        # 财（阳面 + 阴面）
        ("财星", "财星"),
        ("财", "财星"),
        ("正财", "正财"),
        ("偏财", "偏财"),
        # 官杀（阳面 + 阴面）
        ("官杀", "官杀"),
        ("官", "官杀"),
        ("正官", "正官"),
        ("七杀", "七杀"),
        # 食伤（阳面 + 阴面）
        ("食伤", "食伤"),
        ("食神", "食神"),
        ("伤官", "伤官"),
        # 比劫（阳面 + 阴面）
        ("比劫", "比劫"),
        ("比肩", "比肩"),
        ("劫财", "劫财"),
    ]:
        if keyword in xiangshen_text:
            if label not in found_any:
                found_any.append(label)

    for p in bz.four_pillars():
        for label in found_any:
            if label == "印星" and p.gan_shishen in ("正印", "偏印"):
                return f"命中{p.gan}{p.zhi}={p.gan_shishen} → {label}护卫用神"
            if label == "财星" and p.gan_shishen in ("正财", "偏财"):
                return f"命中{p.gan}{p.zhi}={p.gan_shishen} → {label}生扶格局"
            if label == "官杀" and p.gan_shishen in ("正官", "七杀"):
                return f"命中{p.gan}{p.zhi}={p.gan_shishen} → {label}护格局"
            if label == "食伤" and p.gan_shishen in ("食神", "伤官"):
                return f"命中{p.gan}{p.zhi}={p.gan_shishen} → {label}助格局"
            if label == "比劫" and p.gan_shishen in ("比肩", "劫财"):
                return f"命中{p.gan}{p.zhi}={p.gan_shishen} → {label}制忌神"

    return None


def zhengge(bz: Bazi) -> dict:
    """正格判定（月令定格 + 透干 + 用神方向 + 破格/救应检测）.

    返回 dict：
    {
        "ge_type": str | None,         # 标准八格名 or "建禄/羊刃" 特殊 or None
        "ge_source": str,              # 一句话格局来源描述
        "yongshen_direction": str,     # 用神方向（中文）
        "yongshen_wuxing": str,        # 用神五行串
        "xiangshen": str,              # 相神
        "jishen": str,                 # 忌神
        "choushen": str,               # 仇神
        "po_ge": str | None,           # 破格描述（如有）
        "jiu_ying": str | None,        # 救应描述（如有）
        "tou_gan": str | None,         # 透干天干位（年/月/日/时）
        "tou_gan_pos": str | None,     # 透干天干具体字
        "month_benqi": str,            # 月令本气
        "month_benqi_shishen": str,    # 月令本气 vs 日主的十神
        "shensha_in_ge": list,         # 与格局相关的辅助十神信息
    }

    算法依据：`references/bazi-zhengge.md` v1.0.1
    流派口径：**主流口径（按月令当令）**—— 月支本气 vs 日主 = 什么十神 = 什么格。
    严格口径（透干）为备选项，在 ge_source 中标注。
    """
    day_master = bz.day_master
    month_zhi = bz.month.zhi
    month_benqi = YUELING_BENQI[month_zhi]
    month_ss = ten_god(day_master, month_benqi)

    # 检查四柱天干，看月令本气是否透出
    four_gans = [
        ("年", bz.year.gan, bz.year),
        ("月", bz.month.gan, bz.month),
        ("日", bz.day.gan, bz.day),
        ("时", bz.hour.gan, bz.hour),
    ]

    tou_gan = None
    tou_gan_pos = None
    tou_gan_pillar_name = None

    for pos_name, gan, p in four_gans:
        if gan == month_benqi:
            tou_gan = pos_name
            tou_gan_pos = gan
            tou_gan_pillar_name = f"{pos_name}干"
            break

    # **主流口径**：ge_type = 月令本气 vs 日主的十神（即使未透干也算正格）
    ge_type = SHISHEN_TO_GE.get(month_ss)

    # 如果没找到 ge_type（理论上不会，因为 SHISHEN_TO_GE 覆盖了所有十神）
    if ge_type is None:
        return {
            "ge_type": None,
            "ge_source": f"月支{month_zhi}本气{month_benqi}（{month_ss}）→ 未知格局",
            "yongshen_direction": "（待人工判定）",
            "yongshen_wuxing": "",
            "xiangshen": "",
            "jishen": "",
            "choushen": "",
            "po_ge": None,
            "jiu_ying": None,
            "tou_gan": None,
            "tou_gan_pos": None,
            "month_benqi": month_benqi,
            "month_benqi_shishen": month_ss,
            "shensha_in_ge": [],
        }

    # 查喜忌总则
    cfg = ZHENGGE_XIJI.get(ge_type, {
        "yongshen_dir": "（未知格局）",
        "yongshen_wuxing": "",
        "xiangshen": "",
        "jishen": "",
        "choushen": "",
        "po_ge_check": "",
        "po_ge_target_ten": [],
    })

    po_ge = _zhengge_check_po_ge(bz, ge_type)
    jiu_ying = _zhengge_check_jiu_ying(bz, ge_type)

    # ge_source 描述
    if tou_gan:
        ge_source = (
            f"月支{month_zhi}本气{month_benqi}（{month_ss}）→ "
            f"{tou_gan_pillar_name}透干 → {ge_type}"
        )
    else:
        ge_source = (
            f"月支{month_zhi}本气{month_benqi}（{month_ss}）→ "
            f"月令当令（主流口径） → {ge_type}（本气未透干）"
        )

    return {
        "ge_type": ge_type,
        "ge_source": ge_source,
        "yongshen_direction": cfg["yongshen_dir"],
        "yongshen_wuxing": cfg["yongshen_wuxing"],
        "xiangshen": cfg["xiangshen"],
        "jishen": cfg["jishen"],
        "choushen": cfg["choushen"],
        "po_ge": po_ge,
        "jiu_ying": jiu_ying,
        "tou_gan": tou_gan,
        "tou_gan_pos": tou_gan_pos,
        "month_benqi": month_benqi,
        "month_benqi_shishen": month_ss,
        "shensha_in_ge": [],
    }


# ============================================================================
# v1.8.0 模块 2：旺衰（wangshuai）—— 旺衰四维度 + 调候 + 流通
# ============================================================================
#
# 设计依据：`references/bazi-wangshuai.md` v1.0.0
# 核心问题：日主旺衰？调候用神？五行流通如何？

# 调候速查表（按 bazi-wangshuai.md §五.2）
# 键：日主天干，值：(春, 夏, 秋, 冬) 的调候用神串
TIAOHOU_TABLE = {
    "甲": ("庚金+壬水", "癸水+庚金", "丁火+壬水", "庚金+丁火+戊土"),
    "乙": ("丙火+癸水", "癸水+丙火", "丁火+丙火", "丙火+戊土"),
    "丙": ("壬水", "壬水+庚金", "壬水+戊土", "壬水+甲木"),
    "丁": ("甲木+庚金", "壬水+庚金", "辛亥+甲木", "甲木+庚金"),
    "戊": ("丙火+乙木", "壬水+甲木", "丙火+甲木+癸水", "丙火+甲木"),
    "己": ("丙火+甲木+癸水", "壬水+丙火+甲木", "丙火+甲木+癸水", "丙火+甲木+戊土"),
    "庚": ("壬水+丁火", "壬水+戊土", "丁火+壬水", "丁火+甲木"),
    "辛": ("壬水+乙木", "壬水+庚金", "丁火+壬水", "壬水+戊土+丙火"),
    "壬": ("庚金+丙火", "壬水+辛金", "丁火+甲木", "丙火+甲木+戊土"),
    "癸": ("庚金+辛金", "丙火+庚金", "丁火+甲木+戊土", "丙火+辛金"),
}

# 月支 → 季节
MONTH_TO_SEASON = {
    "寅": "春", "卯": "春", "辰": "春",
    "巳": "夏", "午": "夏", "未": "夏",
    "申": "秋", "酉": "秋", "戌": "秋",
    "亥": "冬", "子": "冬", "丑": "冬",
}

# 日干 → 禄位（用于得地判定）
LU_POS = {
    "甲": "寅", "乙": "卯", "丙": "巳", "丁": "午",
    "戊": "巳", "己": "午", "庚": "申", "辛": "酉",
    "壬": "亥", "癸": "子",
}

# 旺衰分级表（按 bazi-wangshuai.md §三.2）
# 总分 → 等级
WANGSHUAI_GRADE = [
    (4, "极旺（考虑从强）"),
    (3, "旺"),
    (2, "中等"),
    (1, "弱"),
    (0, "极弱（考虑从弱）"),
]


def _wangshuai_check_de_ling(bz: Bazi) -> bool:
    """得令：月支五行 = 日主五行 OR 月支五行生日主."""
    me = GAN_WUXING[bz.day_master]
    month_zhi_wx = ZHI_WUXING[bz.month.zhi]
    return month_zhi_wx == me or SHENG_ME[me] == month_zhi_wx


def _wangshuai_check_de_di(bz: Bazi) -> bool:
    """得地：日支五行 = 日主五行 OR 日支 = 日主禄位."""
    me = GAN_WUXING[bz.day_master]
    day_zhi_wx = ZHI_WUXING[bz.day.zhi]
    if day_zhi_wx == me:
        return True
    return bz.day.zhi == LU_POS[bz.day_master]


def _wangshuai_check_de_sheng(bz: Bazi) -> bool:
    """得生：命中是否有印星（天干透出 OR 地支藏干有根）."""
    me = bz.day_master
    # 检查天干
    for p in [bz.year, bz.month, bz.hour]:
        ss = p.gan_shishen
        if ss in ("正印", "偏印"):
            return True
    # 检查地支（本气）
    for p in [bz.year, bz.month, bz.day, bz.hour]:
        for cg in p.canggan:
            cg_ss = ten_god(me, cg)
            if cg_ss in ("正印", "偏印"):
                return True
    return False


def _wangshuai_check_de_zhu(bz: Bazi) -> bool:
    """得助：命中是否有比劫（天干透出 OR 地支藏干有根）."""
    me = bz.day_master
    for p in [bz.year, bz.month, bz.hour]:
        if p.gan_shishen in ("比肩", "劫财"):
            return True
    for p in [bz.year, bz.month, bz.day, bz.hour]:
        for cg in p.canggan:
            cg_ss = ten_god(me, cg)
            if cg_ss in ("比肩", "劫财"):
                return True
    return False


def wangshuai(bz: Bazi) -> dict:
    """旺衰分析（旺衰四维度 + 调候 + 流通 + 用神精化）.

    返回 dict：
    {
        "wangshuai": str,         # 旺衰等级
        "wangshuai_score": int,   # 4 维度得分
        "de_ling": bool,
        "de_di": bool,
        "de_sheng": bool,
        "de_zhu": bool,
        "tiaohou": str,           # 调候用神
        "liutong": str,           # 流通描述
        "yongshen_jinhua": str,   # 精化用神
        "zhuan_ge": str | None,   # 特殊格局（从强/从弱/化气等）
    }

    算法依据：`references/bazi-wangshuai.md` v1.0.0
    """
    de_ling = _wangshuai_check_de_ling(bz)
    de_di = _wangshuai_check_de_di(bz)
    de_sheng = _wangshuai_check_de_sheng(bz)
    de_zhu = _wangshuai_check_de_zhu(bz)

    score = sum([de_ling, de_di, de_sheng, de_zhu])
    grade = next((g for s, g in WANGSHUAI_GRADE if score >= s), "未知")

    # 调候查表
    season = MONTH_TO_SEASON[bz.month.zhi]
    tiaohou_raw = TIAOHOU_TABLE[bz.day_master]
    season_idx = {"春": 0, "夏": 1, "秋": 2, "冬": 3}[season]
    tiaohou = tiaohou_raw[season_idx]

    # 精化用神（基于旺衰）
    if score >= 3:
        jinhua = "克泄（食伤/财星/官杀）"
    elif score == 2:
        jinhua = "看具体配合（调候优先）"
    elif score == 1:
        jinhua = "生扶（印星/比劫）"
    else:
        jinhua = "财+官杀（从弱格考虑）"

    # 流通分析（简化版）
    liutong_lines = []
    if de_ling and de_di and de_sheng and de_zhu:
        liutong_lines.append("日主极旺（4/4 维度），身极强")
    elif de_ling and de_di:
        liutong_lines.append("月令+日支双重助力")
    elif de_ling and not de_di:
        liutong_lines.append("月令助力但日支不助")

    # 检测印太旺（流通阻滞点 1）
    if bz.month.gan_shishen in ("正印", "偏印"):
        liutong_lines.append(f"月干{bz.month.gan}={bz.month.gan_shishen} → 可能印旺，需财制印")
    if bz.hour.gan_shishen in ("正印", "偏印"):
        liutong_lines.append(f"时干{bz.hour.gan}={bz.hour.gan_shishen} → 印星再助，需调候制化")

    # 检测比劫旺（流通阻滞点 2）
    bijie_count = sum(
        1 for p in [bz.year, bz.month, bz.hour] if p.gan_shishen in ("比肩", "劫财")
    )
    if bijie_count >= 2:
        liutong_lines.append(f"天干比劫{bijie_count}个 → 比劫旺，需官杀制")

    liutong = "；".join(liutong_lines) if liutong_lines else "五行流通平稳"

    # 特殊格局检测（简化）
    zhuan_ge = None
    if score == 4:
        # 检查是否有财官食伤（任一克泄十神）
        has_ke_xie = any(
            p.gan_shishen in ("正官", "七杀", "正财", "偏财", "食神", "伤官")
            for p in [bz.year, bz.month, bz.hour]
        )
        if not has_ke_xie:
            zhuan_ge = "从强格（极旺无比劫印星以外十神）"
    elif score == 0:
        has_yin_bijie = any(
            p.gan_shishen in ("正印", "偏印", "比肩", "劫财")
            for p in [bz.year, bz.month, bz.hour]
        )
        if not has_yin_bijie:
            zhuan_ge = "从弱格（极弱无印星比劫）"

    return {
        "wangshuai": f"{score}/4 {grade}",
        "wangshuai_score": score,
        "de_ling": de_ling,
        "de_di": de_di,
        "de_sheng": de_sheng,
        "de_zhu": de_zhu,
        "tiaohou": tiaohou,
        "liutong": liutong,
        "yongshen_jinhua": jinhua,
        "zhuan_ge": zhuan_ge,
    }


# ============================================================================
# v1.8.0 模块 3：神煞（shensha）—— 28 神煞一体两面
# ============================================================================
#
# 设计依据：`references/bazi-shensha.md` v2.1.1
# 核心问题：命中 28 神煞有哪些？阳面 + 阴面 解读

# 神煞查表（按 bazi-shensha.md §3 速查矩阵）

# A. 贵人星类（按日干）
TIANYI_GUIREN = {
    "甲": ["丑", "未"], "乙": ["子", "申"], "丙": ["亥", "酉"], "丁": ["亥", "酉"],
    "戊": ["丑", "未"], "己": ["子", "申"], "庚": ["丑", "未"], "辛": ["午", "寅"],
    "壬": ["巳", "卯"], "癸": ["巳", "卯"],
}

# v2.2.0 修正：文昌贵人传统派主流为多值版（甲乙→巳午、丙戊→申酉、丁己→亥子、庚辛→寅卯、壬癸→辰戌丑未）
WENCHANG_GUIREN = {
    "甲": ["巳", "午"], "乙": ["巳", "午"],
    "丙": ["申", "酉"], "戊": ["申", "酉"],
    "丁": ["亥", "子"], "己": ["亥", "子"],
    "庚": ["寅", "卯"], "辛": ["寅", "卯"],
    "壬": ["辰", "戌", "丑", "未"], "癸": ["辰", "戌", "丑", "未"],
}

# v2.2.0 修正：太极贵人采用传统派主流版本（壬癸→巳卯、丙丁→亥酉、戊己→寅申、庚辛→寅午）
TAIJI_GUIREN = {
    "甲": ["子", "午"], "乙": ["子", "午"],
    "丙": ["亥", "酉"], "丁": ["亥", "酉"],
    "戊": ["寅", "申"], "己": ["寅", "申"],
    "庚": ["寅", "午"], "辛": ["寅", "午"],
    "壬": ["巳", "卯"], "癸": ["巳", "卯"],
}

GUOYIN_GUIREN = {
    "甲": "戌", "乙": "亥", "丙": "丑", "丁": "寅", "戊": "辰",
    "己": "巳", "庚": "未", "辛": "申", "壬": "午", "癸": "酉",
}

# B. 月支 → 天德 / 月德
TIANDE_GUIREN = {
    "寅": "丁", "午": "丁", "戌": "丁",
    "巳": "癸", "酉": "癸", "丑": "癸",
    "申": "壬", "子": "壬", "辰": "壬",
    "亥": "甲", "卯": "甲", "未": "甲",
}

YUEDE_GUIREN = {
    "寅": "丙", "午": "丙", "戌": "丙",
    "巳": "庚", "酉": "庚", "丑": "庚",
    "申": "壬", "子": "壬", "辰": "壬",
    "亥": "甲", "卯": "甲", "未": "甲",
}

# C. 日支 → 驿马 / 桃花 / 华盖 / 将星 / 亡神 / 劫煞 / 灾煞
# 简化记忆：日支所在三合局
# 申子辰 → 马寅 / 桃酉 / 盖辰 / 将子 / 亡亥 / 劫巳 / 灾午
# 寅午戌 → 马申 / 桃卯 / 盖戌 / 将午 / 亡巳 / 劫亥 / 灾子
# 亥卯未 → 马巳 / 桃子 / 盖未 / 将卯 / 亡申 / 劫寅 / 灾酉
# 巳酉丑 → 马亥 / 桃午 / 盖丑 / 将酉 / 亡寅 / 劫申 / 灾未
YIMA = {"申": "寅", "子": "寅", "辰": "寅",
        "寅": "申", "午": "申", "戌": "申",
        "亥": "巳", "卯": "巳", "未": "巳",
        "巳": "亥", "酉": "亥", "丑": "亥"}

TAOHUA = {"申": "酉", "子": "酉", "辰": "酉",
          "寅": "卯", "午": "卯", "戌": "卯",
          "亥": "子", "卯": "子", "未": "子",
          "巳": "午", "酉": "午", "丑": "午"}

HUAGAI = {"申": "辰", "子": "辰", "辰": "辰",
          "寅": "戌", "午": "戌", "戌": "戌",
          "亥": "未", "卯": "未", "未": "未",
          "巳": "丑", "酉": "丑", "丑": "丑"}

JIANGXING = {"申": "子", "子": "子", "辰": "子",
             "寅": "午", "午": "午", "戌": "午",
             "亥": "卯", "卯": "卯", "未": "卯",
             "巳": "酉", "酉": "酉", "丑": "酉"}

WANGSHEN = {"申": "亥", "子": "亥", "辰": "亥",
            "寅": "巳", "午": "巳", "戌": "巳",
            "亥": "申", "卯": "申", "未": "申",
            "巳": "寅", "酉": "寅", "丑": "寅"}

JIESHA = {"申": "巳", "子": "巳", "辰": "巳",
          "寅": "亥", "午": "亥", "戌": "亥",
          "亥": "寅", "卯": "寅", "未": "寅",
          "巳": "申", "酉": "申", "丑": "申"}

# 传统口诀（《渊海子平/三命通会》口径）：申子辰→午、寅午戌→子、巳酉丑→卯、亥卯未→酉
ZAISHA = {"申": "午", "子": "午", "辰": "午",
          "寅": "子", "午": "子", "戌": "子",
          "巳": "卯", "酉": "卯", "丑": "卯",
          "亥": "酉", "卯": "酉", "未": "酉"}

# D. 年支 → 孤辰 / 寡宿 / 红鸾 / 天喜 / 丧门 / 吊客 / 天罗 / 地网
GUCHEN_GUASU = {
    "寅": ("寅", "辰"), "卯": ("寅", "辰"), "辰": ("寅", "辰"),
    "巳": ("申", "未"), "午": ("申", "未"), "未": ("申", "未"),
    "申": ("亥", "戌"), "酉": ("亥", "戌"), "戌": ("亥", "戌"),
    "亥": ("巳", "子"), "子": ("巳", "子"), "丑": ("巳", "子"),
}

HONGLUAN = {
    "子": "卯", "丑": "寅", "寅": "丑", "卯": "子",
    "辰": "亥", "巳": "戌", "午": "酉", "未": "申",
    "申": "未", "酉": "午", "戌": "巳", "亥": "辰",
}

# 天喜 = 红鸾对冲
def _tianxi(zhi: str) -> str:
    """天喜 = 红鸾对冲."""
    idx = DIZHI.index(zhi)
    return DIZHI[(idx + 6) % 12]


SANGSMEN = {
    "子": "寅", "丑": "卯", "寅": "辰", "卯": "巳",
    "辰": "午", "巳": "未", "午": "申", "未": "酉",
    "申": "戌", "酉": "亥", "戌": "子", "亥": "丑",
}

# 吊客 = 丧门对冲
def _diaoke(zhi: str) -> str:
    """吊客 = 丧门对冲."""
    idx = DIZHI.index(zhi)
    return DIZHI[(idx + 6) % 12]


TIANLUO_DIWANG = {"辰": "天罗", "戌": "天罗", "巳": "地网", "亥": "地网"}

# E. 日干 → 羊刃（禄前一位）
YANGREN = {
    "甲": "卯", "乙": "辰", "丙": "午", "丁": "未",
    "戊": "午", "己": "未", "庚": "酉", "辛": "戌",
    "壬": "子", "癸": "丑",
}

# F. 日柱 → 金神 / 阴阳差错
JINSHEN_DAYS = {"乙丑", "己巳", "癸酉"}

YINYANG_CUOCUO = {
    "丙子", "丁丑", "戊寅", "辛卯", "壬辰", "癸巳",
    "丙午", "丁未", "戊申", "辛酉", "壬戌", "癸亥",
}

# G. 日柱所在旬 → 空亡（按 bazi-shensha.md §3.6）
KONGWANG = {
    "甲子": ["戌", "亥"], "甲戌": ["申", "酉"], "甲申": ["午", "未"],
    "甲午": ["辰", "巳"], "甲辰": ["寅", "卯"], "甲寅": ["子", "丑"],
}

# J. 福星贵人（按日干查，v2.2.0 新增传统派补充）
FUXING_GUIREN = {
    "甲": ["子", "丑"], "乙": ["子", "丑"],
    "丙": ["丑", "寅"], "丁": ["丑", "寅"],
    "戊": ["丑", "未"], "己": ["丑", "未"],
    "庚": ["申", "酉"], "辛": ["申", "酉"],
    "壬": ["辰", "巳"], "癸": ["辰", "巳"],
}

# K. 天厨贵人（按年干查，v2.2.0 新增传统派补充）
TIANCHU_GUIREN = {
    "甲": ["巳", "午"], "乙": ["巳", "午"],
    "丙": ["巳", "午"], "丁": ["巳", "午"],
    "戊": ["申", "酉"], "己": ["申", "酉"],
    "庚": ["亥", "子"], "辛": ["亥", "子"],
    "壬": ["寅", "卯"], "癸": ["寅", "卯"],
}

# L. 德秀贵人（按月支三合局查，v2.2.0 新增传统派补充）
DEXIU_SANHE = {
    "亥": ["亥", "卯", "未"], "卯": ["亥", "卯", "未"], "未": ["亥", "卯", "未"],
    "申": ["申", "子", "辰"], "子": ["申", "子", "辰"], "辰": ["申", "子", "辰"],
    "巳": ["巳", "酉", "丑"], "酉": ["巳", "酉", "丑"], "丑": ["巳", "酉", "丑"],
    "寅": ["寅", "午", "戌"], "午": ["寅", "午", "戌"], "戌": ["寅", "午", "戌"],
}

# M. 披麻（按年支查，v2.2.0 新增传统派补充）
PIMA = {
    "寅": "子", "午": "子", "戌": "子",
    "申": "辰", "子": "辰", "辰": "辰",
    "巳": "酉", "酉": "酉", "丑": "酉",
    "亥": "卯", "卯": "卯", "未": "卯",
}

# N. 飞刃（按日干查，v2.2.0 新增传统派补充）
FEIREN = {
    "甲": "卯", "乙": "辰", "丙": "午",
    "丁": "未", "戊": "午", "己": "未",
    "庚": "酉", "辛": "戌", "壬": "子",
    "癸": "巳",
}

# O. 退神（按日干查日支，v2.2.0 新增传统派补充）
TUISHEN = {
    "甲": "申", "乙": "酉", "丙": "戌", "丁": "亥",
    "戊": "子", "己": "丑", "庚": "寅", "辛": "卯",
    "壬": "辰", "癸": "巳",
}


@lru_cache(maxsize=60)
def _kongwang_for_day(day_gan: str, day_zhi: str) -> tuple | None:
    """v1.13.0 优化（P2-1）：日柱 → 空亡列表的高效查询（lru_cache 避免 60 次循环）.

    返回对应空亡的两支元组，或 None（理论上不会，因为 60 甲子每柱都有对应旬）。
    """
    for xun_gan_zhi, kw in KONGWANG.items():
        xun_gan_idx = TIANGAN.index(xun_gan_zhi[0])
        xun_zhi_idx = DIZHI.index(xun_gan_zhi[1])
        for i in range(10):
            if (TIANGAN[(xun_gan_idx + i) % 10] == day_gan and
                    DIZHI[(xun_zhi_idx + i) % 12] == day_zhi):
                return tuple(kw)
    return None


# H. 月支 + 日柱 → 天赦日
TIANSHE = {
    "寅": "戊寅", "卯": "戊寅", "辰": "戊寅",
    "巳": "甲午", "午": "甲午", "未": "甲午",
    "申": "戊申", "酉": "戊申", "戌": "戊申",
    "亥": "甲子", "子": "甲子", "丑": "甲子",
}

# I. 月支 → 月破日（对冲）
YUEPO = {
    "寅": "申", "卯": "酉", "辰": "戌", "巳": "亥",
    "午": "子", "未": "丑", "申": "寅", "酉": "卯",
    "戌": "辰", "亥": "巳", "子": "午", "丑": "未",
}

# 28 神煞阴阳面（按 bazi-shensha.md §4.0.4 速查表）
SHENSHA_YINYANG = {
    "天乙贵人": ("遇难呈祥、贵人运强", "依赖外力、自力懈怠"),
    "文昌贵人": ("学业聪慧、文书助力", "思虑过度、不务实际"),
    "天德贵人": ("逢凶化吉、上天庇佑", "庇护依赖、不敢担责"),
    "月德贵人": ("长辈提携、灾厄救济", "依赖人和、懈怠自力"),
    "太极贵人": ("聪明好学、哲学天赋", "陷玄思、脱实向虚"),
    "国印贵人": ("掌权有印、行政信誉", "权力执着、形式主义"),
    "桃花": ("异性缘旺、艺术魅力", "烂桃花扰、感情纠葛"),
    "红鸾": ("姻缘速成、婚嫁吉兆", "冲动结合、闪婚闪离"),
    "天喜": ("喜庆连连、人缘和合", "浮于喜乐、不积深度"),
    "驿马": ("迁动得财、出差获利", "奔波劳碌、动中不安"),
    "天马": ("突发转机、被动得益", "突遭变故、身不由己"),
    "华盖": ("才华出众、艺术天赋", "孤僻自闭、不合群"),
    "将星": ("天生权威、统御力强", "孤高难群、独断专行"),
    "金神": ("刚毅果断、杀伐决断", "杀气过重、人缘紧张"),
    "羊刃": ("刚毅果敢、执行力惊人", "刚烈易怒、克配偶 / 血光"),
    "亡神": ("警觉敏锐、能识阴谋", "官非损耗、暗算缠身"),
    "劫煞": ("应激反应强、能脱困", "劫夺破财、意外损伤"),
    "孤辰": ("独立自主、不随波逐流", "婚姻不顺、六亲缘薄"),
    "寡宿": ("独立自主、不随波逐流", "婚姻不顺、六亲缘薄"),
    "灾煞": ("危机意识强、能避祸于先", "突发不顺、意外血光"),
    "丧门": ("珍惜当下、情感有深度", "丧事哀痛、亲缘考验"),
    "吊客": ("哀痛中反思、情感细腻", "伤痛缠绵、难以自拔"),
    "天赦日": ("逢凶化吉、可赦可解", "依赖赦免、规避责任"),
    "月破日": ("破旧立新、敢于颠覆", "所求破败、损耗失败"),
    "阴阳差错": ("独特视角、非主流路径", "婚恋波折、节奏异常"),
    "天罗地网": ("制度保护、约束有度", "束缚限制、牢狱之灾"),
    "六甲空亡": ("真空则灵、超脱执念", "所求落空、福德不实"),
    # v2.2.0 新增传统派补充（6 项）
    "福星贵人": ("享福、有福气", "懒惰、不思进取"),
    "天厨贵人": ("美食缘、有口福", "贪吃、纵欲"),
    "德秀贵人": ("人品好、德行端正", "沽名钓誉、形式主义"),
    "披麻": ("有丧事相关缘", "亲近者有伤病/离世"),
    "退神": ("愿意退让、随缘", "退缩、错失机会"),
    "飞刃": ("魄力十足、执行力强", "脾气暴、容易冲动"),
}


def _shensha_match_zhi(zhi: str, target: str) -> bool:
    """检查地支是否命中 target（单值字符串或串列表）."""
    if isinstance(target, list):
        return zhi in target
    return zhi == target


def _shensha_match_gan(gan: str, target: str) -> bool:
    return gan == target


def shensha(bz: Bazi) -> list:
    """神煞清单（28 神煞 × 4 柱 = 一体两面解读）.

    返回 list[dict]，每个 dict:
    {
        "name": str,
        "yang": str,         # 阳面
        "yin": str,          # 阴面
        "zhiwei": str,       # 位置（如 "日支"、"时干"）
        "activation": str,   # 激活条件
        "control": str,      # 制化机制
    }

    算法依据：`references/bazi-shensha.md` v2.1.1 §3 速查矩阵
    """
    day_master = bz.day_master
    day_zhi = bz.day.zhi
    year_zhi = bz.year.zhi
    month_zhi = bz.month.zhi
    day_pillar_str = bz.day.gan + bz.day.zhi

    results = []

    # ========== A. 贵人星类（按日干） ==========

    # 1. 天乙贵人（按日干查：年支、月支、日支、时支）
    tianyi_zhi = TIANYI_GUIREN[day_master]
    for pos_name, zhi, p in [
        ("年支", bz.year.zhi, bz.year),
        ("月支", bz.month.zhi, bz.month),
        ("日支", bz.day.zhi, bz.day),
        ("时支", bz.hour.zhi, bz.hour),
    ]:
        if zhi in tianyi_zhi:
            yang, yin = SHENSHA_YINYANG["天乙贵人"]
            results.append({
                "name": "天乙贵人",
                "yang": yang,
                "yin": yin,
                "zhiwei": pos_name,
                "activation": "遇急难事时有人出手相助",
                "control": "最忌刑冲（遇冲则贵人失力）",
            })

    # 2. 文昌贵人（按日干查：年干、月干、日干、时干；v2.2.0 改多值版）
    wenchang = WENCHANG_GUIREN[day_master]
    for pos_name, gan, p in [
        ("年干", bz.year.gan, bz.year),
        ("月干", bz.month.gan, bz.month),
        ("日干", bz.day.gan, bz.day),
        ("时干", bz.hour.gan, bz.hour),
    ]:
        if gan in wenchang:
            yang, yin = SHENSHA_YINYANG["文昌贵人"]
            results.append({
                "name": "文昌贵人",
                "yang": yang,
                "yin": yin,
                "zhiwei": pos_name,
                "activation": "流年逢文昌 = 当年考试/学习运佳",
                "control": "无明显制化",
            })
            break

    # 3. 天德贵人（按月支查某天干是否在四柱天干）
    tiande_gan = TIANDE_GUIREN[month_zhi]
    for pos_name, gan, p in [
        ("年干", bz.year.gan, bz.year),
        ("月干", bz.month.gan, bz.month),
        ("时干", bz.hour.gan, bz.hour),
    ]:
        if gan == tiande_gan:
            yang, yin = SHENSHA_YINYANG["天德贵人"]
            results.append({
                "name": "天德贵人",
                "yang": yang,
                "yin": yin,
                "zhiwei": f"{pos_name}（月支{month_zhi}生天德{tiande_gan}）",
                "activation": "逢凶化吉",
                "control": "天德 + 天乙 / 月德 同临则吉力增强",
            })
            break

    # 4. 月德贵人（同上）
    yuede_gan = YUEDE_GUIREN[month_zhi]
    for pos_name, gan, p in [
        ("年干", bz.year.gan, bz.year),
        ("月干", bz.month.gan, bz.month),
        ("时干", bz.hour.gan, bz.hour),
    ]:
        if gan == yuede_gan:
            yang, yin = SHENSHA_YINYANG["月德贵人"]
            results.append({
                "name": "月德贵人",
                "yang": yang,
                "yin": yin,
                "zhiwei": f"{pos_name}（月支{month_zhi}生月德{yuede_gan}）",
                "activation": "长辈/领导提携",
                "control": "月德 + 天德 同临 = 贵格",
            })
            break

    # 5. 太极贵人（按日干查地支）
    taiji_zhi = TAIJI_GUIREN[day_master]
    for pos_name, zhi, p in [
        ("年支", bz.year.zhi, bz.year),
        ("月支", bz.month.zhi, bz.month),
        ("日支", bz.day.zhi, bz.day),
        ("时支", bz.hour.zhi, bz.hour),
    ]:
        if zhi in taiji_zhi:
            yang, yin = SHENSHA_YINYANG["太极贵人"]
            results.append({
                "name": "太极贵人",
                "yang": yang,
                "yin": yin,
                "zhiwei": pos_name,
                "activation": "对哲学/玄学/中医有兴趣或天赋",
                "control": "无明显制化",
            })

    # 6. 国印贵人（按日干查地支）
    guoyin_zhi = GUOYIN_GUIREN[day_master]
    for pos_name, zhi, p in [
        ("年支", bz.year.zhi, bz.year),
        ("月支", bz.month.zhi, bz.month),
        ("日支", bz.day.zhi, bz.day),
        ("时支", bz.hour.zhi, bz.hour),
    ]:
        if zhi == guoyin_zhi:
            yang, yin = SHENSHA_YINYANG["国印贵人"]
            results.append({
                "name": "国印贵人",
                "yang": yang,
                "yin": yin,
                "zhiwei": pos_name,
                "activation": "适合行政管理/执法/签章",
                "control": "国印 + 天乙 同临 = 大贵",
            })

    # ========== B. 桃花 / 红鸾 / 天喜 ==========

    # 7. 桃花（按日支和年支）
    taohua_zhi = TAOHUA[day_zhi]
    for pos_name, zhi, p in [
        ("年支", bz.year.zhi, bz.year),
        ("月支", bz.month.zhi, bz.month),
        ("日支", bz.day.zhi, bz.day),
        ("时支", bz.hour.zhi, bz.hour),
    ]:
        if zhi == taohua_zhi and pos_name != "日支":  # 自坐桃花也算
            yang, yin = SHENSHA_YINYANG["桃花"]
            results.append({
                "name": "桃花",
                "yang": yang,
                "yin": yin,
                "zhiwei": pos_name,
                "activation": "未婚 = 异性缘广；婚内 = 外缘重",
                "control": "桃花逢合 = 情定一人；逢冲 = 情感动荡",
            })
    # 自坐桃花特殊标记
    if day_zhi == taohua_zhi:
        yang, yin = SHENSHA_YINYANG["桃花"]
        results.append({
            "name": "桃花",
            "yang": yang,
            "yin": yin,
            "zhiwei": "日支（自坐桃花）",
            "activation": "配偶本身有桃花特质",
            "control": "桃花逢合 = 情定一人；逢冲 = 情感动荡",
        })

    # 8. 红鸾（按年支）
    hongluan_zhi = HONGLUAN[year_zhi]
    for pos_name, zhi, p in [
        ("年支", bz.year.zhi, bz.year),
        ("月支", bz.month.zhi, bz.month),
        ("日支", bz.day.zhi, bz.day),
        ("时支", bz.hour.zhi, bz.hour),
    ]:
        if zhi == hongluan_zhi and pos_name != "年支":
            yang, yin = SHENSHA_YINYANG["红鸾"]
            results.append({
                "name": "红鸾",
                "yang": yang,
                "yin": yin,
                "zhiwei": pos_name,
                "activation": "流年逢红鸾 = 当年有婚恋运",
                "control": "红鸾 + 天喜 同临 = 大喜",
            })

    # 9. 天喜（同上）
    tianxi_zhi = _tianxi(year_zhi)
    for pos_name, zhi, p in [
        ("年支", bz.year.zhi, bz.year),
        ("月支", bz.month.zhi, bz.month),
        ("日支", bz.day.zhi, bz.day),
        ("时支", bz.hour.zhi, bz.hour),
    ]:
        if zhi == tianxi_zhi and pos_name != "年支":
            yang, yin = SHENSHA_YINYANG["天喜"]
            results.append({
                "name": "天喜",
                "yang": yang,
                "yin": yin,
                "zhiwei": pos_name,
                "activation": "当年多喜事（升迁/添丁/结婚/获奖）",
                "control": "无明显制化",
            })

    # ========== C. 驿马 / 天马 ==========

    # 10. 驿马（按日支和年支）
    yima_zhi = YIMA[day_zhi]
    for pos_name, zhi, p in [
        ("年支", bz.year.zhi, bz.year),
        ("月支", bz.month.zhi, bz.month),
        ("日支", bz.day.zhi, bz.day),
        ("时支", bz.hour.zhi, bz.hour),
    ]:
        if zhi == yima_zhi and pos_name != "日支":
            yang, yin = SHENSHA_YINYANG["驿马"]
            results.append({
                "name": "驿马",
                "yang": yang,
                "yin": yin,
                "zhiwei": pos_name,
                "activation": "出差/迁居/出国/工作调动",
                "control": "驿马逢冲 = 奔波不安；逢合 = 动中有定",
            })

    # 11. 天马（按年支所在三合局对冲）
    tianma_zhi = YIMA[year_zhi]  # 与驿马同位（按 bazi-shensha.md §2.C.2）
    for pos_name, zhi, p in [
        ("年支", bz.year.zhi, bz.year),
        ("月支", bz.month.zhi, bz.month),
        ("日支", bz.day.zhi, bz.day),
        ("时支", bz.hour.zhi, bz.hour),
    ]:
        if zhi == tianma_zhi and pos_name != "年支":
            yang, yin = SHENSHA_YINYANG["天马"]
            results.append({
                "name": "天马",
                "yang": yang,
                "yin": yin,
                "zhiwei": pos_name,
                "activation": "突发性迁动/调动",
                "control": "天马与驿马同临 = 终身多动",
            })

    # ========== D. 才华将星类 ==========

    # 12. 华盖（按日支）
    huagai_zhi = HUAGAI[day_zhi]
    for pos_name, zhi, p in [
        ("年支", bz.year.zhi, bz.year),
        ("月支", bz.month.zhi, bz.month),
        ("日支", bz.day.zhi, bz.day),
        ("时支", bz.hour.zhi, bz.hour),
    ]:
        if zhi == huagai_zhi and pos_name != "日支":
            yang, yin = SHENSHA_YINYANG["华盖"]
            results.append({
                "name": "华盖",
                "yang": yang,
                "yin": yin,
                "zhiwei": pos_name,
                "activation": "适合钻研学问/艺术/宗教哲学",
                "control": "华盖逢冲 = 才华外露；逢合 = 收敛内敛",
            })

    # 13. 将星（按日支）
    jiangxing_zhi = JIANGXING[day_zhi]
    for pos_name, zhi, p in [
        ("年支", bz.year.zhi, bz.year),
        ("月支", bz.month.zhi, bz.month),
        ("日支", bz.day.zhi, bz.day),
        ("时支", bz.hour.zhi, bz.hour),
    ]:
        if zhi == jiangxing_zhi and pos_name != "日支":
            yang, yin = SHENSHA_YINYANG["将星"]
            results.append({
                "name": "将星",
                "yang": yang,
                "yin": yin,
                "zhiwei": pos_name,
                "activation": "适合做管理/当领导",
                "control": "将星 + 天乙 同临 = 贵上加贵",
            })

    # 14. 金神（按日柱）
    if day_pillar_str in JINSHEN_DAYS:
        yang, yin = SHENSHA_YINYANG["金神"]
        results.append({
            "name": "金神",
            "yang": yang,
            "yin": yin,
            "zhiwei": "日柱（入命）",
            "activation": "夏季金神力量最强；冬季最弱",
            "control": "金神遇火 = 大贵；遇水 = 大凶",
        })

    # ========== E. 羊刃刚强类 ==========

    # 15. 羊刃（按日干查地支）
    yangren_zhi = YANGREN[day_master]
    for pos_name, zhi, p in [
        ("年支", bz.year.zhi, bz.year),
        ("月支", bz.month.zhi, bz.month),
        ("日支", bz.day.zhi, bz.day),
        ("时支", bz.hour.zhi, bz.hour),
    ]:
        if zhi == yangren_zhi:
            yang, yin = SHENSHA_YINYANG["羊刃"]
            results.append({
                "name": "羊刃",
                "yang": yang,
                "yin": yin,
                "zhiwei": pos_name,
                "activation": "身旺 = 大贵（武将/开拓）；身弱 = 大凶",
                "control": "食神（己土）制刃最佳；羊刃逢冲 = 倒戈",
            })

    # ========== F. 凶煞破败类 ==========

    # 16. 亡神
    wangshen_zhi = WANGSHEN[day_zhi]
    for pos_name, zhi, p in [
        ("年支", bz.year.zhi, bz.year),
        ("月支", bz.month.zhi, bz.month),
        ("日支", bz.day.zhi, bz.day),
        ("时支", bz.hour.zhi, bz.hour),
    ]:
        if zhi == wangshen_zhi and pos_name != "日支":
            yang, yin = SHENSHA_YINYANG["亡神"]
            results.append({
                "name": "亡神",
                "yang": yang,
                "yin": yin,
                "zhiwei": pos_name,
                "activation": "易遭意外破财/官非诉讼/阴谋暗算",
                "control": "亡神 + 吉星同临 = 凶力减弱",
            })

    # 17. 劫煞
    jiesha_zhi = JIESHA[day_zhi]
    for pos_name, zhi, p in [
        ("年支", bz.year.zhi, bz.year),
        ("月支", bz.month.zhi, bz.month),
        ("日支", bz.day.zhi, bz.day),
        ("时支", bz.hour.zhi, bz.hour),
    ]:
        if zhi == jiesha_zhi and pos_name != "日支":
            yang, yin = SHENSHA_YINYANG["劫煞"]
            results.append({
                "name": "劫煞",
                "yang": yang,
                "yin": yin,
                "zhiwei": pos_name,
                "activation": "易遭抢劫/诈骗/意外破财",
                "control": "劫煞 + 羊刃同临 = 大凶；逢合 = 凶力减弱",
            })

    # 18. 孤辰寡宿（按年支）
    guchen, guasu = GUCHEN_GUASU[year_zhi]
    for pos_name, zhi, p in [
        ("年支", bz.year.zhi, bz.year),
        ("月支", bz.month.zhi, bz.month),
        ("日支", bz.day.zhi, bz.day),
        ("时支", bz.hour.zhi, bz.hour),
    ]:
        if zhi == guchen and pos_name != "年支":
            yang, yin = SHENSHA_YINYANG["孤辰"]
            results.append({
                "name": "孤辰",
                "yang": yang,
                "yin": yin,
                "zhiwei": pos_name,
                "activation": "易晚婚/配偶缘薄",
                "control": "无明显制化",
            })
        if zhi == guasu and pos_name != "年支":
            yang, yin = SHENSHA_YINYANG["寡宿"]
            results.append({
                "name": "寡宿",
                "yang": yang,
                "yin": yin,
                "zhiwei": pos_name,
                "activation": "婚姻风险较高",
                "control": "无明显制化",
            })

    # 19. 灾煞
    zaisha_zhi = ZAISHA[day_zhi]
    for pos_name, zhi, p in [
        ("年支", bz.year.zhi, bz.year),
        ("月支", bz.month.zhi, bz.month),
        ("日支", bz.day.zhi, bz.day),
        ("时支", bz.hour.zhi, bz.hour),
    ]:
        if zhi == zaisha_zhi and pos_name != "日支":
            yang, yin = SHENSHA_YINYANG["灾煞"]
            results.append({
                "name": "灾煞",
                "yang": yang,
                "yin": yin,
                "zhiwei": pos_name,
                "activation": "易遭水火之灾/跌打损伤/突发意外",
                "control": "灾煞 + 天乙/天德 = 凶力大减",
            })

    # 20. 丧门（按年支）
    sangmen_zhi = SANGSMEN[year_zhi]
    for pos_name, zhi, p in [
        ("年支", bz.year.zhi, bz.year),
        ("月支", bz.month.zhi, bz.month),
        ("日支", bz.day.zhi, bz.day),
        ("时支", bz.hour.zhi, bz.hour),
    ]:
        if zhi == sangmen_zhi and pos_name != "年支":
            yang, yin = SHENSHA_YINYANG["丧门"]
            results.append({
                "name": "丧门",
                "yang": yang,
                "yin": yin,
                "zhiwei": pos_name,
                "activation": "当年易有丧事（亲人离世/伤病）",
                "control": "丧门 + 吊客同临 = 凶力加倍",
            })

    # 21. 吊客
    diaoke_zhi = _diaoke(year_zhi)
    for pos_name, zhi, p in [
        ("年支", bz.year.zhi, bz.year),
        ("月支", bz.month.zhi, bz.month),
        ("日支", bz.day.zhi, bz.day),
        ("时支", bz.hour.zhi, bz.hour),
    ]:
        if zhi == diaoke_zhi and pos_name != "年支":
            yang, yin = SHENSHA_YINYANG["吊客"]
            results.append({
                "name": "吊客",
                "yang": yang,
                "yin": yin,
                "zhiwei": pos_name,
                "activation": "主哀痛/伤痛",
                "control": "吊客 + 丧门同临 = 大凶",
            })

    # ========== G. 特殊日类 ==========

    # 22. 天赦日（按月支 + 日柱）
    tianshe_day = TIANSHE[month_zhi]
    if day_pillar_str == tianshe_day:
        yang, yin = SHENSHA_YINYANG["天赦日"]
        results.append({
            "name": "天赦日",
            "yang": yang,
            "yin": yin,
            "zhiwei": "日柱（入命）",
            "activation": "当日/命主逢凶化吉",
            "control": "无明显制化",
        })

    # 23. 月破日（按月支查日支是否对冲）
    yuepo_zhi = YUEPO[month_zhi]
    if day_zhi == yuepo_zhi:
        yang, yin = SHENSHA_YINYANG["月破日"]
        results.append({
            "name": "月破日",
            "yang": yang,
            "yin": yin,
            "zhiwei": "日支（与月支对冲）",
            "activation": "所求之事易破败/损耗",
            "control": "无明显制化",
        })

    # 24. 阴阳差错日（按日柱）
    if day_pillar_str in YINYANG_CUOCUO:
        yang, yin = SHENSHA_YINYANG["阴阳差错"]
        results.append({
            "name": "阴阳差错",
            "yang": yang,
            "yin": yin,
            "zhiwei": "日柱（入命）",
            "activation": "婚姻多波折/易有感情纠纷",
            "control": "男命带 = 妻缘浅；女命带 = 夫缘浅",
        })

    # ========== H. 杂煞类 ==========

    # 25. 天罗地网（按年支 → 辰戌天罗，巳亥地网）
    for pos_name, zhi, p in [
        ("年支", bz.year.zhi, bz.year),
        ("月支", bz.month.zhi, bz.month),
        ("日支", bz.day.zhi, bz.day),
        ("时支", bz.hour.zhi, bz.hour),
    ]:
        if zhi in TIANLUO_DIWANG:
            kind = TIANLUO_DIWANG[zhi]
            yang, yin = SHENSHA_YINYANG["天罗地网"]
            results.append({
                "name": f"{kind}",
                "yang": yang,
                "yin": yin,
                "zhiwei": pos_name,
                "activation": f"命带{kind}",
                "control": "天罗 + 地网同临 = 牢狱/重大约束",
            })

    # 26. 六甲空亡（按日柱所在旬：6 旬首 → 每旬空亡两支，统一走旬遍历）
    # v1.13.0 优化（P2-1）：用 lru_cache 包裹日柱→空亡查询，避免重复 60 次循环
    kongwang_zhi = _kongwang_for_day(bz.day.gan, bz.day.zhi)

    if kongwang_zhi:
        for pos_name, zhi, p in [
            ("年支", bz.year.zhi, bz.year),
            ("月支", bz.month.zhi, bz.month),
            ("日支", bz.day.zhi, bz.day),
            ("时支", bz.hour.zhi, bz.hour),
        ]:
            if zhi in kongwang_zhi:
                yang, yin = SHENSHA_YINYANG["六甲空亡"]
                results.append({
                    "name": "六甲空亡",
                    "yang": yang,
                    "yin": yin,
                    "zhiwei": pos_name,
                    "activation": "所求之事易落空",
                    "control": "空亡逢冲 = 填实，反而有好事",
                })

    # ========== I. 传统派补充神煞（v2.2.0 新增 6 项） ==========

    # 27. 福星贵人（按日干查）
    fuxing_zhi = FUXING_GUIREN[day_master]
    for pos_name, zhi, p in [
        ("年支", bz.year.zhi, bz.year),
        ("月支", bz.month.zhi, bz.month),
        ("日支", bz.day.zhi, bz.day),
        ("时支", bz.hour.zhi, bz.hour),
    ]:
        if zhi in fuxing_zhi:
            yang, yin = SHENSHA_YINYANG["福星贵人"]
            results.append({
                "name": "福星贵人",
                "yang": yang,
                "yin": yin,
                "zhiwei": pos_name,
                "activation": "享福、有福气，遇事多逢吉人",
                "control": "无明显制化",
            })

    # 28. 天厨贵人（按年干查）
    tianchu_zhi = TIANCHU_GUIREN[bz.year.gan]
    for pos_name, zhi, p in [
        ("年支", bz.year.zhi, bz.year),
        ("月支", bz.month.zhi, bz.month),
        ("日支", bz.day.zhi, bz.day),
        ("时支", bz.hour.zhi, bz.hour),
    ]:
        if zhi in tianchu_zhi:
            yang, yin = SHENSHA_YINYANG["天厨贵人"]
            results.append({
                "name": "天厨贵人",
                "yang": yang,
                "yin": yin,
                "zhiwei": pos_name,
                "activation": "美食缘、有口福",
                "control": "无明显制化",
            })

    # 29. 德秀贵人（按月支三合局查）
    dexiu_zhi_list = DEXIU_SANHE[month_zhi]
    for pos_name, zhi, p in [
        ("年支", bz.year.zhi, bz.year),
        ("月支", bz.month.zhi, bz.month),
        ("日支", bz.day.zhi, bz.day),
        ("时支", bz.hour.zhi, bz.hour),
    ]:
        if zhi in dexiu_zhi_list:
            yang, yin = SHENSHA_YINYANG["德秀贵人"]
            results.append({
                "name": "德秀贵人",
                "yang": yang,
                "yin": yin,
                "zhiwei": pos_name,
                "activation": "品德高尚、人缘好",
                "control": "无明显制化",
            })

    # 30. 披麻（按年支查）
    pima_zhi = PIMA[year_zhi]
    for pos_name, zhi, p in [
        ("年支", bz.year.zhi, bz.year),
        ("月支", bz.month.zhi, bz.month),
        ("日支", bz.day.zhi, bz.day),
        ("时支", bz.hour.zhi, bz.hour),
    ]:
        if zhi == pima_zhi and pos_name != "年支":
            yang, yin = SHENSHA_YINYANG["披麻"]
            results.append({
                "name": "披麻",
                "yang": yang,
                "yin": yin,
                "zhiwei": pos_name,
                "activation": "亲近者有伤病/离世",
                "control": "披麻 + 丧门/吊客同临 = 凶力加倍",
            })

    # 31. 飞刃（按日干查）
    feiren_zhi = FEIREN[day_master]
    for pos_name, zhi, p in [
        ("年支", bz.year.zhi, bz.year),
        ("月支", bz.month.zhi, bz.month),
        ("日支", bz.day.zhi, bz.day),
        ("时支", bz.hour.zhi, bz.hour),
    ]:
        if zhi == feiren_zhi and pos_name != "年支":
            yang, yin = SHENSHA_YINYANG["飞刃"]
            results.append({
                "name": "飞刃",
                "yang": yang,
                "yin": yin,
                "zhiwei": pos_name,
                "activation": "魄力十足、执行力强",
                "control": "飞刃 + 羊刃同临 = 大凶",
            })

    # 32. 退神（按日干查日支）
    tuishen_zhi = TUISHEN[day_master]
    for pos_name, zhi, p in [
        ("年支", bz.year.zhi, bz.year),
        ("月支", bz.month.zhi, bz.month),
        ("日支", bz.day.zhi, bz.day),
        ("时支", bz.hour.zhi, bz.hour),
    ]:
        if zhi == tuishen_zhi:
            yang, yin = SHENSHA_YINYANG["退神"]
            results.append({
                "name": "退神",
                "yang": yang,
                "yin": yin,
                "zhiwei": pos_name,
                "activation": "愿意退让、随缘",
                "control": "无明显制化",
            })

    return results


# ============================================================================
# v1.8.0 模块 4：用神（yongshen）—— 正格 ∩ 旺衰 融合
# ============================================================================
#
# 设计依据：`references/bazi-yongshen.md` v1.0.0
# 核心问题：融合正格方向 + 旺衰精化 → 最终用神
# ⚠️ 神煞不进入用神判定（神煞 = 28 神星；用神 = 十神五行）

# 用神五行映射（按十神 → 五行）
# 用于把十神喜忌总则转换成五行方向
SHISHEN_WUXING = {
    "比肩": {"阳": "木", "阴": "木"} | {"丙": "火", "丁": "火"},  # placeholder
}


# 直接定义：每个日主 → 用神方向（基于 zhengge）
# 避免复杂查询，这里按"用神方向"中文描述 → 五行串
YONGSHEN_WUXING_MAP = {
    # 正官格
    "财星": "金水木",  # 我克
    "食神": "火土",  # 我生
    "印星": "木水",  # 生我
    "官杀": "金水",
    "官星": "金水",
    "比劫": "同我",
    # 七杀格
    # 食神制杀
    # 偏财格
    "食伤": "火土",
    # 通用
    "财+官": "金水",
}


def _yongshen_resolve_wuxing(zhengge_out: dict, wangshuai_out: dict, bz: Bazi) -> str:
    """解析最终用神五行（融合正格 + 旺衰）.

    三层模型：
    - L1（正格）：方向 → 五行
    - L2（旺衰）：精化 → 五行
    - L3（融合）：最终 → 五行

    优先级：正格方向 > 调候 > 扶抑（神煞不进入用神判定）
    """
    # 正格方向（最高优先级）
    zg_dir = zhengge_out.get("yongshen_wuxing", "")
    if not zg_dir or "（走旺衰精化）" in zg_dir:
        zg_dir = ""

    # 调候五行（旺衰精化）
    tiaohou = wangshuai_out.get("tiaohou", "")
    tiaohou_wuxing = []
    if "庚" in tiaohou or "辛" in tiaohou:
        tiaohou_wuxing.append("金")
    if "壬" in tiaohou or "癸" in tiaohou:
        tiaohou_wuxing.append("水")
    if "甲" in tiaohou or "乙" in tiaohou:
        tiaohou_wuxing.append("木")
    if "丙" in tiaohou or "丁" in tiaohou:
        tiaohou_wuxing.append("火")
    if "戊" in tiaohou or "己" in tiaohou:
        tiaohou_wuxing.append("土")

    # 旺衰精化方向
    score = wangshuai_out.get("wangshuai_score", 2)
    if score >= 3:
        fuyi_wuxing = "金水"  # 身旺 → 克泄（金水为主）
    elif score <= 1:
        fuyi_wuxing = "木火"  # 身弱 → 生扶
    else:
        fuyi_wuxing = ""

    # 融合优先级：正格方向 > 调候 > 扶抑
    final = []
    for wx in zg_dir:
        if wx not in final:
            final.append(wx)
    for wx in tiaohou_wuxing:
        if wx not in final:
            final.append(wx)
    for wx in fuyi_wuxing:
        if wx not in final:
            final.append(wx)

    return "".join(final) if final else "（待人工判定）"


def yongshen(bz: Bazi) -> dict:
    """用神融合（正格方向 ∩ 旺衰精化）.

    返回 dict：
    {
        "final": str,            # 最终用神（五行串）
        "final_desc": str,       # 一句话总结
        "xiangshen": str,        # 相神
        "jishen": str,           # 忌神
        "choushen": str,         # 仇神
        "zhengge_direction": str,    # 正格方向
        "wangshuai_jinhua": str,     # 旺衰精化
        "tiaohou": str,          # 调候
        "fusion_source": str,    # 融合来源说明
        "wangshuai_score": int,  # 旺衰得分
    }

    算法依据：`references/bazi-yongshen.md` v1.0.0
    ⚠️ 神煞不进入用神判定（神煞 = 28 神星；用神 = 十神五行）
    """
    # 取正格和旺衰
    zg_out = zhengge(bz)
    sj_out = wangshuai(bz)

    # 融合最终五行
    final_wuxing = _yongshen_resolve_wuxing(zg_out, sj_out, bz)

    # 提取相神 / 忌神 / 仇神（从正格取）
    xiangshen = zg_out.get("xiangshen", "")
    jishen = zg_out.get("jishen", "")
    choushen = zg_out.get("choushen", "")

    # 一句话最终用神
    tiaohou = sj_out.get("tiaohou", "")
    if tiaohou and final_wuxing:
        final_desc = f"{final_wuxing}（{tiaohou}为调候核，{zg_out.get('ge_type', '用神')}为体）"
    else:
        final_desc = final_wuxing or "（待人工判定）"

    # 融合来源说明
    ge_type = zg_out.get("ge_type", "（无格）")
    fusion_source = (
        f"正格（{ge_type} → {zg_out.get('yongshen_direction', '未知')}）∩ "
        f"旺衰（{sj_out.get('yongshen_jinhua', '未知')}，调候={tiaohou or '无'}）"
    )

    return {
        "final": final_wuxing,
        "final_desc": final_desc,
        "xiangshen": xiangshen,
        "jishen": jishen,
        "choushen": choushen,
        "zhengge_direction": zg_out.get("yongshen_direction", ""),
        "wangshuai_jinhua": sj_out.get("yongshen_jinhua", ""),
        "tiaohou": tiaohou,
        "fusion_source": fusion_source,
        "wangshuai_score": sj_out.get("wangshuai_score", 0),
    }


# ============================================================================
# v1.8.0 模块 5：大运（dayun）—— 顺/逆排 + 起运岁数 + 10 步大运
# ============================================================================
#
# 设计依据：传统子平术 + 老板 2026-08-10 17:31 拍板
# 核心规则：
# 1. 阳男 / 阴女 → 顺排
# 2. 阴男 / 阳女 → 逆排
# 3. 阳年干 = 甲丙戊庚壬；阴年干 = 乙丁己辛癸
# 4. 起运岁数 = 出生日 → 下一个节（顺排）/ 上一个节（逆排）的天数 ÷ 3
# 5. 10 步大运：顺排 = 从月柱下一个干支开始；逆排 = 从月柱上一个干支开始

# 24 节气表（公历近似日期，用于起运计算）
# 实际应使用 cnlunar 的近似时间（cnlunar 返回 (month, day) tuple）
# 来源：references/bazi-rules.md §三 节气切月
# 注意：子平术只用"节"（每月的第一个节气），不用"气"（第二个）
# 节列表（按时间顺序）：
JIE_NAMES = [
    "小寒",   # 丑月起点
    "立春",   # 寅月起点
    "惊蛰",   # 卯月起点
    "清明",   # 辰月起点
    "立夏",   # 巳月起点
    "芒种",   # 午月起点
    "小暑",   # 未月起点
    "立秋",   # 申月起点
    "白露",   # 酉月起点
    "寒露",   # 戌月起点
    "立冬",   # 亥月起点
    "大雪",   # 子月起点
]

# 节对应的月支
JIE_TO_ZHI = {
    "小寒": "丑", "立春": "寅", "惊蛰": "卯", "清明": "辰",
    "立夏": "巳", "芒种": "午", "小暑": "未", "立秋": "申",
    "白露": "酉", "寒露": "戌", "立冬": "亥", "大雪": "子",
}


def _get_jieqi_datetime(year: int, jieqi_name: str) -> "datetime | None":
    """获取指定年份某个节气的近似 datetime（用 cnlunar 节气表）.

    cnlunar 节气返回 (month, day) tuple（精度 ±1 天），
    本函数默认 12:00 作为节气当日时间点。
    """
    try:
        # cnlunar.getSolarTermsDateList 是 instance method
        # 通过 Lunar 对象调用
        ref_dt = datetime(year, 6, 15, 12, 0)
        l = cnlunar.Lunar(ref_dt)
        terms_dict = l.thisYearSolarTermsDic
        if jieqi_name in terms_dict:
            m, d = terms_dict[jieqi_name]
            return datetime(year, m, d, 12, 0)
    except Exception:
        pass
    return None


def _find_nearest_jie(bz: Bazi, direction: str) -> tuple:
    """找最近的节（direction='forward' 或 'backward'）.

    返回 (jie_name, jie_datetime, days_diff).
    """
    birth = bz.solar
    month_zhi = bz.month.zhi

    if direction == "forward":
        # 找出生日之后的下一个节（**不在月内的节**）
        # 先在当年找，然后下一年
        for year in [birth.year, birth.year + 1]:
            for jq_name in JIE_NAMES:
                # 跳过本月起点（这个节前在月外，下一个节才是真正的下一个）
                if JIE_TO_ZHI[jq_name] == month_zhi:
                    continue
                jt = _get_jieqi_datetime(year, jq_name)
                if jt and jt > birth:
                    return (jq_name, jt, (jt - birth).days)
        return (None, None, 0)
    else:
        # 找出生日之前的上一个节（逆排：上一个节恰恰就是本月起点节，不能跳过）
        for year in [birth.year, birth.year - 1]:
            for jq_name in reversed(JIE_NAMES):
                jt = _get_jieqi_datetime(year, jq_name)
                if jt and jt < birth:
                    return (jq_name, jt, (birth - jt).days)
        return (None, None, 0)


def _next_gan_zhi(gan: str, zhi: str, forward: bool = True) -> tuple:
    """在 60 甲子表中找下一个（或上一个）干支."""
    gan_idx = TIANGAN.index(gan)
    zhi_idx = DIZHI.index(zhi)
    if forward:
        new_gan = TIANGAN[(gan_idx + 1) % 10]
        new_zhi = DIZHI[(zhi_idx + 1) % 12]
    else:
        new_gan = TIANGAN[(gan_idx - 1) % 10]
        new_zhi = DIZHI[(zhi_idx - 1) % 12]
    return (new_gan, new_zhi)


def dayun(bz: Bazi, gender: str = "男") -> dict:
    """大运推算（顺/逆排 + 起运岁数 + 10 步大运）.

    参数：
    - bz: Bazi 对象
    - gender: '男' 或 '女'

    返回 dict：
    {
        "shunni": str,                # '顺排' 或 '逆排'
        "qi_yun_age": int,            # 起运岁数
        "qi_yun_jie": str,            # 所对节
        "qi_yun_note": str,           # 起运计算说明
        "steps": [
            {
                "index": int,
                "gan": str,
                "zhi": str,
                "gan_shishen": str,
                "zhi_shishen": str,
                "start_age": int,
                "end_age": int,
            }
        ]
    }

    算法依据：传统子平术
    """
    year_gan = bz.year.gan
    is_yang_year = YIN_YANG[TIANGAN.index(year_gan)] == "阳"
    is_male = (gender == "男") or (gender == "male") or (gender == "M")

    # 顺/逆判定
    if (is_yang_year and is_male) or (not is_yang_year and not is_male):
        shunni = "顺排"
        forward = True
    else:
        shunni = "逆排"
        forward = False

    # 起运岁数
    direction = "forward" if forward else "backward"
    if bz.solar is not None:
        jie_name, jie_dt, days_diff = _find_nearest_jie(bz, direction)
        # v1.13.0 优化（P2-2）：折叠余数折算（1 天≈4 个月 → 1%3=0 余 1 天 折 4 个月）
        # qi_yun_age 保持 int（向下游 step_start 计算兼容），加 qi_yun_age_detail 字符串显示
        qi_yun_years = days_diff // 3
        qi_yun_months = (days_diff % 3) * 4
        qi_yun_age = qi_yun_years  # 保持 int（与下游代码兼容）
        if qi_yun_months > 0:
            qi_yun_age_detail = f"{qi_yun_years}岁{qi_yun_months}个月"
        else:
            qi_yun_age_detail = f"{qi_yun_years}岁"
        qi_yun_note = (
            f"出生日 → {'下一个' if forward else '上一个'}节"
            f"{jie_name or '（未找到）'} 的天数{days_diff} → {qi_yun_age_detail} 起运"
        )
        # 简化口径：起运岁数按 3 天=1 岁取整（1 天≈4 个月、1 时辰≈10 天）
        qi_yun_rule = "起运岁数按 3 天=1 岁取整 + 余数折月（1 天≈4 个月、1 时辰≈10 天）"
    else:
        # 四柱直接输入：无公历日期，无法精确起运（干支大运仍可排）
        jie_name, qi_yun_age = "", None
        qi_yun_note = "四柱输入无公历日期，起运岁数未知（可用 --reverse 反查日期）"
        qi_yun_rule = ""

    # 10 步大运（从月柱顺/逆推）
    month_gan = bz.month.gan
    month_zhi = bz.month.zhi
    cur_gan, cur_zhi = month_gan, month_zhi
    # 第一步大运从月柱的下一（或上一）个开始
    cur_gan, cur_zhi = _next_gan_zhi(cur_gan, cur_zhi, forward=forward)

    steps = []
    for i in range(10):
        if qi_yun_age is not None:
            step_start = qi_yun_age + i * 10
            step_end = step_start + 9
        else:
            step_start, step_end = None, None
        steps.append({
            "index": i + 1,
            "gan": cur_gan,
            "zhi": cur_zhi,
            "gan_shishen": ten_god(bz.day_master, cur_gan),
            "zhi_shishen": ten_god_of_zhi(bz.day_master, cur_zhi),
            "start_age": step_start,
            "end_age": step_end,
        })
        cur_gan, cur_zhi = _next_gan_zhi(cur_gan, cur_zhi, forward=forward)

    return {
        "shunni": shunni,
        "qi_yun_age": qi_yun_age,
        "qi_yun_jie": jie_name or "",
        "qi_yun_note": qi_yun_note,
        "qi_yun_rule": qi_yun_rule,
        "steps": steps,
    }


# ============================================================================
# v1.8.0 模块 6：八字反查（reverse_lookup）—— 60 甲子反推
# ============================================================================
#
# 设计依据：传统 60 甲子循环 + cnlunar
# 核心算法：
# 1. 给定 4 柱（年/月/日/时），反查候选公历日期
# 2. 用 cnlunar 验证每个候选（注意 ±1 天节气误差）

# 60 甲子表（用于反查年份循环）
JIAZI_60 = [
    "甲子", "乙丑", "丙寅", "丁卯", "戊辰", "己巳", "庚午", "辛未", "壬申", "癸酉",
    "甲戌", "乙亥", "丙子", "丁丑", "戊寅", "己卯", "庚辰", "辛巳", "壬午", "癸未",
    "甲申", "乙酉", "丙戌", "丁亥", "戊子", "己丑", "庚寅", "辛卯", "壬辰", "癸巳",
    "甲午", "乙未", "丙申", "丁酉", "戊戌", "己亥", "庚子", "辛丑", "壬寅", "癸卯",
    "甲辰", "乙巳", "丙午", "丁未", "戊申", "己酉", "庚戌", "辛亥", "壬子", "癸丑",
    "甲寅", "乙卯", "丙辰", "丁巳", "戊午", "己未", "庚申", "辛酉", "壬戌", "癸亥",
]


def reverse_lookup(year_gz: str, month_gz: str, day_gz: str, hour_gz: str,
                   year_range: tuple = (1900, 2100)) -> list:
    """八字反查 —— 给定 4 柱，反查候选公历日期.

    参数：
    - year_gz: 年柱（甲子）
    - month_gz: 月柱
    - day_gz: 日柱
    - hour_gz: 时柱
    - year_range: 搜索年份范围（默认 1900-2100）

    返回 list[dict]，每个候选：
    {
        "solar": "YYYY-MM-DD",
        "lunar": "...",
        "shengxiao": "...",
        "year_pillar": "...",
        "month_pillar": "...",
        "day_pillar": "...",
        "hour_pillar": "...",
        "jieqi_match": str,        # 节气匹配说明
        "cnlunar_precision": str,  # cnlunar 精度说明
        "candidate_rank": int,     # 候选排名
        "score": float,            # 匹配置信度
    }

    限制：cnlunar 节气精度 ±1 天，反查为候选范围而非唯一日期。
    """
    candidates = []

    if year_gz not in JIAZI_60 or day_gz not in JIAZI_60:
        return [{
            "error": "输入的干支不在 60 甲子表内",
            "year_pillar": year_gz,
            "month_pillar": month_gz,
            "day_pillar": day_gz,
            "hour_pillar": hour_gz,
            "notes": "请检查输入是否正确",
        }]

    year_start, year_end = year_range

    # 60 甲子索引
    target_year_idx = JIAZI_60.index(year_gz)
    target_day_idx = JIAZI_60.index(day_gz)

    # Step 1: 找出候选年份（按 60 甲子循环）
    # 由于 cnlunar 用 立春 换年，年份判定时取 (year, 6, 1) 作为参考点（年中无歧义）
    candidate_years = []
    for y in range(year_start, year_end + 1):
        try:
            l = cnlunar.Lunar(datetime(y, 6, 1, 12, 0))
            if l.year8Char == year_gz:
                candidate_years.append(y)
        except Exception:
            continue

    # Step 2: 对每个候选年份，遍历月份找月柱匹配
    rank = 1
    for y in candidate_years:
        for m in range(1, 13):
            # 取月中（15 号）作为参考点
            try:
                l = cnlunar.Lunar(datetime(y, m, 15, 12, 0))
            except Exception:
                continue

            if l.month8Char != month_gz:
                continue

            # Step 3: 月柱匹配 → 遍历该月日期找日柱
            # 按该月实际天数遍历（1-月末），避免漏掉 29/30/31 日出生
            last_day = calendar.monthrange(y, m)[1]
            for d in range(1, last_day + 1):
                try:
                    l_d = cnlunar.Lunar(datetime(y, m, d, 12, 0))
                except Exception:
                    continue

                if l_d.day8Char != day_gz:
                    continue

                # Step 4: 日柱匹配 → 遍历时辰
                # 12 个时辰，从 23:00 上一天 到 22:00 当天
                # 简化：取 12:00 作为默认检查点 + 23:30 边界
                # 如果 12:00 命中，则考虑该日所有时辰
                matched_hours = []
                for hour_int in range(0, 24):
                    # 子时 23:00-00:59 跨日，需要用 24:00 之前的时刻
                    if hour_int >= 23:
                        # 23:00+ 当天 → 次日日柱（但小时柱不变）
                        # 用 hour=23 测试
                        test_dt = datetime(y, m, d, hour_int, 0)
                    else:
                        test_dt = datetime(y, m, d, hour_int, 0)
                    try:
                        l_h = cnlunar.Lunar(test_dt)
                    except Exception:
                        continue
                    if l_h.twohour8Char == hour_gz:
                        matched_hours.append(hour_int)

                if not matched_hours:
                    continue

                # Step 5: 找匹配日中最早一个时辰的代表
                rep_hour = matched_hours[0] if 0 in matched_hours else matched_hours[0]
                rep_dt = datetime(y, m, d, rep_hour, 0)

                try:
                    l_final = cnlunar.Lunar(rep_dt)
                    solar_str = rep_dt.strftime("%Y-%m-%d")
                    lunar_tuple = l_final.get_lunarCn()
                    lunar_str = (
                        f"{lunar_tuple[0][4:]}年 {lunar_tuple[1]} {lunar_tuple[2]}"
                        if len(lunar_tuple) >= 3
                        else ""
                    )
                    shengxiao = SHENGXIAO_MAP.get(l_final.year8Char[1], "")

                    # 节气说明
                    jieqi = l_final.get_todaySolarTerms() or ""
                    jieqi_match = (
                        f"生当月节气={jieqi}（按 cnlunar）"
                        if jieqi
                        else f"无特殊节气"
                    )

                    candidates.append({
                        "solar": solar_str,
                        "lunar": lunar_str,
                        "shengxiao": shengxiao,
                        "year_pillar": l_final.year8Char,
                        "month_pillar": l_final.month8Char,
                        "day_pillar": l_final.day8Char,
                        "hour_pillar": l_final.twohour8Char,
                        "jieqi_match": jieqi_match,
                        "cnlunar_precision": "±1 天（节气日级精度限制）",
                        "matched_hours": [f"{h:02d}:00" for h in matched_hours],
                        "candidate_rank": rank,
                        "score": 1.0,
                    })
                    rank += 1
                except Exception:
                    continue

    return candidates


# ============================================================================
# v1.9.0 模块 7：农历输入解析（农历 → 公历）+ 四柱直接排盘
# ============================================================================
#
# 设计说明：
# - 农历 → 公历：不自己写历法，用 cnlunar 反向搜索（对候选公历日逐一验证
#   农历年月日是否匹配）。cnlunar 已正确处理闰月、大小月，搜索窗口按农历年
#   覆盖（±1 个公历年）足够，性能 ~0.02s。
# - 四柱直接排盘：`build_bazi_from_pillars` 只依赖干支本身（日主十神/藏干/
#   生肖/月支节气区间），不需要公历日期；solar 置 None，输出时标注"公历未知"。

from datetime import timedelta as _timedelta

# 中文数字（农历年/月/日解析）
CN_DIGITS = {
    "零": 0, "〇": 0, "一": 1, "二": 2, "三": 3, "四": 4,
    "五": 5, "六": 6, "七": 7, "八": 8, "九": 9,
}

# 农历月名 → 数字（正月=1 … 腊月=12；冬月=11 为北方俗称）
LUNAR_MONTH_CN = {
    "正": 1, "一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
    "六": 6, "七": 7, "八": 8, "九": 9, "十": 10,
    "冬": 11, "腊": 12,
}

# 时辰 → 代表时刻（取各时辰中点为默认时刻）
# 子[23-01]→00:00  丑[01-03]→02:00 … 酉[17-19]→18:00 … 亥[21-23]→22:00
SHICHEN_HOUR = {
    "子": 0, "丑": 2, "寅": 4, "卯": 6, "辰": 8, "巳": 10,
    "午": 12, "未": 14, "申": 16, "酉": 18, "戌": 20, "亥": 22,
}

# 月支 → 节气区间（四柱输入时展示月令对应节气，如 卯月=惊蛰—清明）
MONTH_ZHI_JIEQI_START = {
    "寅": "立春", "卯": "惊蛰", "辰": "清明", "巳": "立夏",
    "午": "芒种", "未": "小暑", "申": "立秋", "酉": "白露",
    "戌": "寒露", "亥": "立冬", "子": "大雪", "丑": "小寒",
}
MONTH_ZHI_JIEQI_END = {
    "寅": "惊蛰", "卯": "清明", "辰": "立夏", "巳": "芒种",
    "午": "小暑", "未": "立秋", "申": "白露", "酉": "寒露",
    "戌": "立冬", "亥": "大雪", "子": "小寒", "丑": "立春",
}


def _cn_year_to_int(s: str) -> int:
    """中文年份 → int（一九九六 → 1996；逐位读）."""
    try:
        return int("".join(str(CN_DIGITS[c]) for c in s))
    except (KeyError, ValueError):
        raise ValueError(f"无法解析中文年份: {s}")


def _cn_month_to_int(s: str) -> tuple[int, bool]:
    """农历月名 → (月数, 是否闰月)（正月→1 … 冬月→11 腊月→12）."""
    leap = s.startswith("闰")
    if leap:
        s = s[1:]
    if s in ("十一月",):
        return 11, leap
    if s in ("十二月",):
        return 12, leap
    if s and s[0] in LUNAR_MONTH_CN:
        return LUNAR_MONTH_CN[s[0]], leap
    raise ValueError(f"无法解析农历月份: {s}")


def _cn_single_digit(s: str) -> int:
    """单个中文/阿拉伯数字 → int（一→1 … 十→10，1→1）."""
    if s in CN_DIGITS:
        return CN_DIGITS[s]
    if s == "十":
        return 10
    if s.isdigit():
        return int(s)
    raise ValueError(f"无法解析数字: {s}")


def _cn_day_to_int(s: str) -> int:
    """农历日名 → int（初一→1 初十→10 十一→11 二十→20 廿一→21 三十→30）."""
    if s.startswith("初"):
        return _cn_single_digit(s[1:])
    if s.startswith("廿"):
        return 20 + (_cn_single_digit(s[1:]) if len(s) > 1 else 0)
    if s.startswith("三十"):
        return 30
    if s.startswith("二十"):
        return 20 + (_cn_single_digit(s[2:]) if len(s) > 2 else 0)
    if s.startswith("十"):
        return 10 + (_cn_single_digit(s[1:]) if len(s) > 1 else 0)
    return _cn_single_digit(s)


def _cn_hour_to_int(s: str) -> tuple[int, int]:
    """时辰名 → (小时, 分钟)（酉时 → (18, 0)；子时取 00:00）."""
    if s.endswith("时") and s[0] in SHICHEN_HOUR:
        return SHICHEN_HOUR[s[0]], 0
    raise ValueError(f"无法解析时辰: {s}")


_DAY_RE = re.compile(
    r"(初[一二三四五六七八九十]|廿[一二三四五六七八九]?|三十|"
    r"[一二三四五六七八九]十[一二三四五六七八九]?|十[一二三四五六七八九]?|"
    r"[一二三四五六七八九]|\d{1,2})"
)


def parse_lunar_input(text: str) -> dict:
    """解析农历输入字符串 → dict(year, month, day, leap, hour, minute).

    支持格式：
    - "一九九六年 正月廿一 酉时"（中文年份 + 农历月日 + 时辰）
    - "1996年正月廿一 18:00"（阿拉伯年份 + 农历月日 + 具体时刻）
    - "1996年闰四月十五"（闰月，缺省时刻 12:00）
    """
    text = text.strip()
    # 年：4 位阿拉伯或中文数字（可带可不带"年"字）
    m_year = re.search(r"(\d{4}|[〇零一二三四五六七八九]{4})\s*年?", text)
    if not m_year:
        raise ValueError(f"无法解析农历年份: {text!r}")
    year_str = m_year.group(1)
    year = int(year_str) if year_str.isdigit() else _cn_year_to_int(year_str)
    rest = text[m_year.end():]

    # 月：可带闰（闰四月）
    m_mon = re.search(r"(闰?[正一二三四五六七八九十冬腊]+)月", rest)
    if not m_mon:
        raise ValueError(f"无法解析农历月份: {text!r}")
    month, leap = _cn_month_to_int(m_mon.group(1))
    rest = rest[m_mon.end():]

    # 日：紧跟月之后
    m_day = _DAY_RE.match(rest.lstrip())
    if not m_day:
        raise ValueError(f"无法解析农历日期: {text!r}")
    day = _cn_day_to_int(m_day.group(1))
    rest = rest[m_day.end():].strip()

    # 时刻：时辰（酉时）或 HH:MM，缺省 12:00
    hour, minute = 12, 0
    if rest:
        m_hour = re.match(r"([子丑寅卯辰巳午未申酉戌亥])时", rest)
        if m_hour:
            hour, minute = _cn_hour_to_int(m_hour.group(0))
        else:
            m_hm = re.match(r"(\d{1,2}):(\d{2})", rest)
            if m_hm:
                hour, minute = int(m_hm.group(1)), int(m_hm.group(2))
            else:
                raise ValueError(f"无法解析时刻: {rest!r}")

    if not (1 <= month <= 12):
        raise ValueError(f"农历月份超出范围: {month}")
    if not (1 <= day <= 30):
        raise ValueError(f"农历日期超出范围: {day}")
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        raise ValueError(f"时刻超出范围: {hour:02d}:{minute:02d}")
    return {"year": year, "month": month, "day": day,
            "leap": leap, "hour": hour, "minute": minute}


def lunar_to_solar(year: int, month: int, day: int, leap: bool = False,
                   hour: int = 12, minute: int = 0) -> datetime | None:
    """农历 → 公历（cnlunar 反向搜索，窗口覆盖农历年前后各约 1 年）.

    返回匹配的公历 datetime（默认取 12:00 参考点），找不到返回 None。
    注意：返回时刻为参考时刻，由调用方按需替换时分。

    v1.12.0 增强（P2-3 修复）：
    - 如果 leap=True 但指定年没有闰该月，**不会**回退到非闰月，而是返回 None。
      调用方需自行检查（可通过 cnlunar.Lunar(year, 6, 15).getLunarMonthName() 判断）。
    - 找不到对应日期时，搜索窗口完整遍历后才返回 None，不存在中途截断。
    """
    # 农历 N 年约从公历 N-1 年 12 月持续到 N+1 年 6 月（春节 1/21-2/21，
    # 除夕在次年 1 月底-2 月中），搜索窗口取 [N-1-12-01, N+1-07-01) 足够。
    cur = datetime(year - 1, 12, 1, 12, 0)
    end = datetime(year + 1, 7, 1, 12, 0)
    while cur < end:
        try:
            l = cnlunar.Lunar(cur)
        except Exception:
            cur += _timedelta(days=1)
            continue
        num = l.get_lunarDateNum()  # (农历年, 农历月, 农历日)
        is_leap = "闰" in l.get_lunarMonthCN()
        if num[0] == year and num[1] == month and num[2] == day and is_leap == leap:
            return cur.replace(hour=hour, minute=minute)
        cur += _timedelta(days=1)
    return None


def build_bazi_from_lunar_str(text: str) -> Bazi:
    """农历输入 → 完整八字（转公历后走统一 build_bazi 管线）."""
    p = parse_lunar_input(text)
    solar = lunar_to_solar(p["year"], p["month"], p["day"], p["leap"],
                           p["hour"], p["minute"])
    if solar is None:
        raise ValueError(
            f"农历日期无法转换到公历: {text!r}（年份需在 cnlunar 支持范围内）"
        )
    return build_bazi(solar)


def build_bazi_from_pillars(year_gz: str, month_gz: str, day_gz: str,
                            hour_gz: str) -> Bazi:
    """四柱直接排盘：给定 4 个干支 → 完整 Bazi（日主十神/藏干/生肖/节气区间）.

    solar 置 None（公历日期未知），农历字段留空，输出时标注"四柱输入"。
    与 --reverse 反查的区别：这里直接排盘分析，不做日期反查。
    """
    pillars = [year_gz, month_gz, day_gz, hour_gz]
    for gz in pillars:
        if len(gz) != 2 or gz[0] not in TIANGAN or gz[1] not in DIZHI:
            raise ValueError(f"无效干支: {gz!r}（应为 天干+地支 两字，如 甲子）")

    year_p = Pillar(gan=year_gz[0], zhi=year_gz[1])
    month_p = Pillar(gan=month_gz[0], zhi=month_gz[1])
    day_p = Pillar(gan=day_gz[0], zhi=day_gz[1])
    hour_p = Pillar(gan=hour_gz[0], zhi=hour_gz[1])
    day_master = day_gz[0]
    for p in (year_p, month_p, day_p, hour_p):
        p.render(day_master)

    mz = month_p.zhi
    jieqi = (
        f"{mz}月（{MONTH_ZHI_JIEQI_START.get(mz, '')}—"
        f"{MONTH_ZHI_JIEQI_END.get(mz, '')}）"
    )
    shengxiao = SHENGXIAO_MAP.get(year_p.zhi, "")

    return Bazi(
        year=year_p, month=month_p, day=day_p, hour=hour_p,
        day_master=day_master,
        solar=None,
        lunar_year_cn="", lunar_month_cn="", lunar_day_cn="",
        shengxiao=shengxiao, jieqi=jieqi,
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