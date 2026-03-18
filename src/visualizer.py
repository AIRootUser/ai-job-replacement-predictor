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

# 设置中文字体
def setup_chinese_font():
    """设置中文字体支持"""
    # 尝试多种中文字体
    chinese_fonts = [
        'SimHei',           # 黑体 (Windows)
        'Microsoft YaHei',  # 微软雅黑 (Windows)
        'PingFang SC',      # 苹方 (macOS)
        'Heiti TC',         # 黑体繁体 (macOS)
        'WenQuanYi Micro Hei',  # 文泉驿 (Linux)
        'Noto Sans CJK SC'  # Noto (跨平台)
    ]
    
    for font in chinese_fonts:
        try:
            matplotlib.rcParams['font.sans-serif'] = [font]
            matplotlib.rcParams['axes.unicode_minus'] = False
            print(f"使用字体：{font}")
            return font
        except:
            continue
    
    # 如果都没有，使用默认
    matplotlib.rcParams['font.sans-serif'] = ['DejaVu Sans']
    print("警告：未找到中文字体，使用默认字体")
    return 'DejaVu Sans'


class JobVisualizer:
    """职业替代概率可视化工具"""
    
    def __init__(self, results: List[Dict[str, Any]], output_dir: str = 'output'):
        """
        初始化可视化工具
        
        Args:
            results: 预测结果列表
            output_dir: 输出目录
        """
        self.results = results
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.font = setup_chinese_font()
        
    def create_cloud_map(self) -> str:
        """
        创建云图（词云风格的热力图）
        
        Returns:
            输出文件路径
        """
        # 准备数据
        names = [r['name'] for r in self.results]
        probs = [r['probability'] for r in self.results]
        categories = [r['category'] for r in self.results]
        
        # 创建颜色映射
        colors = []
        for p in probs:
            if p < 30:
                colors.append('#2ecc71')  # 绿色 - 低风险
            elif p < 60:
                colors.append('#f1c40f')  # 黄色 - 中风险
            else:
                colors.append('#e74c3c')  # 红色 - 高风险
        
        # 创建图表
        fig, ax = plt.subplots(figsize=(16, 20))
        
        # 按类别分组
        unique_categories = list(set(categories))
        y_pos = 0
        y_positions = []
        
        for cat in sorted(unique_categories):
            cat_indices = [i for i, c in enumerate(categories) if c == cat]
            
            # 绘制类别标签
            ax.text(-0.15, y_pos + len(cat_indices)/2, cat, 
                   transform=ax.transAxes, fontsize=12, 
                   fontweight='bold', va='center', ha='right')
            
            # 绘制该类别的职业
            for idx in cat_indices:
                y_positions.append(y_pos)
                y_pos += 1
            
            y_pos += 0.5  # 类别间间距
        
        # 创建散点图（词云效果）
        sizes = [(p / 100) * 500 + 100 for p in probs]  # 字体大小与概率相关
        
        scatter = ax.scatter(
            probs, 
            range(len(names)),
            s=sizes,
            c=colors,
            alpha=0.7,
            edgecolors='white',
            linewidths=1
        )
        
        # 添加职业名称标签
        for i, (name, prob, y) in enumerate(zip(names, probs, range(len(names)))):
            ax.annotate(name, 
                       xy=(prob, y),
                       xytext=(5, 0),
                       textcoords='offset points',
                       fontsize=9,
                       va='center',
                       alpha=0.9)
        
        ax.set_xlabel('AI 替代概率 (%)', fontsize=12, fontweight='bold')
        ax.set_title('AI 职业替代概率云图 (2-3 年预测)', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlim(-5, 105)
        ax.set_ylim(-1, len(names))
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # 添加风险区域背景
        ax.axvspan(0, 30, alpha=0.1, color='green', label='低风险 (<30%)')
        ax.axvspan(30, 60, alpha=0.1, color='yellow', label='中风险 (30-60%)')
        ax.axvspan(60, 100, alpha=0.1, color='red', label='高风险 (>60%)')
        
        # 添加图例
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#2ecc71', label='低风险 (<30%)'),
            Patch(facecolor='#f1c40f', label='中风险 (30-60%)'),
            Patch(facecolor='#e74c3c', label='高风险 (>60%)')
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        
        plt.tight_layout()
        
        # 保存图片
        output_path = os.path.join(self.output_dir, 'job_replacement_cloud_map.png')
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def create_heatmap(self) -> str:
        """
        创建热力图（按类别和概率）
        
        Returns:
            输出文件路径
        """
        # 准备数据
        data = []
        for r in self.results:
            data.append({
                '职业': r['name'],
                '类别': r['category'],
                '概率': r['probability'],
                '风险等级': r['risk_level']
            })
        
        df = pd.DataFrame(data)
        
        # 按类别和概率排序
        df = df.sort_values(['类别', '概率'], ascending=[True, False])
        
        # 创建透视表
        pivot_data = []
        categories = df['类别'].unique()
        
        for cat in sorted(categories):
            cat_jobs = df[df['类别'] == cat]
            for _, row in cat_jobs.iterrows():
                pivot_data.append({
                    '类别': cat,
                    '职业': row['职业'],
                    '概率': row['概率']
                })
        
        pivot_df = pd.DataFrame(pivot_data)
        
        # 创建图表
        fig, ax = plt.subplots(figsize=(14, 16))
        
        # 创建热力图
        pivot_table = pivot_df.pivot(index='职业', columns='类别', values='概率')
        
        # 自定义颜色映射
        cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
            'risk_colors', 
            ['#2ecc71', '#f1c40f', '#e74c3c'],
            N=256
        )
        
        sns.heatmap(pivot_table.T, 
                   annot=True, 
                   fmt='.1f',
                   cmap=cmap,
                   vmin=0, 
                   vmax=100,
                   center=50,
                   cbar_kws={'label': '替代概率 (%)'},
                   ax=ax,
                   linewidths=0.5,
                   linecolor='gray')
        
        ax.set_title('AI 职业替代概率热力图 (按类别)', fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('职业', fontsize=11)
        ax.set_ylabel('类别', fontsize=11)
        
        plt.tight_layout()
        
        # 保存图片
        output_path = os.path.join(self.output_dir, 'job_replacement_heatmap.png')
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def create_category_bar_chart(self) -> str:
        """
        创建类别平均概率柱状图
        
        Returns:
            输出文件路径
        """
        # 计算类别平均值
        category_stats = {}
        for r in self.results:
            cat = r['category']
            if cat not in category_stats:
                category_stats[cat] = []
            category_stats[cat].append(r['probability'])
        
        category_avg = {cat: np.mean(probs) for cat, probs in category_stats.items()}
        
        # 排序
        sorted_cats = sorted(category_avg.items(), key=lambda x: x[1], reverse=True)
        categories = [c[0] for c in sorted_cats]
        averages = [c[1] for c in sorted_cats]
        
        # 创建图表
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # 颜色根据风险等级
        colors = []
        for avg in averages:
            if avg < 30:
                colors.append('#2ecc71')
            elif avg < 60:
                colors.append('#f1c40f')
            else:
                colors.append('#e74c3c')
        
        bars = ax.barh(categories, averages, color=colors, edgecolor='black', linewidth=0.5)
        
        # 添加数值标签
        for bar, avg in zip(bars, averages):
            ax.text(avg + 1, bar.get_y() + bar.get_height()/2, 
                   f'{avg:.1f}%', va='center', fontsize=10, fontweight='bold')
        
        ax.set_xlabel('平均替代概率 (%)', fontsize=12, fontweight='bold')
        ax.set_title('各类别 AI 替代概率对比', fontsize=14, fontweight='bold')
        ax.set_xlim(0, 100)
        
        # 添加参考线
        ax.axvline(x=30, color='green', linestyle='--', alpha=0.5, label='低风险线')
        ax.axvline(x=60, color='red', linestyle='--', alpha=0.5, label='高风险线')
        
        ax.legend()
        ax.grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        
        # 保存图片
        output_path = os.path.join(self.output_dir, 'category_comparison.png')
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def create_distribution_chart(self) -> str:
        """
        创建概率分布直方图
        
        Returns:
            输出文件路径
        """
        probs = [r['probability'] for r in self.results]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # 直方图
        n, bins, patches = ax.hist(probs, bins=20, edgecolor='black', alpha=0.7)
        
        # 根据风险等级设置颜色
        for i, patch in enumerate(patches):
            center = (bins[i] + bins[i+1]) / 2
            if center < 30:
                patch.set_facecolor('#2ecc71')
            elif center < 60:
                patch.set_facecolor('#f1c40f')
            else:
                patch.set_facecolor('#e74c3c')
        
        ax.set_xlabel('AI 替代概率 (%)', fontsize=12, fontweight='bold')
        ax.set_ylabel('职业数量', fontsize=12, fontweight='bold')
        ax.set_title('职业替代概率分布', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        
        # 添加风险区域标注
        ax.axvline(x=30, color='green', linestyle='--', alpha=0.7, linewidth=2)
        ax.axvline(x=60, color='red', linestyle='--', alpha=0.7, linewidth=2)
        ax.text(15, max(n)*0.9, '低风险', color='green', fontweight='bold', ha='center')
        ax.text(45, max(n)*0.9, '中风险', color='#b7950b', fontweight='bold', ha='center')
        ax.text(80, max(n)*0.9, '高风险', color='red', fontweight='bold', ha='center')
        
        plt.tight_layout()
        
        # 保存图片
        output_path = os.path.join(self.output_dir, 'probability_distribution.png')
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def generate_all(self) -> List[str]:
        """
        生成所有图表
        
        Returns:
            输出文件路径列表
        """
        paths = []
        
        print("正在生成云图...")
        paths.append(self.create_cloud_map())
        
        print("正在生成热力图...")
        paths.append(self.create_heatmap())
        
        print("正在生成类别对比图...")
        paths.append(self.create_category_bar_chart())
        
        print("正在生成分布图...")
        paths.append(self.create_distribution_chart())
        
        print(f"\n所有图表已保存到：{self.output_dir}/")
        return paths


if __name__ == '__main__':
    # 测试
    from predictor import load_jobs, JobPredictor
    
    jobs = load_jobs('data/jobs.json')
    predictor = JobPredictor()
    results = predictor.predict_all(jobs)
    
    visualizer = JobVisualizer(results)
    paths = visualizer.generate_all()
    
    print("\n生成的文件:")
    for p in paths:
        print(f"  - {p}")
