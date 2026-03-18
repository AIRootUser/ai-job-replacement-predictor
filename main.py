#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 职业替代概率预测器 - 主入口

预测 2-3 年后 AI 环境下各职业被替代的概率，并生成可视化图表。

使用方法:
    python main.py

输出:
    - output/job_replacement_cloud_map.png - 云图
    - output/job_replacement_heatmap.png - 热力图
    - output/category_comparison.png - 类别对比图
    - output/probability_distribution.png - 分布图
    - output/prediction_report.txt - 文本报告
    - output/predictions.json - 完整预测数据
"""

import json
import os
from datetime import datetime
from src.predictor import JobPredictor, load_jobs, save_results
from src.visualizer import JobVisualizer


def generate_report(results: list, category_stats: dict, output_path: str):
    """
    生成文本报告
    
    Args:
        results: 预测结果列表
        category_stats: 类别统计
        output_path: 输出路径
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("AI 职业替代概率预测报告 (2-3 年预测)\n")
        f.write("=" * 60 + "\n")
        f.write(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"分析职业数量：{len(results)}\n\n")
        
        # 高风险职业 TOP 10
        f.write("-" * 60 + "\n")
        f.write("🔴 高风险职业 TOP 10 (替代概率 > 60%)\n")
        f.write("-" * 60 + "\n")
        high_risk = [r for r in results if r['probability'] >= 60]
        for i, r in enumerate(high_risk[:10], 1):
            f.write(f"{i:2}. {r['name']:<15} ({r['category']:<6}) {r['probability']:5.1f}%\n")
        
        if not high_risk:
            f.write("无高风险职业\n")
        
        # 中风险职业
        f.write("\n" + "-" * 60 + "\n")
        f.write("🟡 中风险职业 (替代概率 30-60%)\n")
        f.write("-" * 60 + "\n")
        medium_risk = [r for r in results if 30 <= r['probability'] < 60]
        for i, r in enumerate(medium_risk[:15], 1):
            f.write(f"{i:2}. {r['name']:<15} ({r['category']:<6}) {r['probability']:5.1f}%\n")
        
        # 低风险职业
        f.write("\n" + "-" * 60 + "\n")
        f.write("🟢 低风险职业 TOP 10 (替代概率 < 30%)\n")
        f.write("-" * 60 + "\n")
        low_risk = [r for r in results if r['probability'] < 30]
        for i, r in enumerate(low_risk[:10], 1):
            f.write(f"{i:2}. {r['name']:<15} ({r['category']:<6}) {r['probability']:5.1f}%\n")
        
        if not low_risk:
            f.write("无低风险职业\n")
        
        # 类别统计
        f.write("\n" + "=" * 60 + "\n")
        f.write("各类别平均替代概率\n")
        f.write("=" * 60 + "\n")
        
        sorted_cats = sorted(
            [(cat, stats['avg_probability']) for cat, stats in category_stats.items()],
            key=lambda x: x[1],
            reverse=True
        )
        
        for cat, avg in sorted_cats:
            stats = category_stats[cat]
            risk_indicator = "🔴" if avg >= 60 else "🟡" if avg >= 30 else "🟢"
            f.write(f"{risk_indicator} {cat:<10} 平均：{avg:5.1f}% (职业数：{stats['total']})\n")
        
        # 评估维度说明
        f.write("\n" + "=" * 60 + "\n")
        f.write("评估维度说明\n")
        f.write("=" * 60 + "\n")
        f.write("""
维度说明 (评分 0-10 分):
- 创造性 (creativity): 工作需要创造力的程度，越高越难被替代
- 社交互动 (social_interaction): 与人交流的程度，越高越难被替代
- 重复性 (repetition): 工作重复性程度，越高越容易被替代
- 技术依赖性 (technical_dependency): 依赖技术的程度，越高越容易被替代
- 精细操作 (physical_dexterity): 需要精细手工操作的程度，越高越难被替代
- 批判性思维 (critical_thinking): 需要复杂思考的程度，越高越难被替代
- 情商需求 (emotional_intelligence): 需要情感理解的程度，越高越难被替代
""")
        
        # 免责声明
        f.write("\n" + "=" * 60 + "\n")
        f.write("免责声明\n")
        f.write("=" * 60 + "\n")
        f.write("""
1. 本预测基于当前 AI 技术发展趋势的假设，实际结果可能因技术突破、
   政策变化、社会接受度等因素而有所不同。

2. 预测结果仅供参考，不构成职业规划或投资建议。

3. "替代概率"指的是工作内容被 AI 自动化的可能性，不代表职业完全消失。
   许多职业会转变为"人机协作"模式。

4. 评估维度和权重基于一般性分析，具体职业情况可能有所不同。

5. 数据更新时间：2026 年 3 月
""")


def main():
    """主函数"""
    print("=" * 60)
    print("AI 职业替代概率预测器")
    print("=" * 60)
    print()
    
    # 创建输出目录
    os.makedirs('output', exist_ok=True)
    
    # 加载数据
    print("📊 加载职业数据...")
    jobs = load_jobs('data/jobs.json')
    print(f"   共加载 {len(jobs)} 个职业")
    
    # 预测
    print("\n🔮 进行预测分析...")
    predictor = JobPredictor()
    results = predictor.predict_all(jobs)
    category_stats = predictor.get_category_stats(results)
    
    # 保存预测结果
    save_path = 'output/predictions.json'
    save_results(results, save_path)
    print(f"   预测结果已保存到：{save_path}")
    
    # 生成可视化
    print("\n📈 生成可视化图表...")
    visualizer = JobVisualizer(results)
    chart_paths = visualizer.generate_all()
    
    # 生成报告
    print("\n📝 生成文本报告...")
    report_path = 'output/prediction_report.txt'
    generate_report(results, category_stats, report_path)
    print(f"   报告已保存到：{report_path}")
    
    # 打印摘要
    print("\n" + "=" * 60)
    print("预测摘要")
    print("=" * 60)
    
    high_risk = [r for r in results if r['probability'] >= 60]
    medium_risk = [r for r in results if 30 <= r['probability'] < 60]
    low_risk = [r for r in results if r['probability'] < 30]
    
    print(f"高风险职业 (≥60%):  {len(high_risk)} 个")
    print(f"中风险职业 (30-60%): {len(medium_risk)} 个")
    print(f"低风险职业 (<30%):  {len(low_risk)} 个")
    
    print("\n🔴 风险最高的 5 个职业:")
    for i, r in enumerate(results[:5], 1):
        print(f"   {i}. {r['name']} ({r['category']}): {r['probability']}%")
    
    print("\n🟢 风险最低的 5 个职业:")
    for i, r in enumerate(results[-5:], 1):
        print(f"   {i}. {r['name']} ({r['category']}): {r['probability']}%")
    
    print("\n" + "=" * 60)
    print("✅ 分析完成！")
    print("=" * 60)
    print("\n生成的文件:")
    print("  📊 output/predictions.json - 完整预测数据")
    print("  📝 output/prediction_report.txt - 文本报告")
    for path in chart_paths:
        print(f"  🖼️  {path}")
    
    return results


if __name__ == '__main__':
    main()
