"""
AI Strategy Generation Module
Generates trading strategies using AI models
"""
import logging
from typing import Dict, Any, Optional
from modules.prompt_optimizer import PromptOptimizer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StrategyGenerator:
    """
    Generates AI-powered trading strategies
    """
    
    def __init__(self, api_key: Optional[str] = None, use_optimization: bool = True):
        """
        Initialize StrategyGenerator
        
        Args:
            api_key: OpenAI API key
            use_optimization: Whether to use prompt optimization
        """
        self.api_key = api_key
        self.use_optimization = use_optimization
        self.optimizer = PromptOptimizer() if use_optimization else None
    
    def create_analysis_prompt(self, 
                              symbol: str,
                              indicators: Dict[str, Any],
                              market_data: Dict[str, Any]) -> str:
        """
        Create a comprehensive analysis prompt
        
        Args:
            symbol: Stock symbol
            indicators: Technical indicator values
            market_data: Current market data
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""
# Trading Strategy Analysis for {symbol}

## Current Market Data
- Symbol: {symbol}
- Current Price: ${market_data.get('current_price', 'N/A')}
- 52-Week High: ${market_data.get('high_52w', 'N/A')}
- 52-Week Low: ${market_data.get('low_52w', 'N/A')}

## Technical Indicators
"""
        
        # Add RSI analysis
        if 'RSI' in indicators:
            prompt += f"\n### RSI (Relative Strength Index): {indicators['RSI']:.2f}"
            if indicators['RSI'] < 30:
                prompt += "\n- Status: OVERSOLD - Potential buy opportunity"
            elif indicators['RSI'] > 70:
                prompt += "\n- Status: OVERBOUGHT - Potential sell signal"
            else:
                prompt += "\n- Status: NEUTRAL"
        
        # Add MACD analysis
        if 'MACD' in indicators:
            prompt += f"\n\n### MACD"
            prompt += f"\n- MACD Line: {indicators['MACD']:.2f}"
            prompt += f"\n- Signal Line: {indicators['MACD_Signal']:.2f}"
            prompt += f"\n- Histogram: {indicators['MACD_Histogram']:.2f}"
            if indicators['MACD'] > indicators['MACD_Signal']:
                prompt += "\n- Trend: BULLISH"
            else:
                prompt += "\n- Trend: BEARISH"
        
        # Add Moving Averages
        if 'SMA_Short' in indicators and 'SMA_Long' in indicators:
            prompt += f"\n\n### Moving Averages"
            prompt += f"\n- Short-term MA (20): ${indicators['SMA_Short']:.2f}"
            prompt += f"\n- Long-term MA (50): ${indicators['SMA_Long']:.2f}"
            if indicators['SMA_Short'] > indicators['SMA_Long']:
                prompt += "\n- Crossover: BULLISH (Golden Cross potential)"
            else:
                prompt += "\n- Crossover: BEARISH (Death Cross potential)"
        
        prompt += """

## Required Analysis
Provide a comprehensive trading strategy including:
1. **Market Outlook**: Current trend and momentum
2. **Entry Strategy**: Optimal entry points with price levels
3. **Exit Strategy**: Target prices and stop-loss levels
4. **Risk Management**: Position sizing and risk/reward ratio
5. **Time Horizon**: Short-term (days) and medium-term (weeks) outlook
6. **Confidence Level**: Rate your confidence (1-10) in this strategy

Keep the analysis concise and actionable.
"""
        
        return prompt
    
    def generate_strategy(self,
                         symbol: str,
                         indicators: Dict[str, Any],
                         market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate AI trading strategy
        
        Args:
            symbol: Stock symbol
            indicators: Technical indicator values
            market_data: Market data summary
            
        Returns:
            Dictionary containing strategy and metadata
        """
        # Create analysis prompt
        original_prompt = self.create_analysis_prompt(symbol, indicators, market_data)
        
        # Optimize prompt if enabled
        optimized_prompt = original_prompt
        optimization_data = None
        
        if self.use_optimization and self.optimizer:
            logger.info("Optimizing analysis prompt...")
            optimization_result = self.optimizer.optimize_prompt(original_prompt)
            optimized_prompt = optimization_result['optimized_prompt']
            optimization_data = optimization_result
        
        # Generate strategy (placeholder for actual AI call)
        strategy = self._generate_mock_strategy(symbol, indicators)
        
        return {
            'symbol': symbol,
            'strategy': strategy,
            'prompt': {
                'original': original_prompt,
                'optimized': optimized_prompt,
                'optimization': optimization_data
            },
            'timestamp': pd.Timestamp.now().isoformat()
        }
    
    def _generate_mock_strategy(self, symbol: str, indicators: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a mock strategy based on indicators
        (This would be replaced with actual AI API call)
        
        Args:
            symbol: Stock symbol
            indicators: Technical indicators
            
        Returns:
            Strategy dictionary
        """
        # Determine overall signal
        signals = []
        
        if 'RSI' in indicators:
            if indicators['RSI'] < 30:
                signals.append('BUY')
            elif indicators['RSI'] > 70:
                signals.append('SELL')
            else:
                signals.append('HOLD')
        
        if 'MACD' in indicators and 'MACD_Signal' in indicators:
            if indicators['MACD'] > indicators['MACD_Signal']:
                signals.append('BUY')
            else:
                signals.append('SELL')
        
        if 'SMA_Short' in indicators and 'SMA_Long' in indicators:
            if indicators['SMA_Short'] > indicators['SMA_Long']:
                signals.append('BUY')
            else:
                signals.append('SELL')
        
        # Count signals
        buy_count = signals.count('BUY')
        sell_count = signals.count('SELL')
        
        if buy_count > sell_count:
            action = 'BUY'
            confidence = (buy_count / len(signals)) * 10
        elif sell_count > buy_count:
            action = 'SELL'
            confidence = (sell_count / len(signals)) * 10
        else:
            action = 'HOLD'
            confidence = 5
        
        return {
            'action': action,
            'confidence': round(confidence, 1),
            'market_outlook': f"Based on technical indicators, the outlook is {'BULLISH' if action == 'BUY' else 'BEARISH' if action == 'SELL' else 'NEUTRAL'}",
            'entry_strategy': f"Consider {action.lower()}ing {symbol} near current levels" if action != 'HOLD' else "Wait for clearer signals",
            'risk_management': "Use 2% position sizing with stop-loss at 5% below entry",
            'time_horizon': "Short to medium term (1-4 weeks)"
        }


# Import pandas here to avoid circular import
import pandas as pd


if __name__ == "__main__":
    # Example usage
    generator = StrategyGenerator(use_optimization=True)
    
    sample_indicators = {
        'RSI': 45.5,
        'MACD': 2.3,
        'MACD_Signal': 1.8,
        'MACD_Histogram': 0.5,
        'SMA_Short': 175.50,
        'SMA_Long': 172.30
    }
    
    sample_market_data = {
        'current_price': 178.25,
        'high_52w': 198.50,
        'low_52w': 145.30
    }
    
    result = generator.generate_strategy('AAPL', sample_indicators, sample_market_data)
    
    print("\nGenerated Strategy:")
    print(f"Symbol: {result['symbol']}")
    print(f"Action: {result['strategy']['action']}")
    print(f"Confidence: {result['strategy']['confidence']}/10")
    print(f"\nStrategy Details:")
    for key, value in result['strategy'].items():
        if key not in ['action', 'confidence']:
            print(f"- {key.replace('_', ' ').title()}: {value}")
