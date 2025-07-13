# Algorithmic Trading System Documentation

## Overview
This algorithmic trading system is designed to analyze and backtest trading strategies in the Indian stock market (NSE) using historical data from the Upstox API. The system implements momentum-based trading strategies with comprehensive backtesting capabilities and performance visualization.

## System Architecture

### 1. Data Collection and Authentication
The system uses the Upstox API for market data access:
- Manual OAuth2 authentication flow with authorization codes
- API credentials stored in `Secrets/upstox_secrets.py`
- Historical data fetching for daily and monthly candles
- Support for both daily and intraday (30-minute) data

### 2. Trading Strategies Implemented

#### 2.1 Performance-Based Trading (Main Strategy - trading.ipynb)
The primary strategy focuses on short to medium-term momentum:

**Data Analysis**:
- Fetches daily candle data (7 days) and intraday 30-minute data
- Calculates daily and weekly performance percentages
- Tracks a curated list of 25+ major Indian stocks

**Performance Calculation**:
- Daily performance: Price movement over last 24 hours using intraday data
- Weekly performance: Price movement over the past week using daily data
- Combined score: `daily_performance * 0.6 + weekly_performance * 0.4`

**Signal Generation**:
- Buy Signal: Performance score ≥ 10
- Hold Signal: Performance score between 0 and 10
- Sell Signal: Performance score < 0

#### 2.2 Medium-Long Hybrid Strategy (MediumLongHybrid.ipynb)
Multi-timeframe momentum strategy for longer-term analysis:

**Analysis Timeframes**:
- 3-month performance analysis
- 6-month performance analysis  
- 1-year performance analysis

**Scoring System**:
- Combined score: `3month * 0.5 + 6month * 0.4 + 1year * 0.1`
- Same signal thresholds as main strategy

**Portfolio Approach**:
- Fixed portfolio of 10 selected stocks
- Equal-weight allocation initially

#### 2.3 Version One Strategy (VersionOne copy.ipynb)
Simplified multi-timeframe approach:

**Analysis Timeframes**:
- 1-month, 3-month, 6-month performance
- Scoring: `1month * 0.6 + 3month * 0.3 + 6month * 0.1`

### 3. Technical Implementation

#### 3.1 Data Processing
- Historical data retrieval via Upstox API endpoints
- Price performance calculations using close prices
- Statistical analysis for performance ranking

#### 3.2 Backtesting Framework
Comprehensive backtesting system with the following features:

**Portfolio Management**:
- Equal-weight portfolio construction
- Dynamic stock selection (top 10 performers for main strategy)
- Position sizing based on available balance
- Transaction cost modeling (2.5% of trade value or ₹20 minimum)

**Backtesting Process**:
- Historical simulation over specified time periods
- Regular portfolio rebalancing (7-day intervals for main strategy, 30-day for others)
- Buy/sell/hold decisions based on performance scores
- Portfolio value tracking over time

**Performance Metrics**:
- CAGR (Compound Annual Growth Rate) calculation
- Portfolio growth tracking
- Total evaluation including cash balance

#### 3.3 Visualization Tools
- Portfolio composition pie charts (initial vs final)
- Portfolio growth charts over time
- Total evaluation growth visualization
- Performance comparison charts (available in Charts/ directory)

### 4. Stock Universe

The system tracks carefully selected Indian stocks including:

**Large-Cap Stocks**:
- RELIANCE, HDFCBANK, INFY, LT, AXISBANK, MARUTI, ULTRACEMCO, BHARTIARTL

**Mid-Cap and Growth Stocks**:
- ZOMATO, TRENT, ADANIGREEN, ADANIPOWER, TATAPOWER, POWERGRID, PIDILITIND, GODREJCP, COLPAL, VEDL, INDIGO, TVSMOTOR, ABB, SIEMENS

**Additional Stocks** (varies by strategy):
- BAJFINANCE, ASIANPAINT, TITAN, BIOCON, PFC, GAIL, IOC

### 5. Actual Performance Results

Based on backtesting logs in the `BacktestLogs/` directory:

**Main Strategy (trading.ipynb)**:
- 10-year backtest: 38.19% CAGR
- Final value: ₹2,434,575 from initial ₹95,840

**Medium-Long Hybrid**:
- 10-year backtest: 10.79% CAGR  
- Final value: ₹272,689 from initial ₹97,871

**Version One**:
- 1-year backtest: 47.48% CAGR
- Final value: ₹130,557 from initial ₹88,527

### 6. System Limitations

**Current Limitations**:
- No real-time trading execution
- No automated trade placement
- Manual authentication token refresh required
- No stop-loss or risk management beyond position sizing
- No options or futures trading capabilities
- No machine learning components
- No sentiment analysis
- No advanced technical indicators beyond momentum

**Data Dependencies**:
- Requires active Upstox API access
- Historical data availability dependent on API limits
- Manual intervention required for token refresh

### 7. System Requirements

**Technical Requirements**:
- Python 3.7+
- Jupyter Notebook environment
- Upstox API account and credentials
- Required Python packages:
  - numpy, pandas, requests, matplotlib, scipy, tqdm, json, statistics, math, datetime

**Usage Requirements**:
- Manual OAuth2 authentication setup
- API rate limiting considerations (15-30 second delays between requests)
- Sufficient historical data for backtesting periods

### 8. File Structure

- `trading.ipynb`: Main momentum-based trading strategy
- `MediumLongHybrid.ipynb`: Long-term multi-timeframe strategy  
- `VersionOne copy.ipynb`: Simplified version of the strategy
- `NSE.csv`: Market data reference file (2MB+)
- `BacktestLogs/`: Historical backtesting results and trade logs
- `Charts/`: Performance visualization exports
- `Secrets/`: API credentials (not included in repository)

## Conclusion

This system provides a solid foundation for momentum-based algorithmic trading research and backtesting in the Indian stock market. The implementation focuses on historical analysis and strategy validation rather than live trading execution. 

**Key Strengths**:
- Robust backtesting framework
- Multiple strategy implementations
- Comprehensive performance tracking
- Good documentation of results

**Areas for Development**:
- Real-time execution capabilities
- Advanced risk management features
- Additional technical indicators
- Automated authentication handling

Users should thoroughly understand the system's limitations and conduct additional validation before considering any live trading implementation. 
