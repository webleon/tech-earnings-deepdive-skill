#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自定义异常类
"""


class TechEarningsError(Exception):
    """基础异常类"""
    pass


class DataFetchError(TechEarningsError):
    """数据获取失败"""
    def __init__(self, ticker: str, source: str, message: str):
        self.ticker = ticker
        self.source = source
        self.message = message
        super().__init__(f"{ticker} 数据获取失败 ({source}): {message}")


class InsufficientDataError(TechEarningsError):
    """数据不足"""
    def __init__(self, ticker: str, missing_data: str):
        self.ticker = ticker
        self.missing_data = missing_data
        super().__init__(f"{ticker} 数据不足：缺少 {missing_data}")


class AnalysisError(TechEarningsError):
    """分析失败"""
    def __init__(self, ticker: str, module: str, message: str):
        self.ticker = ticker
        self.module = module
        self.message = message
        super().__init__(f"{ticker} 分析失败 ({module}): {message}")


class ExportError(TechEarningsError):
    """导出失败"""
    def __init__(self, ticker: str, message: str):
        self.ticker = ticker
        self.message = message
        super().__init__(f"{ticker} 导出失败：{message}")
