---
name: stock-analysis
description: Chinese stock technical analysis with resonance-based framework (客观共振五维框架). Use when users provide Chinese stock codes (A-shares or Hong Kong stocks) and request: (1) Technical indicator analysis, (2) Stock price/MA analysis, (3) MACD/KDJ/RSI indicators, (4) Volume analysis, (5) Bollinger Bands/ATR analysis, (6) Comprehensive stock reports, (7) Price trend analysis, (8) Acceleration/limit-up detection. **CORE**: Uses multi-dimensional resonance validation (客观共振) and probability-based scoring (not absolute predictions). Supports 6-digit A-share codes (e.g., 000001, 600036, 603259) and 5-digit Hong Kong stock codes with .HK suffix (e.g., 00700.HK, 03690.HK).
---

# Stock Technical Analysis - 客观共振五维框架

基于**多维度共振验证**和**概率化评分**的股票技术分析工具，支持A股和港股，拒绝主观预判，让信号自己说话。

## 核心设计原则

1. **客观信号优先**：先收集信号，不下预设结论
2. **评分化判断**：从"硬性规则"转向"概率评分"，避免一刀切
3. **阶段动态适配**：根据行情阶段动态调整信号解读规则
4. **维度共振验证**：五维相互印证，任一维度不配合即降低置信度
5. **概率思维**：评分代表"概率高低"，非"绝对涨跌"
6. **周期分层**：区分超短线/短线/中长线，不同周期不同策略

---

## 环境配置

### 自动依赖安装

脚本会在首次运行时尝试**自动检查并安装**缺失的依赖包，但在某些
环境（例如 macOS 自带的、由 Homebrew 管理或其他系统受控的 Python）
中，pip 无法修改系统站点包。这时会看到类似“externally-managed-environment”
的错误，脚本会报告安装失败。在这种情况下请改用手动安装或虚拟环境。

支持的自动安装方法（按优先级）：

1. **--break-system-packages** 用于 macOS/Linux 新版 pip
2. **--user** 标志用于用户级别安装
3. **标准 pip 安装**

如果自动安装失败，请参照“故障排除”部分的手动方法。

### 手动初始化（可选）

也可以提前初始化依赖：

```bash
python scripts/init_dependencies.py
```

> ⚠️ **网络说明**：港股数据依赖第三方接口，偶尔会出现连接中断或响应错误。
> 脚本具有重试机制，但如果多次失败，可以：
> 1. 检查网络连接后重试。

> 3. 下载本地 CSV 并直接分析或更换到其他数据源。

### 依赖包列表

- **aishare-txt>=0.1.0** - A股数据处理和技术分析
- **akshare>=1.15.0** - 港股数据获取和处理

  （**可选**：脚本默认不强制安装；如果 akshare 方法网路不稳或返回错误，
  安装此包后会使用额外的备选方案）
- **TA-Lib>=0.4.26** - 技术指标计算（MA、MACD、RSI、KDJ、BB、ATR等）
- **pandas>=1.5.0** - 数据处理和分析
- **numpy>=1.21.0** - 数值计算
- **scipy>=1.9.0** - 科学计算

**数据来源说明**：
- A股：使用 aishare-txt 库（基于专业财务数据源）
- 港股：使用 akshare 库（实时港股数据）

### 系统要求

- Python 3.10+
- macOS/Linux/Windows 均支持
- TA-Lib 需要系统级依赖：
  - macOS: `brew install ta-lib`
  - Linux: `sudo apt-get install ta-lib`
  - Windows: 从 https://github.com/cgohlke/talib-build 下载预编译wheel

### 故障排除

若遇到依赖安装问题：

**方法 1（推荐在Claude中执行）**
```bash
python scripts/analyze_stock.py 000001
```
脚本会自动尝试安装依赖。

**方法 2（手动安装）**
```bash
pip install --break-system-packages -r requirements.txt
```

**方法 3（用户级别安装）**
```bash
pip install --user -r requirements.txt
```

> ⚠️ 如果你得到类似 “externally-managed-environment” 的错误，表明当前
> Python 解释器受到系统管理，无法通过 pip 修改全局包。在这种情形下
> 建议创建虚拟环境：
>
> ```bash
> python3 -m venv venv
> source venv/bin/activate
> pip install -r requirements.txt
> ```
>
> 或者仅单独安装可选模块：
> ```bash

> ```

---

## 运行分析

### Windows (PowerShell)
```powershell
.\ scripts\run.ps1 000001
.\ scripts\run.ps1 00700.HK
```

### Windows (Batch)
```bash
scripts\run.bat 000001
scripts\run.bat 00700.HK
```

### Linux/macOS
```bash
chmod +x scripts/run.sh
./scripts/run.sh 000001
./scripts/run.sh 00700.HK
```

### 直接运行Python

```bash
python scripts/analyze_stock.py 000001
python scripts/analyze_stock.py 00700.HK
```

---

## 常用股票代码

**A股（沪深京）**
- `000001` - 平安银行
- `600036` - 招商银行
- `603259` - 药明康德
- `000858` - 五粮液
- `002957` - 科瑞技术

