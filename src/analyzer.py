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

def _get_screener_data(ticker):
    """Get data from screener mock if available."""
    try:
        from screener import MOCK_STOCK_DATA, CONGRESS_DATA
        return MOCK_STOCK_DATA.get(ticker), CONGRESS_DATA.get(ticker, [])
    except Exception:
        return None, []


# SWOT data for major stocks
SWOT_DATA = {
    'AAPL': {'strengths':['Strongest brand loyalty in tech','Services revenue growing 15%+ YoY','$162B cash reserve','Ecosystem lock-in (1.2B active devices)'],
             'weaknesses':['iPhone revenue >50% of total (concentration)','China market risk (17% revenue)','Limited AI/cloud presence vs peers','Premium pricing limits TAM in emerging markets'],
             'opportunities':['AR/VR (Vision Pro ecosystem)','India market expansion','AI integration across products','Healthcare wearables'],
             'threats':['EU antitrust regulation (DMA)','China geopolitical tensions','Samsung/Google Pixel competition','Services revenue regulation']},
    'MSFT': {'strengths':['Azure #2 cloud (30% market share)','Office 365 recurring revenue','GitHub + LinkedIn ecosystem','Enterprise AI (Copilot) leader'],
             'weaknesses':['Gaming division underperforming','Surface hardware low margins','Legacy Windows declining','Activision integration risk'],
             'opportunities':['AI Copilot monetization ($30/user/mo)','Sovereign cloud contracts','Healthcare cloud','Edge computing'],
             'threats':['AWS competition in cloud','Google Workspace gaining share','Antitrust scrutiny','Open-source AI alternatives']},
    'NVDA': {'strengths':['90%+ market share in AI training GPUs','CUDA ecosystem moat','Data center revenue +200% YoY','Full-stack AI platform'],
             'weaknesses':['Customer concentration (hyperscalers)','China export restrictions','Cyclical semiconductor demand','High valuation expectations'],
             'opportunities':['Sovereign AI infrastructure','Automotive (self-driving)','Robotics / Omniverse','Edge AI inference'],
             'threats':['AMD MI300 competition','Custom chips (Google TPU, Amazon Trainium)','AI winter risk','Supply chain (TSMC dependency)']},
}

# Management data
MANAGEMENT_DATA = {
    'AAPL': [{'name':'Tim Cook','role':'CEO','since':'2011','compensation':'$63M'},{'name':'Luca Maestri','role':'CFO','since':'2014','compensation':'$27M'},{'name':'Craig Federighi','role':'SVP Software','since':'2012','compensation':'$26M'}],
    'MSFT': [{'name':'Satya Nadella','role':'CEO & Chairman','since':'2014','compensation':'$55M'},{'name':'Amy Hood','role':'CFO','since':'2013','compensation':'$20M'},{'name':'Judson Althoff','role':'President & CRO','since':'2024','compensation':'$18M'}],
    'NVDA': [{'name':'Jensen Huang','role':'CEO & Founder','since':'1993','compensation':'$34M'},{'name':'Colette Kress','role':'CFO','since':'2013','compensation':'$20M'}],
}

