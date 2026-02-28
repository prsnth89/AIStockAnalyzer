# 🚀 QUICK START GUIDE

## Method 1: Use the Quick Start Script (Easiest!)

Simply run:
```powershell
.\START.ps1
```

That's it! The script will:
- ✅ Activate virtual environment
- ✅ Check dependencies
- ✅ Start the Flask server
- ✅ Display the URL to open

## Method 2: Manual Start

```powershell
# Step 1: Activate virtual environment
.\venv\Scripts\Activate.ps1

# Step 2: Navigate to src folder
cd src

# Step 3: Start the server
python app.py
```

## Method 3: First Time Setup

If this is your first time running the app:

```powershell
# Create virtual environment (one-time)
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# Install dependencies (one-time)
pip install -r requirements.txt

# Start the server
cd src
python app.py
```

---

## 📊 How to Use

1. **Open browser**: Go to `http://127.0.0.1:5000`

2. **Enter a ticker**: Type AAPL, MSFT, or GOOGL

3. **View analysis**: See comprehensive dashboard with:
   - 📈 Interactive financial trends chart
   - 🎩 Warren Buffett investment analysis
   - 📊 10 years of quarterly & annual data
   - 🌍 Geographic revenue breakdown (pie charts!)
   - 💰 Business segment analysis (pie charts!)

---

## ⚡ Features Highlights

### Interactive Financial Trends Chart
- **Select metrics**: Revenue, Gross Profit, Net Profit, Debt
- **Toggle period**: 40 quarters or 10 years
- **Default view**: Revenue + Net Profit + Debt (yearly)

### Warren Buffett Analysis
- **Investment score**: 0-100 points
- **Verdict**: STRONG BUY / BUY / HOLD / PASS
- **Confidence**: Very High / High / Moderate / Low
- **Detailed reasoning**: Positive factors + risk warnings

### Debt Tracking
- **10 years of debt data**: Quarter-by-quarter tracking
- **Growth indicators**: Color-coded (green = positive, red = negative)
- **Debt/Equity ratio**: Evaluate leverage levels

### Revenue Breakdown
- **Geographic**: See revenue by region (bar + pie charts)
- **Business segments**: Analyze income streams (bar + pie charts)

---

## 🎯 Available Tickers

Currently loaded with realistic data:
- **AAPL** - Apple Inc. ✅ (Full 10-year history)
- **MSFT** - Microsoft Corp. (Limited data)
- **GOOGL** - Alphabet Inc. (Limited data)

---

## 🛑 Stop the Server

Press **Ctrl+C** in the terminal window

---

## ❓ Troubleshooting

### Server won't start
```powershell
# Make sure you're in the correct directory
cd C:\Automation\AIStockAnalyzer
.\START.ps1
```

### Port already in use
```powershell
# Find and kill the process using port 5000
netstat -ano | findstr :5000
taskkill /PID <process_id> /F
```

### Charts not loading
- Clear browser cache (Ctrl+Shift+Delete)
- Hard refresh page (Ctrl+F5)
- Check browser console for errors (F12)

### Virtual environment issues
```powershell
deactivate
.\venv\Scripts\Activate.ps1
```

---

## 📖 Full Documentation

See **README.md** for complete documentation including:
- Architecture details
- Customization guide
- Adding new tickers
- Technical specifications

---

## ⚠️ Important Notes

- **Mock Data**: Currently uses demonstration data (corporate firewall blocks Yahoo Finance)
- **Educational Purpose**: Not for actual trading decisions
- **Consult Advisor**: Always seek professional financial advice
- **Past Performance**: Does not guarantee future results

---

## 🎨 Dashboard Sections

When you analyze a stock, you'll see:

1. **Valuation Summary** - Current price, fair value, buy/sell ranges
2. **Financial Health Cards** - Revenue, profit margins, debt, cash reserves
3. **Key Valuation Metrics** - P/E, PEG, Market Cap, D/E ratio, P/B ratio
4. **Warren Buffett Analysis** - Investment scoring and recommendations
5. **Interactive Chart** - Configurable financial trends visualization
6. **Revenue & Profitability** - 40 quarters + 10 years of detailed financials
7. **Geographic Breakdown** - Worldwide revenue with bar + pie charts
8. **Business Segments** - Core income streams with bar + pie charts

---

**Last Updated**: February 28, 2026  
**Version**: 0.1 (Day 1 Prototype)

Need help? Check the terminal output for error messages or review README.md for detailed troubleshooting.
