"""
Example: Compare Multiple Stocks
"""
from modules.data_collector import DataCollector
from modules.indicators import TechnicalIndicators
from modules.strategy_generator import StrategyGenerator


def analyze_stock(symbol: str, period: str = '3mo'):
    """Analyze a single stock"""
    # Fetch data
    collector = DataCollector(symbol=symbol, period=period)
    data = collector.fetch_data()
    
    if data is None:
        return None
    
    # Calculate indicators
    indicators = TechnicalIndicators(data)
    indicators.calculate_all_indicators()
    signals = indicators.get_latest_signals()
    
    # Generate strategy
    generator = StrategyGenerator(use_optimization=False)
    ticker_info = collector.get_ticker_info()
    
    market_data = {
        'current_price': collector.get_latest_price(),
        'high_52w': ticker_info.get('fiftyTwoWeekHigh', 0),
        'low_52w': ticker_info.get('fiftyTwoWeekLow', 0)
    }
    
    strategy_result = generator.generate_strategy(
        symbol=symbol,
        indicators=signals['indicators'],
        market_data=market_data
    )
    
    return {
        'symbol': symbol,
        'price': collector.get_latest_price(),
        'action': strategy_result['strategy']['action'],
        'confidence': strategy_result['strategy']['confidence'],
        'rsi': signals['indicators'].get('RSI', 0),
        'signals': signals['signals']
    }


def main():
    # Stocks to compare
    STOCKS = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN']
    
    print("=" * 90)
    print("MULTI-STOCK COMPARISON")
    print("=" * 90)
    
    results = []
    for symbol in STOCKS:
        print(f"\nAnalyzing {symbol}...")
        result = analyze_stock(symbol)
        if result:
            results.append(result)
            print(f"✅ {symbol}: {result['action']} (Confidence: {result['confidence']}/10)")
    
    # Display results table
    print("\n" + "=" * 90)
    print(f"{'Symbol':<10} {'Price':<12} {'Action':<10} {'Confidence':<12} {'RSI':<10}")
    print("-" * 90)
    
    for result in results:
        print(f"{result['symbol']:<10} ${result['price']:<11.2f} {result['action']:<10} "
              f"{result['confidence']:<12.1f} {result['rsi']:<10.2f}")
    
    # Show top recommendations
    print("\n" + "=" * 90)
    print("TOP BUY RECOMMENDATIONS")
    print("=" * 90)
    
    buy_stocks = [r for r in results if r['action'] == 'BUY']
    buy_stocks.sort(key=lambda x: x['confidence'], reverse=True)
    
    for i, stock in enumerate(buy_stocks[:3], 1):
        print(f"{i}. {stock['symbol']} - Confidence: {stock['confidence']}/10")
        print(f"   Signals: {stock['signals']}")


if __name__ == "__main__":
    main()
