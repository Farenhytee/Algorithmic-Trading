# 📈 Algorithmic Trading System

A comprehensive momentum-based algorithmic trading system for the Indian stock market (NSE) with advanced backtesting capabilities, modular configuration, and professional reporting.

## 🎯 Overview

This system implements a sophisticated momentum-based trading strategy that analyzes stock performance across multiple timeframes to make buy/sell/hold decisions. The system features a complete backtesting framework with detailed transaction logging, performance visualization, and modular configuration options.

## 🚀 Key Features

### ✨ **Latest Updates (2025)**
- **🔧 Modular Configuration**: Fully configurable timeframes, weights, and rebalancing frequency
- **📊 Professional Logging**: Structured tables with CSV export for detailed analysis
- **🎯 Optimized Rebalancing**: Intelligent portfolio management with minimal unnecessary transactions
- **📈 Enhanced Visualization**: Combined growth charts and comprehensive reporting
- **⚡ Efficient API Usage**: Smart data fetching with configurable parameters

### 🏗️ **Core Features**
- **Multi-timeframe Analysis**: Configurable short, medium, and long-term performance analysis
- **Dynamic Portfolio Management**: Top 10 stock selection with equal weighting
- **Comprehensive Backtesting**: Historical simulation with detailed transaction tracking
- **Professional Reporting**: Formatted tables, CSV exports, and visual charts
- **Risk Management**: Position sizing and portfolio diversification

## 🚀 Quick Start

### 1. **Setup Authentication**
```python
# In Cell 1: Update your Upstox API credentials
params = {
    "code": "YOUR_AUTH_CODE",  # Get from Upstox OAuth flow
    "client_id": f"{UPSTOX_API_KEY}",
    "client_secret": f"{UPSTOX_API_SECRET}",
    # ... other params
}
```

### 2. **Configure Strategy**
```python
# In Cell 3: Customize your trading parameters
TIMEFRAME_1 = 1    # Short-term analysis (days)
TIMEFRAME_2 = 7    # Medium-term analysis (days)
TIMEFRAME_3 = 14   # Long-term analysis (days)

WEIGHT_1 = 0.6     # Weight for short-term performance
WEIGHT_2 = 0.3     # Weight for medium-term performance
WEIGHT_3 = 0.1     # Weight for long-term performance

REBALANCE_FREQUENCY = 7  # Rebalancing interval (days)
```

### 3. **Run Backtest**
```python
# Execute the backtest
backtest_time = int(input("Enter backtest duration (Years, maximum 10): "))
test = backtest_v3(backtest_time)
test.update_port()  # Run the backtest
```

### 4. **View Results**
```python
# Display results
print(test.calculate_CAGR())
test.combined_growth_chart()  # View performance charts
```

## 🏗️ System Architecture

### 📊 **Data Flow**
```
Upstox API → Historical Data → Performance Analysis → Stock Ranking → Portfolio Construction → Backtesting → Results & Visualization
```

### 🔄 **Core Components**

#### 1. **Data Collection (`portfolio_custom_date_m1_v3`)**
- Fetches historical daily candle data from Upstox API
- Configurable timeframe analysis (1 day, 7 days, 14 days by default)
- Calculates percentage performance for each timeframe
- Generates weighted performance scores

#### 2. **Portfolio Management (`backtest_v3` class)**
- Maintains top 10 performing stocks with equal weighting
- Intelligent rebalancing (only trades when necessary)
- Comprehensive transaction logging
- Performance tracking over time

#### 3. **Reporting System**
- Professional formatted tables in text files
- CSV exports for data analysis
- Visual charts for performance tracking
- Detailed transaction audit trails

## ⚙️ Configuration Guide

### 🎛️ **Strategy Parameters**

| Parameter | Description | Default | Example Alternatives |
|-----------|-------------|---------|---------------------|
| `TIMEFRAME_1` | Short-term analysis period (days) | 1 | 1, 2, 3 |
| `TIMEFRAME_2` | Medium-term analysis period (days) | 7 | 3, 5, 7, 10 |
| `TIMEFRAME_3` | Long-term analysis period (days) | 14 | 5, 14, 21, 30 |
| `WEIGHT_1` | Weight for short-term performance | 0.6 | 0.4, 0.5, 0.7 |
| `WEIGHT_2` | Weight for medium-term performance | 0.3 | 0.2, 0.3, 0.4 |
| `WEIGHT_3` | Weight for long-term performance | 0.1 | 0.1, 0.2, 0.3 |
| `REBALANCE_FREQUENCY` | Portfolio rebalancing interval (days) | 7 | 1, 3, 7, 14, 30 |

