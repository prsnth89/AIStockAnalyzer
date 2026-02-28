import sys
sys.path.insert(0, 'src')
from analyzer import analyze_ticker

try:
    result = analyze_ticker('AAPL')
    print('\n=== RESULT ===')
    print(f'Ticker: {result["ticker"]}')
    print(f'Current Price: ${result["current_price"]}')
    print(f'Fair Value: ${result["fair_value"]}')
    print(f'Buy Range: ${result["strong_buy"]} - ${result["buy"]}')
    print(f'Sell Range: ${result["sell"]} - ${result["strong_sell"]}')
    print(f'Recommendation: {result["recommendation"]}')
    print(f'P/E Ratio: {result["pe_ratio"]}')
except Exception as e:
    print(f'\n=== ERROR ===')
    print(f'{type(e).__name__}: {e}')
    import traceback
    traceback.print_exc()
