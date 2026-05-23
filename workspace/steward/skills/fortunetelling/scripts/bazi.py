#!/usr/bin/env python3
"""
八字排盘器 v3.0

使用 lunar_python 专业库进行精确八字排盘。
支持阳历和阴历输入，自动处理节气、闰月等复杂情况。
"""

import argparse
from lunar_python import Solar, Lunar, EightChar

# 天干
TIANGAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

# 地支
DIZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

# 五行
WUXING = {
    '甲': '木', '乙': '木',
    '丙': '火', '丁': '火',
    '戊': '土', '己': '土',
    '庚': '金', '辛': '金',
    '壬': '水', '癸': '水'
}

# 地支对应五行
DIZHI_WUXING = {
    '子': '水', '丑': '土', '寅': '木', '卯': '木',
    '辰': '土', '巳': '火', '午': '火', '未': '土',
    '申': '金', '酉': '金', '戌': '土', '亥': '水'
}


def get_wuxing(ganzhi: str) -> str:
    """获取干支的五行"""
    gan = ganzhi[0]
    zhi = ganzhi[1]
    return WUXING.get(gan, '') + DIZHI_WUXING.get(zhi, '')


def analyze_bazi(year: int, month: int, day: int, hour: int,
                 gender: str = '男', is_lunar: bool = False) -> dict:
    """
    分析八字
    
    Args:
        year: 年
        month: 月
        day: 日
        hour: 小时(0-23)
        gender: 性别
        is_lunar: 输入是否为阴历
    """
    result = {}
    
    if is_lunar:
        # 阴历直接创建Lunar对象
        lunar = Lunar(year, month, day, hour, 0, 0)
        solar = lunar.getSolar()
    else:
        # 阳历创建Solar对象
        solar = Solar(year, month, day, hour, 0, 0)
        lunar = solar.getLunar()
    
    # 使用专业库计算八字
    ec = EightChar(lunar)
    
    result['year'] = ec.getYear()
    result['month'] = ec.getMonth()
    result['day'] = ec.getDay()
    result['hour'] = ec.getTime()
    
    result['wuxing'] = {
        'year': get_wuxing(result['year']),
        'month': get_wuxing(result['month']),
        'day': get_wuxing(result['day']),
        'hour': get_wuxing(result['hour'])
    }
    
    result['rizhu'] = result['day'][0]
    result['rizhu_wuxing'] = WUXING[result['day'][0]]
    result['gender'] = gender
    
    # 阳历和阴历信息
    result['solar'] = solar.toString()
    result['lunar'] = lunar.toString()
    
    return result


def print_bazi(bazi: dict):
    """打印八字排盘"""
    print("=" * 40)
    print("八字排盘")
    print("=" * 40)
    print(f"阳历: {bazi['solar']}")
    print(f"阴历: {bazi['lunar']}")
    print("-" * 40)
    print(f"年柱: {bazi['year']}  {bazi['wuxing']['year']}")
    print(f"月柱: {bazi['month']}  {bazi['wuxing']['month']}")
    print(f"日柱: {bazi['day']}  {bazi['wuxing']['day']}")
    print(f"时柱: {bazi['hour']}  {bazi['wuxing']['hour']}")
    print("-" * 40)
    print(f"日主: {bazi['rizhu']}（{bazi['rizhu_wuxing']}）")
    print(f"性别: {bazi['gender']}")
    print("=" * 40)


def main():
    parser = argparse.ArgumentParser(description='八字排盘 v3.0（使用lunar_python库）')
    parser.add_argument('year', type=int, help='年份')
    parser.add_argument('month', type=int, help='月份')
    parser.add_argument('day', type=int, help='日期')
    parser.add_argument('hour', type=int, help='小时(0-23)')
    parser.add_argument('--gender', default='男', choices=['男', '女'], help='性别')
    parser.add_argument('--lunar', action='store_true', help='输入为阴历日期')
    
    args = parser.parse_args()
    
    bazi = analyze_bazi(args.year, args.month, args.day, args.hour,
                       args.gender, args.lunar)
    print_bazi(bazi)


if __name__ == '__main__':
    main()
