// AI Trading Strategy Agent Frontend JavaScript
const API_BASE = 'http://localhost:5000/api';

let currentData = null;

async function analyzeStock() {
    const symbol = document.getElementById('symbol').value;
    const period = document.getElementById('period').value;

    if (!symbol) {
        alert('Please enter a stock symbol');
        return;
    }

    showLoading(true);
    hideResults();

    try {
        // Fetch market data and indicators
        const [marketData, indicators] = await Promise.all([
            fetch(`${API_BASE}/market-data?symbol=${symbol}&period=${period}`).then(r => r.json()),
            fetch(`${API_BASE}/indicators?symbol=${symbol}&period=${period}`).then(r => r.json())
        ]);

        if (marketData.error || indicators.error) {
            throw new Error(marketData.error || indicators.error);
        }

        // Generate strategy
        const strategyResponse = await fetch(`${API_BASE}/strategy`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ symbol, period, use_optimization: true })
        });
        const strategy = await strategyResponse.json();

        currentData = { marketData, indicators, strategy };

        displayResults(currentData);
        showLoading(false);
        showResults();
    } catch (error) {
        showLoading(false);
        alert(`Error: ${error.message}`);
    }
}

async function runBacktest() {
    if (!currentData) {
        alert('Please analyze a stock first');
        return;
    }

    const symbol = document.getElementById('symbol').value.toUpperCase();
    const period = document.getElementById('period').value;

    showLoading(true);

    try {
        const response = await fetch(`${API_BASE}/backtest`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                symbol,
                period,
                strategy_type: 'combined',
                initial_capital: 10000
            })
        });

        const backtestData = await response.json();

        if (backtestData.error) {
            throw new Error(backtestData.error);
        }

        displayBacktestResults(backtestData);
        showLoading(false);
    } catch (error) {
        showLoading(false);
        alert(`Backtest Error: ${error.message}`);
    }
}

function displayResults(data) {
    const { marketData, indicators, strategy } = data;

    // Display Market Info
    const marketInfo = marketData.ticker_info;
    document.getElementById('marketInfo').innerHTML = `
        <div class="info-grid">
            <div class="info-item">
                <label>Company</label>
                <div class="value">${marketInfo.name}</div>
            </div>
            <div class="info-item">
                <label>Current Price</label>
                <div class="value">₹${marketInfo.currentPrice.toFixed(2)}</div>
            </div>
            <div class="info-item">
                <label>52-Week High</label>
                <div class="value">₹${marketInfo.fiftyTwoWeekHigh.toFixed(2)}</div>
            </div>
            <div class="info-item">
                <label>52-Week Low</label>
                <div class="value">₹${marketInfo.fiftyTwoWeekLow.toFixed(2)}</div>
            </div>
            <div class="info-item">
                <label>Sector</label>
                <div class="value">${marketInfo.sector}</div>
            </div>
            <div class="info-item">
                <label>Industry</label>
                <div class="value">${marketInfo.industry}</div>
            </div>
        </div>
    `;

    // Display Indicators
    const ind = indicators.indicators;
    const sig = indicators.signals;
    document.getElementById('indicators').innerHTML = `
        <div class="info-grid">
            <div class="info-item">
                <label>RSI</label>
                <div class="value">${ind.RSI.toFixed(2)}</div>
                <span class="signal ${getSignalClass(sig.RSI)}">${sig.RSI}</span>
            </div>
            <div class="info-item">
                <label>MACD</label>
                <div class="value">${ind.MACD.toFixed(2)}</div>
                <span class="signal ${getSignalClass(sig.MACD)}">${sig.MACD}</span>
            </div>
            <div class="info-item">
                <label>MA Crossover</label>
                <div class="value">SMA ${ind.SMA_Short.toFixed(2)} / ${ind.SMA_Long.toFixed(2)}</div>
                <span class="signal ${getSignalClass(sig.MA_Crossover)}">${sig.MA_Crossover}</span>
            </div>
        </div>
    `;

    // Display Strategy
    const strat = strategy.strategy;
    document.getElementById('strategy').innerHTML = `
        <div class="strategy-content">
            <div style="text-align: center; margin-bottom: 20px;">
                <h3 style="font-size: 2rem; margin-bottom: 10px;">
                    <span class="signal ${strat.action.toLowerCase()}">${strat.action}</span>
                </h3>
                <p style="color: var(--text-secondary);">Confidence: ${strat.confidence}/10</p>
            </div>
            <div class="metric">
                <span class="metric-label">Market Outlook</span>
                <span class="metric-value">${strat.market_outlook}</span>
            </div>
            <div class="metric">
                <span class="metric-label">Entry Strategy</span>
                <span class="metric-value">${strat.entry_strategy}</span>
            </div>
            <div class="metric">
                <span class="metric-label">Risk Management</span>
                <span class="metric-value">${strat.risk_management}</span>
            </div>
            <div class="metric">
                <span class="metric-label">Time Horizon</span>
                <span class="metric-value">${strat.time_horizon}</span>
            </div>
        </div>
    `;

    // Display Chart
    plotPriceChart(marketData.data);
}

