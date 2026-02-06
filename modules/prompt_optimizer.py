"""
Prompt Optimization Module
Integrates with ScaleDown API to optimize AI prompts
"""
import requests
import logging
from typing import Dict, Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PromptOptimizer:
    """
    Optimizes prompts using ScaleDown API to reduce token usage and cost
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize PromptOptimizer
        
        Args:
            api_key: ScaleDown API key
        """
        self.api_key = api_key
        self.base_url = "https://api.skills.sh/v1"  # ScaleDown API endpoint
        self.headers = {
            "Authorization": f"Bearer {api_key}" if api_key else "",
            "Content-Type": "application/json"
        }
    
    def optimize_prompt(self, prompt: str, target_reduction: float = 0.5) -> Dict[str, Any]:
        """
        Optimize a prompt using ScaleDown API
        
        Args:
            prompt: Original prompt text
            target_reduction: Target token reduction ratio (0.0 to 1.0)
            
        Returns:
            Dictionary containing optimized prompt and metadata
        """
        if not self.api_key:
            logger.warning("ScaleDown API key not provided. Using original prompt.")
            return {
                'original_prompt': prompt,
                'optimized_prompt': prompt,
                'original_tokens': len(prompt.split()),
                'optimized_tokens': len(prompt.split()),
                'reduction_percentage': 0,
                'cost_savings': 0,
                'optimized': False
            }
        
        try:
            # Prepare request payload
            payload = {
                "prompt": prompt,
                "target_reduction": target_reduction,
                "preserve_meaning": True,
                "output_format": "text"
            }
            
            # Make API request
            logger.info("Sending prompt to ScaleDown API for optimization...")
            response = requests.post(
                f"{self.base_url}/optimize",
                json=payload,
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                optimized_data = {
                    'original_prompt': prompt,
                    'optimized_prompt': result.get('optimized_prompt', prompt),
                    'original_tokens': result.get('original_tokens', 0),
                    'optimized_tokens': result.get('optimized_tokens', 0),
                    'reduction_percentage': result.get('reduction_percentage', 0),
                    'cost_savings': result.get('cost_savings', 0),
                    'optimized': True
                }
                
                logger.info(f"Prompt optimized: {optimized_data['reduction_percentage']:.1f}% token reduction")
                return optimized_data
            else:
                logger.error(f"ScaleDown API error: {response.status_code} - {response.text}")
                return self._fallback_optimization(prompt)
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error calling ScaleDown API: {str(e)}")
            return self._fallback_optimization(prompt)
        except Exception as e:
            logger.error(f"Error optimizing prompt: {str(e)}")
            return self._fallback_optimization(prompt)
    
    def _fallback_optimization(self, prompt: str) -> Dict[str, Any]:
        """
        Fallback optimization using basic text compression
        
        Args:
            prompt: Original prompt
            
        Returns:
            Dictionary with basic optimization
        """
        # Simple optimization: remove extra whitespace and redundant words
        optimized = ' '.join(prompt.split())
        
        return {
            'original_prompt': prompt,
            'optimized_prompt': optimized,
            'original_tokens': len(prompt.split()),
            'optimized_tokens': len(optimized.split()),
            'reduction_percentage': ((len(prompt) - len(optimized)) / len(prompt) * 100) if len(prompt) > 0 else 0,
            'cost_savings': 0,
            'optimized': False,
            'note': 'Fallback optimization used (API unavailable)'
        }
    
    def batch_optimize(self, prompts: list) -> list:
        """
        Optimize multiple prompts in batch
        
        Args:
            prompts: List of prompt strings
            
        Returns:
            List of optimization results
        """
        results = []
        for prompt in prompts:
            result = self.optimize_prompt(prompt)
            results.append(result)
        
        return results
    
    def get_optimization_stats(self, optimization_results: list) -> Dict[str, Any]:
        """
        Calculate aggregate optimization statistics
        
        Args:
            optimization_results: List of optimization result dictionaries
            
        Returns:
            Dictionary with aggregate stats
        """
        total_original = sum(r['original_tokens'] for r in optimization_results)
        total_optimized = sum(r['optimized_tokens'] for r in optimization_results)
        total_savings = sum(r.get('cost_savings', 0) for r in optimization_results)
        
        return {
            'total_prompts': len(optimization_results),
            'total_original_tokens': total_original,
            'total_optimized_tokens': total_optimized,
            'total_tokens_saved': total_original - total_optimized,
            'average_reduction': ((total_original - total_optimized) / total_original * 100) if total_original > 0 else 0,
            'total_cost_savings': total_savings
        }


if __name__ == "__main__":
    # Example usage
    optimizer = PromptOptimizer()  # Will use fallback without API key
    
    sample_prompt = """
    Analyze the following stock data and provide a comprehensive trading strategy.
    Consider technical indicators including RSI, MACD, and Moving Averages.
    Provide entry points, exit points, and risk management recommendations.
    Include both short-term and long-term perspectives in your analysis.
    """
    
    result = optimizer.optimize_prompt(sample_prompt)
    
    print("\nPrompt Optimization Result:")
    print(f"Original tokens: {result['original_tokens']}")
    print(f"Optimized tokens: {result['optimized_tokens']}")
    print(f"Reduction: {result['reduction_percentage']:.1f}%")
    print(f"\nOptimized prompt:\n{result['optimized_prompt']}")
