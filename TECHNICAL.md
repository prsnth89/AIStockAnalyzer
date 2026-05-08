# 🔧 Technical Documentation - AI Stock Analyzer

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     BROWSER (Client)                        │
│  Homepage: Top 10 Recommendations                           │
│  Detail:   Full Stock Analysis Dashboard                    │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP
┌──────────────────────────▼──────────────────────────────────┐
│                  FLASK WEB SERVER (:5000)                    │
│  Routes: / (home), /analyze (POST), /api/recommendations    │
└──────┬────────────────┬────────────────┬────────────────────┘
       │                │                │
┌──────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐
│  Screener   │  │  Analyzer   │  │  Congress   │
│  (Top 10)   │  │  (Detail)   │  │  Tracker    │
│             │  │             │  │             │
│ Score 0-100 │  │ Buffett     │  │ QuiverQuant │
│ Rank & Sort │  │ Financials  │  │ Scraper     │
│ Multi-factor│  │ Charts Data │  │ Capitol     │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       │                │                │
┌──────▼────────────────▼────────────────▼────────────────────┐
│                    DATA SOURCES                              │
│  yfinance (prices, fundamentals, financial statements)       │
│  QuiverQuant (congress trading - web scrape)                 │
│  Mock data fallback (when APIs unavailable)                  │
└─────────────────────────────────────────────────────────────┘
```

## Project Structure

```
AIStockAnalyzer/
├── src/
│   ├── app.py               # Flask application - routes & server
│   ├── analyzer.py           # Stock analysis engine + Buffett scoring
│   ├── congress_tracker.py   # Congress trading data scraper
│   └── screener.py           # Stock screener - generates Top 10
├── templates/
│   ├── index.html            # Homepage - Top 10 recommendations
│   ├── result.html           # Detailed stock analysis dashboard
│   └── error.html            # Error page
├── data/
│   └── congress_cache.json   # Cached congress trading data
├── requirements.txt          # Python dependencies
├── README.md                 # Product/features documentation
├── TECHNICAL.md              # This file - technical docs
├── START.ps1                 # Quick-start script
└── test_analyzer.py          # Test script
```

## Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Backend | Python | 3.11+ |
| Web Framework | Flask | 3.0.0 |
| Stock Data | yfinance | 0.2.51 |
| Data Processing | pandas | 2.1.4 |
| Web Scraping | BeautifulSoup4 | 4.12.3 |
| HTTP Client | requests | 2.31.0 |
| Charts | Chart.js | 4.4.1 (CDN) |
| Frontend | HTML5, CSS3, JavaScript | - |

## Key Modules

### `src/congress_tracker.py`
Scrapes QuiverQuant for recent politician stock trades.

**Functions:**
- `fetch_congress_trades()` → Fetches latest trades from QuiverQuant
- `get_congress_signals(ticker)` → Gets congress activity for a specific stock
- `get_top_congress_stocks()` → Returns stocks with most congress buying activity
- `calculate_congress_score(ticker)` → Scores 0-30 based on congress signals

**Data Sources:**
- QuiverQuant Congress Trading page (web scraping)
- Caches results in `data/congress_cache.json` (1-hour TTL)

### `src/screener.py`
Multi-factor stock scoring engine for Top 10 recommendations.

**Functions:**
- `generate_recommendations()` → Produces scored & ranked Top 10 list
- `score_fundamentals(ticker)` → Scores 0-30 based on financial health
- `score_valuation(ticker)` → Scores 0-20 based on valuation metrics
- `score_momentum(ticker)` → Scores 0-20 based on price trends
- `get_composite_score(ticker)` → Combines all scores into 0-100

**Scoring Formula:**
```
Total Score = Congress(0-30) + Fundamentals(0-30) + Valuation(0-20) + Momentum(0-20)
```

### `src/analyzer.py`
Deep stock analysis with financial data and Buffett-style evaluation.

**Functions:**
- `analyze_ticker(ticker)` → Full analysis with financials, valuation bands
- `calculate_buffett_score(data)` → Warren Buffett investment scoring
- `get_recommendation(price, fair_value)` → Buy/sell recommendation

**Data Flow:**
1. Fetch current price + fundamentals from yfinance
2. Pull quarterly/annual financial statements
3. Calculate valuation bands (±15%, ±30% from fair value)
4. Run Buffett analysis (profitability, debt, growth, valuation)
5. Attach congress trading signals
6. Return comprehensive analysis dict

### `src/app.py`
Flask web server with routes.

**Routes:**
| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Homepage with Top 10 recommendations |
| `/analyze` | POST | Detailed stock analysis page |
| `/api/recommendations` | GET | JSON API for Top 10 stocks |
| `/api/congress` | GET | JSON API for congress trades |

## Configuration

### Environment Variables (Optional)
```
FLASK_PORT=5000          # Server port (default: 5000)
CACHE_TTL=3600           # Congress data cache TTL in seconds
USE_MOCK_DATA=false      # Force mock data mode
```

### Cache Strategy
- **Congress trades**: Cached for 1 hour (data updates infrequently)
- **Stock prices**: Fresh on each request (yfinance is fast)
- **Financial statements**: Cached in memory during session
- **Recommendations**: Regenerated every 4 hours

## API Response Format

### GET /api/recommendations
```json
{
  "recommendations": [
    {
      "rank": 1,
      "ticker": "NVDA",
      "company": "NVIDIA Corp.",
      "price": 875.28,
      "total_score": 82,
      "congress_score": 25,
      "fundamental_score": 28,
      "valuation_score": 12,
      "momentum_score": 17,
      "rating": "STRONG BUY",
      "congress_trades": [
        {
          "politician": "John Boozman",
          "party": "R",
          "chamber": "Senate",
          "type": "Purchase",
          "amount": "$1,001 - $15,000",
          "date": "2026-03-19"
        }
      ],
      "target_return": "35%",
      "stop_loss": "$780"
    }
  ],
  "last_updated": "2026-04-29T14:30:00Z"
}
```

## Development

### Setup
```powershell
cd C:\Automation\AIStockAnalyzer
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Run Development Server
```powershell
cd src
python app.py
```

### Run Tests
```powershell
python test_analyzer.py
```

### Adding New Data Sources
1. Create a new module in `src/` (e.g., `src/options_flow.py`)
2. Add scoring function returning 0-N points
3. Integrate into `screener.py` composite score
4. Adjust weights in scoring formula

## Error Handling

| Error | Cause | Fallback |
|-------|-------|----------|
| yfinance timeout | Network/firewall | Use cached or mock data |
| QuiverQuant blocked | Rate limiting | Use cached congress data |
| Invalid ticker | User input | Error page with suggestions |
| API rate limit | Too many requests | Exponential backoff + cache |

## Security Notes

- No API keys stored in code (all free-tier sources)
- SSL verification can be disabled for corporate firewalls
- No user data collected or stored
- All data is publicly available information

---

**Version**: 2.0 | **Updated**: April 29, 2026
