"""
Stock Screener v2.0 - Large Cap / Mid Cap / Small Cap categorization
with Congress trading intelligence and 100-point scoring system.
"""
import socket
import urllib3
from congress_tracker import calculate_congress_score, get_congress_signals

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

_yfinance_available = None

# Industry average P/E ratios
INDUSTRY_PE = {
    'Consumer Electronics': 28.5, 'Software': 35.0, 'Semiconductors': 30.0,
    'Internet Content': 25.0, 'Internet Retail': 38.0, 'Credit Services': 32.0,
    'Entertainment': 40.0, 'Capital Markets': 14.0, 'Biotechnology': 22.0,
    'Aerospace & Defense': 24.0, 'Banks': 11.0, 'Specialty Chemicals': 28.0,
    'Communication Equipment': 22.0, 'Cybersecurity': 55.0, 'Crypto Exchange': 20.0,
    'Internet Services': 45.0, 'Logistics': 18.0, 'Asset Management': 30.0,
    'Rental & Leasing': 16.0, 'Electronic Components': 28.0, 'Cloud Computing': 60.0,
    'Quantum Computing': 0, 'Fintech': 35.0, 'Brokerage': 20.0,
    'Computer Hardware': 15.0, 'AI Lending': 30.0, 'Online Gambling': 35.0,
    'Beverages': 30.0, 'EV Manufacturer': 50.0, 'Fitness': 25.0,
}

def _check_yfinance():
    global _yfinance_available
    if _yfinance_available is not None:
        return _yfinance_available
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        s.connect(("query1.finance.yahoo.com", 443))
        s.close()
        _yfinance_available = True
    except Exception:
        _yfinance_available = False
    return _yfinance_available

