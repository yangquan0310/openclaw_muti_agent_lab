#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文献主题分类器 - 面向对象版本

功能：读取主题笔记文件，根据研究问题判断文献是否适合当前主题，
      如不适合则记录建议移动到的主题。
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from collections import Counter


@dataclass
class TopicConfig:
    """主题配置类"""
    name: str
    keywords: List[str]
    
    def matches(self, text: str) -> int:
        """计算文本与主题的匹配度得分"""
        text_lower = text.lower()
        return sum(1 for kw in self.keywords if kw in text_lower)


class TopicClassifier:
    """主题分类器"""
    
    # 7个主题定义
    TOPICS = [
        TopicConfig("自传体记忆的概念", ["定义", "结构", "模型", "理论", "概念", "分类", "系统", "框架"]),
        TopicConfig("自传体记忆的功能", ["功能", "作用", "应用", "叙事身份", "回忆疗法", "自我连续", "社会功能", "指导功能"]),
        TopicConfig("自传体记忆的编码", ["编码", "自我参照", "注意", "加工", "形成", "获得", "学习", "识记"]),
        TopicConfig("自传体记忆的存储", ["存储", "巩固", "保持", "海马", "皮层", "睡眠", "长期", "保存"]),
        TopicConfig("自传体记忆的遗忘", ["遗忘", "衰退", "抑制", "定向遗忘", "过度概括", "丢失", "减弱"]),
        TopicConfig("自传体记忆的提取", ["提取", "检索", "回忆", "搜索", "访问", "回想", "记起"]),
        TopicConfig("数字化使用对自传体记忆的影响", ["数字", "拍照", "谷歌效应", "认知卸载", "社交媒体", "技术", "设备"])
    ]
    
    def __init__(self):
        self.topic_map = {t.name: t for t in self.TOPICS}
    
    def classify(self, paper_id: str, paper_data: Dict, current_topic: str) -> Tuple[bool, str, str]:
        """
        根据研究问题判断文献是否适合当前主题
        
        Returns:
            (is_suitable, suggested_topic, reason)
        """
        title = paper_data.get('title', '')
        content = paper_data.get('content', {})
        research_question = content.get('research_question', '') or content.get('question', '')
        
        if not research_question:
            return True, current_topic, "无法获取研究问题，保持原主题"
        
        # 基于关键词匹配判断
        text_to_check = f"{research_question} {title}"
        
        # 检查当前主题得分
        current_config = self.topic_map.get(current_topic)
        current_score = current_config.matches(text_to_check) if current_config else 0
        
        # 检查其他主题得分
        best_topic = current_topic
        best_score = current_score
        
        for topic_config in self.TOPICS:
            if topic_config.name == current_topic:
                continue
            score = topic_config.matches(text_to_check)
            if score > best_score:
                best_score = score
                best_topic = topic_config.name
        
        # 如果当前主题得分最高或相等，保持原主题
        if best_topic == current_topic or best_score == 0:
            return True, current_topic, f"当前主题匹配度最高（得分：{current_score}）"
        
        return False, best_topic, f"检测到更适合的主题：{best_topic}（匹配度：{best_score} > {current_score}）"


class NotesLoader:
    """笔记加载器"""
    
    def __init__(self, notes_dir: str):
        self.notes_dir = Path(notes_dir)
    
    def load(self, filename: str) -> Dict:
        """加载笔记文件"""
        filepath = self.notes_dir / filename
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_topic_from_filename(self, filename: str) -> str:
        """从文件名提取主题"""
        for topic in [t.name for t in TopicClassifier.TOPICS]:
            if topic in filename:
                return topic
        return "未知主题"


class ClassificationResult:
    """分类结果类"""
    
    def __init__(self, source_file: str, current_topic: str, range_str: str):
        self.source_file = source_file
        self.current_topic = current_topic
        self.range = range_str
        self.total_checked = 0
        self.modifications: List[Dict] = []
    
    def add_modification(self, paper_id: str, title: str, suggested_topic: str, 
                        research_question: str, reason: str):
        """添加修改记录"""
        self.modifications.append({
            "id": paper_id,
            "title": title,
            "current_topic": self.current_topic,
            "suggested_topic": suggested_topic,
            "research_question": research_question,
            "reason": reason
        })
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "source_file": self.source_file,
            "current_topic": self.current_topic,
            "range": self.range,
            "total_checked": self.total_checked,
            "modifications_count": len(self.modifications),
            "modifications": self.modifications
        }
    
    def save(self, output_file: str):
        """保存结果到文件"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)


class BatchClassifier:
    """批量分类器"""
    
    def __init__(self, notes_dir: str):
        self.notes_dir = notes_dir
        self.loader = NotesLoader(notes_dir)
        self.classifier = TopicClassifier()
    
    def classify_batch(self, notes_file: str, start_idx: int, end_idx: int, 
                      output_file: str) -> ClassificationResult:
        """批量分类指定范围的文献"""
        # 加载笔记文件
        data = self.loader.load(notes_file)
        current_topic = self.loader.get_topic_from_filename(notes_file)
        
        # 获取所有文献ID并排序
        all_ids = sorted(data.get('notes', {}).keys())
        selected_ids = all_ids[start_idx:end_idx]
        
        # 创建结果对象
        result = ClassificationResult(
            source_file=notes_file,
            current_topic=current_topic,
            range_str=f"{start_idx+1}-{end_idx}"
        )
        result.total_checked = len(selected_ids)
        
        # 分类处理
        for paper_id in selected_ids:
            paper_data = data['notes'][paper_id]
            is_suitable, suggested_topic, reason = self.classifier.classify(
                paper_id, paper_data, current_topic
            )
            
            if not is_suitable:
                research_question = (paper_data.get('content', {}).get('research_question', '') or 
                                   paper_data.get('content', {}).get('question', ''))
                result.add_modification(
                    paper_id=paper_id,
                    title=paper_data.get('title', ''),
                    suggested_topic=suggested_topic,
                    research_question=research_question,
                    reason=reason
                )
                print(f"  ⚠ {paper_id}: 建议移动到 '{suggested_topic}'")
        
        # 保存结果
        result.save(output_file)
        return result


def main():
    if len(sys.argv) < 5:
        print("用法: python3 classify_papers.py <主题文件> <起始索引> <结束索引> <输出文件>")
        print("示例: python3 classify_papers.py '自传体记忆的概念.json' 0 30 '/tmp/调整_概念_1-30.json'")
        sys.exit(1)
    
    notes_file = sys.argv[1]
    start_idx = int(sys.argv[2])
    end_idx = int(sys.argv[3])
    output_file = sys.argv[4]
    
    notes_dir = "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/笔记"
    
    print(f"==========================================")
    print(f"文献主题分类")
    print(f"==========================================")
    print(f"主题文件: {notes_file}")
    print(f"处理范围: 第{start_idx+1}-{end_idx} 篇")
    print(f"输出文件: {output_file}")
    print(f"==========================================")
    
    # 执行分类
    classifier = BatchClassifier(notes_dir)
    result = classifier.classify_batch(notes_file, start_idx, end_idx, output_file)
    
    print(f"\n✅ 完成！")
    print(f"  检查文献: {result.total_checked}篇")
    print(f"  建议修改: {len(result.modifications)}篇")
    print(f"  输出文件: {output_file}")


if __name__ == "__main__":
    main()