# Insider Trading Activity (recent transactions)
INSIDER_TRADING = {
    'AAPL': [
        {'name':'Tim Cook','role':'CEO','date':'2026-03-15','type':'Sell','shares':200000,'price':225.40,'value':'$45.1M'},
        {'name':'Luca Maestri','role':'CFO','date':'2026-02-28','type':'Sell','shares':50000,'price':221.80,'value':'$11.1M'},
        {'name':'Craig Federighi','role':'SVP Software','date':'2026-01-20','type':'Sell','shares':30000,'price':218.50,'value':'$6.6M'},
        {'name':'Jeff Williams','role':'COO','date':'2025-12-10','type':'Sell','shares':45000,'price':230.10,'value':'$10.4M'},
        {'name':'Deirdre O\'Brien','role':'SVP Retail','date':'2025-11-15','type':'Sell','shares':15000,'price':228.75,'value':'$3.4M'},
        {'name':'Tim Cook','role':'CEO','date':'2025-10-01','type':'Sell','shares':300000,'price':215.20,'value':'$64.6M'},
    ],
    'MSFT': [
        {'name':'Satya Nadella','role':'CEO','date':'2026-04-10','type':'Sell','shares':100000,'price':445.30,'value':'$44.5M'},
        {'name':'Amy Hood','role':'CFO','date':'2026-03-05','type':'Sell','shares':25000,'price':440.20,'value':'$11.0M'},
        {'name':'Brad Smith','role':'Vice Chair','date':'2026-01-15','type':'Sell','shares':35000,'price':430.50,'value':'$15.1M'},
        {'name':'Judson Althoff','role':'President','date':'2025-12-20','type':'Buy','shares':5000,'price':418.90,'value':'$2.1M'},
        {'name':'Satya Nadella','role':'CEO','date':'2025-11-01','type':'Sell','shares':150000,'price':425.60,'value':'$63.8M'},
    ],
    'NVDA': [
        {'name':'Jensen Huang','role':'CEO','date':'2026-04-22','type':'Sell','shares':240000,'price':132.50,'value':'$31.8M'},
        {'name':'Jensen Huang','role':'CEO','date':'2026-03-18','type':'Sell','shares':240000,'price':128.40,'value':'$30.8M'},
        {'name':'Colette Kress','role':'CFO','date':'2026-02-10','type':'Sell','shares':50000,'price':125.80,'value':'$6.3M'},
        {'name':'Jensen Huang','role':'CEO','date':'2026-01-15','type':'Sell','shares':240000,'price':140.20,'value':'$33.6M'},
        {'name':'Debora Shoquist','role':'EVP Operations','date':'2025-12-05','type':'Sell','shares':20000,'price':138.90,'value':'$2.8M'},
    ],
    'GOOGL': [
        {'name':'Sundar Pichai','role':'CEO','date':'2026-03-20','type':'Sell','shares':22000,'price':175.80,'value':'$3.9M'},
        {'name':'Ruth Porat','role':'President & CIO','date':'2026-02-14','type':'Sell','shares':15500,'price':172.30,'value':'$2.7M'},
        {'name':'Prabhakar Raghavan','role':'SVP Knowledge','date':'2025-12-18','type':'Sell','shares':8000,'price':168.50,'value':'$1.3M'},
    ],
    'META': [
        {'name':'Mark Zuckerberg','role':'CEO','date':'2026-04-05','type':'Sell','shares':75000,'price':590.20,'value':'$44.3M'},
        {'name':'Mark Zuckerberg','role':'CEO','date':'2026-03-01','type':'Sell','shares':75000,'price':580.50,'value':'$43.5M'},
        {'name':'Susan Li','role':'CFO','date':'2026-02-20','type':'Sell','shares':5000,'price':575.80,'value':'$2.9M'},
        {'name':'Mark Zuckerberg','role':'CEO','date':'2026-01-10','type':'Sell','shares':75000,'price':560.30,'value':'$42.0M'},
    ],
}

# Management ownership percentage
MGMT_HOLDINGS = {
    'AAPL': {'insider_pct': 0.07, 'institutional_pct': 60.5, 'retail_pct': 39.43, 'top_holders': [
        {'name':'Tim Cook','shares':'3.28M','pct':0.021},
        {'name':'Art Levinson','shares':'1.13M','pct':0.007},
        {'name':'Jeff Williams','shares':'0.89M','pct':0.006},
    ]},
    'MSFT': {'insider_pct': 1.38, 'institutional_pct': 72.8, 'retail_pct': 25.82, 'top_holders': [
        {'name':'Satya Nadella','shares':'1.72M','pct':0.023},
        {'name':'Brad Smith','shares':'0.85M','pct':0.011},
        {'name':'Amy Hood','shares':'0.42M','pct':0.006},
    ]},
    'NVDA': {'insider_pct': 4.23, 'institutional_pct': 65.3, 'retail_pct': 30.47, 'top_holders': [
        {'name':'Jensen Huang','shares':'86.7M','pct':3.55},
        {'name':'Mark Stevens','shares':'6.8M','pct':0.28},
        {'name':'Colette Kress','shares':'0.52M','pct':0.02},
    ]},
    'GOOGL': {'insider_pct': 11.4, 'institutional_pct': 62.1, 'retail_pct': 26.5, 'top_holders': [
        {'name':'Larry Page','shares':'18.5M','pct':5.8},
        {'name':'Sergey Brin','shares':'17.2M','pct':5.4},
        {'name':'Sundar Pichai','shares':'0.24M','pct':0.008},
    ]},
    'META': {'insider_pct': 13.6, 'institutional_pct': 59.8, 'retail_pct': 26.6, 'top_holders': [
        {'name':'Mark Zuckerberg','shares':'350M','pct':13.5},
        {'name':'Susan Li','shares':'0.05M','pct':0.002},
    ]},
}

