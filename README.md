# AI Stock Analyzer 📊

A comprehensive stock analysis tool that provides Warren Buffett-style investment insights with interactive visualizations.

## Features ✨

- **Real-time Stock Analysis** - Get current price, valuation bands, and buy/sell recommendations
- **10-Year Financial History** - Analyze 40 quarters and 10 years of financial data
- **Interactive Charts** - Visualize trends with configurable bar charts and pie charts
- **Warren Buffett Analysis** - Investment scoring based on value investing principles
- **Debt Tracking** - Monitor debt levels and growth over time
- **Geographic & Segment Breakdown** - See revenue distribution with pie charts
- **Position Sizing Calculator** - Calculate optimal position size based on risk tolerance

## Quick Start 🚀

### Prerequisites
- Python 3.11 or higher
- Windows PowerShell

### Installation & Running

1. **Open PowerShell** and navigate to the project directory:
```powershell
cd C:\Automation\AIStockAnalyzer
```

2. **Activate virtual environment** (if not already activated):
```powershell
.\venv\Scripts\Activate.ps1
```

3. **Install dependencies** (first time only):
```powershell
pip install -r requirements.txt
```

4. **Start the Flask server**:
```powershell
cd src
python app.py
```

5. **Open your browser** and go to:
```
http://127.0.0.1:5000
```

6. **Enter a stock ticker** (e.g., AAPL, MSFT, GOOGL) and click "Analyze"

## Available Tickers 📈

Currently available for analysis with realistic data:
- **AAPL** - Apple Inc. (Full 10-year history)
- **MSFT** - Microsoft Corporation (Limited data)
- **GOOGL** - Alphabet Inc. (Limited data)

More tickers can be added to the `MOCK_DATA` dictionary in `src/analyzer.py`.

## How to Use 📖

### 1. Search for a Stock
Enter a ticker symbol (e.g., AAPL) in the search box on the homepage.

### 2. View Analysis Dashboard
You'll see:
- **Current price and valuation** - Fair value estimate with buy/sell ranges
- **Interactive financial trends chart** - Select metrics to display (Revenue, Net Profit, Debt, etc.)
- **Warren Buffett analysis** - Investment score out of 100 with buy recommendation
- **Key valuation metrics** - P/E ratio, PEG, Market Cap, Debt/Equity, etc.
- **Revenue & profitability tables** - 10 years of quarterly and annual data

### 3. Customize the View
- **Select quarters/years** - Check/uncheck boxes to show specific periods
- **Configure chart metrics** - Choose which financial metrics to visualize
- **Toggle chart period** - Switch between quarterly (40 periods) and yearly (10 periods)

### 4. Analyze Geographic & Segment Data
Scroll down to see:
- **Worldwide revenue by region** - Bar chart + pie chart
- **Core income streams** - Business segment breakdown with visualizations

## Dashboard Sections 📊

### 1. Valuation Summary
- Current price vs fair value
- Buy/Sell ranges with confidence levels
- Position sizing recommendations

### 2. Warren Buffett Analysis (🎩)
- **Score**: 0-100 points based on value investing principles
- **Verdict**: STRONG BUY / BUY / HOLD / PASS
- **Confidence**: Very High / High / Moderate / Low
- **Positive factors**: Consistent profitability, low debt, cash strength
- **Risk factors**: Overvaluation, high debt, declining margins

### 3. Interactive Financial Trends Chart
- **Default view**: Yearly data with Revenue, Net Profit, and Debt
- **Configurable metrics**: Choose from Revenue, Gross Profit, Net Profit, Debt
- **Period toggle**: Switch between 40 quarters or 10 years
- **Hover tooltips**: See exact dollar amounts

### 4. Revenue & Profitability Analysis
**Quarterly Table** (40 quarters - Q2 2016 to Q1 2026):
- Revenue and growth %
- Gross profit and margin %
- Net profit and margin %
- Debt and growth %

**Yearly Table** (10 years - 2016 to 2025):
- Same metrics aggregated annually
- Easy comparison of year-over-year performance

### 5. Geographic & Segment Breakdown
- **Bar charts**: Horizontal bars showing dollar amounts and percentages
- **Pie charts**: Visual proportional distribution
- **Regions**: Americas, Europe, China, Japan, APAC
- **Segments**: iPhone, Services, Mac, iPad, Wearables