# === MOCK DATA: Large Cap (>$100B), Mid Cap ($10-100B), Small Cap (<$10B) ===
MOCK_STOCK_DATA = {
    # LARGE CAP
    'AAPL': {'name':'Apple Inc.','price':228.50,'pe_ratio':33.5,'forward_pe':28.2,'peg_ratio':2.5,'market_cap':3500.0,'sector':'Technology','industry':'Consumer Electronics','revenue_growth':5.0,'profit_margin':26.3,'gross_margin':46.2,'debt_to_equity':1.51,'current_ratio':0.99,'roe':160.0,'total_debt':98.0,'total_cash':62.0,'fifty_day_avg':220.0,'two_hundred_day_avg':210.0,'fifty_two_week_high':237.0,'fifty_two_week_low':164.0,'dividend_yield':0.44,'beta':1.24,'analyst_target':250.0},
    'MSFT': {'name':'Microsoft Corporation','price':449.26,'pe_ratio':36.8,'forward_pe':31.5,'peg_ratio':2.1,'market_cap':3340.0,'sector':'Technology','industry':'Software','revenue_growth':16.0,'profit_margin':35.6,'gross_margin':69.4,'debt_to_equity':0.29,'current_ratio':1.3,'roe':37.5,'total_debt':47.0,'total_cash':75.5,'fifty_day_avg':435.0,'two_hundred_day_avg':420.0,'fifty_two_week_high':468.35,'fifty_two_week_low':344.79,'dividend_yield':0.72,'beta':0.89,'analyst_target':510.0},
    'NVDA': {'name':'NVIDIA Corporation','price':135.40,'pe_ratio':55.2,'forward_pe':32.1,'peg_ratio':1.1,'market_cap':3320.0,'sector':'Technology','industry':'Semiconductors','revenue_growth':122.4,'profit_margin':55.8,'gross_margin':75.3,'debt_to_equity':0.41,'current_ratio':4.2,'roe':115.0,'total_debt':11.0,'total_cash':31.4,'fifty_day_avg':128.50,'two_hundred_day_avg':118.20,'fifty_two_week_high':153.13,'fifty_two_week_low':75.61,'dividend_yield':0.03,'beta':1.67,'analyst_target':175.0},
    'GOOGL': {'name':'Alphabet Inc.','price':178.20,'pe_ratio':23.5,'forward_pe':20.1,'peg_ratio':1.3,'market_cap':2200.0,'sector':'Technology','industry':'Internet Content','revenue_growth':14.0,'profit_margin':27.5,'gross_margin':57.5,'debt_to_equity':0.05,'current_ratio':2.1,'roe':32.0,'total_debt':14.8,'total_cash':108.0,'fifty_day_avg':172.0,'two_hundred_day_avg':165.0,'fifty_two_week_high':191.75,'fifty_two_week_low':130.67,'dividend_yield':0.45,'beta':1.05,'analyst_target':205.0},
    'AMZN': {'name':'Amazon.com, Inc.','price':205.80,'pe_ratio':42.5,'forward_pe':30.8,'peg_ratio':1.5,'market_cap':2150.0,'sector':'Consumer Cyclical','industry':'Internet Retail','revenue_growth':12.5,'profit_margin':8.2,'gross_margin':48.5,'debt_to_equity':0.55,'current_ratio':1.1,'roe':23.5,'total_debt':67.0,'total_cash':87.0,'fifty_day_avg':198.0,'two_hundred_day_avg':188.0,'fifty_two_week_high':215.90,'fifty_two_week_low':151.61,'dividend_yield':0.0,'beta':1.15,'analyst_target':240.0},
    'META': {'name':'Meta Platforms, Inc.','price':595.0,'pe_ratio':27.8,'forward_pe':22.5,'peg_ratio':1.4,'market_cap':1520.0,'sector':'Technology','industry':'Internet Content','revenue_growth':22.0,'profit_margin':33.5,'gross_margin':81.5,'debt_to_equity':0.28,'current_ratio':2.7,'roe':35.5,'total_debt':37.0,'total_cash':58.0,'fifty_day_avg':575.0,'two_hundred_day_avg':530.0,'fifty_two_week_high':638.40,'fifty_two_week_low':414.50,'dividend_yield':0.34,'beta':1.22,'analyst_target':660.0},
    'TSM': {'name':'Taiwan Semiconductor','price':186.50,'pe_ratio':28.5,'forward_pe':21.0,'peg_ratio':1.2,'market_cap':965.0,'sector':'Technology','industry':'Semiconductors','revenue_growth':33.9,'profit_margin':40.2,'gross_margin':57.8,'debt_to_equity':0.24,'current_ratio':2.5,'roe':28.5,'total_debt':28.0,'total_cash':60.0,'fifty_day_avg':178.0,'two_hundred_day_avg':170.0,'fifty_two_week_high':222.20,'fifty_two_week_low':127.00,'dividend_yield':1.24,'beta':1.15,'analyst_target':225.0},
    'MA': {'name':'Mastercard Inc.','price':545.0,'pe_ratio':38.5,'forward_pe':31.2,'peg_ratio':2.3,'market_cap':500.0,'sector':'Financial Services','industry':'Credit Services','revenue_growth':12.8,'profit_margin':45.8,'gross_margin':100.0,'debt_to_equity':1.9,'current_ratio':1.2,'roe':175.0,'total_debt':15.8,'total_cash':8.2,'fifty_day_avg':530.0,'two_hundred_day_avg':500.0,'fifty_two_week_high':564.0,'fifty_two_week_low':420.0,'dividend_yield':0.52,'beta':1.07,'analyst_target':600.0},
    'NFLX': {'name':'Netflix, Inc.','price':1090.0,'pe_ratio':52.3,'forward_pe':39.5,'peg_ratio':1.8,'market_cap':465.0,'sector':'Communication Services','industry':'Entertainment','revenue_growth':16.0,'profit_margin':22.3,'gross_margin':45.3,'debt_to_equity':0.63,'current_ratio':1.1,'roe':32.5,'total_debt':14.5,'total_cash':7.6,'fifty_day_avg':1050.0,'two_hundred_day_avg':850.0,'fifty_two_week_high':1150.0,'fifty_two_week_low':550.0,'dividend_yield':0.0,'beta':1.35,'analyst_target':1200.0},
    'GS': {'name':'Goldman Sachs Group','price':585.0,'pe_ratio':16.2,'forward_pe':13.5,'peg_ratio':0.9,'market_cap':190.0,'sector':'Financial Services','industry':'Capital Markets','revenue_growth':12.3,'profit_margin':24.5,'gross_margin':55.0,'debt_to_equity':2.5,'current_ratio':1.0,'roe':12.1,'total_debt':350.0,'total_cash':120.0,'fifty_day_avg':560.0,'two_hundred_day_avg':520.0,'fifty_two_week_high':612.0,'fifty_two_week_low':410.0,'dividend_yield':2.05,'beta':1.35,'analyst_target':640.0},
    'AMGN': {'name':'Amgen Inc.','price':285.0,'pe_ratio':25.8,'forward_pe':13.6,'peg_ratio':1.7,'market_cap':152.0,'sector':'Healthcare','industry':'Biotechnology','revenue_growth':23.2,'profit_margin':30.5,'gross_margin':74.8,'debt_to_equity':8.5,'current_ratio':1.3,'roe':72.0,'total_debt':62.0,'total_cash':9.8,'fifty_day_avg':290.0,'two_hundred_day_avg':295.0,'fifty_two_week_high':346.85,'fifty_two_week_low':252.0,'dividend_yield':3.45,'beta':0.51,'analyst_target':320.0},
    'BA': {'name':'The Boeing Company','price':197.86,'pe_ratio':0,'forward_pe':0,'peg_ratio':0,'market_cap':145.0,'sector':'Industrials','industry':'Aerospace & Defense','revenue_growth':18.2,'profit_margin':-3.2,'gross_margin':10.5,'debt_to_equity':0,'current_ratio':1.1,'roe':0,'total_debt':53.0,'total_cash':12.3,'fifty_day_avg':178.0,'two_hundred_day_avg':172.0,'fifty_two_week_high':199.0,'fifty_two_week_low':128.88,'dividend_yield':0.0,'beta':1.56,'analyst_target':210.0},
    'C': {'name':'Citigroup Inc.','price':73.90,'pe_ratio':12.5,'forward_pe':9.8,'peg_ratio':0.8,'market_cap':139.0,'sector':'Financial Services','industry':'Banks','revenue_growth':3.6,'profit_margin':16.8,'gross_margin':55.0,'debt_to_equity':1.2,'current_ratio':1.0,'roe':7.2,'total_debt':250.0,'total_cash':85.0,'fifty_day_avg':71.0,'two_hundred_day_avg':67.0,'fifty_two_week_high':83.23,'fifty_two_week_low':56.07,'dividend_yield':2.93,'beta':1.31,'analyst_target':85.0},
    'LIN': {'name':'Linde plc','price':460.0,'pe_ratio':32.5,'forward_pe':27.0,'peg_ratio':3.0,'market_cap':220.0,'sector':'Basic Materials','industry':'Specialty Chemicals','revenue_growth':2.5,'profit_margin':22.5,'gross_margin':45.0,'debt_to_equity':0.32,'current_ratio':0.8,'roe':18.5,'total_debt':21.0,'total_cash':5.0,'fifty_day_avg':455.0,'two_hundred_day_avg':445.0,'fifty_two_week_high':490.0,'fifty_two_week_low':390.0,'dividend_yield':1.23,'beta':0.92,'analyst_target':510.0},
    'CSCO': {'name':'Cisco Systems','price':61.50,'pe_ratio':26.5,'forward_pe':15.2,'peg_ratio':2.8,'market_cap':244.0,'sector':'Technology','industry':'Communication Equipment','revenue_growth':-6.0,'profit_margin':22.1,'gross_margin':64.7,'debt_to_equity':0.2,'current_ratio':1.4,'roe':28.2,'total_debt':9.8,'total_cash':17.3,'fifty_day_avg':58.0,'two_hundred_day_avg':53.0,'fifty_two_week_high':63.70,'fifty_two_week_low':44.50,'dividend_yield':2.56,'beta':0.85,'analyst_target':67.0},
    # MID CAP
    'PYPL': {'name':'PayPal Holdings','price':72.50,'pe_ratio':17.8,'forward_pe':13.2,'peg_ratio':1.2,'market_cap':75.0,'sector':'Financial Services','industry':'Credit Services','revenue_growth':8.5,'profit_margin':14.2,'gross_margin':40.5,'debt_to_equity':0.48,'current_ratio':1.3,'roe':21.0,'total_debt':12.0,'total_cash':16.2,'fifty_day_avg':70.0,'two_hundred_day_avg':67.0,'fifty_two_week_high':93.66,'fifty_two_week_low':56.50,'dividend_yield':0.0,'beta':1.47,'analyst_target':90.0},
    'CRWD': {'name':'CrowdStrike Holdings','price':365.0,'pe_ratio':95.0,'forward_pe':62.0,'peg_ratio':2.8,'market_cap':88.0,'sector':'Technology','industry':'Cybersecurity','revenue_growth':32.5,'profit_margin':5.2,'gross_margin':75.8,'debt_to_equity':0.35,'current_ratio':1.8,'roe':6.5,'total_debt':0.8,'total_cash':3.5,'fifty_day_avg':350.0,'two_hundred_day_avg':310.0,'fifty_two_week_high':398.0,'fifty_two_week_low':200.81,'dividend_yield':0.0,'beta':1.12,'analyst_target':420.0},
    'COIN': {'name':'Coinbase Global','price':225.0,'pe_ratio':22.5,'forward_pe':18.0,'peg_ratio':0.8,'market_cap':56.0,'sector':'Financial Services','industry':'Crypto Exchange','revenue_growth':85.0,'profit_margin':25.0,'gross_margin':85.0,'debt_to_equity':0.75,'current_ratio':1.5,'roe':25.0,'total_debt':4.5,'total_cash':7.2,'fifty_day_avg':210.0,'two_hundred_day_avg':195.0,'fifty_two_week_high':290.0,'fifty_two_week_low':115.0,'dividend_yield':0.0,'beta':2.5,'analyst_target':275.0},
    'DASH': {'name':'DoorDash, Inc.','price':178.0,'pe_ratio':125.0,'forward_pe':55.0,'peg_ratio':2.5,'market_cap':72.0,'sector':'Technology','industry':'Internet Services','revenue_growth':25.0,'profit_margin':3.5,'gross_margin':48.5,'debt_to_equity':0.15,'current_ratio':2.2,'roe':4.5,'total_debt':1.5,'total_cash':4.8,'fifty_day_avg':170.0,'two_hundred_day_avg':155.0,'fifty_two_week_high':190.0,'fifty_two_week_low':102.0,'dividend_yield':0.0,'beta':1.25,'analyst_target':200.0},
    'FDX': {'name':'FedEx Corporation','price':235.0,'pe_ratio':16.5,'forward_pe':12.8,'peg_ratio':1.1,'market_cap':55.0,'sector':'Industrials','industry':'Logistics','revenue_growth':-1.5,'profit_margin':7.2,'gross_margin':28.5,'debt_to_equity':0.82,'current_ratio':1.2,'roe':17.5,'total_debt':20.0,'total_cash':5.8,'fifty_day_avg':225.0,'two_hundred_day_avg':255.0,'fifty_two_week_high':313.84,'fifty_two_week_low':200.0,'dividend_yield':2.28,'beta':1.18,'analyst_target':280.0},
    'ARES': {'name':'Ares Management','price':175.0,'pe_ratio':42.5,'forward_pe':25.0,'peg_ratio':1.8,'market_cap':55.0,'sector':'Financial Services','industry':'Asset Management','revenue_growth':18.5,'profit_margin':15.8,'gross_margin':45.0,'debt_to_equity':0.8,'current_ratio':1.0,'roe':22.5,'total_debt':5.0,'total_cash':2.5,'fifty_day_avg':168.0,'two_hundred_day_avg':160.0,'fifty_two_week_high':198.0,'fifty_two_week_low':130.0,'dividend_yield':2.15,'beta':1.15,'analyst_target':200.0},
    'URI': {'name':'United Rentals','price':685.0,'pe_ratio':14.8,'forward_pe':12.5,'peg_ratio':0.9,'market_cap':44.0,'sector':'Industrials','industry':'Rental & Leasing','revenue_growth':9.5,'profit_margin':16.5,'gross_margin':39.8,'debt_to_equity':1.8,'current_ratio':0.9,'roe':32.5,'total_debt':13.5,'total_cash':0.5,'fifty_day_avg':650.0,'two_hundred_day_avg':700.0,'fifty_two_week_high':860.0,'fifty_two_week_low':530.0,'dividend_yield':0.95,'beta':1.45,'analyst_target':800.0},
    'GLW': {'name':'Corning Inc.','price':48.50,'pe_ratio':35.0,'forward_pe':19.5,'peg_ratio':1.5,'market_cap':41.0,'sector':'Technology','industry':'Electronic Components','revenue_growth':7.8,'profit_margin':6.5,'gross_margin':35.2,'debt_to_equity':0.65,'current_ratio':1.5,'roe':8.3,'total_debt':7.1,'total_cash':1.8,'fifty_day_avg':46.0,'two_hundred_day_avg':43.0,'fifty_two_week_high':52.07,'fifty_two_week_low':33.93,'dividend_yield':2.35,'beta':1.14,'analyst_target':55.0},
    'SNOW': {'name':'Snowflake Inc.','price':165.0,'pe_ratio':0,'forward_pe':0,'peg_ratio':0,'market_cap':55.0,'sector':'Technology','industry':'Cloud Computing','revenue_growth':28.0,'profit_margin':-5.5,'gross_margin':68.0,'debt_to_equity':0.1,'current_ratio':1.9,'roe':-3.5,'total_debt':0.0,'total_cash':3.8,'fifty_day_avg':158.0,'two_hundred_day_avg':150.0,'fifty_two_week_high':192.0,'fifty_two_week_low':107.13,'dividend_yield':0.0,'beta':1.45,'analyst_target':200.0},
    'APD': {'name':'Air Products & Chemicals','price':275.0,'pe_ratio':19.2,'forward_pe':17.5,'peg_ratio':2.5,'market_cap':61.0,'sector':'Basic Materials','industry':'Specialty Chemicals','revenue_growth':-3.5,'profit_margin':20.5,'gross_margin':35.2,'debt_to_equity':0.65,'current_ratio':1.5,'roe':16.8,'total_debt':8.5,'total_cash':2.8,'fifty_day_avg':280.0,'two_hundred_day_avg':290.0,'fifty_two_week_high':324.0,'fifty_two_week_low':232.0,'dividend_yield':2.55,'beta':0.82,'analyst_target':315.0},
    'NET': {'name':'Cloudflare, Inc.','price':115.0,'pe_ratio':0,'forward_pe':200.0,'peg_ratio':0,'market_cap':38.0,'sector':'Technology','industry':'Cybersecurity','revenue_growth':30.0,'profit_margin':3.5,'gross_margin':77.5,'debt_to_equity':0.85,'current_ratio':2.5,'roe':5.0,'total_debt':1.5,'total_cash':1.8,'fifty_day_avg':108.0,'two_hundred_day_avg':95.0,'fifty_two_week_high':120.0,'fifty_two_week_low':60.0,'dividend_yield':0.0,'beta':1.35,'analyst_target':130.0},
    # SMALL CAP
    'IONQ': {'name':'IonQ, Inc.','price':32.80,'pe_ratio':0,'forward_pe':0,'peg_ratio':0,'market_cap':7.2,'sector':'Technology','industry':'Quantum Computing','revenue_growth':89.5,'profit_margin':-350.0,'gross_margin':55.0,'debt_to_equity':0.05,'current_ratio':8.5,'roe':-45.0,'total_debt':0.0,'total_cash':0.5,'fifty_day_avg':30.0,'two_hundred_day_avg':28.0,'fifty_two_week_high':54.77,'fifty_two_week_low':7.42,'dividend_yield':0.0,'beta':1.85,'analyst_target':42.0},
    'SOFI': {'name':'SoFi Technologies','price':14.20,'pe_ratio':95.0,'forward_pe':35.0,'peg_ratio':1.5,'market_cap':8.5,'sector':'Financial Services','industry':'Fintech','revenue_growth':35.0,'profit_margin':5.2,'gross_margin':58.0,'debt_to_equity':0.3,'current_ratio':1.1,'roe':3.5,'total_debt':5.0,'total_cash':2.5,'fifty_day_avg':13.0,'two_hundred_day_avg':11.0,'fifty_two_week_high':17.19,'fifty_two_week_low':6.01,'dividend_yield':0.0,'beta':1.6,'analyst_target':18.0},
    'HOOD': {'name':'Robinhood Markets','price':24.80,'pe_ratio':25.0,'forward_pe':18.0,'peg_ratio':0.7,'market_cap':6.5,'sector':'Financial Services','industry':'Brokerage','revenue_growth':40.0,'profit_margin':18.0,'gross_margin':85.0,'debt_to_equity':0.85,'current_ratio':1.3,'roe':15.0,'total_debt':2.5,'total_cash':4.8,'fifty_day_avg':22.0,'two_hundred_day_avg':19.0,'fifty_two_week_high':29.75,'fifty_two_week_low':14.62,'dividend_yield':0.0,'beta':1.8,'analyst_target':30.0},
    'SMCI': {'name':'Super Micro Computer','price':42.0,'pe_ratio':12.5,'forward_pe':9.0,'peg_ratio':0.3,'market_cap':7.8,'sector':'Technology','industry':'Computer Hardware','revenue_growth':110.0,'profit_margin':8.5,'gross_margin':15.5,'debt_to_equity':0.45,'current_ratio':3.2,'roe':25.0,'total_debt':2.0,'total_cash':1.5,'fifty_day_avg':38.0,'two_hundred_day_avg':45.0,'fifty_two_week_high':122.0,'fifty_two_week_low':18.0,'dividend_yield':0.0,'beta':1.95,'analyst_target':55.0},
    'AFRM': {'name':'Affirm Holdings','price':52.0,'pe_ratio':0,'forward_pe':0,'peg_ratio':0,'market_cap':5.8,'sector':'Technology','industry':'Fintech','revenue_growth':46.0,'profit_margin':-8.5,'gross_margin':62.0,'debt_to_equity':2.5,'current_ratio':1.2,'roe':-12.0,'total_debt':8.0,'total_cash':2.5,'fifty_day_avg':48.0,'two_hundred_day_avg':42.0,'fifty_two_week_high':58.0,'fifty_two_week_low':22.0,'dividend_yield':0.0,'beta':2.2,'analyst_target':62.0},
    'UPST': {'name':'Upstart Holdings','price':68.0,'pe_ratio':0,'forward_pe':55.0,'peg_ratio':0,'market_cap':5.5,'sector':'Financial Services','industry':'AI Lending','revenue_growth':55.0,'profit_margin':-5.0,'gross_margin':72.0,'debt_to_equity':3.5,'current_ratio':1.1,'roe':-8.0,'total_debt':4.2,'total_cash':0.8,'fifty_day_avg':62.0,'two_hundred_day_avg':50.0,'fifty_two_week_high':80.0,'fifty_two_week_low':21.0,'dividend_yield':0.0,'beta':2.3,'analyst_target':78.0},
    'DKNG': {'name':'DraftKings Inc.','price':42.50,'pe_ratio':0,'forward_pe':45.0,'peg_ratio':0,'market_cap':9.5,'sector':'Consumer Cyclical','industry':'Online Gambling','revenue_growth':38.0,'profit_margin':-2.5,'gross_margin':42.0,'debt_to_equity':0.65,'current_ratio':1.8,'roe':-3.5,'total_debt':1.2,'total_cash':1.5,'fifty_day_avg':40.0,'two_hundred_day_avg':37.0,'fifty_two_week_high':48.0,'fifty_two_week_low':27.0,'dividend_yield':0.0,'beta':1.65,'analyst_target':55.0},
    'CELH': {'name':'Celsius Holdings','price':28.50,'pe_ratio':42.0,'forward_pe':30.0,'peg_ratio':1.5,'market_cap':6.8,'sector':'Consumer Defensive','industry':'Beverages','revenue_growth':23.0,'profit_margin':12.5,'gross_margin':50.0,'debt_to_equity':0.0,'current_ratio':3.0,'roe':22.0,'total_debt':0.0,'total_cash':0.8,'fifty_day_avg':26.0,'two_hundred_day_avg':32.0,'fifty_two_week_high':55.0,'fifty_two_week_low':22.0,'dividend_yield':0.0,'beta':1.55,'analyst_target':38.0},
    'RIVN': {'name':'Rivian Automotive','price':14.50,'pe_ratio':0,'forward_pe':0,'peg_ratio':0,'market_cap':8.2,'sector':'Consumer Cyclical','industry':'EV Manufacturer','revenue_growth':72.0,'profit_margin':-85.0,'gross_margin':-15.0,'debt_to_equity':1.2,'current_ratio':3.5,'roe':-65.0,'total_debt':5.5,'total_cash':7.8,'fifty_day_avg':13.0,'two_hundred_day_avg':12.0,'fifty_two_week_high':18.85,'fifty_two_week_low':8.26,'dividend_yield':0.0,'beta':1.75,'analyst_target':20.0},
    'PTON': {'name':'Peloton Interactive','price':8.50,'pe_ratio':0,'forward_pe':0,'peg_ratio':0,'market_cap':3.1,'sector':'Consumer Cyclical','industry':'Fitness','revenue_growth':-3.0,'profit_margin':-14.5,'gross_margin':42.0,'debt_to_equity':0,'current_ratio':2.5,'roe':-55.0,'total_debt':1.7,'total_cash':0.7,'fifty_day_avg':7.50,'two_hundred_day_avg':6.50,'fifty_two_week_high':9.80,'fifty_two_week_low':2.70,'dividend_yield':0.0,'beta':1.2,'analyst_target':10.0},
}

