# Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Clone & Install
```bash
git clone https://github.com/moditejas2005/Trading-Strategy-Agent.git
cd Trading-Strategy-Agent
pip install -r requirements.txt
```

### Step 2: Setup Database
```bash
# Create PostgreSQL database
psql -U postgres
CREATE DATABASE trading_agent;
\q

# Initialize tables
python database.py
```

### Step 3: Configure
Edit `.env` and set your PostgreSQL password:
```env
POSTGRES_PASSWORD=your_password
```

### Step 4: Run
```bash
python app.py
```

Open: [http://localhost:5000](http://localhost:5000)

---

## 📚 Example Usage

### Run Complete Analysis
```bash
python examples/complete_analysis.py
```

This will:
1. Fetch AAPL market data
2. Calculate technical indicators
3. Generate AI trading strategy
4. Run backtest with $10,000

### Compare Multiple Stocks
```bash
python examples/compare_stocks.py
```

Analyzes AAPL, GOOGL, MSFT, TSLA, AMZN and shows top recommendations.

### Test Alpha Vantage API
```bash
python examples/alpha_vantage_example.py
```

Demonstrates real-time quotes and company fundamentals.

---

## 🧪 Run Tests
```bash
pytest tests/ -v
```

## 📊 Using the Dashboard

1. Enter stock symbol (e.g., AAPL)
2. Select time period
3. Click "Analyze Strategy"
4. View indicators and recommendations
5. Click "Run Backtest" for historical performance

---

## 🔑 API Keys (Already Configured)

- ✅ ScaleDown API: Active
- ✅ Alpha Vantage API: Active

**Just set your PostgreSQL password and you're ready!**

---

## 🆘 Troubleshooting

**Database connection error?**
- Ensure PostgreSQL is running
- Check password in `.env`
- Run: `python database.py`

**Import errors?**
- Run: `pip install -r requirements.txt`

**API rate limits?**
- yfinance: No key needed
- Alpha Vantage: 5 calls/minute limit

---

## 📖 Documentation

- [README.md](README.md) - Full documentation
- [DATABASE_SETUP.md](DATABASE_SETUP.md) - Database guide
- [Project Mangement.md](Project%20Mangement.md) - Requirements

---

**Need help?** Open an issue on GitHub!