# Company strategic investments / subsidiaries
COMPANY_INVESTMENTS = {
    'AAPL': [
        {'company':'Shazam','year':2018,'amount':'$400M','type':'Acquisition','status':'Integrated'},
        {'company':'Intel Modem Division','year':2019,'amount':'$1B','type':'Acquisition','status':'Integrated (5G modems)'},
        {'company':'Beats Electronics','year':2014,'amount':'$3B','type':'Acquisition','status':'Active subsidiary'},
        {'company':'Lattice Data','year':2017,'amount':'$200M','type':'Acquisition','status':'Integrated (AI/ML)'},
        {'company':'Drive.ai','year':2019,'amount':'$77M','type':'Acqui-hire','status':'Self-driving R&D'},
        {'company':'Didi Global (stake)','year':2016,'amount':'$1B','type':'Strategic Investment','status':'Divested 2021'},
    ],
    'MSFT': [
        {'company':'Activision Blizzard','year':2023,'amount':'$68.7B','type':'Acquisition','status':'Active subsidiary'},
        {'company':'LinkedIn','year':2016,'amount':'$26.2B','type':'Acquisition','status':'Active subsidiary'},
        {'company':'Nuance Communications','year':2022,'amount':'$19.7B','type':'Acquisition','status':'Integrated (AI healthcare)'},
        {'company':'GitHub','year':2018,'amount':'$7.5B','type':'Acquisition','status':'Active subsidiary'},
        {'company':'OpenAI','year':2023,'amount':'$13B','type':'Strategic Investment','status':'49% economic interest'},
        {'company':'Mistral AI','year':2024,'amount':'$16M','type':'Strategic Investment','status':'Partnership'},
    ],
    'NVDA': [
        {'company':'Arm Holdings (attempted)','year':2022,'amount':'$40B','type':'Acquisition (Failed)','status':'Blocked by regulators'},
        {'company':'Mellanox Technologies','year':2020,'amount':'$6.9B','type':'Acquisition','status':'Integrated (networking)'},
        {'company':'CoreWeave','year':2024,'amount':'$100M','type':'Strategic Investment','status':'Cloud GPU partner'},
        {'company':'Recursion Pharmaceuticals','year':2023,'amount':'$50M','type':'Strategic Investment','status':'AI drug discovery'},
        {'company':'SoundHound AI','year':2024,'amount':'$3.7M','type':'Strategic Investment','status':'Voice AI'},
    ],
    'GOOGL': [
        {'company':'Wiz','year':2025,'amount':'$32B','type':'Acquisition','status':'Pending regulatory'},
        {'company':'Mandiant','year':2022,'amount':'$5.4B','type':'Acquisition','status':'Integrated (cybersecurity)'},
        {'company':'Fitbit','year':2021,'amount':'$2.1B','type':'Acquisition','status':'Integrated (Pixel Watch)'},
        {'company':'DeepMind','year':2014,'amount':'$500M','type':'Acquisition','status':'Core AI research'},
        {'company':'Anthropic','year':2023,'amount':'$2B','type':'Strategic Investment','status':'AI safety partner'},
        {'company':'SpaceX (stake)','year':2015,'amount':'$900M','type':'Strategic Investment','status':'Starlink partnership'},
    ],
    'META': [
        {'company':'Oculus VR','year':2014,'amount':'$2B','type':'Acquisition','status':'Renamed Meta Quest'},
        {'company':'WhatsApp','year':2014,'amount':'$19B','type':'Acquisition','status':'Active (2B+ users)'},
        {'company':'Instagram','year':2012,'amount':'$1B','type':'Acquisition','status':'Active (2B+ users)'},
        {'company':'Jio Platforms (stake)','year':2020,'amount':'$5.7B','type':'Strategic Investment','status':'India commerce'},
        {'company':'Mapillary','year':2020,'amount':'Undisclosed','type':'Acquisition','status':'Integrated (mapping)'},
    ],
}