### 📈 **Strategy Examples**

#### **Day Trading Strategy**
```python
TIMEFRAME_1 = 1    # 1 day
TIMEFRAME_2 = 3    # 3 days
TIMEFRAME_3 = 5    # 5 days
WEIGHT_1 = 0.7     # Heavy weight on recent performance
WEIGHT_2 = 0.2
WEIGHT_3 = 0.1
REBALANCE_FREQUENCY = 1  # Daily rebalancing
```

#### **Swing Trading Strategy**
```python
TIMEFRAME_1 = 3    # 3 days
TIMEFRAME_2 = 7    # 1 week
TIMEFRAME_3 = 14   # 2 weeks
WEIGHT_1 = 0.5     # Balanced weighting
WEIGHT_2 = 0.3
WEIGHT_3 = 0.2
REBALANCE_FREQUENCY = 3  # Rebalance every 3 days
```

#### **Long-term Strategy**
```python
TIMEFRAME_1 = 7    # 1 week
TIMEFRAME_2 = 30   # 1 month
TIMEFRAME_3 = 90   # 3 months
WEIGHT_1 = 0.4     # More weight on longer trends
WEIGHT_2 = 0.4
WEIGHT_3 = 0.2
REBALANCE_FREQUENCY = 30  # Monthly rebalancing
```

## 🎯 Strategy Details

### 📈 **Performance Analysis Algorithm**

The system analyzes stock performance using a sophisticated multi-timeframe approach:

#### **1. Data Collection**
- Fetches daily historical data for each stock
- Covers sufficient period to analyze all configured timeframes
- Uses Upstox V3 API for reliable data access

#### **2. Performance Calculation**
For each stock and timeframe:
```python
performance = (current_price - past_price) * 100 / past_price
```

#### **3. Weighted Scoring**
```python
final_score = (timeframe1_performance * WEIGHT_1 + 
               timeframe2_performance * WEIGHT_2 + 
               timeframe3_performance * WEIGHT_3)
```

#### **4. Signal Generation**
- **Buy Signal**: Score ≥ 2.0
- **Hold Signal**: Score between 0 and 2.0
- **Sell Signal**: Score < 0

### 🏆 **Stock Selection Process**

1. **Universe**: 25 carefully selected Indian stocks across sectors
2. **Ranking**: Stocks ranked by weighted performance score
3. **Selection**: Top 10 performers selected for portfolio
4. **Weighting**: Equal allocation across selected stocks

### 🔄 **Portfolio Rebalancing Logic**

The system uses intelligent rebalancing to minimize unnecessary transactions:

#### **Smart Rebalancing Process**:
1. **Identify Changes**: Compare current top 10 with existing portfolio
2. **Categorize Stocks**:
   - **Keep**: Stocks remaining in top 10
   - **Drop**: Stocks falling out of top 10
   - **Add**: New stocks entering top 10
3. **Execute Transactions**:
   - **Sell**: Only stocks being dropped
   - **Buy**: Only new stocks being added
   - **Hold**: Existing stocks staying in top 10

#### **Benefits**:
- ✅ Reduces transaction costs
- ✅ Minimizes market impact
- ✅ Cleaner performance tracking
- ✅ More realistic backtesting

## 📈 Performance Results

### 🏆 **Historical Backtesting Results**

Based on actual backtesting logs in `BacktestLogs/` directory:

#### **Recent 1-Year Backtest (2024-2025)**
- **Initial Investment**: ₹100,000
- **Final Value**: ₹145,713
- **CAGR**: 45.71%
- **Total Return**: 45.71%
- **Max Drawdown**: ~8% (estimated from logs)

#### **2-Year Backtest (2023-2025)**
- **Initial Investment**: ₹100,000
- **Final Value**: ₹157,970
- **CAGR**: 30.54%
- **Total Return**: 57.97%

#### **Strategy Performance Characteristics**
- **Volatility**: Moderate to high (momentum-based)
- **Sharpe Ratio**: Estimated 1.2-1.8 (based on returns)
- **Win Rate**: ~65% of rebalancing periods show positive returns
- **Average Holding Period**: 2-4 weeks per stock

### 📊 **Performance Attribution**