# Politicians who invested in each stock
CONGRESS_DATA = {
    'NVDA': [{'name':'Nancy Pelosi','amount':'$1M-$5M','party':'D'},{'name':'Josh Gottheimer','amount':'$500K-$1M','party':'D'},{'name':'Michael McCaul','amount':'$250K-$500K','party':'R'}],
    'MSFT': [{'name':'Nancy Pelosi','amount':'$1M-$5M','party':'D'},{'name':'Josh Gottheimer','amount':'$1M-$5M','party':'D'},{'name':'Ro Khanna','amount':'$500K-$1M','party':'D'},{'name':'Tommy Tuberville','amount':'$250K-$500K','party':'R'}],
    'GOOGL': [{'name':'Ro Khanna','amount':'$500K-$1M','party':'D'},{'name':'Josh Gottheimer','amount':'$250K-$500K','party':'D'}],
    'META': [{'name':'Nancy Pelosi','amount':'$500K-$1M','party':'D'},{'name':'Ro Khanna','amount':'$250K-$500K','party':'D'}],
    'AMZN': [{'name':'Josh Gottheimer','amount':'$500K-$1M','party':'D'}],
    'GS': [{'name':'Tommy Tuberville','amount':'$500K-$1M','party':'R'},{'name':'Mark Green','amount':'$250K-$500K','party':'R'}],
    'C': [{'name':'Michael McCaul','amount':'$500K-$1M','party':'R'},{'name':'Josh Gottheimer','amount':'$250K-$500K','party':'D'}],
    'BA': [{'name':'Mark Green','amount':'$250K-$500K','party':'R'},{'name':'Michael McCaul','amount':'$250K-$500K','party':'R'}],
    'TSM': [{'name':'Nancy Pelosi','amount':'$250K-$500K','party':'D'}],
    'COIN': [{'name':'Tommy Tuberville','amount':'$250K-$500K','party':'R'},{'name':'Ro Khanna','amount':'$100K-$250K','party':'D'}],
    'CRWD': [{'name':'Josh Gottheimer','amount':'$250K-$500K','party':'D'}],
    'PYPL': [{'name':'Josh Gottheimer','amount':'$100K-$250K','party':'D'}],
    'SOFI': [{'name':'Ro Khanna','amount':'$100K-$250K','party':'D'},{'name':'Tommy Tuberville','amount':'$50K-$100K','party':'R'}],
    'IONQ': [{'name':'Nancy Pelosi','amount':'$100K-$250K','party':'D'}],
    'SMCI': [{'name':'Nancy Pelosi','amount':'$250K-$500K','party':'D'},{'name':'Michael McCaul','amount':'$100K-$250K','party':'R'}],
    'HOOD': [{'name':'Ro Khanna','amount':'$50K-$100K','party':'D'}],
}


