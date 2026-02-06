"""
Alpha Vantage Data Collector Module
Alternative data source for market data
"""
import requests
import pandas as pd
from typing import Optional, Dict, Any
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AlphaVantageCollector:
    """
    Collect stock data using Alpha Vantage API
    """
    
    def __init__(self, api_key: str, symbol: str = 'AAPL'):
        """
        Initialize AlphaVantageCollector
        
        Args:
            api_key: Alpha Vantage API key
            symbol: Stock ticker symbol
        """
        self.api_key = api_key
        self.symbol = symbol.upper()
        self.base_url = "https://www.alphavantage.co/query"
        self.data = None
    
    def fetch_intraday_data(self, interval: str = '5min') -> Optional[pd.DataFrame]:
        """
        Fetch intraday stock data
        
        Args:
            interval: Time interval ('1min', '5min', '15min', '30min', '60min')
            
        Returns:
            DataFrame with intraday data
        """
        try:
            params = {
                'function': 'TIME_SERIES_INTRADAY',
                'symbol': self.symbol,
                'interval': interval,
                'apikey': self.api_key,
                'outputsize': 'full'
            }
            
            logger.info(f"Fetching intraday data for {self.symbol} ({interval})...")
            response = requests.get(self.base_url, params=params, timeout=30)
            data = response.json()
            
            # Check for errors
            if 'Error Message' in data:
                logger.error(f"API Error: {data['Error Message']}")
                return None
            
            if 'Note' in data:
                logger.warning(f"API Rate Limit: {data['Note']}")
                return None
            
            # Parse time series data
            time_series_key = f'Time Series ({interval})'
            if time_series_key not in data:
                logger.error("No time series data found in response")
                return None
            
            time_series = data[time_series_key]
            
            # Convert to DataFrame
            df = pd.DataFrame.from_dict(time_series, orient='index')
            df.index = pd.to_datetime(df.index)
            df = df.sort_index()
            
            # Rename columns
            df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            
            # Convert to numeric
            for col in df.columns:
                df[col] = pd.to_numeric(df[col])
            
            self.data = df
            logger.info(f"Successfully fetched {len(df)} intraday records")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching intraday data: {str(e)}")
            return None
    
    def fetch_daily_data(self, outputsize: str = 'full') -> Optional[pd.DataFrame]:
        """
        Fetch daily stock data
        
        Args:
            outputsize: 'compact' (100 days) or 'full' (20+ years)
            
        Returns:
            DataFrame with daily data
        """
        try:
            params = {
                'function': 'TIME_SERIES_DAILY',
                'symbol': self.symbol,
                'apikey': self.api_key,
                'outputsize': outputsize
            }
            
            logger.info(f"Fetching daily data for {self.symbol}...")
            response = requests.get(self.base_url, params=params, timeout=30)
            data = response.json()
            
            # Check for errors
            if 'Error Message' in data:
                logger.error(f"API Error: {data['Error Message']}")
                return None
            
            if 'Note' in data:
                logger.warning(f"API Rate Limit: {data['Note']}")
                return None
            
            # Parse time series data
            if 'Time Series (Daily)' not in data:
                logger.error("No daily data found in response")
                return None
            
            time_series = data['Time Series (Daily)']
            
            # Convert to DataFrame
            df = pd.DataFrame.from_dict(time_series, orient='index')
            df.index = pd.to_datetime(df.index)
            df = df.sort_index()
            
            # Rename columns
            df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            
            # Convert to numeric
            for col in df.columns:
                df[col] = pd.to_numeric(df[col])
            
            self.data = df
            logger.info(f"Successfully fetched {len(df)} daily records")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching daily data: {str(e)}")
            return None
    
    def get_quote(self) -> Dict[str, Any]:
        """
        Get real-time quote data
        
        Returns:
            Dictionary with quote information
        """
        try:
            params = {
                'function': 'GLOBAL_QUOTE',
                'symbol': self.symbol,
                'apikey': self.api_key
            }
            
            logger.info(f"Fetching quote for {self.symbol}...")
            response = requests.get(self.base_url, params=params, timeout=30)
            data = response.json()
            
            if 'Global Quote' not in data:
                logger.error("No quote data found")
                return {}
            
            quote = data['Global Quote']
            
            return {
                'symbol': quote.get('01. symbol', self.symbol),
                'open': float(quote.get('02. open', 0)),
                'high': float(quote.get('03. high', 0)),
                'low': float(quote.get('04. low', 0)),
                'price': float(quote.get('05. price', 0)),
                'volume': int(quote.get('06. volume', 0)),
                'latest_trading_day': quote.get('07. latest trading day', ''),
                'previous_close': float(quote.get('08. previous close', 0)),
                'change': float(quote.get('09. change', 0)),
                'change_percent': quote.get('10. change percent', '0%').rstrip('%'),
            }
            
        except Exception as e:
            logger.error(f"Error fetching quote: {str(e)}")
            return {}
    
    def get_company_overview(self) -> Dict[str, Any]:
        """
        Get company fundamental data
        
        Returns:
            Dictionary with company information
        """
        try:
            params = {
                'function': 'OVERVIEW',
                'symbol': self.symbol,
                'apikey': self.api_key
            }
            
            logger.info(f"Fetching company overview for {self.symbol}...")
            response = requests.get(self.base_url, params=params, timeout=30)
            data = response.json()
            
            if not data or 'Symbol' not in data:
                logger.error("No company data found")
                return {}
            
            return {
                'symbol': data.get('Symbol', self.symbol),
                'name': data.get('Name', 'N/A'),
                'description': data.get('Description', 'N/A'),
                'sector': data.get('Sector', 'N/A'),
                'industry': data.get('Industry', 'N/A'),
                'market_cap': data.get('MarketCapitalization', 'N/A'),
                'pe_ratio': data.get('PERatio', 'N/A'),
                'dividend_yield': data.get('DividendYield', 'N/A'),
                '52_week_high': data.get('52WeekHigh', 'N/A'),
                '52_week_low': data.get('52WeekLow', 'N/A'),
            }
            
        except Exception as e:
            logger.error(f"Error fetching company overview: {str(e)}")
            return {}


if __name__ == "__main__":
    # Example usage
    collector = AlphaVantageCollector(api_key='8MZEFUFMBSNMQWA9', symbol='AAPL')
    
    # Get real-time quote
    quote = collector.get_quote()
    if quote:
        print("\n📊 Real-time Quote:")
        print(f"Price: ${quote['price']:.2f}")
        print(f"Change: {quote['change']:.2f} ({quote['change_percent']}%)")
        print(f"Volume: {quote['volume']:,}")
    
    # Get company overview
    overview = collector.get_company_overview()
    if overview:
        print(f"\n🏢 Company: {overview['name']}")
        print(f"Sector: {overview['sector']}")
        print(f"Industry: {overview['industry']}")
    
    # Fetch daily data
    daily_data = collector.fetch_daily_data(outputsize='compact')
    if daily_data is not None:
        print(f"\n📈 Daily Data: {len(daily_data)} records")
        print(daily_data.tail())