**港股（香港上市）**
- `00700.HK` - 腾讯控股
- `03690.HK` - 美团
- `01398.HK` - 工商银行
- `02778.HK` - 小米集团
- `00175.HK` - 吉利汽车

---

## 调用说明

**从Claude Code调用此技能时**：

1. 设置`USER_WORKING_DIR`环境变量为用户当前工作目录
2. 运行分析脚本获取原始技术数据
3. 按照**客观共振五步分析法**生成报告（参考下方）
4. **评分规则**详见 `templates/strategy_rules.md`
5. **报告输出格式**详见 `templates/report_template.md`
6. 保存Markdown报告到用户工作目录

```bash
cd  ~/.claude/skills/stock-analysis

# A股示例
USER_WORKING_DIR={用户工作目录} python scripts/analyze_stock.py 000001

# 港股示例
USER_WORKING_DIR={用户工作目录} python scripts/analyze_stock.py 00700.HK
```

---

## 客观共振五步分析法

**这是本技能的核心分析框架，必须严格按此顺序执行，不得跳步或预设结论。**

执行时必须同时参考：
- `templates/strategy_rules.md` - 详细评分标准和策略规则
- `templates/report_template.md` - 报告输出格式

---

### 第一步：客观信号收集 📋

**目的**：不做任何预设，客观记录五维核心的多空信号。

**原则**：
- 只记录客观信号，不做解读
- 多空信号平等记录，不提前过滤
- 信号必须来自原始数据，不得主观推断

**五维核心信号收集**：

| 维度 | 多头信号 | 空头信号 |
|------|---------|---------|
| 量能 | 从数据中提取 | 从数据中提取 |
| 价格 | 从数据中提取 | 从数据中提取 |
| 时间 | 从数据中提取 | 从数据中提取 |
| 空间 | 从数据中提取 | 从数据中提取 |
| 趋势 | 从数据中提取 | 从数据中提取 |

**⚠️ 信号统计**：按 `templates/strategy_rules.md` 中的"综合评分机制"进行五维评分。

---

### 第二步：行情阶段识别 🎯

**目的**：识别当前所处行情阶段，为下一步动态解读提供依据。

#### 三大行情阶段识别标准

| 阶段 | 识别标准（满足3条以上） | 特征描述 |
|------|---------------------|---------|
| **震荡市** | 1.ADX<25<br>2.MA均线粘合<br>3.价格在布林带中轨附近<br>4.近10日涨跌幅<10% | 方向不明，箱体波动 |
| **趋势加速市** | 1.ADX>25且上升<br>2.MA均线发散<br>3.价格突破布林上轨<br>4.近5日涨跌幅>10% | 方向明确，动能强劲 |
| **反转市** | 1.原趋势衰竭<br>2.出现反向突破信号<br>3.MA即将金叉/死叉<br>4.成交量异常放大 | 趋势转换，变盘点 |

**⚠️ 如果判定为"趋势加速市"**：必须执行 `templates/strategy_rules.md` 中的"趋势阶段细分"评分判定。

---

### 第二步-B：趋势阶段细分（仅趋势加速市）

**当第二步判定为"趋势加速市"时，必须执行此步骤。**

参考 `templates/strategy_rules.md` 中的"趋势阶段细分评分规则"：

- 计算加速初期、中期、末期的各自得分
- 得分最高的阶段为当前阶段
- 末期得分≥6分：进入高风险区

**动态阈值调整**：
- 强势牛市：涨幅阈值+10%，BIAS阈值+3%
- 弱势熊市：涨幅阈值-10%，BIAS阈值-3%
- 高波成长股：涨幅阈值+15%，BIAS阈值+5%

---

### 第三步：动态信号解读 🔄

**目的**：根据行情阶段，动态调整信号的解读规则。

**关键原则**：同一信号在不同阶段有完全不同的含义，绝不能用同一套规则套所有行情。

**必须参考** `templates/strategy_rules.md` 中的：
- "综合评分机制"（五维评分）
- "动态信号解读规则"（概率化表达）
- "例外情况识别"（涨停板、高控盘等）

**解读原则**：
- 使用概率表达（如"80%向上"）而非绝对判断
- 识别例外情况（涨停板缩量是正常的）
- 区分交易周期（超短线/短线/中长线）

---

### 第四步：五维共振验证 🔗

**目的**：检查各维度之间是否相互印证，形成共振闭环。

#### 维度联动验证

| 维度A | 维度B | 验证重点 |
|-------|-------|---------|
| 量能 | 价格 | 放量上涨/缩量上涨/放量下跌/缩量下跌 |
| 价格 | 趋势 | 价格站上均线/跌破均线 + MACD多空 |
| 趋势 | 资金 | 趋势方向 + 资金流向 |
| 资金 | 量能 | 资金流向 + OBV/成交量 |
| 动量 | 趋势 | RSI/KDJ状态 + 趋势强度 |

#### 共振强度评级

基于综合评分（满分100分）：

