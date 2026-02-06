# PostgreSQL Database Setup Guide

## Prerequisites
- PostgreSQL 12+ installed
- Database credentials configured in `.env`

## Quick Setup

### 1. Install PostgreSQL
**Windows:**
```bash
# Download from: https://www.postgresql.org/download/windows/
# Or use chocolatey:
choco install postgresql
```

**Mac:**
```bash
brew install postgresql
brew services start postgresql
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### 2. Create Database

```bash
# Login to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE trading_agent;

# Create user (optional)
CREATE USER trading_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE trading_agent TO trading_user;

# Exit
\q
```

### 3. Update .env File

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password_here
POSTGRES_DATABASE=trading_agent
```

### 4. Initialize Database Tables

**Option A: Using Python**
```bash
python database.py
```

**Option B: Using SQL**
```bash
psql -U postgres -d trading_agent -f schema.sql
```

## Database Schema

### Tables Created:
1. **trading_strategies** - AI-generated trading strategies
2. **backtest_results** - Historical backtest performance
3. **market_data** - Cached market data
4. **prompt_optimizations** - Optimization metrics

## Verify Installation

```bash
# Connect to database
psql -U postgres -d trading_agent

# List tables
\dt

# Query example
SELECT COUNT(*) FROM trading_strategies;
```

## Connection String

Your app uses this connection string:
```
postgresql://postgres:password@localhost:5432/trading_agent
```

## Troubleshooting

**Connection refused:**
- Ensure PostgreSQL service is running
- Check firewall settings
- Verify credentials in `.env`

**Permission denied:**
- Grant proper privileges to user
- Check pg_hba.conf settings

**Tables not created:**
- Run `python database.py` to create tables
- Or manually execute `schema.sql`

## Production Notes

For production deployment:
1. Use strong passwords
2. Enable SSL connections
3. Set up regular backups
4. Configure connection pooling
5. Use environment variables (never commit passwords)

## Next Steps

After setup:
1. Start the Flask app: `python app.py`
2. Strategies and backtests will automatically save to PostgreSQL
3. View data: `SELECT * FROM trading_strategies LIMIT 10;`
