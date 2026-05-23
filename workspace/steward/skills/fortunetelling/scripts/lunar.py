#!/usr/bin/env python3
"""
阴历转公历转换器

将阴历日期转换为公历日期。
"""

import argparse
from datetime import datetime, timedelta


# 阴历月份天数（平年）
LUNAR_MONTHS = [0, 31, 29, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# 闰年月份（阴历）
LUNAR_LEAP_MONTHS = {
    1990: 8, 1992: 2, 1993: 3, 1995: 8, 1998: 5,
    2001: 4, 2004: 2, 2006: 7, 2009: 5, 2012: 4,
    2014: 9, 2017: 6, 2020: 4, 2023: 2, 2025: 6
}

# 天干
TIANGAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

# 地支
DIZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']


def lunar_to_solar(year: int, month: int, day: int) -> datetime:
    """
    将阴历日期转换为公历日期

    Args:
        year: 阴历年（4位数）
        month: 阴历月
        day: 阴历日

    Returns:
        公历日期
    """
    # 简单近似算法：阴历比公历晚约11-12天
    # 这里使用简化算法，实际应用需要查表
    base_solar = datetime(year, 1, 1)
    lunar_days = sum(LUNAR_MONTHS[:month]) + day - 1

    # 粗略估计：每阴历月平均29.53天
    offset = int(lunar_days * 29.53)

    # 调整：阴历比公历晚约11-13天
    solar = base_solar + timedelta(days=offset + 11)

    return solar


def get_lunar_ganzhi(year: int, month: int = 1, day: int = 1) -> tuple:
    """
    计算干支纪年

    Args:
        year: 年份
        month: 月份
        day: 日期

    Returns:
        (天干, 地支)
    """
    # 计算年干支
    year_gan = TIANGAN[(year - 4) % 10]
    year_zhi = DIZHI[(year - 4) % 12]

    # 计算月干支
    month_gan = TIANGAN[(year * 12 + month + 3) % 10]
    month_zhi = DIZHI[(month + 1) % 12]

    # 计算日干支（简化）
    base_day = datetime(2000, 1, 1)
    base_ganzhi = (37, 0)  # 2000年1月1日为庚辰
    days_diff = (datetime(year, month, day) - base_day).days
    day_gan = TIANGAN[(base_ganzhi[0] + days_diff) % 10]
    day_zhi = DIZHI[(base_ganzhi[1] + days_diff) % 12]

    return (year_gan + year_zhi, month_gan + month_zhi, day_gan + day_zhi)


def get_hour_ganzhi(day_gan: str, hour: int) -> str:
    """
    计算时干支

    Args:
        day_gan: 日天干
        hour: 小时(0-23)

    Returns:
        时干支
    """
    # 时支
    hour_zhi = DIZHI[(hour + 1) // 2 % 12]

    # 时干：日干配合表
    day_gan_idx = TIANGAN.index(day_gan)
    hour_gan_idx = (day_gan_idx * 2 + (hour + 1) // 2) % 10
    hour_gan = TIANGAN[hour_gan_idx]

    return hour_gan + hour_zhi


def main():
    parser = argparse.ArgumentParser(description='阴历转公历')
    parser.add_argument('year', type=int, help='阴历年')
    parser.add_argument('month', type=int, help='阴历月')
    parser.add_argument('day', type=int, help='阴历日')
    parser.add_argument('--hour', type=int, default=12, help='出生小时')

    args = parser.parse_args()

    solar = lunar_to_solar(args.year, args.month, args.day)
    ganzhi = get_lunar_ganzhi(args.year, args.month, args.day)

    print(f"阴历: {args.year}年{args.month}月{args.day}日")
    print(f"公历: {solar.strftime('%Y年%m月%d日')}")
    print(f"年柱: {ganzhi[0]}")
    print(f"月柱: {ganzhi[1]}")
    print(f"日柱: {ganzhi[2]}")
    print(f"时柱: {get_hour_ganzhi(ganzhi[2][0], args.hour)}")


if __name__ == '__main__':
    main()
