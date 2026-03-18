#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 职业替代概率预测器

根据职业的多个维度评估 AI 替代概率。
评估维度：
- 创造性 (creativity): 越高越难被替代
- 社交互动 (social_interaction): 越高越难被替代
- 重复性 (repetition): 越高越容易被替代
- 技术依赖性 (technical_dependency): 越高越容易被替代
- 精细操作 (physical_dexterity): 越高越难被替代
- 批判性思维 (critical_thinking): 越高越难被替代
- 情商需求 (emotional_intelligence): 越高越难被替代
"""

import json
from typing import Dict, List, Any


class JobPredictor:
    """职业替代概率预测器"""
    
    def __init__(self):
        # 维度权重（总和为 1）
        # 正权重：增加替代概率
        # 负权重：降低替代概率
        self.weights = {
            'creativity': -0.15,           # 创造性高 → 难替代
            'social_interaction': -0.15,   # 社交多 → 难替代
            'repetition': 0.25,            # 重复性高 → 易替代
            'technical_dependency': 0.15,  # 技术依赖高 → 易替代
            'physical_dexterity': -0.10,   # 精细操作 → 难替代
            'critical_thinking': -0.10,    # 批判思维 → 难替代
            'emotional_intelligence': -0.10  # 情商需求 → 难替代
        }
        
    def calculate_score(self, dimensions: Dict[str, int]) -> float:
        """
        计算替代概率分数 (0-100)
        
        Args:
            dimensions: 各维度分数 (0-10)
            
        Returns:
            替代概率 (0-100)
        """
        score = 50.0  # 基础分数
        
        for dim, weight in self.weights.items():
            dim_value = dimensions.get(dim, 5)
            # 将 0-10 的分数转换为 -5 到 +5 的偏移
            offset = (dim_value - 5) * weight * 10
            score += offset
            
        # 限制在 0-100 范围
        return max(0, min(100, score))
    
    def get_risk_level(self, probability: float) -> str:
        """
        根据概率返回风险等级
        
        Args:
            probability: 替代概率
            
        Returns:
            风险等级字符串
        """
        if probability < 30:
            return "低风险"
        elif probability < 60:
            return "中风险"
        else:
            return "高风险"
    
    def predict(self, job: Dict[str, Any]) -> Dict[str, Any]:
        """
        预测单个职业的替代概率
        
        Args:
            job: 职业数据
            
        Returns:
            包含预测结果的字典
        """
        probability = self.calculate_score(job['dimensions'])
        risk_level = self.get_risk_level(probability)
        
        return {
            'name': job['name'],
            'category': job['category'],
            'probability': round(probability, 1),
            'risk_level': risk_level,
            'dimensions': job['dimensions'],
            'skills': job['skills']
        }
    
    def predict_all(self, jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        批量预测所有职业
        
        Args:
            jobs: 职业数据列表
            
        Returns:
            预测结果列表
        """
        results = []
        for job in jobs:
            result = self.predict(job)
            results.append(result)
        
        # 按替代概率降序排序
        results.sort(key=lambda x: x['probability'], reverse=True)
        
        return results
    
    def get_category_stats(self, results: List[Dict[str, Any]]) -> Dict[str, Dict]:
        """
        按类别统计
        
        Args:
            results: 预测结果列表
            
        Returns:
            各类别的统计数据
        """
        categories = {}
        
        for result in results:
            cat = result['category']
            if cat not in categories:
                categories[cat] = {
                    'jobs': [],
                    'probabilities': [],
                    'high_risk': 0,
                    'medium_risk': 0,
                    'low_risk': 0
                }
            
            categories[cat]['jobs'].append(result['name'])
            categories[cat]['probabilities'].append(result['probability'])
            
            if result['risk_level'] == "高风险":
                categories[cat]['high_risk'] += 1
            elif result['risk_level'] == "中风险":
                categories[cat]['medium_risk'] += 1
            else:
                categories[cat]['low_risk'] += 1
        
        # 计算平均值
        for cat in categories:
            probs = categories[cat]['probabilities']
            categories[cat]['avg_probability'] = round(sum(probs) / len(probs), 1)
            categories[cat]['total'] = len(probs)
        
        return categories


def load_jobs(filepath: str) -> List[Dict[str, Any]]:
    """加载职业数据"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['jobs']


def save_results(results: List[Dict[str, Any]], filepath: str):
    """保存预测结果"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    # 测试
    predictor = JobPredictor()
    jobs = load_jobs('data/jobs.json')
    results = predictor.predict_all(jobs)
    
    print("前 10 个高风险职业:")
    for i, r in enumerate(results[:10], 1):
        print(f"{i}. {r['name']} ({r['category']}): {r['probability']}% - {r['risk_level']}")
