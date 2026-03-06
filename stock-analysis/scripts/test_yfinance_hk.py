#!/usr/bin/env python3
"""
yfinance 港股数据获取测试脚本

测试使用 yfinance 库获取港股数据的功能
"""

import yfinance as yf
import pandas as pd
from datetime import datetime

def test_yfinance_hk_basic():
    """测试基本的港股数据获取"""
    print("=== yfinance 港股数据测试 ===\n")
    
    # 测试股票列表（代码：市场名称）
    test_stocks = {
        "0700.HK": "腾讯",
        "0001.HK": "长和",
        "0175.HK": "吉利汽车",
    }
    
    for ticker, name in test_stocks.items():
        print(f"获取 {name} ({ticker}) 数据...")
        try:
            stock = yf.Ticker(ticker)
            
            # 获取最近 5 天数据
            df = stock.history(period="5d")
            
            if df is not None and not df.empty:
                print(f"  ✓ 成功获取 {len(df)} 条数据")
                print(f"    最新数据:")
                print(f"      日期: {df.index[-1].date()}")
                print(f"      开盘: {df['Open'].iloc[-1]:.2f}")
                print(f"      收盘: {df['Close'].iloc[-1]:.2f}")
                print(f"      最高: {df['High'].iloc[-1]:.2f}")
                print(f"      最低: {df['Low'].iloc[-1]:.2f}")
                print(f"      成交量: {int(df['Volume'].iloc[-1]):,}")
            else:
                print(f"  ✗ 未获取到数据")
        except Exception as e:
            print(f"  ✗ 错误: {e}")
        
        print()

def test_date_range():
    """测试指定日期范围获取数据"""
    print("=== 自定义日期范围测试 ===\n")
    
    ticker = "0700.HK"
    print(f"获取腾讯 ({ticker}) 最近 3 个月数据...")
    
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period="3mo")
        
        if df is not None and not df.empty:
            print(f"  ✓ 成功获取 {len(df)} 个交易日")
            print(f"    时间跨度: {df.index[0].date()} 至 {df.index[-1].date()}")
            print(f"    价格范围: {df['Open'].min():.2f} - {df['High'].max():.2f}")
        else:
            print(f"  ✗ 未获取到数据")
    except Exception as e:
        print(f"  ✗ 错误: {e}")

def test_data_normalization():
    """测试数据标准化"""
    print("\n=== 数据标准化测试 ===\n")
    
    ticker = "0700.HK"
    print(f"获取腾讯 ({ticker}) 数据并标准化...")
    
    try:
        stock = yf.Ticker(ticker)
        yf_df = stock.history(period="1mo")  # 改为支持的期限
        
        if yf_df is not None and not yf_df.empty:
            # 标准化处理
            normalized_df = pd.DataFrame({
                'date': yf_df.index.strftime('%Y-%m-%d'),
                'open': yf_df['Open'],
                'close': yf_df['Close'],
                'high': yf_df['High'],
                'low': yf_df['Low'],
                'volume': yf_df['Volume']
            })
            normalized_df['date'] = pd.to_datetime(normalized_df['date']).dt.date.astype(str)
            
            print(f"  ✓ 数据标准化成功")
            print(f"    列: {list(normalized_df.columns)}")
            print(f"    行数: {len(normalized_df)}")
            print(f"\n  样本数据：")
            print(normalized_df.head(3).to_string(index=False))
        else:
            print(f"  ✗ 未获取到数据")
    except Exception as e:
        print(f"  ✗ 错误: {e}")

def main():
    """主测试函数"""
    print("yfinance 港股数据测试\n")
    print("=" * 50)
    
    # 验证库是否已安装
    try:
        import yfinance as yf
        print(f"✓ yfinance 版本: {yf.__version__}\n")
    except ImportError as e:
        print(f"✗ yfinance 未安装: {e}")
        return
    
    # 运行各项测试
    test_yfinance_hk_basic()
    test_date_range()
    test_data_normalization()
    
    print("\n" + "=" * 50)
    print("✓ 所有测试完成")
    print("\n提示: yfinance 可用于获取港股数据")

if __name__ == "__main__":
    main()
