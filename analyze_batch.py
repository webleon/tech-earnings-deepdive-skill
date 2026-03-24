#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量分析入口
用法：python analyze_batch.py AAPL MSFT GOOGL
"""

import sys
import os
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict
import time

# 添加模块路径
sys.path.insert(0, str(Path(__file__).parent / 'modules'))

from core import analyze_single_stock, export_report


class BatchAnalyzer:
    """批量分析器（带速率限制）"""
    
    def __init__(self, tickers: List[str], max_workers: int = 3, 
                 rate_limit: int = 10, rate_period: int = 60):
        """
        Args:
            tickers: 股票代码列表
            max_workers: 最大并发数
            rate_limit: 每 rate_period 秒最多请求次数
            rate_period: 速率限制周期 (秒)
        """
        self.tickers = tickers
        self.max_workers = max_workers
        self.rate_limit = rate_limit
        self.rate_period = rate_period
        self.results = {}
        self.request_times = []  # 记录请求时间
        
        # 输出目录
        output_base = os.environ.get('OUTPUT_DIR', Path.home() / '.openclaw' / 'tech-earnings-output')
        self.output_dir = Path(output_base) / 'batch'
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def _enforce_rate_limit(self):
        """执行速率限制"""
        now = time.time()
        
        # 移除过期的请求时间
        self.request_times = [t for t in self.request_times if now - t < self.rate_period]
        
        # 如果达到限制，等待
        if len(self.request_times) >= self.rate_limit:
            oldest = min(self.request_times)
            wait_time = self.rate_period - (now - oldest) + 1
            if wait_time > 0:
                print(f"⏳ 触发速率限制，等待 {wait_time:.1f} 秒...")
                time.sleep(wait_time)
                self.request_times = []  # 重置
        
        # 记录本次请求
        self.request_times.append(time.time())
    
    def analyze_all(self, use_cache: bool = True) -> Dict:
        """分析所有股票（完整流程）"""
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
            # 提交任务（始终完整分析，包含 Variant View）
            future_to_ticker = {}
            for ticker in self.tickers:
                # 速率限制
                self._enforce_rate_limit()
                future = executor.submit(analyze_single_stock, ticker, use_cache)
                future_to_ticker[future] = ticker
            
            # 收集结果
            completed = 0
            for future in as_completed(future_to_ticker):
                ticker = future_to_ticker[future]
                try:
                    result = future.result()
                    self.results[ticker] = result
                    completed += 1
                    
                    # 显示进度
                    score = result['summary']['overall_score']
                    rec = result['summary']['recommendation']
                    print(f"✅ [{completed}/{len(self.tickers)}] {ticker}: "
                          f"{score:.1f}/100 - {rec}")
                except Exception as e:
                    print(f"❌ [{ticker}] 分析失败：{e}")
        
        print()
        print("=" * 70)
        print(f"✅ 批量分析完成：{len(self.results)}/{len(self.tickers)} 只股票")
        print("=" * 70)
        
        # 生成对比报告
        self.generate_comparison_report()
        
        return self.results
    
    def generate_comparison_report(self):
        """生成多股对比报告（增强版）"""
        if not self.results:
            return
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"comparison_{timestamp}.html"
        filepath = self.output_dir / filename
        
        # 增强版对比报告
        html = ['<!DOCTYPE html>', '<html><head><meta charset="UTF-8">',
                '<title>批量分析对比报告</title>',
                '<style>',
                'body { font-family: Arial, sans-serif; padding: 40px; }',
                'table { border-collapse: collapse; width: 100%; margin: 20px 0; }',
                'th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }',
                'th { background: #333; color: white; }',
                'tr:nth-child(even) { background: #f5f5f5; }',
                '.score-high { color: #27ae60; font-weight: bold; }',
                '.score-medium { color: #f39c12; font-weight: bold; }',
                '.score-low { color: #c0392b; font-weight: bold; }',
                'h2 { color: #333; border-left: 4px solid #333; padding-left: 15px; margin-top: 40px; }',
                '.section { margin: 30px 0; }',
                '</style>',
                '</head><body>',
                '<h1>📊 批量分析对比报告</h1>',
                f'<p>生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>',
                f'<p>分析股票：{", ".join(self.results.keys())}</p>']
        
        # 第一部分：综合评分对比
        html.extend(['<div class="section">',
                    '<h2>1️⃣ 综合评分对比</h2>',
                    '<table>',
                    '<tr><th>股票代码</th><th>综合评分</th><th>MSCI Barra</th>',
                    '<th>投资建议</th><th>置信度</th></tr>'])
        
        for ticker, result in sorted(self.results.items()):
            summary = result['summary']
            score = summary['overall_score']
            barra = summary['barra_score']
            rec = summary['recommendation']
            conf = summary['confidence']
            
            score_class = 'score-high' if score >= 70 else 'score-medium' if score >= 50 else 'score-low'
            
            html.append(f'<tr>'
                       f'<td><strong>{ticker}</strong></td>'
                       f'<td class="{score_class}">{score:.1f}/100</td>'
                       f'<td>{barra:.1f}</td>'
                       f'<td>{rec}</td>'
                       f'<td>{conf}</td>'
                       f'</tr>')
        
        html.extend(['</table>', '</div>'])
        
        # 第二部分：基础估值指标
        html.extend(['<div class="section">',
                    '<h2>2️⃣ 基础估值指标</h2>',
                    '<table>',
                    '<tr><th>股票</th><th>股价</th><th>市值 (亿)</th>',
                    '<th>PE</th><th>Forward PE</th><th>PB</th></tr>'])
        
        for ticker, result in sorted(self.results.items()):
            price_data = result['data'].get('price', {})
            price = price_data.get('current_price', 0)
            market_cap = price_data.get('market_cap', 0) / 1e8  # 转换为亿
            pe = price_data.get('pe_ratio', 0)
            forward_pe = price_data.get('forward_pe', 0)
            pb = price_data.get('price_to_book', 0)
            
            html.append(f'<tr>'
                       f'<td><strong>{ticker}</strong></td>'
                       f'<td>${price:.2f}</td>'
                       f'<td>${market_cap:.1f}B</td>'
                       f'<td>{pe:.1f}</td>'
                       f'<td>{forward_pe:.1f}</td>'
                       f'<td>{pb:.1f}</td>'
                       f'</tr>')
        
        html.extend(['</table>', '</div>'])
        
        # 第三部分：6 种估值方法对比
        html.extend(['<div class="section">',
                    '<h2>3️⃣ 6 种估值方法对比（上涨空间 %）</h2>',
                    '<table>',
                    '<tr><th>股票</th>',
                    '<th>Owner Earnings</th>',
                    '<th>PEG</th>',
                    '<th>Reverse DCF</th>',
                    '<th>Magic Formula</th>',
                    '<th>EV/EBITDA</th>',
                    '<th>EV/Revenue+Rule40</th></tr>'])
        
        method_map = {
            'owner_earnings': 'owner_earnings',
            'peg': 'peg',
            'reverse_dcf': 'reverse_dcf',
            'magic_formula': 'magic_formula',
            'ev_ebitda': 'ev_ebitda',
            'ev_revenue_rule40': 'ev_revenue_rule40'
        }
        
        for ticker, result in sorted(self.results.items()):
            valuation = result['valuation']
            
            html.append(f'<tr><td><strong>{ticker}</strong></td>')
            for method_key in method_map.values():
                method_data = valuation.get(method_key, {})
                upside = method_data.get('upside_downside', 0)
                color_class = 'score-high' if upside > 20 else 'score-medium' if upside > -20 else 'score-low'
                html.append(f'<td class="{color_class}">{upside:+.1f}%</td>')
            html.append('</tr>')
        
        html.extend(['</table>', '</div>'])
        
        # 第四部分：综合估值结果
        html.extend(['<div class="section">',
                    '<h2>4️⃣ 综合估值结果</h2>',
                    '<table>',
                    '<tr><th>股票</th><th>平均合理价值</th><th>当前股价</th>',
                    '<th>上涨/下跌空间</th><th>投资建议</th><th>置信度</th></tr>'])
        
        for ticker, result in sorted(self.results.items()):
            valuation_summary = result['valuation'].get('summary', {})
            fair_value = valuation_summary.get('average_fair_value', 0)
            current_price = valuation_summary.get('current_price', 0)
            upside = valuation_summary.get('upside_downside', 0)
            rec = valuation_summary.get('recommendation', 'N/A')
            conf = valuation_summary.get('confidence', 'N/A')
            
            upside_class = 'score-high' if upside > 20 else 'score-medium' if upside > -20 else 'score-low'
            
            html.append(f'<tr>'
                       f'<td><strong>{ticker}</strong></td>'
                       f'<td>${fair_value:.2f}</td>'
                       f'<td>${current_price:.2f}</td>'
                       f'<td class="{upside_class}">{upside:+.1f}%</td>'
                       f'<td>{rec}</td>'
                       f'<td>{conf}</td>'
                       f'</tr>')
        
        html.extend(['</table>', '</div>'])
        
        # 第五部分：6 大投资视角
        html.extend(['<div class="section">',
                    '<h2>5️⃣ 6 大投资视角评分</h2>',
                    '<table>',
                    '<tr><th>股票</th>',
                    '<th>质量复利</th>',
                    '<th>想象力成长</th>',
                    '<th>基本面多空</th>',
                    '<th>深度价值</th>',
                    '<th>催化剂驱动</th>',
                    '<th>宏观战术</th></tr>'])
        
        perspective_names = {
            'quality_compounder': '质量复利',
            'imaginative_growth': '想象力成长',
            'fundamental_long_short': '基本面多空',
            'deep_value': '深度价值',
            'catalyst_driven': '催化剂驱动',
            'macro_tactical': '宏观战术'
        }
        
        for ticker, result in sorted(self.results.items()):
            perspectives = result['perspectives']
            
            html.append(f'<tr><td><strong>{ticker}</strong></td>')
            for key in perspective_names.keys():
                perspective = perspectives.get(key, {})
                score = perspective.get('total_score', 0)
                color_class = 'score-high' if score >= 70 else 'score-medium' if score >= 50 else 'score-low'
                html.append(f'<td class="{color_class}">{score:.1f}</td>')
            html.append('</tr>')
        
        html.extend(['</table>', '</div>'])
        
        # 第六部分：Key Forces
        html.extend(['<div class="section">',
                    '<h2>6️⃣ 关键驱动力（Key Forces）</h2>',
                    '<table>',
                    '<tr><th>股票</th><th>关键驱动力</th></tr>'])
        
        for ticker, result in sorted(self.results.items()):
            key_forces = result['key_forces']
            forces_text = '<br>'.join([
                f"• {kf.get('name', 'N/A')} (影响力：{kf.get('impact_score', 0)}/10)"
                for kf in key_forces[:3]  # 只显示前 3 个
            ])
            html.append(f'<tr>'
                       f'<td><strong>{ticker}</strong></td>'
                       f'<td>{forces_text}</td>'
                       f'</tr>')
        
        html.extend(['</table>', '</div>'])
        
        html.extend(['</body></html>'])
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(html))
        
        print(f"📊 对比报告已生成：{filepath}")


def main():
    if len(sys.argv) < 2:
        print("用法：python analyze_batch.py <股票代码列表>")
        print("示例：python analyze_batch.py AAPL MSFT GOOGL")
        sys.exit(1)
    
    tickers = [t.upper() for t in sys.argv[1:]]
    analyzer = BatchAnalyzer(tickers, max_workers=3)
    analyzer.analyze_all(use_cache=True)


if __name__ == '__main__':
    main()
