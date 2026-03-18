# AI 职业替代概率预测器

<div align="center">

**预测 2-3 年后 AI 环境下各职业被替代的概率**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[English](#english) | 简体中文

</div>

---

## 📖 项目介绍

本项目通过分析职业的 7 个关键维度，预测在 AI 技术快速发展背景下，各职业在未来 2-3 年内被自动化替代的概率。

### 评估维度

| 维度 | 说明 | 对替代概率的影响 |
|------|------|------------------|
| 创造性 (creativity) | 工作需要创造力的程度 | 越高越难被替代 ↓ |
| 社交互动 (social_interaction) | 与人交流的程度 | 越高越难被替代 ↓ |
| 重复性 (repetition) | 工作重复性程度 | 越高越容易被替代 ↑ |
| 技术依赖性 (technical_dependency) | 依赖技术的程度 | 越高越容易被替代 ↑ |
| 精细操作 (physical_dexterity) | 需要精细手工操作的程度 | 越高越难被替代 ↓ |
| 批判性思维 (critical_thinking) | 需要复杂思考的程度 | 越高越难被替代 ↓ |
| 情商需求 (emotional_intelligence) | 需要情感理解的程度 | 越高越难被替代 ↓ |

### 风险等级

- 🟢 **低风险 (<30%)**: AI 难以替代，人类优势明显
- 🟡 **中风险 (30-60%)**: 部分工作可能被自动化，人机协作趋势
- 🔴 **高风险 (>60%)**: 大部分工作内容可能被 AI 替代

---

## 🚀 快速开始

### 安装依赖

```bash
# 创建虚拟环境（可选）
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 运行预测

```bash
python main.py
```

### 输出文件

运行后会在 `output/` 目录生成以下文件：

| 文件 | 说明 |
|------|------|
| `predictions.json` | 完整预测数据 (JSON 格式) |
| `prediction_report.txt` | 文本报告 |
| `job_replacement_cloud_map.png` | 职业云图 |
| `job_replacement_heatmap.png` | 类别热力图 |
| `category_comparison.png` | 类别对比柱状图 |
| `probability_distribution.png` | 概率分布直方图 |

---

## 📊 示例输出

### 高风险职业示例

```
1. 数据录入员 (行政): 85.0%
2. 流水线工人 (制造): 82.5%
3. 银行柜员 (金融): 75.0%
4. 电话客服 (服务): 72.5%
5. 清洁工 (服务): 70.0%
```

### 低风险职业示例

```
1. 音乐家 (创意): 12.5%
2. 作家 (创意): 15.0%
3. 心理咨询师 (医疗): 17.5%
4. 社会工作者 (服务): 18.0%
5. 演员 (创意): 20.0%
```

---

## 🔧 自定义配置

### 调整权重

编辑 `src/predictor.py` 中的权重配置：

```python
self.weights = {
    'creativity': -0.15,           # 创造性权重
    'social_interaction': -0.15,   # 社交互动权重
    'repetition': 0.25,            # 重复性权重
    'technical_dependency': 0.15,  # 技术依赖权重
    'physical_dexterity': -0.10,   # 精细操作权重
    'critical_thinking': -0.10,    # 批判思维权重
    'emotional_intelligence': -0.10  # 情商权重
}
```

### 添加新职业

编辑 `data/jobs.json`，添加新的职业数据：

```json
{
  "name": "职业名称",
  "category": "类别",
  "skills": ["技能 1", "技能 2"],
  "dimensions": {
    "creativity": 5,
    "social_interaction": 6,
    "repetition": 4,
    "technical_dependency": 7,
    "physical_dexterity": 3,
    "critical_thinking": 6,
    "emotional_intelligence": 5
  }
}
```

---

## 📁 项目结构

```
ai-job-replacement-predictor/
├── data/
│   └── jobs.json              # 职业数据
├── src/
│   ├── predictor.py           # 预测算法
│   └── visualizer.py          # 可视化工具
├── output/                    # 输出目录（运行后生成）
├── main.py                    # 主入口
├── requirements.txt           # 依赖列表
└── README.md                  # 说明文档
```

---

## ⚠️ 免责声明

1. **预测性质**: 本预测基于当前 AI 技术发展趋势的假设，实际结果可能因技术突破、政策变化、社会接受度等因素而有所不同。

2. **参考用途**: 预测结果仅供参考，不构成职业规划或投资建议。

3. **替代定义**: "替代概率"指的是工作内容被 AI 自动化的可能性，不代表职业完全消失。许多职业会转变为"人机协作"模式。

4. **评估局限**: 评估维度和权重基于一般性分析，具体职业情况可能有所不同。

5. **数据时效**: 数据基于 2026 年的技术认知，建议定期更新评估。

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

- 添加更多职业数据
- 改进评估算法
- 优化可视化效果
- 提供反馈和建议

---

## 📄 许可证

MIT License

---

## 📬 联系方式

如有问题或建议，请提交 Issue。

---

# English

## 📖 Introduction

This project predicts the probability of various occupations being automated by AI in the next 2-3 years, based on analysis of 7 key dimensions.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run prediction
python main.py
```

## 📊 Output Files

| File | Description |
|------|-------------|
| `predictions.json` | Complete prediction data (JSON) |
| `prediction_report.txt` | Text report |
| `job_replacement_cloud_map.png` | Job cloud map |
| `job_replacement_heatmap.png` | Category heatmap |
| `category_comparison.png` | Category comparison chart |
| `probability_distribution.png` | Probability distribution |

## 🔧 Customization

### Adjust Weights

Edit weights in `src/predictor.py`:

```python
self.weights = {
    'creativity': -0.15,
    'social_interaction': -0.15,
    'repetition': 0.25,
    'technical_dependency': 0.15,
    'physical_dexterity': -0.10,
    'critical_thinking': -0.10,
    'emotional_intelligence': -0.10
}
```

### Add New Jobs

Edit `data/jobs.json` to add new occupations.

## ⚠️ Disclaimer

Predictions are based on current AI technology trends and should be used for reference only. Actual outcomes may vary due to technological breakthroughs, policy changes, and social factors.

---

**Generated:** 2026-03-17
