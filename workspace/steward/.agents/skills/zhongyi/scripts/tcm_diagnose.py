#!/usr/bin/env python3
"""tcm_diagnose.py — 中医辨证核心推理引擎（v1）

设计原则（v1 规则匹配）：
  1. 输入用户文本症状 → 拆分为特征（主诉、舌、脉、寒热、出汗、二便、情志、部位）
  2. 对每个证型按"症状→证型"关键词计算 score
  3. 引入 bagang（八纲）冲突惩罚（e.g. 用户说"恶寒重"则对热证大幅扣分）
  4. 取 Top-N 候选 → 映射主方（formula_id）
  5. 输出 JSON：含 bagang / 候选证型 / 主方 / disclaimer

⚠️ 本模块仅供学术参考与工程演示，不构成医疗建议。
数据源见 references/zhongyi-zhenduan.md 与 references/zhongyi-fangji.md。
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# ============================================================================
# 数据：证型表（与 references/zhongyi-zhenduan.md 同步）
# ============================================================================
# 每个 zheng 包含 ID、八纲归类、主症特征关键词、舌脉关键词、主方 ID
# 关键词权重：主症 3 分；舌象/脉象 2 分；部位/寒热/汗等 1 分

ZHENG_TABLE: List[Dict] = [
    # ===== 外感类 =====
    {
        "id": "Z-外感-001", "name": "风寒感冒",
        "bagang": {"表": True, "实": True, "寒": True, "阳": True},
        "keywords": {
            "high": ["恶寒重", "发热轻", "无汗", "鼻塞", "流清涕", "咳嗽", "痰白稀", "脉浮紧", "苔薄白"],
            "mid":  ["头身痛", "关节酸痛", "身痛", "头痛", "脉浮", "恶寒"],
            "low":  ["怕冷", "怕风"],
        },
        "tongue": "舌淡红，苔薄白润",
        "pulse":  "浮紧",
        "category": "外感",
        "main_formula": "F-解表-001",
        "alt_formulas": ["F-解表-002"],
        "source": "中医诊断学第二章·伤寒论",
    },
    {
        "id": "Z-外感-002", "name": "风热感冒",
        "bagang": {"表": True, "实": True, "热": True, "阳": True},
        "keywords": {
            "high": ["咽痛", "咽干", "口渴", "咳嗽痰黄", "痰黄稠", "鼻塞流黄", "脉浮数", "苔薄黄"],
            "mid":  ["发热重", "恶寒轻", "舌尖红", "头痛", "口干"],
            "low":  ["发热", "出汗"],
        },
        "tongue": "舌尖红，苔薄黄",
        "pulse":  "浮数",
        "category": "外感",
        "main_formula": "F-解表-003",
        "alt_formulas": ["F-解表-004"],
        "source": "中医诊断学第二章·温病条辨",
    },
    {
        "id": "Z-外感-003", "name": "风燥感冒（温燥）",
        "bagang": {"表": True, "实": True, "燥": True, "阳": True},
        "keywords": {
            "high": ["干咳少痰", "干咳", "无痰", "口鼻干燥", "咽干", "痰黏", "痰黏难咯", "苔干"],
            "mid":  ["发热微恶风寒", "微恶寒", "少津", "脉浮细数"],
            "low":  ["咳嗽", "秋季"],
        },
        "tongue": "舌红少津，苔薄白干",
        "pulse":  "浮细数",
        "category": "外感",
        "main_formula": "F-补-013",
        "alt_formulas": [],
        "source": "中医诊断学第二章·温病条辨·秋燥",
    },
    {
        "id": "Z-外感-004", "name": "暑湿感冒",
        "bagang": {"表": True, "实": True, "暑湿": True, "阳": True},
        "keywords": {
            "high": ["夏季", "暑湿", "发热汗出不解", "汗出热不解", "头重如裹", "身重倦怠", "胸闷", "苔黄腻"],
            "mid":  ["呕恶", "纳呆", "腹泻", "脉濡数"],
            "low":  ["发热", "疲倦", "倦怠"],
        },
        "tongue": "舌红，苔黄腻",
        "pulse":  "濡数",
        "category": "外感",
        "main_formula": "F-暑湿-001",
        "alt_formulas": ["F-暑湿-002"],
        "source": "中医诊断学第二章·温病条辨",
    },

    # ===== 心系类 =====
    {
        "id": "Z-心-001", "name": "心气虚",
        "bagang": {"里": True, "虚": True, "气虚": True},
        "keywords": {
            "high": ["心悸气短", "心悸", "气短", "自汗", "神疲乏力", "面色㿠白"],
            "mid":  ["活动时加重", "活动后加重", "语低声怯", "脉虚"],
            "low":  ["乏力", "疲倦"],
        },
        "tongue": "舌淡，苔薄白",
        "pulse":  "虚细",
        "category": "心系",
        "main_formula": "F-补益-005",
        "alt_formulas": ["F-补益-001"],
        "source": "中医诊断学第四章·方剂学补益剂",
    },
    {
        "id": "Z-心-002", "name": "心血虚",
        "bagang": {"里": True, "虚": True, "血虚": True},
        "keywords": {
            "high": ["失眠多梦", "心悸", "眩晕", "健忘", "面色无华", "唇甲色淡"],
            "mid":  ["脉细", "舌淡", "失眠"],
            "low":  ["多梦"],
        },
        "tongue": "舌淡，苔薄白",
        "pulse":  "细弱",
        "category": "心系",
        "main_formula": "F-补益-005",
        "alt_formulas": ["F-补-009"],
        "source": "中医诊断学第四章·金匮要略",
    },
    {
        "id": "Z-心-003", "name": "心火旺",
        "bagang": {"里": True, "实": True, "热": True, "阳": True},
        "keywords": {
            "high": ["心烦", "口舌生疮", "舌尖红", "小便短赤", "小便短赤涩痛", "口渴"],
            "mid":  ["失眠", "脉数"],
            "low":  ["口苦", "烦躁"],
        },
        "tongue": "舌尖红，苔黄",
        "pulse":  "数",
        "category": "心系",
        "main_formula": "F-清热-003",
        "alt_formulas": [],
        "source": "中医诊断学第四章·小儿药证直诀",
    },
    {
        "id": "Z-心-004", "name": "心阳虚",
        "bagang": {"里": True, "虚": True, "寒": True, "阴": True},
        "keywords": {
            "high": ["心悸怔忡", "心悸", "胸闷气短", "形寒肢冷", "面色苍白", "唇甲青紫"],
            "mid":  ["脉沉细无力", "脉结代", "舌淡胖"],
            "low":  ["畏寒"],
        },
        "tongue": "舌淡胖嫩，苔白滑",
        "pulse":  "沉细无力或结代",
        "category": "心系",
        "main_formula": "F-温里-003",
        "alt_formulas": ["F-温里-001"],
        "source": "中医诊断学第四章·伤寒论",
    },

    # ===== 肝系类 =====
    {
        "id": "Z-肝-001", "name": "肝阳上亢",
        "bagang": {"里": True, "本虚标实": True, "阳亢": True},
        "keywords": {
            "high": ["头晕胀痛", "面红目赤", "耳鸣如潮", "急躁易怒", "口苦", "腰膝酸软", "脉弦"],
            "mid":  ["头痛", "口苦", "失眠多梦", "舌红"],
            "low":  ["眩晕", "易怒"],
        },
        "tongue": "舌红，苔黄",
        "pulse":  "弦细数",
        "category": "肝系",
        "main_formula": "F-补-014",
        "alt_formulas": [],
        "source": "中医诊断学第四章·胡光慈中医内科杂病证治新义",
    },
    {
        "id": "Z-肝-002", "name": "肝气郁结",
        "bagang": {"里": True, "实": True, "气滞": True},
        "keywords": {
            "high": ["情志抑郁", "急躁易怒", "胸胁胀闷", "胁肋胀痛", "善太息", "梅核气", "咽部异物感", "脉弦"],
            "mid":  ["少腹胀痛", "月经不调", "乳房胀痛", "胁痛", "叹气"],
            "low":  ["烦躁", "情绪"],
        },
        "tongue": "舌淡红，苔薄白",
        "pulse":  "弦",
        "category": "肝系",
        "main_formula": "F-理气-001",
        "alt_formulas": ["F-补-006"],
        "source": "中医诊断学第四章·景岳全书",
    },
    {
        "id": "Z-肝-003", "name": "肝火旺",
        "bagang": {"里": True, "实": True, "热": True, "阳": True},
        "keywords": {
            "high": ["胁肋灼痛", "面红目赤", "耳鸣如潮", "口苦口干", "急躁易怒", "便秘尿黄", "脉弦数"],
            "mid":  ["头痛眩晕", "舌红", "苔黄"],
            "low":  ["口苦"],
        },
        "tongue": "舌红，苔黄",
        "pulse":  "弦数",
        "category": "肝系",
        "main_formula": "F-清热-004",
        "alt_formulas": [],
        "source": "中医诊断学第四章·医方集解",
    },
    {
        "id": "Z-肝-004", "name": "肝血虚",
        "bagang": {"里": True, "虚": True, "血虚": True},
        "keywords": {
            "high": ["眩晕耳鸣", "目涩", "夜盲", "爪甲不荣", "面色无华", "肢体麻木", "筋脉拘挛"],
            "mid":  ["月经量少", "舌淡", "脉弦细"],
            "low":  ["月经量少色淡"],
        },
        "tongue": "舌淡，苔薄白",
        "pulse":  "弦细",
        "category": "肝系",
        "main_formula": "F-补益-002",
        "alt_formulas": [],
        "source": "中医诊断学第四章·仙授理伤续断秘方",
    },

    # ===== 脾系类 =====
    {
        "id": "Z-脾-001", "name": "脾气虚",
        "bagang": {"里": True, "虚": True, "气虚": True},
        "keywords": {
            "high": ["纳少", "腹胀", "食后胀", "食后腹胀", "便溏", "神疲乏力", "少气懒言", "面色萎黄", "舌淡胖"],
            "mid":  ["齿痕", "脉濡缓", "脉弱", "苔白"],
            "low":  ["疲倦", "乏力"],
        },
        "tongue": "舌淡胖有齿痕，苔白",
        "pulse":  "濡缓",
        "category": "脾系",
        "main_formula": "F-补益-001",
        "alt_formulas": ["F-补益-004"],
        "source": "中医诊断学第四章·太平惠民和剂局方",
    },
    {
        "id": "Z-脾-002", "name": "脾阳虚",
        "bagang": {"里": True, "虚": True, "寒": True, "阴": True},
        "keywords": {
            "high": ["脘腹冷痛", "喜温喜按", "大便清稀", "完谷不化", "四肢不温", "舌淡胖"],
            "mid":  ["脉沉迟", "苔白滑", "畏寒"],
            "low":  ["腹胀", "纳呆"],
        },
        "tongue": "舌淡胖，苔白滑",
        "pulse":  "沉迟无力",
        "category": "脾系",
        "main_formula": "F-温里-001",
        "alt_formulas": [],
        "source": "中医诊断学第四章·伤寒论",
    },
    {
        "id": "Z-脾-003", "name": "脾虚湿困",
        "bagang": {"里": True, "虚": True, "湿": True},
        "keywords": {
            "high": ["脘腹胀闷", "纳呆便溏", "肢体困重", "倦怠嗜睡", "头重如裹", "苔白腻"],
            "mid":  ["舌淡胖", "脉濡缓", "脉濡"],
            "low":  ["疲倦", "嗜睡"],
        },
        "tongue": "舌淡胖，苔白腻",
        "pulse":  "濡缓",
        "category": "脾系",
        "main_formula": "F-补益-004",
        "alt_formulas": ["F-祛湿-002"],
        "source": "中医诊断学第四章·太平惠民和剂局方",
    },
    {
        "id": "Z-脾-004", "name": "脾不统血",
        "bagang": {"里": True, "虚": True, "气不摄血": True},
        "keywords": {
            "high": ["皮下紫癜", "鼻衄", "齿衄", "崩漏", "月经量多色淡", "食少便溏", "神疲乏力"],
            "mid":  ["舌淡胖", "脉细弱"],
            "low":  ["出血"],
        },
        "tongue": "舌淡胖，苔白",
        "pulse":  "细弱",
        "category": "脾系",
        "main_formula": "F-补益-005",
        "alt_formulas": [],
        "source": "中医诊断学第四章·济生方",
    },
    {
        "id": "Z-脾-005", "name": "湿热蕴脾",
        "bagang": {"里": True, "实": True, "热": True, "湿": True},
        "keywords": {
            "high": ["脘腹胀满", "恶心呕吐", "口苦黏腻", "身重困倦", "尿黄", "大便溏", "下利脓血", "苔黄腻", "脉濡数"],
            "mid":  ["舌红", "纳呆"],
            "low":  ["口苦"],
        },
        "tongue": "舌红，苔黄腻",
        "pulse":  "濡数",
        "category": "脾系",
        "main_formula": "F-清热-002",
        "alt_formulas": ["F-清热-004"],
        "source": "中医诊断学第四章·伤寒论",
    },

    # ===== 肺系类 =====
    {
        "id": "Z-肺-001", "name": "肺气虚",
        "bagang": {"里": True, "虚": True, "气虚": True},
        "keywords": {
            "high": ["咳嗽气短", "痰清稀", "语低声怯", "自汗畏风", "易感冒", "神疲乏力"],
            "mid":  ["脉虚弱", "舌淡"],
            "low":  ["气短"],
        },
        "tongue": "舌淡，苔薄白",
        "pulse":  "虚弱",
        "category": "肺系",
        "main_formula": "F-补益-004",
        "alt_formulas": ["F-补益-001"],
        "source": "中医诊断学第四章·方剂学",
    },
    {
        "id": "Z-肺-002", "name": "肺阴虚",
        "bagang": {"里": True, "虚": True, "阴虚": True, "热": True},
        "keywords": {
            "high": ["干咳少痰", "痰中带血", "口干咽燥", "声音嘶哑", "潮热盗汗", "颧红", "舌红少津", "少苔"],
            "mid":  ["脉细数", "无苔", "裂纹"],
            "low":  ["咳嗽", "盗汗"],
        },
        "tongue": "舌红少津，少苔或无苔",
        "pulse":  "细数",
        "category": "肺系",
        "main_formula": "F-补-013",
        "alt_formulas": [],
        "source": "中医诊断学第四章·温病条辨",
    },
    {
        "id": "Z-肺-003", "name": "风寒犯肺",
        "bagang": {"表": True, "实": True, "寒": True, "阳": True},
        "keywords": {
            "high": ["咳嗽声重", "咳痰稀薄", "痰白", "鼻塞流清", "脉浮紧"],
            "mid":  ["恶寒发热", "苔薄白", "头痛"],
            "low":  ["咳嗽", "气急"],
        },
        "tongue": "舌淡红，苔薄白",
        "pulse":  "浮紧",
        "category": "肺系",
        "main_formula": "F-解表-001",
        "alt_formulas": [],
        "source": "中医诊断学第四章·医学心悟",
    },
    {
        "id": "Z-肺-004", "name": "风热犯肺",
        "bagang": {"表里": True, "实": True, "热": True, "阳": True},
        "keywords": {
            "high": ["咳嗽频剧", "咳声嘶哑", "痰黄黏稠", "咽痛", "口渴", "鼻流黄涕", "脉浮数"],
            "mid":  ["舌红", "苔薄黄"],
            "low":  ["咳嗽"],
        },
        "tongue": "舌红，苔薄黄",
        "pulse":  "浮数",
        "category": "肺系",
        "main_formula": "F-解表-004",
        "alt_formulas": ["F-解表-003"],
        "source": "中医诊断学第四章·温病条辨",
    },
    {
        "id": "Z-肺-005", "name": "痰湿阻肺",
        "bagang": {"里": True, "实": True, "痰湿": True},
        "keywords": {
            "high": ["咳嗽痰多", "痰白黏稠", "痰白黏稠易咯", "胸闷脘痞", "苔白腻"],
            "mid":  ["纳呆", "身重", "脉滑"],
            "low":  ["咳嗽"],
        },
        "tongue": "舌淡胖，苔白腻",
        "pulse":  "滑",
        "category": "肺系",
        "main_formula": "F-祛湿-003",
        "alt_formulas": [],
        "source": "中医诊断学第四章·太平惠民和剂局方",
    },

    # ===== 肾系类 =====
    {
        "id": "Z-肾-001", "name": "肾阴虚",
        "bagang": {"里": True, "虚": True, "阴虚": True, "热": True},
        "keywords": {
            "high": ["腰膝酸软", "头晕耳鸣", "潮热盗汗", "五心烦热", "失眠多梦", "口干咽燥", "舌红少苔", "脉细数"],
            "mid":  ["遗精", "月经量少", "裂纹"],
            "low":  ["腰酸", "耳鸣"],
        },
        "tongue": "舌红少苔或裂纹",
        "pulse":  "细数",
        "category": "肾系",
        "main_formula": "F-补益-003",
        "alt_formulas": ["F-补-008"],
        "source": "中医诊断学第四章·小儿药证直诀",
    },
    {
        "id": "Z-肾-002", "name": "肾阳虚",
        "bagang": {"里": True, "虚": True, "寒": True, "阴": True},
        "keywords": {
            "high": ["腰膝酸冷", "腰膝冷痛", "畏寒肢冷", "面色㿠白", "精神萎靡", "小便清长", "夜尿多", "浮肿", "舌淡胖"],
            "mid":  ["脉沉细", "脉沉迟", "苔白"],
            "low":  ["畏寒", "腰痛"],
        },
        "tongue": "舌淡胖，苔白",
        "pulse":  "沉细无力",
        "category": "肾系",
        "main_formula": "F-温里-003",
        "alt_formulas": [],
        "source": "中医诊断学第四章·金匮要略",
    },
    {
        "id": "Z-肾-003", "name": "肾气虚",
        "bagang": {"里": True, "虚": True, "气虚": True},
        "keywords": {
            "high": ["腰膝酸软", "听力减退", "小便频数清长", "小便频数", "夜尿多", "滑精", "早泄", "带下清稀"],
            "mid":  ["脉沉弱", "舌淡", "苔白"],
            "low":  ["腰痛", "尿频"],
        },
        "tongue": "舌淡，苔白",
        "pulse":  "沉弱",
        "category": "肾系",
        "main_formula": "F-温里-003",
        "alt_formulas": [],
        "source": "中医诊断学第四章·方剂学",
    },
    {
        "id": "Z-肾-004", "name": "肾精不足",
        "bagang": {"里": True, "虚": True, "精亏": True},
        "keywords": {
            "high": ["发育迟缓", "五迟", "五软", "早衰", "耳鸣耳聋", "健忘恍惚", "须发早白", "精少不育"],
            "mid":  ["月经量少", "舌淡红", "脉细"],
            "low":  ["健忘", "耳鸣"],
        },
        "tongue": "舌淡红，苔薄白",
        "pulse":  "细弱",
        "category": "肾系",
        "main_formula": "F-补-008",
        "alt_formulas": [],
        "source": "中医诊断学第四章·丹溪心法",
    },

    # ===== 复合证 =====
    {
        "id": "Z-复合-001", "name": "气血两虚",
        "bagang": {"里": True, "虚": True, "气虚": True, "血虚": True},
        "keywords": {
            "high": ["神疲乏力", "少气懒言", "面色淡白", "面色萎黄", "头晕目眩", "心悸失眠", "唇甲淡白"],
            "mid":  ["舌淡", "苔薄白", "脉细弱"],
            "low":  ["乏力", "面色差"],
        },
        "tongue": "舌淡，苔薄白",
        "pulse":  "细弱",
        "category": "复合",
        "main_formula": "F-补益-001",
        "alt_formulas": ["F-补益-002", "F-补益-005"],
        "source": "中医诊断学第四章·正体类要",
    },
    {
        "id": "Z-复合-002", "name": "气滞血瘀",
        "bagang": {"里": True, "实": True, "气滞": True, "血瘀": True},
        "keywords": {
            "high": ["胸胁胀闷窜痛", "刺痛固定", "刺痛", "拒按", "经前乳胀", "月经色暗有块", "舌紫暗", "瘀斑", "脉涩"],
            "mid":  ["脉弦", "舌暗"],
            "low":  ["疼痛固定"],
        },
        "tongue": "舌紫暗或瘀斑",
        "pulse":  "弦涩",
        "category": "复合",
        "main_formula": "F-理气-001",
        "alt_formulas": ["F-理血-001"],
        "source": "中医诊断学第四章·医林改错",
    },
    {
        "id": "Z-复合-003", "name": "痰湿内阻",
        "bagang": {"里": True, "实": True, "痰湿": True},
        "keywords": {
            "high": ["形体肥胖", "痰多易咯", "胸闷脘痞", "呕恶纳呆", "头晕目眩", "嗜睡", "苔白腻"],
            "mid":  ["舌胖", "脉滑"],
            "low":  ["痰多", "胸闷"],
        },
        "tongue": "舌胖，苔白腻或白滑",
        "pulse":  "滑",
        "category": "复合",
        "main_formula": "F-祛湿-003",
        "alt_formulas": [],
        "source": "中医诊断学第四章·三因极一病证方论",
    },
    {
        "id": "Z-复合-004", "name": "阴虚火旺",
        "bagang": {"里": True, "虚": True, "阴虚": True, "火旺": True},
        "keywords": {
            "high": ["潮热盗汗", "五心烦热", "颧红咽干", "遗精", "口舌生疮", "咳嗽痰少带血", "舌红少苔"],
            "mid":  ["脉细数", "剥苔"],
            "low":  ["盗汗"],
        },
        "tongue": "舌红，少苔或剥苔",
        "pulse":  "细数",
        "category": "复合",
        "main_formula": "F-补-007",
        "alt_formulas": ["F-补益-003"],
        "source": "中医诊断学第四章·医宗金鉴",
    },
    {
        "id": "Z-复合-005", "name": "阳虚水泛",
        "bagang": {"里": True, "虚": True, "寒": True, "水停": True},
        "keywords": {
            "high": ["全身浮肿", "腰以下为甚", "畏寒肢冷", "小便不利", "心悸气短", "腹胀便溏", "舌淡胖"],
            "mid":  ["脉沉迟", "苔白滑"],
            "low":  ["浮肿"],
        },
        "tongue": "舌淡胖，苔白滑",
        "pulse":  "沉迟无力",
        "category": "复合",
        "main_formula": "F-温里-003",
        "alt_formulas": ["F-祛湿-001"],
        "source": "中医诊断学第四章·伤寒论",
    },
    {
        "id": "Z-复合-006", "name": "心脾两虚",
        "bagang": {"里": True, "虚": True, "气血两虚": True},
        "keywords": {
            "high": ["心悸怔忡", "失眠多梦", "健忘", "纳少腹胀", "神疲乏力", "面色萎黄", "月经量少色淡", "淋漓不断"],
            "mid":  ["舌淡嫩", "脉细弱"],
            "low":  ["心悸", "失眠"],
        },
        "tongue": "舌淡嫩，苔白",
        "pulse":  "细弱",
        "category": "复合",
        "main_formula": "F-补益-005",
        "alt_formulas": [],
        "source": "中医诊断学第四章·济生方",
    },

    # ===== 杂病 =====
    {
        "id": "Z-杂-001", "name": "寒热错杂（半夏泻心证）",
        "bagang": {"里": True, "虚实夹杂": True, "寒热错杂": True},
        "keywords": {
            "high": ["心下痞满", "呕恶", "肠鸣下利", "胃脘灼热", "喜温按", "苔黄白相间"],
            "mid":  ["舌淡", "脉弦数"],
            "low":  ["胃脘不适"],
        },
        "tongue": "舌淡，苔黄白相间",
        "pulse":  "弦数或滑",
        "category": "杂病",
        "main_formula": "F-温里-001",
        "alt_formulas": [],
        "source": "中医诊断学第四章·伤寒论",
    },
    {
        "id": "Z-杂-002", "name": "表寒里热（外寒内热）",
        "bagang": {"表里": True, "实": True, "寒": True, "热": True},
        "keywords": {
            "high": ["恶寒发热无汗", "无汗", "头身痛", "烦躁", "口渴", "便秘尿黄"],
            "mid":  ["脉浮紧", "舌红", "苔黄"],
            "low":  ["发热"],
        },
        "tongue": "舌红，苔黄",
        "pulse":  "浮紧或数",
        "category": "杂病",
        "main_formula": "F-解表-001",
        "alt_formulas": [],
        "source": "中医诊断学第二章·伤寒论",
    },
]

assert len(ZHENG_TABLE) >= 30, f"证型数量不足: {len(ZHENG_TABLE)}"

# ============================================================================
# 数据：方剂表（与 references/zhongyi-fangji.md 同步）
# ============================================================================

FORMULA_TABLE: Dict[str, Dict] = {
    # ===== 六淫·风 =====
    "F-解表-001": {"name": "感冒清热颗粒", "classic_formula": "麻黄汤", "category": "六淫·风",
                   "indications": "风寒感冒：怕冷、无汗、流清涕、头痛、咳嗽痰白",
                   "dosage": "开水冲服，一次1袋，一日2次",
                   "caution": "风热感冒禁用；孕妇慎用；忌生冷油腻",
                   "source": "《伤寒论》麻黄汤演化"},
    "F-解表-002": {"name": "桂枝颗粒", "classic_formula": "桂枝汤", "category": "六淫·风",
                   "indications": "风寒表虚：发热、汗出恶风、鼻鸣干呕",
                   "dosage": "开水冲服，一次1袋，一日3次",
                   "caution": "表实无汗者不宜；风热感冒不适用",
                   "source": "《伤寒论》"},
    "F-解表-003": {"name": "银翘解毒片/丸", "classic_formula": "银翘散", "category": "六淫·风",
                   "indications": "风热感冒：发热重、微恶风、咽痛、口渴、黄涕",
                   "dosage": "片剂一次4片，一日2-3次；丸剂一次1丸，一日2-3次",
                   "caution": "风寒感冒禁用；忌辛辣油腻",
                   "source": "《温病条辨》"},
    "F-解表-004": {"name": "桑菊感冒片", "classic_formula": "桑菊饮", "category": "六淫·风",
                   "indications": "风热咳嗽：咳嗽、身热不甚、口微渴",
                   "dosage": "一次4-8片，一日2-3次",
                   "caution": "风寒咳嗽不适用",
                   "source": "《温病条辨》"},
    "F-解表-005": {"name": "九味羌活丸", "classic_formula": "九味羌活汤（羌活胜湿汤近）", "category": "六淫·风",
                   "indications": "外感风寒夹湿：头身重痛、肩背痛、肢体酸楚",
                   "dosage": "水丸一次3-4.5g，一日2-3次",
                   "caution": "风热感冒不适用；阴虚气弱者慎用",
                   "source": "《此事难知》"},
    "F-解表-006": {"name": "连花清瘟胶囊", "classic_formula": "麻杏石甘汤+银翘散", "category": "六淫·风",
                   "indications": "风热/热毒感冒：发热、咽痛、咳嗽黄痰、流浊涕；流感",
                   "dosage": "一次4粒，一日3次",
                   "caution": "风寒感冒禁用；孕妇慎用",
                   "source": "《伤寒论》+《温病条辨》合方"},
    "F-解表-007": {"name": "正柴胡饮颗粒", "classic_formula": "正柴胡饮", "category": "六淫·风",
                   "indications": "风寒感冒初起：恶寒发热、头痛身痛、鼻塞清涕",
                   "dosage": "开水冲服，一次1袋，一日3次",
                   "caution": "风热感冒不适用；孕妇慎用",
                   "source": "《景岳全书》"},

    # ===== 六淫·寒 =====
    "F-温里-001": {"name": "附子理中丸/理中丸", "classic_formula": "理中丸", "category": "六淫·寒",
                   "indications": "脾胃虚寒：脘腹冷痛、喜温喜按、呕吐泄泻、手足不温",
                   "dosage": "大蜜丸一次1丸，一日2-3次",
                   "caution": "实热证、感冒发热停用；孕妇慎用；忌生冷",
                   "source": "《伤寒论》"},
    "F-温里-003": {"name": "金匮肾气丸", "classic_formula": "肾气丸（崔氏八味丸）", "category": "脏腑·补肾阳",
                   "indications": "肾阳虚：腰膝酸冷、夜尿多、小便不利或反多、畏寒肢冷",
                   "dosage": "大蜜丸一次1丸，一日2次",
                   "caution": "阴虚火旺、实热者不宜；孕妇慎用；忌生冷",
                   "source": "《金匮要略》"},

    # ===== 六淫·暑 =====
    "F-暑湿-001": {"name": "藿香正气水/胶囊", "classic_formula": "藿香正气散", "category": "六淫·暑",
                   "indications": "暑湿/胃肠型感冒：发热恶寒、头昏重胀、胸闷脘痞、呕吐腹泻",
                   "dosage": "水剂一次5-10ml，一日2次；胶囊一次2-4粒，一日2次",
                   "caution": "水剂含酒精：驾驶员/酒精过敏禁用；孕妇慎用",
                   "source": "《太平惠民和剂局方》"},
    "F-暑湿-002": {"name": "保济丸", "classic_formula": "藿香正气散类", "category": "六淫·暑",
                   "indications": "暑湿吐泻：腹痛吐泻、恶心呕吐、肠胃不适",
                   "dosage": "一次1.85-3.7g（1-2瓶），一日3次",
                   "caution": "孕妇慎用；外感燥热者不宜",
                   "source": "岭南验方"},

    # ===== 六淫·湿 =====
    "F-祛湿-001": {"name": "五苓散/片", "classic_formula": "五苓散", "category": "六淫·湿",
                   "indications": "水湿内停：小便不利、水肿、口渴饮水不解、泄泻",
                   "dosage": "散剂一次6-9g，一日2次",
                   "caution": "阴虚津少者不宜；肾功能异常者遵医嘱",
                   "source": "《伤寒论》"},
    "F-祛湿-002": {"name": "平胃丸", "classic_formula": "平胃散", "category": "六淫·湿",
                   "indications": "湿滞脾胃：脘腹胀满、不思饮食、口淡无味、恶心嗳气、苔白厚腻",
                   "dosage": "水丸一次4.5-6g，一日2次",
                   "caution": "阴虚燥热者不宜；忌生冷油腻",
                   "source": "《太平惠民和剂局方》"},
    "F-祛湿-003": {"name": "二陈丸", "classic_formula": "二陈汤", "category": "六淫·湿",
                   "indications": "湿痰咳嗽：痰多色白易咯、胸膈痞闷、恶心、苔白腻",
                   "dosage": "水丸一次9g（或浓缩丸12-16丸），一日2次",
                   "caution": "阴虚燥咳、痰中带血者不宜；忌辛辣",
                   "source": "《太平惠民和剂局方》"},
    # ===== 六淫·燥 =====
    "F-补-013":   {"name": "百合固金丸", "classic_formula": "百合固金汤", "category": "六淫·燥",
                   "indications": "肺肾阴虚燥咳：干咳少痰或痰中带血、咽干喉痛、潮热",
                   "dosage": "大蜜丸一次1丸，一日2次",
                   "caution": "痰湿壅盛、风寒咳嗽者不宜；忌辛辣",
                   "source": "《慎斋遗书》"},

    # ===== 六淫·火 =====
    "F-清热-002": {"name": "黄连解毒丸", "classic_formula": "黄连解毒汤", "category": "六淫·火",
                   "indications": "三焦火毒：大热烦躁、口燥咽干、口舌生疮、目赤尿黄",
                   "dosage": "水丸一次3g，一日2-3次（以说明书为准）",
                   "caution": "脾胃虚寒者不宜；不宜久服；孕妇禁用",
                   "source": "《肘后备急方》《外台秘要》"},
    "F-清热-003": {"name": "导赤丸", "classic_formula": "导赤散", "category": "六淫·火",
                   "indications": "心经火热：口舌生疮、心烦、小便赤涩刺痛",
                   "dosage": "大蜜丸一次1丸，一日2次",
                   "caution": "脾胃虚寒者慎用；孕妇慎用",
                   "source": "《小儿药证直诀》"},
    "F-清热-004": {"name": "龙胆泻肝丸", "classic_formula": "龙胆泻肝汤", "category": "六淫·火",
                   "indications": "肝胆实火/湿热：头痛目赤、胁痛口苦、耳肿；阴肿带下、小便淋浊",
                   "dosage": "水丸一次3-6g，一日2次",
                   "caution": "脾胃虚寒者慎用；不宜久服；孕妇慎用",
                   "source": "《医方集解》引《局方》"},

    # ===== 气血·气虚 =====
    "F-补益-001": {"name": "四君子颗粒/丸", "classic_formula": "四君子汤", "category": "气血·气虚",
                   "indications": "脾胃气虚：面色萎白、语低声怯、食少便溏、四肢乏力",
                   "dosage": "颗粒一次15g，一日3次",
                   "caution": "实证、湿热者不宜；忌生冷",
                   "source": "《太平惠民和剂局方》"},
    "F-补益-004": {"name": "补中益气丸", "classic_formula": "补中益气汤", "category": "气血·气虚",
                   "indications": "中气不足/下陷：体倦乏力、少气懒言、食少腹胀、久泻脱肛",
                   "dosage": "浓缩丸一次8-10丸，一日3次",
                   "caution": "阴虚火旺、实热者不宜；感冒发热停用",
                   "source": "《脾胃论》"},
    "F-补益-005": {"name": "归脾丸", "classic_formula": "归脾汤", "category": "气血·气虚",
                   "indications": "心脾两虚：心悸怔忡、健忘失眠、食少体倦、面色萎黄、月经量少",
                   "dosage": "大蜜丸一次1丸，一日3次",
                   "caution": "痰热、实火者不宜；忌辛辣",
                   "source": "《济生方》"},

    # ===== 气血·血虚 =====
    "F-补益-002": {"name": "四物合剂/颗粒", "classic_formula": "四物汤", "category": "气血·血虚",
                   "indications": "营血虚滞：头晕目眩、心悸失眠、面色无华、月经量少",
                   "dosage": "合剂一次10-15ml，一日3次",
                   "caution": "月经期经量多者慎用；孕妇遵医嘱",
                   "source": "《仙授理伤续断秘方》"},
    "F-补-009":   {"name": "枣仁安神胶囊/酸枣仁合剂", "classic_formula": "酸枣仁汤", "category": "气血·血虚",
                   "indications": "肝血不足虚烦不眠：失眠多梦、易醒、心悸、盗汗",
                   "dosage": "胶囊一次5粒，一日1次（睡前服）",
                   "caution": "痰火内扰失眠不宜；孕妇慎用",
                   "source": "《金匮要略》"},

    # ===== 气血·气滞 =====
    "F-补-006":   {"name": "逍遥丸", "classic_formula": "逍遥散", "category": "气血·气滞",
                   "indications": "肝郁脾虚：心情郁闷、爱叹气、胁胀、食欲差、月经不调、乳胀",
                   "dosage": "浓缩丸一次8丸，一日3次",
                   "caution": "感冒发热停用；孕妇慎用；忌生冷油腻",
                   "source": "《太平惠民和剂局方》"},
    "F-理气-001": {"name": "柴胡疏肝丸", "classic_formula": "柴胡疏肝散", "category": "气血·气滞",
                   "indications": "肝气郁滞：胁肋胀痛、脘腹胀满、善太息、乳胀",
                   "dosage": "大蜜丸一次1丸，一日2次",
                   "caution": "气虚无郁滞者不宜；孕妇慎用",
                   "source": "《景岳全书》"},
    "F-理气-003": {"name": "苏子降气丸", "classic_formula": "苏子降气汤", "category": "气血·气滞",
                   "indications": "上实下虚喘咳：痰涎壅盛、喘咳短气、胸膈满闷、腰膝酸软",
                   "dosage": "水丸一次3-6g，一日2次",
                   "caution": "肺热痰黄、阴虚燥咳者不宜",
                   "source": "《太平惠民和剂局方》"},
    # ===== 气血·血瘀 =====
    "F-理血-001": {"name": "血府逐瘀丸/胶囊", "classic_formula": "血府逐瘀汤", "category": "气血·血瘀",
                   "indications": "胸中血瘀：胸痛头痛如针刺、固定不移、心悸失眠、舌暗瘀斑",
                   "dosage": "大蜜丸一次1-2丸，一日2次",
                   "caution": "孕妇禁用；月经过多者慎用；出血性疾病禁用",
                   "source": "《医林改错》"},
    "F-理血-002": {"name": "补阳还五丸/胶囊", "classic_formula": "补阳还五汤", "category": "气血·血瘀",
                   "indications": "气虚血瘀中风后遗症：半身不遂、口眼歪斜、语言不利、肢体麻木",
                   "dosage": "丸剂一次1丸，一日2次",
                   "caution": "中风急性期、出血性中风禁用；孕妇禁用",
                   "source": "《医林改错》"},

    # ===== 脏腑·补肾阴 =====
    "F-补益-003": {"name": "六味地黄丸", "classic_formula": "六味地黄丸", "category": "脏腑·补肾阴",
                   "indications": "肾阴虚：腰膝酸软、头晕耳鸣、盗汗遗精、手足心热、口干",
                   "dosage": "浓缩丸一次8丸，一日3次",
                   "caution": "脾虚便溏、痰湿内盛者不宜；感冒发热停用",
                   "source": "《小儿药证直诀》"},
    "F-补-008":   {"name": "左归丸", "classic_formula": "左归丸", "category": "脏腑·补肾阴",
                   "indications": "真阴不足：头晕目眩、腰酸腿软、遗精滑泄、自汗盗汗、口燥咽干",
                   "dosage": "水蜜丸一次9g，一日2次",
                   "caution": "脾虚便溏者慎用；感冒发热停用",
                   "source": "《景岳全书》"},
    "F-补-007":   {"name": "知柏地黄丸", "classic_formula": "知柏地黄丸", "category": "脏腑·补肾阴",
                   "indications": "阴虚火旺：腰膝酸软、骨蒸潮热、盗汗遗精、五心烦热、颧红咽干",
                   "dosage": "浓缩丸一次8丸，一日3次",
                   "caution": "脾虚便溏者不宜；感冒发热停用",
                   "source": "《医宗金鉴》"},

    # ===== 六淫·风（内风） =====
    "F-补-014":   {"name": "天麻钩藤颗粒", "classic_formula": "天麻钩藤饮", "category": "六淫·风",
                   "indications": "肝阳上亢：头痛眩晕、失眠、面红目赤、血压偏高、舌红苔黄",
                   "dosage": "开水冲服，一次1袋（10g），一日3次",
                   "caution": "属内风证非外感药；低血压者注意监测",
                   "source": "《中医内科杂病证治新义》"},

    # ===== 脏腑·通腑 =====
}

assert len(FORMULA_TABLE) >= 20, f"方剂数量不足: {len(FORMULA_TABLE)}"


# ============================================================================
# 核心：TCMDiagnose 类
# ============================================================================

KEYWORD_WEIGHTS = {"high": 5, "mid": 2, "low": 1}

# 寒热关键词（用于八纲判定 + 冲突惩罚）
COLD_STRONG = ["恶寒重", "形寒肢冷", "畏寒肢冷", "腰膝酸冷", "腰膝冷痛", "畏寒", "怕冷"]
HEAT_STRONG = ["发热重", "五心烦热", "潮热", "壮热", "烦躁", "口苦", "盗汗", "颧红"]
HOT_HOT     = ["发热", "口渴", "口干", "咽干", "舌红", "苔黄", "脉数", "脉洪大", "烦躁", "易怒", "便干", "便秘"]


@dataclass
class TCMDiagnose:
    """中医辨证推理器 v1.0.0（规则匹配 + 简单排序）"""

    zheng_table: List[Dict] = field(default_factory=lambda: ZHENG_TABLE)
    formula_table: Dict[str, Dict] = field(default_factory=lambda: FORMULA_TABLE)
    skill_root: Optional[Path] = None

    # -------- 特征提取 --------
    def extract_features(self, symptoms: str) -> Dict:
        """把用户文本拆分为可命中的特征。
        
        返回：
          {
            'text': str,              # 原始
            'has_cold': bool,         # 寒象关键词命中
            'has_heat': bool,         # 热象关键词命中
            'has_pulse_strong': bool, # 脉浮/紧/数/洪大等
            'has_tongue_strong': bool,
            ...
          }
        """
        text = (symptoms or "").strip()
        return {
            "text":      text,
            "has_cold":  any(k in text for k in COLD_STRONG),
            "has_heat":  any(k in text for k in HEAT_STRONG),
            "has_hot_attr": any(k in text for k in HOT_HOT),
            "has_xiong": "胸" in text,
            "has_xie":   "胁" in text,
            "has_fu":    "腹" in text,
            "has_yu":    "腰" in text,
            "has_xin_fan": "心烦" in text,
            "has_ou_tu":   "呕" in text,
            "has_ke":   "咳" in text,
            "has_tan":  any(k in text for k in ["痰", "咳痰"]),
            "has_dai_xie":  any(k in text for k in ["便溏", "腹泻", "下利", "大便清稀"]),
        }

    # -------- 八纲判定 --------
    def _judge_bagang(self, features: Dict) -> Dict:
        """基于文本特征判断八纲（粗粒度）。
        
        粗糙规则：
          - 表 vs 里：有无"寒热"主诉 + 病程短 / 部位偏表 → 表；偏内里脏腑 → 里
          - 寒 vs 热：has_cold → 寒；has_heat/hot_attr → 热
          - 虚 vs 实：典型虚症关键词（乏力、气短、盗汗、自汗、久病等） → 虚
          - 阴 vs 阳：寒+虚 → 阴；热+实 → 阳
        """
        text = features["text"]
        table_keywords = ["恶寒发热", "苔薄", "脉浮", "无汗", "鼻塞", "咳嗽"]  # 表证相关
        interior_keywords = ["心悸", "失眠", "腹胀", "胁痛", "腰膝", "眩晕", "耳鸣", "月经"]
        deficiency_keywords = ["乏力", "疲倦", "气短", "自汗", "盗汗", "久病", "腰膝酸软", "面色㿠白", "面色萎黄"]
        excess_keywords = ["面红目赤", "烦躁", "便秘", "尿黄", "痰多", "苔黄腻"]

        is_table = any(k in text for k in table_keywords) and not any(k in text for k in interior_keywords)
        is_interior = any(k in text for k in interior_keywords)

        is_cold = features["has_cold"]
        is_hot = features["has_heat"] or features["has_hot_attr"]

        is_deficiency = any(k in text for k in deficiency_keywords)
        is_excess     = any(k in text for k in excess_keywords)

        # 阴阳 → 八纲中与寒热虚实组合
        is_yin = (is_cold and is_deficiency) or (not is_hot and is_deficiency and "畏寒" in text)
        is_yang = (is_hot and is_excess) or (is_hot and not is_deficiency)

        return {
            "表里": "表" if is_table else ("里" if is_interior else "未明"),
            "寒热": "寒" if is_cold else ("热" if is_hot else "未明"),
            "虚实": "虚" if is_deficiency else ("实" if is_excess else "未明"),
            "阴阳": "阴" if is_yin else ("阳" if is_yang else "未明"),
        }

    # -------- 证型打分 --------
    def _score_zheng(self, features: Dict) -> List[Tuple[Dict, float]]:
        """对每个证型按关键词命中打分（含八纲冲突惩罚）。"""
        text = features["text"]
        scored: List[Tuple[Dict, float]] = []

        # 八纲冲突：如果用户文本明显为寒（has_cold），则热证大幅扣分；反之亦然
        for zheng in self.zheng_table:
            score = 0.0
            for tier, kws in zheng["keywords"].items():
                weight = KEYWORD_WEIGHTS.get(tier, 1)
                for kw in kws:
                    if kw in text:
                        score += weight
            # 八纲冲突惩罚（粗）：用户明显为寒 zheng["bagang"]["热"] 为真 → 大幅扣分
            if features["has_cold"] and zheng["bagang"].get("热"):
                if "脉数" in text or "口渴" in text:
                    pass  # 用户文本矛盾，保留少量分数
                else:
                    score -= 3
            if features["has_heat"] and zheng["bagang"].get("寒"):
                score -= 3
            # 用户明显为热，阴虚火旺 still ok（但虚 vs 实可不冲突）

            # 文本空 → 给一个极小基础分，避免全是 0
            if not text:
                score = 0.01
            scored.append((zheng, score))

        # 排序：score 降序
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored

    # -------- 单条诊断入口 --------
    def diagnose(self, symptoms: str, top_n: int = 3) -> Dict:
        """主入口：输入文本症状，返回 JSON 结构诊断。"""
        features = self.extract_features(symptoms)
        bagang = self._judge_bagang(features)
        scored = self._score_zheng(features)

        # 取 top_n（score > 0 的优先；如无则 fallback 取 3 条）
        positive = [(z, s) for z, s in scored if s > 0][:top_n]
        if not positive:
            positive = scored[:top_n]

        # 取每个候选对应的主方
        formulas_out = []
        for zheng, score in positive:
            main_id = zheng["main_formula"]
            formula = self.formula_table.get(main_id, {})
            formulas_out.append({
                "formula_id": main_id,
                "name": formula.get("name", main_id),
                "classic_formula": formula.get("classic_formula", ""),
                "category": formula.get("category", ""),
                "indications": formula.get("indications", ""),
                "dosage": formula.get("dosage", ""),
                "caution": formula.get("caution", ""),
                "source": formula.get("source", ""),
                "linked_zheng_id": zheng["id"],
                "linked_zheng_name": zheng["name"],
            })

        disclaimer_text = self._load_disclaimer_text()

        candidates = [
            {
                "id":       z["id"],
                "name":     z["name"],
                "category": z.get("category", ""),
                "bagang":   z["bagang"],
                "score":    round(s, 2),
                "tongue":   z.get("tongue", ""),
                "pulse":    z.get("pulse", ""),
                "source":   z.get("source", ""),
                "main_formula_id": z["main_formula"],
            }
            for z, s in positive
        ]

        return {
            "engine": "zhongyi v1.2.0",
            "input_symptoms": symptoms,
            "extracted_features": {
                "has_cold_signal": features["has_cold"],
                "has_heat_signal": features["has_heat"],
                "has_hot_attrs":   features["has_hot_attr"],
            },
            "bagang": bagang,
            "zheng_candidates": candidates,
            "formulas": formulas_out,
            "disclaimer": {
                "title": "免责声明 / Disclaimer",
                "text":  disclaimer_text,
                "must_acknowledge": True,
            },
            "_meta": {
                "skill_root": str(self.skill_root) if self.skill_root else None,
                "top_n": top_n,
                "scoring_method": "keyword_substring + bagang_conflict_penalty",
            },
        }

    def _load_disclaimer_text(self) -> str:
        """免责声明（内联，不依赖外部文件——老板 2026-08-22 拍板删免责文件）。"""
        return ("⚠️ 本技能仅供学习参考，**不构成医疗建议**。"
                "请前往中医院由执业中医师面诊，"
                "急症请拨 120 或就近医院。")


# ============================================================================
# 辅助函数：从测试用例验证
# ============================================================================

def run_self_test(skill_root: Path) -> Dict:
    """跑 test_cases.json 中的全部用例，返回统计。"""
    import json as _json
    test_path = skill_root / "scripts" / "test_cases.json"
    with open(test_path, encoding="utf-8") as f:
        data = _json.load(f)
    cases = data.get("cases", data) if isinstance(data, dict) else data

    diag = TCMDiagnose(skill_root=skill_root)
    results = []
    passed = 0

    for case in cases:
        output = diag.diagnose(case["symptoms"], top_n=3)
        top_id = output["zheng_candidates"][0]["id"] if output["zheng_candidates"] else None
        ok = (top_id == case["expected_top_zheng_id"])
        results.append({
            "case_id":    case.get("case_id", ""),
            "case_title": case.get("title", ""),
            "input":      case["symptoms"],
            "expected":   case["expected_top_zheng_id"],
            "got":        top_id,
            "got_name":   output["zheng_candidates"][0]["name"] if output["zheng_candidates"] else None,
            "passed":     ok,
            "formula":    output["formulas"][0]["name"] if output["formulas"] else None,
            "formula_source": output["formulas"][0]["source"] if output["formulas"] else None,
        })
        if ok:
            passed += 1

    return {
        "total":  len(cases),
        "passed": passed,
        "failed": len(cases) - passed,
        "results": results,
    }


# ============================================================================
# CLI 接入（被 tcm_cli.py 调用）
# ============================================================================

if __name__ == "__main__":
    # 直接执行：演示
    here = Path(__file__).resolve().parent
    skill_root = here.parent
    diag = TCMDiagnose(skill_root=skill_root)
    sample = "头痛3天，怕冷，无汗，鼻塞流清涕，咳嗽痰白稀，舌淡红苔薄白，脉浮紧"
    out = diag.diagnose(sample, top_n=3)
    print(json.dumps(out, ensure_ascii=False, indent=2))
