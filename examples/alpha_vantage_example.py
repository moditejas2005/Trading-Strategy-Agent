"""
Example: Use Alpha Vantage API
"""
from modules.alpha_vantage_collector import AlphaVantageCollector


def main():
    SYMBOL = 'AAPL'
    API_KEY = '8MZEFUFMBSNMQWA9'
    
    print("=" * 70)
    print(f"Alpha Vantage API Example - {SYMBOL}")
    print("=" * 70)
    
    # Initialize collector
    collector = AlphaVantageCollector(api_key=API_KEY, symbol=SYMBOL)
    
    # 1. Get Real-time Quote
    print("\n📊 Real-time Quote:")
    quote = collector.get_quote()
    if quote:
        print(f"   Symbol: {quote['symbol']}")
        print(f"   Price: ${quote['price']:.2f}")
        print(f"   Change: ${quote['change']:.2f} ({quote['change_percent']}%)")
        print(f"   Volume: {quote['volume']:,}")
        print(f"   High: ${quote['high']:.2f}")
        print(f"   Low: ${quote['low']:.2f}")
    
    # 2. Get Company Overview
    print("\n🏢 Company Overview:")
    overview = collector.get_company_overview()
    if overview:
        print(f"   Name: {overview['name']}")
        print(f"   Sector: {overview['sector']}")
        print(f"   Industry: {overview['industry']}")
        print(f"   Market Cap: {overview['market_cap']}")
        print(f"   P/E Ratio: {overview['pe_ratio']}")
        print(f"   52W High: ${overview['52_week_high']}")
        print(f"   52W Low: ${overview['52_week_low']}")
    
    # 3. Get Daily Data
    print("\n📈 Daily Historical Data (Last 5 Days):")
    daily_data = collector.fetch_daily_data(outputsize='compact')
    if daily_data is not None:
        print(daily_data.tail())
        print(f"\n   Total records: {len(daily_data)}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
