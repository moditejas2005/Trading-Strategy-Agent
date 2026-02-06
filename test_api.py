"""
Test ScaleDown API Integration
"""
from modules.prompt_optimizer import PromptOptimizer

# Initialize with API key
optimizer = PromptOptimizer(api_key='V6UNcDCSAO4xocJl3NPaSaoFAH8357aa17VRMcJZ')

# Test prompt
test_prompt = """
Analyze this stock data and provide comprehensive trading recommendations.
Consider technical indicators including RSI, MACD, and Moving Averages.
Provide entry points, exit points, and risk management strategies.
"""

print("🧪 Testing ScaleDown API Integration...")
print("=" * 60)

result = optimizer.optimize_prompt(test_prompt)

print(f"\n✅ API Status: {'Connected' if result['optimized'] else 'Using Fallback'}")
print(f"📊 Original Tokens: {result['original_tokens']}")
print(f"⚡ Optimized Tokens: {result['optimized_tokens']}")
print(f"💰 Reduction: {result['reduction_percentage']:.1f}%")

if 'cost_savings' in result:
    print(f"💵 Cost Savings: ${result['cost_savings']:.4f}")

print("\n" + "=" * 60)
print("✨ ScaleDown API is ready to use!")
