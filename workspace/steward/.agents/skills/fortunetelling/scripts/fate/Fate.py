#!/usr/bin/env python3
"""
运势分析脚本 v4.0

修复大运方向计算问题：
- 阳干（甲丙戊庚壬）+ 男 = 顺行
- 阴干（乙丁己辛癸）+ 男 = 逆行
- 阳干 + 女 = 逆行
- 阴干 + 女 = 顺行
"""

import argparse
from lunar_python import Solar, Lunar, EightChar
from datetime import datetime


class Fate:
    """运势分析类"""

    TIANGAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    DIZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    GANZHI60 = [
        '甲子', '乙丑', '丙寅', '丁卯', '戊辰', '己巳', '庚午', '辛未', '壬申', '癸酉',
        '甲戌', '乙亥', '丙子', '丁丑', '戊寅', '己卯', '庚辰', '辛巳', '壬午', '癸未',
        '甲申', '乙酉', '丙戌', '丁亥', '戊子', '己丑', '庚寅', '辛卯', '壬辰', '癸巳',
        '甲午', '乙未', '丙申', '丁酉', '戊戌', '己亥', '庚子', '辛丑', '壬寅', '癸卯',
        '甲辰', '乙巳', '丙午', '丁未', '戊申', '己酉', '庚戌', '辛亥', '壬子', '癸丑',
        '甲寅', '乙卯', '丙辰', '丁巳', '戊午', '己未', '庚申', '辛酉', '壬戌', '癸亥'
    ]
    WUXING = {
        '甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土', '己': '土',
        '庚': '金', '辛': '金', '壬': '水', '癸': '水'
    }

    @staticmethod
    def get_shishen(rizhu, other):
        m = {
            ('甲', '甲'): '比肩', ('甲', '乙'): '劫财', ('乙', '甲'): '劫财', ('乙', '乙'): '比肩',
            ('丙', '丙'): '比肩', ('丙', '丁'): '劫财', ('丁', '丙'): '劫财', ('丁', '丁'): '比肩',
            ('戊', '戊'): '比肩', ('戊', '己'): '劫财', ('己', '戊'): '劫财', ('己', '己'): '比肩',
            ('庚', '庚'): '比肩', ('庚', '辛'): '劫财', ('辛', '庚'): '劫财', ('辛', '辛'): '比肩',
            ('壬', '壬'): '比肩', ('壬', '癸'): '劫财', ('癸', '壬'): '劫财', ('癸', '癸'): '比肩',
            ('甲', '丙'): '食神', ('甲', '丁'): '伤官', ('乙', '丁'): '食神', ('乙', '丙'): '伤官',
            ('丙', '戊'): '食神', ('丙', '己'): '伤官', ('丁', '己'): '食神', ('丁', '戊'): '伤官',
            ('戊', '庚'): '食神', ('戊', '辛'): '伤官', ('己', '辛'): '食神', ('己', '庚'): '伤官',
            ('庚', '壬'): '食神', ('庚', '癸'): '伤官', ('辛', '癸'): '食神', ('辛', '壬'): '伤官',
            ('壬', '甲'): '食神', ('壬', '乙'): '伤官', ('癸', '乙'): '食神', ('癸', '甲'): '伤官',
            ('甲', '戊'): '偏财', ('甲', '己'): '正财', ('乙', '己'): '偏财', ('乙', '戊'): '正财',
            ('丙', '庚'): '偏财', ('丙', '辛'): '正财', ('丁', '辛'): '偏财', ('丁', '庚'): '正财',
            ('戊', '壬'): '偏财', ('戊', '癸'): '正财', ('己', '癸'): '偏财', ('己', '壬'): '正财',
            ('庚', '甲'): '偏财', ('庚', '乙'): '正财', ('辛', '乙'): '偏财', ('辛', '甲'): '正财',
            ('壬', '丙'): '偏财', ('壬', '丁'): '正财', ('癸', '丁'): '偏财', ('癸', '丙'): '正财',
            ('甲', '庚'): '七杀', ('甲', '辛'): '正官', ('乙', '辛'): '七杀', ('乙', '庚'): '正官',
            ('丙', '壬'): '七杀', ('丙', '癸'): '正官', ('丁', '癸'): '七杀', ('丁', '壬'): '正官',
            ('戊', '甲'): '七杀', ('戊', '乙'): '正官', ('己', '乙'): '七杀', ('己', '甲'): '正官',
            ('庚', '丙'): '七杀', ('庚', '丁'): '正官', ('辛', '丁'): '七杀', ('辛', '丙'): '正官',
            ('壬', '戊'): '七杀', ('壬', '己'): '正官', ('癸', '己'): '七杀', ('癸', '戊'): '正官',
            ('甲', '壬'): '偏印', ('甲', '癸'): '正印', ('乙', '癸'): '偏印', ('乙', '壬'): '正印',
            ('丙', '甲'): '偏印', ('丙', '乙'): '正印', ('丁', '乙'): '偏印', ('丁', '甲'): '正印',
            ('戊', '丙'): '偏印', ('戊', '丁'): '正印', ('己', '丁'): '偏印', ('己', '丙'): '正印',
            ('庚', '戊'): '偏印', ('庚', '己'): '正印', ('辛', '己'): '偏印', ('辛', '戊'): '正印',
            ('壬', '庚'): '偏印', ('壬', '辛'): '正印', ('癸', '辛'): '偏印', ('癸', '庚'): '正印',
        }
        return m.get((rizhu, other), '')

    @staticmethod
    def get_day_ganzhi(y, m, d):
        diff = (datetime(y, m, d) - datetime(2000, 1, 1)).days
        return Fate.GANZHI60[(16 + diff) % 60]

    @staticmethod
    def get_hour_ganzhi(day_gan, hour):
        hz = Fate.DIZHI[(hour + 1) // 2 % 12]
        gi = Fate.TIANGAN.index(day_gan)
        start = (gi % 5) * 2 % 10
        return Fate.TIANGAN[(start + Fate.DIZHI.index(hz)) % 10] + hz

    @staticmethod
    def get_month_ganzhi(year_gan, month):
        mz = Fate.DIZHI[(month + 1) % 12]
        table = {
            '寅': ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'],
            '卯': ['乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸', '甲'],
            '辰': ['丙', '丁', '戊', '己', '庚', '辛', '壬', '癸', '甲', '乙'],
            '巳': ['丁', '戊', '己', '庚', '辛', '壬', '癸', '甲', '乙', '丙'],
            '午': ['戊', '己', '庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁'],
            '未': ['己', '庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁', '戊'],
            '申': ['庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁', '戊', '己'],
            '酉': ['辛', '壬', '癸', '甲', '乙', '丙', '丁', '戊', '己', '庚'],
            '戌': ['壬', '癸', '甲', '乙', '丙', '丁', '戊', '己', '庚', '辛'],
            '亥': ['癸', '甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬'],
            '子': ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'],
            '丑': ['乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸', '甲'],
        }
        return table[mz][Fate.TIANGAN.index(year_gan)] + mz

    @staticmethod
    def is_yang_gan(gan):
        """判断天干阴阳"""
        return gan in ['甲', '丙', '戊', '庚', '壬']

    @staticmethod
    def calc_dayun_direction(year_gan, gender):
        """计算大运方向"""
        yang = Fate.is_yang_gan(year_gan)
        if gender == '男':
            return yang
        else:
            return not yang

    @classmethod
    def analyze_dayun(cls, year, month, day, hour, gender, start_y=2020, end_y=2030):
        """大运流年分析"""
        solar = Solar(year, month, day, hour, 0, 0)
        lunar_obj = solar.getLunar()
        ec = EightChar(lunar_obj)

        year_gan = ec.getYear()[0]
        month_zhi = ec.getMonth()[1]
        rizhu_gan = ec.getDay()[0]

        correct_forward = cls.calc_dayun_direction(year_gan, gender)

        yun_lib = ec.getYun(1 if gender == '女' else 0)
        start_age = yun_lib.getStartYear()
        start_year = year + start_age

        month_gan = ec.getMonth()[0]
        month_zhi = ec.getMonth()[1]
        month_gan_idx = cls.TIANGAN.index(month_gan)
        month_zhi_idx = cls.DIZHI.index(month_zhi)
        step = 1 if correct_forward else -1

        dayun = []
        for i in range(1, 9):
            gan_idx = (month_gan_idx + step * i) % 10
            zhi_idx = (month_zhi_idx + step * i) % 12
            gz = cls.TIANGAN[gan_idx] + cls.DIZHI[zhi_idx]
            start_a = start_age + (i - 1) * 10
            end_a = start_a + 9
            start_yy = start_year + (i - 1) * 10
            dayun.append({
                'age': f"{start_a}-{end_a}岁",
                'years': f"{start_yy}-{start_yy + 9}",
                'ganzhi': gz,
                'wuxing': cls.WUXING.get(cls.TIANGAN[gan_idx], ''),
                'shishen': cls.get_shishen(rizhu_gan, cls.TIANGAN[gan_idx])
            })

        liunian = []
        for d in dayun:
            start_yy = int(d['years'].split('-')[0])
            for i in range(10):
                yy = start_yy + i
                if start_y <= yy <= end_y:
                    ln_gan = cls.TIANGAN[(yy - 4) % 10]
                    ln_zhi = cls.DIZHI[(yy - 4) % 12]
                    gz = ln_gan + ln_zhi
                    shen = cls.get_shishen(rizhu_gan, ln_gan)
                    jx = '吉' if shen in ['正官', '七杀', '正财', '偏财'] else '凶' if shen in ['伤官', '劫财'] else '平'
                    liunian.append({'year': yy, 'ganzhi': gz, 'shishen': shen, 'jixiong': jx})
        liunian.sort(key=lambda x: x['year'])

        return {
            'birth': solar.toString(),
            'rizhu': ec.getDay(),
            'rizhu_gan': rizhu_gan,
            'year_gan': year_gan,
            'gender': gender,
            'yun_start': f"{start_age}岁",
            'yun_dir': '顺' if correct_forward else '逆',
            'dayun': dayun,
            'liunian': liunian
        }

    @classmethod
    def analyze_timing(cls, year, month, day, hour, gender):
        """指定时间点的流年流月流日流时"""
        solar = Solar(year, month, day, hour, 0, 0)
        ec = EightChar(solar.getLunar())
        rizhu_gan = ec.getDay()[0]

        ln_gan = cls.TIANGAN[(year - 4) % 10]
        ln_zhi = cls.DIZHI[(year - 4) % 12]
        lm_ganzhi = cls.get_month_ganzhi(ln_gan, month)
        lr_ganzhi = cls.get_day_ganzhi(year, month, day)
        ls_ganzhi = cls.get_hour_ganzhi(lr_ganzhi[0], hour)

        return {
            'birth': ec.getDay(),
            'target': solar.toString(),
            'rizhu_gan': rizhu_gan,
            'liunian': {'ganzhi': ln_gan + ln_zhi, 'wuxing': cls.WUXING[ln_gan], 'shishen': cls.get_shishen(rizhu_gan, ln_gan)},
            'liuyue': {'ganzhi': lm_ganzhi, 'wuxing': cls.WUXING[lm_ganzhi[0]], 'shishen': cls.get_shishen(rizhu_gan, lm_ganzhi[0])},
            'liuri': {'ganzhi': lr_ganzhi, 'wuxing': cls.WUXING[lr_ganzhi[0]], 'shishen': cls.get_shishen(rizhu_gan, lr_ganzhi[0])},
            'liushi': {'ganzhi': ls_ganzhi, 'wuxing': cls.WUXING[ls_ganzhi[0]], 'shishen': cls.get_shishen(rizhu_gan, ls_ganzhi[0])},
        }

    @staticmethod
    def main():
        parser = argparse.ArgumentParser(description='运势分析 v4.0（修复大运方向）')
        parser.add_argument('year', type=int, help='出生年份')
        parser.add_argument('month', type=int, help='出生月份')
        parser.add_argument('day', type=int, help='出生日期')
        parser.add_argument('hour', type=int, help='出生小时(0-23)')
        parser.add_argument('--gender', default='男', choices=['男', '女'])
        parser.add_argument('--type', default='dayun', choices=['dayun', 'timing'])
        parser.add_argument('--target', help='timing模式: YYYY-MM-DD-HH')
        parser.add_argument('--start-year', type=int, default=2020)
        parser.add_argument('--end-year', type=int, default=2030)

        args = parser.parse_args()

        if args.type == 'timing' and args.target:
            ty, tm, td, th = map(int, args.target.split('-'))
            r = Fate.analyze_timing(ty, tm, td, th, args.gender)
            print("=" * 45)
            print("流年流月流日流时")
            print("=" * 45)
            print(f"日主: {r['birth']}")
            print(f"目标: {r['target']}")
            for label, data in [('流年', r['liunian']), ('流月', r['liuyue']), ('流日', r['liuri']), ('流时', r['liushi'])]:
                print(f"【{label}】{data['ganzhi']} ({data['wuxing']}) {data['shishen']}")
            print("=" * 45)
        else:
            r = Fate.analyze_dayun(args.year, args.month, args.day, args.hour, args.gender, args.start_year, args.end_year)
            print("=" * 50)
            print(f"大运流年（{r['gender']}命）")
            print("=" * 50)
            print(f"出生: {r['birth']}")
            print(f"年干: {r['year_gan']} ({'阳' if Fate.is_yang_gan(r['year_gan']) else '阴'}干)")
            print(f"日柱: {r['rizhu']}")
            print(f"起运: {r['yun_start']} {r['yun_dir']}行")
            print()
            print("【大运】")
            for d in r['dayun'][:5]:
                print(f"  {d['age']}: {d['ganzhi']} ({d['wuxing']}) {d['shishen']}")
            print()
            print("【流年运势】")
            print("-" * 40)
            for ln in r['liunian']:
                print(f"  {ln['year']}年({ln['ganzhi']}): {ln['shishen']} {ln['jixiong']}")
            print("-" * 40)
            print("=" * 50)
