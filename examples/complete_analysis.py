"""
Complete Example: Analyze Stock and Run Backtest
"""
from modules.data_collector import DataCollector
from modules.indicators import TechnicalIndicators
from modules.strategy_generator import StrategyGenerator
from modules.backtester import Backtester


def main():
    # Configuration
    SYMBOL = 'AAPL'
    PERIOD = '6mo'
    INITIAL_CAPITAL = 10000
    
    print("=" * 70)
    print("AI Trading Strategy Agent - Complete Example")
    print("=" * 70)
    
    # Step 1: Fetch Market Data
    print(f"\n📊 Step 1: Fetching market data for {SYMBOL}...")
    collector = DataCollector(symbol=SYMBOL, period=PERIOD, interval='1d')
    data = collector.fetch_data()
    
    if data is None:
        print("❌ Failed to fetch market data")
        return
    
    print(f"✅ Fetched {len(data)} records")
    print(f"   Latest Price: ₹{collector.get_latest_price():.2f}")
    
    # Step 2: Calculate Technical Indicators
    print(f"\n📈 Step 2: Calculating technical indicators...")
    indicators = TechnicalIndicators(data)
    all_indicators = indicators.calculate_all_indicators()
    signals = indicators.get_latest_signals()
    
    print("✅ Indicators calculated:")
    for name, value in signals['indicators'].items():
        print(f"   {name}: {value:.2f}")
    
    print("\n🎯 Trading Signals:")
    for name, signal in signals['signals'].items():
        print(f"   {name}: {signal}")
    
    # Step 3: Generate AI Strategy
    print(f"\n🤖 Step 3: Generating AI trading strategy...")
    generator = StrategyGenerator(use_optimization=True)
    
    ticker_info = collector.get_ticker_info()
    market_data = {
        'current_price': collector.get_latest_price(),
        'high_52w': ticker_info.get('fiftyTwoWeekHigh', 0),
        'low_52w': ticker_info.get('fiftyTwoWeekLow', 0)
    }
    
    strategy_result = generator.generate_strategy(
        symbol=SYMBOL,
        indicators=signals['indicators'],
        market_data=market_data
    )
    
    strategy = strategy_result['strategy']
    print(f"✅ Strategy Generated:")
    print(f"   📍 Action: {strategy['action']}")
    print(f"   📊 Confidence: {strategy['confidence']}/10")
    print(f"   📋 Outlook: {strategy['market_outlook']}")
    print(f"   💡 Entry: {strategy['entry_strategy']}")
    
    # Optimization info
    if strategy_result['prompt'].get('optimization'):
        opt = strategy_result['prompt']['optimization']
        print(f"\n⚡ Prompt Optimization:")
        print(f"   Original Tokens: {opt['original_tokens']}")
        print(f"   Optimized Tokens: {opt['optimized_tokens']}")
        print(f"   Reduction: {opt['reduction_percentage']:.1f}%")
    
    # Step 4: Run Backtest
    print(f"\n🔄 Step 4: Running backtest (${INITIAL_CAPITAL:,.0f} initial capital)...")
    
    # Add indicators to data
    for name, series in all_indicators.items():
        data[name] = series
    
    backtester = Backtester(data, initial_capital=INITIAL_CAPITAL)
    backtest_results = backtester.run_backtest(strategy_type='combined')
    
    print("✅ Backtest Complete:")
    print(f"   💵 Initial Capital: ${backtest_results['initial_capital']:,.2f}")
    print(f"   💰 Final Value: ${backtest_results['final_value']:,.2f}")
    print(f"   📈 Total Return: ${backtest_results['total_return']:,.2f} ({backtest_results['total_return_pct']:.2f}%)")
    print(f"   🎯 Win Rate: {backtest_results['win_rate']:.2f}%")
    print(f"   📊 Total Trades: {backtest_results['total_trades']}")
    print(f"   📉 Max Drawdown: {backtest_results['max_drawdown']:.2f}%")
    print(f"   💎 Sharpe Ratio: {backtest_results['sharpe_ratio']:.2f}")
    
    # Step 5: Summary
    print("\n" + "=" * 70)
    print("📋 SUMMARY")
    print("=" * 70)
    print(f"Symbol: {SYMBOL}")
    print(f"Recommended Action: {strategy['action']}")
    print(f"Strategy Confidence: {strategy['confidence']}/10")
    print(f"Backtest Return: {backtest_results['total_return_pct']:.2f}%")
    print(f"Historical Win Rate: {backtest_results['win_rate']:.2f}%")
    print("=" * 70)


if __name__ == "__main__":
    main()
