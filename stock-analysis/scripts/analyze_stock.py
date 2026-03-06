#!/usr/bin/env python3
"""
Stock Technical Analysis Script

Generates comprehensive technical indicator reports for Chinese stocks and Hong Kong stocks

This script outputs raw technical indicator data that can be analyzed by LLM.

Supported Stock Codes:
- A-shares (Shanghai/Shenzhen): 6-digit codes, e.g., 000001, 600036
- Hong Kong stocks: 5-digit codes with .HK suffix, e.g., 00700.HK, 03690.HK (uses akshare)
"""

import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime


def try_install_dependencies():
    """
    Attempt to install missing dependencies automatically.
    Tries multiple methods to handle various environment restrictions.
    """
    requirements_file = Path(__file__).parent.parent / "requirements.txt"
    
    if not requirements_file.exists():
        return False
    
    install_methods = [
        # Method 1: Try with --break-system-packages (for newer pip versions on macOS)
        [sys.executable, "-m", "pip", "install", "--break-system-packages", "-q", "-r", str(requirements_file)],
        # Method 2: Try with --user flag (for user-level install)
        [sys.executable, "-m", "pip", "install", "--user", "-q", "-r", str(requirements_file)],
        # Method 3: Standard pip install
        [sys.executable, "-m", "pip", "install", "-q", "-r", str(requirements_file)],
    ]
    
    for i, cmd in enumerate(install_methods, 1):
        try:
            print(f"Attempting to install dependencies (method {i})...", file=sys.stderr)
            result = subprocess.run(cmd, capture_output=True, timeout=120)
            if result.returncode == 0:
                print("Dependencies installed successfully.", file=sys.stderr)
                return True
        except subprocess.TimeoutExpired:
            continue
        except Exception:
            continue
    
    return False


def ensure_dependencies():
    """
    Ensure all required packages are available.
    Returns True if successful, False otherwise.
    """
    required_packages = {
        "AIShareTxt": "aishare-txt",
        "talib": "TA-Lib",
        "pandas": "pandas",
        "numpy": "numpy",
        "akshare": "akshare",
    }
    
    # Check if all packages are installed
    all_installed = True
    for import_name, package_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            all_installed = False
            break
    
    if all_installed:
        return True
    
    # Try to install missing dependencies
    print("Some dependencies are missing. Attempting automatic installation...", file=sys.stderr)
    if try_install_dependencies():
        return True
    
    return False


