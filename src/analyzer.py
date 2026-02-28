import yfinance as yf
import requests
import urllib3

# Disable SSL warnings for corporate firewall
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Mock data for demonstration (corporate firewall blocks Yahoo Finance)
MOCK_DATA = {
    'AAPL': {
        'price': 178.50, 'pe': 29.2, 'forward_pe': 27.8, 'industry_pe': 31.5, 'peg': 2.1, 
        'market_cap': 2840, 'book_value': 4.21, 'pb_ratio': 42.4, 'name': 'Apple Inc.',
        'quarterly': [
            # 2026 - 2025 (last 4 shown earlier + full 10 year history - 40 quarters total)
            {'period': 'Q1 2026', 'revenue': 119.6, 'revenue_growth': 2.1, 'gross_profit': 54.9, 'gross_margin': 45.9, 'net_profit': 33.9, 'net_margin': 28.3, 'net_profit_growth': 4.3, 'debt': 111.1, 'debt_growth': 2.8},
            {'period': 'Q4 2025', 'revenue': 124.3, 'revenue_growth': 6.1, 'gross_profit': 57.1, 'gross_margin': 45.9, 'net_profit': 36.2, 'net_margin': 29.1, 'net_profit_growth': 8.2, 'debt': 108.1, 'debt_growth': 3.1},
            {'period': 'Q3 2025', 'revenue': 94.9, 'revenue_growth': 4.7, 'gross_profit': 43.9, 'gross_margin': 46.2, 'net_profit': 25.0, 'net_margin': 26.3, 'net_profit_growth': 5.9, 'debt': 104.8, 'debt_growth': 2.5},
            {'period': 'Q2 2025', 'revenue': 85.8, 'revenue_growth': 5.8, 'gross_profit': 39.7, 'gross_margin': 46.3, 'net_profit': 21.4, 'net_margin': 24.9, 'net_profit_growth': 6.8, 'debt': 102.3, 'debt_growth': 1.9},
            # 2024
            {'period': 'Q1 2025', 'revenue': 117.2, 'revenue_growth': -0.4, 'gross_profit': 54.0, 'gross_margin': 46.1, 'net_profit': 32.5, 'net_margin': 27.7, 'net_profit_growth': -2.1, 'debt': 100.4, 'debt_growth': 1.3},
            {'period': 'Q4 2024', 'revenue': 119.6, 'revenue_growth': 2.0, 'gross_profit': 55.2, 'gross_margin': 46.2, 'net_profit': 33.4, 'net_margin': 27.9, 'net_profit_growth': 3.5, 'debt': 99.1, 'debt_growth': 0.8},
            {'period': 'Q3 2024', 'revenue': 90.8, 'revenue_growth': 6.1, 'gross_profit': 42.1, 'gross_margin': 46.4, 'net_profit': 23.6, 'net_margin': 26.0, 'net_profit_growth': 7.2, 'debt': 98.3, 'debt_growth': -0.5},
            {'period': 'Q2 2024', 'revenue': 81.8, 'revenue_growth': 4.9, 'gross_profit': 37.8, 'gross_margin': 46.2, 'net_profit': 20.0, 'net_margin': 24.5, 'net_profit_growth': 5.4, 'debt': 98.8, 'debt_growth': -1.2},
            # 2023
            {'period': 'Q1 2024', 'revenue': 117.2, 'revenue_growth': -5.5, 'gross_profit': 54.5, 'gross_margin': 46.5, 'net_profit': 33.2, 'net_margin': 28.3, 'net_profit_growth': -4.8, 'debt': 100.0, 'debt_growth': -2.8},
            {'period': 'Q4 2023', 'revenue': 117.2, 'revenue_growth': 3.7, 'gross_profit': 54.0, 'gross_margin': 46.1, 'net_profit': 32.3, 'net_margin': 27.5, 'net_profit_growth': 4.2, 'debt': 102.9, 'debt_growth': 5.1},
            {'period': 'Q3 2023', 'revenue': 85.8, 'revenue_growth': -13.4, 'gross_profit': 39.3, 'gross_margin': 45.8, 'net_profit': 22.0, 'net_margin': 25.6, 'net_profit_growth': -11.2, 'debt': 97.9, 'debt_growth': 4.8},
            {'period': 'Q2 2023', 'revenue': 78.0, 'revenue_growth': -2.5, 'gross_profit': 35.4, 'gross_margin': 45.4, 'net_profit': 19.0, 'net_margin': 24.4, 'net_profit_growth': -3.8, 'debt': 93.4, 'debt_growth': 3.2},
            # 2022
            {'period': 'Q1 2023', 'revenue': 124.1, 'revenue_growth': 8.6, 'gross_profit': 54.7, 'gross_margin': 44.1, 'net_profit': 34.9, 'net_margin': 28.1, 'net_profit_growth': 9.5, 'debt': 90.5, 'debt_growth': 8.4},
            {'period': 'Q4 2022', 'revenue': 113.1, 'revenue_growth': 6.5, 'gross_profit': 49.8, 'gross_margin': 44.0, 'net_profit': 31.0, 'net_margin': 27.4, 'net_profit_growth': 7.8, 'debt': 83.5, 'debt_growth': 12.5},
            {'period': 'Q3 2022', 'revenue': 99.0, 'revenue_growth': 29.0, 'gross_profit': 43.3, 'gross_margin': 43.7, 'net_profit': 24.8, 'net_margin': 25.0, 'net_profit_growth': 31.5, 'debt': 74.2, 'debt_growth': 15.8},
            {'period': 'Q2 2022', 'revenue': 80.0, 'revenue_growth': 36.5, 'gross_profit': 34.5, 'gross_margin': 43.1, 'net_profit': 19.7, 'net_margin': 24.6, 'net_profit_growth': 38.2, 'debt': 64.1, 'debt_growth': 18.2},
            # 2021
            {'period': 'Q1 2022', 'revenue': 114.3, 'revenue_growth': 54.0, 'gross_profit': 45.7, 'gross_margin': 40.0, 'net_profit': 31.9, 'net_margin': 27.9, 'net_profit_growth': 62.5, 'debt': 54.2, 'debt_growth': 22.1},
            {'period': 'Q4 2021', 'revenue': 106.2, 'revenue_growth': 35.1, 'gross_profit': 41.2, 'gross_margin': 38.8, 'net_profit': 28.8, 'net_margin': 27.1, 'net_profit_growth': 41.2, 'debt': 44.4, 'debt_growth': 18.5},
            {'period': 'Q3 2021', 'revenue': 76.8, 'revenue_growth': 36.4, 'gross_profit': 31.5, 'gross_margin': 41.0, 'net_profit': 18.9, 'net_margin': 24.6, 'net_profit_growth': 93.2, 'debt': 37.5, 'debt_growth': 20.3},
            {'period': 'Q2 2021', 'revenue': 58.6, 'revenue_growth': 54.0, 'gross_profit': 24.9, 'gross_margin': 42.5, 'net_profit': 14.3, 'net_margin': 24.4, 'net_profit_growth': 110.0, 'debt': 31.2, 'debt_growth': 25.8},
            # 2020
            {'period': 'Q1 2021', 'revenue': 74.3, 'revenue_growth': 11.0, 'gross_profit': 28.2, 'gross_margin': 38.0, 'net_profit': 19.6, 'net_margin': 26.4, 'net_profit_growth': 29.0, 'debt': 24.8, 'debt_growth': -8.5},
            {'period': 'Q4 2020', 'revenue': 78.6, 'revenue_growth': 21.0, 'gross_profit': 29.8, 'gross_margin': 37.9, 'net_profit': 20.4, 'net_margin': 26.0, 'net_profit_growth': 35.1, 'debt': 27.1, 'debt_growth': -12.3},
            {'period': 'Q3 2020', 'revenue': 56.3, 'revenue_growth': -10.6, 'gross_profit': 22.7, 'gross_margin': 40.3, 'net_profit': 9.8, 'net_margin': 17.4, 'net_profit_growth': -27.0, 'debt': 30.9, 'debt_growth': -6.8},
            {'period': 'Q2 2020', 'revenue': 38.0, 'revenue_growth': -8.1, 'gross_profit': 14.9, 'gross_margin': 39.2, 'net_profit': 6.8, 'net_margin': 17.9, 'net_profit_growth': -18.9, 'debt': 33.2, 'debt_growth': -4.3},
            # 2019
            {'period': 'Q1 2020', 'revenue': 66.9, 'revenue_growth': 1.0, 'gross_profit': 24.4, 'gross_margin': 36.5, 'net_profit': 15.2, 'net_margin': 22.7, 'net_profit_growth': 2.3, 'debt': 34.7, 'debt_growth': -1.7},
            {'period': 'Q4 2019', 'revenue': 65.0, 'revenue_growth': -0.6, 'gross_profit': 24.1, 'gross_margin': 37.1, 'net_profit': 15.1, 'net_margin': 23.2, 'net_profit_growth': 0.4, 'debt': 35.3, 'debt_growth': 2.9},
            {'period': 'Q3 2019', 'revenue': 63.0, 'revenue_growth': 1.8, 'gross_profit': 24.0, 'gross_margin': 38.1, 'net_profit': 13.4, 'net_margin': 21.3, 'net_profit_growth': 3.1, 'debt': 34.3, 'debt_growth': 4.5},
            {'period': 'Q2 2019', 'revenue': 41.4, 'revenue_growth': -5.1, 'gross_profit': 16.5, 'gross_margin': 39.9, 'net_profit': 8.4, 'net_margin': 20.3, 'net_profit_growth': -7.2, 'debt': 32.8, 'debt_growth': 6.2},
            # 2018
            {'period': 'Q1 2019', 'revenue': 66.3, 'revenue_growth': 5.5, 'gross_profit': 25.3, 'gross_margin': 38.2, 'net_profit': 14.9, 'net_margin': 22.5, 'net_profit_growth': 10.4, 'debt': 30.9, 'debt_growth': -1.9},
            {'period': 'Q4 2018', 'revenue': 65.4, 'revenue_growth': 12.7, 'gross_profit': 24.8, 'gross_margin': 37.9, 'net_profit': 15.0, 'net_margin': 22.9, 'net_profit_growth': 17.2, 'debt': 31.5, 'debt_growth': -2.5},
            {'period': 'Q3 2018', 'revenue': 61.9, 'revenue_growth': 19.6, 'gross_profit': 23.9, 'gross_margin': 38.6, 'net_profit': 13.0, 'net_margin': 21.0, 'net_profit_growth': 32.1, 'debt': 32.3, 'debt_growth': -1.8},
            {'period': 'Q2 2018', 'revenue': 43.6, 'revenue_growth': 14.5, 'gross_profit': 17.2, 'gross_margin': 39.5, 'net_profit': 9.1, 'net_margin': 20.9, 'net_profit_growth': 24.7, 'debt': 32.9, 'debt_growth': 0.6},
            # 2017
            {'period': 'Q1 2018', 'revenue': 62.8, 'revenue_growth': 15.9, 'gross_profit': 24.1, 'gross_margin': 38.4, 'net_profit': 13.5, 'net_margin': 21.5, 'net_profit_growth': 25.0, 'debt': 32.7, 'debt_growth': 3.2},
            {'period': 'Q4 2017', 'revenue': 58.0, 'revenue_growth': 13.0, 'gross_profit': 22.2, 'gross_margin': 38.3, 'net_profit': 12.8, 'net_margin': 22.1, 'net_profit_growth': 12.4, 'debt': 31.7, 'debt_growth': 4.1},
            {'period': 'Q3 2017', 'revenue': 51.8, 'revenue_growth': 12.4, 'gross_profit': 20.1, 'gross_margin': 38.8, 'net_profit': 9.8, 'net_margin': 18.9, 'net_profit_growth': 24.1, 'debt': 30.5, 'debt_growth': 5.2},
            {'period': 'Q2 2017', 'revenue': 38.1, 'revenue_growth': 5.0, 'gross_profit': 14.8, 'gross_margin': 38.8, 'net_profit': 7.3, 'net_margin': 19.2, 'net_profit_growth': 17.0, 'debt': 29.0, 'debt_growth': 6.8},
            # 2016
            {'period': 'Q1 2017', 'revenue': 54.2, 'revenue_growth': 4.6, 'gross_profit': 21.3, 'gross_margin': 39.3, 'net_profit': 10.8, 'net_margin': 19.9, 'net_profit_growth': 4.9, 'debt': 27.2, 'debt_growth': 8.4},
            {'period': 'Q4 2016', 'revenue': 51.3, 'revenue_growth': -9.0, 'gross_profit': 20.0, 'gross_margin': 39.0, 'net_profit': 11.4, 'net_margin': 22.2, 'net_profit_growth': -19.4, 'debt': 25.1, 'debt_growth': 10.1},
            {'period': 'Q3 2016', 'revenue': 46.1, 'revenue_growth': -14.6, 'gross_profit': 17.9, 'gross_margin': 38.8, 'net_profit': 7.9, 'net_margin': 17.1, 'net_profit_growth': -27.0, 'debt': 22.8, 'debt_growth': 12.4},
            {'period': 'Q2 2016', 'revenue': 36.3, 'revenue_growth': -23.0, 'gross_profit': 14.3, 'gross_margin': 39.4, 'net_profit': 6.2, 'net_margin': 17.1, 'net_profit_growth': -34.0, 'debt': 20.3, 'debt_growth': 15.2}
        ],
        'yearly': [
            {'period': '2025', 'revenue': 394.3, 'revenue_growth': 2.8, 'gross_profit': 182.8, 'gross_margin': 46.4, 'net_profit': 101.9, 'net_margin': 25.8, 'net_profit_growth': 5.1, 'debt': 111.1, 'debt_growth': 11.2},
            {'period': '2024', 'revenue': 383.3, 'revenue_growth': -2.8, 'gross_profit': 178.4, 'gross_margin': 46.5, 'net_profit': 97.0, 'net_margin': 25.3, 'net_profit_growth': 0.1, 'debt': 99.9, 'debt_growth': -2.7},
            {'period': '2023', 'revenue': 394.3, 'revenue_growth': 7.8, 'gross_profit': 170.8, 'gross_margin': 43.3, 'net_profit': 96.9, 'net_margin': 24.6, 'net_profit_growth': 2.3, 'debt': 102.7, 'debt_growth': 23.1},
            {'period': '2022', 'revenue': 365.8, 'revenue_growth': 28.4, 'gross_profit': 152.8, 'gross_margin': 41.8, 'net_profit': 94.7, 'net_margin': 25.9, 'net_profit_growth': 20.4, 'debt': 83.4, 'debt_growth': 75.8},
            {'period': '2021', 'revenue': 284.9, 'revenue_growth': 33.3, 'gross_profit': 125.8, 'gross_margin': 44.2, 'net_profit': 78.6, 'net_margin': 27.6, 'net_profit_growth': 64.9, 'debt': 47.4, 'debt_growth': 56.0},
            {'period': '2020', 'revenue': 239.8, 'revenue_growth': 0.4, 'gross_profit': 91.8, 'gross_margin': 38.3, 'net_profit': 47.7, 'net_margin': 19.9, 'net_profit_growth': -7.2, 'debt': 30.4, 'debt_growth': -12.9},
            {'period': '2019', 'revenue': 235.7, 'revenue_growth': -2.0, 'gross_profit': 90.0, 'gross_margin': 38.2, 'net_profit': 51.4, 'net_margin': 21.8, 'net_profit_growth': 7.8, 'debt': 34.9, 'debt_growth': 8.1},
            {'period': '2018', 'revenue': 233.7, 'revenue_growth': 15.9, 'gross_profit': 90.0, 'gross_margin': 38.5, 'net_profit': 47.7, 'net_margin': 20.4, 'net_profit_growth': 23.2, 'debt': 32.3, 'debt_growth': 19.3},
            {'period': '2017', 'revenue': 202.1, 'revenue_growth': 6.3, 'gross_profit': 78.4, 'gross_margin': 38.8, 'net_profit': 38.7, 'net_margin': 19.1, 'net_profit_growth': 5.8, 'debt': 27.1, 'debt_growth': 8.4},
            {'period': '2016', 'revenue': 185.5, 'revenue_growth': -14.9, 'gross_profit': 73.6, 'gross_margin': 39.7, 'net_profit': 36.6, 'net_margin': 19.7, 'net_profit_growth': -24.3, 'debt': 25.0, 'debt_growth': 42.0}
        ],
        'debt': 111.1, 'debt_to_equity': 1.87, 'cash': 162.1,
        'regions': [
            {'name': 'Americas', 'revenue': 169.0, 'percent': 42.9},
            {'name': 'Europe', 'revenue': 101.3, 'percent': 25.7},
            {'name': 'China', 'revenue': 67.8, 'percent': 17.2},
            {'name': 'Japan', 'revenue': 26.0, 'percent': 6.6},
            {'name': 'Rest of APAC', 'revenue': 30.2, 'percent': 7.7}
        ],
        'segments': [
            {'name': 'iPhone', 'revenue': 200.6, 'percent': 50.9},
            {'name': 'Services', 'revenue': 85.2, 'percent': 21.6},
            {'name': 'Mac', 'revenue': 29.4, 'percent': 7.5},
            {'name': 'iPad', 'revenue': 28.3, 'percent': 7.2},
            {'name': 'Wearables', 'revenue': 50.8, 'percent': 12.9}
        ]
    },
    'MSFT': {
        'price': 420.55, 'pe': 36.8, 'forward_pe': 33.5, 'industry_pe': 31.5, 'peg': 2.8, 
        'market_cap': 3120, 'book_value': 38.50, 'pb_ratio': 10.9, 'name': 'Microsoft Corp.',
        'quarterly': [
            {'period': 'Q1 2026', 'revenue': 65.6, 'revenue_growth': 16.1, 'gross_profit': 46.2, 'gross_margin': 70.4, 'net_profit': 25.9, 'net_margin': 39.5, 'net_profit_growth': 18.2},
            {'period': 'Q4 2025', 'revenue': 64.7, 'revenue_growth': 16.5, 'gross_profit': 45.7, 'gross_margin': 70.6, 'net_profit': 24.1, 'net_margin': 37.3, 'net_profit_growth': 17.8}
        ],
        'yearly': [
            {'period': '2025', 'revenue': 245.1, 'revenue_growth': 15.7, 'gross_profit': 174.3, 'gross_margin': 71.1, 'net_profit': 95.2, 'net_margin': 38.8, 'net_profit_growth': 16.5}
        ],
        'debt': 97.7, 'debt_to_equity': 0.35, 'cash': 80.0,
        'regions': [
            {'name': 'United States', 'revenue': 124.5, 'percent': 50.8},
            {'name': 'EMEA', 'revenue': 69.1, 'percent': 28.2},
            {'name': 'APAC', 'revenue': 36.3, 'percent': 14.8}
        ],
        'segments': [
            {'name': 'Intelligent Cloud (Azure)', 'revenue': 96.8, 'percent': 39.5},
            {'name': 'Productivity (Office)', 'revenue': 80.1, 'percent': 32.7},
            {'name': 'Personal Computing (Windows)', 'revenue': 68.1, 'percent': 27.8}
        ]
    },
    'GOOGL': {
        'price': 140.22, 'pe': 24.5, 'forward_pe': 22.1, 'industry_pe': 31.5, 'peg': 1.8, 
        'market_cap': 1750, 'book_value': 28.35, 'pb_ratio': 4.9, 'name': 'Alphabet Inc.',
        'quarterly': [
            {'period': 'Q1 2026', 'revenue': 86.3, 'revenue_growth': 13.4, 'gross_profit': 49.2, 'gross_margin': 57.0, 'net_profit': 23.7, 'net_margin': 27.5, 'net_profit_growth': 14.5}
        ],
        'yearly': [
            {'period': '2025', 'revenue': 323.9, 'revenue_growth': 13.6, 'gross_profit': 183.9, 'gross_margin': 56.8, 'net_profit': 87.7, 'net_margin': 27.1, 'net_profit_growth': 15.2}
        ],
        'debt': 28.4, 'debt_to_equity': 0.07, 'cash': 110.9,
        'regions': [
            {'name': 'United States', 'revenue': 153.2, 'percent': 47.3},
            {'name': 'EMEA', 'revenue': 96.8, 'percent': 29.9},
            {'name': 'APAC', 'revenue': 55.4, 'percent': 17.1}
        ],
        'segments': [
            {'name': 'Google Search & Ads', 'revenue': 250.7, 'percent': 77.4},
            {'name': 'Google Cloud', 'revenue': 35.0, 'percent': 10.8},
            {'name': 'YouTube Ads', 'revenue': 33.0, 'percent': 10.2}
        ]
    },
    # Basic data for other tickers
    'TSLA': {'price': 195.50, 'pe': 62.4, 'name': 'Tesla Inc.'},
    'AMZN': {'price': 178.25, 'pe': 53.1, 'name': 'Amazon.com Inc.'},
    'NVDA': {'price': 875.28, 'pe': 70.8, 'name': 'NVIDIA Corp.'},
    'META': {'price': 502.19, 'pe': 32.1, 'name': 'Meta Platforms Inc.'},
    'BRK.B': {'price': 455.40, 'pe': 0, 'name': 'Berkshire Hathaway B'},
    'JPM': {'price': 215.18, 'pe': 13.5, 'name': 'JPMorgan Chase & Co.'},
    'JNJ': {'price': 148.27, 'pe': 21.8, 'name': 'Johnson & Johnson'}
}

