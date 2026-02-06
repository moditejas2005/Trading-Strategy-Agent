"""
Data Collection Module
Fetches financial market data from APIs
"""
import yfinance as yf
import pandas as pd
from typing import Optional, Dict, Any
import logging
from modules.currency_converter import get_converter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataCollector:
    """
    Collects stock and cryptocurrency data from financial APIs
    """
    
    def __init__(self, symbol: str = 'AAPL', period: str = '1y', interval: str = '1d'):
        """
        Initialize DataCollector
        
        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL', 'GOOGL')
            period: Data period ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
            interval: Data interval ('1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo')
        """
        self.symbol = symbol
        self.period = period
        self.interval = interval
        self.data = None
        
    def fetch_data(self) -> Optional[pd.DataFrame]:
        """
        Fetch historical market data with retry logic
        
        Returns:
            DataFrame with OHLCV data or None if fetch fails
        """
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                logger.info(f"Fetching data for {self.symbol} (attempt {retry_count + 1}/{max_retries})...")
                
                # Create ticker with enhanced settings
                ticker = yf.Ticker(self.symbol)
                
                # Try to fetch data
                self.data = ticker.history(
                    period=self.period, 
                    interval=self.interval,
                    auto_adjust=True,
                    actions=False
                )
                
                if self.data is not None and not self.data.empty:
                    # Remove timezone information if present
                    if self.data.index.tz is not None:
                        self.data.index = self.data.index.tz_localize(None)
                    
                    # Convert USD prices to INR
                    converter = get_converter()
                    price_columns = ['Open', 'High', 'Low', 'Close']
                    for col in price_columns:
                        if col in self.data.columns:
                            self.data[col] = self.data[col].apply(converter.usd_to_inr)
                    
                    logger.info(f"Successfully fetched {len(self.data)} records for {self.symbol} (prices converted to INR)")
                    return self.data
                else:
                    logger.warning(f"No data found for {self.symbol} on attempt {retry_count + 1}")
                    retry_count += 1
                    
            except Exception as e:
                logger.error(f"Error fetching data for {self.symbol} (attempt {retry_count + 1}): {str(e)}")
                retry_count += 1
        
        # All retries failed
        logger.error(f"Failed to fetch data for {self.symbol} after {max_retries} attempts")
        return None
    
    def get_latest_price(self) -> Optional[float]:
        """
        Get the latest closing price
        
        Returns:
            Latest closing price or None
        """
        if self.data is None or self.data.empty:
            self.fetch_data()
        
        if self.data is not None and not self.data.empty:
            return float(self.data['Close'].iloc[-1])
        return None
    
    def get_ticker_info(self) -> Dict[str, Any]:
        """
        Get detailed ticker information
        
        Returns:
            Dictionary containing ticker info
        """
        try:
            ticker = yf.Ticker(self.symbol)
            info = ticker.info
            
            converter = get_converter()
            
            return {
                'symbol': self.symbol,
                'name': info.get('longName', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'marketCap': info.get('marketCap', 0),
                'currentPrice': converter.usd_to_inr(info.get('currentPrice', 0)),
                'fiftyTwoWeekHigh': converter.usd_to_inr(info.get('fiftyTwoWeekHigh', 0)),
                'fiftyTwoWeekLow': converter.usd_to_inr(info.get('fiftyTwoWeekLow', 0)),
            }
        except Exception as e:
            logger.error(f"Error getting ticker info: {str(e)}")
            return {}
    
    def get_data_summary(self) -> Dict[str, Any]:
        """
        Get summary statistics of the data
        
        Returns:
            Dictionary with data summary
        """
        if self.data is None or self.data.empty:
            self.fetch_data()
            
        if self.data is None or self.data.empty:
            return {}
        
        return {
            'symbol': self.symbol,
            'period': self.period,
            'interval': self.interval,
            'records': len(self.data),
            'start_date': str(self.data.index[0]),
            'end_date': str(self.data.index[-1]),
            'highest_price': float(self.data['High'].max()),
            'lowest_price': float(self.data['Low'].min()),
            'average_volume': float(self.data['Volume'].mean()),
        }


if __name__ == "__main__":
    # Example usage
    collector = DataCollector(symbol='AAPL', period='1mo', interval='1d')
    data = collector.fetch_data()
    
    if data is not None:
        print("\nData Summary:")
        print(collector.get_data_summary())
        
        print("\nTicker Info:")
        print(collector.get_ticker_info())
        
        print(f"\nLatest Price: ${collector.get_latest_price():.2f}")
