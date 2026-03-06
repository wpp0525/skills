# Stock Analysis Skill - 优化记录

## 最近优化内容

### 问题
在Claude Code中每次执行stock-analysis skill时，都会报"AIShareTxt package not installed"错误，需要人工干预安装依赖。

### 解决方案

#### 1. **自动依赖安装机制** (analyze_stock.py)
脚本现在会在首次运行时自动检查和安装缺失的依赖，尝试策略：
- `pip install --break-system-packages` (macOS/Linux新版pip)
- `pip install --user` (用户级别安装)
- `pip install` (标准安装)

#### 2. **依赖初始化脚本** (init_dependencies.py)
新增初始化脚本，用于手动或提前检查和安装依赖：
```bash
python scripts/init_dependencies.py
```

#### 3. **改进错误提示**
- 更详细的错误信息和故障排除步骤
- JSON格式的错误响应，便于Claude解析和提示用户

#### 4. **支持港股代码**
已支持分析港股和A股：
- A股：6位数字 (如 000001、600036)
- 港股：5位数字+.HK (如 00700.HK、03690.HK)

---

## 使用方式

### 在Claude中快速启动

```bash
python scripts/analyze_stock.py 000001
python scripts/analyze_stock.py 00700.HK
```

### 使用shell脚本

```bash
./scripts/run.sh 000001
./scripts/run.ps1 00700.HK  # PowerShell
scripts\run.bat 000001      # Windows Batch
```

### 初始化依赖（可选）

```bash
python scripts/init_dependencies.py
```

---

## 技术细节

### 自动安装流程

1. 脚本启动时调用 `ensure_dependencies()`
2. 检查所需包是否可导入：AIShareTxt, talib, pandas, numpy
3. 如果缺失，调用 `try_install_dependencies()`
4. 依次尝试3种安装方法
5. 最后3秒内重新导入验证

### 支持的环境

- ✅ macOS (系统Python + pip限制)
- ✅ Linux (系统Python + pip限制)
- ✅ Windows (系统Python)
- ✅ Claude Code集成环境
- ✅ CI/CD 管道

### 依赖包列表

| 包名 | 版本 | 用途 |
|------|------|------|
| aishare-txt | >=0.1.0 | 中国股票数据处理 |
| TA-Lib | >=0.4.26 | 技术指标计算 |
| pandas | >=1.5.0 | 数据处理和分析 |
| numpy | >=1.21.0 | 数值计算 |
| scipy | >=1.9.0 | 科学计算 |

---

## 故障排除

### 场景1：在Claude中还是报缺失依赖

**解决方案：** 脚本现在会自动安装，但如果仍然失败，尝试：
```bash
python scripts/init_dependencies.py
```

### 场景2：TA-Lib导入失败

**解决方案：** 需要系统级依赖
```bash
# macOS
brew install ta-lib

# Ubuntu/Debian
sudo apt-get install build-essential python3-dev ta-lib

# 然后重新安装Python包
pip install --break-system-packages TA-Lib
```

### 场景3：externally-managed-environment 错误

**解决方案：** 使用以下方法之一：
```bash
# 方式1：使用--break-system-packages
pip install --break-system-packages -r requirements.txt

# 方式2：用户级别安装
pip install --user -r requirements.txt

# 方式3：创建虚拟环境
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

---

## 改进前后对比

| 方面 | 优化前 | 优化后 |
|------|--------|--------|
| 首次运行 | 需要手动安装依赖 | ✅ 自动安装 |
| 反复出现错误 | 是 | ✅ 否（缓存依赖） |
| Claude集成 | 不稳定 | ✅ 配置友好 |
| 港股支持 | ❌ 无 | ✅ 已支持 |
| 错误提示 | 简单 | ✅ 详细 |

---

## 后续优化方向

- [ ] 缓存已安装包信息，避免重复检查
- [ ] 支持离线模式（预加载数据）
- [ ] 性能优化：增量更新指标计算
- [ ] web界面支持
- [ ] 实时推送通知功能