def analyze_ticker(ticker: str) -> dict:
    """Fetch data and calculate valuation bands."""
    print(f"\nUsing demonstration data for {ticker}")
    
    # Get mock data
    if ticker in MOCK_DATA:
        stock_data = MOCK_DATA[ticker]
        current_price = stock_data['price']
        pe_ratio = stock_data['pe']
        company_name = stock_data['name']
    else:
        raise ValueError(f"Ticker {ticker} not found in demonstration data. Try: {', '.join(MOCK_DATA.keys())}")
    
    # Calculate fair value (simplified)
    pe_avg_5y = pe_ratio * 0.85 if pe_ratio else pe_ratio
    fair_value = current_price * (pe_avg_5y / pe_ratio) if pe_ratio else current_price
    
    # Get financial data if available
    ticker_data = MOCK_DATA.get(ticker, {})
    quarterly_data = ticker_data.get('quarterly', [])
    yearly_data = ticker_data.get('yearly', [])
    debt = ticker_data.get('debt')
    debt_to_equity = ticker_data.get('debt_to_equity')
    cash = ticker_data.get('cash')
    regions = ticker_data.get('regions', [])
    segments = ticker_data.get('segments', [])
    forward_pe = ticker_data.get('forward_pe')
    industry_pe = ticker_data.get('industry_pe')
    peg = ticker_data.get('peg')
    market_cap = ticker_data.get('market_cap')
    book_value = ticker_data.get('book_value')
    pb_ratio = ticker_data.get('pb_ratio')
    
    # Warren Buffett / Charlie Munger style analysis
    buffett_score = calculate_buffett_score(ticker_data, pe_ratio, current_price, fair_value)
    
    # Simple bands: ±15% and ±30% from fair value
    return {
        'ticker': ticker,
        'company_name': company_name,
        'current_price': round(current_price, 2),
        'fair_value': round(fair_value, 2),
        'strong_buy': round(fair_value * 0.70, 2),
        'buy': round(fair_value * 0.85, 2),
        'sell': round(fair_value * 1.15, 2),
        'strong_sell': round(fair_value * 1.30, 2),
        'pe_ratio': round(pe_ratio, 2) if pe_ratio else 'N/A',
        'forward_pe': forward_pe,
        'industry_pe': industry_pe,
        'peg': peg,
        'market_cap': market_cap,
        'book_value': book_value,
        'pb_ratio': pb_ratio,
        'recommendation': get_recommendation(current_price, fair_value),
        'quarterly': quarterly_data,
        'yearly': yearly_data,
        'debt': debt,
        'debt_to_equity': debt_to_equity,
        'cash': cash,
        'regions': regions,
        'segments': segments,
        'has_financials': len(quarterly_data) > 0,
        'buffett_analysis': buffett_score
    }