def get_hk_stock_data(stock_code):
    """
    获取港股数据，使用akshare库的多个备选方案和yfinance作为备选数据源
    
    Args:
        stock_code: 港股代码，如 00700.HK 或 3690
    
    Returns:
        技术指标数据的JSON字符串或错误信息
    """

    try:
        import akshare as ak
        import pandas as pd
        import talib
        import numpy as np
    except ImportError as e:
        return json.dumps({
            "error": f"Failed to import required packages for HK stocks: {str(e)}",
            "message": "Please ensure akshare, pandas, and TA-Lib are installed"
        }, ensure_ascii=False, indent=2)
    
    try:
        # 移除 .HK 后缀获取数据
        hk_code_full = stock_code.replace(".HK", "")  # 保留完整代码（包括前导零）
        hk_code = hk_code_full.lstrip("0")  # 移除前导零用于其他接口
        print(f"Fetching HK stock data for {stock_code} (code: {hk_code})...", file=sys.stderr)
        
        df = None
        error_messages = []

        # helper for retrying network calls
        import time
        def attempt(func, *args, tries=3, delay=1, description=None, **kwargs):
            for attempt_idx in range(1, tries + 1):
                try:
                    if description:
                        print(f"    attempt {attempt_idx}/{tries} for {description}", file=sys.stderr)
                    return func(*args, **kwargs)
                except Exception as exc:
                    print(f"      error on attempt {attempt_idx}: {exc}", file=sys.stderr)
                    if attempt_idx < tries:
                        time.sleep(delay)
                    last_exc = exc
            raise last_exc
        
        # 方案1：使用 stock_hk_hist
        try:
            print(f"  Trying method 1: stock_hk_hist...", file=sys.stderr)
            df = attempt(ak.stock_hk_hist, symbol=hk_code,
                         description="stock_hk_hist")
            if df is not None and not df.empty:
                print(f"  ✓ Method 1 succeeded", file=sys.stderr)
                # 转换列名
                df_renamed = pd.DataFrame({
                    'date': pd.to_datetime(df['日期']).dt.date,
                    'open': pd.to_numeric(df['开盘'], errors='coerce'),
                    'close': pd.to_numeric(df['收盘'], errors='coerce'),
                    'high': pd.to_numeric(df['最高'], errors='coerce'),
                    'low': pd.to_numeric(df['最低'], errors='coerce'),
                    'volume': pd.to_numeric(df['成交量'], errors='coerce')
                })
                df = df_renamed
        except Exception as e1:
            error_messages.append(f"Method 1 failed: {str(e1)[:200]}")
        
        # 方案2：使用 stock_hk_daily
        if df is None or df.empty:
            try:
                print(f"  Trying method 2: stock_hk_daily...", file=sys.stderr)
                df = attempt(ak.stock_hk_daily, symbol=hk_code,
                             description="stock_hk_daily")
                if df is not None and not df.empty:
                    print(f"  ✓ Method 2 succeeded", file=sys.stderr)
                    # 确保列名为标准格式
                    df.columns = [col.lower() for col in df.columns]
            except Exception as e2:
                error_messages.append(f"Method 2 failed: {str(e2)[:200]}")
        
        # 方案3：使用 stock_hk_hist 带日期范围
        if df is None or df.empty:
            try:
                from datetime import datetime, timedelta
                print(f"  Trying method 3: stock_hk_hist with date range...", file=sys.stderr)
                end_date = datetime.now().strftime('%Y%m%d')
                start_date = (datetime.now() - timedelta(days=500)).strftime('%Y%m%d')
                df = attempt(ak.stock_hk_hist, symbol=hk_code, period='daily',
                             start_date=start_date, end_date=end_date,
                             description="stock_hk_hist(range)")
                if df is not None and not df.empty:
                    print(f"  ✓ Method 3 succeeded", file=sys.stderr)
                    # 转换列名
                    df_renamed = pd.DataFrame({
                        'date': pd.to_datetime(df['日期']).dt.date if '日期' in df.columns else df.index,
                        'open': pd.to_numeric(df['开盘'], errors='coerce') if '开盘' in df.columns else None,
                        'close': pd.to_numeric(df['收盘'], errors='coerce') if '收盘' in df.columns else None,
                        'high': pd.to_numeric(df['最高'], errors='coerce') if '最高' in df.columns else None,
                        'low': pd.to_numeric(df['最低'], errors='coerce') if '最低' in df.columns else None,
                        'volume': pd.to_numeric(df['成交量'], errors='coerce') if '成交量' in df.columns else None,
                    })
                    df = df_renamed
            except Exception as e3:
                error_messages.append(f"Method 3 failed: {str(e3)[:200]}")
        
        # 方案4：使用 yfinance（备选方案）
        if df is None or df.empty:
            try:
                print(f"  Trying method 4: yfinance...", file=sys.stderr)
                try:
                    import yfinance as yf
                except ImportError:
                    raise ImportError("yfinance not installed")
                
                # yfinance 使用完整的港股代码（包括前导零）+ .HK 后缀
                ticker_str = f"{hk_code_full}.HK"
                stock = yf.Ticker(ticker_str)
                yf_df = stock.history(period="1y")  # 获取一年的历史数据
                
                if yf_df is not None and not yf_df.empty:
                    print(f"  ✓ Method 4 succeeded", file=sys.stderr)
                    # 标准化列名
                    yf_df_renamed = pd.DataFrame({
                        'date': yf_df.index.strftime('%Y-%m-%d'),
                        'open': yf_df['Open'],
                        'close': yf_df['Close'],
                        'high': yf_df['High'],
                        'low': yf_df['Low'],
                        'volume': yf_df['Volume']
                    })
                    yf_df_renamed['date'] = pd.to_datetime(yf_df_renamed['date']).dt.date.astype(str)
                    df = yf_df_renamed
            except Exception as e4:
                error_messages.append(f"Method 4 (yfinance) failed: {str(e4)[:200]}")
        
        
        if df is None or df.empty:
            error_msg = "\n".join(error_messages) if error_messages else "No specific error"
            return json.dumps({
                "error": f"Failed to fetch Hong Kong stock {stock_code} data from all available methods",
                "code": hk_code,
                "methods_tried": ["stock_hk_hist", "stock_hk_daily", "stock_hk_hist with date range"],
                "details": error_msg,
                "message": "Please try again or verify the stock code"
            }, ensure_ascii=False, indent=2)
        
        # 确保列名为小写且一致
        df.columns = [col.lower() for col in df.columns]
        df = df.sort_values('date', ascending=False).reset_index(drop=True)
        
        # 确保数据类型正确
        for col in ['close', 'open', 'high', 'low', 'volume']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # 转换date为字符串
        if 'date' in df.columns:
            df['date'] = df['date'].astype(str)
        
        # 移除包含NaN的行
        df = df.dropna(subset=['close'])
        
        if df.empty:
            return json.dumps({
                "error": f"No valid data for Hong Kong stock {stock_code}",
                "message": "After data filtering"
            }, ensure_ascii=False, indent=2)
        
        print(f"  Total records: {len(df)}", file=sys.stderr)
        
        # 计算技术指标
        close = df['close'].values
        if len(close) > 0:
            high = df['high'].values if 'high' in df.columns else close
            low = df['low'].values if 'low' in df.columns else close
            volume = df['volume'].values if 'volume' in df.columns else np.ones(len(close))
        
        indicators = {
            "stock_code": stock_code,
            "market": "Hong Kong",
            "data_source": "akshare (multiple methods)",
            "latest_date": str(df.iloc[0]['date']) if len(df) > 0 else None,
            "records_count": len(df),
            "latest_price": float(df.iloc[0]['close']) if len(df) > 0 else None,
            "price_change_1d": float(df.iloc[0]['close'] - df.iloc[1]['close']) if len(df) > 1 else None,
            "price_change_ytd": float(df.iloc[0]['close'] - df.iloc[-1]['close']) if len(df) > 0 else None,
            "technical_indicators": {}
        }
        
        # 计算MA指标
        try:
            if len(close) >= 60:
                indicators["technical_indicators"]["MA5"] = float(talib.SMA(close, timeperiod=5)[-1])
                indicators["technical_indicators"]["MA10"] = float(talib.SMA(close, timeperiod=10)[-1])
                indicators["technical_indicators"]["MA20"] = float(talib.SMA(close, timeperiod=20)[-1])
                indicators["technical_indicators"]["MA60"] = float(talib.SMA(close, timeperiod=60)[-1])
        except Exception as e:
            print(f"Warning: Failed to calculate MA: {e}", file=sys.stderr)
        
        # 计算MACD
        try:
            if len(close) >= 26:
                macd, macdsignal, macdhist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
                indicators["technical_indicators"]["MACD"] = float(macd[-1])
                indicators["technical_indicators"]["MACD_SIGNAL"] = float(macdsignal[-1])
                indicators["technical_indicators"]["MACD_HIST"] = float(macdhist[-1])
        except Exception as e:
            print(f"Warning: Failed to calculate MACD: {e}", file=sys.stderr)
        
        # 计算RSI
        try:
            if len(close) >= 14:
                rsi = talib.RSI(close, timeperiod=14)
                indicators["technical_indicators"]["RSI"] = float(rsi[-1])
        except Exception as e:
            print(f"Warning: Failed to calculate RSI: {e}", file=sys.stderr)
        
        # 计算KDJ
        try:
            if len(close) >= 9:
                fastk, fastd = talib.STOCH(high, low, close, fastk_period=9, slowk_period=3, slowd_period=3)
                indicators["technical_indicators"]["K"] = float(fastk[-1])
                indicators["technical_indicators"]["D"] = float(fastd[-1])
        except Exception as e:
            print(f"Warning: Failed to calculate KDJ: {e}", file=sys.stderr)
        
        # 计算Bollinger Bands
        try:
            if len(close) >= 20:
                upperband, middleband, lowerband = talib.BBANDS(close, timeperiod=20)
                indicators["technical_indicators"]["BB_UPPER"] = float(upperband[-1])
                indicators["technical_indicators"]["BB_MIDDLE"] = float(middleband[-1])
                indicators["technical_indicators"]["BB_LOWER"] = float(lowerband[-1])
        except Exception as e:
            print(f"Warning: Failed to calculate Bollinger Bands: {e}", file=sys.stderr)
        
        # 计算成交量指标
        try:
            if len(close) >= 14 and volume is not None:
                obv = talib.OBV(close, volume)
                indicators["technical_indicators"]["OBV"] = float(obv[-1])
        except Exception as e:
            print(f"Warning: Failed to calculate OBV: {e}", file=sys.stderr)
        
        # 计算ATR
        try:
            if len(close) >= 14:
                atr = talib.ATR(high, low, close, timeperiod=14)
                indicators["technical_indicators"]["ATR"] = float(atr[-1])
        except Exception as e:
            print(f"Warning: Failed to calculate ATR: {e}", file=sys.stderr)
        
        # 添加原始数据的最后20条记录
        recent_data = df.head(20).copy()
        indicators["recent_data"] = recent_data.to_dict('records')
        
        print(f"✓ Successfully analyzed {stock_code}", file=sys.stderr)
        return json.dumps(indicators, ensure_ascii=False, indent=2, default=str)
        
    except Exception as e:
        import traceback
        return json.dumps({
            "error": f"Failed to fetch or analyze HK stock {stock_code}",
            "message": str(e),
            "type": type(e).__name__,
            "traceback": traceback.format_exc()[:300]
        }, ensure_ascii=False, indent=2)



