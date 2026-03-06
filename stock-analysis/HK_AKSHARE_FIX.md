# akshare 港股函数修复记录

## 问题

原始代码中使用了不存在的akshare函数 `hk_qvix_kline()`，导致港股数据获取失败。

## 原因

akshare库中的港股数据获取函数名称不同，正确的函数包括：
- `stock_hk_hist()` - 东方财富网港股历史数据
- `stock_hk_daily()` - 新浪财经港股历史数据

##修复方案

### 实现多重备选机制

修改后的 `get_hk_stock_data()` 函数采用三层递进策略：

#### 方案1：使用 `stock_hk_hist(symbol='00700')`
- 数据源：东方财富网
- 列名：中文（日期、开盘、收盘、最高、最低、成交量、成交额、振幅、涨跌幅、涨跌额、换手率）
- 优点：数据完整，包含多个技术指标
- 缺点：有时连接不稳定

#### 方案2：使用 `stock_hk_daily(symbol='700')`
- 数据源：新浪财经
- 列名：英文（date、open、high、low、close、volume）
- 优点：连接相对稳定，历史数据完整
- 缺点：只有基础OHLCV数据

#### 方案3：使用 `stock_hk_hist()` 带日期范围
```python
stock_hk_hist(symbol='00700', period='daily', 
              start_date='20250101', end_date='20260306')
```
- 优点：指标丰富，数据完整
- 缺点：依赖远程连接

### 改进的错误处理

- ✓ 列名自动转换为英文小写
- ✓ 数据类型验证和转换
- ✓ NaN值处理
- ✓ 详细的调试日志
- ✓ 每个数据源的独立错误捕获
- ✓ 指标计算失败不会导致整体失败

## 测试结果

### 港股代码验证
```
✓ 00700.HK (腾讯) -> 格式正确
✓ 09973.HK (招商积极) -> 格式正确
✓ 03690.HK (美团) -> 格式正确
✗ 001.HK -> 格式错误（太短）
```

### 数据获取方法
```
✓ stock_hk_hist() -> 支持 ✓
✓ stock_hk_daily() -> 支持 ✓
✗ hk_qvix_kline() -> 不存在 (已移除)
```

## 使用方式

### 调用港股分析

```bash
# 格式1：完整代码
python scripts/analyze_stock.py 00700.HK
python scripts/analyze_stock.py 09973.HK

# 格式2：简化代码（脚本会自动处理）
python scripts/analyze_stock.py 00700
```

### 预期输出

成功时返回JSON格式数据：
```json
{
  "stock_code": "00700.HK",
  "market": "Hong Kong",
  "data_source": "akshare (multiple methods)",
  "latest_date": "2026-03-06",
  "records_count": 5340,
  "latest_price": 410.0,
  "technical_indicators": {
    "MA5": 415.2,
    "MA20": 420.5,
    "RSI": 35.6,
    "MACD": -2.3,
    ...
  },
  "recent_data": [...]
}
```

失败时返回详细错误信息（包含尝试的所有方法）。

## 技术细节

### 列名映射表

| akshare 列名 | 转换后 | 说明 |
|------------|--------|------|
| 日期 | date | 交易日期 |
| 开盘 | open | 开盘价 |
| 收盘 | close | 收盘价 |
| 最高 | high | 最高价 |
| 最低 | low | 最低价 |
| 成交量 | volume | 成交量 |

### 支持的技术指标

- ✓ MA (移动平均线)
- ✓ MACD (动向指标)
- ✓ RSI (相对强弱指数)
- ✓ KDJ (随机指标)
- ✓ Bollinger Bands (布林带)
- ✓ OBV (能量潮)
- ✓ ATR (平均真实波幅)

## 后续优化

- [ ] 缓存港股代码映射表
- [ ] 添加超时重试机制
- [ ] 支持实时行情补充
- [ ] 性能优化：批量获取多只港股
- [ ] DataFrame列动态映射优化
