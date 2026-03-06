#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成单只股票完整分析报告
用法：python generate_single_report.py AAPL
"""

import sys
import os
import statistics
from pathlib import Path

# 添加模块路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR / 'modules'))

from fetch_data import fetch_stock_data
from analyze_full import analyze_16_modules
from perspectives_full import analyze_perspectives_full
from valuation_full import ValuationCalculator
from key_forces import identify_key_forces
from bias_framework import check_biases
from variant_view import generate_variant_view
from export_report import ReportExporter


def calculate_summary(modules: dict, perspectives: dict, valuation: dict, biases: dict) -> dict:
    """计算综合评分和摘要信息"""
    
    # ========== 16 模块基础评分 ==========
    module_scores = []
    for key, module in modules.items():
        if isinstance(module, dict) and 'score' in module:
            module_scores.append(module['score'])
    
    avg_module_score = sum(module_scores) / len(module_scores) if module_scores else 0
    
    # ========== 6 大视角评分 ==========
    # 排除 'summary' 键，只计算 6 个实际视角
    perspective_scores = []
    perspective_keys = ['quality_compounder', 'imaginative_growth', 'fundamental_long_short', 
                       'deep_value', 'catalyst_driven', 'macro_tactical']
    
    for key in perspective_keys:
        if key in perspectives and isinstance(perspectives[key], dict) and 'total_score' in perspectives[key]:
            perspective_scores.append(perspectives[key]['total_score'])
    
    avg_perspective_score = sum(perspective_scores) / len(perspective_scores) if perspective_scores else 0
    
    # ========== 估值空间评分 ==========
    valuation_upside = valuation.get('summary', {}).get('upside_downside', 0)
    # 将上涨空间转换为评分：>20% 得 100 分，-20% 得 50 分，<-40% 得 0 分
    valuation_score = min(100, max(0, 75 + valuation_upside * 1.25))
    
    # ========== 综合评分（50% + 20% + 30%） ==========
    base_score = (
        avg_module_score * 0.50 +
        avg_perspective_score * 0.20 +
        valuation_score * 0.30
    )
    
    # ========== 财务红旗减分 ==========
    red_flags_data = biases.get('financial_red_flags', {})
    red_flags = red_flags_data.get('flags', []) if isinstance(red_flags_data, dict) else []
    red_flag_penalty = sum(
        15 if flag.get('risk') == '高' else
        8 if flag.get('risk') == '中' else
        3 if flag.get('risk') == '低' else 0
        for flag in red_flags
    )
    
    overall_score = max(0, base_score - red_flag_penalty)
    
    # ========== MSCI Barra 6 大因子评分 ==========
    # 质量因子（30%）- 7 个模块
    quality_modules = ['A_revenue_quality', 'B_profitability', 'C_cash_flow', 
                      'E_competitive_landscape', 'H_partners', 
                      'I_management', 'O_accounting']
    quality_score = sum(modules.get(m, {}).get('score', 0) for m in quality_modules if modules.get(m)) / 7
    
    # 成长因子（25%）- 3 个模块
    growth_modules = ['F_core_kpis', 'G_products', 'N_rd_efficiency']
    growth_score = sum(modules.get(m, {}).get('score', 0) for m in growth_modules if modules.get(m)) / 3
    
    # 价值因子（20%）
    value_score = modules.get('K_valuation', {}).get('score', 0)
    
    # 情绪因子（10%）
    sentiment_modules = ['D_forward_guidance', 'L_ownership']
    sentiment_score = sum(modules.get(m, {}).get('score', 0) for m in sentiment_modules if modules.get(m)) / 2
    
    # 宏观因子（10%）
    macro_score = modules.get('J_macro', {}).get('score', 0)
    
    # ESG 因子（5%）
    esg_score = modules.get('P_esg', {}).get('score', 0)
    
    # MSCI Barra 综合评分（0-100 分制）
    barra_score = (
        quality_score * 0.30 +
        growth_score * 0.25 +
        value_score * 0.20 +
        sentiment_score * 0.10 +
        macro_score * 0.10 +
        esg_score * 0.05
    )
    # 注意：模块评分是 0-100 分制，所以 barra_score 也是 0-100 分
    
    # ========== 置信度计算 ==========
    # 投资视角分歧度
    if len(perspective_scores) >= 2:
        perspective_std = statistics.stdev(perspective_scores)
        if perspective_std < 10:
            perspective_conf = 100
        elif perspective_std < 20:
            perspective_conf = 70
        else:
            perspective_conf = 40
    else:
        perspective_conf = 50
    
    # 估值方法分歧度
    valuation_methods = valuation.get('methods', {})
    upside_values = [m.get('upside_downside', 0) for m in valuation_methods.values() if isinstance(m, dict) and 'upside_downside' in m]
    
    if len(upside_values) >= 2:
        upside_std = statistics.stdev(upside_values)
        if upside_std < 10:
            upside_conf = 100
        elif upside_std < 20:
            upside_conf = 70
        else:
            upside_conf = 40
    else:
        upside_conf = 50
    
    # 综合置信度
    confidence_score = (perspective_conf + upside_conf) / 2
    if confidence_score >= 80:
        confidence = '高'
    elif confidence_score >= 60:
        confidence = '中'
    else:
        confidence = '低'
    
    # ========== 投资建议 ==========
    if overall_score >= 80:
        recommendation = '强烈买入'
    elif overall_score >= 70:
        recommendation = '买入'
    elif overall_score >= 60:
        recommendation = '持有'
    elif overall_score >= 50:
        recommendation = '减持'
    else:
        recommendation = '卖出'
    
    return {
        'overall_score': overall_score,
        'recommendation': recommendation,
        'confidence': confidence,
        'valuation_upside': valuation_upside,
        'barra_score': barra_score,
        'barra_factors': {
            'quality': quality_score,
            'growth': growth_score,
            'value': value_score,
            'sentiment': sentiment_score,
            'macro': macro_score,
            'esg': esg_score
        }
    }


def main():
    if len(sys.argv) < 2:
        print("用法：python generate_single_report.py <股票代码>")
        print("示例：python generate_single_report.py AAPL")
        sys.exit(1)
    
    ticker = sys.argv[1].upper()
    print(f"🚀 开始分析 {ticker}...")
    
    # 1. 获取数据
    print("📊 获取数据...")
    data = fetch_stock_data(ticker)
    
    if not data:
        print("❌ 数据获取失败")
        sys.exit(1)
    
    # 2. 16 模块分析
    print("🔍 执行 16 模块分析...")
    modules_result = analyze_16_modules(data)
    
    # 3. 6 大视角分析
    print("👁️ 执行 6 大投资哲学视角分析...")
    perspectives_result = analyze_perspectives_full(ticker, data)
    
    # 4. 估值分析
    print("💰 执行估值分析...")
    valuation_analyzer = ValuationCalculator(data)
    valuation_result = valuation_analyzer.calculate_all()
    
    # 5. Key Forces
    print("🎯 识别关键驱动力...")
    forces = identify_key_forces(data)
    
    # 6. 反偏见框架
    print("⚠️ 反偏见检查...")
    biases = check_biases(data)
    
    # 7. Variant View
    print("💡 生成变异视角...")
    variant_view = generate_variant_view(ticker, data)
    
    # 8. 计算综合评分
    print("📊 计算综合评分...")
    summary = calculate_summary(modules_result, perspectives_result, valuation_result, biases)
    
    print(f"   综合评分：{summary['overall_score']:.1f}/100")
    print(f"   MSCI Barra: {summary['barra_score']:.1f}/100")
    print(f"   投资建议：{summary['recommendation']}")
    print(f"   置信度：{summary['confidence']}")
    
    # 9. 整合结果
    result = {
        'ticker': ticker,
        'data': data,
        'modules': modules_result,
        'perspectives': perspectives_result,
        'valuation': valuation_result,
        'key_forces': forces,
        'biases': biases,
        'variant_view': variant_view,
        'summary': summary
    }
    
    # 10. 导出报告
    print("📝 生成报告...")
    output_dir = os.environ.get('OUTPUT_DIR', Path.home() / '.openclaw' / 'tech-earnings-output')
    exporter = ReportExporter(result, str(output_dir))
    html_file = exporter.export_html()
    
    print(f"\n✅ 报告生成完成：{html_file}")
    return html_file

if __name__ == '__main__':
    main()
