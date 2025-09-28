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

You'll need an Upstox Account to get their API. Follow the steps here:
https://upstox.com/trading-api/

Once you receive your Client ID, API Key, and API Secret, you'll need to authorize your credentials using the code in Cell 1. After you authorise, you'll receive a 6 letter code on the redirect URL. Use that in Cell 2 to get the access token.

This part has to be done manually due to regulations.

Do not hardcode any of your credentials. Make a .env file or a separate .py file to store all the credentials (except the auth and access tokens, because they have an expiration time and have to be acquired again), and use f strings and imports to get them. 

```python
# In Cell 1 and 2: Update your Upstox API credentials
params = {
    "code": "YOUR_AUTH_CODE",  # Get from Upstox OAuth flow
    "client_id": f"{UPSTOX_API_KEY}",
    "client_secret": f"{UPSTOX_API_SECRET}",
    # ... other params
}
```

After you get the access token, the algorithm is ready.

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

## Before running, create a folder named "BacktestLogs". The backtesting logs, including the csv files and a detailed txt file will be saved there. If you wish to change the directory, please also make the changes in the update_port method inside the backtest_v3 class, cell 5.

```python
# Execute the backtest
backtest_time = int(input("Enter backtest duration (Years, maximum 10): "))
test = backtest_v3(backtest_time)
test.old_graph() # Gets the initial portfolio chart
test.update_port()  # Run the backtest, this will take time
test.new_graph() #Gets the final portfolio graph
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
- Configurable timeframe analysis
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

#### **Short Trading Strategy**
```python
TIMEFRAME_1 = 1    # 1 day
TIMEFRAME_2 = 3    # 3 days
TIMEFRAME_3 = 5    # 5 days
WEIGHT_1 = 0.7     # Heavy weight on recent performance
WEIGHT_2 = 0.2
WEIGHT_3 = 0.1
REBALANCE_FREQUENCY = 3  # Daily rebalancing
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

1. **Universe**: 24 carefully selected Indian stocks across sectors. You can modify to include any stocks, no limits. Analysis and backtest times will increase accordingly.
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

## 📈 Performance Results

### 🏆 **Historical Backtesting Results**

Based on actual backtesting logs in `BacktestLogs/` directory:

#### **Recent 5-Year Backtest (2020-2025)**
- **Initial Investment**: ₹100,000
- **Final Value**: ₹383,814
- **CAGR**: 30.75%

#### **10-Year Backtest (2015-2025)**
- **Initial Investment**: ₹100,000
- **Final Value**: ₹790,671
- **CAGR**: 23.06%

#### **Strategy Performance Characteristics**
- **Volatility**: Moderate to high (momentum-based)
- **Sharpe Ratio**: Estimated 1.2-1.8 (based on returns)
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

## 🔑 API Setup Guide

### 🚀 **Upstox API Setup (Recommended)**

1. **Create Upstox Account**:
   - Sign up at [Upstox Developer Console](https://upstox.com/developer/apps)
   - Create a new app to get API credentials

2. **Get API Credentials**:
   - **API Key**: Your application's API key
   - **API Secret**: Your application's secret key
   - **Redirect URI**: Set to `https://localhost:3000`

3. **Create Secrets File**:
   ```python
   # Create: Secrets/upstox_secrets.py
   UPSTOX_API_KEY = "your_api_key_here"
   UPSTOX_API_SECRET = "your_api_secret_here"
   ```

4. **OAuth Flow**:
   - Run Cell 1 to get authorization URL
   - Visit URL, login, and copy the authorization code
   - Paste code in Cell 1 and run to get access token

### 🔄 **Using Other APIs**

To use a different API provider, modify these components:

#### **1. Authentication (Cells 1-2)**:
Replace Upstox OAuth with your API's authentication method

#### **2. Data Fetching Function**:
In `portfolio_custom_date_m1_v3()`, update:
```python
# Change this URL format:
url2 = f'https://api.upstox.com/v3/historical-candle/{key}/days/1/{to_date}/{from_date}'

# To your API's endpoint format, example:
url2 = f'https://your-api.com/historical/{symbol}?from={from_date}&to={to_date}'
```

#### **3. Response Structure**:
Update data parsing based on your API's response format:
```python
# Upstox format: response2["data"]["candles"]
# Your API format: response2["your_data_key"]
```

#### **4. Stock Symbols**:
Update the `keys` dictionary with your API's symbol format:
```python
keys = {"YOUR_SYMBOL_FORMAT": "STOCK_NAME", ...}
```

### 📦 **Installation**

```bash
pip install numpy pandas requests matplotlib tqdm
```

## 📁 Project Structure

```
Algorithmic-Trading/
├── 📓 StratOne.ipynb              # Main trading system
├── 📄 README.md                   # Documentation
├── 📁 BacktestLogs/               # Generated backtest results
├── 📁 Charts/                     # Generated performance charts
└── 📁 Secrets/                    # Your API credentials (create this)
    └── 🔐 upstox_secrets.py       # API keys (you create this file)
```

### 🎯 **Key Files**:
- **`StratOne.ipynb`**: The main algorithm - start here!
- **`.env` or `secrets.py`**: The file which contains your credentials
## ⚠️ Disclaimer

**This is for educational and research purposes only. This is not financial advice.**

- 📚 **Educational Tool**: Learn algorithmic trading concepts
- 🧪 **Research Only**: Backtest and analyze your own strategies
- ⚠️ **Risk Warning**: Trading involves substantial risk of loss
- 🚫 **No Guarantees**: Past performance ≠ future results

**Use at your own risk. Always do your own research.**

## 🤝 Contributing

Feel free to:
- 🐛 Report bugs
- 💡 Suggest improvements  
- 🔧 Submit pull requests
- ⭐ Star the repo if you find it useful!

Currently, I'm working on adding smart stop loss methods in this. Feel free to reach out with suggestions!

---

**Open Source Algorithmic Trading System**  
**Made with ❤️ for the trading community** 
