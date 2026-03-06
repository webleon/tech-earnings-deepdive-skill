#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据获取模块 - 使用 yfinance + SEC EDGAR
无需 API Key，完全免费
"""

import yfinance as yf
import requests
import json
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

# edgartools for SEC Form 4 (insider trades)
try:
    from edgar import Company, set_identity
    set_identity("Tech Earnings Deepdive script@example.com")
    EDGAR_AVAILABLE = True
except ImportError:
    EDGAR_AVAILABLE = False
    print("⚠️ edgartools not installed. Run: pip install edgartools")

# 缓存配置
CACHE_DIR = Path(__file__).parent / '..' / 'cache'
CACHE_DIR.mkdir(parents=True, exist_ok=True)
CACHE_TTL_HOURS = 1  # 缓存有效期 1 小时（股价实时变化）


class StockDataFetcher:
    """股票数据获取器（yfinance）"""
    
    def __init__(self, ticker: str):
        self.ticker = ticker.upper()
        self.stock = yf.Ticker(ticker)
        self.cache_file = CACHE_DIR / f"{self.ticker}_data.json"
        
        # SEC User-Agent（必须设置）
        # 从本地配置文件读取，避免提交敏感信息到 GitHub
        local_config_file = Path(__file__).parent / '..' / 'config.local.json'
        sec_user_agent = 'Tech Earnings Deepdive script@example.com'  # 默认值
        
        if local_config_file.exists():
            try:
                with open(local_config_file, 'r') as f:
                    local_config = json.load(f)
                    sec_user_agent = local_config.get('sec_user_agent', sec_user_agent)
            except:
                pass
        
        self.sec_headers = {
            'User-Agent': sec_user_agent
        }
    
    def is_cache_valid(self) -> bool:
        """检查缓存是否有效"""
        if not self.cache_file.exists():
            return False
        
        try:
            with open(self.cache_file, 'r') as f:
                cache = json.load(f)
            
            cached_at = datetime.fromisoformat(cache['fetched_at'])
            if datetime.now() - cached_at < timedelta(hours=CACHE_TTL_HOURS):
                return True
        except:
            pass
        
        return False
    
    def load_cache(self) -> dict:
        """加载缓存数据（带异常处理）"""
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError, PermissionError) as e:
            print(f"⚠️ 加载缓存失败：{e}")
            return {}
    
    def save_cache(self, data: dict):
        """保存缓存数据（带异常处理）"""
        try:
            CACHE_DIR.mkdir(parents=True, exist_ok=True)
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except (PermissionError, OSError) as e:
            print(f"⚠️ 保存缓存失败：{e}")
    
    def get_price_data(self) -> dict:
        """获取价格数据"""
        try:
            history = self.stock.history(period="1y")
            info = self.stock.info
            
            return {
                'current_price': info.get('currentPrice', history['Close'].iloc[-1]),
                'previous_close': info.get('previousClose', 0),
                'open': info.get('open', 0),
                'day_high': info.get('dayHigh', 0),
                'day_low': info.get('dayLow', 0),
                '52_week_high': info.get('fiftyTwoWeekHigh', history['High'].max()),
                '52_week_low': info.get('fiftyTwoWeekLow', history['Low'].min()),
                'volume': info.get('volume', history['Volume'].iloc[-1]),
                'avg_volume': info.get('averageVolume', 0),
                'market_cap': info.get('marketCap', 0),
                'beta': info.get('beta', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'forward_pe': info.get('forwardPE', 0),
                'dividend_yield': info.get('dividendYield', 0),
                'eps': info.get('trailingEps', 0),
                'shares_outstanding': info.get('sharesOutstanding', 0)
            }
        except Exception as e:
            print(f"⚠️ 获取价格数据失败：{e}")
            return {}
    
    def get_financials(self) -> dict:
        """获取利润表数据"""
        try:
            financials = self.stock.financials
            cashflow = self.stock.cashflow
            info = self.stock.info
            
            # 获取最新年度数据
            def get_latest(series):
                """安全获取最新数据，返回 None 表示缺失"""
                if len(series) > 0:
                    value = series.iloc[0]
                    # 处理 NaN 和无穷大
                    if pd.isna(value) or not np.isfinite(value):
                        return None
                    return value
                return None
            
            # 获取股票期权费用 (SBC)
            def get_sbc():
                try:
                    if 'Stock Based Compensation' in cashflow.index:
                        return get_latest(cashflow.loc['Stock Based Compensation'])
                except:
                    pass
                return 0
            
            # 获取股本数据
            def get_shares_outstanding():
                try:
                    # 当前流通股数
                    current = info.get('sharesOutstanding', 0)
                    
                    # 尝试获取历史股数（简化：用当前代替）
                    # 完整实现需要查询历史数据
                    return {
                        'current': current,
                        'previous_year': current * 0.98,  # 估算：假设年稀释 2%
                        'change_rate': 0.02  # 估算稀释率
                    }
                except:
                    return {
                        'current': 0,
                        'previous_year': 0,
                        'change_rate': 0
                    }
            
            sbc = get_sbc()
            net_income = get_latest(financials.loc['Net Income']) if 'Net Income' in financials.index else 0
            revenue = get_latest(financials.loc['Total Revenue']) if 'Total Revenue' in financials.index else 1
            
            # 估算 Non-GAAP 净利润（GAAP + SBC）
            non_gaap_net_income = net_income + sbc if sbc > 0 else net_income
            
            # 计算稀释相关指标
            shares = get_shares_outstanding()
            dilution_rate = shares['change_rate']
            sbc_to_revenue_ratio = (sbc / revenue) * 100 if revenue > 0 else 0
            
            # 计算应收账款/收入比率
            balance_sheet = self.stock.balance_sheet
            accounts_receivable = get_latest(balance_sheet.loc['Accounts Receivable']) if 'Accounts Receivable' in balance_sheet.index else 0
            receivables_ratio = (accounts_receivable / revenue * 100) if revenue > 0 else 0
            
            # 计算内部人卖出/总股本比率
            insider_trades = self.get_insider_trades()
            insider_selling_shares = sum(t.get('shares', 0) for t in insider_trades.get('recent_trades', []) if t.get('direction') == 'sell')
            insider_selling_ratio = (insider_selling_shares / shares['current'] * 100) if shares['current'] > 0 else 0
            
            return {
                'total_revenue': revenue,
                'cost_of_revenue': get_latest(financials.loc['Cost Of Revenue']) if 'Cost Of Revenue' in financials.index else 0,
                'gross_profit': get_latest(financials.loc['Gross Profit']) if 'Gross Profit' in financials.index else 0,
                'operating_expenses': get_latest(financials.loc['Total Operating Expenses']) if 'Total Operating Expenses' in financials.index else 0,
                'operating_income': get_latest(financials.loc['Operating Income']) if 'Operating Income' in financials.index else 0,
                'net_income': net_income,
                'ebitda': get_latest(financials.loc['EBITDA']) if 'EBITDA' in financials.index else 0,
                'research_development': get_latest(financials.loc['Research Development']) if 'Research Development' in financials.index else 0,
                'stock_based_compensation': sbc,
                'non_gaap_net_income': non_gaap_net_income,
                'shares_outstanding': shares['current'],
                'shares_dilution_rate': dilution_rate,
                'sbc_to_revenue_ratio': sbc_to_revenue_ratio,
                # 新增指标
                'accounts_receivable': accounts_receivable,
                'receivables_ratio': receivables_ratio,
                'insider_selling_ratio': insider_selling_ratio,
                # 增长率计算
                'revenue_growth_yoy': self._calculate_growth(financials.loc['Total Revenue']) if 'Total Revenue' in financials.index else 0,
                'net_income_growth_yoy': self._calculate_growth(financials.loc['Net Income']) if 'Net Income' in financials.index else 0
            }
        except Exception as e:
            print(f"⚠️ 获取利润表失败：{e}")
            return {}
    
    def get_balance_sheet(self) -> dict:
        """获取资产负债表数据"""
        try:
            bs = self.stock.balance_sheet
            
            def get_latest(series):
                if len(series) > 0:
                    return series.iloc[0]
                return 0
            
            return {
                'total_assets': get_latest(bs.loc['Total Assets']) if 'Total Assets' in bs.index else 0,
                'total_liabilities': get_latest(bs.loc['Total Liabilities Net Minority Interest']) if 'Total Liabilities Net Minority Interest' in bs.index else 0,
                'total_equity': get_latest(bs.loc['Total Equity Gross Minority Interest']) if 'Total Equity Gross Minority Interest' in bs.index else 0,
                'cash_and_equivalents': get_latest(bs.loc['Cash And Cash Equivalents']) if 'Cash And Cash Equivalents' in bs.index else 0,
                'accounts_receivable': get_latest(bs.loc['Accounts Receivable']) if 'Accounts Receivable' in bs.index else 0,
                'inventory': get_latest(bs.loc['Inventory']) if 'Inventory' in bs.index else 0,
                'current_assets': get_latest(bs.loc['Current Assets']) if 'Current Assets' in bs.index else 0,
                'current_liabilities': get_latest(bs.loc['Current Liabilities']) if 'Current Liabilities' in bs.index else 0,
                'long_term_debt': get_latest(bs.loc['Long Term Debt']) if 'Long Term Debt' in bs.index else 0,
                'total_debt': get_latest(bs.loc['Total Debt']) if 'Total Debt' in bs.index else 0,
                # 计算指标
                'current_ratio': get_latest(bs.loc['Current Assets']) / get_latest(bs.loc['Current Liabilities']) if 'Current Assets' in bs.index and 'Current Liabilities' in bs.index and get_latest(bs.loc['Current Liabilities']) > 0 else 0,
                'debt_to_equity': get_latest(bs.loc['Total Debt']) / get_latest(bs.loc['Total Equity Gross Minority Interest']) if 'Total Equity Gross Minority Interest' in bs.index and get_latest(bs.loc['Total Equity Gross Minority Interest']) > 0 else 0
            }
        except Exception as e:
            print(f"⚠️ 获取资产负债表失败：{e}")
            return {}
    
    def get_cashflow(self) -> dict:
        """获取现金流量表数据"""
        try:
            cf = self.stock.cashflow
            
            def get_latest(series):
                if len(series) > 0:
                    return series.iloc[0]
                return 0
            
            return {
                'operating_cashflow': get_latest(cf.loc['Operating Cash Flow']) if 'Operating Cash Flow' in cf.index else 0,
                'investing_cashflow': get_latest(cf.loc['Investing Cash Flow']) if 'Investing Cash Flow' in cf.index else 0,
                'financing_cashflow': get_latest(cf.loc['Financing Cash Flow']) if 'Financing Cash Flow' in cf.index else 0,
                'free_cashflow': get_latest(cf.loc['Free Cash Flow']) if 'Free Cash Flow' in cf.index else 0,
                'capital_expenditure': get_latest(cf.loc['Capital Expenditure']) if 'Capital Expenditure' in cf.index else 0,
                'depreciation_amortization': get_latest(cf.loc['Depreciation And Amortization']) if 'Depreciation And Amortization' in cf.index else 0,
                # 计算指标
                'fcf_margin': get_latest(cf.loc['Free Cash Flow']) / get_latest(cf.loc['Operating Cash Flow']) if 'Operating Cash Flow' in cf.index and get_latest(cf.loc['Operating Cash Flow']) > 0 else 0,
                'cash_conversion': get_latest(cf.loc['Free Cash Flow']) / get_latest(cf.loc['Net Income']) if 'Net Income' in cf.index and get_latest(cf.loc['Net Income']) > 0 else 0
            }
        except Exception as e:
            print(f"⚠️ 获取现金流量表失败：{e}")
            return {}
    
    def get_analyst_estimates(self) -> dict:
        """获取分析师预期"""
        try:
            return {
                'target_price_mean': self.stock.analyst_price_targets.get('mean', 0),
                'target_price_high': self.stock.analyst_price_targets.get('high', 0),
                'target_price_low': self.stock.analyst_price_targets.get('low', 0),
                'recommendation': self.stock.recommendations.iloc[0]['period'] if len(self.stock.recommendations) > 0 else '',
                'strong_buy': int(self.stock.recommendations.iloc[0]['strongBuy']) if len(self.stock.recommendations) > 0 else 0,
                'buy': int(self.stock.recommendations.iloc[0]['buy']) if len(self.stock.recommendations) > 0 else 0,
                'hold': int(self.stock.recommendations.iloc[0]['hold']) if len(self.stock.recommendations) > 0 else 0,
                'sell': int(self.stock.recommendations.iloc[0]['sell']) if len(self.stock.recommendations) > 0 else 0,
                'strong_sell': int(self.stock.recommendations.iloc[0]['strongSell']) if len(self.stock.recommendations) > 0 else 0
            }
        except Exception as e:
            print(f"⚠️ 获取分析师预期失败：{e}")
            return {}
    
    def get_insider_trades(self) -> dict:
        """获取内部人交易数据（SEC Form 4）"""
        if not EDGAR_AVAILABLE:
            print("⚠️ edgartools 未安装，跳过内部人交易数据")
            return {}
        
        try:
            print(f"📊 获取 {self.ticker} 内部人交易数据...")
            company = Company(self.ticker)
            
            # 获取最近 10 条 Form 4 记录
            filings = company.get_filings(form="4")
            if not filings or len(filings) == 0:
                print("⚠️ 未找到 Form 4 记录")
                return {}
            
            recent_filings = filings[:10]  # 最近 10 条
            
            insider_trades = []
            total_buy_value = 0
            total_sell_value = 0
            buy_count = 0
            sell_count = 0
            
            for filing in recent_filings:
                try:
                    form4 = filing.obj()
                    insider_name = form4.insider_name if hasattr(form4, 'insider_name') else 'Unknown'
                    reporting_period = str(form4.reporting_period) if hasattr(form4, 'reporting_period') else ''
                    
                    # 获取交易活动
                    activities = form4.get_transaction_activities() if hasattr(form4, 'get_transaction_activities') else []
                    
                    for txn in activities:
                        # 提取交易信息
                        txn_code = getattr(txn, 'code', '')
                        shares = getattr(txn, 'shares', 0) or 0
                        value = getattr(txn, 'value', 0) or 0
                        price = getattr(txn, 'price_per_share', 0) or 0
                        txn_type = getattr(txn, 'transaction_type', '')
                        
                        # 判断买卖方向
                        direction = 'other'
                        if txn_code in ['P', 'A', 'M'] or 'purchase' in txn_type.lower() or 'award' in txn_type.lower():
                            direction = 'buy'
                            buy_count += 1
                            total_buy_value += value
                        elif txn_code in ['S', 'D', 'F'] or 'sale' in txn_type.lower() or 'disposal' in txn_type.lower():
                            direction = 'sell'
                            sell_count += 1
                            total_sell_value += value
                        
                        trade = {
                            'filing_date': str(filing.filing_date),
                            'transaction_date': str(reporting_period),
                            'insider_name': str(insider_name),
                            'transaction_type': str(txn_type),
                            'transaction_code': str(txn_code),
                            'shares': int(shares) if shares else 0,
                            'price_per_share': float(price) if price and price > 0 else None,
                            'total_value': float(value) if value else 0,
                            'direction': direction
                        }
                        insider_trades.append(trade)
                        
                except Exception as e:
                    print(f"⚠️ 解析单条 Form 4 失败：{e}")
                    continue
            
            # 计算净买卖
            net_value = total_buy_value - total_sell_value
            net_direction = 'neutral'
            if net_value > 0:
                net_direction = 'net_buy'
            elif net_value < 0:
                net_direction = 'net_sell'
            
            # 内部人情绪
            if buy_count == 0 and sell_count == 0:
                sentiment = 'neutral'
            elif buy_count > sell_count * 1.5:
                sentiment = 'bullish'
            elif sell_count > buy_count * 1.5:
                sentiment = 'bearish'
            else:
                sentiment = 'neutral'
            
            print(f"✅ 获取到 {len(insider_trades)} 条内部人交易记录 (买:{buy_count}, 卖:{sell_count})")
            
            return {
                'recent_trades': insider_trades[:20],  # 最多返回 20 条
                'summary': {
                    'total_trades': len(insider_trades),
                    'buy_count': buy_count,
                    'sell_count': sell_count,
                    'total_buy_value': total_buy_value,
                    'total_sell_value': total_sell_value,
                    'net_value': net_value,
                    'net_direction': net_direction,
                    'insider_sentiment': sentiment
                }
            }
        except Exception as e:
            print(f"⚠️ 获取内部人交易失败：{e}")
            return {}
    
    def get_institutional_ownership(self) -> dict:
        """获取机构持仓数据（SEC Form 13F）"""
        if not EDGAR_AVAILABLE:
            print("⚠️ edgartools 未安装，跳过机构持仓数据")
            return {}
        
        try:
            print(f"📊 获取 {self.ticker} 机构持仓数据...")
            
            # 获取最新的 13F 文件
            from edgar import get_filings
            filings = get_filings(form="13F-HR")
            if not filings or len(filings) == 0:
                print("⚠️ 未找到 13F 记录")
                return {}
            
            # 解析最新几份 13F 报告，查找持有该股票的机构
            # 使用 yfinance 获取机构持仓数据（数据来源：SEC 13F）
            try:
                institutional_holders = self.stock.institutional_holders
                if institutional_holders is not None and len(institutional_holders) > 0:
                    # 转换为字典列表
                    holders_list = []
                    total_shares = 0
                    total_value = 0
                    
                    for _, row in institutional_holders.iterrows():
                        holder = {
                            'holder': str(row.get('Holder', '')),
                            'shares': int(row.get('Shares', 0)) if pd.notna(row.get('Shares')) else 0,
                            'date_reported': str(row.get('Date Reported', '')),
                            'percent_out': float(row.get('% Out', 0)) if pd.notna(row.get('% Out')) else 0,
                            'value': int(row.get('Value', 0)) if pd.notna(row.get('Value')) else 0
                        }
                        holders_list.append(holder)
                        total_shares += holder['shares']
                        total_value += holder['value']
                    
                    # 计算机构持仓比例
                    try:
                        shares_outstanding = self.stock.info.get('sharesOutstanding', 0)
                    except:
                        shares_outstanding = 0
                    ownership_percentage = (total_shares / shares_outstanding * 100) if shares_outstanding > 0 else 0
                    
                    print(f"✅ 获取到 {len(holders_list)} 家机构持仓数据")
                    
                    return {
                        'top_holders': holders_list[:20],  # 前 20 大机构
                        'summary': {
                            'total_institutions': len(holders_list),
                            'total_shares_held': total_shares,
                            'total_value': total_value,
                            'ownership_percentage': round(ownership_percentage, 2),
                            'concentration_top10': sum(h['shares'] for h in holders_list[:10]) / total_shares * 100 if total_shares > 0 else 0
                        }
                    }
                else:
                    print("⚠️ 无机构持仓数据")
                    return {}
            except Exception as e:
                print(f"⚠️ 获取机构持仓失败：{e}")
                return {}
                
        except Exception as e:
            print(f"⚠️ 获取机构持仓失败：{e}")
            return {}
    
    def get_sec_filings(self) -> dict:
        """获取 SEC 文件列表"""
        try:
            # 获取 CIK 编号
            cik_url = f"https://data.sec.gov/submissions/CIK{self.ticker}.json"
            response = requests.get(cik_url, headers=self.sec_headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                recent = data.get('filings', {}).get('recent', {})
                return {
                    'accession_numbers': recent.get('accessionNumber', [])[:10],
                    'filing_dates': recent.get('filingDate', [])[:10],
                    'report_dates': recent.get('reportDate', [])[:10],
                    'form_types': recent.get('form', [])[:10],
                    'titles': recent.get('primaryDocument', [])[:10]
                }
        except Exception as e:
            print(f"⚠️ 获取 SEC 文件失败：{e}")
        return {}
    
    def get_company_info(self) -> dict:
        """获取公司基本信息"""
        try:
            info = self.stock.info
            return {
                'company_name': info.get('longName', ''),
                'sector': info.get('sector', ''),
                'industry': info.get('industry', ''),
                'website': info.get('website', ''),
                'description': info.get('longBusinessSummary', ''),
                'employees': info.get('fullTimeEmployees', 0),
                'headquarters': info.get('city', '') + ', ' + info.get('state', '') + ', ' + info.get('country', '') if info.get('city') else '',
                'founded': info.get('founded', 0),
                'ceo': info.get('companyOfficers', [{}])[0].get('name', '') if info.get('companyOfficers') else ''
            }
        except Exception as e:
            print(f"⚠️ 获取公司信息失败：{e}")
            return {}
    
    def _calculate_growth(self, series) -> float:
        """计算增长率（YoY）"""
        if len(series) >= 2:
            current = series.iloc[0]
            previous = series.iloc[1]
            if previous > 0:
                return (current - previous) / previous
        return 0
    
    def get_sm_expense(self) -> dict:
        """
        获取 S&M 费用（Selling & Marketing Expense）
        
        数据来源：
        1. yfinance 财报数据（主要）
        2. Finnhub 备用（如配置）
        
        返回：
        {
            'annual': [年度 S&M 费用列表],
            'quarterly': [季度 S&M 费用列表],
            'latest_annual': 最新年度费用,
            'latest_quarterly': 最新季度费用,
            'yoy_growth': 同比增长率
        }
        """
        result = {
            'annual': [],
            'quarterly': [],
            'latest_annual': 0,
            'latest_quarterly': 0,
            'yoy_growth': 0
        }
        
        try:
            # 1. 从 yfinance 获取 S&M 费用
            financials = self.stock.financials
            
            # 查找 S&M 相关字段
            sm_keywords = [
                'Selling And Marketing Expense',
                'Selling General And Administration',
                'Selling General Administrative',
                'Sales And Marketing'
            ]
            
            sm_row = None
            for keyword in sm_keywords:
                if keyword in financials.index:
                    sm_row = financials.loc[keyword]
                    break
            
            if sm_row is not None and len(sm_row) > 0:
                # 获取年度数据
                result['annual'] = sm_row.tolist()
                result['latest_annual'] = sm_row.iloc[0] if len(sm_row) > 0 else 0
                
                # 计算增长率
                if len(sm_row) >= 2 and sm_row.iloc[1] > 0:
                    result['yoy_growth'] = (sm_row.iloc[0] - sm_row.iloc[1]) / sm_row.iloc[1]
                
                print(f"✅ 获取到 S&M 费用：${result['latest_annual']/1e9:.2f}B (增长：{result['yoy_growth']*100:.1f}%)")
            
            # 2. Finnhub 备用（如 yfinance 失败）
            if result['latest_annual'] == 0 and self.finnhub_client:
                try:
                    financials_finnhub = self.finnhub_client.company_basic_financials(self.ticker, 'all')
                    if financials_finnhub:
                        # Finnhub 数据提取逻辑
                        pass  # 暂时不实现，yfinance 通常够用
                except:
                    pass
            
        except Exception as e:
            print(f"⚠️ 获取 S&M 费用失败：{e}")
        
        return result
    
    def get_all_data(self, use_cache=True) -> dict:
        """获取所有数据"""
        # 检查缓存
        if use_cache and self.is_cache_valid():
            print(f"✅ 使用缓存数据：{self.ticker}")
            return self.load_cache()
        
        print(f"📊 获取 {self.ticker} 数据...")
        
        data = {
            'symbol': self.ticker,
            'fetched_at': datetime.now().isoformat(),
            'company_info': self.get_company_info(),
            'price': self.get_price_data(),
            'financials': self.get_financials(),
            'balance_sheet': self.get_balance_sheet(),
            'cashflow': self.get_cashflow(),
            'analyst_estimates': self.get_analyst_estimates(),
            'sec_filings': self.get_sec_filings(),
            'insider_trades': self.get_insider_trades(),
            'institutional_ownership': self.get_institutional_ownership(),
            'sm_expense': self.get_sm_expense()  # S&M 费用
        }
        
        # 保存到缓存
        self.save_cache(data)
        print(f"✅ 数据已缓存：{self.cache_file}")
        
        return data


def fetch_stock_data(ticker: str, use_cache=True) -> dict:
    """便捷函数：获取股票数据"""
    fetcher = StockDataFetcher(ticker)
    return fetcher.get_all_data(use_cache=use_cache)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("用法：python fetch_data.py <股票代码> [use_cache=true/false]")
        print("示例：python fetch_data.py NVDA")
        print("      python fetch_data.py TSLA false")
        sys.exit(1)
    
    ticker = sys.argv[1]
    use_cache = sys.argv[2].lower() != 'false' if len(sys.argv) > 2 else True
    
    data = fetch_stock_data(ticker, use_cache)
    print(json.dumps(data, indent=2, ensure_ascii=False))
