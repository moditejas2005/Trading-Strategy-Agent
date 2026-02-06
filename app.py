"""
Flask API Backend for AI Trading Strategy Agent
"""
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import logging
from config import config
from modules.data_collector import DataCollector
from modules.indicators import TechnicalIndicators
from modules.strategy_generator import StrategyGenerator
from modules.backtester import Backtester
from modules.prompt_optimizer import PromptOptimizer
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure app
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/')
def index():
    """Serve the main dashboard"""
    return render_template('index.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'AI Trading Strategy Agent'
    })


@app.route('/api/market-data', methods=['GET'])
def get_market_data():
    """
    Get market data for a symbol
    Query params: symbol, period, interval
    """
    try:
        symbol = request.args.get('symbol', app.config['DEFAULT_SYMBOL'])
        period = request.args.get('period', '1mo')
        interval = request.args.get('interval', app.config['DEFAULT_TIMEFRAME'])
        
        collector = DataCollector(symbol=symbol, period=period, interval=interval)
        data = collector.fetch_data()
        
        if data is None:
            return jsonify({'error': 'Failed to fetch market data'}), 404
        
        # Get summary and ticker info
        summary = collector.get_data_summary()
        ticker_info = collector.get_ticker_info()
        
        # Convert data to dictionary
        data_dict = data.reset_index().to_dict(orient='records')
        
        return jsonify({
            'symbol': symbol,
            'data': data_dict,
            'summary': summary,
            'ticker_info': ticker_info
        })
    
    except Exception as e:
        logger.error(f"Error in get_market_data: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/indicators', methods=['GET'])
def get_indicators():
    """
    Calculate technical indicators
    Query params: symbol, period, interval
    """
    try:
        symbol = request.args.get('symbol', app.config['DEFAULT_SYMBOL'])
        period = request.args.get('period', '3mo')
        interval = request.args.get('interval', app.config['DEFAULT_TIMEFRAME'])
        
        # Fetch data
        collector = DataCollector(symbol=symbol, period=period, interval=interval)
        data = collector.fetch_data()
        
        if data is None:
            return jsonify({'error': 'Failed to fetch market data'}), 404
        
        # Calculate indicators
        indicators = TechnicalIndicators(data)
        all_indicators = indicators.calculate_all_indicators()
        signals = indicators.get_latest_signals()
        
        return jsonify({
            'symbol': symbol,
            'indicators': signals['indicators'],
            'signals': signals['signals']
        })
    
    except Exception as e:
        logger.error(f"Error in get_indicators: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/strategy', methods=['POST'])
def generate_strategy():
    """
    Generate AI trading strategy
    Body: { symbol, period, interval, use_optimization }
    """
    try:
        data = request.get_json()
        symbol = data.get('symbol', app.config['DEFAULT_SYMBOL'])
        period = data.get('period', '3mo')
        interval = data.get('interval', app.config['DEFAULT_TIMEFRAME'])
        use_optimization = data.get('use_optimization', True)
        
        # Fetch market data
        collector = DataCollector(symbol=symbol, period=period, interval=interval)
        market_data_df = collector.fetch_data()
        
        if market_data_df is None:
            return jsonify({'error': 'Failed to fetch market data'}), 404
        
        # Calculate indicators
        indicator_calc = TechnicalIndicators(market_data_df)
        indicator_calc.calculate_all_indicators()
        signals = indicator_calc.get_latest_signals()
        
        # Get market data summary
        ticker_info = collector.get_ticker_info()
        market_data = {
            'current_price': collector.get_latest_price(),
            'high_52w': ticker_info.get('fiftyTwoWeekHigh', 0),
            'low_52w': ticker_info.get('fiftyTwoWeekLow', 0)
        }
        
        # Generate strategy
        generator = StrategyGenerator(use_optimization=use_optimization)
        result = generator.generate_strategy(
            symbol=symbol,
            indicators=signals['indicators'],
            market_data=market_data
        )
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error in generate_strategy: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/backtest', methods=['POST'])
def run_backtest():
    """
    Run strategy backtest
    Body: { symbol, period, interval, strategy_type, initial_capital }
    """
    try:
        data = request.get_json()
        symbol = data.get('symbol', app.config['DEFAULT_SYMBOL'])
        period = data.get('period', '1y')
        interval = data.get('interval', app.config['DEFAULT_TIMEFRAME'])
        strategy_type = data.get('strategy_type', 'combined')
        initial_capital = data.get('initial_capital', 10000)
        
        # Fetch data
        collector = DataCollector(symbol=symbol, period=period, interval=interval)
        market_data = collector.fetch_data()
        
        if market_data is None:
            return jsonify({'error': 'Failed to fetch market data'}), 404
        
        # Calculate indicators
        indicators = TechnicalIndicators(market_data)
        indicators.calculate_all_indicators()
        
        # Add indicators to dataframe
        for name, series in indicators.indicators.items():
            market_data[name] = series
        
        # Run backtest
        backtester = Backtester(market_data, initial_capital=initial_capital)
        results = backtester.run_backtest(strategy_type=strategy_type)
        
        # Get trade and portfolio history
        trade_history = backtester.get_trade_history().to_dict(orient='records')
        portfolio_history = backtester.get_portfolio_history().to_dict(orient='records')
        
        return jsonify({
            'symbol': symbol,
            'strategy_type': strategy_type,
            'results': results,
            'trade_history': trade_history,
            'portfolio_history': portfolio_history
        })
    
    except Exception as e:
        logger.error(f"Error in run_backtest: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/optimize-prompt', methods=['POST'])
def optimize_prompt():
    """
    Optimize a prompt using ScaleDown API
    Body: { prompt, target_reduction }
    """
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        target_reduction = data.get('target_reduction', 0.5)
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        scaledown_key = app.config.get('SCALEDOWN_API_KEY')
        optimizer = PromptOptimizer(api_key=scaledown_key)
        result = optimizer.optimize_prompt(prompt, target_reduction=target_reduction)
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error in optimize_prompt: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = app.config.get('PORT', 5000)
    debug = app.config.get('DEBUG', True)
    
    logger.info(f"Starting AI Trading Strategy Agent API on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
