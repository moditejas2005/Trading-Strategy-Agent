"""
Technical Indicators Module
Calculates RSI, MACD, and Moving Averages
"""
import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TechnicalIndicators:
    """
    Calculate technical indicators for trading analysis
    """
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize TechnicalIndicators
        
        Args:
            data: DataFrame with OHLCV data
        """
        self.data = data.copy()
        self.indicators = {}
    
    def calculate_rsi(self, period: int = 14) -> pd.Series:
        """
        Calculate Relative Strength Index (RSI)
        
        Args:
            period: RSI period (default: 14)
            
        Returns:
            Series with RSI values
        """
        try:
            delta = self.data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            self.indicators['RSI'] = rsi
            logger.info(f"RSI calculated with period={period}")
            return rsi
            
        except Exception as e:
            logger.error(f"Error calculating RSI: {str(e)}")
            return pd.Series()
    
    def calculate_macd(self, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        Calculate MACD (Moving Average Convergence Divergence)
        
        Args:
            fast: Fast EMA period (default: 12)
            slow: Slow EMA period (default: 26)
            signal: Signal line period (default: 9)
            
        Returns:
            Tuple of (MACD line, Signal line, Histogram)
        """
        try:
            exp1 = self.data['Close'].ewm(span=fast, adjust=False).mean()
            exp2 = self.data['Close'].ewm(span=slow, adjust=False).mean()
            
            macd = exp1 - exp2
            signal_line = macd.ewm(span=signal, adjust=False).mean()
            histogram = macd - signal_line
            
            self.indicators['MACD'] = macd
            self.indicators['MACD_Signal'] = signal_line
            self.indicators['MACD_Histogram'] = histogram
            
            logger.info(f"MACD calculated with fast={fast}, slow={slow}, signal={signal}")
            return macd, signal_line, histogram
            
        except Exception as e:
            logger.error(f"Error calculating MACD: {str(e)}")
            return pd.Series(), pd.Series(), pd.Series()
    
    def calculate_moving_averages(self, short_period: int = 20, long_period: int = 50) -> Tuple[pd.Series, pd.Series]:
        """
        Calculate Simple Moving Averages (SMA)
        
        Args:
            short_period: Short-term MA period (default: 20)
            long_period: Long-term MA period (default: 50)
            
        Returns:
            Tuple of (Short MA, Long MA)
        """
        try:
            sma_short = self.data['Close'].rolling(window=short_period).mean()
            sma_long = self.data['Close'].rolling(window=long_period).mean()
            
            self.indicators['SMA_Short'] = sma_short
            self.indicators['SMA_Long'] = sma_long
            
            logger.info(f"Moving Averages calculated: short={short_period}, long={long_period}")
            return sma_short, sma_long
            
        except Exception as e:
            logger.error(f"Error calculating Moving Averages: {str(e)}")
            return pd.Series(), pd.Series()
    
    def calculate_bollinger_bands(self, period: int = 20, std_dev: int = 2) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        Calculate Bollinger Bands
        
        Args:
            period: Period for SMA (default: 20)
            std_dev: Standard deviation multiplier (default: 2)
            
        Returns:
            Tuple of (Upper band, Middle band, Lower band)
        """
        try:
            middle = self.data['Close'].rolling(window=period).mean()
            std = self.data['Close'].rolling(window=period).std()
            
            upper = middle + (std * std_dev)
            lower = middle - (std * std_dev)
            
            self.indicators['BB_Upper'] = upper
            self.indicators['BB_Middle'] = middle
            self.indicators['BB_Lower'] = lower
            
            logger.info(f"Bollinger Bands calculated with period={period}, std_dev={std_dev}")
            return upper, middle, lower
            
        except Exception as e:
            logger.error(f"Error calculating Bollinger Bands: {str(e)}")
            return pd.Series(), pd.Series(), pd.Series()
    
    def calculate_all_indicators(self) -> Dict[str, pd.Series]:
        """
        Calculate all technical indicators
        
        Returns:
            Dictionary with all calculated indicators
        """
        self.calculate_rsi()
        self.calculate_macd()
        self.calculate_moving_averages()
        self.calculate_bollinger_bands()
        
        return self.indicators
    
    def get_latest_signals(self) -> Dict[str, Any]:
        """
        Get latest indicator values and trading signals
        
        Returns:
            Dictionary with latest signals
        """
        if not self.indicators:
            self.calculate_all_indicators()
        
        latest = {}
        for name, series in self.indicators.items():
            if not series.empty:
                latest[name] = float(series.iloc[-1])
        
        # Generate trading signals
        signals = {
            'indicators': latest,
            'signals': {}
        }
        
        # RSI Signals
        if 'RSI' in latest:
            rsi = latest['RSI']
            if rsi < 30:
                signals['signals']['RSI'] = 'OVERSOLD (Buy Signal)'
            elif rsi > 70:
                signals['signals']['RSI'] = 'OVERBOUGHT (Sell Signal)'
            else:
                signals['signals']['RSI'] = 'NEUTRAL'
        
        # MACD Signals
        if 'MACD' in latest and 'MACD_Signal' in latest:
            if latest['MACD'] > latest['MACD_Signal']:
                signals['signals']['MACD'] = 'BULLISH (Buy Signal)'
            else:
                signals['signals']['MACD'] = 'BEARISH (Sell Signal)'
        
        # MA Crossover Signals
        if 'SMA_Short' in latest and 'SMA_Long' in latest:
            if latest['SMA_Short'] > latest['SMA_Long']:
                signals['signals']['MA_Crossover'] = 'BULLISH (Buy Signal)'
            else:
                signals['signals']['MA_Crossover'] = 'BEARISH (Sell Signal)'
        
        return signals


if __name__ == "__main__":
    # Example usage with sample data
    from modules.data_collector import DataCollector
    
    collector = DataCollector(symbol='AAPL', period='3mo', interval='1d')
    data = collector.fetch_data()
    
    if data is not None:
        indicators = TechnicalIndicators(data)
        signals = indicators.get_latest_signals()
        
        print("\nLatest Indicator Values:")
        for name, value in signals['indicators'].items():
            print(f"{name}: {value:.2f}")
        
        print("\nTrading Signals:")
        for name, signal in signals['signals'].items():
            print(f"{name}: {signal}")