def get_ashare_stock_data(stock_code):
    """
    获取A股数据，使用AIShareTxt库
    
    Args:
        stock_code: A股代码，6位数字
    
    Returns:
        技术指标数据的JSON字符串或错误信息
    """
    try:
        from AIShareTxt import StockDataProcessor
    except ImportError as e:
        return json.dumps({
            "error": f"Failed to import AIShareTxt: {str(e)}",
            "troubleshooting": [
                "1. Run: pip install --break-system-packages aishare-txt",
                "2. Or: pip install --user -r requirements.txt"
            ]
        }, ensure_ascii=False, indent=2)

    # Create processor and generate report
    processor = StockDataProcessor()

    try:
        # Get technical report from AIShareTxt
        report = processor.generate_stock_report(stock_code)

        return json.dumps({
            "stock_code": stock_code,
            "market": "A-share",
            "market_type": "A-share",
            "report": report,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({
            "error": f"Failed to analyze A-share stock {stock_code}",
            "message": str(e)
        }, ensure_ascii=False, indent=2)


def analyze_stock(stock_input):
    """
    Analyze a stock by code and return raw technical data.
    Automatically routes to appropriate analyzer based on stock code format.

    Args:
        stock_input: Stock code (6 digits for A-share or 5 digits with .HK for HK stock)

    Returns:
        JSON string containing the technical data or error message
    """
    # Ensure dependencies are available
    if not ensure_dependencies():
        return json.dumps({
            "error": "Failed to ensure dependencies are installed.",
            "troubleshooting": [
                "1. Please ensure Python 3.10+ is installed",
                "2. Install TA-Lib system dependency (see: https://ta-lib.org/install/)",
                "3. Try manual installation: pip install --break-system-packages -r requirements.txt",
                "4. If using macOS system Python and you see PEP 668 errors, create a virtualenv or use pipx for package isolation"
            ]
        }, ensure_ascii=False, indent=2)

    # Validate stock code format and route to appropriate analyzer
    stock_code = stock_input.strip().upper()
    is_valid = False
    market_type = ""
    
    if stock_code.endswith(".HK"):
        # Hong Kong stock format: 5 digits + .HK
        code_part = stock_code[:-3]
        if code_part.isdigit() and len(code_part) == 5:
            is_valid = True
            market_type = "HK"
    elif stock_code.isdigit() and len(stock_code) == 6:
        # A-share format: 6 digits
        is_valid = True
        market_type = "A-share"
    
    if not is_valid:
        return json.dumps({
            "error": f"Invalid stock code format: '{stock_code}'.",
            "valid_formats": {
                "A-shares": "6-digit codes, e.g., 000001, 600036",
                "Hong Kong stocks": "5-digit codes with .HK suffix, e.g., 00700.HK, 03690.HK"
            },
            "examples": {
                "A-shares": "000001 (Ping An Bank), 600036 (China Merchants Bank)",
                "Hong Kong": "00700.HK (Tencent), 03690.HK (Meituan Dianping)"
            }
        }, ensure_ascii=False, indent=2)

    # Route to appropriate analyzer
    if market_type == "HK":
        return get_hk_stock_data(stock_code)
    else:  # A-share
        return get_ashare_stock_data(stock_code)


def main():
    """Command line interface"""
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Usage: python analyze_stock.py <stock_code> [--output-dir <path>]",
            "examples": {
                "A-share": "python analyze_stock.py 000001",
                "Hong Kong stock": "python analyze_stock.py 00700.HK"
            }
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    stock_input = sys.argv[1]

    # Parse optional output directory argument
    # Default to user's current working directory from environment or use skill directory
    import os
    output_dir_str = os.environ.get("USER_WORKING_DIR", "")
    output_dir = Path(output_dir_str) if output_dir_str else Path.cwd()

    # Allow override via --output-dir argument
    if len(sys.argv) >= 4 and sys.argv[2] == "--output-dir":
        output_dir = Path(sys.argv[3])

    result_json = analyze_stock(stock_input)
    result = json.loads(result_json)

    # Print report to console
    if "report" in result:
        print(result["report"])

        # Save report to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"stock_report_{stock_input}_{timestamp}.txt"
        report_path = output_dir / report_filename

        with open(report_path, "w", encoding="utf-8") as f:
            f.write(result["report"])

        # Also save JSON
        json_filename = f"stock_data_{stock_input}_{timestamp}.json"
        json_path = output_dir / json_filename

        with open(json_path, "w", encoding="utf-8") as f:
            f.write(result_json)

        print(f"\n报告已保存: {report_path}", file=sys.stderr)
        print(f"数据已保存: {json_path}", file=sys.stderr)
    else:
        print(result_json)


if __name__ == "__main__":
    main()
