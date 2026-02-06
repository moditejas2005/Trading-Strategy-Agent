"""
Currency Converter Module
Converts USD prices to INR
"""
import requests
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fallback rate if API fails
DEFAULT_USD_TO_INR = 83.0


class CurrencyConverter:
    """
    Converts currency from USD to INR
    """
    
    def __init__(self):
        """Initialize currency converter"""
        self.usd_to_inr_rate = DEFAULT_USD_TO_INR
        self.update_exchange_rate()
    
    def update_exchange_rate(self) -> Optional[float]:
        """
        Fetch latest USD to INR exchange rate
        Falls back to default rate if fetch fails
        
        Returns:
            Exchange rate or None if failed
        """
        try:
            # Using exchangerate-api.com (free tier)
            url = "https://api.exchangerate-api.com/v4/latest/USD"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if 'rates' in data and 'INR' in data['rates']:
                    self.usd_to_inr_rate = data['rates']['INR']
                    logger.info(f"Updated exchange rate: 1 USD = ₹{self.usd_to_inr_rate:.2f}")
                    return self.usd_to_inr_rate
            
            logger.warning(f"Could not fetch exchange rate, using default: ₹{DEFAULT_USD_TO_INR}")
            return None
            
        except Exception as e:
            logger.warning(f"Error fetching exchange rate: {str(e)}, using default: ₹{DEFAULT_USD_TO_INR}")
            return None
    
    def usd_to_inr(self, usd_amount: float) -> float:
        """
        Convert USD to INR
        
        Args:
            usd_amount: Amount in USD
            
        Returns:
            Amount in INR
        """
        if usd_amount is None or usd_amount == 0:
            return 0.0
        
        inr_amount = usd_amount * self.usd_to_inr_rate
        return round(inr_amount, 2)
    
    def get_rate(self) -> float:
        """
        Get current exchange rate
        
        Returns:
            Current USD to INR rate
        """
        return self.usd_to_inr_rate


# Global instance
_converter = None

def get_converter():
    """Get or create global converter instance"""
    global _converter
    if _converter is None:
        _converter = CurrencyConverter()
    return _converter


if __name__ == "__main__":
    # Example usage
    converter = CurrencyConverter()
    
    print(f"Current Rate: 1 USD = ₹{converter.get_rate():.2f}")
    print(f"\nConversions:")
    print(f"$100 = ₹{converter.usd_to_inr(100):.2f}")
    print(f"$1,000 = ₹{converter.usd_to_inr(1000):,.2f}")
    print(f"$10,000 = ₹{converter.usd_to_inr(10000):,.2f}")
