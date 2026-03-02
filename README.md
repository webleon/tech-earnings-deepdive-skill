# Tech Earnings Deep Dive Skill

科技股财报深度分析与多视角投资备忘录系统

Institutional-Grade Tech Stock Earnings Analysis & Multi-Perspective Investment Memo System

基于 Day1Global 框架 · 复刻专业投资机构分析方法论

Based on Day1Global Framework · Replicating Professional Investment Analysis Methodology

---

## 🌐 语言切换 / Language Switch

- [🇨🇳 中文版本](#-系统概述)
- [🇺🇸 English Version](#-system-overview)

---

## 🎯 系统概述 / System Overview

Tech Earnings Deep Dive 是一个为 AI 助手打造的机构级投资分析系统，专为科技股财报深度分析设计。系统完整复刻了专业投资机构的研究方法论，提供从数据获取、多维度分析到报告生成的全流程自动化解决方案。

Tech Earnings Deep Dive is an institutional-grade investment analysis system built for AI assistants, specifically designed for deep analysis of tech stock earnings. The system fully replicates professional investment research methodologies, providing a fully automated solution from data acquisition to multi-dimensional analysis and report generation.

通过整合 **16 大分析模块**、**6 大投资哲学视角**、**6 种估值方法**，配合反偏见框架和 Pre-Mortem 事前尸检工具，帮助投资者做出更理性、更全面、更可靠的投资决策。

By integrating **16 Analysis Modules**, **6 Investment Philosophy Perspectives**, and **6 Valuation Methods**, along with anti-bias frameworks and Pre-Mortem tools, it helps investors make more rational, comprehensive, and reliable investment decisions.

---

## 🚀 快速开始 / Quick Start

### 方法 1：命令行调用 / Method 1: Command Line

```bash
# 基本用法 / Basic Usage
~/.openclaw/workspace/skills/tech-earnings-deepdive/run.sh NVDA

# 完整报告 / Full Report
~/.openclaw/workspace/skills/tech-earnings-deepdive/run.sh TSLA --full

# 指定投资视角 / Specify Investment Perspective
~/.openclaw/workspace/skills/tech-earnings-deepdive/run.sh MSFT --perspective buffett
```

### 方法 2：在对话中使用 / Method 2: In Conversation

直接在对话中询问：
Ask directly in conversation:

- "帮我深度分析一下 NVDA 最新一季的财报"
- "Analyze NVDA's latest quarterly earnings in depth"

- "TSLA 这季度财报出来了，帮我做个全面的 deep dive"
- "TSLA just reported earnings, do a comprehensive deep dive"

- "从多个投资大师的视角帮我看看 MSFT，现在值得买入吗？"
- "Analyze MSFT from multiple investment masters' perspectives, is it worth buying now?"

---

## 📁 模块架构 / Module Architecture

```
tech-earnings-deepdive/
├── modules/
│   ├── fetch_data.py          # 数据获取 / Data Acquisition
│   ├── analyze_full.py        # 16 模块分析 / 16-Module Analysis
│   ├── perspectives_full.py   # 6 大视角评分 / 6 Perspectives Scoring
│   ├── valuation_full.py      # 6 种估值方法 / 6 Valuation Methods
│   ├── key_forces.py          # Key Forces 识别 / Key Forces Identification
│   ├── bias_framework.py      # 反偏见框架 / Anti-Bias Framework
│   ├── variant_view.py        # Variant View 生成 / Variant View Generation
│   ├── batch_analysis.py      # 批量分析 / Batch Analysis
│   └── export_report.py       # 报告导出 / Report Export
├── SKILL.md                   # Skill 配置文件 / Skill Config
├── config.json                # 运行时配置 / Runtime Config
└── run.sh                     # 命令行入口 / Command Line Entry
```

---

## 🔍 核心功能详解 / Core Features

### 1️⃣ 数据获取层 / Data Acquisition Layer

| 数据类型 / Data Type | 数据源 / Source | 获取内容 / Content | 状态 / Status |
|---------|--------|---------|--------|
| **股价数据** / Stock Price | yfinance API | 当前股价、市值、PE、52 周区间 | ✅ 已实现 |
| **财报数据** / Financials | yfinance API | 营收、净利润、毛利率、运营利润 | ✅ 已实现 |
| **资产负债表** / Balance Sheet | yfinance API | 总资产、总负债、现金、应收账款 | ✅ 已实现 |
| **现金流量表** / Cash Flow | yfinance API | 经营现金流、自由现金流、资本支出 | ✅ 已实现 |
| **分析师评级** / Analyst Ratings | yfinance API | 买入/持有/卖出评级、目标价 | ✅ 已实现 |
| **数据缓存** / Data Cache | 本地 JSON 文件 | 24 小时缓存，避免重复请求 | ✅ 已实现 |

---

### 2️⃣ 16 模块分析引擎 / 16-Module Analysis Engine

| 模块 / Module | 分析方法 / Method | 核心指标 / Metrics | 评分逻辑 / Scoring |
|------|---------|---------|---------|
| **A. 收入质量** / Revenue Quality | 增长率分析 | YoY、QoQ、毛利率 | 增长>20% 且毛利>50% |
| **B. 盈利能力** / Profitability | 利润率分析 | 净利率、ROE、运营利润率 | ROE>20% 且净利率>20% |
| **C. 现金流** / Cash Flow | 现金流质量 | FCF 利润率、现金转化率 | FCF 利润率>25% |
| **D. 前瞻指引** / Forward Guidance | 分析师预期 | 目标价上涨空间 | 上涨>30% |
| **E. 竞争格局** / Competitive Landscape | 护城河分析 | 毛利率（定价权） | 毛利率>60% |
| **F. 核心 KPI** / Core KPIs | 增长质量 | 收入增长 vs 利润增长 | 双增长>20% |
| **G. 产品与新业务** / Products | 创新能力 | 研发投入占比 | 研发>15% |
| **H. 合作伙伴生态** / Partners | 渠道健康度 | 应收账款占比 | 应收<20% |
| **I. 高管团队** / Management | 管理层评估 | CEO 信息、员工数 | 基础信息展示 |
| **J. 宏观政策** / Macro Policy | 行业分析 | 行业分类 | 科技行业默认中等 |
| **K. 估值模型** / Valuation | 估值水平 | PE、PB | PE<15 |
| **L. 筹码分布** / Ownership | 分析师评级 | 买入比例 | 买入>80% |
| **M. 长期监控变量** / Monitoring | 风险识别 | 5 个关键指标 | 固定 80 分 |
| **N. 研发效率** / R&D Efficiency | 研发 ROI | 利润增长/研发投入 | 效率>2x |
| **O. 会计质量** / Accounting | 财务健康度 | 流动比率、负债率 | 流动>1.5 且负债<0.5 |
| **P. ESG 筛查** / ESG Screening | ESG 评估 | 基础评估 | 默认 65 分 |

---

### 3️⃣ 6 大投资哲学视角 / 6 Investment Philosophy Perspectives

| 视角 / Perspective | 代表人物 / Representatives | 评分维度 / Dimensions | 核心问题 / Core Question |
|------|---------|---------|---------|
| **质量复利** / Quality Compounder | 巴菲特/芒格 | 护城河、ROE、自由现金流、管理层 | 市场关闭 10 年能安心睡觉吗？ |
| **想象力成长** / Imaginative Growth | Baillie Gifford/ARK | TAM、创新能力、成长速度、长期潜力 | 5 年后不买会后悔吗？ |
| **基本面多空** / Fundamental L/S | Tiger Cubs | 相对价值、催化剂、风险收益、做空机会 | 有 Variant View 吗？ |
| **深度价值** / Deep Value | Klarman/Marks | 安全边际、资产价值、逆向机会、清算价值 | 比清算价值低多少？ |
| **催化剂驱动** / Catalyst-Driven | Tepper/Ackman | 催化剂强度、activist 机会、重组、并购 | 6-18 个月有什么催化剂？ |
| **宏观战术** / Macro Tactical | Druckenmiller | 宏观环境、流动性、行业轮动、趋势 | 宏观是顺风还是逆风？ |

---

### 4️⃣ 多方法估值矩阵 / Multi-Method Valuation Matrix

| 方法 / Method | 创始人 / Founder | 公式 / Formula | 判断标准 / Criteria |
|------|-------|---------|---------|
| **Owner Earnings** | 巴菲特 / Buffett | 净利润 + 折旧 - 资本支出 | 10-15 倍合理 |
| **PEG Ratio** | 彼得·林奇 / Lynch | PE / 盈利增长率 | <0.5 极具吸引力 |
| **Reverse DCF** | 逆向思维 | 从股价反推隐含增长率 | 隐含增长<历史=低估 |
| **Magic Formula** | 格林布拉特 / Greenblatt | 盈利收益率 + ROIC 排名 | 综合排名<10% 优秀 |
| **EV/EBITDA** | 达摩达兰 / Damodaran | 企业价值 / EBITDA | 低于行业 20%+=低估 |
| **Rule of 40** | SaaS 行业 | 增长率 + 利润率 | ≥40% 优秀 |

---

### 5️⃣ 反偏见框架 / Anti-Bias Framework

#### 认知偏见 / Cognitive Biases（6 个）

| 偏见 / Bias | 检测方法 / Detection | 警告条件 / Warning |
|------|---------|---------|
| **确认偏误** / Confirmation Bias | 卖出评级比例 | <5% 则警告 |
| **锚定效应** / Anchoring | 股价位置（52 周区间） | 接近极值则警告 |
| **叙事谬误** / Narrative Fallacy | 增长 vs 利润 | 高增长低利润则警告 |
| **从众心理** / Herding | 买入评级比例 | >90% 则警告 |
| **处置效应** / Disposition Effect | 通用检查 | 针对持仓场景 |
| **过度自信** / Overconfidence | 通用检查 | 区间估计场景 |

#### 财务红旗 / Financial Red Flags（7 个）

| 红旗 / Red Flag | 检测方法 / Detection | 警告条件 / Warning |
|------|---------|---------|
| **收入确认异常** | 待实现 / TBD | - |
| **GAAP vs Non-GAAP** | 待实现 / TBD | - |
| **应收账款异常** / Receivables | 应收/收入 | >30% 则标记 |
| **内部人交易** / Insider Trading | 待接入 SEC Form 4 | - |
| **资本支出暴增** / CapEx Surge | CapEx/收入 | >20% 则标记 |
| **现金流背离** / Cash Flow Divergence | 利润 vs 现金流 | 利润正但现金流负 |
| **负债结构恶化** / Debt Structure | 负债率、流动比率 | 负债>1 或流动<1 |

#### 科技盲区 / Tech Blind Spots（5 个）

| 盲区 / Blind Spot | 检测方法 / Detection | 警告条件 / Warning |
|------|---------|---------|
| **TAM 幻觉** / TAM Illusion | 待实现 / TBD | - |
| **AI 收入真实性** / AI Revenue | AI 关键词 | AI 相关则提示核实 |
| **股票期权稀释** / Stock Dilution | 待实现 / TBD | - |
| **CAC 拐点** / CAC Inflection | 待实现 / TBD | - |
| **监管尾部风险** / Regulatory Risk | 市值 | >1 万亿则警告 |

---

### 6️⃣ Key Forces 识别 / Key Forces Identification

| 类型 / Type | 判断逻辑 / Logic | 影响力评分 / Score |
|------|---------|-----------|
| **增长驱动** / Growth Driver | 收入/利润增长>20% | 增长率/5（最高 10 分） |
| **技术变革** / Tech Shift | AI/云/机器学习关键词 | 关键词数×2+4（最高 10 分） |
| **护城河加深** / Moat Deepening | 毛利率>60% | 毛利率/8（最高 10 分） |
| **财务实力** / Financial Strength | FCF 利润率>20% 且流动>1.5 | FCF/3 + 流动×2 |
| **市场情绪** / Market Sentiment | 分析师买入>80% 或上涨>30% | 买入%/15 + 上涨/5 |
| **行业趋势** / Industry Trend | 科技/软件/半导体行业 | 固定 6 分 |

---

### 7️⃣ Variant View 生成器 / Variant View Generator

| 功能 / Function | 实现方法 / Method | 输出内容 / Output |
|------|---------|---------|
| **市场共识** / Market Consensus | 分析师评级汇总 | 买入比例、目标价、上涨空间 |
| **盲点识别** / Blind Spot ID | 数据对比分析 | 现金流、增长质量、共识盲点 |
| **变异认知** / Variant Perception | 盲点方向分析 | 看多/看空/中性 |
| **置信度评估** / Confidence | 盲点数量及严重程度 | 高/中/低 |
| **可执行观点** / Actionable View | 根据方向生成建议 | 做多/做空/观望 + 理由 |

---

### 8️⃣ Pre-Mortem（事前尸检）

| 组件 / Component | 内容 / Content |
|------|------|
| **核心问题** / Core Questions | 5 个标准化问题（核心假设、风险、竞争、管理层、宏观） |
| **静态提示** / Static Hints | 每个问题配思考方向提示 |
| **行动建议** / Action Recommendations | 4 步风险评估（概率、影响、应对、监控） |

---

## 📝 输出示例 / Output Example

报告将包含以下部分：
Report includes:

1. **📋 投资摘要** / Investment Summary - 详细描述性总结
2. **📊 模块分析** / Module Analysis - 16 个模块详细评分
3. **💼 投资视角** / Investment Perspectives - 6 大投资哲学视角
4. **✅ 关键驱动因素** / Key Drivers - Top 3 关键力量
5. **🧠 认知偏见检测** / Cognitive Biases - 完整 6 项检测表
6. **🚩 财务红旗** / Financial Red Flags - 风险警示
7. **💀 Pre-Mortem** - 事前检查

---

## ⚙️ 配置 / Configuration

编辑 `config.json` 自定义：
Edit `config.json` to customize:

```json
{
  "default_stock": "NVDA",
  "output_format": "markdown",
  "cache_ttl_hours": 24,
  "enable_modules": "all",
  "enable_perspectives": "all"
}
```

---

## 🔌 协同技能 / Synergistic Skills

| 技能 / Skill | 协同方式 / Synergy |
|------|---------|
| us-value-investing | 四维价值评分交叉验证 |
| us-market-sentiment | 宏观情绪联动 |
| macro-liquidity | 流动性环境分析 |

---

## ⚠️ 免责声明 / Disclaimer

此 Skill 生成的分析基于公开信息和模型推算，仅供研究参考，不构成投资建议。投资有风险，决策需谨慎。

Analysis generated by this Skill is based on public information and model calculations, for research reference only, does not constitute investment advice. Investment involves risks, make decisions cautiously.

---

## 📄 许可证 / License

基于 Day1Global 开源项目改编  
Based on Day1Global open source project

原项目 / Original Project: https://github.com/star23/Day1Global-Skills/

---

## 🔄 版本 / Version

**v1.0.0** - 2026-03-02

**新增功能 / New Features:**
- 投资摘要模块 / Investment Summary Module
- 16 模块分析 / 16-Module Analysis
- 6 大投资视角 / 6 Investment Perspectives
- 关键驱动因素 / Key Forces
- 认知偏见检测 / Cognitive Biases Detection
- 财务红旗 / Financial Red Flags
- Pre-Mortem 事前检查

**优化改进 / Improvements:**
- 全局字体层级统一 / Unified Font Hierarchy
- 24 个评分维度名称优化 / 24 Dimension Names Optimized
- 章节名中文化 / Chinese Section Names
- 布局优化 / Layout Optimization

**问题修复 / Bug Fixes:**
- 核心问题重复显示 / Duplicate Core Questions
- 评分维度名称重复 / Duplicate Dimension Names
- 字号不统一 / Inconsistent Font Sizes

详细变更历史请查看 [CHANGELOG.md](CHANGELOG.md)
See [CHANGELOG.md](CHANGELOG.md) for detailed changelog

---

*最后更新 / Last Updated: 2026-03-02*
