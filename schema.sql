-- Trading Strategy Agent Database Schema
-- PostgreSQL

-- Trading Strategies Table
CREATE TABLE IF NOT EXISTS trading_strategies (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    strategy_type VARCHAR(50),
    action VARCHAR(10),
    confidence FLOAT,
    indicators JSONB,
    market_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_strategies_symbol ON trading_strategies(symbol);
CREATE INDEX idx_strategies_created ON trading_strategies(created_at DESC);

-- Backtest Results Table
CREATE TABLE IF NOT EXISTS backtest_results (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    strategy_type VARCHAR(50),
    initial_capital FLOAT,
    final_value FLOAT,
    total_return FLOAT,
    total_return_pct FLOAT,
    total_trades INTEGER,
    win_rate FLOAT,
    max_drawdown FLOAT,
    sharpe_ratio FLOAT,
    backtest_period VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_backtest_symbol ON backtest_results(symbol);
CREATE INDEX idx_backtest_created ON backtest_results(created_at DESC);

-- Market Data Cache Table
CREATE TABLE IF NOT EXISTS market_data (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    date TIMESTAMP NOT NULL,
    open FLOAT,
    high FLOAT,
    low FLOAT,
    close FLOAT,
    volume BIGINT,
    source VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(symbol, date, source)
);

CREATE INDEX idx_market_symbol ON market_data(symbol);
CREATE INDEX idx_market_date ON market_data(date DESC);

-- Prompt Optimization History Table
CREATE TABLE IF NOT EXISTS prompt_optimizations (
    id SERIAL PRIMARY KEY,
    original_prompt TEXT,
    optimized_prompt TEXT,
    original_tokens INTEGER,
    optimized_tokens INTEGER,
    reduction_percentage FLOAT,
    cost_savings FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_optimization_created ON prompt_optimizations(created_at DESC);

-- Sample queries for analytics
COMMENT ON TABLE trading_strategies IS 'Stores AI-generated trading strategies';
COMMENT ON TABLE backtest_results IS 'Stores historical backtest performance results';
COMMENT ON TABLE market_data IS 'Caches market data from various sources';
COMMENT ON TABLE prompt_optimizations IS 'Tracks prompt optimization metrics and savings';
