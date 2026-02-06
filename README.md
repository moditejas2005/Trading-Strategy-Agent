# 🤖 AI Trading Strategy Agent

[![CI/CD](https://github.com/moditejas2005/Trading-Strategy-Agent/actions/workflows/ci.yml/badge.svg)](https://github.com/moditejas2005/Trading-Strategy-Agent/actions)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An intelligent AI-powered trading strategy system that analyzes financial markets, generates automated trading strategies, and optimizes AI prompts using the **ScaleDown API** to reduce costs and improve response speed.

![Trading Dashboard](https://img.shields.io/badge/Status-Production%20Ready-success)

## ✨ Features

### Core Functionality
- 📊 **Real-time Market Data** - Fetch live stock and cryptocurrency data
- 📈 **Technical Indicators** - RSI, MACD, Moving Averages, Bollinger Bands
- 🤖 **AI Strategy Generation** - Intelligent trading recommendations
- ⚡ **Prompt Optimization** - ScaleDown API integration for cost reduction
- 📉 **Backtesting Engine** - Test strategies on historical data
- 📱 **Interactive Dashboard** - Modern dark-themed web interface
- 📊 **Performance Analytics** - Comprehensive metrics and visualizations

### Technical Highlights
- RESTful API with Flask
- Modular Python architecture
- Real-time data visualization with Plotly
- CI/CD pipeline with GitHub Actions
- Comprehensive backtesting with performance metrics

## 🚀 Quick Start

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

3. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. **Run the application**
```bash
python app.py
```

5. **Open your browser**
```
http://localhost:5000
```

## 🔑 API Keys Setup

### Required APIs (Optional - fallback modes available)
- **ScaleDown API** (https://skills.sh) - For prompt optimization
- **OpenAI API** - For advanced AI strategy generation

### Configuration
Edit `.env` file:
```env
SCALEDOWN_API_KEY=your_scaledown_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

> **Note**: The system works without API keys using fallback optimization and rule-based strategies.

## 🧪 When You Need API Keys

### ScaleDown API Key Required:
You'll need the **ScaleDown API key** from https://skills.sh when:
- You want to optimize prompts to reduce token usage
- You need cost-efficient AI operations
- You want to see optimization metrics and savings

**Without the key**: The system uses basic text optimization (works but no advanced features)

### Getting Your ScaleDown API Key:
1. Visit https://skills.sh
2. Sign up for an account
3. Navigate to API settings
4. Copy your API key
5. Add it to your `.env` file

## 📖 Project Structure

```
Trading-Strategy-Agent/
├── modules/
│   ├── data_collector.py      # Market data fetching
│   ├── indicators.py           # Technical indicators
│   ├── strategy_generator.py  # AI strategy generation
│   ├── prompt_optimizer.py    # ScaleDown API integration
│   └── backtester.py          # Backtesting engine
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

## 🎯 Usage Examples

### Analyze a Stock
```python
from modules.data_collector import DataCollector
from modules.indicators import TechnicalIndicators

# Fetch data
collector = DataCollector(symbol='AAPL', period='3mo')
data = collector.fetch_data()

# Calculate indicators
indicators = TechnicalIndicators(data)
signals = indicators.get_latest_signals()

print(signals)
```

### Run Backtest
```python
from modules.backtester import Backtester

backtester = Backtester(data, initial_capital=10000)
results = backtester.run_backtest(strategy_type='combined')

print(f"Total Return: {results['total_return_pct']:.2f}%")
print(f"Win Rate: {results['win_rate']:.2f}%")
```

### Optimize Prompts
```python
from modules.prompt_optimizer import PromptOptimizer

optimizer = PromptOptimizer(api_key='your_scaledown_key')
result = optimizer.optimize_prompt("Your trading analysis prompt here")

print(f"Token Reduction: {result['reduction_percentage']:.1f}%")
```

## 🌐 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/market-data` | GET | Fetch market data |
| `/api/indicators` | GET | Calculate indicators |
| `/api/strategy` | POST | Generate strategy |
| `/api/backtest` | POST | Run backtest |
| `/api/optimize-prompt` | POST | Optimize prompt |

## 📊 Dashboard Features

- **Real-time Analysis** - Live market data and indicators
- **Strategy Recommendations** - BUY/SELL/HOLD signals with confidence scores
- **Interactive Charts** - Price history and portfolio performance
- **Backtest Results** - Historical performance metrics
- **Dark Theme** - Modern, eye-friendly interface

## 🧪 Testing

Run tests:
```bash
pytest tests/ -v
```

Run with coverage:
```bash
pytest tests/ --cov=modules --cov-report=html
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [yfinance](https://github.com/ranaroussi/yfinance) - Market data provider
- [ScaleDown API](https://skills.sh) - Prompt optimization
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Plotly](https://plotly.com/) - Visualization library

## ⚠️ Disclaimer

This software is for educational purposes only. Always do your own research before making trading decisions. The developers are not responsible for any financial losses.

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Made with ❤️ by the Trading Strategy Agent Team**