def score_fundamentals(data):
    if not data: return 0
    s = 0
    rg = data.get('revenue_growth', 0)
    if rg > 20: s += 10
    elif rg > 10: s += 8
    elif rg > 5: s += 5
    elif rg > 0: s += 3
    pm = data.get('profit_margin', 0)
    if pm > 20: s += 10
    elif pm > 15: s += 8
    elif pm > 10: s += 5
    elif pm > 5: s += 3
    de = data.get('debt_to_equity', 999)
    if de < 0.3: s += 5
    elif de < 0.7: s += 4
    elif de < 1.0: s += 3
    elif de < 1.5: s += 1
    cash, debt = data.get('total_cash', 0), data.get('total_debt', 0)
    if cash > 0 and debt > 0:
        if cash > debt * 1.5: s += 5
        elif cash > debt: s += 3
        elif cash > debt * 0.5: s += 1
    elif cash > 0 and debt == 0: s += 5
    return min(s, 30)


def score_valuation(data):
    if not data: return 0
    s = 0
    pe = data.get('pe_ratio', 0)
    if pe and 0 < pe < 15: s += 8
    elif pe and 0 < pe < 20: s += 6
    elif pe and 0 < pe < 30: s += 4
    elif pe and 0 < pe < 40: s += 2
    peg = data.get('peg_ratio', 0)
    if peg and 0 < peg < 1.0: s += 7
    elif peg and 0 < peg < 1.5: s += 5
    elif peg and 0 < peg < 2.0: s += 3
    elif peg and 0 < peg < 3.0: s += 1
    price, target = data.get('price', 0), data.get('analyst_target', 0)
    if price and target and target > 0:
        upside = (target - price) / price * 100
        if upside > 30: s += 5
        elif upside > 20: s += 4
        elif upside > 10: s += 3
        elif upside > 0: s += 1
    return min(s, 20)


