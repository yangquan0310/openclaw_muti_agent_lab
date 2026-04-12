#!/usr/bin/env python3
"""
添加剩余的32篇文献到学生论文修改项目知识库
基于Semantic Scholar检索结果
"""
import json
from datetime import datetime

index_path = "/root/实验室仓库/项目文件/学生论文修改/知识库/index.json"

# 读取现有知识库
with open(index_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 获取当前最大ID
current_ids = [int(p['id']) for p in data.get('papers', []) if str(p['id']).isdigit()]
max_id = max(current_ids) if current_ids else 0

print(f"当前最大ID: {max_id}")
print(f"现有文献数量: {len(data.get('papers', []))}")

# 从Semantic Scholar检索结果中提取的剩余32篇文献
# 第一批：sleep quality rumination（剩余15篇，ID 29-43）
# 第二批：sleep quality anxiety thinking（剩余17篇，ID 44-60）

new_papers = [
    # 第一批剩余 - sleep quality rumination
    {
        "id": "29",
        "title": "Effectiveness of Compassion Focused Group Therapy on Sleep Quality, Rumination and Resilience of Women in Isfahan City Suffering From Depression in Summer 2018",
        "authors": ["Ahdieh Eslamian", "A. Moradi", "A. Salehi"],
        "year": 2019,
        "venue": "",
        "citation_count": 3,
        "url": "https://www.semanticscholar.org/paper/50df6390e6e421179c0407fe0453b3ffb6c87bce",
        "abstract": None,
        "topic": ["多元负性思维与睡眠质量"],
        "labels": {"importance": "🔵一般", "type": "📋待分类", "jcr_quartile": "待筛选"}
    },
    {
        "id": "30",
        "title": "Interaction of sleep quality,rumination and negative emotions in elderly patients with chronic diseases",
        "authors": ["Chang Guosheng", "Li Li", "Zhu Runrui", "Zhang Ruixing"],
        "year": 2019,
        "venue": "",
        "citation_count": 0,
        "url": "https://www.semanticscholar.org/paper/705c92bb9289dd1a7f9114c49d8eaa44ae247fc8",
        "abstract": None,
        "topic": ["多元负性思维与睡眠质量"],
        "labels": {"importance": "🔵一般", "type": "📋待分类", "jcr_quartile": "待筛选"}
    },
    {
        "id": "31",
        "title": "Reciprocal causation relationship between rumination thinking and sleep quality: a resting-state fMRI study",
        "authors": ["Shiyan Yang", "Xu Lei"],
        "year": 2025,
        "venue": "Cognitive Neurodynamics",
        "citation_count": 5,
        "url": "https://www.semanticscholar.org/paper/1b28a644740e4ad403de23cc30fe90c8d9363ceb",
        "abstract": None,
        "topic": ["多元负性思维与睡眠质量"],
        "labels": {"importance": "🔵一般", "type": "📋待分类", "jcr_quartile": "待筛选"}
    },
    {
        "id": "32",
        "title": "The effectiveness of mindful self-compassion treatment on sleep quality, rumination and self-compassion in people with cardiovascular disease",
        "authors": ["A. Foroughi", "Sajjad Reisi", "N. Montazeri", "Motaleb Naseri"],
        "year": 2022,
        "venue": "Shenakht Journal of Psychology and Psychiatry",
        "citation_count": 4,
        "url": "https://www.semanticscholar.org/paper/7fa3e2a7cf2d00f21d87bf776a72605fee9b8893",
        "abstract": "Introduction: Cardiovascular diseases are the most common cause of death in the world and psychological components play an important role in cardiovascular diseases...",
        "topic": ["多元负性思维与睡眠质量"],
        "labels": {"importance": "🔵一般", "type": "📋待分类", "jcr_quartile": "待筛选"}
    },
    {
        "id": "33",
        "title": "Effects of physical activity on sleep quality among university students: chain mediation between rumination and depression levels",
        "authors": ["Lijing Xu", "Wenjing Yan", "Guohuan Hua", "Ziqing He", "Chunmei Wu", "Ming Hao"],
        "year": 2025,
        "venue": "BMC Psychiatry",
        "citation_count": 12,
        "url": "https://www.semanticscholar.org/paper/f07c675e243e995349bb7394a8e9756a70b67487",
        "abstract": "Colleges and universities are currently facing the major public health issue of poor sleep quality...",
        "topic": ["多元负性思维与睡眠质量"],
        "labels": {"importance": "🔵一般", "type": "📋待分类", "jcr_quartile": "待筛选"}
    },
    {
        "id": "34",
        "title": "The Role of Rumination and Worry in the Bidirectional Relationship Between Stress and Sleep Quality in Students",
        "authors": ["Ana Petak", "Jelena Maričić"],
        "year": 2025,
        "venue": "International Journal of Environmental Research and Public Health",
        "citation_count": 4,
        "url": "https://www.semanticscholar.org/paper/ea6740f33be0c93fcab094301dec077cd8c0ffb8",
        "abstract": "Poor sleep is strongly associated with stress; however, the mediators of this relationship are not well understood...",
        "topic": ["多元负性思维与睡眠质量"],
        "labels": {"importance": "🔵一般", "type": "📋待分类", "jcr_quartile": "待筛选"}
    },
    {
        "id": "35",
        "title": "Effects of stress on sleep quality: multiple mediating effects of rumination and social anxiety",
        "authors": ["Jun Zhang", "Xiaowen Li", "Zhenxing Tang", "Shungui Xiang", "Yin Tang", "Wenxin Hu", "Chenchen Tan", "Xin Wang"],
        "year": 2024,
        "venue": "Psicologia: Reflexão e Crítica",
        "citation_count": 29,
        "url": "https://www.semanticscholar.org/paper/ed26006430b555d03b71638cd2579ea9bafc1f22",
        "abstract": "Background In contemporary society, with the accelerated pace of work and life...",
        "topic": ["多元负性思维与睡眠质量"],
        "labels": {"importance": "🔵一般", "type": "📋待分类", "jcr_quartile": "待筛选"}
    },
    {
        "id": "36",
        "title": "The Relationship Between Bedtime Procrastination, Rumination, and Sleep Quality Among Physically Inactive Undergraduate Students",
        "authors": [""],
        "year": 2025,
        "venue": "EDUCATUM Journal of Social Sciences",
        "citation_count": 1,
        "url": "https://www.semanticscholar.org/paper/e6006f1ac15c957de87d80814a3c6bec42b1ace5",
        "abstract": "This study investigated the relationships between bedtime procrastination, rumination, and sleep quality among physically inactive students...",
        "topic": ["多元负性思维与睡眠质量"],
        "labels": {"importance": "🔵一般", "type": "📋待分类", "jcr_quartile": "待筛选"}
    },
    {
        "id": "37",
        "title": "Sleep Quality, Pain, Worry, and Rumination in Fibromyalgia: Results from Mediation Analyses",
        "authors": ["M. Tenti", "W. Raffaeli", "C. Fagnani", "E. Medda", "Martina Basciu", "Valentina Benassi", "Noemi Boschetti", "Lorelay Martorana", "S. Palmieri", "Giorgia Panini", "Leandra Scovotto", "V. Toccaceli"],
        "year": 2025,
        "venue": "Journal of Clinical Medicine",
        "citation_count": 2,
        "url": "https://www.semanticscholar.org/paper/9d284d4b7f9ee902d0dded90ad0faf397f83c452",
        "abstract": "Background/Objectives: Fibromyalgia (FM) is a chronic pain syndrome frequently associated with severe pain, sleep disturbances, worry, and depressive rumination...",
        "topic": ["多元负性思维与睡眠质量"],
        "labels": {"importance": "🔵一般", "type": "📋待分类", "jcr_quartile": "待筛选"}
    },
    {
        "id": "38",
        "title": "The Role of Bedtime Procrastination, Rumination, Loneliness, and Positive Body Image in Predicting Sleep Quality Among University Students: A Sex-Specific Analysis",
        "authors": ["Ying Wang", "Xiaoying Wang", "Qi Wang", "Guoqiu Liu", "Chunmei Wu", "Ming Hao"],
        "year": 2025,
        "venue": "ALPHA PSYCHIATRY",
        "citation_count": 1,
        "url": "https://www.semanticscholar.org/paper/9f0ffa787713dcc5a0f4b3bd8993166e4f74c801",
        "abstract": "Objective: This study aimed to analyze the impact of bedtime procrastination, rumination, loneliness, and positive body image on university students' sleep quality...",
        "topic": ["多元负性思维与睡眠质量"],
        "labels": {"importance": "🔵一般", "type": "📋待分类", "jcr_quartile": "待筛选"}
    },
    {
        "id": "39",
        "title": "The mediating role of rumination and psychological resilience between physical activity and sleep quality among college students",
        "authors": ["Yanying Liu", "Yao Tong", "Guihua Huang", "Kelei Guo"],
        "year": 2025,
        "venue": "Scientific Reports",
        "citation_count": 1,
        "url": "https://www.semanticscholar.org/paper/55f1e630ba3dd2b8c91a33b1d5a633a98778ebcc",
        "abstract": "Sleep quality is a critical issue among college students, significantly affecting their academic performance, mental health, and overall well-being...",
        "topic": ["多元负性思维与睡眠质量"],
        "labels": {"importance": "🔵一般", "type": "📋待分类", "jcr_quartile": "待筛选"}
    },
    {
        "id": "40",
        "title": "Perceived stress and sleep quality among primary health care workers: mediating roles of positive rumination and negative rumination",
        "authors": ["Quyi Zhang", "Shibin Chen", "Xuntao He", "Shu He", "Lin Yang", "Jun Ma"],
        "year": 2025,
        "venue": "Current Psychology",
        "citation_count": 1,
        "url": "https://www.semanticscholar.org/paper/68c9fd696353b32a86dc466299375c675d6d4257",
        "abstract": None,
        "topic": ["多元负性思维与睡眠质量"],
        "labels": {"importance": "🔵一般", "type": "📋待分类", "jcr_quartile": "待筛选"}
    },
    {
        "id": "41",
        "title": "Examining the association between perceived racism and sleep quality: The mediating role of rumination",
        "authors": ["Clysha Whitlow", "P. Zendels", "Andrew D Case"],
        "year": 2025,
        "venue": "Cultural diversity & ethnic minority psychology",
        "citation_count": 1,
        "url": "https://www.semanticscholar.org/paper/8db2d58025874797c920c2e68636857c3b5a4b69",
        "abstract": "OBJECTIVES: Sleep problems and disorders are associated with various health problems, such as heart disease and cancer...",
        "topic": ["多元负性思维与睡眠质量"],
        "labels": {"importance": "🔵一般", "type": "📋待分类", "jcr_quartile": "待筛选"}
    },
    {
        "id": "42",
        "title": "Reflections on the mirror: associations among body image rumination, sleep quality, and self-reported physical health",
        "authors": ["Abigail R. Hardy", "Jean M. Lamont"],
        "year": 2025,
        "venue": "Psychology, Health & Medicine",
        "citation_count": 0,
        "url": "https://www.semanticscholar.org/paper/d24a0c924ebd5cb74791fb7f53b2f9aa27692c86",
        "abstract": "Poor body image, a common occurrence across the lifespan, has been linked to poor physical health...",
        "topic": ["多元负性思维与睡眠质量"],
        "labels": {"importance": "🔵一般", "type": "📋待分类", "jcr_quartile": "待筛选"}
    },
    {
        "id": "43",
        "title": "Depressive symptoms among kidney transplant recipients: Modeling stress-related pathways involving chronotype, perceived stress, rumination, and sleep quality",
        "authors": ["Jiayi Zhu", "Jianfei Xie", "Gang Gan", "Zitong Lu", "Huiyi Zhang", "Jingying Wang", "Xiaoqian Dong", "Qingcheng Zheng", "Lijun Li", "Yanan Zhang", "Min Liu"],
        "year": 2025,
        "venue": "Comprehensive Psychiatry",
        "citation_count": 0,
        "url": "https://www.semanticscholar.org/paper/827c7d7ba93e0958f34897713f1fd30063958f91",
        "abstract": "BACKGROUND: Depressive symptoms are common among kidney transplant recipients and are linked to adverse clinical and psychosocial outcomes...",
        "topic": ["多元负性思维与睡眠质量"],
        "labels": {"importance": "🔵一般", "type": "📋待分类", "jcr_quartile": "待筛选"}
    },
    # 第二批 - sleep quality anxiety thinking（17篇，ID 44-60）
    {
        "id": "44",
        "title": "Generalized anxiety disorder, depressive symptoms and sleep quality during COVID-19 outbreak in China: a web-based cross-sectional survey",
        "authors": ["Yeen Huang", "N. Zhao"],
        "year": 2020,
        "venue": "Psychiatry Research",
        "citation_count": 2996,
        "url": "https://www.semanticscholar.org/paper/ff9c8b3d364d027da407dd772be53cb237a349f2",
        "abstract": "Highlights: The COVID-19 outbreak significantly affects the mental health of Chinese public...",
        "topic": ["多元负性思维与睡眠质量"],
        "labels": {"importance": "🔴奠基", "type": "📋待分类", "jcr_quartile": "待筛选"}
    },
    {
        "id": "45",
        "title": "Sleep Quality, Stress, and Mental Health in College Students: The Protective Role of Optimism and Critical Thinking",
        "authors": ["Rosa Angela Fabio", "Alessia Di Pietro", "Rossella Suriano"],
        "year": 2025,
        "venue": "Psychiatry International",
        "citation_count": 2,
        "url": "https://www.semanticscholar.org/paper/6d87cabeceab73cddd516f817fc3cecebcd5561c",
        "abstract": "Mental health among university students is an issue of growing global concern, impacting both psychological well-being and academic outcomes...",
        "topic": ["多元负性思维与睡眠质量"],
        "labels": {"importance": "🔵一般", "type": "📋待分类", "jcr_quartile": "待筛选"}
    },
    {
        "id": "46",
        "title": "EFFECT OF STRESS, ANXIETY AND DEPRESSION ON SLEEP QUALITY AMONG UNIVERSITY STUDENTS",
        "authors": ["Payal Chakerwarti", "Divyanshi Singh"],
        "year": 2025,
        "venue": "International Journal of Psychosocial Rehabilitation",
        "citation_count": 0,
        "url": "https://www.semanticscholar.org/paper/7d00cbdab558072ab44bff28c8f4715651e2ca43",
        "abstract": "Sleep is a basic human need. Abraham Maslow showed that sleep as part of your physiological needs in the hierarchy of five basic human needs...",
        "topic": ["多元负性思维与睡眠质量"],
        "labels": {"importance": "🔵一般", "type": "📋待分类", "jcr_quartile": "待筛选"}
    },
    {
        "id": "47",
        "title": "The associations between repetitive negative thinking, insomnia symptoms, and sleep quality in adults with a history of trauma",
        "authors": ["Kimberly A. Arditte Hall", "Christopher M. McGrory", "Alana M Snelson", "S. Pineles"],
        "year": 2024,
        "venue": "Anxiety, Stress, & Coping",
        "citation_count": 0,
        "url": "https://www.semanticscholar.org/paper/c52bd8132f4a286e3c8d8f0e46f3801",
        "abstract": "ABSTRACT Background Posttraumatic stress disorder (PTSD) and sleep disturbance are highly comorbid...",
        "topic": ["多元负性思维与睡眠质量"],
        "labels": {"importance": "🔵一般", "type": "📋待分类", "jcr_quartile": "待筛选"}
    },
    {
        "id": "48",
        "title": "The relationship between repetitive negative thinking, sleep disturbance, and subjective fatigue in women with Generalized Anxiety Disorder",
        "authors": ["Phoebe Leung", "Sophie H. Li", "B. Graham"],
        "year": 2022,
        "venue": "British Journal of Clinical Psychology",
        "citation_count": 25,
        "url": "https://www.semanticscholar.org/paper/d1370fdf8d45ad1b15bc589b6e1f3883b56b9fcf",
        "abstract": "Objectives Fatigue is a prominent symptom of Generalized Anxiety Disorder (GAD)...",
        "topic": ["多元负性思维与睡眠质量"],
        "labels": {"importance": "🔵一般", "type": "📋待分类", "jcr_quartile": "待筛选"}
    },
    {
        "id": "49",
        "title": "Does notifying clinicians about poor sleep quality influence patient-perceived empathy? Results from a randomized controlled trial",
        "authors": ["Sina Ramtin", "Jada Thompson", "David Ring", "Mark Queralt"],
        "year": 2025,
        "venue": "Sleep Medicine",
        "citation_count": 0,
        "url": "https://www.semanticscholar.org/paper/5565efe945fb9f3c93b5cf38583981",
        "abstract": "BACKGROUND: Evidence suggests that greater levels of comfort and capability are associated with lower levels of distress...",
        "topic": ["多元负性思维与睡眠质量"],
        "labels": {"importance": "🔵一般", "type": "📋待分类", "jcr_quartile": "待筛选"}
    },
    {
        "id": "50",
        "title": "The Relationship Between Anxiety Level and Sleep Status Among Uyghur High School Students in Kashgar, Xinjiang: the Mediating Role of Rumination",
        "authors": ["Xujie Huang", "Huixia Zhou", "Xiangyang Zhang"],
        "year": 2024,
        "venue": "Advances in Social Development and Education Research",
        "citation_count": 0,
        "url": "https://www.semanticscholar.org/paper/91f8ffc9ea4bb030417f3c247d1febdfdc509df5",
        "abstract": "This study explored the relationship between anxiety and sleep and the mediating role of rumination among Uyghur high school students...",
        "topic": ["多元负性思维与睡眠质量"],
        "labels": {"importance": "🔵一般", "type": "📋待分类", "jcr_quartile": "待筛选"}
    },
    {
        "id": "51",
        "title": "Is there an association between sleep quality and magnitude of capability?",
        "authors": ["J. Padilla", "Sina Ramtin", "D. Ring", "T. Crijns", "Mark Queralt"],
        "year": 2023,
        "venue": "Sleep Medicine",
        "citation_count": 3,
        "url": "https://www.semanticscholar.org/paper/893aa44dbcbfe5eb1436548c1f1c3be27540afc7",
        "abstract": "PURPOSE: Given the stigma surrounding mental health, a discussion of how symptoms interfere with sleep might be a useful first step...",
        "topic": ["多元负性思维与睡眠质量"],
        "labels": {"importance": "🔵一般", "type": "📋待分类", "jcr_quartile": "待筛选"}
    },
    {
        "id": "52",
        "title": "Anhedonia is central for the association between quality of life, metacognition, sleep, and affective symptoms in generalized anxiety disorder: A complex network analysis",
        "authors": ["Abigail L. Barthel", "Megan A. Pinaire", "Joshua E. Curtiss", "Amanda W. Baker", "Mackenzie L. Brown", "S. Hoeppner", "E. Bui", "N. Simon", "S. Hofmann"],
        "year": 2020,
        "venue": "Journal of Affective Disorders",
        "citation_count": 33,
        "url": "https://www.semanticscholar.org/paper/789df9549f0712d7de51d97be4e781c43edae673",
        "abstract": "BACKGROUND: Poor quality of life, sleep problems, anhedonia, and negative metacognitions are common in anxiety and depression...",
        "topic": ["多元负性思维与睡眠质量"],
        "labels": {"importance": "🔵一般", "type": "📋待分类", "jcr_quartile": "待筛选"}
    },
    {
        "id": "53",
        "title": "Smartphone addiction and college students' sleep quality: Analysis of mediating and moderating effects",
        "authors": ["Qiong Zhao"],
        "year": 2023,
        "venue": "Applied & Educational Psychology",
        "citation_count": 0,
        "url": "https://www.semanticscholar.org/paper/940fb947c3b5b0de9e17953895a91a4e53af8609",
        "abstract": "This study took college students from four universities in Zhengzhou, Henan Province as the research subjects...",
        "topic": ["多元负性思维与睡眠质量"],
        "labels": {"importance": "🔵一般", "type": "📋待分类", "jcr_quartile": "待筛选"}
    },
    {
        "id": "54",
        "title": "Study on the combination of innovative and entrepreneurial thinking training and psychological nursing intervention to alleviate college students' employment anxiety",
        "authors": ["Haohe Wang", "Yuqi Jiang"],
        "year": 2023,
        "venue": "CNS Spectrums",
        "citation_count": 3,
        "url": "https://www.semanticscholar.org/paper/070c9e7382f4e286eac0edbf3c8c942f1d646708",
        "abstract": "Background Employment anxiety is a kind of nervous and persistent negative emotion that college students have toward the future...",
        "topic": ["多元负性思维与睡眠质量"],
        "labels": {"importance": "🔵一般", "type": "📋待分类", "jcr_quartile": "待筛选"}
    },
    {
        "id": "55",
        "title": "Psychological Impact and Sleep Quality in the COVID-19 Pandemic in Brazil, Colombia and Portugal",
        "authors": ["U. R. Rodríguez-De Avila", "Fabíola Rodrigues-De França", "Maria de Fátima Jesus Simões"],
        "year": 2021,
        "venue": "Duazary",
        "citation_count": 4,
        "url": "https://www.semanticscholar.org/paper/a27b4a61095d622d13912fd6bbc4f6085b0fa64b",
        "abstract": "The objective of the study was to evaluate, through an online questionnaire, aspects related to levels of anxiety, suicidal thoughts and quality of sleep...",
        "topic": ["多元负性思维与睡眠质量"],
        "labels": {"importance": "🔵一般", "type": "📋待分类", "jcr_quartile": "待筛选"}
    },
    {
        "id": "56",
        "title": "Keeps me awake at night: The potential of the COVID-19 pandemic to affect sleep quality among sexual minority men in the U.S.A",
        "authors": ["B. Millar", "Trinae Adebayo", "Trey V. Dellucci", "Evelyn Behar", "Tyrel J. Starks"],
        "year": 2020,
        "venue": "Psychology of Sexual Orientation and Gender Diversity",
        "citation_count": 14,
        "url": "https://www.semanticscholar.org/paper/df6629be0939b8617f4984000863b4832f9c4d52",
        "abstract": "Sleep health, a crucial component and predictor of physical and mental health, has likely been adversely impacted by the stress and disruption wrought by the COVID-19 pandemic...",
        "topic": ["多元负性思维与睡眠质量"],
        "labels": {"importance": "🔵一般", "type": "📋待分类", "jcr_quartile": "待筛选"}
    },
    {
        "id": "57",
        "title": "Modeling the Effects of Stress, Anxiety, and Depression on Rumination, Sleep, and Fatigue in a Nonclinical Sample",
        "authors": ["E. Thorsteinsson", "R. Brown", "M. Owens"],
        "year": 2019,
        "venue": "Journal of Nervous and Mental Disease",
        "citation_count": 35,
        "url": "https://www.semanticscholar.org/paper/7b53d73ac7e7efda677e7b95821b55143e0fec1c",
        "abstract": "Abstract Stress and affective distress have previously been shown to predict sleep quality, and all the factors have been shown to predict fatigue severity...",
        "topic": ["多元负性思维与睡眠质量"],
        "labels": {"importance": "🔵一般", "type": "📋待分类", "jcr_quartile": "待筛选"}
    },
    {
        "id": "58",
        "title": "Sleep disturbance is associated with less emotional reactivity in individuals with heightened repetitive negative thinking",
        "authors": ["Jacob A. Nota", "Jeremy V. Hermanson", "M. Coles"],
        "year": 2021,
        "venue": "Current Psychology",
        "citation_count": 2,
        "url": "https://www.semanticscholar.org/paper/e37ba5792d8483362728528ef84bb70e128285d1",
        "abstract": None,
        "topic": ["多元负性思维与睡眠质量"],
        "labels": {"importance": "🔵一般", "type": "📋待分类", "jcr_quartile": "待筛选"}
    },
    {
        "id": "59",
        "title": "Suicide Risk and Its Associations with Psychiatric Symptoms and Sleep Disturbances in Schizophrenia Inpatients",
        "authors": ["Chaowei Li", "Yun Chen", "Lyufeng Zhang", "Hongle Zhang", "Shun Zhang", "Qianqian Chen", "Meihua Yang", "Na Liang", "Sifan Hu", "Zhaojun Ni", "Lin Lu", "Xinyu Sun", "Hongqiang Sun"],
        "year": 2025,
        "venue": "China CDC Weekly",
        "citation_count": 2,
        "url": "https://www.semanticscholar.org/paper/73786d1a6551056eab7c573d852b48e85903958c",
        "abstract": "What is already known about this topic? Suicide behaviors are prevalent among inpatients with schizophrenia...",
        "topic": ["多元负性思维与睡眠质量"],
        "labels": {"importance": "🔵一般", "type": "📋待分类", "jcr_quartile": "待筛选"}
    },
    {
        "id": "60",
        "title": "The impacts of rumination and affective symptoms on subjective-objective sleep discrepancy",
        "authors": ["Xinyi Deng", "Shuo Wang", "Yulin Wang", "Xu Lei"],
        "year": 2025,
        "venue": "Journal of Clinical and Experimental Neuropsychology",
        "citation_count": 1,
        "url": "https://www.semanticscholar.org/paper/4577ade14c9263322e62387b4e73eb71f99e1858",
        "abstract": "ABSTRACT Prior research has shown a strong association between insomnia and affective symptoms including depressive and anxiety symptoms...",
        "topic": ["多元负性思维与睡眠质量"],
        "labels": {"importance": "🔵一般", "type": "📋待分类", "jcr_quartile": "待筛选"}
    }
]

print(f"准备添加 {len(new_papers)} 篇新文献...")

# 添加到知识库
data['papers'].extend(new_papers)

# 更新统计信息
stats = data.get('statistics', {})
stats['total_count'] = len(data['papers'])

# 计算各类统计
foundation_count = sum(1 for p in data['papers'] if p.get('labels', {}).get('importance') == '🔴奠基')
important_count = sum(1 for p in data['papers'] if p.get('labels', {}).get('importance') == '🟡重要')
general_count = sum(1 for p in data['papers'] if p.get('labels', {}).get('importance') == '🔵一般')

stats['foundation_count'] = foundation_count
stats['important_count'] = important_count
stats['general_count'] = general_count

# 更新版本号和时间戳
data['version'] = '1.4.0'
data['updated_at'] = datetime.now().isoformat()

# 保存
with open(index_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n更新完成：")
print(f"  - 新增文献: {len(new_papers)}篇")
print(f"  - 总计: {len(data['papers'])}篇")
print(f"  - 奠基文献: {foundation_count}篇")
print(f"  - 重要文献: {important_count}篇")
print(f"  - 一般文献: {general_count}篇")
print(f"  - 版本号: {data['version']}")
print(f"  - 更新时间: {data['updated_at']}")
