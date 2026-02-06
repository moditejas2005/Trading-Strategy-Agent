"""
PostgreSQL Database Module
Handles database operations for the Trading Strategy Agent
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()


class TradingStrategy(Base):
    """Trading strategy records"""
    __tablename__ = 'trading_strategies'
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), nullable=False, index=True)
    strategy_type = Column(String(50))
    action = Column(String(10))  # BUY, SELL, HOLD
    confidence = Column(Float)
    indicators = Column(JSON)  # Store technical indicators as JSON
    market_data = Column(JSON)  # Store market data as JSON
    created_at = Column(DateTime, default=datetime.utcnow)


class BacktestResult(Base):
    """Backtest result records"""
    __tablename__ = 'backtest_results'
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), nullable=False, index=True)
    strategy_type = Column(String(50))
    initial_capital = Column(Float)
    final_value = Column(Float)
    total_return = Column(Float)
    total_return_pct = Column(Float)
    total_trades = Column(Integer)
    win_rate = Column(Float)
    max_drawdown = Column(Float)
    sharpe_ratio = Column(Float)
    backtest_period = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)


class MarketData(Base):
    """Historical market data cache"""
    __tablename__ = 'market_data'
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), nullable=False, index=True)
    date = Column(DateTime, nullable=False, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
    source = Column(String(20))  # yfinance, alpha_vantage
    created_at = Column(DateTime, default=datetime.utcnow)


class PromptOptimization(Base):
    """Prompt optimization history"""
    __tablename__ = 'prompt_optimizations'
    
    id = Column(Integer, primary_key=True)
    original_prompt = Column(Text)
    optimized_prompt = Column(Text)
    original_tokens = Column(Integer)
    optimized_tokens = Column(Integer)
    reduction_percentage = Column(Float)
    cost_savings = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


class DatabaseManager:
    """
    Manages PostgreSQL database connections and operations
    """
    
    def __init__(self, database_uri: str):
        """
        Initialize database manager
        
        Args:
            database_uri: SQLAlchemy database URI
        """
        self.engine = create_engine(database_uri, pool_pre_ping=True)
        self.Session = scoped_session(sessionmaker(bind=self.engine))
        logger.info("Database connection established")
    
    def create_tables(self):
        """Create all database tables"""
        try:
            Base.metadata.create_all(self.engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating tables: {str(e)}")
            raise
    
    def drop_tables(self):
        """Drop all database tables (use with caution!)"""
        try:
            Base.metadata.drop_all(self.engine)
            logger.info("Database tables dropped successfully")
        except Exception as e:
            logger.error(f"Error dropping tables: {str(e)}")
            raise
    
    def get_session(self):
        """Get a database session"""
        return self.Session()
    
    def save_strategy(self, symbol: str, strategy_data: dict):
        """
        Save trading strategy to database
        
        Args:
            symbol: Stock symbol
            strategy_data: Strategy details dictionary
        """
        session = self.get_session()
        try:
            strategy = TradingStrategy(
                symbol=symbol,
                strategy_type=strategy_data.get('strategy_type', 'combined'),
                action=strategy_data.get('action'),
                confidence=strategy_data.get('confidence'),
                indicators=strategy_data.get('indicators'),
                market_data=strategy_data.get('market_data')
            )
            session.add(strategy)
            session.commit()
            logger.info(f"Strategy saved for {symbol}")
            return strategy.id
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving strategy: {str(e)}")
            raise
        finally:
            session.close()
    
    def save_backtest_result(self, symbol: str, result_data: dict):
        """
        Save backtest result to database
        
        Args:
            symbol: Stock symbol
            result_data: Backtest result dictionary
        """
        session = self.get_session()
        try:
            result = BacktestResult(
                symbol=symbol,
                strategy_type=result_data.get('strategy_type'),
                initial_capital=result_data.get('initial_capital'),
                final_value=result_data.get('final_value'),
                total_return=result_data.get('total_return'),
                total_return_pct=result_data.get('total_return_pct'),
                total_trades=result_data.get('total_trades'),
                win_rate=result_data.get('win_rate'),
                max_drawdown=result_data.get('max_drawdown'),
                sharpe_ratio=result_data.get('sharpe_ratio'),
                backtest_period=result_data.get('period', 'unknown')
            )
            session.add(result)
            session.commit()
            logger.info(f"Backtest result saved for {symbol}")
            return result.id
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving backtest result: {str(e)}")
            raise
        finally:
            session.close()
    
    def get_strategies_by_symbol(self, symbol: str, limit: int = 10):
        """
        Get recent strategies for a symbol
        
        Args:
            symbol: Stock symbol
            limit: Maximum number of records to return
            
        Returns:
            List of strategy records
        """
        session = self.get_session()
        try:
            strategies = session.query(TradingStrategy)\
                .filter_by(symbol=symbol)\
                .order_by(TradingStrategy.created_at.desc())\
                .limit(limit)\
                .all()
            return strategies
        finally:
            session.close()
    
    def get_backtest_history(self, symbol: str = None, limit: int = 10):
        """
        Get backtest history
        
        Args:
            symbol: Optional stock symbol filter
            limit: Maximum number of records
            
        Returns:
            List of backtest records
        """
        session = self.get_session()
        try:
            query = session.query(BacktestResult)
            if symbol:
                query = query.filter_by(symbol=symbol)
            results = query.order_by(BacktestResult.created_at.desc()).limit(limit).all()
            return results
        finally:
            session.close()


if __name__ == "__main__":
    # Example: Create database and tables
    from config import config
    
    app_config = config['development']
    db_uri = app_config.SQLALCHEMY_DATABASE_URI
    
    print(f"Database URI: {db_uri}")
    
    db_manager = DatabaseManager(db_uri)
    db_manager.create_tables()
    
    print("✅ PostgreSQL database initialized successfully!")
    print("\nCreated tables:")
    print("- trading_strategies")
    print("- backtest_results")
    print("- market_data")
    print("- prompt_optimizations")
