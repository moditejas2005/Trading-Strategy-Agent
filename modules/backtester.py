"""
Backtesting Module
Evaluates trading strategy performance using historical data
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Backtester:
    """
    Backtest trading strategies on historical data
    """
    
    def __init__(self, data: pd.DataFrame, initial_capital: float = 10000.0):
        """
        Initialize Backtester
        
        Args:
            data: Historical OHLCV data with indicators
            initial_capital: Starting capital for backtesting
        """
        self.data = data.copy()
        self.initial_capital = initial_capital
        self.trades = []
        self.portfolio_value = []
    
    def generate_signals(self, strategy_type: str = 'rsi_macd') -> pd.DataFrame:
        """
        Generate buy/sell signals based on strategy
        
        Args:
            strategy_type: Type of strategy ('rsi_macd', 'ma_crossover', 'combined')
            
        Returns:
            DataFrame with signals
        """
        df = self.data.copy()
        df['signal'] = 0  # 0 = hold, 1 = buy, -1 = sell
        
        if strategy_type == 'rsi_macd':
            # RSI + MACD strategy
            df.loc[(df['RSI'] < 30) & (df['MACD'] > df['MACD_Signal']), 'signal'] = 1
            df.loc[(df['RSI'] > 70) & (df['MACD'] < df['MACD_Signal']), 'signal'] = -1
            
        elif strategy_type == 'ma_crossover':
            # Moving Average Crossover
            df.loc[df['SMA_Short'] > df['SMA_Long'], 'signal'] = 1
            df.loc[df['SMA_Short'] < df['SMA_Long'], 'signal'] = -1
            
        elif strategy_type == 'combined':
            # Combined strategy
            buy_conditions = (
                (df['RSI'] < 40) &
                (df['MACD'] > df['MACD_Signal']) &
                (df['SMA_Short'] > df['SMA_Long'])
            )
            sell_conditions = (
                (df['RSI'] > 60) &
                (df['MACD'] < df['MACD_Signal']) &
                (df['SMA_Short'] < df['SMA_Long'])
            )
            df.loc[buy_conditions, 'signal'] = 1
            df.loc[sell_conditions, 'signal'] = -1
        
        return df
    
    def run_backtest(self, 
                     strategy_type: str = 'rsi_macd',
                     commission: float = 0.001) -> Dict[str, Any]:
        """
        Run backtest simulation
        
        Args:
            strategy_type: Trading strategy to test
            commission: Trading commission (0.001 = 0.1%)
            
        Returns:
            Dictionary with backtest results
        """
        df = self.generate_signals(strategy_type)
        
        capital = self.initial_capital
        position = 0  # Number of shares held
        entry_price = 0
        self.trades = []
        self.portfolio_value = []
        
        for i in range(len(df)):
            row = df.iloc[i]
            current_price = row['Close']
            signal = row['signal']
            
            # Calculate current portfolio value
            portfolio_val = capital + (position * current_price)
            self.portfolio_value.append({
                'date': df.index[i],
                'value': portfolio_val
            })
            
            # Execute trades based on signals
            if signal == 1 and position == 0:  # Buy signal
                shares_to_buy = int(capital / current_price)
                if shares_to_buy > 0:
                    cost = shares_to_buy * current_price * (1 + commission)
                    if cost <= capital:
                        position = shares_to_buy
                        capital -= cost
                        entry_price = current_price
                        
                        self.trades.append({
                            'date': df.index[i],
                            'type': 'BUY',
                            'price': current_price,
                            'shares': shares_to_buy,
                            'commission': shares_to_buy * current_price * commission
                        })
                        logger.debug(f"BUY: {shares_to_buy} shares at ${current_price:.2f}")
            
            elif signal == -1 and position > 0:  # Sell signal
                proceeds = position * current_price * (1 - commission)
                capital += proceeds
                
                profit = (current_price - entry_price) * position
                profit_pct = ((current_price - entry_price) / entry_price) * 100
                
                self.trades.append({
                    'date': df.index[i],
                    'type': 'SELL',
                    'price': current_price,
                    'shares': position,
                    'commission': position * current_price * commission,
                    'profit': profit,
                    'profit_pct': profit_pct
                })
                logger.debug(f"SELL: {position} shares at ${current_price:.2f} (Profit: ${profit:.2f})")
                
                position = 0
                entry_price = 0
        
        # Close any remaining position
        if position > 0:
            final_price = df.iloc[-1]['Close']
            proceeds = position * final_price * (1 - commission)
            capital += proceeds
            
            profit = (final_price - entry_price) * position
            profit_pct = ((final_price - entry_price) / entry_price) * 100
            
            self.trades.append({
                'date': df.index[-1],
                'type': 'SELL',
                'price': final_price,
                'shares': position,
                'commission': position * final_price * commission,
                'profit': profit,
                'profit_pct': profit_pct
            })
        
        # Calculate performance metrics
        return self.calculate_metrics()
    
    def calculate_metrics(self) -> Dict[str, Any]:
        """
        Calculate performance metrics
        
        Returns:
            Dictionary with performance metrics
        """
        final_value = self.portfolio_value[-1]['value'] if self.portfolio_value else self.initial_capital
        
        total_return = final_value - self.initial_capital
        total_return_pct = (total_return / self.initial_capital) * 100
        
        # Calculate winning/losing trades
        profitable_trades = [t for t in self.trades if t.get('profit', 0) > 0]
        losing_trades = [t for t in self.trades if t.get('profit', 0) < 0]
        
        win_rate = (len(profitable_trades) / len([t for t in self.trades if 'profit' in t])) * 100 if self.trades else 0
        
        # Calculate average profit/loss
        avg_profit = np.mean([t['profit'] for t in profitable_trades]) if profitable_trades else 0
        avg_loss = np.mean([t['profit'] for t in losing_trades]) if losing_trades else 0
        
        # Calculate max drawdown
        portfolio_values = [pv['value'] for pv in self.portfolio_value]
        peak = np.maximum.accumulate(portfolio_values)
        drawdown = (peak - portfolio_values) / peak * 100
        max_drawdown = np.max(drawdown) if len(drawdown) > 0 else 0
        
        return {
            'initial_capital': self.initial_capital,
            'final_value': final_value,
            'total_return': total_return,
            'total_return_pct': total_return_pct,
            'total_trades': len(self.trades),
            'buy_trades': len([t for t in self.trades if t['type'] == 'BUY']),
            'sell_trades': len([t for t in self.trades if t['type'] == 'SELL']),
            'profitable_trades': len(profitable_trades),
            'losing_trades': len(losing_trades),
            'win_rate': win_rate,
            'avg_profit': avg_profit,
            'avg_loss': avg_loss,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': self._calculate_sharpe_ratio()
        }
    
    def _calculate_sharpe_ratio(self, risk_free_rate: float = 0.02) -> float:
        """
        Calculate Sharpe ratio
        
        Args:
            risk_free_rate: Annual risk-free rate
            
        Returns:
            Sharpe ratio
        """
        if len(self.portfolio_value) < 2:
            return 0.0
        
        values = pd.Series([pv['value'] for pv in self.portfolio_value])
        returns = values.pct_change().dropna()
        
        if len(returns) == 0 or returns.std() == 0:
            return 0.0
        
        excess_returns = returns - (risk_free_rate / 252)  # Daily risk-free rate
        sharpe = np.sqrt(252) * (excess_returns.mean() / excess_returns.std())
        
        return sharpe
    
    def get_trade_history(self) -> pd.DataFrame:
        """
        Get trade history as DataFrame
        
        Returns:
            DataFrame with trade history
        """
        if not self.trades:
            return pd.DataFrame()
        
        return pd.DataFrame(self.trades)
    
    def get_portfolio_history(self) -> pd.DataFrame:
        """
        Get portfolio value history
        
        Returns:
            DataFrame with portfolio history
        """
        if not self.portfolio_value:
            return pd.DataFrame()
        
        return pd.DataFrame(self.portfolio_value)


if __name__ == "__main__":
    # Example usage
    from modules.data_collector import DataCollector
    from modules.indicators import TechnicalIndicators
    
    # Collect data
    collector = DataCollector(symbol='AAPL', period='1y', interval='1d')
    data = collector.fetch_data()
    
    if data is not None:
        # Calculate indicators
        indicators = TechnicalIndicators(data)
        indicators.calculate_all_indicators()
        
        # Add indicators to data
        for name, series in indicators.indicators.items():
            data[name] = series
        
        # Run backtest
        backtester = Backtester(data, initial_capital=10000)
        results = backtester.run_backtest(strategy_type='combined')
        
        print("\n=== Backtest Results ===")
        print(f"Initial Capital: ${results['initial_capital']:,.2f}")
        print(f"Final Value: ${results['final_value']:,.2f}")
        print(f"Total Return: ${results['total_return']:,.2f} ({results['total_return_pct']:.2f}%)")
        print(f"\nTrade Statistics:")
        print(f"Total Trades: {results['total_trades']}")
        print(f"Win Rate: {results['win_rate']:.2f}%")
        print(f"Average Profit: ${results['avg_profit']:.2f}")
        print(f"Average Loss: ${results['avg_loss']:.2f}")
        print(f"Max Drawdown: {results['max_drawdown']:.2f}%")
        print(f"Sharpe Ratio: {results['sharpe_ratio']:.2f}")