function displayBacktestResults(backtestData) {
    const results = backtestData.results;

    document.getElementById('backtestData').innerHTML = `
        <div class="info-grid">
            <div class="info-item">
                <label>Initial Capital</label>
                <div class="value">₹${results.initial_capital.toLocaleString()}</div>
            </div>
            <div class="info-item">
                <label>Final Value</label>
                <div class="value">₹${results.final_value.toLocaleString()}</div>
            </div>
            <div class="info-item">
                <label>Total Return</label>
                <div class="value ${results.total_return >= 0 ? 'positive' : 'negative'}">
                    ${results.total_return >= 0 ? '+' : ''}₹${results.total_return.toFixed(2)} 
                    (${results.total_return_pct.toFixed(2)}%)
                </div>
            </div>
            <div class="info-item">
                <label>Win Rate</label>
                <div class="value">${results.win_rate.toFixed(2)}%</div>
            </div>
            <div class="info-item">
                <label>Total Trades</label>
                <div class="value">${results.total_trades}</div>
            </div>
            <div class="info-item">
                <label>Max Drawdown</label>
                <div class="value negative">${results.max_drawdown.toFixed(2)}%</div>
            </div>
        </div>
    `;

    plotPortfolioChart(backtestData.portfolio_history);
    document.getElementById('backtestResults').style.display = 'block';
}

function plotPriceChart(data) {
    const dates = data.map(d => d.Date);
    const closes = data.map(d => d.Close);

    const trace = {
        x: dates,
        y: closes,
        type: 'scatter',
        mode: 'lines',
        name: 'Close Price',
        line: { color: '#2563eb', width: 2 }
    };

    const layout = {
        title: 'Price History',
        paper_bgcolor: '#1e293b',
        plot_bgcolor: '#0f172a',
        font: { color: '#f1f5f9' },
        xaxis: { gridcolor: '#334155' },
        yaxis: { gridcolor: '#334155', title: 'Price (₹)' }
    };

    Plotly.newPlot('chart', [trace], layout, { responsive: true });
}

function plotPortfolioChart(data) {
    const dates = data.map(d => d.date);
    const values = data.map(d => d.value);

    const trace = {
        x: dates,
        y: values,
        type: 'scatter',
        mode: 'lines',
        fill: 'tozeroy',
        name: 'Portfolio Value',
        line: { color: '#10b981', width: 2 }
    };

    const layout = {
        title: 'Portfolio Value Over Time',
        paper_bgcolor: '#1e293b',
        plot_bgcolor: '#0f172a',
        font: { color: '#f1f5f9' },
        xaxis: { gridcolor: '#334155' },
        yaxis: { gridcolor: '#334155', title: 'Value ($)' }
    };

    Plotly.newPlot('portfolioChart', [trace], layout, { responsive: true });
}

function getSignalClass(signal) {
    if (signal.includes('Buy') || signal.includes('BULLISH')) return 'buy';
    if (signal.includes('Sell') || signal.includes('BEARISH')) return 'sell';
    return 'neutral';
}

function showLoading(show) {
    document.getElementById('loading').style.display = show ? 'block' : 'none';
}

function showResults() {
    document.getElementById('results').style.display = 'block';
}

function hideResults() {
    document.getElementById('results').style.display = 'none';
}
