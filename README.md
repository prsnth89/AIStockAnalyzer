# 🏛️ AI Stock Analyzer - Smart Money Congress Tracker

**Follow the smart money.** Track what U.S. politicians are buying, combine it with deep fundamental analysis, and get **Top 10 stock recommendations** designed to target **30%+ annual returns**.

> 💡 **The Idea**: Members of Congress often trade stocks with an information edge. By tracking their purchases and combining with strong fundamentals, we identify high-conviction opportunities.

---

## 🎯 What This App Does

### 📊 Top 10 Recommended Stocks (Homepage)
Every stock is scored on a **100-point system** combining:

| Signal | Weight | Source |
|--------|--------|--------|
| 🏛️ **Congress Trading Activity** | 30 pts | QuiverQuant - recent politician purchases |
| 📈 **Fundamental Strength** | 30 pts | Revenue growth, margins, low debt (yfinance) |
| 💰 **Valuation Discount** | 20 pts | P/E vs sector, PEG ratio, price vs fair value |
| 🔥 **Momentum & Trend** | 20 pts | 50/200-day MA, RSI, recent price action |

### 🏛️ Congress Trading Intelligence
- **Real-time tracking** of politician stock purchases from SEC filings
- **Smart filtering**: Focuses on purchases > $15,000 (excludes small dividend reinvestments)
- **Politician ranking**: Weights trades by historically successful traders (e.g., Pelosi, Gottheimer)
- **Recency scoring**: Recent trades (< 30 days) score higher than older ones

### 📈 Deep Stock Analysis (Per-Ticker)
- **10-year financial history**: 40 quarters + 10 years of revenue, profit, debt
- **Warren Buffett scoring**: Value investing analysis with confidence levels
- **Interactive charts**: Configurable bar charts + pie charts (Chart.js)
- **Position sizing**: Risk-based recommendations for portfolio allocation
- **Geographic & segment breakdown**: Revenue distribution visualization

---

## 🚀 Quick Start

```powershell
cd C:\Automation\AIStockAnalyzer
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
cd src
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

---

## 📊 How the Scoring Works

### Congress Signal Score (0-30 points)
| Criteria | Points |
|----------|--------|
| Recent politician purchases (< 30 days) | up to 15 |
| Multiple politicians buying same stock | up to 10 |
| Large position sizes (> $50K) | up to 5 |

### Fundamental Score (0-30 points)
| Criteria | Points |
|----------|--------|
| Revenue growing > 10% YoY | 10 |
| Net margin > 15% consistently | 10 |
| Debt/Equity < 1.0 | 5 |
| Cash > Debt | 5 |

### Valuation Score (0-20 points)
| Criteria | Points |
|----------|--------|
| P/E below sector average | 8 |
| PEG ratio < 1.5 | 7 |
| Price below fair value | 5 |

### Momentum Score (0-20 points)
| Criteria | Points |
|----------|--------|
| Price above 200-day MA | 8 |
| RSI between 40-65 (not overbought) | 7 |
| Positive 3-month price change | 5 |

### Score Guide
| Score | Rating | Action |
|-------|--------|--------|
| 80-100 | ⭐⭐⭐⭐⭐ STRONG BUY | High conviction - full position |
| 65-79 | ⭐⭐⭐⭐ BUY | Good opportunity - build position |
| 50-64 | ⭐⭐⭐ ACCUMULATE | Start small, add on dips |
| 35-49 | ⭐⭐ HOLD | Wait for better entry |
| 0-34 | ⭐ AVOID | Weak signals |

---

## 💰 Targeting 30% Annual Returns

The strategy combines multiple edge factors:

1. **Information Asymmetry**: Politicians often trade before public knowledge of legislation
2. **Fundamental Quality**: Only recommends stocks with strong financials
3. **Valuation Discipline**: Avoids overpaying (Buffett-style margin of safety)
4. **Trend Confirmation**: Ensures stocks are in uptrends before entry

### Risk Management
- **Position sizing**: Never > 10% of portfolio in one stock
- **Stop losses**: Suggested exit points on every recommendation
- **Diversification**: Top 10 spans multiple sectors
- **Rebalancing**: Refreshes when new congress trades are detected

---

## 🏛️ Data Sources

| Source | Data | Access |
|--------|------|--------|
| [QuiverQuant](https://www.quiverquant.com/congresstrading) | Congress stock trades | Web scraping |
| [Capitol Trades](https://www.capitoltrades.com) | Politician trading activity | Reference |
| [Yahoo Finance](https://finance.yahoo.com) | Stock prices, fundamentals | yfinance (free) |
| [Unusual Whales](https://unusualwhales.com) | Options flow (future) | Premium API |

---

## 📱 Features

| Feature | Status |
|---------|--------|
| ✅ Top 10 stock recommendations with scores | Live |
| ✅ Congress trading tracker | Live |
| ✅ Real-time stock data (yfinance) | Live |
| ✅ Warren Buffett analysis | Live |
| ✅ Interactive financial charts (Chart.js) | Live |
| ✅ 10-year quarterly/annual financials | Live |
| ✅ Geographic & segment pie charts | Live |
| ✅ Position sizing calculator | Live |
| ✅ Politician trade history per stock | Live |
| 🔄 Unusual Whales options flow | Planned |
| 🔄 Email/SMS price alerts | Planned |
| 🔄 Portfolio tracking | Planned |

---

## ⚠️ Disclaimer

**For research and educational purposes only.** NOT personalized financial advice.
Past performance ≠ future results. Congress trading data has a reporting lag (up to 45 days).
Always consult a licensed financial advisor. All investments carry risk of loss.

---

📖 **Technical docs**: See [TECHNICAL.md](TECHNICAL.md)

**Version**: 2.0 | **Updated**: April 29, 2026
