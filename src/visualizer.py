#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 职业替代概率可视化工具

生成云图、热力图等可视化图表
"""

import json
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import numpy as np
import pandas as pd
from typing import List, Dict, Any
import os

# 现代配色方案
COLORS = {
    'low': '#10b981',
    'medium': '#f59e0b',
    'high': '#ef4444',
    'bg': '#ffffff',
    'grid': '#e5e7eb',
    'text': '#1f2937',
    'text_light': '#6b7280'
}

# 设置中文字体 - macOS 优先使用苹方
def setup_chinese_font():
    """设置中文字体支持"""
    # macOS 系统字体
    if os.name == 'posix' and 'Darwin' in os.popen('uname -a').read():
        font_list = ['PingFang SC', 'Heiti SC', 'STHeiti', 'Arial Unicode MS']
    else:
        font_list = ['Microsoft YaHei', 'SimHei', 'WenQuanYi Micro Hei']
    
    for font in font_list:
        try:
            matplotlib.rcParams['font.sans-serif'] = [font]
            matplotlib.rcParams['axes.unicode_minus'] = False
            return font
        except:
            continue
    
    # 最后方案：使用英文标签
    matplotlib.rcParams['font.sans-serif'] = ['DejaVu Sans']
    return None


class JobVisualizer:
    """职业替代概率可视化工具"""
    
    def __init__(self, results: List[Dict[str, Any]], output_dir: str = 'output'):
        self.results = results
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.font = setup_chinese_font()
        
        # 使用英文标签（避免字体问题）
        self.labels = {
            'title_cloud': 'AI Job Replacement Probability',
            'title_heatmap': 'Probability by Category',
            'title_bar': 'Average Risk by Category',
            'title_dist': 'Probability Distribution',
            'x_prob': 'Replacement Probability (%)',
            'x_avg': 'Average Probability (%)',
            'y_jobs': 'Jobs',
            'y_count': 'Number of Jobs',
            'low_risk': 'Low Risk',
            'mid_risk': 'Medium Risk',
            'high_risk': 'High Risk',
            'category': 'Category'
        }
        
        # 类别英文映射
        self.category_en = {
            '行政': 'Admin',
            '服务': 'Service',
            '技术': 'Tech',
            '医疗': 'Healthcare',
            '创意': 'Creative',
            '教育': 'Education',
            '金融': 'Finance',
            '制造': 'Manufacturing',
            '销售': 'Sales',
            '法律': 'Legal'
        }
        
    def create_cloud_map(self) -> str:
        """创建职业替代概率散点图"""
        names = [r['name'] for r in self.results]
        probs = [r['probability'] for r in self.results]
        categories = [r['category'] for r in self.results]
        
        colors = [COLORS['low'] if p < 30 else COLORS['medium'] if p < 60 else COLORS['high'] for p in probs]
        
        fig, ax = plt.subplots(figsize=(14, 12))
        
        # 按类别分组
        unique_categories = sorted(set(categories))
        y_current = 0
        
        for cat in unique_categories:
            cat_en = self.category_en.get(cat, cat)
            cat_jobs = [(i, names[i], probs[i]) for i, c in enumerate(categories) if c == cat]
            
            for idx, (i, name, prob) in enumerate(cat_jobs):
                y = y_current + idx
                size = 80 + (prob / 100) * 300
                ax.scatter(prob, y, s=size, c=colors[i], alpha=0.7, edgecolors='white', linewidth=1)
            
            # 类别标签（英文）
            if cat_jobs:
                mid_y = y_current + len(cat_jobs) / 2
                ax.text(-8, mid_y, cat_en, fontsize=10, fontweight='bold', 
                       va='center', ha='right', color=COLORS['text_light'])
            
            y_current += len(cat_jobs) + 0.5
        
        # 风险区域背景
        ax.axvspan(0, 30, alpha=0.1, color=COLORS['low'])
        ax.axvspan(30, 60, alpha=0.1, color=COLORS['medium'])
        ax.axvspan(60, 100, alpha=0.1, color=COLORS['high'])
        
        # 参考线
        ax.axvline(x=30, color=COLORS['low'], linestyle='--', alpha=0.6, linewidth=2)
        ax.axvline(x=60, color=COLORS['high'], linestyle='--', alpha=0.6, linewidth=2)
        
        ax.set_xlabel(self.labels['x_prob'], fontsize=12, fontweight='bold')
        ax.set_title(self.labels['title_cloud'], fontsize=14, fontweight='bold', pad=15)
        ax.set_xlim(-5, 105)
        ax.set_ylim(-1, len(names))
        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # 图例
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor=COLORS['low'], alpha=0.7, label=f'{self.labels["low_risk"]} (<30%)'),
            Patch(facecolor=COLORS['medium'], alpha=0.7, label=f'{self.labels["mid_risk"]} (30-60%)'),
            Patch(facecolor=COLORS['high'], alpha=0.7, label=f'{self.labels["high_risk"]} (>60%)')
        ]
        ax.legend(handles=legend_elements, loc='upper right', framealpha=0.9)
        
        plt.tight_layout()
        output_path = os.path.join(self.output_dir, 'job_replacement_cloud_map.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return output_path
    
    def create_heatmap(self) -> str:
        """创建类别 - 职业热力图"""
        data = []
        for r in self.results:
            cat_en = self.category_en.get(r['category'], r['category'])
            data.append({'job': r['name'], 'category': cat_en, 'prob': r['probability']})
        df = pd.DataFrame(data)
        
        # 按类别和概率排序
        df = df.sort_values(['category', 'prob'], ascending=[True, False])
        
        # 创建透视表
        pivot_table = df.pivot(index='job', columns='category', values='prob')
        
        fig, ax = plt.subplots(figsize=(14, 10))
        
        cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
            'custom_risk',
            [COLORS['low'], '#fbbf24', COLORS['high']],
            N=100
        )
        
        sns.heatmap(pivot_table.T, annot=False, cmap=cmap,
                   vmin=0, vmax=100, center=50,
                   cbar_kws={'label': 'Probability (%)', 'shrink': 0.8},
                   linewidths=0.5, linecolor='white',
                   ax=ax)
        
        ax.set_title(self.labels['title_heatmap'], fontsize=14, fontweight='bold', pad=15)
        ax.set_xlabel('Jobs', fontsize=11)
        ax.set_ylabel(self.labels['category'], fontsize=11)
        
        plt.tight_layout()
        output_path = os.path.join(self.output_dir, 'job_replacement_heatmap.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return output_path
    
    def create_category_bar_chart(self) -> str:
        """创建类别平均概率柱状图"""
        category_stats = {}
        for r in self.results:
            cat = r['category']
            if cat not in category_stats:
                category_stats[cat] = []
            category_stats[cat].append(r['probability'])
        
        category_avg = {cat: np.mean(probs) for cat, probs in category_stats.items()}
        sorted_cats = sorted(category_avg.items(), key=lambda x: x[1], reverse=True)
        
        # 使用英文类别名
        categories_en = [self.category_en.get(c[0], c[0]) for c in sorted_cats]
        averages = [c[1] for c in sorted_cats]
        colors = [COLORS['low'] if avg < 30 else COLORS['medium'] if avg < 60 else COLORS['high'] for avg in averages]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        bars = ax.barh(categories_en, averages, color=colors, edgecolor='white', linewidth=1.5)
        
        # 数值标签
        for bar, avg in zip(bars, averages):
            ax.text(avg + 1, bar.get_y() + bar.get_height()/2,
                   f'{avg:.0f}%', va='center', fontsize=10, fontweight='bold')
        
        ax.set_xlabel(self.labels['x_avg'], fontsize=11, fontweight='bold')
        ax.set_title(self.labels['title_bar'], fontsize=14, fontweight='bold', pad=15)
        ax.set_xlim(0, 100)
        
        # 参考线
        ax.axvline(x=30, color=COLORS['low'], linestyle='--', alpha=0.6, linewidth=2)
        ax.axvline(x=60, color=COLORS['high'], linestyle='--', alpha=0.6, linewidth=2)
        
        ax.grid(True, alpha=0.3, axis='x', linestyle='--')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        plt.tight_layout()
        output_path = os.path.join(self.output_dir, 'category_comparison.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return output_path
    
    def create_distribution_chart(self) -> str:
        """创建概率分布直方图"""
        probs = [r['probability'] for r in self.results]
        
        fig, ax = plt.subplots(figsize=(10, 5))
        
        bins = np.linspace(0, 100, 21)
        n, bins, patches = ax.hist(probs, bins=bins, edgecolor='white', linewidth=0.5, alpha=0.9)
        
        for i, patch in enumerate(patches):
            center = (bins[i] + bins[i+1]) / 2
            if center < 30:
                patch.set_facecolor(COLORS['low'])
            elif center < 60:
                patch.set_facecolor(COLORS['medium'])
            else:
                patch.set_facecolor(COLORS['high'])
        
        ax.set_xlabel(self.labels['x_prob'], fontsize=11, fontweight='bold')
        ax.set_ylabel(self.labels['y_count'], fontsize=11, fontweight='bold')
        ax.set_title(self.labels['title_dist'], fontsize=14, fontweight='bold', pad=15)
        
        # 参考线
        ax.axvline(x=30, color=COLORS['low'], linestyle='--', alpha=0.7, linewidth=2)
        ax.axvline(x=60, color=COLORS['high'], linestyle='--', alpha=0.7, linewidth=2)
        
        # 区域标签
        ax.text(15, max(n)*0.9, self.labels['low_risk'], color=COLORS['low'], 
               fontweight='bold', ha='center', fontsize=11)
        ax.text(45, max(n)*0.9, self.labels['mid_risk'], color='#b45309', 
               fontweight='bold', ha='center', fontsize=11)
        ax.text(80, max(n)*0.9, self.labels['high_risk'], color=COLORS['high'], 
               fontweight='bold', ha='center', fontsize=11)
        
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        plt.tight_layout()
        output_path = os.path.join(self.output_dir, 'probability_distribution.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return output_path
    
    def generate_all(self) -> List[str]:
        """生成所有图表"""
        paths = []
        
        print("生成云图...")
        paths.append(self.create_cloud_map())
        
        print("生成热力图...")
        paths.append(self.create_heatmap())
        
        print("生成类别对比图...")
        paths.append(self.create_category_bar_chart())
        
        print("生成分布图...")
        paths.append(self.create_distribution_chart())
        
        print(f"\n图表已保存到：{self.output_dir}/")
        return paths


if __name__ == '__main__':
    from predictor import load_jobs, JobPredictor
    
    jobs = load_jobs('data/jobs.json')
    predictor = JobPredictor()
    results = predictor.predict_all(jobs)
    
    visualizer = JobVisualizer(results)
    paths = visualizer.generate_all()
    
    print("\n生成的文件:")
    for p in paths:
        print(f"  - {p}")
