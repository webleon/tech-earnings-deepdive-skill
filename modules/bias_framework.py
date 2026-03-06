#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
反偏见框架模块
6 大认知陷阱 + 7 大财务红旗 + 5 大科技盲区
"""

import sys
import json
from datetime import datetime


class BiasFramework:
    """反偏见检查框架"""
    
    def __init__(self, data: dict):
        self.data = data
        self.ticker = data.get('symbol', 'UNKNOWN')
        self.price = data.get('price', {})
        self.financials = data.get('financials', {})
        self.balance_sheet = data.get('balance_sheet', {})
        self.cashflow = data.get('cashflow', {})
        self.analyst = data.get('analyst_estimates', {})
    
    def check_all(self) -> dict:
        """执行所有反偏见检查"""
        print("⚠️ 执行反偏见检查...")
        
        result = {
            'cognitive_biases': self._check_cognitive_biases(),
            'financial_red_flags': self._check_financial_red_flags(),
            'tech_blind_spots': self._check_tech_blind_spots(),
            'pre_mortem': self._pre_mortem()
        }
        
        # 计算风险评分
        total_flags = (
            result['financial_red_flags']['total'] +
            result['tech_blind_spots']['total']
        )
        
        bias_count = sum(
            1 for bias in result['cognitive_biases'].values() 
            if bias.get('risk', False)
        )
        
        result['summary'] = {
            'total_red_flags': total_flags,
            'bias_warnings': bias_count,
            'risk_level': '高' if total_flags >= 3 or bias_count >= 3 else '中' if total_flags >= 1 else '低'
        }
        
        print(f"✅ 反偏见检查完成")
        print(f"   财务红旗：{total_flags}个")
        print(f"   认知偏见警告：{bias_count}个")
        print(f"   风险等级：{result['summary']['risk_level']}")
        
        return result
    
    def _check_cognitive_biases(self) -> dict:
        """检查 6 大认知陷阱"""
        biases = {}
        
        # 1. 确认偏误
        biases['confirmation_bias'] = self._check_confirmation_bias()
        
        # 2. 锚定效应
        biases['anchoring'] = self._check_anchoring()
        
        # 3. 叙事谬误
        biases['narrative'] = self._check_narrative()
        
        # 4. 从众心理
        biases['herding'] = self._check_herding()
        
        # 5. 处置效应
        biases['disposition'] = self._check_disposition()
        
        # 6. 过度自信
        biases['overconfidence'] = self._check_overconfidence()
        
        return biases
    
    def _check_confirmation_bias(self) -> dict:
        """检查确认偏误"""
        # 检查是否有看空观点
        analyst_ratings = self.analyst
        
        sell_count = analyst_ratings.get('sell', 0) + analyst_ratings.get('strong_sell', 0)
        total = sum([
            analyst_ratings.get('strong_buy', 0),
            analyst_ratings.get('buy', 0),
            analyst_ratings.get('hold', 0),
            sell_count
        ])
        
        sell_ratio = sell_count / total * 100 if total > 0 else 0
        
        risk = sell_ratio < 5  # 如果几乎没有卖出评级，可能存在确认偏误
        
        return {
            'name': '确认偏误',
            'description': '是否只关注支持自己看法的信息？',
            'checklist': [
                '是否主动搜索了看空分析？',
                '是否认真阅读了卖出评级理由？',
                '正面和负面论点是否平衡？'
            ],
            'action': '搜索 [ticker] bear case / short thesis',
            'risk': risk,
            'data': {
                'sell_ratio': round(sell_ratio, 2)
            }
        }
    
    def _check_anchoring(self) -> dict:
        """检查锚定效应"""
        current_price = self.price.get('current_price', 0)
        week_52_high = self.price.get('52_week_high', 0)
        week_52_low = self.price.get('52_week_low', 0)
        
        # 检查当前价格是否在 52 周区间内
        if week_52_high > 0:
            position = (current_price - week_52_low) / (week_52_high - week_52_low) * 100
        else:
            position = 50
        
        risk = position < 20 or position > 80  # 接近极值时容易被锚定
        
        return {
            'name': '锚定效应',
            'description': '是否被历史股价锚定了判断？',
            'checklist': [
                '是否参考 52 周高/低价判断贵贱？',
                '如果不看历史价格，愿意现价买入吗？',
                '估值参数是否被历史数据锚定？'
            ],
            'action': '独立估值，不看当前股价',
            'risk': risk,
            'data': {
                'current_price': current_price,
                '52_week_range': f"${week_52_low:.0f} - ${week_52_high:.0f}",
                'position': round(position, 1)
            }
        }
    
    def _check_narrative(self) -> dict:
        """检查叙事谬误"""
        # 检查增长率与利润率的匹配
        revenue_growth = self.financials.get('revenue_growth_yoy', 0) * 100
        net_margin = self.financials.get('net_income', 0) / self.financials.get('total_revenue', 1) * 100
        
        # 高增长低利润可能是叙事陷阱
        risk = revenue_growth > 30 and net_margin < 10
        
        return {
            'name': '叙事谬误',
            'description': '是否被好故事冲昏头脑？',
            'checklist': [
                '剥离故事后，财务数字还吸引人吗？',
                '管理层故事有数据支撑吗？',
                '叙事是否有可证伪的时间节点？'
            ],
            'action': '写一份"剥离叙事的纯财务分析"',
            'risk': risk,
            'data': {
                'revenue_growth': round(revenue_growth, 1),
                'net_margin': round(net_margin, 1)
            }
        }
    
    def _check_herding(self) -> dict:
        """检查从众心理"""
        strong_buy = self.analyst.get('strong_buy', 0)
        buy = self.analyst.get('buy', 0)
        total = strong_buy + buy + self.analyst.get('hold', 0) + self.analyst.get('sell', 0)
        
        consensus_buy_ratio = (strong_buy + buy) / total * 100 if total > 0 else 0
        
        # 过度一致可能是风险
        risk = consensus_buy_ratio > 90
        
        return {
            'name': '从众心理',
            'description': '是否因为"所有人都在买"就跟着买？',
            'checklist': [
                '看法是基于自己分析还是别人推荐？',
                '如果知名基金经理清仓会改变看法吗？',
                '当前市场共识是什么？'
            ],
            'action': '搜索 [ticker] analyst ratings distribution',
            'risk': risk,
            'data': {
                'consensus_buy_ratio': round(consensus_buy_ratio, 1)
            }
        }
    
    def _check_disposition(self) -> dict:
        """检查处置效应"""
        # 这个检查主要针对已持仓用户
        # 对于新分析，提供一般性检查
        return {
            'name': '处置效应',
            'description': '是否"过早卖出赢家，过晚卖出输家"？',
            'checklist': [
                '如果空仓，会现价买入吗？',
                '持有理由是基于前景还是不甘心？',
                '止损/止盈线是预设的还是调整的？'
            ],
            'action': '假设从零开始评估',
            'risk': False,  # 对新分析不构成风险
            'data': {}
        }
    
    def _check_overconfidence(self) -> dict:
        """检查过度自信"""
        # 检查估值假设的确定性
        # 简化：检查是否使用单一估计而非区间
        return {
            'name': '过度自信',
            'description': '是否高估自己预测能力？',
            'checklist': [
                '估值是否使用区间而非单点？',
                '核心假设有 20% 误差会怎样？',
                '仓位是否过于集中？'
            ],
            'action': '使用情景分析（牛/中/熊）',
            'risk': False,
            'data': {}
        }
    
    def _check_financial_red_flags(self) -> dict:
        """检查 7 大财务红旗"""
        flags = []
        
        # 红旗 1: 收入确认异常
        flag1 = self._check_revenue_recognition()
        if flag1:
            flags.append(flag1)
        
        # 红旗 2: GAAP vs Non-GAAP 差异
        flag2 = self._check_gaap_gap()
        if flag2:
            flags.append(flag2)
        
        # 红旗 3: 应收账款增速异常
        flag3 = self._check_receivables()
        if flag3:
            flags.append(flag3)
        
        # 红旗 4: 内部人交易
        flag4 = self._check_insider_trading()
        if flag4:
            flags.append(flag4)
        
        # 红旗 5: 资本支出异常
        flag5 = self._check_capex()
        if flag5:
            flags.append(flag5)
        
        # 红旗 6: 现金流与利润背离
        flag6 = self._check_cashflow_divergence()
        if flag6:
            flags.append(flag6)
        
        # 红旗 7: 负债结构恶化
        flag7 = self._check_debt_structure()
        if flag7:
            flags.append(flag7)
        
        return {
            'flags': flags,
            'total': len(flags)
        }
    
    def _check_revenue_recognition(self) -> dict:
        """
        检查收入确认异常
        
        红旗信号：
        1. 应收账款增速 >> 收入增速（可能提前确认收入）
        2. 应收账款/收入 > 30%（回款慢，可能渠道压货）
        """
        try:
            # 获取数据
            balance_sheet = self.data.get('balance_sheet', {})
            financials = self.data.get('financials', {})
            
            accounts_receivable = balance_sheet.get('accounts_receivable', 0)
            revenue = financials.get('total_revenue', 1)
            revenue_growth = financials.get('revenue_growth_yoy', 0)
            
            # 计算应收账款/收入比率
            receivables_ratio = (accounts_receivable / revenue * 100) if revenue > 0 else 0
            
            # 计算应收账款增长率（简化：假设去年应收 = 今年应收 / (1 + 收入增长率)）
            # 注意：这是简化估算，精确计算需要历史数据
            if revenue_growth > 0:
                implied_receivables_growth = revenue_growth  # 假设应收与收入同步增长
            else:
                implied_receivables_growth = 0
            
            # 红旗 1: 应收账款/收入 > 30%
            if receivables_ratio > 30:
                severity = '高' if receivables_ratio > 50 else '中'
                return {
                    'name': '收入确认异常',
                    'description': f'应收账款占收入{receivables_ratio:.1f}%（警戒线 30%）',
                    'risk': severity,
                    'data': {
                        'accounts_receivable': accounts_receivable,
                        'revenue': revenue,
                        'receivables_ratio': round(receivables_ratio, 1)
                    },
                    'analysis': f'应收账款占收入{receivables_ratio:.1f}%，{"⚠️ 偏高" if receivables_ratio > 30 else "✅ 合理"}。可能渠道压货或回款放缓。'
                }
            
            # 红旗 2: 应收账款增速 >> 收入增速（需要历史数据，当前简化检查）
            # 如果有历史数据，可以添加：
            # if receivables_growth > revenue_growth * 2:
            #     return {...}
            
            return None  # 未触发红旗
            
        except Exception as e:
            print(f"⚠️ 检查收入确认异常失败：{e}")
            return None
    
    def _check_gaap_gap(self) -> dict:
        """检查 GAAP 与 Non-GAAP 利润差异"""
        try:
            financials = self.data.get('financials', {})
            
            net_income = financials.get('net_income', 0)
            non_gaap_net_income = financials.get('non_gaap_net_income', 0)
            sbc = financials.get('stock_based_compensation', 0)
            revenue = financials.get('total_revenue', 1)
            
            if net_income == 0 or non_gaap_net_income == 0:
                return None
            
            # 计算差异
            gap = non_gaap_net_income - net_income
            gap_percentage = (gap / abs(net_income)) * 100 if net_income != 0 else 0
            sbc_to_revenue_ratio = (sbc / revenue) * 100 if revenue > 0 else 0
            
            # 判断是否构成红旗
            is_red_flag = gap_percentage > 50 or sbc_to_revenue_ratio > 15
            
            if is_red_flag:
                severity = '高' if gap_percentage > 100 else '中'
                return {
                    'name': 'GAAP vs Non-GAAP 差异',
                    'description': f'GAAP 净利润${net_income/1e9:.1f}亿 vs Non-GAAP 净利润${non_gaap_net_income/1e9:.1f}亿，差异{gap_percentage:.1f}%（主要调整项：SBC ${sbc/1e9:.1f}亿）',
                    'risk': severity,
                    'data': {
                        'gaap_net_income': net_income,
                        'non_gaap_net_income': non_gaap_net_income,
                        'gap': gap,
                        'gap_percentage': gap_percentage,
                        'sbc': sbc,
                        'sbc_to_revenue_ratio': sbc_to_revenue_ratio
                    },
                    'analysis': f'差异{gap_percentage:.1f}%，{"⚠️ 偏高" if gap_percentage > 50 else "✅ 合理"}。SBC 占收入{sbc_to_revenue_ratio:.1f}%，{"⚠️ 偏高" if sbc_to_revenue_ratio > 15 else "✅ 合理"}'
                }
            else:
                return None  # 没有触发红旗，返回 None
        except Exception as e:
            return None
    
    def _check_receivables(self) -> dict:
        """检查应收账款"""
        receivables = self.balance_sheet.get('accounts_receivable', 0)
        revenue = self.financials.get('total_revenue', 1)
        
        receivables_ratio = receivables / revenue * 100 if revenue > 0 else 0
        
        if receivables_ratio > 30:
            return {
                'name': '应收账款占比过高',
                'description': f'应收账款占收入{receivables_ratio:.1f}%',
                'risk': '中',
                'data': {
                    'receivables_ratio': round(receivables_ratio, 1)
                }
            }
        return None
    
    def _check_insider_trading(self) -> dict:
        """检查内部人交易（财务红旗）"""
        try:
            insider_data = self.data.get('insider_trades', {})
            if not insider_data:
                return None
            
            summary = insider_data.get('summary', {})
            buy_count = summary.get('buy_count', 0)
            sell_count = summary.get('sell_count', 0)
            net_value = summary.get('net_value', 0)
            sentiment = summary.get('insider_sentiment', 'neutral')
            
            # 判断是否触发红旗
            # 红旗条件：大规模净卖出（卖出 > 买入 * 2，根据公开资料调整）
            if sell_count > 0 and buy_count > 0 and sell_count > buy_count * 2:
                severity = '高' if sell_count > buy_count * 4 else '中'
                ratio = sell_count / buy_count if buy_count > 0 else float('inf')
                return {
                    'name': '内部人交易 - 大规模减持',
                    'description': f'最近内部人交易：买入{buy_count}次 vs 卖出{sell_count}次，净卖出${abs(net_value)/1e6:.1f}M',
                    'risk': severity,
                    'data': {
                        'buy_count': buy_count,
                        'sell_count': sell_count,
                        'net_value': net_value,
                        'sentiment': sentiment,
                        'sell_buy_ratio': round(ratio, 2)
                    },
                    'analysis': f'卖出/买入比率{ratio:.1f}x，{"⚠️ 红旗：内部人大规模减持" if ratio > 2 else "✅ 正常"}'
                }
            
            # 只有卖出没有买入（极端情况）
            elif sell_count > 0 and buy_count == 0:
                return {
                    'name': '内部人交易 - 只有卖出',
                    'description': f'最近内部人交易：0 次买入 vs {sell_count}次卖出，净卖出${abs(net_value)/1e6:.1f}M',
                    'risk': '高',
                    'data': {
                        'buy_count': buy_count,
                        'sell_count': sell_count,
                        'net_value': net_value,
                        'sentiment': sentiment
                    },
                    'analysis': f'⚠️ 红旗：内部人只有卖出没有买入，净卖出${abs(net_value)/1e6:.1f}M'
                }
            
            # 净卖出情绪（低风险提示）
            elif sentiment == 'bearish' and sell_count > buy_count:
                ratio = sell_count / buy_count if buy_count > 0 else float('inf')
                return {
                    'name': '内部人交易 - 净卖出',
                    'description': f'内部人情绪：看空（买入{buy_count}次 vs 卖出{sell_count}次）',
                    'risk': '低',
                    'data': {
                        'buy_count': buy_count,
                        'sell_count': sell_count,
                        'sentiment': sentiment
                    },
                    'analysis': f'内部人情绪看空，卖出/买入比率{ratio:.1f}x，建议关注'
                }
            
            # 没有触发红旗
            return None
            
        except Exception as e:
            print(f"⚠️ 检查内部人交易失败：{e}")
            return None
    
    def _check_capex(self) -> dict:
        """检查资本支出"""
        capex = abs(self.cashflow.get('capital_expenditure', 0))
        revenue = self.financials.get('total_revenue', 1)
        
        capex_ratio = capex / revenue * 100 if revenue > 0 else 0
        
        if capex_ratio > 20:
            return {
                'name': '资本支出占比高',
                'description': f'CapEx 占收入{capex_ratio:.1f}%',
                'risk': '中',
                'data': {
                    'capex_ratio': round(capex_ratio, 1)
                }
            }
        return None
    
    def _check_cashflow_divergence(self) -> dict:
        """检查现金流与利润背离"""
        net_income = self.financials.get('net_income', 0)
        operating_cf = self.cashflow.get('operating_cashflow', 0)
        
        if net_income > 0 and operating_cf < 0:
            return {
                'name': '现金流与利润背离',
                'description': f'净利润${net_income/1e9:.1f}亿，经营现金流${operating_cf/1e9:.1f}亿',
                'risk': '高',
                'data': {
                    'net_income': round(net_income/1e9, 1),
                    'operating_cf': round(operating_cf/1e9, 1),
                    'cash_flow_ratio': round(operating_cf/net_income, 2) if net_income > 0 else 0
                }
            }
        return None
    
    def _check_debt_structure(self) -> dict:
        """检查负债结构"""
        debt_to_equity = self.balance_sheet.get('debt_to_equity', 0)
        current_ratio = self.balance_sheet.get('current_ratio', 0)
        
        if debt_to_equity > 1 or current_ratio < 1:
            return {
                'name': '负债结构风险',
                'description': f'负债率{debt_to_equity:.2f}，流动比率{current_ratio:.2f}',
                'risk': '高' if debt_to_equity > 1.5 or current_ratio < 0.8 else '中',
                'data': {
                    'debt_ratio': round(debt_to_equity, 2),
                    'current_ratio': round(current_ratio, 2)
                }
            }
        return None
    
    def _check_tech_blind_spots(self) -> dict:
        """检查科技股盲区（只包含实际可用的检查）"""
        blind_spots = []
        
        # 1. 股票期权稀释（✅ 已实现）
        spot1 = self._check_stock_dilution()
        if spot1:
            blind_spots.append(spot1)
        
        # 2. AI 收入真实性（✅ 已实现 - 基于公司描述）
        spot2 = self._check_ai_revenue()
        if spot2:
            blind_spots.append(spot2)
        
        # 注意：以下检查需要 SEC 文本挖掘或精确的 CAC 数据
        # 由于数据源不可靠，暂不实现，避免误导用户
        # - TAM 幻觉检查：需要公司声称的 TAM 数据（SEC 10-K 文本挖掘）
        # - CAC 拐点检查：需要新增客户数（SEC 10-K 文本挖掘）
        # - 监管尾部风险：需要法律章节分析（SEC 10-K 文本挖掘）
        
        return {
            'blind_spots': blind_spots,
            'total': len(blind_spots)
        }
    

    def _check_stock_dilution(self) -> dict:
        """分析股票期权稀释情况"""
        try:
            financials = self.data.get('financials', {})
            
            shares_outstanding = financials.get('shares_outstanding', 0)
            dilution_rate = financials.get('shares_dilution_rate', 0)
            sbc = financials.get('stock_based_compensation', 0)
            revenue = financials.get('total_revenue', 1)
            net_income = financials.get('net_income', 1)
            
            # 计算关键指标
            sbc_to_revenue_ratio = (sbc / revenue) * 100 if revenue > 0 else 0
            sbc_to_net_income_ratio = (sbc / abs(net_income)) * 100 if net_income != 0 else 0
            
            # 判断是否构成红旗
            is_red_flag = dilution_rate > 5 or sbc_to_revenue_ratio > 15
            
            if is_red_flag:
                severity = '高' if dilution_rate > 10 or sbc_to_revenue_ratio > 25 else '中'
            else:
                severity = None
            
            # 只有在检测到风险时才返回
            if severity:
                return {
                    'name': '股票期权稀释',
                    'description': f'年股权稀释率{dilution_rate:.1f}%，SBC 占收入{sbc_to_revenue_ratio:.1f}%，SBC 占净利润{sbc_to_net_income_ratio:.1f}%',
                    'risk': severity,
                    'data': {
                        'shares_outstanding': shares_outstanding,
                        'dilution_rate': dilution_rate,
                        'sbc': sbc,
                        'sbc_to_revenue_ratio': sbc_to_revenue_ratio,
                        'sbc_to_net_income_ratio': sbc_to_net_income_ratio
                    },
                    'analysis': f'稀释率{dilution_rate:.1f}%，{"⚠️ 偏高" if dilution_rate > 5 else "✅ 合理"}。SBC 占收入{sbc_to_revenue_ratio:.1f}%，{"⚠️ 偏高" if sbc_to_revenue_ratio > 15 else "✅ 合理"}'
                }
            else:
                return None
        except Exception as e:
            return None

    def _check_ai_revenue(self) -> dict:
        """检查 AI 收入真实性（基于公司描述）"""
        # 从公司描述中检查是否涉及 AI
        description = self.data.get('company_info', {}).get('description', '')
        if not description:
            return None
        
        description_lower = description.lower()
        
        if 'ai' in description_lower or 'artificial intelligence' in description_lower:
            return {
                'name': 'AI 收入真实性',
                'description': '公司涉及 AI 业务，需核实 AI 收入定义和可持续性',
                'checklist': [
                    'AI 收入的具体定义是什么？',
                    '是经常性收入还是一次性？',
                    '客户是试用还是大规模部署？'
                ],
                'risk': '中'
            }
        return None
    
    def _pre_mortem(self) -> dict:
        """Pre-Mortem 事前尸检"""
        return {
            'exercise': '假设 1 年后投资失败，原因可能是：',
            'questions': [
                '核心假设中哪个错了？',
                '是否忽略了某个重大风险？',
                '竞争格局是否发生了意外变化？',
                '管理层是否做出了错误决策？',
                '宏观环境是否恶化？'
            ],
            'action': '写下 3 个最可能的失败原因，并制定监控指标'
        }


def check_biases(data: dict) -> dict:
    """便捷函数：执行反偏见检查"""
    framework = BiasFramework(data)
    return framework.check_all()


if __name__ == '__main__':
    sys.path.insert(0, 'modules')
    from fetch_data import StockDataFetcher
    
    if len(sys.argv) < 2:
        print("用法：python bias_framework.py <股票代码>")
        sys.exit(1)
    
    ticker = sys.argv[1]
    
    # 获取数据
    fetcher = StockDataFetcher(ticker)
    data = fetcher.get_all_data(use_cache=True)
    
    # 执行反偏见检查
    result = check_biases(data)
    
    print("\n" + "=" * 60)
    print(f"{ticker} 反偏见检查")
    print("=" * 60)
    
    # 认知偏见
    print("\n🧠 认知偏见检查:")
    for name, bias in result['cognitive_biases'].items():
        risk_marker = "⚠️" if bias.get('risk', False) else "✅"
        print(f"   {risk_marker} {bias['name']}: {bias['description']}")
    
    # 财务红旗
    print("\n🚩 财务红旗:")
    if result['financial_red_flags']['flags']:
        for flag in result['financial_red_flags']['flags']:
            print(f"   ⚠️ {flag['name']}: {flag['description']} (风险：{flag['risk']})")
    else:
        print("   ✅ 未发现明显财务红旗")
    
    # 科技盲区
    print("\n🔍 科技盲区:")
    if result['tech_blind_spots']['blind_spots']:
        for spot in result['tech_blind_spots']['blind_spots']:
            print(f"   ⚠️ {spot['name']}: {spot['description']}")
    else:
        print("   ✅ 未发现明显科技盲区")
    
    # Pre-Mortem
    print("\n💀 Pre-Mortem:")
    print(f"   {result['pre_mortem']['exercise']}")
    for i, q in enumerate(result['pre_mortem']['questions'], 1):
        print(f"   {i}. {q}")
    
    # 总结
    print("\n" + "=" * 60)
    print(f"风险等级：{result['summary']['risk_level']}")
    print(f"财务红旗：{result['summary']['total_red_flags']}个")
    print(f"偏见警告：{result['summary']['bias_warnings']}个")
    print("=" * 60)