| 等级 | 分数区间 | 含义 | 建议仓位 |
|------|---------|------|---------|
| 🔴 强共振 | ≥90分 | 五维共振向上，高概率上涨 | 50-70% |
| 🟠 中等共振 | 75-89分 | 五维偏多，上涨概率较大 | 30-50% |
| 🟡 弱共振 | 60-74分 | 五维分歧，方向不确定 | 10-30% |
| 🟢 无共振/分歧 | <60分 | 五维混乱，等待信号明确 | 0-10% |

**⚠️ 背离检测**：

参考 `templates/strategy_rules.md` 中的"背离检测规则"：
- 量价背离：-5至-8分
- 量能背离：-5至-10分
- 动量背离：-5至-10分
- 豁免条件：涨停板、高控盘、市场整体缩量等

背离总分 > 15分：降低评级至少1级

---

### 第五步：结论推导与策略 📝

**目的**：基于前四步的客观分析，推导最终结论和操作建议。

**严禁**：在此步骤引入主观预设或与前面分析矛盾的观点。

#### 综合评级标准

| 总分 | 评级 | 含义 | 建议仓位 |
|------|------|------|---------|
| ≥90 | ⭐⭐⭐⭐⭐ 明确看多 | 高概率上涨，五维共振 | 50-70% |
| 75-89 | ⭐⭐⭐⭐ 偏多 | 上涨概率较大，机会>风险 | 30-50% |
| 60-74 | ⭐⭐⭐ 中性 | 方向不明，观望为主 | 10-30% |
| 45-59 | ⭐⭐ 偏空 | 下跌概率较大，风险>机会 | 0-10% |
| <45 | ⭐ 明确看空 | 高概率下跌，五维向下 | 0% |

**注意**：评分是概率判断，90分代表"高概率上涨"，非"一定上涨"。

#### 操作策略

**必须根据行情阶段、细分阶段、交易周期，选择对应的策略模板**。

参考 `templates/strategy_rules.md` 中的"分阶段操作策略模板"：

**交易周期分层**：

| 周期 | 持有期 | 风险容忍 | 策略特点 |
|------|--------|---------|---------|
| 超短线 | <3天 | 高 | 严格止损，可追涨 |
| 短线 | 3-10天 | 中 | 等待确认，控制仓位 |
| 中长线 | >10天 | 低 | 趋势跟踪，分批建仓 |

**加速末期策略（末期得分≥6分）**：
- 稳健型：观望为主，不新开仓
- 短线型：极低仓位（5-10%）参与反弹
- 超短线：涨停确认可小仓位（≤10%）
- 持筹者：逐步减仓至≤30%

**特殊情况策略**：
- 大盘暴跌日(>3%)：所有策略仓位减半
- 涨停板：超短线可追，中长线等待开板确认

---

## 格式要求

- 严禁使用 `<br>` 标签，改用列表形式或分隔线
- 使用标准Markdown格式
- emoji增强可读性（📋🎯🔄🔗📝✅❌🔴🟠🟡🟢）
- 共振评级用彩色圆点标识
- 使用概率化表达（如"80%向上"）而非绝对判断
- 完整报告格式参考 `templates/report_template.md`

---

## 文件结构

```
stock-analysis/
├── scripts/                 # 脚本目录
│   ├── run.ps1 / run.bat / run.sh
│   └── analyze_stock.py
├── templates/               # 规则和模板目录
│   ├── strategy_rules.md   # 评分规则和策略模板
│   └── report_template.md  # 报告输出格式
└── SKILL.md                 # 本文件（核心框架说明）
```

---

## 错误处理

- 依赖包缺失 → 返回安装步骤
- TA-Lib未安装 → 返回安装链接
- 无效股票代码 → 返回错误提示和示例

---

## 重要说明

### 股票代码格式

| 市场 | 格式 | 示例 | 数据源 |
|------|------|------|--------|
| A股（沪深京） | 6位数字 | 000001、600036、603259 | aishare-txt |
| 港股（香港） | 5位数字+.HK | 00700.HK、03690.HK | akshare |

### 技术指标支持

**所有市场支持的指标**：
- 移动平均线：MA5、MA10、MA20、MA60
- MACD：MACD、MACD_SIGNAL、MACD_HIST
- RSI：相对强弱指数
- KDJ：随机指标（K、D）
- Bollinger Bands：上轨、中轨、下轨
- OBV：能量潮
- ATR：平均真实波幅

### 数据来源与更新

- **A股数据**：aishare-txt（实时更新，包含完整技术指标）
- **港股数据**：akshare（实时港股行情，计算技术指标）
- **更新频度**：交易时段实时更新，非交易时段使用最新收盘数据

### 免责声明

- 报告仅供参考，不构成投资建议
- 所有分析基于历史数据和技术指标
- 股票投资存在风险，请谨慎决策
- 所有报告自动保存到用户当前工作目录
- **核心**：客观共振五步分析法 + 概率化评分
- **评分**：详见 `templates/strategy_rules.md`
- **格式**：详见 `templates/report_template.md`
- **原则**：评分代表概率，非绝对预测
