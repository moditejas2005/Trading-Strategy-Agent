"""
Configuration management for AI Trading Strategy Agent
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Base configuration class"""
    
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    SCALEDOWN_API_KEY = os.getenv('SCALEDOWN_API_KEY')
    ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', '8MZEFUFMBSNMQWA9')
    
    # Database Configuration
    DB_TYPE = os.getenv('DB_TYPE', 'postgresql')
    
    # PostgreSQL Configuration
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = int(os.getenv('POSTGRES_PORT', 5432))
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', '')
    POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE', 'trading_agent')
    
    # SQLAlchemy Database URI for PostgreSQL
    SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Application Settings
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    PORT = int(os.getenv('PORT', 5000))
    
    # Trading Parameters
    DEFAULT_SYMBOL = os.getenv('DEFAULT_SYMBOL', 'AAPL')
    DEFAULT_TIMEFRAME = os.getenv('DEFAULT_TIMEFRAME', '1d')
    BACKTESTING_PERIOD = int(os.getenv('BACKTESTING_PERIOD', 365))
    
    # Technical Indicator Parameters
    RSI_PERIOD = 14
    MACD_FAST = 12
    MACD_SLOW = 26
    MACD_SIGNAL = 9
    MA_SHORT = 20
    MA_LONG = 50


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
