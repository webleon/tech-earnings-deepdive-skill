# 📊 Tech Earnings Deep Dive

**机构级科技股财报深度分析系统** · 基于 Day1Global 框架

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)

---

## 🚀 快速开始

### 安装

```bash
# 1. 克隆仓库
git clone https://github.com/webleon/tech-earnings-deepdive-openclaw-skill.git
cd tech-earnings-deepdive-openclaw-skill

# 2. 安装依赖
pip3 install yfinance pandas numpy requests edgartools

# 3. 运行
python3 analyze.py AAPL           # 单股分析
python3 analyze_batch.py NVDA AMD # 批量对比
```

### 输出

- **个股报告**: `~/.openclaw/workspace/output/tech-earnings-deepdive/`
- **对比报告**: `~/.openclaw/workspace/output/tech-earnings-deepdive/batch/`

---

## 📖 核心功能

| 功能 | 说明 | 状态 |
|------|------|------|
| **16 模块分析** | 收入质量、盈利能力、现金流等 16 维度 | ✅ |
| **6 大投资视角** | 巴菲特/芒格/Baillie Gifford 等大师视角 | ✅ |
| **6 种估值方法** | Owner Earnings/PEG/Reverse DCF 等 | ✅ |
| **MSCI Barra** | 质量/成长/价值/情绪/宏观/ESG 六因子 | ✅ |
| **反偏见框架** | 认知陷阱/财务红旗检查 | ✅ |
| **HTML 报告** | 专业格式投资备忘录 | ✅ |

---

## 📊 数据来源

| 数据源 | 用途 | 权威性 |
|--------|------|--------|
| **Yahoo Finance** | 股价、财报、分析师评级 | ⭐⭐⭐⭐⭐ |
| **SEC EDGAR** | 内部人交易、机构持仓、10-K/Q | ⭐⭐⭐⭐⭐ |

---

## 🔗 相关文档

| 文档 | 说明 |
|------|------|
| [技术架构](docs/ARCHITECTURE.md) | 系统架构、模块设计、评分算法 |
| [数据准确性](docs/DATA_ACCURACY.md) | 数据验证和准确性说明 |
| [变更日志](CHANGELOG.md) | 版本更新记录 |

---

## 🙏 致谢

**本项目完全基于 [Day1Global-Skills](https://github.com/star23/Day1Global-Skills) 框架开发**

特别感谢 **Day1Global 团队（Star & Ruby）** 提供原始框架、方法论指导和开源精神。

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

## ⚠️ 免责声明

本工具仅供学习和研究使用，不构成投资建议。投资有风险，决策需谨慎。