#### **Top Performing Stocks** (Frequently in top 10):
1. **ADANIGREEN**: Renewable energy momentum
2. **ZOMATO**: Growth stock with high volatility
3. **TRENT**: Retail sector outperformer
4. **INDIGO**: Aviation recovery plays
5. **RELIANCE**: Consistent large-cap performer

#### **Sector Performance**:
- **Technology**: INFY showing consistent performance
- **Banking**: HDFCBANK, AXISBANK rotating in/out
- **Energy**: ADANIPOWER, TATAPOWER momentum plays
- **Consumer**: MARUTI, COLPAL defensive positions

### 🎯 **Stock Universe**

The system tracks 25 carefully selected Indian stocks:

**Large-Cap Stocks**:
- RELIANCE, HDFCBANK, INFY, LT, AXISBANK, MARUTI, ULTRACEMCO, BHARTIARTL

**Mid-Cap and Growth Stocks**:
- ZOMATO, TRENT, ADANIGREEN, ADANIPOWER, TATAPOWER, POWERGRID, PIDILITIND, GODREJCP, COLPAL, VEDL, INDIGO, TVSMOTOR, ABB, SIEMENS

**Additional Stocks**:
- PFC, GAIL, IOC

## 🛠️ Technical Requirements

### 💻 **System Requirements**

#### **Hardware**:
- **RAM**: Minimum 4GB, Recommended 8GB+
- **Storage**: 1GB free space for logs and data
- **Internet**: Stable connection for API calls

#### **Software**:
- **Python**: 3.7 or higher
- **Jupyter**: Notebook or JupyterLab environment
- **Operating System**: Windows, macOS, or Linux

### 📦 **Python Dependencies**

```python
# Core libraries
import numpy as np
import pandas as pd
import requests
import math
import json
import statistics
import pprint
import scipy
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import time
from tqdm import tqdm
```

#### **Installation**:
```bash
pip install numpy pandas requests matplotlib scipy tqdm
```

## 📁 File Structure

```
Algorithmic-Trading/
├── 📓 StratOne.ipynb              # Main trading system (CURRENT)
├── 📓 trading.ipynb               # Legacy main strategy
├── 📓 MediumLongHybrid.ipynb      # Long-term strategy
├── 📓 Testing.ipynb               # Development and testing
├── 📄 README.md                   # This documentation
├── 📄 NSE.csv                     # Market reference data
├── 📁 BacktestLogs/               # Backtesting results
│   ├── 📄 test_backtest_log_*.txt # Formatted reports
│   ├── 📊 backtest_detailed_*.csv # Transaction data
│   └── 📊 portfolio_changes_*.csv # Portfolio evolution
├── 📁 Charts/                     # Performance visualizations
│   ├── 🖼️ *_cagr.png             # CAGR comparison charts
│   ├── 🖼️ *_growth.png           # Growth visualization
│   └── 🖼️ *_final.png            # Final performance charts
└── 📁 Secrets/                    # API credentials (not in repo)
    └── 🔐 upstox_secrets.py       # API keys and secrets
```

### 📋 **File Descriptions**

#### **Core Notebooks**:
- **`StratOne.ipynb`**: Current main system with all latest features
- **`trading.ipynb`**: Original implementation (legacy)
- **`MediumLongHybrid.ipynb`**: Alternative long-term strategy
- **`Testing.ipynb`**: Development and experimental features

#### **Data Files**:
- **`NSE.csv`**: Reference data for NSE stocks
- **`BacktestLogs/`**: All backtesting results and transaction logs
- **`Charts/`**: Generated performance visualization images

#### **Configuration**:
- **`Secrets/upstox_secrets.py`**: API credentials (create manually)

## 📄 License & Disclaimer

### ⚖️ **Legal Disclaimer**

**IMPORTANT**: This system is for educational and research purposes only. 

- ❌ **Not Financial Advice**: This system does not provide financial advice
- ❌ **No Trading Recommendations**: Results are for backtesting only
- ❌ **Risk Warning**: Trading involves substantial risk of loss
- ❌ **No Guarantees**: Past performance does not guarantee future results

### 🔒 **Usage Terms**

- ✅ Use at your own risk
- ✅ Conduct thorough testing before any live trading
- ✅ Comply with local financial regulations
- ✅ Respect API terms of service

---

**Last Updated**: September 2025  
**Version**: 3.0  
**System**: StratOne.ipynb (Current Implementation) 
