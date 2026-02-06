"""
Unit tests for Trading Strategy Agent modules
"""
import pytest
import pandas as pd
from modules.data_collector import DataCollector
from modules.indicators import TechnicalIndicators
from modules.strategy_generator import StrategyGenerator
from modules.prompt_optimizer import PromptOptimizer
from modules.backtester import Backtester


class TestDataCollector:
    """Test DataCollector module"""
    
    def test_initialization(self):
        """Test DataCollector initialization"""
        collector = DataCollector(symbol='AAPL', period='1mo')
        assert collector.symbol == 'AAPL'
        assert collector.period == '1mo'
    
    def test_fetch_data(self):
        """Test data fetching"""
        collector = DataCollector(symbol='AAPL', period='5d')
        data = collector.fetch_data()
        assert data is not None
        assert isinstance(data, pd.DataFrame)
        assert 'Close' in data.columns
    
    def test_get_latest_price(self):
        """Test latest price retrieval"""
        collector = DataCollector(symbol='AAPL', period='5d')
        price = collector.get_latest_price()
        assert price is not None
        assert isinstance(price, float)
        assert price > 0


class TestTechnicalIndicators:
    """Test TechnicalIndicators module"""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing"""
        collector = DataCollector(symbol='AAPL', period='3mo')
        return collector.fetch_data()
    
    def test_rsi_calculation(self, sample_data):
        """Test RSI calculation"""
        indicators = TechnicalIndicators(sample_data)
        rsi = indicators.calculate_rsi()
        assert not rsi.empty
        assert rsi.max() <= 100
        assert rsi.min() >= 0
    
    def test_macd_calculation(self, sample_data):
        """Test MACD calculation"""
        indicators = TechnicalIndicators(sample_data)
        macd, signal, hist = indicators.calculate_macd()
        assert not macd.empty
        assert not signal.empty
        assert not hist.empty
    
    def test_moving_averages(self, sample_data):
        """Test Moving Average calculation"""
        indicators = TechnicalIndicators(sample_data)
        sma_short, sma_long = indicators.calculate_moving_averages()
        assert not sma_short.empty
        assert not sma_long.empty
    
    def test_get_latest_signals(self, sample_data):
        """Test signal generation"""
        indicators = TechnicalIndicators(sample_data)
        signals = indicators.get_latest_signals()
        assert 'indicators' in signals
        assert 'signals' in signals


class TestPromptOptimizer:
    """Test PromptOptimizer module"""
    
    def test_initialization(self):
        """Test optimizer initialization"""
        optimizer = PromptOptimizer()
        assert optimizer is not None
    
    def test_optimize_prompt(self):
        """Test prompt optimization"""
        optimizer = PromptOptimizer()
        result = optimizer.optimize_prompt("Test prompt for optimization")
        assert 'original_prompt' in result
        assert 'optimized_prompt' in result
        assert 'reduction_percentage' in result


class TestStrategyGenerator:
    """Test StrategyGenerator module"""
    
    def test_initialization(self):
        """Test generator initialization"""
        generator = StrategyGenerator()
        assert generator is not None
    
    def test_create_analysis_prompt(self):
        """Test prompt creation"""
        generator = StrategyGenerator()
        indicators = {'RSI': 45.5, 'MACD': 2.3, 'MACD_Signal': 1.8}
        market_data = {'current_price': 150.0, 'high_52w': 180.0, 'low_52w': 120.0}
        
        prompt = generator.create_analysis_prompt('AAPL', indicators, market_data)
        assert 'AAPL' in prompt
        assert 'RSI' in prompt
    
    def test_generate_strategy(self):
        """Test strategy generation"""
        generator = StrategyGenerator(use_optimization=False)
        indicators = {'RSI': 45.5, 'MACD': 2.3, 'MACD_Signal': 1.8, 
                     'SMA_Short': 150.0, 'SMA_Long': 145.0}
        market_data = {'current_price': 150.0, 'high_52w': 180.0, 'low_52w': 120.0}
        
        result = generator.generate_strategy('AAPL', indicators, market_data)
        assert 'symbol' in result
        assert 'strategy' in result
        assert 'action' in result['strategy']


class TestBacktester:
    """Test Backtester module"""
    
    @pytest.fixture
    def sample_data_with_indicators(self):
        """Create sample data with indicators"""
        collector = DataCollector(symbol='AAPL', period='6mo')
        data = collector.fetch_data()
        
        indicators = TechnicalIndicators(data)
        indicators.calculate_all_indicators()
        
        for name, series in indicators.indicators.items():
            data[name] = series
        
        return data
    
    def test_initialization(self, sample_data_with_indicators):
        """Test backtester initialization"""
        backtester = Backtester(sample_data_with_indicators, initial_capital=10000)
        assert backtester.initial_capital == 10000
    
    def test_generate_signals(self, sample_data_with_indicators):
        """Test signal generation"""
        backtester = Backtester(sample_data_with_indicators)
        df = backtester.generate_signals(strategy_type='rsi_macd')
        assert 'signal' in df.columns
    
    def test_run_backtest(self, sample_data_with_indicators):
        """Test backtest execution"""
        backtester = Backtester(sample_data_with_indicators, initial_capital=10000)
        results = backtester.run_backtest(strategy_type='combined')
        
        assert 'initial_capital' in results
        assert 'final_value' in results
        assert 'total_return' in results
        assert 'win_rate' in results
        assert results['initial_capital'] == 10000


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
