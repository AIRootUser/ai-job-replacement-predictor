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
    'low': '#10b981',      # 翠绿 - 低风险
    'medium': '#f59e0b',   # 琥珀 - 中风险
    'high': '#ef4444',     # 红 - 高风险
    'bg': '#ffffff',
    'grid': '#e5e7eb',
    'text': '#1f2937',
    'text_light': '#6b7280'
}

# 设置中文字体
def setup_chinese_font():
    """设置中文字体支持"""
    chinese_fonts = [
        'PingFang SC',
        'Microsoft YaHei',
        'SimHei',
        'Heiti TC',
        'Noto Sans CJK SC'
    ]
    
    for font in chinese_fonts:
        try:
            matplotlib.rcParams['font.sans-serif'] = [font]
            matplotlib.rcParams['axes.unicode_minus'] = False
            matplotlib.rcParams['font.size'] = 10
            return font
        except:
            continue
    
    matplotlib.rcParams['font.sans-serif'] = ['DejaVu Sans']
    return 'DejaVu Sans'


class JobVisualizer:
    """职业替代概率可视化工具"""
    
    def __init__(self, results: List[Dict[str, Any]], output_dir: str = 'output'):
        self.results = results
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.font = setup_chinese_font()
        
        # 设置现代样式
        plt.style.use('seaborn-v0_8-whitegrid')
        sns.set_palette([COLORS['low'], COLORS['medium'], COLORS['high']])
        
    def create_cloud_map(self) -> str:
        """创建职业替代概率散点图"""
        names = [r['name'] for r in self.results]
        probs = [r['probability'] for r in self.results]
        categories = [r['category'] for r in self.results]
        
        # 颜色映射
        colors = [COLORS['low'] if p < 30 else COLORS['medium'] if p < 60 else COLORS['high'] for p in probs]
        
        fig, ax = plt.subplots(figsize=(14, 16))
        
        # 按类别分组绘制
        unique_categories = sorted(set(categories))
        y_positions = {}
        y_current = 0
        
        for cat in unique_categories:
            cat_jobs = [(i, names[i], probs[i]) for i, c in enumerate(categories) if c == cat]
            y_positions[cat] = (y_current, y_current + len(cat_jobs))
            
            for idx, (i, name, prob) in enumerate(cat_jobs):
                y = y_current + idx
                size = 100 + (prob / 100) * 400
                ax.scatter(prob, y, s=size, c=colors[i], alpha=0.8, edgecolors='white', linewidth=1.5)
                ax.annotate(name, (prob, y), xytext=(8, 0), textcoords='offset points',
                           va='center', fontsize=9, color=COLORS['text'])
            
            y_current += len(cat_jobs) + 0.8
        
        # 风险区域背景
        ax.axvspan(0, 30, alpha=0.08, color=COLORS['low'])
        ax.axvspan(30, 60, alpha=0.08, color=COLORS['medium'])
        ax.axvspan(60, 100, alpha=0.08, color=COLORS['high'])
        
        # 参考线
        ax.axvline(x=30, color=COLORS['low'], linestyle='--', alpha=0.5, linewidth=1.5)
        ax.axvline(x=60, color=COLORS['high'], linestyle='--', alpha=0.5, linewidth=1.5)
        
        ax.set_xlabel('AI 替代概率 (%)', fontsize=11, fontweight='bold', color=COLORS['text'])
        ax.set_title('AI 职业替代概率分布 (2-3 年预测)', fontsize=16, fontweight='bold', pad=20, color=COLORS['text'])
        ax.set_xlim(-5, 105)
        ax.set_ylim(-1, len(names))
        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # 风险标签
        ax.text(15, -0.8, '🟢 低风险', color=COLORS['low'], fontweight='bold', ha='center', fontsize=10)
        ax.text(45, -0.8, '🟡 中风险', color=COLORS['medium'], fontweight='bold', ha='center', fontsize=10)
        ax.text(80, -0.8, '🔴 高风险', color=COLORS['high'], fontweight='bold', ha='center', fontsize=10)
        
        plt.tight_layout()
        output_path = os.path.join(self.output_dir, 'job_replacement_cloud_map.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return output_path
    
    def create_heatmap(self) -> str:
        """创建类别 - 职业热力图"""
        data = [{'职业': r['name'], '类别': r['category'], '概率': r['probability']} for r in self.results]
        df = pd.DataFrame(data)
        
        # 按类别和概率排序
        df = df.sort_values(['类别', '概率'], ascending=[True, False])
        
        # 创建透视表
        pivot_table = df.pivot(index='职业', columns='类别', values='概率')
        
        fig, ax = plt.subplots(figsize=(12, 14))
        
        # 自定义配色
        cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
            'custom_risk',
            [COLORS['low'], '#fbbf24', COLORS['high']],
            N=100
        )
        
        # 热力图
        sns.heatmap(pivot_table.T, annot=True, fmt='.0f', cmap=cmap,
                   vmin=0, vmax=100, center=50,
                   cbar_kws={'label': '替代概率 (%)', 'shrink': 0.8},
                   linewidths=0.5, linecolor='white',
                   ax=ax, annot_kws={'size': 8, 'weight': 'bold'})
        
        ax.set_title('AI 职业替代概率热力图', fontsize=15, fontweight='bold', pad=20, color=COLORS['text'])
        ax.set_xlabel('职业', fontsize=11, color=COLORS['text'])
        ax.set_ylabel('类别', fontsize=11, color=COLORS['text'])
        
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
        categories = [c[0] for c in sorted_cats]
        averages = [c[1] for c in sorted_cats]
        
        # 柱状颜色
        colors = [COLORS['low'] if avg < 30 else COLORS['medium'] if avg < 60 else COLORS['high'] for avg in averages]
        
        fig, ax = plt.subplots(figsize=(12, 7))
        
        bars = ax.barh(categories, averages, color=colors, edgecolor='white', linewidth=1.5)
        
        # 数值标签
        for bar, avg in zip(bars, averages):
            ax.text(avg + 1.5, bar.get_y() + bar.get_height()/2,
                   f'{avg:.1f}%', va='center', fontsize=10, fontweight='bold', color=COLORS['text'])
        
        ax.set_xlabel('平均替代概率 (%)', fontsize=11, fontweight='bold', color=COLORS['text'])
        ax.set_title('各类别 AI 替代概率对比', fontsize=15, fontweight='bold', pad=20, color=COLORS['text'])
        ax.set_xlim(0, 100)
        
        # 参考线
        ax.axvline(x=30, color=COLORS['low'], linestyle='--', alpha=0.6, linewidth=1.5)
        ax.axvline(x=60, color=COLORS['high'], linestyle='--', alpha=0.6, linewidth=1.5)
        
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
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # 分段着色
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
        
        ax.set_xlabel('AI 替代概率 (%)', fontsize=11, fontweight='bold', color=COLORS['text'])
        ax.set_ylabel('职业数量', fontsize=11, fontweight='bold', color=COLORS['text'])
        ax.set_title('职业替代概率分布', fontsize=15, fontweight='bold', pad=20, color=COLORS['text'])
        
        # 参考线
        ax.axvline(x=30, color=COLORS['low'], linestyle='--', alpha=0.7, linewidth=2)
        ax.axvline(x=60, color=COLORS['high'], linestyle='--', alpha=0.7, linewidth=2)
        
        ax.text(15, max(n)*0.9, '低风险', color=COLORS['low'], fontweight='bold', ha='center', fontsize=11)
        ax.text(45, max(n)*0.9, '中风险', color='#b45309', fontweight='bold', ha='center', fontsize=11)
        ax.text(80, max(n)*0.9, '高风险', color=COLORS['high'], fontweight='bold', ha='center', fontsize=11)
        
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
