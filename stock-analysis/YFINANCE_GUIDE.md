# yfinance 港股数据获取指南

## 概述

本项目现已集成 yfinance 库来获取港股数据，作为 akshare 和 tushare 的补充数据源。yfinance 提供稳定的港股历史数据获取能力。

## 安装

yfinance 已自动包含在 `requirements.txt` 中，可以通过以下命令安装：

```bash
pip install yfinance>=0.2.0
```

或安装全部依赖：

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本用法

```python
import yfinance as yf
import pandas as pd

# 获取腾讯 (0700.HK) 数据
stock = yf.Ticker("0700.HK")

# 获取最近 5 天的数据
df = stock.history(period="5d")

print(df)
print(df.tail())
```

### 支持的时间周期

yfinance 支持以下时间周期参数：

| 周期 | 说明 | 示例 |
|------|------|------|
| `1d` | 最近 1 天 | `period="1d"` |
| `5d` | 最近 5 天 | `period="5d"` |
| `1mo` | 最近 1 个月 | `period="1mo"` |
| `3mo` | 最近 3 个月 | `period="3mo"` |
| `6mo` | 最近 6 个月 | `period="6mo"` |
| `1y` | 最近 1 年 | `period="1y"` |
| `2y` | 最近 2 年 | `period="2y"` |
| `5y` | 最近 5 年 | `period="5y"` |
| `10y` | 最近 10 年 | `period="10y"` |
| `ytd` | 今年至今 | `period="ytd"` |
| `max` | 全部历史数据 | `period="max"` |

### 常见港股代码

| 公司 | 代码 |
|------|------|
| 腾讯 | 0700.HK |
| 长和 | 0001.HK |
| 吉利汽车 | 0175.HK |
| 京东 | 09618.HK |
| 小米 | 01810.HK |
| 网易 | 09999.HK |
| 阿里巴巴 | 09988.HK |
| 百度 | 09888.HK |

### 实现代码

在 `analyze_stock.py` 中的 yfinance 集成代码：

```python
# 方案4：使用 yfinance（备选方案）
if df is None or df.empty:
    try:
        print(f"  Trying method 4: yfinance...", file=sys.stderr)
        try:
            import yfinance as yf
        except ImportError:
            raise ImportError("yfinance not installed")
        
        # yfinance 使用 HK 前缀
        ticker_str = f"{hk_code}.HK" if not hk_code.endswith(".HK") else hk_code
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
```

## 数据获取优先级

系统会按以下顺序尝试获取港股数据：

1. **tushare** - 如果配置了有效的 Token
2. **akshare stock_hk_hist** - 第一个 akshare 方法
3. **akshare stock_hk_daily** - 第二个 akshare 方法
4. **akshare stock_hk_hist with date range** - 第三个 akshare 方法
5. **yfinance** - 最后的备选方案（本项目新增）

## 测试

运行测试脚本验证 yfinance 功能：

```bash
python3 scripts/test_yfinance_hk.py
```

测试脚本包括：
- 基本数据获取测试
- 自定义日期范围测试
- 数据标准化测试

## 优点

- ✅ 稳定可靠的数据来源
- ✅ 无需 API Token
- ✅ 支持长期历史数据
- ✅ 自动处理时区信息
- ✅ 完整的 OHLCV（开高低收成交量）数据

## 限制

- ⚠️ 数据延迟约 15-20 分钟（Yahoo Finance 的限制）
- ⚠️ 无实时行情数据
- ⚠️ 无法获取分钟级数据

## 错误处理

```python
import yfinance as yf

try:
    stock = yf.Ticker("0700.HK")
    df = stock.history(period="1mo")
    
    if df is None or df.empty:
        print("未获取到数据")
    else:
        print(f"成功获取 {len(df)} 条数据")
        
except Exception as e:
    print(f"错误: {e}")
```

## 常见问题

### Q: yfinance 和其他数据源的区别？

A: 
- **yfinance**: 适合长期历史数据分析，无需认证，稳定可靠
- **akshare**: 中文数据源，支持更多国内股票
- **tushare**: 专业数据服务，支持实时和特殊数据

### Q: 可以获取实时数据吗？

A: yfinance 不支持完全实时数据，但数据延迟不超过 20 分钟。如需实时数据，建议使用 tushare。

### Q: 如何获取更多历史数据？

A: 使用 `period="max"` 获取全部可用历史数据：

```python
stock = yf.Ticker("0700.HK")
df = stock.history(period="max")  # 获取全部历史数据
```

### Q: 如何自定义日期范围？

A: 使用 `start` 和 `end` 参数：

```python
import yfinance as yf
from datetime import datetime

stock = yf.Ticker("0700.HK")
df = stock.history(start="2020-01-01", end="2024-12-31")
```

## 参考资源

- [yfinance 官方文档](https://github.com/ranaroussi/yfinance)
- [YahooFinance 数据](https://finance.yahoo.com/)
- [港股代码查询](https://www.hkex.com.hk/)

## 版本信息

- yfinance>=0.2.0

---

**最后更新**: 2026年3月6日