def calculate_buffett_score(ticker_data, pe_ratio, current_price, fair_value):
    """Generate Warren Buffett / Charlie Munger style investment analysis."""
    score = 0
    reasons = []
    warnings = []
    
    # Check profitability consistency (last 10 years)
    yearly = ticker_data.get('yearly', [])
    if len(yearly) >= 5:
        profitable_years = sum(1 for y in yearly if y.get('net_margin', 0) > 15)
        if profitable_years >= 4:
            score += 20
            reasons.append(f"✓ Consistent profitability: {profitable_years} out of {len(yearly)} years with >15% margins")
        else:
            warnings.append(f"⚠ Inconsistent margins: Only {profitable_years}/{len(yearly)} years with >15% net margin")
    
    # Check revenue growth trend
    if len(yearly) >= 3:
        recent_growth = yearly[0].get('revenue_growth', 0)
        if recent_growth > 10:
            score += 15
            reasons.append(f"✓ Strong revenue growth: {recent_growth}% (last year)")
        elif recent_growth < 0:
            warnings.append(f"⚠ Revenue declining: {recent_growth}% (last year)")
    
    # Check debt levels (Buffett prefers low debt)
    debt_to_equity = ticker_data.get('debt_to_equity')
    if debt_to_equity:
        if debt_to_equity < 0.5:
            score += 20
            reasons.append(f"✓ Conservative debt: D/E ratio {debt_to_equity} (Buffett likes <0.5)")
        elif debt_to_equity > 2.0:
            warnings.append(f"⚠ High debt burden: D/E ratio {debt_to_equity} (risky)")
        else:
            score += 10
            reasons.append(f"○ Moderate debt: D/E ratio {debt_to_equity}")
    
    # Check cash reserves (margin of safety)
    cash = ticker_data.get('cash')
    debt = ticker_data.get('debt')
    if cash and debt:
        if cash > debt:
            score += 15
            reasons.append(f"✓ Excellent liquidity: Cash ${cash}B > Debt ${debt}B")
        else:
            warnings.append(f"○ Cash ${cash}B < Debt ${debt}B (watch liquidity)")
    
    # Check valuation (price vs fair value)
    price_ratio = current_price / fair_value if fair_value else 1
    if price_ratio < 0.85:
        score += 20
        reasons.append(f"✓ Trading at discount: {int((1-price_ratio)*100)}% below fair value (margin of safety)")
    elif price_ratio > 1.3:
        score -= 10
        warnings.append(f"⚠ Overvalued: {int((price_ratio-1)*100)}% above fair value")
    
    # Check PEG ratio (Peter Lynch's metric, Munger approved)
    peg = ticker_data.get('peg')
    if peg:
        if peg < 1.5:
            score += 10
            reasons.append(f"✓ Reasonable PEG ratio: {peg} (growth at reasonable price)")
        elif peg > 3.0:
            warnings.append(f"⚠ High PEG ratio: {peg} (expensive for growth)")
    
    # Final recommendation
    if score >= 70:
        verdict = "STRONG BUY - Exceptional Buffett-style opportunity"
        confidence = "Very High"
    elif score >= 50:
        verdict = "BUY - Good long-term investment characteristics"
        confidence = "High"
    elif score >= 30:
        verdict = "HOLD - Fair business, but wait for better price"
        confidence = "Moderate"
    else:
        verdict = "PASS - Does not meet value investing criteria"
        confidence = "Low"
    
    return {
        'score': score,
        'verdict': verdict,
        'confidence': confidence,
        'reasons': reasons,
        'warnings': warnings
    }

def get_recommendation(price, fair_value):
    ratio = price / fair_value if fair_value else 1
    if ratio < 0.85: return "STRONG BUY"
    elif ratio < 1.0: return "BUY"
    elif ratio < 1.15: return "HOLD"
    elif ratio < 1.30: return "SELL"
    else: return "STRONG SELL"
