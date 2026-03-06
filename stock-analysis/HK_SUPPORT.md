# Stock Analysis Skill - 港股支持优化记录

## 优化内容

### 问题描述
AIShareTxt 库只支持 A股（6位数字代码），不支持港股（5位数字+.HK格式），导致港股分析请求失败。

### 解决方案

#### 1. **双数据源架构**
- **A股**：继续使用 AIShareTxt 库（专业财务数据源）
- **港股**：使用 akshare 库（实时港股数据获取）
- 自动根据股票代码格式路由到不同的数据源

#### 2. **智能路由逻辑**
```python
# 港股代码格式：5位数字+.HK
00700.HK -> 路由到 get_hk_stock_data()
# A股代码格式：6位数字
000001 -> 路由到 get_ashare_stock_data()
```

#### 3. **港股数据处理** (analyze_stock.py)
- 使用 `akshare.hk_qvix_kline()` 获取港股历史K线数据
- 自动计算所有技术指标（MA、MACD、RSI、KDJ、BB、ATR、OBV等）  
- 返回 JSON 格式的技术指标和最近20条行情记录
- 完整的错误处理和异常捕获

#### 4. **更新依赖包** (requirements.txt)
新增：`akshare>=1.15.0` - 港股和其他市场数据源

#### 5. **文档更新** (SKILL.md)
- 补充港股支持说明
- 添加技术指标支持矩阵
- 说明两种数据源的区别
- 更新数据更新频度说明

---

## 支持的技术指标

| 指标 | 说明 | A股 | 港股 |
|------|------|-----|------|
| MA5/10/20/60 | 移动平均线 | ✓ | ✓ |
| MACD | MACD动向指标 | ✓ | ✓ |
| RSI | 相对强弱指数 | ✓ | ✓ |
| KDJ | 随机指标 | ✓ | ✓ |
| BBANDS | 布林带 | ✓ | ✓ |
| OBV | 能量潮 | ✓ | ✓ |
| ATR | 平均真实波幅 | ✓ | ✓ |

---

## 使用示例

### 分析A股
```bash
python scripts/analyze_stock.py 000001
python scripts/analyze_stock.py 600036
```

### 分析港股
```bash
python scripts/analyze_stock.py 00700.HK
python scripts/analyze_stock.py 09973.HK
```

### 指定输出目录
```bash
python scripts/analyze_stock.py 00700.HK --output-dir /path/to/output
```

---

## 技术细节

### 港股数据获取流程

1. **验证代码格式**：确保是5位数字+.HK
2. **获取原始数据**：调用 akshare 获取日K线数据
3. **列名转换**：统一列名格式
4. **指标计算**：使用TA-Lib计算所有技术指标
5. **错误处理**：任何单项指标失败不影响整体结果
6. **数据返回**：JSON格式包含指标和最近20条记录

### 错误处理策略

- 单个指标计算失败 → 打印警告，继续处理其他指标
- 数据获取失败 → 返回详细错误信息和故障排除建议
- 依赖包缺失 → 自动尝试安装

---

## 代码验证结果

✓ 港股代码验证：00700.HK → True
✓ 港股代码验证：03690.HK → True  
✓ 港股代码验证：09973.HK → True
✓ 港股代码验证：001.HK → False (格式错误)
✓ A股代码验证：000001 → True
✓ A股代码验证：600036 → True
✓ A股代码验证：00001 → False (格式错误)

---

## 改进前后对比

| 功能 | 优化前 | 优化后 |
|------|--------|--------|
| A股支持 | ✓ | ✓ |
| 港股支持 | ❌ | ✓ |
| 自动路由 | ❌ | ✓ |
| 技术指标 | 仅A股 | A股+港股 |
| 错误处理 | 简单 | ✓ 详细 |
| 数据源 | aishare-txt | aishare-txt + akshare |

---

## 文件修改列表

1. **scripts/analyze_stock.py** - 新增港股支持，实现双数据源路由
2. **requirements.txt** - 新增 akshare 依赖
3. **scripts/init_dependencies.py** - 新增 akshare 依赖检查
4. **SKILL.md** - 文档更新，补充港股支持说明

---

## 后续优化方向

- [ ] 缓存港股数据，减少网络请求
- [ ] 支持更多港股技术指标
- [ ] 支持美股和其他国际市场
- [ ] 增加B股和债券支持
- [ ] 性能优化：并行获取多只股票数据