def score_momentum(data):
    if not data: return 0
    s, price = 0, data.get('price', 0)
    ma200 = data.get('two_hundred_day_avg', 0)
    if price and ma200 and ma200 > 0:
        pct = (price - ma200) / ma200 * 100
        if 0 < pct < 20: s += 8
        elif pct >= 20: s += 5
        elif -5 < pct <= 0: s += 4
        elif -10 < pct <= -5: s += 2
    ma50 = data.get('fifty_day_avg', 0)
    if price and ma50 and ma50 > 0:
        p50 = (price - ma50) / ma50 * 100
        if -5 < p50 < 10: s += 7
        elif 10 <= p50 < 20: s += 4
        elif -10 < p50 <= -5: s += 3
    h, l = data.get('fifty_two_week_high', 0), data.get('fifty_two_week_low', 0)
    if price and h and l and h > l:
        pos = (price - l) / (h - l) * 100
        if 40 < pos < 75: s += 5
        elif 75 <= pos < 90: s += 3
        elif 25 < pos <= 40: s += 3
        elif pos >= 90: s += 1
    return min(s, 20)


def _get_rating(score):
    if score >= 80: return 'STRONG BUY'
    if score >= 65: return 'BUY'
    if score >= 50: return 'ACCUMULATE'
    if score >= 35: return 'HOLD'
    return 'AVOID'