## Technical Details 🔧

### Architecture
- **Backend**: Flask 3.0.0 (Python web framework)
- **Data Source**: Mock data (demonstration purposes - Yahoo Finance blocked by firewall)
- **Frontend**: HTML5, CSS3, JavaScript, Chart.js 4.4.1
- **Charts**: Chart.js for interactive bar and pie charts

### Project Structure
```
AIStockAnalyzer/
├── src/
│   ├── app.py              # Flask application (routes)
│   └── analyzer.py         # Stock analysis logic + mock data
├── templates/
│   ├── index.html          # Landing page (ticker search)
│   ├── result.html         # Analysis dashboard (main view)
│   └── error.html          # Error handling page
├── requirements.txt        # Python dependencies
├── test_analyzer.py        # Testing script
└── README.md              # This file
```

### Key Files

**src/app.py**
- Flask routes: `/` (home), `/analyze` (POST)
- Error handling and template rendering

**src/analyzer.py**
- `MOCK_DATA` dictionary: Financial data for tickers
- `analyze_ticker()`: Main analysis function
- `calculate_buffett_score()`: Investment scoring algorithm
- `get_recommendation()`: Buy/sell/hold logic

**templates/result.html**
- Complete dashboard with all visualizations
- Chart.js integration for interactive charts
- Responsive design with mobile support

## Troubleshooting 🔍

### Server won't start
```powershell
# Make sure you're in the src directory
cd src
python app.py
```

### Port already in use
```powershell
# Kill existing process or use different port
netstat -ano | findstr :5000
taskkill /PID <process_id> /F
```

### Virtual environment issues
```powershell
# Deactivate and reactivate
deactivate
.\venv\Scripts\Activate.ps1
```

### Charts not loading
- Clear browser cache (Ctrl+Shift+Delete)
- Check browser console for JavaScript errors (F12)
- Ensure Chart.js CDN is accessible

### "Ticker not found" error
- Only AAPL, MSFT, GOOGL available in mock data
- Add more tickers to `MOCK_DATA` in `src/analyzer.py`

## Customization 🎨

### Adding New Tickers
Edit `src/analyzer.py` and add to `MOCK_DATA`:
```python
'TSLA': {
    'price': 250.00,
    'pe': 65.5,
    'quarterly': [...],  # 40 quarters of data
    'yearly': [...],     # 10 years of data
    'regions': [...],    # Geographic breakdown
    'segments': [...]    # Business segments
}
```

### Changing Default Chart Metrics
Edit `templates/result.html`, find the checkboxes and modify `checked` attribute:
```html
<input type="checkbox" id="chart-revenue" value="revenue" checked>
<input type="checkbox" id="chart-net-profit" value="net_profit" checked>
```

### Adjusting Portfolio Size
Default is $10,000. Change in the analysis output or modify the calculator logic in `analyzer.py`.

## Data Disclaimer ⚠️

This application uses **demonstration/mock data** for educational purposes only. 

**Why mock data?**
- Corporate firewall blocks Yahoo Finance API
- Day 1 prototype focused on functionality demonstration
- Real data integration planned for future versions

**Not for actual trading decisions!**
- Data is illustrative, not real-time
- For research and education only
- Always consult a licensed financial advisor
- Past performance ≠ future results

## Future Enhancements 🚀

- [ ] Live data integration (Yahoo Finance, Alpha Vantage, IEX Cloud)
- [ ] Database storage (PostgreSQL + Redis caching)
- [ ] User authentication and watchlists
- [ ] Email/SMS price alerts
- [ ] Export reports to PDF
- [ ] Mobile app (React Native)
- [ ] Broker integration (read-only portfolio)
- [ ] More technical indicators (RSI, MACD, Bollinger Bands)
- [ ] News sentiment analysis
- [ ] Peer comparison (compare multiple stocks)

## Support 💬

For questions or issues:
1. Check the Troubleshooting section above
2. Review error messages in terminal and browser console
3. Verify all dependencies are installed: `pip list`
4. Ensure Python 3.11+ is being used: `python --version`

## License 📄

Educational project - Not for commercial use or actual trading decisions.

---

**Last Updated**: February 28, 2026  
**Version**: 0.1 (Day 1 Prototype)  
**Status**: Demonstration/Educational
