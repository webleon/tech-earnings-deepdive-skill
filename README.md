# 📊 Tech Earnings Deep Dive

**机构级科技股财报深度分析系统**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🚀 快速开始

```bash
# 1. 克隆
git clone https://github.com/webleon/tech-earnings-deepdive-openclaw-skill.git
cd tech-earnings-deepdive-openclaw-skill

# 2. 安装依赖
pip3 install yfinance pandas numpy requests edgartools

# 3. 运行
python3 analyze.py AAPL           # 单股
python3 analyze_batch.py NVDA AMD # 批量
```

**输出**: `~/.openclaw/workspace/output/tech-earnings-deepdive/`

---

## 📖 核心功能

| 功能 | 说明 |
|------|------|
| **16 模块分析** | 收入/盈利/现金流/竞争等 16 维度 |
| **6 大投资视角** | 巴菲特/芒格/Baillie Gifford 等大师视角 |
| **6 种估值方法** | Owner Earnings/PEG/Reverse DCF 等 |
| **MSCI Barra** | 质量/成长/价值/情绪/宏观/ESG 六因子 |
| **反偏见框架** | 认知陷阱/财务红旗检查 |
| **HTML 报告** | 专业格式投资备忘录 |

---

## 📚 完整文档

查看 [docs/GUIDE.md](docs/GUIDE.md) 了解：
- 详细功能说明
- 使用指南
- 技术架构
- 评分算法
- 扩展开发

---

## 🙏 致谢

基于 [Day1Global-Skills](https://github.com/star23/Day1Global-Skills) 框架开发

---

## 📄 许可证

MIT License

## ⚠️ 免责声明

本工具仅供学习研究，不构成投资建议。