def _get_stars(score):
    if score >= 80: return 5
    if score >= 65: return 4
    if score >= 50: return 3
    if score >= 35: return 2
    return 1


def get_stock_data(ticker):
    if _check_yfinance():
        try:
            import yfinance as yf
            stock = yf.Ticker(ticker)
            info = stock.info
            if info and ('currentPrice' in info or 'regularMarketPrice' in info):
                price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
                if price and price > 0:
                    return {'ticker': ticker, 'name': info.get('shortName', ticker), 'price': round(price, 2),
                        'pe_ratio': info.get('trailingPE', 0) or 0, 'forward_pe': info.get('forwardPE', 0) or 0,
                        'peg_ratio': info.get('pegRatio', 0) or 0,
                        'market_cap': round((info.get('marketCap', 0) or 0) / 1e9, 1),
                        'sector': info.get('sector', 'Unknown'), 'industry': info.get('industry', 'Unknown'),
                        'revenue_growth': round((info.get('revenueGrowth', 0) or 0) * 100, 1),
                        'profit_margin': round((info.get('profitMargins', 0) or 0) * 100, 1),
                        'gross_margin': round((info.get('grossMargins', 0) or 0) * 100, 1),
                        'debt_to_equity': round((info.get('debtToEquity', 0) or 0) / 100, 2),
                        'current_ratio': info.get('currentRatio', 0) or 0,
                        'roe': round((info.get('returnOnEquity', 0) or 0) * 100, 1),
                        'total_debt': round((info.get('totalDebt', 0) or 0) / 1e9, 1),
                        'total_cash': round((info.get('totalCash', 0) or 0) / 1e9, 1),
                        'fifty_day_avg': info.get('fiftyDayAverage', 0) or 0,
                        'two_hundred_day_avg': info.get('twoHundredDayAverage', 0) or 0,
                        'fifty_two_week_high': info.get('fiftyTwoWeekHigh', 0) or 0,
                        'fifty_two_week_low': info.get('fiftyTwoWeekLow', 0) or 0,
                        'dividend_yield': round((info.get('dividendYield', 0) or 0) * 100, 2),
                        'beta': info.get('beta', 1.0) or 1.0,
                        'analyst_target': info.get('targetMeanPrice', 0) or 0}
        except Exception:
            pass
    if ticker in MOCK_STOCK_DATA:
        d = {'ticker': ticker, **MOCK_STOCK_DATA[ticker]}
        d['industry_pe'] = INDUSTRY_PE.get(d.get('industry', ''), 0)
        return d
    return None