def analyze_ticker(ticker: str) -> dict:
    """Fetch data and calculate comprehensive analysis."""
    # Try detailed mock data first
    if ticker in MOCK_DATA:
        stock_data = MOCK_DATA[ticker]
        current_price = stock_data['price']
        pe_ratio = stock_data['pe']
        company_name = stock_data['name']
    else:
        # Fallback to screener data
        screener_data, _ = _get_screener_data(ticker)
        if screener_data:
            current_price = screener_data['price']
            pe_ratio = screener_data.get('pe_ratio', 0)
            company_name = screener_data['name']
            # Build minimal stock_data from screener
            MOCK_DATA[ticker] = {
                'price': current_price, 'pe': pe_ratio, 'name': company_name,
                'forward_pe': screener_data.get('forward_pe'), 'peg': screener_data.get('peg_ratio'),
                'market_cap': screener_data.get('market_cap', 0) * 1000 if screener_data.get('market_cap', 0) < 10 else screener_data.get('market_cap', 0),
                'debt_to_equity': screener_data.get('debt_to_equity'),
                'debt': screener_data.get('total_debt'), 'cash': screener_data.get('total_cash'),
                'quarterly': [], 'yearly': [], 'regions': [], 'segments': []
            }
            stock_data = MOCK_DATA[ticker]
        else:
            raise ValueError(f"Ticker {ticker} not found. Try: AAPL, MSFT, NVDA, GOOGL, META, AMZN, TSM, etc.")

    # Calculate fair value
    pe_avg_5y = pe_ratio * 0.85 if pe_ratio else pe_ratio
    fair_value = current_price * (pe_avg_5y / pe_ratio) if pe_ratio else current_price

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

    # Buffett analysis
    buffett_score = calculate_buffett_score(ticker_data, pe_ratio, current_price, fair_value)

    # Get screener + congress data
    screener_info, congress_pols = _get_screener_data(ticker)

    # Build comprehensive result
    result = {
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
        'buffett_analysis': buffett_score,
        # New comprehensive sections
        'sector': screener_info.get('sector', 'Technology') if screener_info else 'Technology',
        'industry': screener_info.get('industry', '') if screener_info else '',
        'beta': screener_info.get('beta', 1.0) if screener_info else 1.0,
        'dividend_yield': screener_info.get('dividend_yield', 0) if screener_info else 0,
        'revenue_growth': screener_info.get('revenue_growth', 0) if screener_info else 0,
        'profit_margin': screener_info.get('profit_margin', 0) if screener_info else 0,
        'gross_margin': screener_info.get('gross_margin', 0) if screener_info else 0,
        'roe': screener_info.get('roe', 0) if screener_info else 0,
        'current_ratio': screener_info.get('current_ratio', 0) if screener_info else 0,
        'fifty_two_week_high': screener_info.get('fifty_two_week_high', 0) if screener_info else 0,
        'fifty_two_week_low': screener_info.get('fifty_two_week_low', 0) if screener_info else 0,
        'analyst_target': screener_info.get('analyst_target', 0) if screener_info else 0,
        'swot': SWOT_DATA.get(ticker),
        'management': MANAGEMENT_DATA.get(ticker, []),
        'congress_politicians': congress_pols,
        'insider_trading': INSIDER_TRADING.get(ticker, []),
        'mgmt_holdings': MGMT_HOLDINGS.get(ticker),
        'company_investments': COMPANY_INVESTMENTS.get(ticker, []),
        'expert_scores': calculate_expert_scores(ticker_data, screener_info, pe_ratio, current_price, fair_value),
    }
    return result

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


