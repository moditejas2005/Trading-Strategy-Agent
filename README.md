# Trading Strategy Agent

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An intelligent AI-powered trading strategy system that analyzes financial markets, generates automated trading strategies, and provides data-driven investment recommendations.

![Trading Dashboard](https://img.shields.io/badge/Status-Production%20Ready-success)

## Features

### Core Functionality
- **Dual Data Sources** - yfinance + Alpha Vantage API for maximum reliability
- **Technical Indicators** - RSI, MACD, Moving Averages, Bollinger Bands
- **AI Strategy Generation** - Intelligent BUY/SELL/HOLD recommendations
- **Advanced Backtesting** - Historical performance with 10+ metrics
- **PostgreSQL Database** - Persistent storage for strategies and results
- **Interactive Dashboard** - Modern dark-themed web interface
- **Real-time Analytics** - Live charts and performance visualizations
- **INR Currency Support** - All prices converted to Indian Rupees

### API Integrations
- **Alpha Vantage API** - Enhanced market data & fundamentals
- **yfinance** - Primary stock data source
- **PostgreSQL** - Production-grade database

### Technical Highlights
- RESTful API with Flask
- SQLAlchemy ORM for database operations
- Modular Python architecture
- Real-time data visualization with Plotly
- Comprehensive test suite with pytest
- Example scripts and documentation

## Available Stocks (25 Total)

### Indian Stocks (NSE) - 15

| Symbol | Company |
|--------|---------|
| RELIANCE.NS | Reliance Industries |
| TCS.NS | Tata Consultancy Services |
| HDFCBANK.NS | HDFC Bank |
| INFY.NS | Infosys |
| ICICIBANK.NS | ICICI Bank |
| HINDUNILVR.NS | Hindustan Unilever |
| SBIN.NS | State Bank of India |
| BHARTIARTL.NS | Bharti Airtel |
| BAJFINANCE.NS | Bajaj Finance |
| WIPRO.NS | Wipro |
| KOTAKBANK.NS | Kotak Mahindra Bank |
| LT.NS | Larsen & Toubro |
| AXISBANK.NS | Axis Bank |
| MARUTI.NS | Maruti Suzuki |
| TATAMOTORS.NS | Tata Motors |

### US Stocks - 10

| Symbol | Company |
|--------|---------|
| AAPL | Apple Inc. |
| GOOGL | Alphabet (Google) |
| MSFT | Microsoft |
| AMZN | Amazon |
| TSLA | Tesla |
| META | Meta (Facebook) |
| NVDA | NVIDIA |
| JPM | JPMorgan Chase |
| V | Visa |
| JNJ | Johnson & Johnson |

> **Note:** All prices are displayed in ₹ (INR) with live USD to INR conversion.

## Quick Start

### Prerequisites
- Python 3.9 or higher
- pip package manager
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/moditejas2005/Trading-Strategy-Agent.git
cd Trading-Strategy-Agent
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Setup PostgreSQL database** (Optional)
```bash
# Install PostgreSQL (if not already installed)
# Windows: https://www.postgresql.org/download/windows/
# Mac: brew install postgresql
# Linux: sudo apt-get install postgresql

# Create database
psql -U postgres
CREATE DATABASE trading_agent;
\q

# Initialize tables
python database.py
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your credentials
```

5. **Run the application**
```bash
python app.py
```

6. **Open your browser**
```
http://localhost:5000
```

## Project Structure

```
Trading-Strategy-Agent/
├── modules/
│   ├── data_collector.py      # Market data fetching
│   ├── indicators.py          # Technical indicators
│   ├── strategy_generator.py  # AI strategy generation
│   ├── backtester.py          # Backtesting engine
│   ├── currency_converter.py  # USD to INR conversion
│   └── alpha_vantage_collector.py  # Alpha Vantage API
├── templates/
│   └── index.html             # Dashboard UI
├── static/
│   ├── css/
│   │   └── style.css          # Modern dark theme
│   └── js/
│       └── app.js             # Frontend logic
├── app.py                     # Flask API server
├── config.py                  # Configuration management
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Usage Examples

### Analyze a Stock
```python
from modules.data_collector import DataCollector
from modules.indicators import TechnicalIndicators

# Fetch data
collector = DataCollector(symbol='RELIANCE.NS', period='3mo')
data = collector.fetch_data()

# Calculate indicators
indicators = TechnicalIndicators(data)
signals = indicators.get_latest_signals()

print(signals)
```

### Run Backtest
```python
from modules.backtester import Backtester

backtester = Backtester(data, initial_capital=100000)
results = backtester.run_backtest(strategy_type='combined')

print(f"Total Return: {results['total_return_pct']:.2f}%")
print(f"Win Rate: {results['win_rate']:.2f}%")
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/market-data` | GET | Fetch market data |
| `/api/indicators` | GET | Calculate indicators |
| `/api/strategy` | POST | Generate strategy |
| `/api/backtest` | POST | Run backtest |

## Dashboard Features

- **Real-time Analysis** - Live market data and indicators
- **Strategy Recommendations** - BUY/SELL/HOLD signals with confidence scores
- **Interactive Charts** - Price history and portfolio performance
- **Backtest Results** - Historical performance metrics
- **Dark Theme** - Modern, eye-friendly interface

## Testing

Run tests:
```bash
pytest tests/ -v
```

Run with coverage:
```bash
pytest tests/ --cov=modules --cov-report=html
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [yfinance](https://github.com/ranaroussi/yfinance) - Market data provider
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Plotly](https://plotly.com/) - Visualization library
- [Alpha Vantage](https://www.alphavantage.co/) - Financial data API

## Disclaimer

This software is for educational purposes only. Always do your own research before making trading decisions. The developers are not responsible for any financial losses.

## Contact

For questions or support, please open an issue on GitHub.

---

**Made with ❤️ by the Trading Strategy Agent Team**
