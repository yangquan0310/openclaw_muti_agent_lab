"""西方占星排盘核心算法 (Western Astrology / Natal Chart).

设计要点
--------
1. **不重新发明轮子**：行星位置、黄道计算、宫位计算全部委托给
   `pyswisseph`（瑞士星历表，2.10+）。我们不重新实现天文计算，避免
   漏掉岁差、章动、ΔT（地球自转变化）等边界条件。

2. **数据驱动**：星座/行星/宫位/相位的对应关系全部存在顶层常量中
   （`SIGNS`、`PLANETS`、`ASPECTS`），不散落在 if/elif 分支里。

3. **明确边界**：本模块只做"排盘"——算行星位置、宫位、相位、10 领域
   强度评分 + 关键词。**不做解读**——解读由 writer / psychologist 派
   根据 references/*.md 框架另行生成。

4. **严守 4 不原则**：
   - 不预测具体事件
   - 不下医学诊断
   - 不替代心理咨询
   - 不传播猎奇/物化

参考:
- SKILL.md（v0.2.0）
- references/astrology-rules.md
- references/*.md 10 领域解读框架

依赖:
- pyswisseph >= 2.10  （瑞士星历表）
- pytz >= 2024.1      （时区数据库）

Author: programmer agent (for 大管家)
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

try:
    import swisseph as swe
except ImportError as e:  # pragma: no cover
    raise ImportError(
        "未安装 pyswisseph，请先运行: pip install pyswisseph"
    ) from e

try:
    import pytz
except ImportError as e:  # pragma: no cover
    raise ImportError(
        "未安装 pytz，请先运行: pip install pytz"
    ) from e


# ============================================================================
# 常量：十二星座
# ============================================================================

# (中文名, 英文名, 符号, 元素, 模式, 阴阳)
SIGNS = [
    ("白羊", "Aries",       "♈", "火", "基本", "阳"),
    ("金牛", "Taurus",      "♉", "土", "固定", "阴"),
    ("双子", "Gemini",      "♊", "风", "变动", "阳"),
    ("巨蟹", "Cancer",      "♋", "水", "基本", "阴"),
    ("狮子", "Leo",         "♌", "火", "固定", "阳"),
    ("处女", "Virgo",       "♍", "土", "变动", "阴"),
    ("天秤", "Libra",       "♎", "风", "基本", "阳"),
    ("天蝎", "Scorpio",     "♏", "水", "固定", "阴"),
    ("射手", "Sagittarius", "♐", "火", "变动", "阳"),
    ("摩羯", "Capricorn",   "♑", "土", "基本", "阴"),
    ("水瓶", "Aquarius",    "♒", "风", "固定", "阳"),
    ("双鱼", "Pisces",      "♓", "水", "变动", "阴"),
]

SIGN_INDEX = {s[0]: i for i, s in enumerate(SIGNS)}
SIGN_BY_INDEX = {i: s[0] for i, s in enumerate(SIGNS)}
SIGN_SYMBOL = {i: s[2] for i, s in enumerate(SIGNS)}
SIGN_ELEMENT = {i: s[3] for i, s in enumerate(SIGNS)}
SIGN_MODE = {i: s[4] for i, s in enumerate(SIGNS)}

# 黄道起始度数（白羊 0°）→ 黄道第 i 星座 = [i*30, (i+1)*30)
SIGN_DEGREE = 30.0

# 星座元素映射（按索引）
ELEMENTS = {"火": ["白羊", "狮子", "射手"],
            "土": ["金牛", "处女", "摩羯"],
            "风": ["双子", "天秤", "水瓶"],
            "水": ["巨蟹", "天蝎", "双鱼"]}

# 星座守护星（传统 + 现代简化版；现代派用括号内）
RULER = {
    "白羊": "火星", "金牛": "金星", "双子": "水星", "巨蟹": "月亮",
    "狮子": "太阳", "处女": "水星", "天秤": "金星", "天蝎": "冥王",
    "射手": "木星", "摩羯": "土星", "水瓶": "天王", "双鱼": "海王",
}


# ============================================================================
# 常量：十大行星
# ============================================================================

# (中文名, swisseph 编号, 主题)
PLANETS = [
    ("太阳", swe.SUN,   "self"),
    ("月亮", swe.MOON,  "emotion"),
    ("水星", swe.MERCURY, "mind"),
    ("金星", swe.VENUS, "love"),
    ("火星", swe.MARS,  "drive"),
    ("木星", swe.JUPITER, "expand"),
    ("土星", swe.SATURN,  "discipline"),
    ("天王", swe.URANUS,  "rebel"),
    ("海王", swe.NEPTUNE, "dream"),
    ("冥王", swe.PLUTO,   "transform"),
]

PLANET_INDEX = {p[0]: i for i, p in enumerate(PLANETS)}
PLANET_BY_INDEX = {i: p[0] for i, p in enumerate(PLANETS)}
PLANET_ID = {p[0]: p[1] for p in PLANETS}
PLANET_THEME = {p[0]: p[2] for p in PLANETS}

# 行星入庙（domicile）/ 失势（detriment）/ 擢升（exaltation）/ 落陷（fall）
DIGNITY = {
    "太阳": {"domicile": "狮子", "detriment": "水瓶",
             "exaltation": "白羊", "fall": "天秤"},
    "月亮": {"domicile": "巨蟹", "detriment": "摩羯",
             "exaltation": "金牛", "fall": "天蝎"},
    "水星": {"domicile": "双子", "detriment": "射手",
             "exaltation": "处女", "fall": "双鱼"},
    "金星": {"domicile": "金牛", "detriment": "天蝎",
             "exaltation": "双鱼", "fall": "处女"},
    "火星": {"domicile": "白羊", "detriment": "天秤",
             "exaltation": "摩羯", "fall": "巨蟹"},
    "木星": {"domicile": "射手", "detriment": "双子",
             "exaltation": "巨蟹", "fall": "摩羯"},
    "土星": {"domicile": "摩羯", "detriment": "巨蟹",
             "exaltation": "天秤", "fall": "白羊"},
    "天王": {"domicile": "水瓶", "detriment": "狮子",
             "exaltation": "天蝎", "fall": "金牛"},
    "海王": {"domicile": "双鱼", "detriment": "处女",
             "exaltation": "狮子", "fall": "水瓶"},
    "冥王": {"domicile": "天蝎", "detriment": "金牛",
             "exaltation": "狮子", "fall": "水瓶"},
}


# ============================================================================
# 常量：十二宫位
# ============================================================================

HOUSE_THEMES = {
    1:  "self",
    2:  "money",
    3:  "communication",
    4:  "home",
    5:  "love",
    6:  "health",
    7:  "partner",
    8:  "intimacy",
    9:  "philosophy",
    10: "career",
    11: "friends",
    12: "subconscious",
}


# ============================================================================
# 常量：主要相位
# ============================================================================

# (中文名, 符号, 角度, 容许度, 类型 hard/soft/neutral)
ASPECTS = [
    ("合相", "☌", 0.0,   8.0, "neutral"),
    ("六合", "⚹", 60.0,  4.0, "soft"),
    ("三分", "△", 120.0, 5.0, "soft"),
    ("刑",   "□", 90.0,  6.0, "hard"),
    ("六刑", "⚺", 30.0,  2.0, "soft"),
    ("冲",   "☍", 180.0, 8.0, "hard"),
]

ASPECT_INDEX = {a[0]: i for i, a in enumerate(ASPECTS)}
ASPECT_BY_INDEX = {i: a for i, a in enumerate(ASPECTS)}


# ============================================================================
# 常量：城市地理数据库
# ============================================================================

# 内置 60+ 城市（中英双语），覆盖主要国际都市 + 中国主要城市
# (lat, lon, timezone)
CITY_DB = {
    # === 中国大陆 ===
    "北京":    (39.9042, 116.4074, "Asia/Shanghai"),
    "上海":    (31.2304, 121.4737, "Asia/Shanghai"),
    "广州":    (23.1291, 113.2644, "Asia/Shanghai"),
    "深圳":    (22.5431, 114.0579, "Asia/Shanghai"),
    "杭州":    (30.2741, 120.1551, "Asia/Shanghai"),
    "南京":    (32.0603, 118.7969, "Asia/Shanghai"),
    "武汉":    (30.5928, 114.3055, "Asia/Shanghai"),
    "成都":    (30.5728, 104.0668, "Asia/Shanghai"),
    "重庆":    (29.5630, 106.5516, "Asia/Shanghai"),
    "西安":    (34.3416, 108.9398, "Asia/Shanghai"),
    "天津":    (39.3434, 117.3616, "Asia/Shanghai"),
    "苏州":    (31.2989, 120.5853, "Asia/Shanghai"),
    "厦门":    (24.4798, 118.0894, "Asia/Shanghai"),
    "青岛":    (36.0671, 120.3826, "Asia/Shanghai"),
    "大连":    (38.9140, 121.6147, "Asia/Shanghai"),
    "长沙":    (28.2282, 112.9388, "Asia/Shanghai"),
    "郑州":    (34.7466, 113.6253, "Asia/Shanghai"),
    "济南":    (36.6512, 117.1201, "Asia/Shanghai"),
    "哈尔滨":  (45.8038, 126.5350, "Asia/Shanghai"),
    "沈阳":    (41.8057, 123.4315, "Asia/Shanghai"),
    "昆明":    (25.0389, 102.7183, "Asia/Shanghai"),
    "拉萨":    (29.6500, 91.1000,  "Asia/Shanghai"),
    "乌鲁木齐": (43.8256, 87.6168, "Asia/Urumqi"),
    "海口":    (20.0444, 110.1989, "Asia/Shanghai"),
    "香港":    (22.3193, 114.1694, "Asia/Hong_Kong"),
    "澳门":    (22.1987, 113.5439, "Asia/Macau"),
    "台北":    (25.0330, 121.5654, "Asia/Taipei"),
    # === 国际 ===
    "纽约":   (40.7128, -74.0060,  "America/New_York"),
    "New York": (40.7128, -74.0060, "America/New_York"),
    "洛杉矶": (34.0522, -118.2437, "America/Los_Angeles"),
    "Los Angeles": (34.0522, -118.2437, "America/Los_Angeles"),
    "芝加哥": (41.8781, -87.6298,  "America/Chicago"),
    "Chicago": (41.8781, -87.6298, "America/Chicago"),
    "伦敦":   (51.5074, -0.1278,   "Europe/London"),
    "London": (51.5074, -0.1278,   "Europe/London"),
    "巴黎":   (48.8566, 2.3522,    "Europe/Paris"),
    "Paris":  (48.8566, 2.3522,    "Europe/Paris"),
    "柏林":   (52.5200, 13.4050,   "Europe/Berlin"),
    "Berlin": (52.5200, 13.4050,   "Europe/Berlin"),
    "罗马":   (41.9028, 12.4964,   "Europe/Rome"),
    "Rome":   (41.9028, 12.4964,   "Europe/Rome"),
    "东京":   (35.6762, 139.6503,  "Asia/Tokyo"),
    "Tokyo":  (35.6762, 139.6503,  "Asia/Tokyo"),
    "首尔":   (37.5665, 126.9780,  "Asia/Seoul"),
    "Seoul":  (37.5665, 126.9780,  "Asia/Seoul"),
    "新加坡": (1.3521,  103.8198,  "Asia/Singapore"),
    "Singapore": (1.3521, 103.8198, "Asia/Singapore"),
    "悉尼":   (-33.8688, 151.2093, "Australia/Sydney"),
    "Sydney": (-33.8688, 151.2093, "Australia/Sydney"),
    "墨尔本": (-37.8136, 144.9631, "Australia/Melbourne"),
    "Melbourne": (-37.8136, 144.9631, "Australia/Melbourne"),
    "莫斯科": (55.7558, 37.6173,   "Europe/Moscow"),
    "Moscow": (55.7558, 37.6173,   "Europe/Moscow"),
    "迪拜":   (25.2048, 55.2708,   "Asia/Dubai"),
    "Dubai":  (25.2048, 55.2708,   "Asia/Dubai"),
    "孟买":   (19.0760, 72.8777,   "Asia/Kolkata"),
    "Mumbai": (19.0760, 72.8777,   "Asia/Kolkata"),
    "多伦多": (43.6532, -79.3832,  "America/Toronto"),
    "Toronto": (43.6532, -79.3832, "America/Toronto"),
    "温哥华": (49.2827, -123.1207, "America/Vancouver"),
    "Vancouver": (49.2827, -123.1207, "America/Vancouver"),
    "墨西哥城": (19.4326, -99.1332, "America/Mexico_City"),
    "Mexico City": (19.4326, -99.1332, "America/Mexico_City"),
    "圣保罗": (-23.5505, -46.6333, "America/Sao_Paulo"),
    "São Paulo": (-23.5505, -46.6333, "America/Sao_Paulo"),
    "开罗":   (30.0444, 31.2357,   "Africa/Cairo"),
    "Cairo":  (30.0444, 31.2357,   "Africa/Cairo"),
    "约翰内斯堡": (-26.2041, 28.0473, "Africa/Johannesburg"),
    "Johannesburg": (-26.2041, 28.0473, "Africa/Johannesburg"),
    "曼谷":   (13.7563, 100.5018,  "Asia/Bangkok"),
    "Bangkok": (13.7563, 100.5018, "Asia/Bangkok"),
    "雅加达": (-6.2088, 106.8456,  "Asia/Jakarta"),
    "Jakarta": (-6.2088, 106.8456, "Asia/Jakarta"),
    "马尼拉": (14.5995, 120.9842,  "Asia/Manila"),
    "Manila": (14.5995, 120.9842,  "Asia/Manila"),
    "马德里": (40.4168, -3.7038,   "Europe/Madrid"),
    "Madrid": (40.4168, -3.7038,   "Europe/Madrid"),
    "阿姆斯特丹": (52.3676, 4.9041, "Europe/Amsterdam"),
    "Amsterdam": (52.3676, 4.9041, "Europe/Amsterdam"),

    # === 山西省 11 地级市（2026-07-29 老板补充）===
    "太原":      (37.8706, 112.5489, "Asia/Shanghai"),
    "Taiyuan":   (37.8706, 112.5489, "Asia/Shanghai"),
    "大同":      (40.0764, 113.2998, "Asia/Shanghai"),
    "Datong":    (40.0764, 113.2998, "Asia/Shanghai"),
    "阳泉":      (37.8576, 113.5763, "Asia/Shanghai"),
    "Yangquan":  (37.8576, 113.5763, "Asia/Shanghai"),
    "长治":      (36.1955, 113.1163, "Asia/Shanghai"),
    "Changzhi":  (36.1955, 113.1163, "Asia/Shanghai"),
    "晋城":      (35.4906, 112.8514, "Asia/Shanghai"),
    "Jincheng":  (35.4906, 112.8514, "Asia/Shanghai"),
    "朔州":      (39.3315, 112.4329, "Asia/Shanghai"),
    "Shuozhou":  (39.3315, 112.4329, "Asia/Shanghai"),
    "晋中":      (37.6878, 112.7528, "Asia/Shanghai"),
    "Jinzhong":  (37.6878, 112.7528, "Asia/Shanghai"),
    "运城":      (35.0269, 111.0030, "Asia/Shanghai"),
    "Yuncheng":  (35.0269, 111.0030, "Asia/Shanghai"),
    "忻州":      (38.4167, 112.7341, "Asia/Shanghai"),
    "Xinzhou":   (38.4167, 112.7341, "Asia/Shanghai"),
    "临汾":      (36.0880, 111.5189, "Asia/Shanghai"),
    "Linfen":    (36.0880, 111.5189, "Asia/Shanghai"),
    "吕梁":      (37.5186, 111.1343, "Asia/Shanghai"),
    "Lvliang":   (37.5186, 111.1343, "Asia/Shanghai"),

    # === 周边省会（2026-07-29 老板补充）===
    "石家庄":    (38.0428, 114.5149, "Asia/Shanghai"),
    "Shijiazhuang": (38.0428, 114.5149, "Asia/Shanghai"),
    "呼和浩特":  (40.8423, 111.7492, "Asia/Shanghai"),
    "Hohhot":    (40.8423, 111.7492, "Asia/Shanghai"),
    "兰州":      (36.0611, 103.8343, "Asia/Shanghai"),
    "Lanzhou":   (36.0611, 103.8343, "Asia/Shanghai"),
    "银川":      (38.4872, 106.2309, "Asia/Shanghai"),
    "Yinchuan":  (38.4872, 106.2309, "Asia/Shanghai"),
    "西宁":      (36.6232, 101.7804, "Asia/Shanghai"),
    "Xining":    (36.6232, 101.7804, "Asia/Shanghai"),
    "贵阳":      (26.6470, 106.6302, "Asia/Shanghai"),
    "Guiyang":   (26.6470, 106.6302, "Asia/Shanghai"),
    "南宁":      (22.8170, 108.3665, "Asia/Shanghai"),
    "Nanning":   (22.8170, 108.3665, "Asia/Shanghai"),
    "福州":      (26.0745, 119.2965, "Asia/Shanghai"),
    "Fuzhou":    (26.0745, 119.2965, "Asia/Shanghai"),
    "合肥":      (31.8206, 117.2272, "Asia/Shanghai"),
    "Hefei":     (31.8206, 117.2272, "Asia/Shanghai"),
    "南昌":      (28.6820, 115.8579, "Asia/Shanghai"),
    "Nanchang":  (28.6820, 115.8579, "Asia/Shanghai"),
}


def resolve_location(location: str) -> tuple[float, float, str]:
    """根据城市名称查表，返回 (纬度, 经度, 时区).

    Args:
        location: 城市名（中文/英文）

    Returns:
        (lat, lon, tz_name)

    Raises:
        ValueError: 未在 CITY_DB 中找到。
    """
    key = location.strip()
    if key in CITY_DB:
        return CITY_DB[key]
    # 尝试大小写不敏感
    for k in CITY_DB:
        if k.lower() == key.lower():
            return CITY_DB[k]
    raise ValueError(
        f"未识别的城市: {location}。请使用 CITY_DB 中已收录的城市，"
        f"或传入 'lat,lon,tz' 字符串。"
    )


def parse_location(location: str) -> tuple[float, float, str]:
    """支持城市名或 'lat,lon,tz' 直传."""
    # 直传格式: "39.9,116.4,Asia/Shanghai"
    m = re.match(r"^(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*,\s*(\S+)$",
                 location.strip())
    if m:
        lat = float(m.group(1))
        lon = float(m.group(2))
        tz = m.group(3)
        return lat, lon, tz
    return resolve_location(location)


# ============================================================================
# 工具函数
# ============================================================================

def longitude_to_sign(lon: float) -> tuple[int, float]:
    """黄道经度 (0-360) → (星座索引, 度数 0-30)."""
    lon = lon % 360.0
    idx = int(lon / SIGN_DEGREE) % 12
    degree = lon - idx * SIGN_DEGREE
    return idx, degree


def longitude_to_sign_name(lon: float) -> str:
    idx, _ = longitude_to_sign(lon)
    return SIGN_BY_INDEX[idx]


def normalize_angle(x: float) -> float:
    """归一化到 [0, 360)."""
    return x % 360.0


def angle_diff(a: float, b: float) -> float:
    """两黄道经度的最短夹角 (0-180)."""
    d = abs(normalize_angle(a) - normalize_angle(b))
    if d > 180.0:
        d = 360.0 - d
    return d


def element_of_sign(idx_or_name) -> str:
    if isinstance(idx_or_name, str):
        return SIGN_ELEMENT[SIGN_INDEX[idx_or_name]]
    return SIGN_ELEMENT[idx_or_name]


def mode_of_sign(idx_or_name) -> str:
    if isinstance(idx_or_name, str):
        return SIGN_MODE[SIGN_INDEX[idx_or_name]]
    return SIGN_MODE[idx_or_name]


def sign_name_of_planet(lon: float) -> str:
    return longitude_to_sign_name(lon)


# ============================================================================
# pyswisseph 计算
# ============================================================================

# 设定儒略日 → UT 时使用的 deltaT 修正（pyswisseph 内置）
def julian_day(year: int, month: int, day: int, hour_frac: float) -> float:
    """公历 → 儒略日（UT）."""
    return swe.julday(year, month, day, hour_frac)


def calc_planet(jd_ut: float, planet_id: int) -> tuple[float, float, float, bool]:
    """行星位置：(lon, lat, speed_lon, retrograde)."""
    result, _ = swe.calc_ut(jd_ut, planet_id)
    lon = result[0]
    lat = result[1]
    speed_lon = result[3]
    retrograde = speed_lon < 0.0
    return lon, lat, speed_lon, retrograde


def calc_houses(jd_ut: float, lat: float, lon: float,
                system: bytes = b"P") -> tuple[list[float], list[float]]:
    """计算宫位。系统: P=Placidus（默认）, W=Whole Sign, K=Koch, E=Equal.

    返回 (cusps[12], ascmc[10]).
    """
    cusps, ascmc = swe.houses(jd_ut, lat, lon, system)
    return list(cusps), list(ascmc)


def planet_house(planet_lon: float, cusps: list[float]) -> int:
    """给定行星黄道经度 + 12 宫位起点 → 1-12 宫."""
    p = planet_lon % 360.0
    for i in range(12):
        c1 = cusps[i] % 360.0
        c2 = cusps[(i + 1) % 12] % 360.0
        if c1 < c2:
            if c1 <= p < c2:
                return i + 1
        else:
            # 跨 0°
            if p >= c1 or p < c2:
                return i + 1
    return 12  # fallback


def compute_aspects(planet_positions: dict[str, float]) -> list[dict]:
    """计算所有行星两两之间的主要相位.

    planet_positions: {"太阳": 54.5, "月亮": 130.2, ...} (lon)
    """
    aspects = []
    names = list(planet_positions.keys())
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            p1 = names[i]
            p2 = names[j]
            d = angle_diff(planet_positions[p1], planet_positions[p2])
            for asp_name, symbol, angle, orb_max, kind in ASPECTS:
                if abs(d - angle) <= orb_max:
                    actual_orb = abs(d - angle)
                    aspects.append({
                        "p1": p1,
                        "p2": p2,
                        "aspect": asp_name,
                        "symbol": symbol,
                        "angle": angle,
                        "orb": round(actual_orb, 2),
                        "kind": kind,
                    })
                    break  # 一个相位对只取第一个匹配的角度
    return aspects


# ============================================================================
# 行星位置描述（关键词）
# ============================================================================

# 行星落入各星座的关键词（按 [love/career/general] 分类）
# 来源：references/*.md 中各领域框架的描述

PLANET_IN_SIGN_KEYWORDS = {
    "太阳": {
        "白羊": "主动、独立、开创", "金牛": "稳定、感官、坚定",
        "双子": "好奇、沟通、多变", "巨蟹": "情感、保护、内敛",
        "狮子": "领导、创造、表现", "处女": "细致、分析、服务",
        "天秤": "平衡、合作、优雅", "天蝎": "深度、强烈、转化",
        "射手": "乐观、探索、自由", "摩羯": "纪律、责任、雄心",
        "水瓶": "独立、创新、人道", "双鱼": "灵性、直觉、同情",
    },
    "月亮": {
        "白羊": "冲动、直接、外显", "金牛": "稳定、依赖、安全",
        "双子": "多变、好奇、理性", "巨蟹": "敏感、保护、滋养",
        "狮子": "热情、戏剧、慷慨", "处女": "细致、谨慎、实际",
        "天秤": "和谐、社交、依赖", "天蝎": "深度、占有、强烈",
        "射手": "乐观、自由、需要空间", "摩羯": "克制、严肃、自律",
        "水瓶": "独立、超然、非常规", "双鱼": "梦幻、敏感、共情",
    },
    "金星": {
        "白羊": "主动、直接、冲动", "金牛": "感官、慢热、稳定",
        "双子": "智识、沟通、新奇", "巨蟹": "温柔、滋养、保护",
        "狮子": "戏剧、赞美、慷慨", "处女": "实际、细致、改进",
        "天秤": "和谐、优雅、平衡", "天蝎": "深度、占有、转化",
        "射手": "自由、冒险、乐观", "摩羯": "责任、稳定、传统",
        "水瓶": "独立、非常规、智识", "双鱼": "浪漫、灵性、梦幻",
    },
    "火星": {
        "白羊": "冲动、直接、行动派", "金牛": "缓慢、持续、感官",
        "双子": "多变、好奇、言语", "巨蟹": "情感、保护、被动",
        "狮子": "戏剧、表演、主动", "处女": "细致、分析、谨慎",
        "天秤": "被动、平衡、依赖", "天蝎": "深度、控制、执着",
        "射手": "冒险、自由、独立", "摩羯": "纪律、压抑、长期",
        "水瓶": "独立、突变、智识", "双鱼": "梦幻、被动、灵性",
    },
    "水星": {
        "白羊": "直接、快速、简洁", "金牛": "缓慢、考虑、实际",
        "双子": "机智、多变、广博", "巨蟹": "情感、保护、隐喻",
        "狮子": "戏剧、表达、创造", "处女": "细致、分析、逻辑",
        "天秤": "平衡、外交、考虑", "天蝎": "深度、探究、沉默",
        "射手": "直率、哲学、夸张", "摩羯": "严肃、简洁、权威",
        "水瓶": "非常规、创新、智识", "双鱼": "梦幻、隐喻、艺术",
    },
    "木星": {
        "白羊": "开拓、勇气、领导", "金牛": "稳定、物质、积累",
        "双子": "学习、传播、多元", "巨蟹": "扩展、滋养、保护",
        "狮子": "创造、表演、慷慨", "处女": "细节、服务、健康",
        "天秤": "合作、公平、平衡", "天蝎": "深度、转化、权力",
        "射手": "哲学、远行、智慧", "摩羯": "结构、传统、权威",
        "水瓶": "愿景、人道、创新", "双鱼": "灵性、同情、梦幻",
    },
    "土星": {
        "白羊": "克制的主动、延迟的开创", "金牛": "稳定、物质、长期",
        "双子": "严肃的沟通、纪律的学习", "巨蟹": "克制的情感、家族责任",
        "狮子": "克制的表达、权威的责任", "处女": "细节的纪律、工作伦理",
        "天秤": "公平的责任、关系纪律", "天蝎": "深度控制、转化纪律",
        "射手": "克制的信念、哲学纪律", "摩羯": "结构、权威、长期目标",
        "水瓶": "结构化创新、人道纪律", "双鱼": "灵性纪律、克制的梦幻",
    },
    "天王": {"白羊": "突发的开创、激进的独立", "金牛": "物质变革、价值颠覆",
        "双子": "沟通革命、思维突破", "巨蟹": "情感颠覆、家庭模式突变",
        "狮子": "创造性突破、自我表达革命", "处女": "工作方式革命、健康议题",
        "天秤": "关系革命、合作模式突变", "天蝎": "深度转化、权力颠覆",
        "射手": "信念突破、远行突变", "摩羯": "结构颠覆、权威革命",
        "水瓶": "创新、人道、解放", "双鱼": "灵性突破、梦幻边界模糊",
    },
    "海王": {"白羊": "梦幻的主动", "金牛": "感官的灵性化",
        "双子": "梦幻的沟通", "巨蟹": "深层的情感",
        "狮子": "灵性的创造", "处女": "细致的灵性",
        "天秤": "和谐的灵性", "天蝎": "深度的灵性",
        "射手": "扩展的灵性", "摩羯": "结构的灵性",
        "水瓶": "解放的灵性", "双鱼": "灵性、直觉、共鸣",
    },
    "冥王": {"白羊": "激进的转化", "金牛": "物质转化、价值重塑",
        "双子": "沟通转化", "巨蟹": "情感转化、家庭议题",
        "狮子": "创造转化", "处女": "细节转化、工作议题",
        "天秤": "关系转化", "天蝎": "深度、权力、转化",
        "射手": "信念转化", "摩羯": "结构转化、权力议题",
        "水瓶": "系统转化、人道议题", "双鱼": "灵性转化、集体议题",
    },
}


# ============================================================================
# 10 领域强度评分（占星版）
# ============================================================================

# 每个领域对应的"评分依据星体权重"
# 公式：领域强度 = Σ(行星分 × 权重)
# 行星分 = 落入庙/擢升=5 / 友好=4 / 中性=3 / 失势=2 / 落陷=1
#         + 相位加成：硬相位 -0.5, 软相位 +0.3, 合相 +0.4

DOMAIN_WEIGHTS = {
    "love":         {"金星": 0.35, "火星": 0.30, "月亮": 0.20, "冥王": 0.15},
    "career":       {"太阳": 0.30, "土星": 0.30, "木星": 0.15, "火星": 0.25},
    "wealth":       {"木星": 0.30, "金星": 0.25, "土星": 0.20, "冥王": 0.25},
    "health":       {"太阳": 0.30, "火星": 0.25, "土星": 0.25, "月亮": 0.20},
    "relationship": {"金星": 0.30, "月亮": 0.25, "水星": 0.20, "木星": 0.25},
    "study":        {"水星": 0.35, "木星": 0.30, "月亮": 0.20, "土星": 0.15},
    "family":       {"月亮": 0.35, "太阳": 0.25, "土星": 0.20, "冥王": 0.20},
    "children":     {"木星": 0.40, "金星": 0.25, "火星": 0.20, "月亮": 0.15},
    "spirituality": {"海王": 0.30, "木星": 0.30, "冥王": 0.20, "月亮": 0.20},
    "sexuality":    {"火星": 0.30, "冥王": 0.25, "金星": 0.20, "月亮": 0.25},
}

DOMAIN_LABEL = {
    "love":         "感情/爱情",
    "career":       "事业/工作",
    "wealth":       "财富/金钱",
    "health":       "健康/身体",
    "relationship": "人际/关系",
    "study":        "学业/学习",
    "family":       "家庭/父母",
    "children":     "子女/后代",
    "spirituality": "灵性/成长",
    "sexuality":    "性欲/性功能",
}


def _planet_base_score(planet: str, sign: str) -> float:
    """行星落入某星座的"基础强度分" 1-5."""
    dig = DIGNITY.get(planet, {})
    if sign == dig.get("domicile"):
        return 5.0
    if sign == dig.get("exaltation"):
        return 4.8
    # 友好元素：同元素 +1, 友好元素 +0.5
    elem_self = SIGN_ELEMENT[SIGN_INDEX[sign]]
    if planet == "太阳":
        # 太阳：火相=同元素
        if elem_self == "火":
            return 4.0
        return 3.0
    if planet == "月亮":
        # 月亮：水相=同元素
        if elem_self == "水":
            return 4.0
        return 3.0
    if planet == "金星":
        # 金星：土相/风相
        if elem_self in ("土", "风"):
            return 4.0
        return 2.8
    if planet == "火星":
        # 火星：火相/水相（天蝎）
        if elem_self in ("火", "水"):
            return 4.0
        return 2.8
    if planet == "水星":
        # 水星：风相/土相
        if elem_self in ("风", "土"):
            return 4.0
        return 3.0
    if planet == "木星":
        # 木星：火相/水相
        if elem_self in ("火", "水"):
            return 4.0
        return 3.0
    if planet == "土星":
        # 土星：土相/风相
        if elem_self in ("土", "风"):
            return 4.0
        return 3.0
    if planet == "天王":
        # 天王：风相
        if elem_self == "风":
            return 4.0
        return 3.0
    if planet == "海王":
        # 海王：水相
        if elem_self == "水":
            return 4.0
        return 3.0
    if planet == "冥王":
        # 冥王：水相/火相
        if elem_self in ("水", "火"):
            return 4.0
        return 3.0
    return 3.0


def _aspect_modifier(aspects: list[dict], target_planet: str) -> float:
    """目标行星被相位修饰：硬相位 -0.5，软相位 +0.3，合相 +0.4."""
    mod = 0.0
    for asp in aspects:
        if asp["p1"] == target_planet or asp["p2"] == target_planet:
            if asp["aspect"] == "合相":
                mod += 0.4
            elif asp["kind"] == "soft":
                mod += 0.3
            elif asp["kind"] == "hard":
                mod -= 0.5
    # 限制在 [-1, +1]
    return max(-1.0, min(1.0, mod))


def compute_domain_score(domain: str, planet_signs: dict[str, str],
                         aspects: list[dict]) -> tuple[float, list[str]]:
    """计算某领域强度 1-5 + 主导关键词.

    planet_signs: {"太阳": "金牛", "金星": "双子", ...}
    aspects: compute_aspects() 的结果
    """
    weights = DOMAIN_WEIGHTS.get(domain, {})
    if not weights:
        return 3.0, []
    total = 0.0
    keywords_per_planet: list[str] = []
    for planet, w in weights.items():
        sign = planet_signs.get(planet, "")
        if not sign:
            continue
        base = _planet_base_score(planet, sign)
        mod = _aspect_modifier(aspects, planet)
        score = max(1.0, min(5.0, base + mod))
        total += score * w
        # 收集关键词
        kw = PLANET_IN_SIGN_KEYWORDS.get(planet, {}).get(sign, "")
        if kw:
            keywords_per_planet.append(f"{planet}{sign}：{kw}")
    # 归一化到 1-5（5 分制），强度足够多直接放大
    final = max(1.0, min(5.0, total))
    return round(final, 1), keywords_per_planet[:4]


def compute_profile(planet_signs: dict[str, str],
                    aspects: list[dict]) -> dict:
    """10 领域完整画像."""
    profile = {}
    for domain in DOMAIN_LABEL:
        intensity, keywords = compute_domain_score(domain, planet_signs, aspects)
        profile[domain] = {
            "intensity": intensity,
            "keywords": keywords,
        }
    return profile


# ============================================================================
# 数据类
# ============================================================================

@dataclass
class PlanetInfo:
    name: str
    lon: float          # 黄道经度
    lat: float          # 黄道纬度
    speed: float        # 黄道方向速度
    sign: str           # 星座
    sign_index: int
    degree: float       # 星座内度数 0-30
    house: int          # 1-12 宫
    retrograde: bool


@dataclass
class Chart:
    solar: datetime
    location: str
    lat: float
    lon: float
    tz_name: str
    jd_ut: float
    house_system: str

    sun: PlanetInfo
    moon: PlanetInfo
    rising: str          # 上升星座（含度数，如"处女 8°"）
    rising_sign: str
    rising_degree: float
    mc: str              # 中天
    mc_sign: str
    mc_degree: float

    planets: dict[str, PlanetInfo]   # 含 sun/moon
    cusps: list[float]               # 12 宫位起点 (0-360)
    aspects: list[dict]              # 所有相位

    # 10 领域画像（可选：compatibility 模式不需要）
    profile: Optional[dict] = None

    # 可选：合盘信息
    compatibility: Optional[dict] = None

    # ---- pretty ----
    def pretty(self) -> str:
        """人类可读排盘（文本输出）。"""
        lines = []
        lines.append(f"公历：{self.solar.strftime('%Y-%m-%d %H:%M')}")
        lines.append(f"地点：{self.location} ({self.lat:.2f}, {self.lon:.2f}, {self.tz_name})")
        lines.append(f"宫位系统：{self.house_system}")
        lines.append("")
        lines.append(f"太阳：{self.sun.sign} {self.sun.degree:.1f}° ({self.sun.house} 宫)")
        lines.append(f"月亮：{self.moon.sign} {self.moon.degree:.1f}° ({self.moon.house} 宫)")
        lines.append(f"上升：{self.rising}")
        lines.append(f"中天：{self.mc}")
        lines.append("")

        lines.append("行星位置：")
        # 排序：日月水金火木土天海冥
        order = ["太阳", "月亮", "水星", "金星", "火星",
                 "木星", "土星", "天王", "海王", "冥王"]
        for name in order:
            p = self.planets[name]
            ret = "（逆行）" if p.retrograde else ""
            lines.append(f"  {name} {SIGN_SYMBOL[p.sign_index]} {p.sign} "
                         f"{p.degree:.1f}°   {p.house} 宫{ret}")
        lines.append("")

        lines.append("主要相位：")
        if not self.aspects:
            lines.append("  （无）")
        else:
            for asp in self.aspects:
                lines.append(
                    f"  {asp['p1']} {asp['symbol']} {asp['p2']}"
                    f"（{asp['angle']}°±{asp['orb']}°）"
                )
        lines.append("")

        if self.profile:
            lines.append("10 领域解读摘要：")
            for i, domain in enumerate(DOMAIN_LABEL, 1):
                info = self.profile[domain]
                stars = "⭐" * int(round(info["intensity"]))
                if not stars:
                    stars = "·"
                lines.append(f"{i:2d}. {DOMAIN_LABEL[domain]}：{stars}")
                if info["keywords"]:
                    lines.append(f"    - 关键词：{info['keywords'][0]}")
            lines.append("")

        if self.compatibility:
            lines.append("合盘摘要：")
            for k, v in self.compatibility.items():
                lines.append(f"  {k}: {v}")
            lines.append("")

        lines.append("⚠️ 本排盘仅供学术研究与文化记录使用，")
        lines.append("   不构成医学/心理学/投资/婚恋建议。")
        return "\n".join(lines)

    def profile_text(self, domain: str) -> str:
        """单领域解读文本."""
        if not self.profile:
            return f"未计算画像（domain={domain}）"
        info = self.profile.get(domain)
        if not info:
            return f"未知领域: {domain}"
        stars = "⭐" * int(round(info["intensity"]))
        if not stars:
            stars = "·"
        lines = []
        lines.append(f"{DOMAIN_LABEL[domain]}：{stars}（{info['intensity']}/5）")
        lines.append("关键词：")
        for kw in info["keywords"]:
            lines.append(f"  - {kw}")
        lines.append("")
        lines.append("⚠️ 本解读仅作文化/心理层面的描述，")
        lines.append("   不构成医学/心理学/职业/婚恋建议。")
        return "\n".join(lines)

    def to_dict(self) -> dict:
        """JSON-friendly dict（按 SKILL.md §JSON 格式）."""
        out = {
            "solar": self.solar.strftime("%Y-%m-%d %H:%M"),
            "location": self.location,
            "lat": round(self.lat, 4),
            "lon": round(self.lon, 4),
            "timezone": self.tz_name,
            "house_system": self.house_system,
            "sun": {
                "sign": self.sun.sign,
                "degree": round(self.sun.degree, 2),
                "house": self.sun.house,
                "retrograde": self.sun.retrograde,
            },
            "moon": {
                "sign": self.moon.sign,
                "degree": round(self.moon.degree, 2),
                "house": self.moon.house,
                "retrograde": self.moon.retrograde,
            },
            "rising": self.rising,
            "rising_sign": self.rising_sign,
            "rising_degree": round(self.rising_degree, 2),
            "mc": self.mc,
            "mc_sign": self.mc_sign,
            "mc_degree": round(self.mc_degree, 2),
            "planets": {},
            "aspects": self.aspects,
        }
        for name, p in self.planets.items():
            out["planets"][name] = {
                "sign": p.sign,
                "degree": round(p.degree, 2),
                "house": p.house,
                "retrograde": p.retrograde,
            }
        if self.profile:
            out["profile"] = {}
            for domain, info in self.profile.items():
                out["profile"][domain] = {
                    "intensity": info["intensity"],
                    "keywords": info["keywords"],
                }
        if self.compatibility:
            out["compatibility"] = self.compatibility
        return out


# ============================================================================
# 核心：build_chart
# ============================================================================

def build_chart(solar_local: datetime,
                lat: float,
                lon: float,
                tz_name: str,
                location: str = "",
                house_system: str = "P") -> Chart:
    """根据公历本地时间 + 经纬度构造完整星盘.

    Args:
        solar_local: 本地时间（naive datetime）。
        lat, lon: 出生地经纬度。
        tz_name: IANA 时区名（e.g. "Asia/Shanghai"）。
        location: 出生地名称（仅用于显示）。
        house_system: 宫位系统（P=Placidus 默认, W=Whole Sign, K=Koch, E=Equal）。
    """
    # 1. 当地时间 → UTC → UT（儒略日）
    tz = pytz.timezone(tz_name)
    # 用户传入 naive datetime 当作本地时间
    if solar_local.tzinfo is None:
        local_dt = tz.localize(solar_local)
    else:
        local_dt = solar_local.astimezone(tz)
    # 转 UTC
    utc_dt = local_dt.astimezone(pytz.UTC)
    hour_frac = utc_dt.hour + utc_dt.minute / 60.0 + utc_dt.second / 3600.0
    jd_ut = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, hour_frac)

    # 2. 计算 10 大行星位置
    planets: dict[str, PlanetInfo] = {}
    for name, pid, _theme in PLANETS:
        lon_p, lat_p, speed_p, retro = calc_planet(jd_ut, pid)
        idx, deg = longitude_to_sign(lon_p)
        planets[name] = PlanetInfo(
            name=name,
            lon=lon_p,
            lat=lat_p,
            speed=speed_p,
            sign=SIGN_BY_INDEX[idx],
            sign_index=idx,
            degree=deg,
            house=0,  # 占位，下面填充
            retrograde=retro,
        )

    # 3. 计算宫位
    sys_b = house_system.encode()[:1] if isinstance(house_system, str) else house_system
    cusps, ascmc = calc_houses(jd_ut, lat, lon, sys_b)

    # 4. 给每个行星分配宫位
    for p in planets.values():
        p.house = planet_house(p.lon, cusps)

    # 5. 上升 / 中天
    asc_lon = ascmc[0]
    mc_lon = ascmc[1]
    asc_idx, asc_deg = longitude_to_sign(asc_lon)
    mc_idx, mc_deg = longitude_to_sign(mc_lon)

    # 6. 相位（仅星体之间，不含 ASC/MC，避免噪音）
    planet_lons = {name: p.lon for name, p in planets.items()}
    aspects = compute_aspects(planet_lons)

    return Chart(
        solar=solar_local,
        location=location or f"{lat:.2f},{lon:.2f}",
        lat=lat,
        lon=lon,
        tz_name=tz_name,
        jd_ut=jd_ut,
        house_system=house_system,
        sun=planets["太阳"],
        moon=planets["月亮"],
        rising=f"{SIGN_BY_INDEX[asc_idx]} {asc_deg:.1f}°",
        rising_sign=SIGN_BY_INDEX[asc_idx],
        rising_degree=asc_deg,
        mc=f"{SIGN_BY_INDEX[mc_idx]} {mc_deg:.1f}°",
        mc_sign=SIGN_BY_INDEX[mc_idx],
        mc_degree=mc_deg,
        planets=planets,
        cusps=cusps,
        aspects=aspects,
        profile=None,           # 按需填
        compatibility=None,
    )


def build_chart_from_str(date_str: str,
                         time_str: str = "12:00",
                         location: str = "北京") -> Chart:
    """便捷入口：`build_chart_from_str("1990-05-15", "14:30", location="纽约")`."""
    y, m, d = date_str.split("-")
    hh, mm = time_str.split(":")
    solar = datetime(int(y), int(m), int(d), int(hh), int(mm))
    lat, lon, tz = parse_location(location)
    chart = build_chart(solar, lat, lon, tz, location=location)
    # 默认填充 profile（性能允许时）
    chart.profile = compute_profile(
        {n: p.sign for n, p in chart.planets.items()},
        chart.aspects,
    )
    return chart


# ============================================================================
# 合盘（synastry）：两个人的行星之间相位
# ============================================================================

def compatibility(chart_a: Chart, chart_b: Chart) -> dict:
    """计算两人合盘的核心指标.

    返回 dict:
    - aspects: A vs B 行星相位列表
    - overlap_signs: A 与 B 落入相同星座的行星对
    - overlap_houses: A 行星落入 B 宫位的列表
    - score: 0-100 综合匹配分（仅供文化参考，不替代关系评估）
    """
    # 1. 行星之间相位
    inter_lons = {**{f"A:{n}": p.lon for n, p in chart_a.planets.items()},
                  **{f"B:{n}": p.lon for n, p in chart_b.planets.items()}}
    inter_aspects = []
    for i, p1 in enumerate(chart_a.planets):
        for p2 in chart_b.planets:
            d = angle_diff(chart_a.planets[p1].lon, chart_b.planets[p2].lon)
            for asp_name, symbol, angle, orb_max, kind in ASPECTS:
                if abs(d - angle) <= orb_max:
                    inter_aspects.append({
                        "a_planet": p1,
                        "b_planet": p2,
                        "aspect": asp_name,
                        "symbol": symbol,
                        "orb": round(abs(d - angle), 2),
                        "kind": kind,
                    })
                    break

    # 2. 同星座
    overlap_signs = []
    for n_a in chart_a.planets:
        for n_b in chart_b.planets:
            if chart_a.planets[n_a].sign == chart_b.planets[n_b].sign:
                overlap_signs.append({
                    "planet": n_a,
                    "b_planet": n_b,
                    "sign": chart_a.planets[n_a].sign,
                })

    # 3. A 行星落入 B 宫位
    overlap_houses = []
    for n_a, p_a in chart_a.planets.items():
        h = planet_house(p_a.lon, chart_b.cusps)
        overlap_houses.append({"a_planet": n_a, "b_house": h})

    # 4. 综合匹配分（文化层面）
    soft = sum(1 for a in inter_aspects if a["kind"] == "soft")
    hard = sum(1 for a in inter_aspects if a["kind"] == "hard")
    conj = sum(1 for a in inter_aspects if a["aspect"] == "合相")
    score = 50 + soft * 5 + conj * 2 - hard * 3
    score = max(0, min(100, score))

    return {
        "aspects": inter_aspects,
        "overlap_signs": overlap_signs,
        "overlap_houses": overlap_houses,
        "score": score,
        "soft_count": soft,
        "hard_count": hard,
        "conjunction_count": conj,
    }


# ============================================================================
# 自测入口
# ============================================================================

if __name__ == "__main__":  # pragma: no cover
    import sys
    if len(sys.argv) >= 3:
        date_str, time_str = sys.argv[1], sys.argv[2]
    elif len(sys.argv) == 2:
        date_str, time_str = sys.argv[1], "12:00"
    else:
        date_str, time_str = "1990-05-15", "14:30"
    loc = "北京"
    chart = build_chart_from_str(date_str, time_str, location=loc)
    print(chart.pretty())