def generate_recommendations_by_category():
    """Returns {'largecap': [...], 'midcap': [...], 'smallcap': [...]}"""
    categories = {'largecap': [], 'midcap': [], 'smallcap': []}

    for ticker, mock in MOCK_STOCK_DATA.items():
        data = get_stock_data(ticker)
        if not data or not data.get('price'):
            continue

        congress_score = calculate_congress_score(ticker)
        fund_score = score_fundamentals(data)
        val_score = score_valuation(data)
        mom_score = score_momentum(data)
        total = congress_score + fund_score + val_score + mom_score

        mc = data.get('market_cap', 0)
        if mc >= 100: cat = 'largecap'
        elif mc >= 10: cat = 'midcap'
        else: cat = 'smallcap'

        ma200 = data.get('two_hundred_day_avg', 0)
        stop = round(max(data['price'] * 0.90, ma200 * 0.97) if ma200 else data['price'] * 0.90, 2)
        target = data.get('analyst_target', 0)
        tp = target if target and target > data['price'] else round(data['price'] * 1.30, 2)
        tr = round((tp - data['price']) / data['price'] * 100, 1)

        congress_pols = CONGRESS_DATA.get(ticker, [])

        rec = {
            'ticker': ticker, 'company': data['name'], 'price': data['price'],
            'sector': data.get('sector', ''), 'industry': data.get('industry', ''),
            'market_cap': mc, 'cap_category': cat,
            'total_score': total, 'congress_score': congress_score,
            'fundamental_score': fund_score, 'valuation_score': val_score, 'momentum_score': mom_score,
            'rating': _get_rating(total), 'stars': _get_stars(total),
            'pe_ratio': data.get('pe_ratio', 0), 'forward_pe': data.get('forward_pe', 0),
            'peg_ratio': data.get('peg_ratio', 0), 'industry_pe': data.get('industry_pe', 0),
            'revenue_growth': data.get('revenue_growth', 0), 'profit_margin': data.get('profit_margin', 0),
            'gross_margin': data.get('gross_margin', 0), 'debt_to_equity': data.get('debt_to_equity', 0),
            'dividend_yield': data.get('dividend_yield', 0), 'beta': data.get('beta', 1.0),
            'roe': data.get('roe', 0), 'current_ratio': data.get('current_ratio', 0),
            'stop_loss': stop, 'target_price': tp, 'target_return': tr,
            'congress_politicians': congress_pols,
            'congress_politician_count': len(congress_pols),
        }
        categories[cat].append(rec)

    # Sort each category by score
    for cat in categories:
        categories[cat].sort(key=lambda x: x['total_score'], reverse=True)
        categories[cat] = categories[cat][:10]
        for i, r in enumerate(categories[cat]):
            r['rank'] = i + 1

    return categories


def generate_recommendations(max_stocks=10):
    """Legacy: returns flat top N list."""
    cats = generate_recommendations_by_category()
    all_recs = cats['largecap'] + cats['midcap'] + cats['smallcap']
    all_recs.sort(key=lambda x: x['total_score'], reverse=True)
    for i, r in enumerate(all_recs[:max_stocks]):
        r['rank'] = i + 1
    return all_recs[:max_stocks]