def calculate_expert_scores(ticker_data, screener_info, pe_ratio, current_price, fair_value):
    """
    Multi-investor scoring engine. Each legendary investor's philosophy is modeled
    with weighted parameters reflecting their actual investment style.
    Score 0-100 per investor. Final AI score is a weighted composite.
    """
    data = screener_info or {}
    price = current_price or 0
    fv = fair_value or price

    # Common metrics
    de = data.get('debt_to_equity', 0) or ticker_data.get('debt_to_equity', 0) or 0
    pe = pe_ratio or 0
    fwd_pe = data.get('forward_pe', 0) or ticker_data.get('forward_pe', 0) or 0
    peg = data.get('peg_ratio', 0) or ticker_data.get('peg', 0) or 0
    roe = data.get('roe', 0) or 0
    margin = data.get('profit_margin', 0) or 0
    gross_margin = data.get('gross_margin', 0) or 0
    rev_growth = data.get('revenue_growth', 0) or 0
    div_yield = data.get('dividend_yield', 0) or 0
    beta = data.get('beta', 1.0) or 1.0
    current_ratio = data.get('current_ratio', 0) or 0
    cash = ticker_data.get('cash', 0) or 0
    debt = ticker_data.get('debt', 0) or 0
    mc = data.get('market_cap', 0) or ticker_data.get('market_cap', 0) or 0
    yearly = ticker_data.get('yearly', [])
    price_to_fv = price / fv if fv else 1.0

    def _clamp(v, lo=0, hi=100):
        return max(lo, min(hi, int(v)))

    # ═══════════════════════════════════════════════════════════════
    # 1. WARREN BUFFETT - Moat, consistent earnings, low debt, margin of safety
    # ═══════════════════════════════════════════════════════════════
    buffett = 0
    buffett_reasons = []
    # Consistent profitability (30 pts)
    if len(yearly) >= 5:
        profitable = sum(1 for y in yearly[:5] if y.get('net_margin', 0) > 15)
        buffett += profitable * 6
        if profitable >= 4: buffett_reasons.append(f"Consistent margins ({profitable}/5 yrs >15%)")
    elif margin > 20: buffett += 20; buffett_reasons.append(f"Strong margin {margin:.1f}%")
    elif margin > 10: buffett += 12
    # Low debt (20 pts)
    if de < 0.3: buffett += 20; buffett_reasons.append("Very low debt")
    elif de < 0.7: buffett += 15
    elif de < 1.2: buffett += 8
    elif de > 2.0: buffett -= 5
    # ROE > 15% (20 pts)
    if roe > 25: buffett += 20; buffett_reasons.append(f"Excellent ROE {roe:.0f}%")
    elif roe > 15: buffett += 15
    elif roe > 10: buffett += 8
    # Margin of safety (20 pts)
    if price_to_fv < 0.80: buffett += 20; buffett_reasons.append("Strong margin of safety")
    elif price_to_fv < 0.95: buffett += 14
    elif price_to_fv < 1.10: buffett += 8
    # Moat indicators - high gross margin (10 pts)
    if gross_margin > 60: buffett += 10; buffett_reasons.append("Wide moat (high gross margin)")
    elif gross_margin > 40: buffett += 6
    elif gross_margin > 25: buffett += 3
    buffett = _clamp(buffett)

    # ═══════════════════════════════════════════════════════════════
    # 2. BENJAMIN GRAHAM - Deep value, asset-heavy, margin of safety, low P/E
    # ═══════════════════════════════════════════════════════════════
    graham = 0
    graham_reasons = []
    # Low P/E (25 pts) - Graham liked P/E < 15
    if pe and 0 < pe < 10: graham += 25; graham_reasons.append(f"Very low P/E ({pe:.1f})")
    elif pe and 0 < pe < 15: graham += 20; graham_reasons.append(f"Low P/E ({pe:.1f})")
    elif pe and 0 < pe < 20: graham += 12
    elif pe and 0 < pe < 25: graham += 5
    # Current ratio > 2 (20 pts)
    if current_ratio > 2.5: graham += 20; graham_reasons.append(f"Strong current ratio {current_ratio:.1f}")
    elif current_ratio > 2.0: graham += 16
    elif current_ratio > 1.5: graham += 10
    elif current_ratio > 1.0: graham += 5
    # Low debt/equity (20 pts)
    if de < 0.3: graham += 20; graham_reasons.append("Minimal debt")
    elif de < 0.5: graham += 15
    elif de < 1.0: graham += 8
    # Dividend (15 pts) - Graham liked dividend payers
    if div_yield > 3.0: graham += 15; graham_reasons.append(f"Good dividend {div_yield:.1f}%")
    elif div_yield > 2.0: graham += 12
    elif div_yield > 1.0: graham += 7
    elif div_yield > 0: graham += 3
    # Earnings stability (20 pts)
    if len(yearly) >= 5:
        positive_yrs = sum(1 for y in yearly[:5] if y.get('net_profit', 0) > 0)
        graham += positive_yrs * 4
        if positive_yrs >= 5: graham_reasons.append("5/5 years profitable")
    elif margin > 10: graham += 12
    graham = _clamp(graham)

    # ═══════════════════════════════════════════════════════════════
    # 3. PETER LYNCH - Growth at reasonable price (GARP), PEG ratio king
    # ═══════════════════════════════════════════════════════════════
    lynch = 0
    lynch_reasons = []
    # PEG ratio (30 pts) - Lynch's key metric
    if peg and 0 < peg < 0.8: lynch += 30; lynch_reasons.append(f"Excellent PEG {peg:.1f} (steal)")
    elif peg and 0 < peg < 1.0: lynch += 25; lynch_reasons.append(f"Great PEG {peg:.1f}")
    elif peg and 0 < peg < 1.5: lynch += 18; lynch_reasons.append(f"Fair PEG {peg:.1f}")
    elif peg and 0 < peg < 2.0: lynch += 10
    elif peg and peg > 3.0: lynch -= 5
    # Revenue growth (25 pts) - Lynch loved growth stories
    if rev_growth > 30: lynch += 25; lynch_reasons.append(f"Explosive growth {rev_growth:.0f}%")
    elif rev_growth > 20: lynch += 20; lynch_reasons.append(f"Strong growth {rev_growth:.0f}%")
    elif rev_growth > 10: lynch += 14
    elif rev_growth > 5: lynch += 8
    elif rev_growth < 0: lynch -= 5
    # Earnings growth (20 pts)
    if len(yearly) >= 2:
        eg = yearly[0].get('net_profit_growth', 0)
        if eg > 25: lynch += 20; lynch_reasons.append(f"Earnings surging +{eg:.0f}%")
        elif eg > 15: lynch += 15
        elif eg > 5: lynch += 8
    elif margin > 15: lynch += 10
    # Manageable debt (15 pts)
    if de < 0.5: lynch += 15
    elif de < 1.0: lynch += 10
    elif de < 1.5: lynch += 5
    # Institutional ownership not too high (10 pts) - Lynch liked undiscovered gems
    if mc and mc < 50: lynch += 10; lynch_reasons.append("Under-followed (mid/small cap)")
    elif mc and mc < 200: lynch += 5
    lynch = _clamp(lynch)

    # ═══════════════════════════════════════════════════════════════
    # 4. GEORGE SOROS - Macro trends, reflexivity, momentum, bold bets
    # ═══════════════════════════════════════════════════════════════
    soros = 0
    soros_reasons = []
    # Momentum / trend strength (30 pts)
    if rev_growth > 40: soros += 30; soros_reasons.append(f"Massive momentum +{rev_growth:.0f}%")
    elif rev_growth > 20: soros += 22; soros_reasons.append(f"Strong trend +{rev_growth:.0f}%")
    elif rev_growth > 10: soros += 14
    elif rev_growth > 0: soros += 6
    # High beta = macro sensitivity (20 pts) - Soros bets on macro
    if beta > 1.5: soros += 20; soros_reasons.append(f"High beta {beta:.2f} (macro play)")
    elif beta > 1.2: soros += 15
    elif beta > 1.0: soros += 10
    elif beta < 0.8: soros += 5
    # Market cap momentum (20 pts) - large caps that are accelerating
    if mc and mc > 500 and rev_growth > 15: soros += 20; soros_reasons.append("Mega-cap with acceleration")
    elif mc and mc > 100 and rev_growth > 10: soros += 12
    elif rev_growth > 25: soros += 15
    # Sector tailwinds - AI/Tech/Energy (15 pts)
    sector = data.get('sector', '')
    if sector in ('Technology',) and rev_growth > 15: soros += 15; soros_reasons.append("Tech sector tailwind")
    elif sector in ('Energy', 'Financial Services') and rev_growth > 5: soros += 10
    # Reflexivity - price above fair value can sustain (15 pts)
    if price_to_fv > 1.0 and rev_growth > 20: soros += 15; soros_reasons.append("Reflexive momentum (growth justifies premium)")
    elif price_to_fv < 0.9 and rev_growth > 10: soros += 10
    soros = _clamp(soros)

    # ═══════════════════════════════════════════════════════════════
    # 5. CHARLIE MUNGER - Quality at fair price, mental models, moats
    # ═══════════════════════════════════════════════════════════════
    munger = 0
    munger_reasons = []
    # Business quality - high margins (30 pts)
    if gross_margin > 65: munger += 30; munger_reasons.append(f"Exceptional business quality (GM {gross_margin:.0f}%)")
    elif gross_margin > 50: munger += 22; munger_reasons.append(f"High-quality business (GM {gross_margin:.0f}%)")
    elif gross_margin > 35: munger += 12
    # ROE - capital efficiency (25 pts)
    if roe > 30: munger += 25; munger_reasons.append(f"Outstanding capital efficiency (ROE {roe:.0f}%)")
    elif roe > 20: munger += 18
    elif roe > 15: munger += 12
    elif roe > 10: munger += 5
    # Not overpaying - fair price (25 pts)
    if pe and 0 < pe < 25 and gross_margin > 40: munger += 25; munger_reasons.append("Quality at reasonable price")
    elif pe and 0 < pe < 35 and gross_margin > 50: munger += 18
    elif pe and 0 < pe < 40: munger += 8
    # Durable competitive advantage (20 pts)
    if margin > 25 and gross_margin > 55: munger += 20; munger_reasons.append("Durable competitive advantage")
    elif margin > 15 and gross_margin > 40: munger += 12
    elif margin > 10: munger += 5
    munger = _clamp(munger)

    # ═══════════════════════════════════════════════════════════════
    # 6. RAY DALIO - All-weather, diversification, risk parity, macro
    # ═══════════════════════════════════════════════════════════════
    dalio = 0
    dalio_reasons = []
    # Low volatility / stability (25 pts)
    if beta < 0.8: dalio += 25; dalio_reasons.append(f"Low volatility (beta {beta:.2f})")
    elif beta < 1.0: dalio += 20; dalio_reasons.append("Below-market volatility")
    elif beta < 1.2: dalio += 12
    elif beta > 1.5: dalio += 3
    # Consistent earnings (25 pts)
    if len(yearly) >= 5:
        consistent = sum(1 for y in yearly[:5] if y.get('revenue_growth', 0) > 0)
        dalio += consistent * 5
        if consistent >= 4: dalio_reasons.append(f"Consistent revenue growth ({consistent}/5 yrs)")
    elif rev_growth > 0: dalio += 10
    # Dividend / income (20 pts)
    if div_yield > 3.0: dalio += 20; dalio_reasons.append(f"Income stream {div_yield:.1f}%")
    elif div_yield > 2.0: dalio += 15
    elif div_yield > 1.0: dalio += 8
    elif div_yield > 0: dalio += 3
    # Balance sheet strength (15 pts)
    if de < 0.5 and current_ratio > 1.5: dalio += 15; dalio_reasons.append("Strong balance sheet")
    elif de < 1.0 and current_ratio > 1.0: dalio += 10
    elif de < 1.5: dalio += 5
    # Size / liquidity (15 pts) - Dalio prefers large liquid names
    if mc and mc > 200: dalio += 15; dalio_reasons.append("Large liquid position")
    elif mc and mc > 50: dalio += 10
    elif mc and mc > 10: dalio += 5
    dalio = _clamp(dalio)

    # ═══════════════════════════════════════════════════════════════
    # 7. JOHN BOGLE - Index-like quality, low cost, long-term, broad market
    # ═══════════════════════════════════════════════════════════════
    bogle = 0
    bogle_reasons = []
    # Large diversified company (20 pts)
    if mc and mc > 500: bogle += 20; bogle_reasons.append("Mega-cap blue chip")
    elif mc and mc > 100: bogle += 15; bogle_reasons.append("Large-cap quality")
    elif mc and mc > 30: bogle += 8
    # Dividend (25 pts)
    if div_yield > 2.5: bogle += 25; bogle_reasons.append(f"Solid income {div_yield:.1f}%")
    elif div_yield > 1.5: bogle += 18
    elif div_yield > 0.5: bogle += 10
    elif div_yield > 0: bogle += 4
    # Low volatility (20 pts)
    if beta < 0.9: bogle += 20; bogle_reasons.append("Low risk profile")
    elif beta < 1.1: bogle += 15
    elif beta < 1.3: bogle += 8
    # Long-term earnings track record (20 pts)
    if len(yearly) >= 5:
        pos = sum(1 for y in yearly[:5] if y.get('net_profit', 0) > 0)
        bogle += pos * 4
        if pos >= 5: bogle_reasons.append("Proven long-term profitability")
    elif margin > 10: bogle += 12
    # Reasonable valuation (15 pts)
    if pe and 10 < pe < 25: bogle += 15; bogle_reasons.append("Reasonable valuation")
    elif pe and 0 < pe < 35: bogle += 8
    bogle = _clamp(bogle)

    # ═══════════════════════════════════════════════════════════════
    # 8. STANLEY DRUCKENMILLER - Concentrated bets, growth + momentum
    # ═══════════════════════════════════════════════════════════════
    druck = 0
    druck_reasons = []
    # Earnings acceleration (30 pts)
    if len(yearly) >= 2:
        eg = yearly[0].get('net_profit_growth', 0)
        if eg > 30: druck += 30; druck_reasons.append(f"Earnings accelerating +{eg:.0f}%")
        elif eg > 20: druck += 22
        elif eg > 10: druck += 14
        elif eg > 0: druck += 6
    elif rev_growth > 20: druck += 18
    # Revenue momentum (25 pts)
    if rev_growth > 40: druck += 25; druck_reasons.append(f"Revenue momentum +{rev_growth:.0f}%")
    elif rev_growth > 25: druck += 20
    elif rev_growth > 15: druck += 13
    elif rev_growth > 5: druck += 6
    # Forward P/E compression (20 pts) - growth making it cheaper
    if fwd_pe and pe and fwd_pe < pe * 0.75: druck += 20; druck_reasons.append("P/E compressing rapidly")
    elif fwd_pe and pe and fwd_pe < pe * 0.85: druck += 14
    elif fwd_pe and pe and fwd_pe < pe: druck += 8
    # Market leadership (15 pts)
    if mc and mc > 500 and rev_growth > 15: druck += 15; druck_reasons.append("Market leader with momentum")
    elif mc and mc > 100 and rev_growth > 20: druck += 12
    elif rev_growth > 30: druck += 10
    # Risk/reward (10 pts)
    if price_to_fv < 0.9 and rev_growth > 10: druck += 10; druck_reasons.append("Asymmetric risk/reward")
    elif price_to_fv < 1.0: druck += 5
    druck = _clamp(druck)

    # ═══════════════════════════════════════════════════════════════
    # 9. CARL ICAHN - Activist value, undervalued assets, catalysts
    # ═══════════════════════════════════════════════════════════════
    icahn = 0
    icahn_reasons = []
    # Deep discount to fair value (30 pts)
    if price_to_fv < 0.70: icahn += 30; icahn_reasons.append("Deeply undervalued (activist opportunity)")
    elif price_to_fv < 0.85: icahn += 22; icahn_reasons.append("Undervalued asset")
    elif price_to_fv < 0.95: icahn += 12
    # Low P/E (20 pts)
    if pe and 0 < pe < 10: icahn += 20; icahn_reasons.append(f"Cheap earnings (P/E {pe:.1f})")
    elif pe and 0 < pe < 15: icahn += 15
    elif pe and 0 < pe < 20: icahn += 8
    # Cash on balance sheet (20 pts) - hidden value
    if cash and debt and cash > debt * 1.5: icahn += 20; icahn_reasons.append("Cash-rich (hidden value)")
    elif cash and debt and cash > debt: icahn += 14
    elif cash and cash > 0: icahn += 6
    # Small/mid cap (more activism opportunities) (15 pts)
    if mc and mc < 20: icahn += 15; icahn_reasons.append("Small cap (activism target)")
    elif mc and mc < 80: icahn += 10
    elif mc and mc < 200: icahn += 5
    # Dividend / buyback potential (15 pts)
    if div_yield > 3.0: icahn += 10
    if de < 0.5: icahn += 5; icahn_reasons.append("Low debt (can lever for buybacks)")
    icahn = _clamp(icahn)

    # ═══════════════════════════════════════════════════════════════
    # 10. AI ANTHROPIC MODEL - Composite weighted score + macro overlay
    # Weights each investor's methodology by relevance to current market
    # ═══════════════════════════════════════════════════════════════
    # Macro environment assumptions (2026): AI boom, high rates, moderate growth
    macro_weights = {
        'buffett': 0.15,      # Always relevant
        'graham': 0.08,       # Less relevant in growth era
        'lynch': 0.15,        # GARP very relevant
        'soros': 0.12,        # Macro matters in 2026
        'munger': 0.14,       # Quality always matters
        'dalio': 0.08,        # Risk parity perspective
        'bogle': 0.06,        # Passive baseline
        'druckenmiller': 0.14, # Momentum key in AI era
        'icahn': 0.08,        # Activist value
    }

    scores_raw = {
        'buffett': buffett, 'graham': graham, 'lynch': lynch,
        'soros': soros, 'munger': munger, 'dalio': dalio,
        'bogle': bogle, 'druckenmiller': druck, 'icahn': icahn
    }

    ai_composite = sum(scores_raw[k] * macro_weights[k] for k in macro_weights)

    # Apply macro adjustments
    # AI/Tech sector premium in 2026
    sector = data.get('sector', '')
    if sector == 'Technology' and rev_growth > 15: ai_composite += 5
    # Penalize high debt in high-rate environment
    if de > 2.0: ai_composite -= 4
    # Reward forward PE compression
    if fwd_pe and pe and fwd_pe < pe * 0.8: ai_composite += 3
    # Penalize no earnings
    if pe == 0 and margin < 0: ai_composite -= 5

    ai_score = _clamp(int(ai_composite))

    # AI verdict
    if ai_score >= 80: ai_verdict = "STRONG BUY — Exceptional across multiple frameworks"
    elif ai_score >= 65: ai_verdict = "BUY — Strong fundamentals with favorable risk/reward"
    elif ai_score >= 50: ai_verdict = "ACCUMULATE — Good business, fair price"
    elif ai_score >= 35: ai_verdict = "HOLD — Mixed signals, wait for better entry"
    elif ai_score >= 20: ai_verdict = "UNDERWEIGHT — Significant concerns"
    else: ai_verdict = "AVOID — Fails most investment frameworks"

    # Build AI reasons from top-scoring investors
    ai_reasons = []
    sorted_scores = sorted(scores_raw.items(), key=lambda x: x[1], reverse=True)
    top_3 = sorted_scores[:3]
    for name, sc in top_3:
        ai_reasons.append(f"{name.title()} framework scores {sc}/100")

    return {
        'investors': [
            {'name': 'Warren Buffett', 'style': 'Value Investing & Moats', 'score': buffett, 'reasons': buffett_reasons, 'icon': '🏛️'},
            {'name': 'Benjamin Graham', 'style': 'Deep Value & Margin of Safety', 'score': graham, 'reasons': graham_reasons, 'icon': '📚'},
            {'name': 'Peter Lynch', 'style': 'Growth at Reasonable Price', 'score': lynch, 'reasons': lynch_reasons, 'icon': '📈'},
            {'name': 'George Soros', 'style': 'Macro & Reflexivity', 'score': soros, 'reasons': soros_reasons, 'icon': '🌍'},
            {'name': 'Charlie Munger', 'style': 'Quality & Mental Models', 'score': munger, 'reasons': munger_reasons, 'icon': '🧠'},
            {'name': 'Ray Dalio', 'style': 'All-Weather & Risk Parity', 'score': dalio, 'reasons': dalio_reasons, 'icon': '⚖️'},
            {'name': 'John Bogle', 'style': 'Index Quality & Long-term', 'score': bogle, 'reasons': bogle_reasons, 'icon': '🏔️'},
            {'name': 'Stanley Druckenmiller', 'style': 'Concentrated Momentum', 'score': druck, 'reasons': druck_reasons, 'icon': '🎯'},
            {'name': 'Carl Icahn', 'style': 'Activist Value', 'score': icahn, 'reasons': icahn_reasons, 'icon': '⚡'},
        ],
        'ai_score': ai_score,
        'ai_verdict': ai_verdict,
        'ai_reasons': ai_reasons,
        'methodology': 'Weighted composite of 9 investment frameworks adjusted for 2026 macro conditions (AI boom, elevated rates, sector rotation). Each score evaluates valuation, growth, quality, momentum, and balance sheet metrics.',
    }
