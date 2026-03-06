#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量分析模块
支持多股票并行分析、对比报告、筛选排序
"""

import sys
import os
import json
import argparse
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Optional

# 导入现有模块
sys.path.insert(0, 'modules')
from fetch_data import StockDataFetcher
from analyze_full import analyze_16_modules
from perspectives_full import analyze_perspectives_full
from valuation_full import ValuationCalculator
from key_forces import identify_key_forces
from bias_framework import check_biases
from variant_view import generate_variant_view
from export_report import ReportExporter


class BatchAnalyzer:
    """批量分析器"""
    
    def __init__(self, tickers: List[str], max_workers: int = 3):
        self.tickers = tickers
        self.max_workers = max_workers
        self.results = {}
        # 使用环境变量 OUTPUT_DIR，默认外部存储
        output_base = os.environ.get('OUTPUT_DIR', Path.home() / '.openclaw' / 'tech-earnings-output')
        self.output_dir = Path(output_base) / 'batch'
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def analyze_all(self, use_cache: bool = True, skip_p2: bool = False) -> Dict:
        """分析所有股票"""
        print("=" * 70)
        print(f"🚀 批量分析 {len(self.tickers)} 只股票")
        print("=" * 70)
        print(f"股票列表：{', '.join(self.tickers)}")
        print(f"并发数：{self.max_workers}")
        print(f"使用缓存：{'是' if use_cache else '否'}")
        print("=" * 70)
        print()
        
        # 多线程并行分析
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 提交任务
            future_to_ticker = {
                executor.submit(self._analyze_single, ticker, use_cache, skip_p2): ticker
                for ticker in self.tickers
            }
            
            # 收集结果
            completed = 0
            for future in as_completed(future_to_ticker):
                ticker = future_to_ticker[future]
                try:
                    result = future.result()
                    self.results[ticker] = result
                    completed += 1
                    
                    # 显示进度
                    summary = result.get('summary', {})
                    score = summary.get('overall_score', 0)
                    recommendation = summary.get('recommendation', 'N/A')
                    
                    print(f"✅ [{completed}/{len(self.tickers)}] {ticker}: "
                          f"{score:.1f}/100 - {recommendation}")
                    
                except Exception as e:
                    print(f"❌ [{ticker}] 分析失败：{e}")
        
        print()
        print("=" * 70)
        print(f"✅ 批量分析完成：{len(self.results)}/{len(self.tickers)} 只股票")
        print("=" * 70)
        
        return self.results
    
    def _analyze_single(self, ticker: str, use_cache: bool, skip_p2: bool) -> Dict:
        """分析单只股票"""
        try:
            # 获取数据
            fetcher = StockDataFetcher(ticker)
            data = fetcher.get_all_data(use_cache=use_cache)
            
            # 16 模块分析
            modules = analyze_16_modules(data)
            
            # 6 大视角
            perspectives = analyze_perspectives_full(ticker, data)
            
            # 估值
            calc = ValuationCalculator(data)
            valuation = calc.calculate_all()
            
            # Key Forces
            key_forces = identify_key_forces(data)
            
            # 反偏见
            biases = check_biases(data)
            
            # ========== 综合评分（16 模块 +6 视角 + 估值） ==========
            avg_module_score = sum(m.get('score', 0) for m in modules.values()) / 16
            perspective_summary = perspectives.get('summary', {})
            perspective_pct = perspective_summary.get('average_score', 0)
            valuation_summary = valuation.get('summary', {})
            upside = valuation_summary.get('upside_downside', 0)
            
            # 估值评分转换：与 generate_single_report.py 保持一致
            # 基准分 75 分，upside 每 +1% 加 1.25 分，范围 0-100
            valuation_score = min(100, max(0, 75 + upside * 1.25))
            
            base_score = (avg_module_score * 0.5 + perspective_pct * 0.2 + valuation_score * 0.3)
            
            # 红旗减分
            red_flags = biases.get('financial_red_flags', {}).get('flags', [])
            red_flag_penalty = sum(
                15 if flag.get('risk') == '高' else
                8 if flag.get('risk') == '中' else
                3 if flag.get('risk') == '低' else 0
                for flag in red_flags
            )
            
            overall_score = max(0, base_score - red_flag_penalty)
            
            # ========== MSCI Barra 6 大因子评分 ==========
            # 质量因子（30%）：A,B,C,E,H,I,O
            quality_modules = ['A_revenue_quality', 'B_profitability', 'C_cash_flow', 
                              'E_competitive_landscape', 'H_partners', 
                              'I_management', 'O_accounting']
            quality_score = sum(modules.get(m, {}).get('score', 0) for m in quality_modules) / len(quality_modules)
            
            # 成长因子（25%）：F,G,N
            growth_modules = ['F_core_kpis', 'G_products', 'N_rd_efficiency']
            growth_score = sum(modules.get(m, {}).get('score', 0) for m in growth_modules) / len(growth_modules)
            
            # 价值因子（20%）：K
            value_score = modules.get('K_valuation', {}).get('score', 0)
            
            # 情绪因子（10%）：D,L
            sentiment_modules = ['D_forward_guidance', 'L_ownership']
            sentiment_score = sum(modules.get(m, {}).get('score', 0) for m in sentiment_modules) / len(sentiment_modules)
            
            # 宏观因子（10%）：J
            macro_score = modules.get('J_macro', {}).get('score', 0)
            
            # ESG 因子（5%）：P
            esg_score = modules.get('P_esg', {}).get('score', 0)
            
            # MSCI Barra 综合评分
            barra_score = (
                quality_score * 0.30 +
                growth_score * 0.25 +
                value_score * 0.20 +
                sentiment_score * 0.10 +
                macro_score * 0.10 +
                esg_score * 0.05
            )
            
            # ========== 置信度计算（基于分歧度） ==========
            import statistics
            
            # 1. 投资视角分歧度（50% 权重）
            perspective_scores = [p.get('total_score', 0) for p in perspectives.values() if isinstance(p, dict) and 'total_score' in p]
            if len(perspective_scores) >= 2:
                perspective_std = statistics.stdev(perspective_scores)
                if perspective_std < 10:
                    perspective_conf = 100
                elif perspective_std < 20:
                    perspective_conf = 70
                else:
                    perspective_conf = 40
            else:
                perspective_conf = 50  # 数据不足，默认中等
            
            # 2. 估值方法分歧度（50% 权重）
            valuation_methods = valuation.get('methods', {})
            upside_values = []
            for method_name, method_data in valuation_methods.items():
                if isinstance(method_data, dict) and 'upside_downside' in method_data:
                    upside_values.append(method_data['upside_downside'])
            
            if len(upside_values) >= 2:
                upside_std = statistics.stdev(upside_values)
                if upside_std < 15:
                    valuation_conf = 100
                elif upside_std < 30:
                    valuation_conf = 70
                else:
                    valuation_conf = 40
            else:
                valuation_conf = 50  # 数据不足，默认中等
            
            # 3. 综合置信度
            confidence_score = (perspective_conf * 0.5 + valuation_conf * 0.5)
            if confidence_score >= 80:
                confidence = '高'
            elif confidence_score >= 60:
                confidence = '中'
            else:
                confidence = '低'
            
            if overall_score >= 80 and upside > 20:
                recommendation = '强烈买入'
            elif overall_score >= 70 and upside > 10:
                recommendation = '买入'
            elif overall_score >= 60:
                recommendation = '持有'
            elif overall_score >= 50:
                recommendation = '减持'
            else:
                recommendation = '卖出'
            
            return {
                'ticker': ticker,
                'timestamp': datetime.now().isoformat(),
                'data': data,
                'modules': modules,
                'perspectives': perspectives,
                'valuation': valuation,
                'key_forces': key_forces,
                'biases': biases,
                'summary': {
                    # 原有综合评分
                    'overall_score': round(overall_score, 1),
                    'module_score': round(avg_module_score, 1),
                    'perspective_score': round(perspective_pct, 1),
                    'valuation_upside': round(upside, 1),
                    'recommendation': recommendation,
                    'confidence': confidence,  # 使用新计算的置信度
                    
                    # MSCI Barra 评分
                    'barra_score': round(barra_score, 1),
                    'barra_factors': {
                        'quality': round(quality_score, 1),
                        'growth': round(growth_score, 1),
                        'value': round(value_score, 1),
                        'sentiment': round(sentiment_score, 1),
                        'macro': round(macro_score, 1),
                        'esg': round(esg_score, 1)
                    }
                }
            }
            
        except Exception as e:
            raise Exception(f"{ticker} 分析失败：{str(e)}")
    
    def generate_comparison_report(self, filename: Optional[str] = None, format: str = 'html') -> str:
        """生成对比报告"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"comparison_{timestamp}.{format}"
        
        filepath = self.output_dir / filename
        
        # 按评分排序
        sorted_results = sorted(
            self.results.items(),
            key=lambda x: x[1]['summary']['overall_score'],
            reverse=True
        )
        
        if format == 'html':
            return self._generate_html_report(filepath, sorted_results)
        else:
            return self._generate_markdown_report(filepath, sorted_results)
    
    def _generate_html_report(self, filepath, sorted_results) -> str:
        """生成 HTML 对比报告"""
        html = []
        
        # HTML 头部
        html.append("""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>批量分析对比报告</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Heiti SC", "Microsoft YaHei", sans-serif;
            line-height: 1.8;
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 50px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 20px;
            font-size: 32px;
        }
        h2 {
            color: #34495e;
            border-left: 5px solid #3498db;
            padding-left: 20px;
            margin-top: 40px;
            font-size: 24px;
            background: linear-gradient(to right, #ecf0f1, transparent);
            padding-top: 10px;
            padding-bottom: 10px;
        }
        h3 {
            color: #7f8c8d;
            font-size: 18px;
            margin-top: 30px;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 30px 0;
            font-size: 14px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 15px;
            text-align: left;
        }
        th {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-weight: 600;
        }
        tr:nth-child(even) {
            background-color: #f8f9fa;
        }
        tr:hover {
            background-color: #e8f4f8;
        }
        .score-high { color: #27ae60; font-weight: bold; }
        .score-medium { color: #f39c12; font-weight: bold; }
        .score-low { color: #c0392b; font-weight: bold; }
        .recommendation-buy { color: #27ae60; }
        .recommendation-hold { color: #f39c12; }
        .recommendation-sell { color: #c0392b; }
        .summary-box {
            background: linear-gradient(135deg, #e8f4f8 0%, #f0f8ff 100%);
            padding: 25px;
            border-radius: 8px;
            margin: 30px 0;
            border-left: 5px solid #3498db;
        }
        .warning-box {
            background: linear-gradient(135deg, #fef9e7 0%, #fff8dc 100%);
            padding: 20px;
            border-radius: 8px;
            margin: 30px 0;
            border-left: 5px solid #f1c40f;
        }
        .footer {
            margin-top: 50px;
            padding-top: 20px;
            border-top: 2px solid #ecf0f1;
            color: #7f8c8d;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">""")
        
        # 标题
        html.append(f"<h1>📊 批量分析对比报告</h1>")
        html.append(f"<p><strong>生成时间：</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>")
        html.append(f"<strong>股票数量：</strong> {len(self.results)}</p>")
        
        # 综合评分排名
        html.append("<h2>🏆 综合评分排名</h2>")
        html.append("<table>")
        html.append("<thead><tr><th>排名</th><th>股票</th><th>综合评分</th><th>16 模块</th><th>6 大视角</th><th>估值空间</th><th>建议</th></tr></thead>")
        html.append("<tbody>")
        
        for i, (ticker, result) in enumerate(sorted_results, 1):
            summary = result['summary']
            score = summary['overall_score']
            score_class = 'score-high' if score >= 70 else 'score-medium' if score >= 50 else 'score-low'
            rec_class = 'recommendation-buy' if '买入' in summary['recommendation'] else 'recommendation-hold' if '持有' in summary['recommendation'] else 'recommendation-sell'
            
            html.append(
                f"<tr>"
                f"<td>{i}</td>"
                f"<td><strong>{ticker}</strong></td>"
                f"<td class='{score_class}'>{score:.1f}</td>"
                f"<td>{summary['module_score']:.1f}</td>"
                f"<td>{summary['perspective_score']:.1f}</td>"
                f"<td>{summary['valuation_upside']:+.1f}%</td>"
                f"<td class='{rec_class}'>{summary['recommendation']}</td>"
                f"</tr>"
            )
        
        html.append("</tbody></table>")
        
        # 投资建议分布
        html.append("<h2>📋 投资建议分布</h2>")
        html.append("<table>")
        html.append("<thead><tr><th>建议</th><th>数量</th><th>股票</th></tr></thead>")
        html.append("<tbody>")
        
        recommendations = {}
        for ticker, result in self.results.items():
            rec = result['summary']['recommendation']
            recommendations[rec] = recommendations.get(rec, 0) + 1
        
        for rec in ['强烈买入', '买入', '持有', '减持', '卖出']:
            if rec in recommendations:
                stocks = [t for t, r in self.results.items() if r['summary']['recommendation'] == rec]
                rec_class = 'recommendation-buy' if '买入' in rec else 'recommendation-hold' if '持有' in rec else 'recommendation-sell'
                html.append(
                    f"<tr>"
                    f"<td class='{rec_class}'>{rec}</td>"
                    f"<td>{recommendations[rec]}</td>"
                    f"<td>{', '.join(stocks)}</td>"
                    f"</tr>"
                )
        
        html.append("</tbody></table>")
        
        # 详细指标对比
        html.append("<h2>🔍 详细指标对比</h2>")
        html.append("<table>")
        html.append("<thead><tr><th>股票</th><th>股价</th><th>PE</th><th>市值 (万亿)</th><th>营收增长</th><th>FCF(亿)</th><th>分析师买入%</th></tr></thead>")
        html.append("<tbody>")
        
        for ticker, result in sorted_results:
            data = result['data']
            price = data.get('price', {})
            financials = data.get('financials', {})
            analyst = data.get('analyst_estimates', {})
            
            total = sum([
                analyst.get('strong_buy', 0),
                analyst.get('buy', 0),
                analyst.get('hold', 0),
                analyst.get('sell', 0),
                analyst.get('strong_sell', 0)
            ])
            buy_ratio = (analyst.get('strong_buy', 0) + analyst.get('buy', 0)) / total * 100 if total > 0 else 0
            
            growth = financials.get('revenue_growth_yoy', 0) * 100
            growth_class = 'score-high' if growth > 20 else 'score-medium' if growth > 0 else 'score-low'
            
            html.append(
                f"<tr>"
                f"<td><strong>{ticker}</strong></td>"
                f"<td>${price.get('current_price', 0):.2f}</td>"
                f"<td>{price.get('pe_ratio', 0):.1f}x</td>"
                f"<td>${price.get('market_cap', 0)/1e12:.2f}</td>"
                f"<td class='{growth_class}'>{growth:+.1f}%</td>"
                f"<td>${data.get('cashflow', {}).get('free_cashflow', 0)/1e9:.1f}</td>"
                f"<td>{buy_ratio:.1f}%</td>"
                f"</tr>"
            )
        
        html.append("</tbody></table>")
        
        # Key Forces 汇总
        html.append("<h2>🎯 Key Forces 汇总</h2>")
        for ticker, result in sorted_results[:5]:
            html.append(f"<h3>{ticker}</h3>")
            html.append("<ol>")
            for i, force in enumerate(result['key_forces'][:3], 1):
                html.append(f"<li><strong>{force['name']}</strong> ({force['impact_score']:.1f}/10)</li>")
            html.append("</ol>")
        
        # 风险提示
        html.append("<h2>⚠️ 风险提示</h2>")
        html.append("<table>")
        html.append("<thead><tr><th>股票</th><th>财务红旗</th><th>认知偏见</th><th>风险等级</th></tr></thead>")
        html.append("<tbody>")
        
        for ticker, result in self.results.items():
            biases = result.get('biases', {})
            bias_summary = biases.get('summary', {})
            risk_level = bias_summary.get('risk_level', 'N/A')
            risk_class = 'score-low' if risk_level == '高' else 'score-medium' if risk_level == '中' else 'score-high'
            
            html.append(
                f"<tr>"
                f"<td><strong>{ticker}</strong></td>"
                f"<td>{bias_summary.get('total_red_flags', 0)}</td>"
                f"<td>{bias_summary.get('bias_warnings', 0)}</td>"
                f"<td class='{risk_class}'>{risk_level}</td>"
                f"</tr>"
            )
        
        html.append("</tbody></table>")
        
        # 详细风险分析
        html.append("<h2>🚩 财务红旗详情</h2>")
        for ticker, result in sorted_results:
            biases = result.get('biases', {})
            red_flags = biases.get('financial_red_flags', {}).get('flags', [])
            
            if red_flags:
                html.append(f"<h3>{ticker}</h3>")
                html.append("<div class='warning-box'>")
                html.append("<ul>")
                for flag in red_flags:
                    html.append(f"<li><strong>{flag['name']}:</strong> {flag['description']} <em>(风险：{flag.get('risk', '中')})</em></li>")
                html.append("</ul>")
                html.append("</div>")
        
        # 认知偏见详情
        html.append("<h2>🧠 认知偏见检查</h2>")
        for ticker, result in sorted_results:
            biases = result.get('biases', {})
            cognitive_biases = biases.get('cognitive_biases', {})
            
            warnings = [name for name, bias in cognitive_biases.items() if bias.get('risk', False)]
            
            if warnings:
                html.append(f"<h3>{ticker}</h3>")
                html.append("<div class='warning-box'>")
                html.append("<ul>")
                for bias_name in warnings:
                    bias = cognitive_biases[bias_name]
                    html.append(f"<li><strong>{bias['name']}:</strong> {bias['description']}</li>")
                html.append("</ul>")
                html.append("</div>")
        
        # 关键优势
        html.append("<h2>✅ 关键优势</h2>")
        for ticker, result in sorted_results[:5]:
            key_forces = result.get('key_forces', [])
            
            if key_forces:
                html.append(f"<h3>{ticker}</h3>")
                html.append("<div class='summary-box'>")
                html.append("<ol>")
                for i, force in enumerate(key_forces[:3], 1):
                    html.append(f"<li><strong>{force['name']}</strong> (影响力：{force['impact_score']:.1f}/10)")
                    html.append(f"<br><small>{force['description']}</small></li>")
                html.append("</ol>")
                html.append("</div>")
        
        # 主要风险
        html.append("<h2>⚠️ 主要风险</h2>")
        for ticker, result in sorted_results:
            blind_spots = result.get('variant_view', {}).get('blind_spots', [])
            
            if blind_spots:
                html.append(f"<h3>{ticker}</h3>")
                html.append("<div class='warning-box'>")
                html.append("<ul>")
                for spot in blind_spots:
                    html.append(f"<li><strong>{spot['type']}:</strong> {spot['description']} <em>(含义：{spot.get('implication', 'N/A')})</em></li>")
                html.append("</ul>")
                html.append("</div>")
        
        # 投资策略建议
        html.append("<h2>💡 投资策略建议</h2>")
        html.append("<div class='summary-box'>")
        
        if sorted_results:
            best = sorted_results[0]
            worst = sorted_results[-1]
            
            html.append(f"<h3>✅ 最佳选择：{best[0]} (评分{best[1]['summary']['overall_score']:.1f})</h3>")
            html.append(f"<ul>")
            html.append(f"<li><strong>建议：</strong> {best[1]['summary']['recommendation']}</li>")
            if best[1]['key_forces']:
                html.append(f"<li><strong>关键优势：</strong> {best[1]['key_forces'][0]['name']}</li>")
            html.append(f"</ul>")
            
            if len(sorted_results) > 1:
                html.append(f"<h3>⚠️ 风险最高：{worst[0]} (评分{worst[1]['summary']['overall_score']:.1f})</h3>")
                html.append(f"<ul>")
                html.append(f"<li><strong>建议：</strong> {worst[1]['summary']['recommendation']}</li>")
                html.append(f"<li><strong>主要风险：</strong> 估值过高 / 增长放缓 / 竞争激烈</li>")
                html.append(f"</ul>")
        
        html.append("</div>")
        
        # 页脚
        html.append("<div class='footer'>")
        html.append("<p>⚠️ <strong>免责声明：</strong> 本报告基于公开信息和模型推算，仅供参考，不构成投资建议。投资有风险，决策需谨慎。</p>")
        html.append(f"<p>报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>")
        html.append("</div>")
        
        # 结束
        html.append("    </div>")
        html.append("</body>")
        html.append("</html>")
        
        # 保存文件
        content = "\n".join(html)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 对比报告已导出：{filepath}")
        return str(filepath)
    
    def _generate_markdown_report(self, filepath, sorted_results) -> str:
        """生成 Markdown 对比报告（简化版）"""
        md = []
        md.append("# 📊 批量分析对比报告")
        md.append(f"**生成时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        md.append(f"**股票数量：** {len(self.results)}")
        md.append("")
        
        # 综合评分排名
        md.append("## 🏆 综合评分排名")
        md.append("")
        md.append("| 排名 | 股票 | 综合评分 | 16 模块 | 6 大视角 | 估值空间 | 建议 |")
        md.append("|------|------|---------|--------|---------|---------|------|")
        
        for i, (ticker, result) in enumerate(sorted_results, 1):
            summary = result['summary']
            md.append(
                f"| {i} | {ticker} | **{summary['overall_score']:.1f}** | "
                f"{summary['module_score']:.1f} | {summary['perspective_score']:.1f} | "
                f"{summary['valuation_upside']:+.1f}% | {summary['recommendation']} |"
            )
        md.append("")
        
        md.append("---")
        md.append("")
        md.append("⚠️ **免责声明：** 仅供参考，不构成投资建议。")
        
        content = "\n".join(md)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 对比报告已导出：{filepath}")
        return str(filepath)
    
    def export_all_reports(self, formats: List[str] = ['html']) -> Dict:
        """导出所有股票的分析报告"""
        results = {}
        
        for ticker, result in self.results.items():
            print(f"📄 导出 {ticker} 详细报告...")
            exporter = ReportExporter(result)
            
            files = {}
            if 'html' in formats:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            files['html'] = exporter.export_html(f"{ticker}_analysis_{timestamp}.html")
            
            results[ticker] = files
        
        return results


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='批量分析多只股票')
    parser.add_argument('tickers', nargs='*', help='股票代码列表')
    parser.add_argument('--file', '-f', help='从文件读取股票列表')
    parser.add_argument('--workers', '-w', type=int, default=3, help='并发数（默认 3）')
    parser.add_argument('--no-cache', action='store_true', help='不使用缓存')
    parser.add_argument('--skip-p2', action='store_true', help='跳过 P2 功能（Variant View 等）')
    parser.add_argument('--export', choices=['md', 'html', 'all'], default='md', help='导出格式')
    parser.add_argument('--output', '-o', help='输出目录')
    
    args = parser.parse_args()
    
    # 获取股票列表
    tickers = args.tickers.copy() if args.tickers else []
    
    if args.file:
        with open(args.file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    tickers.append(line)
    
    if not tickers:
        print("❌ 请提供股票代码")
        print("用法：python batch_analysis.py AAPL MSFT GOOGL")
        print("      python batch_analysis.py --file stocks.txt")
        sys.exit(1)
    
    # 去重
    tickers = list(dict.fromkeys([t.upper() for t in tickers]))
    
    # 创建分析器
    analyzer = BatchAnalyzer(tickers, max_workers=args.workers)
    
    # 执行分析
    results = analyzer.analyze_all(
        use_cache=not args.no_cache,
        skip_p2=args.skip_p2
    )
    
    # 生成对比报告（HTML 格式）
    print()
    print("📊 生成对比报告...")
    comparison_file = analyzer.generate_comparison_report(format='html')
    
    # 导出 individual 报告（HTML 格式）
    print()
    print("📄 导出 individual 报告（HTML 格式）...")
    analyzer.export_all_reports(['html'])
    
    # 总结
    print()
    print("=" * 70)
    print("✅ 批量分析全部完成")
    print("=" * 70)
    print(f"分析股票：{len(results)} 只")
    print(f"对比报告：{comparison_file}")
    print(f"输出目录：{analyzer.output_dir}")
    print("=" * 70)


if __name__ == '__main__':
    main()
