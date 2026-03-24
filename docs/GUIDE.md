# Tech Earnings Deep Dive - 完整指南

**版本**: v3.0  
**最后更新**: 2026-03-24

---

## 📖 目录

### 第一部分：产品指南
1. [产品概述](#1-产品概述)
2. [核心功能](#2-核心功能)
3. [使用指南](#3-使用指南)
4. [常见问题](#4-常见问题)

### 第二部分：技术架构
5. [系统架构](#5-系统架构)
6. [模块设计](#6-模块设计)
7. [评分算法](#7-评分算法)
8. [配置说明](#8-配置说明)
9. [扩展开发](#9-扩展开发)

---

# 第一部分：产品指南


## 1. 产品概述



### 1.1 产品定位

Tech Earnings Deep Dive 是一个**机构级科技股财报深度分析系统**，专为 AI 助手打造，提供专业投资机构级别的分析能力。

### 1.2 核心价值

| 价值点 | 说明 |
|--------|------|
| **专业级分析** | 复刻 Day1Global 框架，16 模块 +6 视角 +6 估值方法 |
| **自动化流程** | 从数据获取到报告生成，全流程自动化 |
| **多维度对比** | 支持多只股票批量对比分析 |
| **客观中立** | 基于数据说话，避免情绪化决策 |

### 1.3 适用人群

| 人群 | 使用场景 |
|------|---------|
| **个人投资者** | 财报分析、持仓决策、估值判断 |
| **投资顾问** | 客户报告、投资建议、风险评估 |
| **研究人员** | 行业分析、公司对比、趋势研究 |
| **AI 助手** | 为用户提供专业的投资分析服务 |

---

## 2. 核心功能

### 2.1 功能总览

```
Tech Earnings Deep Dive
│
├── 📊 16 模块分析      # 基本面深度分析
├── 👁️ 6 大投资视角     # 大师视角评估
├── 💰 6 种估值方法     # 多方法估值矩阵
├── 🎯 MSCI Barra      # 多因子评分
├── ⚠️ 反偏见框架      # 风险识别
├── 🔍 批量对比        # 多股对比分析
└── 📑 HTML 报告       # 专业格式输出
```

### 2.2 16 模块分析

| 模块 | 名称 | 说明 |
|------|------|------|
| A | 收入质量 | 收入增长率、收入构成、客户集中度 |
| B | 盈利能力 | 毛利率、净利率、ROE、ROA |
| C | 现金流 | 自由现金流、现金流利润率 |
| D | 前瞻指引 | 管理层指引、分析师预期 |
| E | 竞争格局 | 市场份额、竞争壁垒 |
| F | 核心 KPI | 行业特定指标 |
| G | 产品与新业务 | 产品线、新业务进展 |
| H | 合作伙伴生态 | 供应商、客户、战略合作 |
| I | 高管团队 | 管理层背景、持股情况 |
| J | 宏观政策 | 行业政策、宏观经济 |
| K | 估值模型 | 多方法估值对比 |
| L | 筹码分布 | 内部人交易、机构持仓 |
| M | 长期监控变量 | 长期跟踪指标 |
| N | 研发效率 | 研发投入产出比 |
| O | 会计质量 | 会计政策、审计意见 |
| P | ESG 筛查 | 环境、社会、治理 |

### 2.3 6 大投资视角

| 视角 | 代表人物 | 关注点 |
|------|----------|--------|
| 质量复利 | 巴菲特/芒格 | ROE 可持续性、护城河 |
| 想象力成长 | Baillie Gifford/ARK | 长期成长潜力 |
| 基本面多空 | Tiger Cubs | 基本面强弱对比 |
| 深度价值 | Klarman/Marks | 安全边际 |
| 催化剂驱动 | Tepper/Ackman | 短期催化剂 |
| 宏观战术 | Druckenmiller | 宏观环境、流动性 |

---

## 3. 使用指南

### 3.1 单股分析

```bash
python3 analyze.py AAPL
python3 analyze.py NVDA --no-cache
```

### 3.2 批量对比

```bash
python3 analyze_batch.py NVDA AMD INTC
python3 analyze_batch.py AAPL MSFT GOOGL --workers 5
```

### 3.3 输出位置

- **个股报告**: `~/.openclaw/workspace/output/tech-earnings-deepdive/`
- **对比报告**: `~/.openclaw/workspace/output/tech-earnings-deepdive/batch/`

### 3.4 配置选项

```json
{
  "batch_analysis": {
    "max_workers": 3,
    "rate_limit": 10,
    "rate_period": 60
  },
  "error_handling": {
    "retry_on_failure": true,
    "max_retries": 2
  }
}
```

---


## 2. 核心功能

### 2.1 功能总览



```
Tech Earnings Deep Dive
│
├── 📊 16 模块分析      # 基本面深度分析
├── 👁️ 6 大投资视角     # 大师视角评估
├── 💰 6 种估值方法     # 多方法估值矩阵
├── 🎯 MSCI Barra      # 多因子评分
├── ⚠️ 反偏见框架      # 风险识别
├── 🔍 批量对比        # 多股对比分析
└── 📑 HTML 报告       # 专业格式输出
```

### 2.2 16 模块分析

| 模块 | 名称 | 说明 |
|------|------|------|
| A | 收入质量 | 收入增长率、收入构成、客户集中度 |
| B | 盈利能力 | 毛利率、净利率、ROE、ROA |
| C | 现金流 | 自由现金流、现金流利润率 |
| D | 前瞻指引 | 管理层指引、分析师预期 |
| E | 竞争格局 | 市场份额、竞争壁垒 |
| F | 核心 KPI | 行业特定指标 |
| G | 产品与新业务 | 产品线、新业务进展 |
| H | 合作伙伴生态 | 供应商、客户、战略合作 |
| I | 高管团队 | 管理层背景、持股情况 |
| J | 宏观政策 | 行业政策、宏观经济 |
| K | 估值模型 | 多方法估值对比 |
| L | 筹码分布 | 内部人交易、机构持仓 |
| M | 长期监控变量 | 长期跟踪指标 |
| N | 研发效率 | 研发投入产出比 |
| O | 会计质量 | 会计政策、审计意见 |
| P | ESG 筛查 | 环境、社会、治理 |


### 2.2 16 模块分析

| 模块 | 名称 | 说明 |
|------|------|------|
| A | 收入质量 | 收入增长率、收入构成、客户集中度 |
| B | 盈利能力 | 毛利率、净利率、ROE、ROA |
| C | 现金流 | 自由现金流、现金流利润率 |
| D | 前瞻指引 | 管理层指引、分析师预期 |
| E | 竞争格局 | 市场份额、竞争壁垒 |
| F | 核心 KPI | 行业特定指标 |
| G | 产品与新业务 | 产品线、新业务进展 |
| H | 合作伙伴生态 | 供应商、客户、战略合作 |
| I | 高管团队 | 管理层背景、持股情况 |
| J | 宏观政策 | 行业政策、宏观经济 |
| K | 估值模型 | 多方法估值对比 |
| L | 筹码分布 | 内部人交易、机构持仓 |
| M | 长期监控变量 | 长期跟踪指标 |
| N | 研发效率 | 研发投入产出比 |
| O | 会计质量 | 会计政策、审计意见 |
| P | ESG 筛查 | 环境、社会、治理 |

### 2.3 6 大投资视角

| 视角 | 代表人物 | 关注点 |
|------|----------|--------|
| 质量复利 | 巴菲特/芒格 | ROE 可持续性、护城河 |
| 想象力成长 | Baillie Gifford/ARK | 长期成长潜力 |
| 基本面多空 | Tiger Cubs | 基本面强弱对比 |
| 深度价值 | Klarman/Marks | 安全边际 |
| 催化剂驱动 | Tepper/Ackman | 短期催化剂 |
| 宏观战术 | Druckenmiller | 宏观环境、流动性 |


## 3. 使用指南



### 3.1 单股分析

```bash
python3 analyze.py AAPL
python3 analyze.py NVDA --no-cache
```

### 3.2 批量对比

```bash
python3 analyze_batch.py NVDA AMD INTC
python3 analyze_batch.py AAPL MSFT GOOGL --workers 5
```

### 3.3 输出位置

- **个股报告**: `~/.openclaw/workspace/output/tech-earnings-deepdive/`
- **对比报告**: `~/.openclaw/workspace/output/tech-earnings-deepdive/batch/`

### 3.4 配置选项

```json
{
  "batch_analysis": {
    "max_workers": 3,
    "rate_limit": 10,
    "rate_period": 60
  },
  "error_handling": {
    "retry_on_failure": true,
    "max_retries": 2
  }
}
```

---


## 4. 常见问题

### Q: 数据准确性如何保证？

A: 数据来源于 Yahoo Finance 和 SEC EDGAR，均为权威数据源。详细的数据验证流程请查看 [数据准确性文档](docs/DATA_ACCURACY.md)。

### Q: 缓存多久更新一次？

A: 
- 股价数据：1 小时
- 财报数据：24 小时
- 内部人交易：24 小时
- 机构持仓：24 小时

### Q: 如何禁用缓存？

A: 使用 `--no-cache` 参数：
```bash
python3 analyze.py AAPL --no-cache
```

### Q: 批量分析太慢怎么办？

A: 可以增加并发数：
```bash
python3 analyze_batch.py NVDA AMD INTC --workers 5
```

### Q: 如何查看技术细节？

A: 请查看 [技术架构文档](docs/ARCHITECTURE.md)，包含系统架构、评分算法、扩展开发等详细内容。

---

**最后更新**

---

# 第二部分：技术架构


## 系统架构



### 1.1 整体架构

```
Tech Earnings Deep Dive
│
├── analyze.py              # 单股分析入口
├── analyze_batch.py        # 批量分析入口
├── config.json             # 配置文件
│
├── modules/                # 核心模块
│   ├── core.py            # 核心分析引擎
│   ├── fetch_data.py      # 数据获取
│   ├── analyze_full.py    # 16 模块分析
│   ├── perspectives_full.py  # 6 大视角分析
│   ├── valuation_full.py  # 估值计算
│   ├── export_report.py   # 报告导出
│   ├── exceptions.py      # 自定义异常
│   └── ...
│
├── references/            # 参考文档
│   ├── valuation-models.md
│   ├── investing-philosophies.md
│   └── bias-checklist.md
│
└── cache/                 # 数据缓存
    └── {TICKER}_data.json
```

### 1.2 核心组件

| 组件 | 文件 | 职责 | 行数 |
|------|------|------|------|
| **数据获取** | `fetch_data.py` | 从 Yahoo Finance/SEC 获取数据 | ~800 行 |
| **16 模块分析** | `analyze_full.py` | 基本面 16 维度分析 | ~600 行 |
| **6 大视角** | `perspectives_full.py` | 投资哲学视角评估 | ~700 行 |
| **估值计算** | `valuation_full.py` | 6 种估值方法 | ~800 行 |
| **报告导出** | `export_report.py` | HTML/MD 报告生成 | ~2200 行 |
| **核心引擎** | `core.py` | 整合所有模块 | ~300 行 |

---



## 模块设计



### 2.1 16 模块分析

```python
modules = {
    'A_revenue_quality': {'name': '收入质量', 'weight': 1/16},
    'B_profitability': {'name': '盈利能力', 'weight': 1/16},
    'C_cash_flow': {'name': '现金流', 'weight': 1/16},
    'D_forward_guidance': {'name': '前瞻指引', 'weight': 1/16},
    'E_competitive_landscape': {'name': '竞争格局', 'weight': 1/16},
    'F_core_kpis': {'name': '核心 KPI', 'weight': 1/16},
    'G_products_new': {'name': '产品与新业务', 'weight': 1/16},
    'H_partners': {'name': '合作伙伴生态', 'weight': 1/16},
    'I_management': {'name': '高管团队', 'weight': 1/16},
    'J_macro_policy': {'name': '宏观政策', 'weight': 1/16},
    'K_valuation': {'name': '估值模型', 'weight': 1/16},
    'L_ownership': {'name': '筹码分布', 'weight': 1/16},
    'M_long_term_vars': {'name': '长期监控变量', 'weight': 1/16},
    'N_rd_efficiency': {'name': '研发效率', 'weight': 1/16},
    'O_accounting_quality': {'name': '会计质量', 'weight': 1/16},
    'P_esg_screening': {'name': 'ESG 筛查', 'weight': 1/16},
}
```

### 2.2 6 大投资视角

```python
perspectives = {
    'quality_compounder': {
        'name': '质量复利',
        'representatives': '巴菲特/芒格',
        'focus': 'ROE 可持续性、护城河、管理层质量'
    },
    'imaginative_growth': {
        'name': '想象力成长',
        'representatives': 'Baillie Gifford/ARK',
        'focus': '长期成长潜力、颠覆性创新'
    },
    'fundamental_long_short': {
        'name': '基本面多空',
        'representatives': 'Tiger Cubs',
        'focus': '基本面强弱、多空机会'
    },
    'deep_value': {
        'name': '深度价值',
        'representatives': 'Klarman/Marks',
        'focus': '安全边际、逆向投资'
    },
    'catalyst_driven': {
        'name': '催化剂驱动',
        'representatives': 'Tepper/Ackman',
        'focus': '短期催化剂、事件驱动'
    },
    'macro_tactical': {
        'name': '宏观战术',
        'representatives': 'Druckenmiller',
        'focus': '宏观环境、流动性、战术配置'
    }
}
```

### 2.3 6 种估值方法

```python
valuation_methods = [
    'owner_earnings',      # 所有者盈余折现
    'peg',                 # PEG 估值
    'reverse_dcf',         # 反向 DCF
    'magic_formula',       # 神奇公式
    'ev_ebitda',           # EV/EBITDA
    'ev_revenue_rule40'    # EV/Revenue (Rule of 40)
]
```

---



## 评分算法



### 4.1 综合评分计算

```python
def calculate_overall_score(modules, perspectives, valuation, biases):
    # 16 模块基础评分 (50%)
    module_scores = [m['score'] for m in modules.values()]
    avg_module_score = sum(module_scores) / len(module_scores)
    
    # 6 大视角评分 (20%)
    perspective_scores = [p['total_score'] for p in perspectives.values()]
    avg_perspective_score = sum(perspective_scores) / len(perspective_scores)
    
    # 估值评分转换 (30%)
    upside = valuation['summary']['upside_downside']
    valuation_score = min(100, max(0, 75 + upside * 1.25))
    
    # 综合评分
    base_score = (
        avg_module_score * 0.50 +
        avg_perspective_score * 0.20 +
        valuation_score * 0.30
    )
    
    # 红旗罚分
    red_flag_penalty = calculate_red_flag_penalty(biases)
    
    overall_score = max(0, base_score - red_flag_penalty)
    
    return overall_score
```

### 4.2 MSCI Barra 6 大因子

```python
barra_factors = {
    'quality': {
        'weight': 0.30,
        'modules': ['A', 'B', 'C', 'E', 'H', 'I', 'O']
    },
    'growth': {
        'weight': 0.25,
        'modules': ['F', 'G', 'N']
    },
    'value': {
        'weight': 0.20,
        'modules': ['K']
    },
    'sentiment': {
        'weight': 0.10,
        'modules': ['L']
    },
    'macro': {
        'weight': 0.10,
        'modules': ['J']
    },
    'esg': {
        'weight': 0.05,
        'modules': ['P']
    }
}
```

### 4.3 投资建议映射

```python
def map_recommendation(score):
    if score >= 80:
        return '强烈买入'
    elif score >= 70:
        return '买入'
    elif score >= 60:
        return '持有'
    elif score >= 50:
        return '减持'
    else:
        return '卖出'
```

---



## 配置说明



### 5.1 config.json 结构

```json
{
  "name": "tech-earnings-deepdive-openclaw-skill",
  "version": "3.0.0",
  "default_stock": "NVDA",
  "output_format": "html",
  "cache_ttl_hours": 24,
  "batch_analysis": {
    "max_workers": 3,
    "rate_limit": 10,
    "rate_period": 60,
    "timeout_per_stock": 300
  },
  "error_handling": {
    "retry_on_failure": true,
    "max_retries": 2,
    "log_level": "INFO"
  }
}
```

### 5.2 环境变量

```bash
# 输出目录
export OUTPUT_DIR=~/.openclaw/workspace/output/tech-earnings-deepdive

# 日志级别
export LOG_LEVEL=INFO

# API 密钥（可选）
export TIINGO_API_KEY=your_key_here
```

---



## 扩展开发



### 6.1 添加新模块

1. 在 `modules/` 目录创建新模块文件
2. 在 `analyze_full.py` 中注册模块
3. 在 `config.json` 中启用模块
4. 更新 `export_report.py` 支持新模块输出

### 6.2 添加新估值方法

1. 在 `valuation_full.py` 中实现计算方法
2. 在 `config.json` 的 `valuation_methods` 列表中添加
3. 更新 `export_report.py` 的估值表格

### 6.3 自定义报告模板

1. 修改 `export_report.py` 中的 HTML 模板
2. 或创建新的导出器类继承 `ReportExporter`

---



---

## 附录

### A. 错误代码

| 错误代码 | 说明 | 解决方案 |
|---------|------|---------|
| `DATA_FETCH_ERROR` | 数据获取失败 | 检查网络连接/API 限流 |
| `INSUFFICIENT_DATA` | 数据不足 | 等待财报发布/检查股票代码 |
| `ANALYSIS_ERROR` | 分析失败 | 查看日志定位具体模块 |
| `EXPORT_ERROR` | 导出失败 | 检查输出目录权限 |

### B. 性能优化建议

1. **启用缓存**：`use_cache=True`（默认）
2. **批量分析限流**：`--rate-limit 10`（10 请求/60 秒）
3. **并发控制**：`--workers 3`（默认 3 并发）
4. **超时设置**：`timeout_per_stock=300`（5 分钟/股）

---

**文档版本**: v3.0  
**最后更新**: 2026-03-24
