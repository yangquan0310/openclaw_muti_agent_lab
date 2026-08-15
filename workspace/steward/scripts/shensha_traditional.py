#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
传统派神煞查表（参考《渊海子平》《三命通会》《神煞探源》）
覆盖 30+ 主流神煞
"""

GAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

ZHIWEIS = ['年支', '月支', '日支', '时支']
GANWEIS = ['年干', '月干', '日干', '时干']

SIXTY_JIAZI = [
    '甲子', '乙丑', '丙寅', '丁卯', '戊辰', '己巳', '庚午', '辛未', '壬申', '癸酉',
    '甲戌', '乙亥', '丙子', '丁丑', '戊寅', '己卯', '庚辰', '辛巳', '壬午', '癸未',
    '甲申', '乙酉', '丙戌', '丁亥', '戊子', '己丑', '庚寅', '辛卯', '壬辰', '癸巳',
    '甲午', '乙未', '丙申', '丁酉', '戊戌', '己亥', '庚子', '辛丑', '壬寅', '癸卯',
    '甲辰', '乙巳', '丙午', '丁未', '戊申', '己酉', '庚戌', '辛亥', '壬子', '癸丑',
    '甲寅', '乙卯', '丙辰', '丁巳', '戊午', '己未', '庚申', '辛酉', '壬戌', '癸亥'
]

XUN_KONG_MAP = {
    '甲子': ['戌', '亥'], '甲戌': ['申', '酉'],
    '甲申': ['午', '未'], '甲午': ['辰', '巳'],
    '甲辰': ['寅', '卯'], '甲寅': ['子', '丑'],
}

def calc_shensha(year_pillar, month_pillar, day_pillar, hour_pillar):
    yg, yz = year_pillar[0], year_pillar[1]
    mg, mz = month_pillar[0], month_pillar[1]
    dg, dz = day_pillar[0], day_pillar[1]
    hg, hz = hour_pillar[0], hour_pillar[1]
    
    pillars = [year_pillar, month_pillar, day_pillar, hour_pillar]
    zhi_list = [yz, mz, dz, hz]
    gan_list = [yg, mg, dg, hg]
    
    results = []
    
    # 1. 天乙贵人 (日干查)
    tianyi = {
        '甲': ['丑', '未'], '戊': ['丑', '未'],
        '乙': ['子', '申'], '己': ['子', '申'],
        '丙': ['亥', '酉'], '丁': ['亥', '酉'],
        '庚': ['丑', '未'], '辛': ['寅', '午'],
        '壬': ['巳', '卯'], '癸': ['巳', '卯'],
    }
    for zhi, wei in zip(zhi_list, ZHIWEIS):
        if zhi in tianyi.get(dg, []):
            results.append(('天乙贵人', wei, '吉', '遇难呈祥、关键时刻有人帮'))
    
    # 2. 太极贵人 (日干查，主流版本：壬癸蛇兔)
    taiji = {
        '甲': ['子', '午'], '乙': ['子', '午'],
        '丙': ['亥', '酉'], '丁': ['亥', '酉'],
        '戊': ['寅', '申'], '己': ['寅', '申'],
        '庚': ['寅', '午'], '辛': ['寅', '午'],
        '壬': ['巳', '卯'], '癸': ['巳', '卯'],
    }
    for zhi, wei in zip(zhi_list, ZHIWEIS):
        if zhi in taiji.get(dg, []):
            results.append(('太极贵人', wei, '吉', '聪明好学、哲学/玄学天赋'))
    
    # 3. 天德贵人 (月支查日干)
    tiande = {
        '寅': '丁', '卯': '申', '辰': '壬',
        '巳': '癸', '午': '丙', '未': '乙',
        '申': '己', '酉': '辛', '戌': '甲',
        '亥': '丙', '子': '辛', '丑': '乙',
    }
    if dg == tiande.get(mz):
        results.append(('天德贵人', '日干', '吉', '一生有上天保佑，化险为夷'))
    
    # 4. 月德贵人 (月支查日干)
    yuede = {
        '寅': '丙', '午': '丙', '戌': '丙',
        '申': '壬', '子': '壬', '辰': '壬',
        '亥': '甲', '卯': '甲', '未': '甲',
        '巳': '庚', '酉': '庚', '丑': '庚',
    }
    if dg == yuede.get(mz):
        results.append(('月德贵人', '日干', '吉', '一生有贵人照拂'))
    
    # 5. 福星贵人 (日干查)
    fuxing = {
        '甲': ['子', '丑'], '乙': ['子', '丑'],
        '丙': ['丑', '寅'], '丁': ['丑', '寅'],
        '戊': ['丑', '未'], '己': ['丑', '未'],
        '庚': ['申', '酉'], '辛': ['申', '酉'],
        '壬': ['辰', '巳'], '癸': ['辰', '巳'],
    }
    for zhi, wei in zip(zhi_list, ZHIWEIS):
        if zhi in fuxing.get(dg, []):
            results.append(('福星贵人', wei, '吉', '享福、有福气'))
    
    # 6. 文昌贵人 (日干查)
    wenchang = {
        '甲': ['巳', '午'], '乙': ['巳', '午'],
        '丙': ['申', '酉'], '戊': ['申', '酉'],
        '丁': ['亥', '子'], '己': ['亥', '子'],
        '庚': ['寅', '卯'], '辛': ['寅', '卯'],
        '壬': ['辰', '戌', '丑', '未'], '癸': ['辰', '戌', '丑', '未'],
    }
    for zhi, wei in zip(zhi_list, ZHIWEIS):
        if zhi in wenchang.get(dg, []):
            results.append(('文昌贵人', wei, '吉', '读书/考试有天赋'))
    
    # 7. 天厨贵人 (年干查)
    tianchu = {
        '甲': ['巳', '午'], '乙': ['巳', '午'],
        '丙': ['巳', '午'], '丁': ['巳', '午'],
        '戊': ['申', '酉'], '己': ['申', '酉'],
        '庚': ['亥', '子'], '辛': ['亥', '子'],
        '壬': ['寅', '卯'], '癸': ['寅', '卯'],
    }
    for zhi, wei in zip(zhi_list, ZHIWEIS):
        if zhi in tianchu.get(yg, []):
            results.append(('天厨贵人', wei, '吉', '美食缘、有口福'))
    
    # 8. 驿马 (年支查三合冲)
    yima = {
        '寅': '申', '午': '申', '戌': '申',
        '申': '寅', '子': '寅', '辰': '寅',
        '巳': '亥', '酉': '亥', '丑': '亥',
        '亥': '巳', '卯': '巳', '未': '巳',
    }
    for zhi, wei in zip(zhi_list, ZHIWEIS):
        if zhi == yima.get(yz):
            results.append(('驿马', wei, '吉', '出行、多动、突发转机'))
    
    # 9. 桃花 (咸池, 年支查)
    taohua = {
        '寅': '卯', '午': '卯', '戌': '卯',
        '申': '酉', '子': '酉', '辰': '酉',
        '巳': '午', '酉': '午', '丑': '午',
        '亥': '子', '卯': '子', '未': '子',
    }
    for zhi, wei in zip(zhi_list, ZHIWEIS):
        if zhi == taohua.get(yz):
            results.append(('桃花', wei, '中', '异性缘、感情丰富'))
    
    # 10. 华盖 (年支查)
    huagai = {
        '寅': '戌', '午': '戌', '戌': '戌',
        '申': '辰', '子': '辰', '辰': '辰',
        '巳': '丑', '酉': '丑', '丑': '丑',
        '亥': '未', '卯': '未', '未': '未',
    }
    for zhi, wei in zip(zhi_list, ZHIWEIS):
        if zhi == huagai.get(yz):
            results.append(('华盖', wei, '中', '艺术/宗教/哲学天赋，性子孤'))
    
    # 11. 将星 (年支查)
    jiangxing = {
        '寅': '午', '午': '午', '戌': '午',
        '申': '子', '子': '子', '辰': '子',
        '巳': '酉', '酉': '酉', '丑': '酉',
        '亥': '卯', '卯': '卯', '未': '卯',
    }
    for zhi, wei in zip(zhi_list, ZHIWEIS):
        if zhi == jiangxing.get(yz):
            results.append(('将星', wei, '吉', '天生有领导力、能压场'))
    
    # 12. 亡神 (年支查)
    wangshen = {
        '寅': '巳', '午': '巳', '戌': '巳',
        '申': '亥', '子': '亥', '辰': '亥',
        '巳': '申', '酉': '申', '丑': '申',
        '亥': '巳', '卯': '巳', '未': '巳',
    }
    for zhi, wei in zip(zhi_list, ZHIWEIS):
        if zhi == wangshen.get(yz):
            results.append(('亡神', wei, '凶', '城府深、喜怒不形于色'))
    
    # 13. 劫煞 (年支查)
    jiesha = {
        '寅': '亥', '午': '亥', '戌': '亥',
        '申': '巳', '子': '巳', '辰': '巳',
        '巳': '寅', '酉': '寅', '丑': '寅',
        '亥': '申', '卯': '申', '未': '申',
    }
    for zhi, wei in zip(zhi_list, ZHIWEIS):
        if zhi == jiesha.get(yz):
            results.append(('劫煞', wei, '凶', '破财、口舌'))
    
    # 14. 灾煞 (年支查)
    zaisha = {
        '寅': '子', '午': '子', '戌': '子',
        '申': '午', '子': '午', '辰': '午',
        '巳': '卯', '酉': '卯', '丑': '卯',
        '亥': '酉', '卯': '酉', '未': '酉',
    }
    for zhi, wei in zip(zhi_list, ZHIWEIS):
        if zhi == zaisha.get(yz):
            results.append(('灾煞', wei, '凶', '突发意外、血光'))
    
    # 15. 孤辰 (年支查)
    guchen = {
        '寅': '巳', '卯': '巳', '辰': '巳',
        '巳': '申', '午': '申', '未': '申',
        '申': '亥', '酉': '亥', '戌': '亥',
        '亥': '寅', '子': '寅', '丑': '寅',
    }
    for zhi, wei in zip(zhi_list, ZHIWEIS):
        if zhi == guchen.get(yz):
            results.append(('孤辰', wei, '凶', '性子独立、不爱合群'))
    
    # 16. 寡宿 (年支查)
    guasu = {
        '寅': '丑', '卯': '丑', '辰': '丑',
        '巳': '辰', '午': '辰', '未': '辰',
        '申': '未', '酉': '未', '戌': '未',
        '亥': '戌', '子': '戌', '丑': '戌',
    }
    for zhi, wei in zip(zhi_list, ZHIWEIS):
        if zhi == guasu.get(yz):
            results.append(('寡宿', wei, '凶', '不易妥协、婚姻晚'))
    
    # 17. 丧门 (年支查)
    sangmen = {
        '寅': '亥', '午': '亥', '戌': '亥',
        '申': '巳', '子': '巳', '辰': '巳',
        '巳': '寅', '酉': '寅', '丑': '寅',
        '亥': '申', '卯': '申', '未': '申',
    }
    for zhi, wei in zip(zhi_list, ZHIWEIS):
        if zhi == sangmen.get(yz):
            results.append(('丧门', wei, '凶', '家人有伤病/离世可能'))
    
    # 18. 吊客 (年支查)
    diaoke = {
        '寅': '巳', '午': '巳', '戌': '巳',
        '申': '亥', '子': '亥', '辰': '亥',
        '巳': '申', '酉': '申', '丑': '申',
        '亥': '寅', '卯': '寅', '未': '寅',
    }
    for zhi, wei in zip(zhi_list, ZHIWEIS):
        if zhi == diaoke.get(yz):
            results.append(('吊客', wei, '凶', '哀痛、情感细腻'))
    
    # 19. 披麻 (年支查)
    pima = {
        '寅': '子', '午': '子', '戌': '子',
        '申': '辰', '子': '辰', '辰': '辰',
        '巳': '酉', '酉': '酉', '丑': '酉',
        '亥': '卯', '卯': '卯', '未': '卯',
    }
    for zhi, wei in zip(zhi_list, ZHIWEIS):
        if zhi == pima.get(yz):
            results.append(('披麻', wei, '凶', '与丧事相关'))
    
    # 20. 飞刃 (日干查)
    feiren = {
        '甲': '卯', '乙': '辰', '丙': '午',
        '丁': '未', '戊': '午', '己': '未',
        '庚': '酉', '辛': '戌', '壬': '子',
        '癸': '巳',
    }
    for zhi, wei in zip(zhi_list, ZHIWEIS):
        if zhi == feiren.get(dg):
            results.append(('飞刃', wei, '凶', '脾气暴、容易冲动'))
    
    # 21. 金神 (日柱查)
    jinshen_days = ['乙丑', '己巳', '癸酉']
    if day_pillar in jinshen_days:
        results.append(('金神', '日柱', '中', '刚毅果断、杀伐决断'))
    
    # 22. 国印贵人 (年干查)
    guoyin = {
        '甲': '戌', '乙': '亥', '丙': '子',
        '丁': '丑', '戊': '子', '己': '丑',
        '庚': '寅', '辛': '卯', '壬': '辰',
        '癸': '巳',
    }
    for zhi, wei in zip(zhi_list, ZHIWEIS):
        if zhi == guoyin.get(yg):
            results.append(('国印贵人', wei, '吉', '适合行政管理、签章'))
    
    # 23. 空亡 (日柱查)
    idx = SIXTY_JIAZI.index(day_pillar)
    xun_start_idx = (idx // 10) * 10
    xun = SIXTY_JIAZI[xun_start_idx][:2]
    kong_zhi = XUN_KONG_MAP.get(xun, [])
    for zhi, wei in zip(zhi_list, ZHIWEIS):
        if zhi in kong_zhi:
            results.append(('空亡', wei, '凶', '内心有"空"感、佛系'))
    
    # 24. 退神 (日干查日支)
    tuishen = {'甲': '申', '乙': '酉', '丙': '戌', '丁': '亥',
               '戊': '子', '己': '丑', '庚': '寅', '辛': '卯',
               '壬': '辰', '癸': '巳'}
    for zhi, wei in zip(zhi_list, ZHIWEIS):
        if zhi == tuishen.get(dg):
            results.append(('退神', wei, '凶', '愿意退让、随缘'))
    
    # 25. 德秀贵人 (日干配支)
    # 阴生阴、阳生阳、阳生阴 → 德秀
    # 简化：日干见月支三合
    sanhe = {
        '亥': ['亥', '卯', '未'], '卯': ['亥', '卯', '未'], '未': ['亥', '卯', '未'],
        '申': ['申', '子', '辰'], '子': ['申', '子', '辰'], '辰': ['申', '子', '辰'],
        '巳': ['巳', '酉', '丑'], '酉': ['巳', '酉', '丑'], '丑': ['巳', '酉', '丑'],
        '寅': ['寅', '午', '戌'], '午': ['寅', '午', '戌'], '戌': ['寅', '午', '戌'],
    }
    for zhi, wei in zip(zhi_list, ZHIWEIS):
        if zhi in sanhe.get(mz, []):
            results.append(('德秀贵人', wei, '吉', '人品好、德行端正'))
    
    # 26. 禄神 (日干查)
    lushen = {
        '甲': '寅', '乙': '卯', '丙': '巳', '丁': '午',
        '戊': '巳', '己': '午', '庚': '申', '辛': '酉',
        '壬': '亥', '癸': '子',
    }
    for zhi, wei in zip(zhi_list, ZHIWEIS):
        if zhi == lushen.get(dg):
            results.append(('禄神', wei, '吉', '衣禄无忧、收入稳定'))
    
    # 27. 羊刃 (日干查)
    yangren = {
        '甲': '卯', '乙': '辰', '丙': '午', '丁': '未',
        '戊': '午', '己': '未', '庚': '酉', '辛': '戌',
        '壬': '子', '癸': '丑',
    }
    for zhi, wei in zip(zhi_list, ZHIWEIS):
        if zhi == yangren.get(dg):
            results.append(('羊刃', wei, '凶', '性子烈、有魄力也有祸'))
    
    # 28. 天赦 (日柱查 - 四季天赦)
    tianshe_days = ['戊寅', '甲午', '戊申', '甲子']
    if day_pillar in tianshe_days:
        results.append(('天赦', '日柱', '吉', '一生有赦免之命，遇难有解'))
    
    # 29. 红鸾 (年支查)
    hongluan = {
        '子': '卯', '丑': '寅', '寅': '丑', '卯': '子',
        '辰': '亥', '巳': '戌', '午': '酉', '未': '申',
        '申': '未', '酉': '午', '戌': '巳', '亥': '辰',
    }
    for zhi, wei in zip(zhi_list, ZHIWEIS):
        if zhi == hongluan.get(yz):
            results.append(('红鸾', wei, '吉', '婚姻喜庆、异性缘'))
    
    # 30. 天喜 (年支查 - 红鸾对冲)
    tianxi = {
        '子': '酉', '丑': '申', '寅': '未', '卯': '午',
        '辰': '巳', '巳': '辰', '午': '卯', '未': '寅',
        '申': '丑', '酉': '子', '戌': '亥', '亥': '戌',
    }
    for zhi, wei in zip(zhi_list, ZHIWEIS):
        if zhi == tianxi.get(yz):
            results.append(('天喜', wei, '吉', '喜事连连、人缘和合'))
    
    return results


def print_report(name, year_pillar, month_pillar, day_pillar, hour_pillar):
    print(f"==================================================")
    print(f"【传统派神煞】{name}")
    print(f"四柱：{year_pillar} {month_pillar} {day_pillar} {hour_pillar}")
    print(f"==================================================")
    
    results = calc_shensha(year_pillar, month_pillar, day_pillar, hour_pillar)
    
    ji = [r for r in results if r[2] == '吉']
    zhong = [r for r in results if r[2] == '中']
    xiong = [r for r in results if r[2] == '凶']
    
    print(f"\n共 {len(results)} 个神煞：吉 {len(ji)} / 中 {len(zhong)} / 凶 {len(xiong)}\n")
    
    cols = ['年支', '月支', '日支', '时支', '日干', '日柱']
    for col in cols:
        items = [r for r in results if r[1] == col]
        if items:
            print(f"■ {col}")
            for name, _, level, desc in items:
                print(f"  [{level}] {name} - {desc}")
            print()
    
    print(f"\n【吉神】({len(ji)} 个)")
    for name, wei, _, desc in ji:
        print(f"  ✓ {name} ({wei}) - {desc}")
    
    print(f"\n【中性】({len(zhong)} 个)")
    for name, wei, _, desc in zhong:
        print(f"  ◇ {name} ({wei}) - {desc}")
    
    print(f"\n【凶神】({len(xiong)} 个)")
    for name, wei, _, desc in xiong:
        print(f"  ✗ {name} ({wei}) - {desc}")


if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 5:
        # 四柱模式
        name = sys.argv[1] if len(sys.argv) > 5 else ""
        yp, mp, dp, hp = sys.argv[-4:]
        print_report(name, yp, mp, dp, hp)
    else:
        # 默认女命
        print_report("女命 1999-05-21 18:00", "己卯", "己巳", "癸酉", "辛酉")
