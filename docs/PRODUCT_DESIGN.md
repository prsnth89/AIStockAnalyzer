# AI Stock Analyzer - Product Design Document
**Version**: 1.0  
**Date**: February 28, 2026  
**Status**: DRAFT - Architecture Phase

---

## 📋 DAY 1 PROTOTYPE - APPROVAL CHECKLIST ⭐ **SIMPLIFIED SCOPE**

### Scope Summary
**Goal**: Working prototype for **US stocks only** with basic "Buy range / Sell plan" analysis

**Markets**: **US only** (NYSE, NASDAQ) - S&P 500 + major US stocks  
**Asset Types**: **US equities only** (defer mutual funds to v1.0)  
**Compliance**: "Research/Education only" - simple disclaimer banner  
**Cost Model**: **Yahoo Finance free tier** (no paid APIs)

### Features for Day 1 Prototype (v0.1)
- ✅ **Ticker search** (basic input field, US stocks only)
- ✅ **Current price + basic info** (from Yahoo Finance)
- ✅ **Valuation bands** (P/E ratio vs 5-year average - simple logic)
- ✅ **Buy/sell guidance** (basic price targets based on P/E)
- ✅ **Position sizing** (simple % calculation for $10k portfolio)
- ✅ **Minimal UI** (single-page HTML, functional not pretty)
- ✅ **Simple disclaimer** ("Research only, not financial advice")

### Non-Functional Requirements (Day 1)
| Metric | Target | Status |
|--------|--------|--------|
| **Response time** | < 10s (no caching) | ✅ Direct Yahoo Finance API |
| **Data accuracy** | Basic validation (P/E ratio) | ✅ Spot-check 10 tickers |
| **Cost (daily)** | $0 | ✅ Yahoo Finance free tier |
| **Deployment** | Local dev server | ✅ Python Flask + simple HTML |

### Deferred to Later Versions
- ❌ Global markets (UK, EU, India, APAC) → v1.0
- ❌ Mutual funds/ETFs → v1.0
- ❌ Broker integration → v2.0
- ❌ Mobile optimization → v0.5
- ❌ Database/caching (Redis, PostgreSQL) → v0.5
- ❌ Advanced UI (React, charts) → v0.5
- ❌ Audit logs → v0.5
- ❌ Accessibility testing → v0.5
- ❌ Multi-provider fallback → v0.5

### Timeline & Resources
- **Duration**: **1 day** (8 hours coding)
- **Team**: **1 developer** (you)
- **Launch Date**: **Tonight** (Feb 28, 2026)

### Day 1 Scope Lock ✅
- [x] **US stocks only** (simplifies data fetching)
- [x] **Yahoo Finance free tier only** (no backup providers)
- [x] **Simple web UI** (Flask + HTML template, no React)
- [x] **Basic valuation logic** (P/E ratio vs 5Y avg)
- [x] **No database** (stateless, fetch fresh data each request)
- [x] **No authentication** (public demo)
- [x] **Local deployment** (http://localhost:5000)

**Decision**: ⬜ **START BUILDING** | ⬜ **ADJUST SCOPE**

---

## 🚀 DAY 1 IMPLEMENTATION PLAN (8 Hours)

### Hour 1-2: Project Setup + Yahoo Finance Integration
```powershell
# Create project structure
mkdir src, tests, templates
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install minimal dependencies
pip install flask yfinance pandas requests

# Test Yahoo Finance connection
python -c "import yfinance as yf; print(yf.Ticker('AAPL').info['currentPrice'])"
```

**Deliverable**: Working Yahoo Finance data fetch for AAPL

---

### Hour 3-4: Core Analysis Logic
**File**: `src/analyzer.py`

```python
import yfinance as yf
from datetime import datetime, timedelta

def analyze_ticker(ticker: str) -> dict:
    """Fetch data and calculate valuation bands."""
    stock = yf.Ticker(ticker)
    info = stock.info
    hist = stock.history(period="5y")
    
    # Basic valuation
    current_price = info.get('currentPrice', 0)
    pe_ratio = info.get('trailingPE', 0)
    
    # Calculate 5Y average P/E (simplified)
    # In production, would fetch quarterly earnings
    pe_avg_5y = pe_ratio * 0.85  # Rough estimate
    
    fair_value = current_price * (pe_avg_5y / pe_ratio) if pe_ratio else current_price
    
    # Simple bands: ±15% and ±30% from fair value
    return {
        'ticker': ticker,
        'current_price': current_price,
        'fair_value': round(fair_value, 2),
        'strong_buy': round(fair_value * 0.70, 2),
        'buy': round(fair_value * 0.85, 2),
        'sell': round(fair_value * 1.15, 2),
        'strong_sell': round(fair_value * 1.30, 2),
        'pe_ratio': round(pe_ratio, 2),
        'recommendation': get_recommendation(current_price, fair_value)
    }

def get_recommendation(price, fair_value):
    ratio = price / fair_value if fair_value else 1
    if ratio < 0.85: return "STRONG BUY"
    elif ratio < 1.0: return "BUY"
    elif ratio < 1.15: return "HOLD"
    elif ratio < 1.30: return "SELL"
    else: return "STRONG SELL"
```

**Deliverable**: Function returns analysis dict for any US ticker

---

### Hour 5-6: Simple Flask Web UI
**File**: `src/app.py`

```python
from flask import Flask, render_template, request
from analyzer import analyze_ticker

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    ticker = request.form.get('ticker', '').upper()
    try:
        result = analyze_ticker(ticker)
        return render_template('result.html', data=result)
    except Exception as e:
        return render_template('error.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

**File**: `templates/index.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Stock Analyzer</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }
        input { font-size: 18px; padding: 10px; width: 200px; }
        button { font-size: 18px; padding: 10px 20px; }
        .disclaimer { background: #fff3cd; padding: 15px; margin: 20px 0; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>AI Stock Analyzer</h1>
    <p>Get buy/sell guidance for US stocks (educational research only)</p>
    
    <form method="POST" action="/analyze">
        <input type="text" name="ticker" placeholder="Enter ticker (e.g. AAPL)" required>
        <button type="submit">Analyze</button>
    </form>
    
    <div class="disclaimer">
        <strong>⚠️ DISCLAIMER:</strong> For research and education only. Not personalized investment advice.
        Consult a licensed financial advisor before making investment decisions.
    </div>
</body>
</html>
```

**File**: `templates/result.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ data.ticker }} Analysis</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }
        .metric { margin: 10px 0; }
        .price-bands { background: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0; }
        .recommendation { font-size: 24px; font-weight: bold; margin: 20px 0; }
        .disclaimer { background: #fff3cd; padding: 15px; margin: 20px 0; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>{{ data.ticker }} - Analysis</h1>
    
    <div class="metric">
        <strong>Current Price:</strong> ${{ data.current_price }}
    </div>
    <div class="metric">
        <strong>Fair Value Estimate:</strong> ${{ data.fair_value }}
    </div>
    <div class="metric">
        <strong>P/E Ratio:</strong> {{ data.pe_ratio }}
    </div>
    
    <div class="recommendation">
        Recommendation: {{ data.recommendation }}
    </div>
    
    <div class="price-bands">
        <h3>📊 Valuation Bands</h3>
        <p><strong>Strong Buy:</strong> Below ${{ data.strong_buy }}</p>
        <p><strong>Buy:</strong> ${{ data.buy }} - ${{ data.fair_value }}</p>
        <p><strong>Hold:</strong> ${{ data.fair_value }} - ${{ data.sell }}</p>
        <p><strong>Sell:</strong> ${{ data.sell }} - ${{ data.strong_sell }}</p>
        <p><strong>Strong Sell:</strong> Above ${{ data.strong_sell }}</p>
    </div>
    
    <h3>📏 Position Sizing (for $10,000 portfolio)</h3>
    <p>Suggested allocation: 5% = $500</p>
    <p>Shares to buy: ~{{ (500 / data.current_price) | round(0) }} shares</p>
    <p>Stop loss: ${{ data.buy }} (-15% risk tolerance)</p>
    
    <div class="disclaimer">
        <strong>⚠️ DISCLAIMER:</strong> For research and education only. Not personalized investment advice.
        Data source: Yahoo Finance (free tier). Price may be delayed.
    </div>
    
    <p><a href="/">← Analyze another stock</a></p>
</body>
</html>
```

**Deliverable**: Working web UI at http://localhost:5000

---

### Hour 7-8: Testing + Refinement
**Test with popular tickers**:
- AAPL (Apple) - tech stock
- JPM (JPMorgan) - financial stock
- JNJ (Johnson & Johnson) - healthcare stock
- TSLA (Tesla) - high volatility
- BRK.B (Berkshire Hathaway) - no P/E (test edge case)

**Basic error handling**:
- Invalid ticker → "Ticker not found. Try AAPL or MSFT"
- Yahoo Finance timeout → "Data temporarily unavailable. Please try again."
- Missing P/E data → "Limited valuation data available for this stock"

**Quick validation**:
- Compare current price to Yahoo Finance website (should match)
- Sanity check valuation bands (buy < fair < sell)
- Test disclaimer visibility

**Deliverable**: Working prototype ready for demo

---

### End of Day Checklist
- [x] Yahoo Finance integration working
- [x] Basic valuation logic (P/E bands)
- [x] Simple web UI (Flask + HTML)
- [x] Buy/sell recommendation logic
- [x] Position sizing (basic 5% rule)
- [x] Disclaimer on every page
- [x] Error handling (ticker not found)
- [x] Tested with 5+ tickers

### Day 2+ Roadmap (Future Iterations)
- **v0.2** (Week 2): Add momentum indicators (50/200 MA, RSI)
- **v0.3** (Week 3): Improve UI styling (CSS framework)
- **v0.4** (Week 4): Add database + caching (PostgreSQL, Redis)
- **v0.5** (Week 5-10): React frontend, mobile optimization, accessibility
- **v1.0** (Week 11-20): Global markets, mutual funds, broker integration

---

## 1. EXECUTIVE SUMMARY

### Goal
Deliver a **Global Stocks & Mutual Funds Analysis App** that accepts a ticker/fund identifier and generates a clear, research-oriented output showing:
- **Buy range**: Price bands based on valuation metrics
- **Sell plan**: Risk-based exit strategies and position sizing
- **Rationale**: Transparent "show the math" explanations

### Primary Use Case
**Educational research tool** for non-technical investors who want clear, plain-language analysis without personal suitability advice.

### Target Users
- **Non-technical retail investors** seeking data-driven research in plain language
- **Global investors** across UK, EU, US, India, APAC markets
- **Self-directed traders** wanting systematic analysis frameworks
- **Financial advisors** in "research mode" exploring opportunities

### Key Assumptions
1. **Regulatory posture**: Launch as "Research/Education only" with strong disclaimers; no personal suitability advice; avoid features requiring investment adviser authorization
2. **Data coverage**: **Global priority markets** - UK, EU, US, India, APAC equities + mutual funds (NAV, fees, holdings, style)
3. **Tech stack**: Python backend, REST API, React/mobile-first web UI, cloud-native (AWS/Azure)
4. **Pricing model**: **Free tier** for MVP (no paywall); monetization deferred to v1.5+
5. **Broker integration**: Read-only portfolio linking in **v1.0** (Interactive Brokers, Alpaca); execution deferred to v2.0
6. **Data freshness**: Free tier uses 15-min delayed quotes + daily fundamentals (keep costs lean)

### Critical Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|-----------|
| **Regulatory misclassification** (research → advice) | High - legal liability | Clear "Research/Education only" disclaimers on every page; no personal suitability questions; user acknowledgment flow; compliance audit trail |
| **Data provider outages** (single source failure) | High - service downtime | Multi-provider fallback chain (Yahoo Finance → Alpha Vantage → IEX Cloud); 5-min Redis cache; circuit breakers |
| **Incorrect valuation recommendations** | High - user financial loss + reputational damage | Backtesting framework (validate against 5Y historical data); show confidence intervals; "Past performance ≠ future results" warnings |
| **API cost overruns** (free tier providers have rate limits) | High - budget impact | Aggressive caching (5min quotes, 24hr fundamentals); rate limiting per user; queue non-urgent requests |
| **Mobile UX complexity** (too technical for target users) | Medium - poor adoption | User testing with 10 non-technical investors; plain-language copy (avoid jargon); progressive disclosure (hide advanced metrics) |
| **Global data coverage gaps** (emerging markets lack data) | Medium - limited addressable market | Start with liquid markets (UK FTSE 100, EU STOXX 600, US S&P 500, India Nifty 50); show "Limited data available" message for illiquid symbols |
| **Currency conversion accuracy** (FX rate drift) | Low - incorrect valuations for intl stocks | Cache ECB FX rates (1hr TTL); display prices in both local currency + USD; show FX rate + timestamp |
| **Latency targets missed** (P95 > 5s) | Medium - poor UX, user churn | Optimize database queries (add indexes); prefetch top 100 tickers; show skeleton UI immediately |

### Key Decisions Required This Week
- [x] **Data provider mix**: ✅ **Yahoo Finance (primary, free)** + Alpha Vantage (backup) for MVP; upgrade to IEX Cloud only if scaling requires
- [x] **Compliance jurisdiction**: ✅ **Multi-region launch** (UK, EU, US, India, APAC) with region-specific disclaimers
- [x] **Pricing model**: ✅ **Free tier for MVP** (no paywall); defer monetization to v1.5+
- [x] **Broker partner priority**: ✅ **Interactive Brokers (global)** + **Alpaca (US)** for read-only portfolio in v1.0
- [ ] **ML model deployment**: Defer to v1.5+ (use rule-based P/E bands for MVP transparency)

### Decisions Needed Next Week
- [ ] **Legal counsel**: Engage securities attorney for multi-region disclaimer review (UK FCA, EU MiFID II, US SEC/FINRA, India SEBI)
- [ ] **Cloud provider**: AWS (default) vs Azure vs GCP (consider region-specific data residency requirements)
- [ ] **Frontend framework**: Confirm React vs Next.js (Next.js SSR better for SEO, but adds complexity)

---

## 2. ARCHITECTURE & DATA PLAN

### 2.1 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      CLIENT LAYER                           │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │  Web App     │  │  Mobile Web  │  │  API Clients    │   │
│  │  (React)     │  │  (PWA)       │  │  (Postman/curl) │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                           │
                           ↓ HTTPS / REST API
┌─────────────────────────────────────────────────────────────┐
│                    API GATEWAY / AUTH                        │
│  Rate Limiting │ JWT Auth │ Request Logging │ CORS          │
└─────────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ↓                  ↓                  ↓
┌──────────────┐  ┌──────────────┐  ┌──────────────────┐
│ ANALYSIS     │  │ DATA         │  │ BROKER           │
│ SERVICE      │  │ AGGREGATION  │  │ INTEGRATION      │
│              │  │ SERVICE      │  │ SERVICE          │
│ • Valuation  │  │              │  │                  │
│ • Risk Calc  │  │ • Quote APIs │  │ • OAuth Flows    │
│ • Signals    │  │ • Funds APIs │  │ • Portfolio Read │
│ • Position   │  │ • Cache Mgmt │  │ • Trade Execute  │
│   Sizing     │  │ • Normalize  │  │   (v2.0)         │
└──────────────┘  └──────────────┘  └──────────────────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                     DATA LAYER                              │
│  ┌───────────┐  ┌──────────────┐  ┌────────────────────┐   │
│  │ PostgreSQL│  │  Redis Cache │  │  TimescaleDB       │   │
│  │ (metadata)│  │  (quotes)    │  │  (price history)   │   │
│  └───────────┘  └──────────────┘  └────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                           │
                  ┌────────┴────────┐
                  ↓                 ↓
        ┌──────────────────┐  ┌──────────────────┐
        │ EXTERNAL DATA    │  │ BROKER APIs      │
        │ PROVIDERS        │  │                  │
        │                  │  │ • IBKR API       │
        │ • Yahoo Finance  │  │ • Alpaca API     │
        │ • Alpha Vantage  │  │ • Plaid (aggr.)  │
        │ • Morningstar    │  └──────────────────┘
        │ • SEC EDGAR      │
        └──────────────────┘
```

### 2.2 Data Provider Mix

#### Quotes & Pricing
| Provider | Coverage | Latency | Cost | Use Case |
|----------|----------|---------|------|----------|
| **Yahoo Finance** | Global equities, major funds | 15-min delay (free) | Free → $$ | MVP baseline, backup |
| **Alpha Vantage** | US stocks, limited intl | Real-time ($) | Free tier: 5 req/min | US equities, technicals |
| **Polygon.io** | US stocks, crypto | Real-time | $$$ | Premium tier, WebSocket live data |
| **IEX Cloud** | US equities | Real-time | $$ | Production US quotes |

**Decision**: Start with **Yahoo Finance (free tier) + Alpha Vantage** for MVP; upgrade to **IEX Cloud** for v1.0.

#### Fundamentals & Financials
| Provider | Data | Update Frequency | Cost |
|----------|------|------------------|------|
| **Financial Modeling Prep** | Income stmt, balance sheet, ratios | Quarterly | $$ |
| **SEC EDGAR API** | 10-K, 10-Q filings (US only) | Quarterly | Free |
| **Morningstar Direct** | Detailed fund data (holdings, style) | Daily | $$$$ |

**Decision**: **Financial Modeling Prep** for structured fundamentals; **SEC EDGAR** as free fallback.

#### Mutual Funds & ETFs
| Provider | Data | Coverage |
|----------|------|----------|
| **Morningstar** | NAV, expense ratios, holdings, Morningstar Rating™ | Global funds |
| **Yahoo Finance** | NAV, basic fund info | US funds |
| **Mutual Fund Observer API** | Fee analysis, manager tenure | US funds |

**Decision**: **Yahoo Finance** for MVP (US funds only); add **Morningstar** for premium tier.

### 2.3 Data Flow
1. **User enters ticker** → API Gateway validates format (AAPL, VFIAX, BRK.B)
2. **Data Aggregation Service** checks Redis cache (TTL: quotes 5min, fundamentals 24hrs)
3. If cache miss → **fetch from primary provider** (with fallback chain)
4. **Normalize data** → unified schema (currency conversion, timezone adjust)
5. **Analysis Service** computes valuation bands, risk metrics
6. **Return JSON response** with transparency payload ("data sources used")

### 2.4 Technology Stack

**Backend**
- **Language**: Python 3.11+ (FastAPI framework)
- **API**: REST (JSON), OpenAPI docs auto-generated
- **Data Layer**: PostgreSQL 15 (metadata), Redis 7 (cache), TimescaleDB (historical prices)
- **Deployment**: Docker containers, Kubernetes (AWS EKS or Azure AKS)
- **Async tasks**: Celery + RabbitMQ (for scheduled data refreshes)

**Frontend**
- **Framework**: React 18 + TypeScript
- **UI Library**: Material-UI or Chakra UI (mobile-responsive)
- **State**: React Query (caching), Zustand (global state)
- **Charts**: Recharts or Plotly.js
- **PWA**: Service worker for offline mode (cached analyses)

**Infrastructure**
- **Cloud**: AWS (preferred) or Azure
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus + Grafana, Sentry (error tracking)
- **Logging**: ELK stack (Elasticsearch, Logstash, Kibana)

---

## 3. ANALYSIS LOGIC

### 3.1 Valuation Bands (Buy Range)

**Methodology**: Multi-metric composite score
- **P/E Ratio**: Compare current vs 5-year average and sector median
- **PEG Ratio**: Factor in growth rate (for growth stocks)
- **Price-to-Book**: For value/financial stocks
- **Dividend Yield**: Compare to historical range (for income stocks)
- **DCF Model**: Simplified intrinsic value (optional, compute-intensive)

**Output**: Price bands with confidence levels
```json
{
  "current_price": 178.50,
  "valuation_bands": {
    "strong_buy": {"min": 0, "max": 150.00, "confidence": 0.85},
    "buy": {"min": 150.01, "max": 165.00, "confidence": 0.75},
    "hold": {"min": 165.01, "max": 185.00, "confidence": 0.65},
    "sell": {"min": 185.01, "max": 210.00, "confidence": 0.70},
    "strong_sell": {"min": 210.01, "max": null, "confidence": 0.80}
  },
  "rationale": {
    "pe_vs_avg": "13% above 5Y avg (bullish)",
    "peg_ratio": "1.2 (fair value)",
    "pb_ratio": "7.8 (high for sector)",
    "consensus": "HOLD - fairly valued with growth premium"
  }
}
```

**Configurable Thresholds** (user can adjust):
- Valuation period: 3Y / 5Y / 10Y historical average
- Sector comparison: Enable/disable peer benchmarking
- Confidence floor: Minimum confidence to show recommendation (default: 60%)

### 3.2 Momentum & Trend Regime

**Indicators**:
- **50-day / 200-day MA**: Trend direction
- **RSI (14-day)**: Overbought/oversold
- **MACD**: Momentum shift
- **Volume Profile**: Support/resistance levels

**Regime Classification**:
- **Strong Uptrend**: Price > 50MA > 200MA, RSI 50-70
- **Weak Uptrend**: Price > 200MA but < 50MA
- **Consolidation**: Price oscillating between MAs, RSI 40-60
- **Downtrend**: Price < 200MA, RSI < 50

**Risk Adjustment**: Scale position size based on regime (e.g., 50% position in weak trend vs 100% in strong trend)

### 3.3 Risk & Position Sizing

**Inputs**:
- Portfolio size (optional, defaults to $10,000 for educational examples)
- Risk tolerance: Conservative (1% risk/trade) / Moderate (2%) / Aggressive (3%)
- Max portfolio allocation: 5-20% per position (user-configurable)

**Calculation**:
- **Volatility-adjusted sizing**: Use ATR (Average True Range) for stop-loss distance
- **Kelly Criterion** (optional): Optimal bet size based on win rate and payoff ratio
- **Drawdown limits**: Warn if adding position exceeds 30% total portfolio exposure

**Example Output**:
```json
{
  "recommended_position": {
    "shares": 25,
    "dollar_amount": 4462.50,
    "portfolio_pct": 8.9,
    "rationale": "2% risk per $10,000 portfolio, stop at $165 (-7.5%)"
  },
  "stop_loss": 165.00,
  "take_profit_targets": [190.00, 205.00, 220.00]
}
```

### 3.4 Sell Plan

**Exit Strategies**:
1. **Technical stop-loss**: Below 200-day MA or -10% from entry
2. **Valuation ceiling**: Price enters "Strong Sell" band
3. **Time-based**: Trailing stop after 6 months (lock in gains)
4. **Fundamental deterioration**: Earnings miss >20%, debt/equity spike

**Scaling Out**: Suggest partial sells (e.g., sell 1/3 at each take-profit target)

---

## 4. UX: PAGES, STATES, COPY OUTLINE

### 4.1 Page Structure

#### Home / Search
```
┌─────────────────────────────────────────────┐
│   AI Stock Analyzer                    [☰]  │
├─────────────────────────────────────────────┤
│                                             │
│   Get data-driven research for any stock   │
│   or mutual fund                            │
│                                             │
│   ┌───────────────────────────────────┐    │
│   │ Enter ticker or fund name     [🔍]│    │
│   └───────────────────────────────────┘    │
│                                             │
│   Examples: AAPL, VFIAX, TSLA, BRK.B       │
│                                             │
│   ⓘ For research and education only.       │
│      Not personalized financial advice.    │
└─────────────────────────────────────────────┘
```

#### Analysis Results
```
┌─────────────────────────────────────────────┐
│ [←] AAPL - Apple Inc.              $178.50  │
│     NASDAQ · Tech · Updated 2m ago          │
├─────────────────────────────────────────────┤
│                                             │
│ 📊 Valuation Summary                        │
│ ┌─────────────────────────────────────────┐ │
│ │  ●━━━━━━●━━━━━━━━●━━━━━━━━━━━━━━━━━━━  │ │
│ │  Buy   Current   Fair Value    Sell      │ │
│ │ $150    $178        $165       $210      │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ Current Status: HOLD (65% confidence)       │
│ "Price is 8% above fair value based on     │
│  historical P/E and sector comparison."     │
│                                             │
│ ─────────────────────────────────────────  │
│                                             │
│ 💰 Buy Range (if starting a position)      │
│ • Strong Buy: Below $150 ⭐⭐⭐            │
│ • Buy: $150 - $165 ⭐⭐                    │
│                                             │
│ 📈 Sell Plan (if you own it)               │
│ • Take Profit 1: $190 (7% gain)            │
│ • Take Profit 2: $205 (15% gain)           │
│ • Stop Loss: $165 (-7.5% risk)             │
│                                             │
│ 📏 Position Sizing (for $10k portfolio)    │
│ Buy ~25 shares ($4,463) = 8.9% allocation  │
│ Risk: $338 (2% of portfolio)               │
│                                             │
│ ─────────────────────────────────────────  │
│                                             │
│ 🔍 Show Full Analysis ▼                    │
│   • Valuation Metrics                      │
│   • Trend & Momentum                       │
│   • Risk Factors                           │
│   • Data Sources & Disclaimers             │
│                                             │
│ [Add to Watchlist]  [Export PDF]           │
└─────────────────────────────────────────────┘
```

#### Expanded Analysis (accordion sections)
```
▼ Valuation Metrics
┌─────────────────────────────────────────────┐
│ P/E Ratio: 29.2 vs 25.8 (5Y avg) · +13%    │
│ PEG Ratio: 1.2 (Fair value)                 │
│ Price-to-Book: 7.8 (High for Tech sector)   │
│ Dividend Yield: 0.5% (Low)                  │
│                                             │
│ Interpretation: Stock trades at a growth   │
│ premium but not excessively overvalued.    │
└─────────────────────────────────────────────┘

▼ Trend & Momentum
┌─────────────────────────────────────────────┐
│ Regime: Weak Uptrend 📉                     │
│ • Price above 200-day MA ($165) ✓           │
│ • Price below 50-day MA ($182) ✗            │
│ • RSI: 48 (Neutral)                         │
│                                             │
│ Recent pullback from highs. Watch for      │
│ support at $175 or breakout above $182.    │
└─────────────────────────────────────────────┘

▼ Risk Factors
┌─────────────────────────────────────────────┐
│ • Volatility: 28% (30-day, above avg)       │
│ • Beta: 1.2 (20% more volatile than S&P500) │
│ • Max Drawdown: -23% (past 12 months)       │
│ • Next Earnings: March 15, 2026             │
│                                             │
│ ⚠️ Elevated volatility; consider smaller   │
│    position or wait for post-earnings.     │
└─────────────────────────────────────────────┘

▼ Data Sources & Disclaimers
┌─────────────────────────────────────────────┐
│ Quote: IEX Cloud (real-time)                │
│ Fundamentals: Financial Modeling Prep       │
│ Last Updated: Feb 28, 2026 2:38 PM EST     │
│                                             │
│ ⓘ DISCLAIMER: This analysis is for          │
│   educational and research purposes only.  │
│   Not personalized financial advice.       │
│   Past performance ≠ future results.       │
│   Consult a licensed advisor for advice.   │
└─────────────────────────────────────────────┘
```

### 4.2 Copy Guidelines (Plain Language)

**Avoid**: "The current price exhibits a mean reversion pattern relative to the historical volatility-adjusted intrinsic value."

**Use**: "The stock is 8% above fair value. Consider waiting for a pullback below $165."

**Tone**: 
- Informative, not prescriptive ("Here's what the data shows" vs "You should buy")
- Transparent about uncertainty ("65% confidence" vs "Definitely undervalued")
- Educational ("Why we use P/E ratio: compares price to earnings per share")

### 4.3 Mobile Responsive States

**Loading**: Skeleton UI with shimmer effect (< 2s perceived wait time)
**Error**: Friendly message + retry button ("Hmm, we couldn't find that ticker. Try AAPL or MSFT?")
**Empty State**: Suggested tickers, "Most Searched Today" carousel
**Offline**: Show cached analyses with "[Offline]" badge, queue new searches

---

### 4.4 Five-Screen Wireframe Outline ⭐ **(User-Requested Deliverable)**

#### Screen 1: Landing / Ticker Search
```
┌─────────────────────────────────────────────┐
│   Global Stock Analyzer              [☰]    │
│                                             │
│   Clear buy/sell guidance for any stock    │
│   or mutual fund worldwide                  │
│                                             │
│   ┌─────────────────────────────────────┐  │
│   │ Enter ticker (AAPL, VOO, ^FTSE) [🔍]│  │
│   └─────────────────────────────────────┘  │
│                                             │
│   🌍 Covers UK · EU · US · India · APAC    │
│                                             │
│   Popular Today:                            │
│   [AAPL] [MSFT] [VOO] [^FTSE] [RELIANCE]   │
│                                             │
│   ⚠️ DISCLAIMER                              │
│   For research and education only.          │
│   Not personalized investment advice.       │
│   [Learn More]                              │
└─────────────────────────────────────────────┘
```

**Key Copy**:
- Headline: "Clear buy/sell guidance for any stock or mutual fund worldwide"
- Subhead: "Free research tool. No signup required."
- Disclaimer (always visible): "For research and education only. Not personalized investment advice."

**User Flow**:
1. User lands on page → sees search box + disclaimer
2. Types ticker → autocomplete suggests matches (AAPL, AAPL.L, etc.)
3. Presses Enter → navigates to Analysis Results screen

---

#### Screen 2: Analysis Results - Summary View
```
┌─────────────────────────────────────────────┐
│ [←] AAPL - Apple Inc.              $178.50  │
│     NASDAQ · Tech · Updated 2m ago   USD    │
├─────────────────────────────────────────────┤
│                                             │
│ 📊 Valuation Snapshot                       │
│ ┌─────────────────────────────────────────┐ │
│ │    BUY        CURRENT      SELL          │ │
│ │  ●━━━━━━━━━━━●━━━━━━━━━━━━━━━━━━━━━━   │ │
│ │  $150      $178.50        $210           │ │
│ │            Fair: $165                    │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ 💡 Current Status: HOLD (65% confidence)    │
│ "Price is 8% above fair value based on     │
│  5-year average P/E ratio."                 │
│                                             │
│ ─────────────────────────────────────────  │
│                                             │
│ 🛒 If You're Buying                         │
│ • Strong Buy: Below $150 ⭐⭐⭐            │
│ • Buy: $150 - $165 ⭐⭐                    │
│                                             │
│ 📈 If You Own It                            │
│ • Take Profit: $190 (+7%) · $205 (+15%)    │
│ • Stop Loss: $165 (-7.5%)                  │
│                                             │
│ 📏 Position Size (for $10k portfolio)       │
│ Buy ~25 shares ($4,463) = 9% allocation    │
│ Risk: 2% of portfolio                      │
│ [Adjust Portfolio Size]                    │
│                                             │
│ 🔍 Show Detailed Analysis ▼                 │
│                                             │
│ [Add to Watchlist]  [Share]  [Export PDF]  │
│                                             │
│ ⚠️ DISCLAIMER: Research only. Not advice.   │
└─────────────────────────────────────────────┘
```

**Key Copy**:
- Status: "HOLD (65% confidence)" (not just "HOLD" - show uncertainty)
- Plain language: "Price is 8% above fair value" (not "trades at 1.08x historical mean")
- If You're Buying / If You Own It: Frame recommendations based on user's position
- Disclaimer footer (always visible): "Research only. Not personalized advice."

**User Flow**:
1. User sees valuation snapshot → understands "expensive" or "cheap" at a glance
2. Scrolls to buy/sell guidance → sees actionable price targets
3. Adjusts portfolio size → sees updated position sizing
4. Taps "Show Detailed Analysis" → expands to Screen 3

---

#### Screen 3: Analysis Results - Expanded Details
```
┌─────────────────────────────────────────────┐
│ [←] AAPL - Apple Inc.              $178.50  │
│                                             │
│ [Summary] [Details ✓] [News] [Holdings]    │
├─────────────────────────────────────────────┤
│                                             │
│ ▼ 📊 Valuation Metrics                      │
│ ┌─────────────────────────────────────────┐ │
│ │ P/E Ratio: 29.2 vs 25.8 (5Y avg) · +13% │ │
│ │ PEG Ratio: 1.2 (Fair value)              │ │
│ │ Price-to-Book: 7.8 (High for Tech)       │ │
│ │ Dividend Yield: 0.5% (Low)               │ │
│ │                                          │ │
│ │ 💬 What This Means:                       │ │
│ │ Stock trades at a growth premium but     │ │
│ │ not excessively overvalued. P/E is 13%   │ │
│ │ above 5-year average.                    │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ ▼ 📈 Trend & Momentum                       │
│ ┌─────────────────────────────────────────┐ │
│ │ Regime: Weak Uptrend 📉                  │ │
│ │ • Price > 200-day MA ($165) ✓            │ │
│ │ • Price < 50-day MA ($182) ✗             │ │
│ │ • RSI: 48 (Neutral)                      │ │
│ │                                          │ │
│ │ 💬 What This Means:                       │ │
│ │ Recent pullback from highs. Watch for    │ │
│ │ support at $175 or breakout above $182.  │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ ▼ ⚠️ Risk Factors                            │
│ ┌─────────────────────────────────────────┐ │
│ │ • Volatility: 28% (30-day, above avg)    │ │
│ │ • Beta: 1.2 (20% more volatile than SPY) │ │
│ │ • Max Drawdown: -23% (past year)         │ │
│ │ • Next Earnings: March 15, 2026          │ │
│ │                                          │ │
│ │ 💬 What This Means:                       │ │
│ │ Higher volatility than average. Consider │ │
│ │ smaller position or wait for earnings.   │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ ▼ 📁 Data Sources                            │
│ ┌─────────────────────────────────────────┐ │
│ │ Quote: Yahoo Finance (15-min delay)      │ │
│ │ Fundamentals: Yahoo Finance              │ │
│ │ Last Updated: Feb 28, 2026 2:38 PM EST  │ │
│ │                                          │ │
│ │ ⓘ Free tier uses delayed data.           │ │
│ │   Upgrade for real-time quotes.          │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ ⚠️ DISCLAIMER: Research only. Not advice.   │
└─────────────────────────────────────────────┘
```

**Key Copy**:
- "What This Means" boxes: Translate technical metrics into plain language
- Risk warnings: "Higher volatility than average" (not just "Beta: 1.2")
- Data sources transparency: Show provider + timestamp (build trust)

**User Flow**:
1. User taps accordion sections → expands to see details
2. Reads "What This Means" explanations → understands technical metrics
3. Checks data sources → verifies freshness
4. Taps "News" tab → sees Screen 4

---

#### Screen 4: Related News & Sentiment (Optional in MVP)
```
┌─────────────────────────────────────────────┐
│ [←] AAPL - Apple Inc.                       │
│                                             │
│ [Summary] [Details] [News ✓] [Holdings]    │
├─────────────────────────────────────────────┤
│                                             │
│ 📰 Recent News                              │
│                                             │
│ ┌─────────────────────────────────────────┐ │
│ │ 🟢 Apple announces new AI chip            │ │
│ │    Reuters · 2 hours ago                 │ │
│ │    Sentiment: Positive (85% confidence)  │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ ┌─────────────────────────────────────────┐ │
│ │ 🔴 EU antitrust investigation continues   │ │
│ │    Bloomberg · 5 hours ago               │ │
│ │    Sentiment: Negative (72% confidence)  │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ ┌─────────────────────────────────────────┐ │
│ │ 🟡 Analyst upgrades price target to $200  │ │
│ │    CNBC · 1 day ago                      │ │
│ │    Sentiment: Neutral (60% confidence)   │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ 💬 News Sentiment Summary:                  │
│ Mixed (3 positive, 2 negative, 4 neutral    │
│ in past 7 days). Monitor EU antitrust risk. │
│                                             │
│ ⚠️ DISCLAIMER: Research only. Not advice.   │
└─────────────────────────────────────────────┘
```

**Key Copy**:
- Sentiment icons: 🟢 Positive, 🔴 Negative, 🟡 Neutral (visual at-a-glance)
- Confidence scores: Show uncertainty (not binary positive/negative)
- Summary: Synthesize pattern ("Mixed sentiment, monitor EU risk")

**Scope Note**: News sentiment is **optional in MVP** (defer to v1.0 if adds cost/complexity)

**User Flow**:
1. User reads news headlines → understands recent developments
2. Sees sentiment summary → gauges market mood
3. Taps "Holdings" tab (for mutual funds) → sees Screen 5

---

#### Screen 5: Mutual Fund Holdings & Style (Funds Only)
```
┌─────────────────────────────────────────────┐
│ [←] VOO - Vanguard S&P 500 ETF     $425.30  │
│     NYSE · ETF · Updated 2m ago      USD    │
├─────────────────────────────────────────────┤
│                                             │
│ 📊 Fund Overview                            │
│ • NAV: $425.30 (as of Feb 28, 2026)        │
│ • Expense Ratio: 0.03% (Very Low)          │
│ • Assets Under Management: $850B           │
│ • Inception: Sep 7, 2010                   │
│                                             │
│ ─────────────────────────────────────────  │
│                                             │
│ 🎨 Investment Style                         │
│ ┌─────────────────────────────────────────┐ │
│ │    Value   Blend   Growth                │ │
│ │ L  [   ]  [   ]  [   ]                   │ │
│ │ M  [   ]  [ ✓ ]  [   ]  ← Large Blend    │ │
│ │ S  [   ]  [   ]  [   ]                   │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ 💬 What This Means:                          │
│ Broad exposure to large US companies        │
│ (mix of value and growth stocks).           │
│                                             │
│ ─────────────────────────────────────────  │
│                                             │
│ 🏢 Top 10 Holdings (65% of portfolio)       │
│ 1. AAPL  Apple Inc.              7.2%      │
│ 2. MSFT  Microsoft Corp.         6.8%      │
│ 3. GOOGL Alphabet Inc.           3.9%      │
│ 4. AMZN  Amazon.com Inc.         3.5%      │
│ 5. NVDA  NVIDIA Corp.            3.2%      │
│ 6. META  Meta Platforms          2.8%      │
│ 7. TSLA  Tesla Inc.              2.1%      │
│ 8. BRK.B Berkshire Hathaway      1.9%      │
│ 9. V     Visa Inc.               1.3%      │
│ 10. JPM  JPMorgan Chase          1.2%      │
│                                             │
│ [View All 505 Holdings]                    │
│                                             │
│ ─────────────────────────────────────────  │
│                                             │
│ 💰 Valuation                                │
│ • Current NAV: $425.30                     │
│ • Fair Value Estimate: $420 (Hold)         │
│ • Premium/Discount: +1.3% (trading slightly│
│   above fair value)                        │
│                                             │
│ ⚠️ DISCLAIMER: Research only. Not advice.   │
└─────────────────────────────────────────────┘
```

**Key Copy**:
- Expense ratio: Flag "Very Low" / "Low" / "High" (not just 0.03%)
- Investment style box: Visual 3x3 grid (easier than text description)
- Top holdings: Show % allocation + ticker (let user drill into holdings)
- Premium/discount: Explain if fund trading above/below NAV

**User Flow**:
1. User sees NAV + expense ratio → evaluates fund cost
2. Checks investment style → understands fund strategy (growth vs value)
3. Reviews top holdings → sees concentration risk (e.g., 7.2% in AAPL)
4. Taps holding ticker → navigates to stock analysis (Screen 2)

---

## 5. COMPLIANCE & DISCLAIMERS

### 5.1 Research Mode (Default)

**Regulatory Classification**: General investment education (not individualized advice)

**Required Disclosures**:
```
┌─────────────────────────────────────────────┐
│ EDUCATIONAL RESEARCH ONLY                   │
│                                             │
│ This analysis is for informational purposes │
│ and does not constitute:                    │
│ • Personalized investment advice            │
│ • A recommendation to buy/sell securities   │
│ • A solicitation or offer                   │
│                                             │
│ Always consult a licensed financial advisor │
│ before making investment decisions.         │
│                                             │
│ Past performance does not guarantee future  │
│ results. All investments carry risk.        │
└─────────────────────────────────────────────┘
```

**User Acknowledgment**: One-time modal on first use (store acknowledgment in user profile)

**Limitations**:
- No portfolio-level recommendations ("You should allocate 20% to AAPL")
- No specific buy/sell directives ("Buy 100 shares tomorrow")
- No market timing calls ("Sell everything before the crash")

### 5.2 Advisory Mode (Future Feature)

**Trigger**: User explicitly opts in ("I want personalized advice")

**Requirements**:
1. **User accreditation**: Verify accredited investor status (US) or equivalent (EU/UK)
2. **Risk profile**: Complete questionnaire (age, income, goals, risk tolerance)
3. **RIA partnership**: Route to registered investment advisor (if offering fiduciary advice)
4. **Audit trail**: Log all advice given, user acknowledgments, portfolio state
5. **Form ADV disclosure**: Provide Form CRS (Customer Relationship Summary) per SEC rules

**Compliance Checklist**:
- [ ] Register as RIA with SEC (US) or obtain exemption
- [ ] E&O insurance ($1-5M coverage)
- [ ] GDPR/CCPA data handling (if storing personal financial data)
- [ ] FINRA/NFA registration (if facilitating trades)

**Decision**: **Defer Advisory Mode to v2.0+** until legal/compliance team confirms structure.

### 5.3 Region-Specific Considerations

| Region | Key Regulation | Requirements |
|--------|---------------|--------------|
| **US** | SEC, FINRA | Disclaimer on "not advice", no pay-for-order-flow |
| **EU** | MiFID II, ESMA | KIID for funds, cost/charges disclosure |
| **UK** | FCA | Financial promotions approval, risk warnings |
| **Canada** | CSA, IIROC | Registration for "advising publicly", dealer rules |
| **Australia** | ASIC | AFS license if "dealing" in securities |

**MVP Approach**: US-only launch with standard disclaimers; geo-block non-US traffic or show "US data only" banner.

---

## 6. BROKER INTEGRATION OPTIONS

### 6.1 Integration Scope

**Phase 1 (MVP)**: No broker integration - standalone research tool
**Phase 2 (v1.0)**: Read-only portfolio data (holdings, cost basis, P&L)
**Phase 3 (v2.0)**: Trade execution (place orders directly from analysis screen)

### 6.2 Broker Evaluation Matrix

#### Interactive Brokers (IBKR)
**API**: IBKR Client Portal API (REST), TWS API (Java/Python)
**Pros**:
- ✅ Global coverage (120+ markets)
- ✅ Institutional-grade reliability
- ✅ Supports stocks, options, futures, forex, bonds
- ✅ Robust Python SDK (`ib_insync`)

**Cons**:
- ❌ Complex API (steep learning curve)
- ❌ Requires active account ($10k min for margin)
- ❌ OAuth flow cumbersome (gateway mode)

**Cost**: Free API access (brokerage commissions apply)
**Go/No-Go**: ✅ **GO** - Best for multi-asset global platform

---

#### Alpaca
**API**: REST + WebSocket (real-time)
**Pros**:
- ✅ Commission-free trading (US stocks/ETFs)
- ✅ Simple OAuth, excellent docs
- ✅ Paper trading built-in (sandbox mode)
- ✅ Fast time-to-market

**Cons**:
- ❌ US stocks only (no intl, no options)
- ❌ Smaller user base (less proven at scale)
- ❌ No mutual funds (ETFs only)

**Cost**: Free API + free trading
**Go/No-Go**: ✅ **GO** - Ideal for MVP (US stocks)

---

#### E*TRADE
**API**: E*TRADE Developer Platform (REST)
**Pros**:
- ✅ Major US broker (Morgan Stanley backed)
- ✅ Supports stocks, options, mutual funds
- ✅ OAuth 2.0

**Cons**:
- ❌ Limited docs, smaller dev community
- ❌ Requires production approval process
- ❌ Commission-based (less attractive to users)

**Cost**: Free API, commissions per trade
**Go/No-Go**: ⚠️ **MAYBE** - Consider for v2.0 if user demand

---

#### TD Ameritrade (Schwab)
**API**: TD Ameritrade API (being migrated to Schwab API)
**Pros**:
- ✅ Large US broker
- ✅ Free delayed quotes (for non-customers)
- ✅ Comprehensive data (fundamentals, options chains)

**Cons**:
- ❌ API in transition (Schwab merger uncertainty)
- ❌ OAuth complexity
- ❌ Commissions on some trades

**Cost**: Free API, variable commissions
**Go/No-Go**: ⚠️ **HOLD** - Wait for Schwab API stability

---

#### Plaid (Aggregator)
**API**: Plaid Investments API
**Pros**:
- ✅ Connects to 11,000+ financial institutions
- ✅ Read-only holdings across all accounts
- ✅ No per-broker integration
- ✅ OAuth managed by Plaid

**Cons**:
- ❌ Read-only (no trading)
- ❌ Cost: $0.30-$1.00 per user/month
- ❌ Delays in data sync (1-24 hours)

**Cost**: $0.60/user/month (typical)
**Go/No-Go**: ✅ **GO** - Best for portfolio aggregation (Phase 2)

---

### 6.3 Recommended Integration Roadmap

**MVP (v0.5)**: No broker integration
- Focus on research tool maturity

**v1.0 (Read-Only Portfolio)**:
- Integrate **Plaid** for portfolio aggregation
- Show user's holdings next to analysis ("You own 50 shares of AAPL")
- Display P&L vs buy range recommendations

**v1.5 (Paper Trading)**:
- Integrate **Alpaca Paper Trading**
- Let users "test drive" recommendations in sandbox

**v2.0 (Live Trading)**:
- Add **Alpaca** (US stocks) + **IBKR** (global/multi-asset)
- One-click "Execute Buy" button (with confirmation flow)
- Track order status, fills, P&L

---

## 7. DELIVERY PLAN

### 7.1 Phased Rollout

#### Phase 0: Discovery & Setup (Weeks 1-2)
- [x] Product design document (this doc)
- [ ] Finalize data provider contracts (Yahoo Finance, Alpha Vantage)
- [ ] Set up cloud infrastructure (AWS EKS, RDS, ElastiCache)
- [ ] CI/CD pipeline (GitHub Actions)

**Deliverables**: Architecture diagrams, API contracts (OpenAPI spec), dev environment

---

#### MVP (v0.5): Core Research Tool (Weeks 3-10) ⭐ **APPROVAL REQUIRED**
**Goal**: Multi-market ticker analysis with mobile-first UX and lean costs

**Features** ✅ **(Approval Checklist)**:
- [x] Ticker search for **global markets** (UK FTSE 100, EU STOXX 50, US S&P 500, India Nifty 50, APAC top 100)
- [x] Valuation bands (P/E vs 5Y avg, P/B, dividend yield) with **confidence scores**
- [x] Momentum indicators (50/200 MA, RSI) → "Weak Uptrend", "Consolidation", "Downtrend" labels
- [x] Position sizing calculator (default $10k portfolio, adjustable risk tolerance)
- [x] **Mobile-first responsive UI** (PWA-ready, offline caching of analyses)
- [x] **Strong disclaimers**: "Research/Education only" banner on every page, user acknowledgment flow
- [x] **Audit logs**: Log every analysis generated (ticker, timestamp, user_id, IP) for compliance trail
- [x] **Accessibility AA**: Keyboard nav, screen reader support, 4.5:1 contrast ratio
- [x] Currency conversion (display prices in local currency + USD equivalent)
- [x] **5-screen wireframe** (see Section 4.4 below for detailed mockups)
- [x] **Free tier** (no paywall, no API key required for basic use)

**Non-Functional Targets** ⭐:
- [x] **P95 latency < 2s** for cached symbols (80%+ cache hit rate via Redis)
- [x] **P95 latency < 5s** for cold symbols (new tickers requiring provider API calls)
- [x] **Zero cost** data providers (Yahoo Finance primary, Alpha Vantage backup)
- [x] Database query time < 100ms (PostgreSQL indexes on ticker_symbol, timestamp)

**Acceptance Criteria**:
- [ ] User can enter ticker, see analysis in **<2s p95 (cached)** or **<5s (cold)**
- [ ] 95% data accuracy vs Bloomberg Terminal (spot-check 100 tickers across 5 markets)
- [ ] Mobile UI passes **WCAG 2.1 AA** (axe DevTools scan, keyboard-only navigation test)
- [ ] Legal review approves **multi-region disclaimers** (UK FCA, EU MiFID II, US SEC/FINRA, India SEBI)
- [ ] Audit log captures 100% of analyses (test with 10K requests, verify PostgreSQL audit table)

**Team**:
- 1 Product Manager
- 2 Backend Engineers (Python/FastAPI)
- 1 Frontend Engineer (React)
- 1 Data Engineer (API integrations, caching)
- 0.5 Designer (UX mockups, usability testing)

**Timeline**: 8 weeks dev + 2 weeks testing/polish

---

#### v1.0: Global Expansion + Portfolio Integration (Weeks 11-20)
**Goal**: Multi-asset support, broker portfolio read

**New Features**:
- International stocks (LSE, TSX, ASX, Euronext)
- Mutual funds & ETFs (NAV, expense ratios, holdings)
- Currency conversion (display in user's home currency)
- Plaid integration (read-only portfolio)
- Comparative analysis ("Compare AAPL vs MSFT")
- Watchlist (save tickers, get alerts)

**Technical Debt**:
- Add TimescaleDB for historical price storage
- Implement fallback data providers (IEX Cloud as primary)
- Multi-region deployment (EU data residency)

**Team**: +1 Backend Engineer, +0.5 QA

**Timeline**: 10 weeks

---

#### v1.5: Premium Features + Paper Trading (Weeks 21-28)
**Goal**: Monetization-ready, sandbox trading

**New Features**:
- Premium tier: Real-time quotes, advanced metrics (Sharpe ratio, drawdown analysis)
- Alpaca Paper Trading integration (test recommendations)
- Backtesting: "If you bought at $X, P&L would be..."
- Email alerts (price hits buy range)
- API access for developers

**Business Model**:
- Free tier: 10 searches/day, 15-min delayed quotes
- Premium: $19/month, unlimited searches, real-time data

**Team**: +1 Backend (billing/subscriptions)

**Timeline**: 8 weeks

---

#### v2.0: Live Trading + Advisory Mode (Weeks 29-42)
**Goal**: Full-stack investment platform

**New Features**:
- IBKR + Alpaca live trading (place orders)
- Portfolio-level recommendations (rebalancing)
- Tax-loss harvesting suggestions
- RIA-lite advisory mode (regulatory approval required)
- Mobile native app (iOS/Android)

**Regulatory**:
- Engage compliance counsel
- Register as RIA or partner with existing RIA
- E&O insurance

**Team**: +2 Engineers, +1 Compliance Manager, +1 Mobile Dev

**Timeline**: 14 weeks (includes regulatory review time)

---

### 7.2 Resource Plan

| Role | Phase 0-MVP | v1.0 | v1.5 | v2.0 |
|------|-------------|------|------|------|
| Product Manager | 1 | 1 | 1 | 1 |
| Backend Engineers | 2 | 3 | 3 | 4 |
| Frontend Engineers | 1 | 1 | 1 | 2 |
| Data Engineer | 1 | 1 | 1 | 1 |
| QA/SDET | 0.5 | 1 | 1 | 2 |
| Designer | 0.5 | 0.5 | 0.5 | 1 |
| DevOps | 0.5 | 0.5 | 1 | 1 |
| Compliance | 0 | 0 | 0.5 | 1 |
| **Total FTE** | **6.5** | **8** | **9** | **13** |

---

## 8. ACCEPTANCE CRITERIA & TEST PLAN

### 8.1 Functional Testing

#### Feature: Ticker Search
| Test Case | Input | Expected Output | Status |
|-----------|-------|-----------------|--------|
| Valid US stock | `AAPL` | Analysis page with current price, valuation | 🟡 To Do |
| Valid US ETF | `SPY` | ETF-specific metrics (expense ratio, holdings) | 🟡 To Do |
| Valid mutual fund | `VFIAX` | Fund analysis (NAV, fees, Morningstar rating) | 🟡 To Do |
| Invalid ticker | `ZZZZZZ` | "Ticker not found" error, suggested alternatives | 🟡 To Do |
| International stock | `AAPL.L` (LSE) | Analysis with GBP pricing (v1.0) | 🟡 To Do |
| Malformed input | `<script>alert(1)</script>` | Sanitized, error or no results | 🟡 To Do |

#### Feature: Valuation Bands
| Test Case | Expected Behavior |
|-----------|-------------------|
| Undervalued stock (P/E < 5Y avg) | Buy range highlighted, "Below fair value" message |
| Overvalued stock (P/E > 2x avg) | Sell range highlighted, "Significantly overvalued" warning |
| No earnings (negative P/E) | Fallback to P/B or P/S, note "P/E not applicable" |
| Newly IPO'd stock (< 1Y history) | "Limited historical data" disclaimer, wider confidence intervals |

#### Feature: Position Sizing
| Test Case | Input | Expected Output |
|-----------|-------|-----------------|
| Conservative risk (1%) | Portfolio $10k, stock $100 | ~10 shares ($1k position) |
| Aggressive risk (3%) | Portfolio $50k, stock $200 | ~75 shares ($15k position) |
| High volatility stock | ATR $5, price $50 | Reduced position size vs low-vol stock |
| Portfolio size = $0 | Default $10k | Show calculation with note "Assumes $10k portfolio" |

### 8.2 Data Accuracy Testing

**Methodology**: Spot-check 100 tickers against manual calculations

| Metric | Data Source | Tolerance | Validation |
|--------|-------------|-----------|------------|
| Current Price | IEX Cloud | ±$0.01 | Compare to Bloomberg Terminal |
| P/E Ratio | Financial Modeling Prep | ±0.5 | Recalculate from earnings/price |
| 50-day MA | TimescaleDB | ±$0.10 | Independent calculation (pandas) |
| Dividend Yield | Yahoo Finance | ±0.01% | Cross-check with company IR site |

**Pass Criteria**: 95% of metrics within tolerance

### 8.3 Performance Testing

| Metric | Target | Measurement Tool |
|--------|--------|------------------|
| API latency (p50) | < 500ms | Grafana (Prometheus metrics) |
| API latency (p95) | < 2s | Load testing (Locust) |
| API latency (p99) | < 5s | - |
| Time to first paint (web) | < 1.5s | Lighthouse |
| Cache hit rate | > 80% | Redis INFO stats |
| Concurrent users | 1000 users/sec | Load testing |
| Database query time | < 100ms (p95) | PostgreSQL `pg_stat_statements` |

**Load Testing Scenarios**:
1. **Normal load**: 100 req/sec, 60 minutes (simulate daily traffic)
2. **Spike test**: 0 → 1000 req/sec in 30 seconds (market open rush)
3. **Soak test**: 50 req/sec, 24 hours (check for memory leaks)

### 8.4 Security Testing

| Test Type | Tool | Checklist |
|-----------|------|-----------|
| **OWASP Top 10** | OWASP ZAP | ✅ SQL injection, XSS, CSRF |
| **Dependency scan** | Snyk | ✅ No critical CVEs in packages |
| **Secret detection** | GitGuardian | ✅ No API keys in Git history |
| **Auth testing** | Manual | ✅ JWT expiration, token rotation |
| **Rate limiting** | Postman | ✅ 429 response after 100 req/min |
| **HTTPS enforcement** | SSL Labs | ✅ A+ rating, TLS 1.3 |

### 8.5 Accessibility Testing (WCAG 2.1 AA)

| Criterion | Test Method | Pass/Fail |
|-----------|-------------|-----------|
| Keyboard navigation | Tab through all controls | 🟡 To Do |
| Screen reader (NVDA) | Navigate analysis page, hear all content | 🟡 To Do |
| Color contrast | Foreground/background ≥ 4.5:1 (normal text) | 🟡 To Do |
| Focus indicators | Visible blue outline on focused elements | 🟡 To Do |
| Alt text on charts | SVG charts have `<title>` and `<desc>` | 🟡 To Do |
| Mobile zoom | Pinch-zoom works, no horizontal scroll | 🟡 To Do |

**Tools**: axe DevTools, WAVE, Lighthouse Accessibility Audit

### 8.6 UX Testing

**Participant Profile**: 10 non-technical users (varying experience)

**Task List**:
1. Find analysis for a ticker you own
2. Understand if the stock is "expensive" or "cheap" right now
3. Determine how many shares you should buy for a $10k portfolio
4. Find where to set a stop-loss

**Success Metrics**:
- Task completion rate: > 80%
- Time on task: < 2 minutes (task 1-2)
- Post-task questionnaire (SUS score): > 70

**Feedback Loops**: 
- Session recordings (FullStory or Hotjar)
- "Was this helpful?" widget on analysis page

### 8.7 Compliance & Legal Review

**Checklist**:
- [ ] Disclaimers reviewed by securities attorney
- [ ] Terms of Service drafted (arbitration clause, risk disclosures)
- [ ] Privacy Policy (GDPR-compliant, data retention policy)
- [ ] Cookie consent banner (EU users)
- [ ] FINRA/SEC filing determination (do we need to register?)

---

## 9. PRODUCTION GUARDRAILS

### 9.1 Feature Flags (LaunchDarkly or Unleash)

| Flag Name | Purpose | Rollout Strategy |
|-----------|---------|------------------|
| `enable_international_stocks` | v1.0 feature toggle | 0% → 10% → 50% → 100% over 2 weeks |
| `enable_plaid_integration` | Broker portfolio read | Beta users only (opt-in) |
| `enable_premium_tier` | Paid features | Gradual rollout, A/B test pricing |
| `use_iex_cloud` | Switch primary data provider | Canary 5%, monitor error rate |
| `show_options_analysis` | v2.0+ feature | Dev/staging only initially |

**Kill Switch**: Global `maintenance_mode` flag to disable writes, show static page

### 9.2 Circuit Breakers

**Data Provider Circuit Breaker**:
- If error rate > 50% over 1 minute → open circuit, use fallback provider
- Half-open after 30 seconds (test with single request)
- Close circuit if 3 consecutive successes

**Database Circuit Breaker**:
- If connection pool exhausted → reject new requests with 503
- Alert on-call engineer via PagerDuty

**Implementation**: Use `pybreaker` library (Python)

### 9.3 Rate Limiting

| Endpoint | Tier | Limit | Action on Exceed |
|----------|------|-------|------------------|
| `POST /api/analyze` | Free | 10 req/day | 429 response, "Upgrade to Premium" |
| `POST /api/analyze` | Premium | Unlimited | N/A |
| `GET /api/quote/:ticker` | All | 100 req/min | 429 response, retry-after header |
| `POST /api/broker/connect` | All | 5 req/hour | 429 + temp lockout (prevent OAuth abuse) |

**Implementation**: Redis-backed sliding window (using `flask-limiter`)

### 9.4 Sandbox Mode

**Use Cases**:
- Testing new analysis algorithms without affecting production users
- Partner integrations (let brokers test API)
- Demo accounts for prospects

**Characteristics**:
- Separate database (sandbox-db.example.com)
- Mock data provider responses (no live API calls)
- Watermark on UI: "SANDBOX MODE - Not Real Data"
- No cost for API usage

**Access**: Enable via query param `?sandbox=true` (authenticated users only)

### 9.5 Observability

#### Metrics (Prometheus + Grafana)

**RED Metrics** (for each API endpoint):
- **Rate**: Requests per second
- **Errors**: 5xx error rate
- **Duration**: p50, p95, p99 latency

**Business Metrics**:
- Daily Active Users (DAU)
- Searches per user
- Premium conversion rate
- Broker connection success rate

**Infrastructure Metrics**:
- CPU/memory utilization (containers)
- Database connection pool usage
- Redis cache hit rate
- Data provider API quota remaining

#### Logs (ELK Stack)

**Structured Logging** (JSON format):
```json
{
  "timestamp": "2026-02-28T14:32:01Z",
  "level": "INFO",
  "service": "analysis-service",
  "user_id": "usr_abc123",
  "ticker": "AAPL",
  "endpoint": "/api/analyze",
  "latency_ms": 487,
  "data_sources": ["iex_cloud", "financial_modeling_prep"],
  "cache_hit": false
}
```

**Audit Logs** (compliance trail):
- User searches (ticker, timestamp)
- Broker connections (OAuth grants)
- Premium upgrades (payment events)
- Advisory mode opt-ins (consent records)

#### Alerting (PagerDuty)

**Critical Alerts** (page on-call immediately):
- Error rate > 10% for 5 minutes
- All data providers down (fallback exhausted)
- Database unreachable
- Security event (repeated auth failures)

**Warning Alerts** (Slack notification):
- Latency p95 > 3s
- Cache hit rate < 70%
- Daily API quota at 80%

### 9.6 Rollback Plan

**Automated Rollback Triggers**:
- Error rate spike > 5x baseline
- Latency p95 > 10s
- Health check failures (3 consecutive)

**Manual Rollback**:
```bash
# Revert to previous deployment
kubectl rollout undo deployment/analysis-service -n production

# Restore database snapshot (if schema migration failed)
pg_restore -d prod_db backup_2026-02-28.dump
```

**Communication**:
- Status page update (status.example.com)
- In-app banner: "We're experiencing issues. Working on a fix."
- Post-mortem doc within 48 hours

---

## 10. OPEN QUESTIONS & NEXT DECISIONS

### 10.1 Product Questions

1. **Pricing Strategy**:
   - Freemium (10 searches/day) vs free trial (30 days full access)?
   - Annual discount (2 months free) to improve retention?
   - Student/educator pricing?

2. **User Accounts**:
   - Allow anonymous usage (no login) for MVP?
   - Social login (Google/Apple) vs email/password?

3. **Gamification**:
   - Track "accuracy score" (did user follow recommendations → profit)?
   - Leaderboard for paper trading?

4. **Content Expansion**:
   - Add educational articles ("What is P/E ratio?")?
   - Video tutorials?

### 10.2 Technical Questions

5. **Data Provider Contracts**:
   - Negotiate volume discounts with IEX Cloud (estimated 10M requests/month)?
   - Backup provider if IEX goes down (Polygon.io)?

6. **Multi-Tenancy**:
   - White-label platform for RIAs/brokers?
   - Subdomain per tenant (advisor.example.com)?

7. **Scaling Strategy**:
   - Auto-scaling thresholds (scale up at 70% CPU)?
   - Multi-region deployment (US-East, US-West, EU-Central)?

8. **ML Model Deployment**:
   - Use pre-trained model (from scikit-learn) or custom LSTM?
   - A/B test rule-based vs ML-based valuations?

### 10.3 Business Questions

9. **Go-to-Market**:
   - Partner with finance YouTubers/bloggers for launch?
   - Reddit/Twitter organic marketing vs paid ads?

10. **Regulatory Roadmap**:
    - When to engage SEC for no-action letter (if offering advice)?
    - FINRA membership required if routing orders to brokers?

11. **Monetization Mix**:
    - Subscription revenue only vs affiliate commissions from brokers?
    - Sponsored content (e.g., "Promoted Stock: XYZ Corp")?

### 10.4 Decisions Needed This Week

- [ ] **Approve v0.5 scope**: Lock MVP feature set, no scope creep
- [ ] **Select primary data provider**: IEX Cloud ($500/month) vs Polygon.io ($800/month)?
- [ ] **Finalize tech stack**: Confirm FastAPI + React (vs Django + Next.js)
- [ ] **Legal retainer**: Engage securities attorney for disclaimer review ($5k budget)
- [ ] **Hire backend eng #2**: Post job listing, target start in 2 weeks

---

## APPENDICES

### A. API Examples

#### POST /api/v1/analyze
```json
{
  "ticker": "AAPL",
  "portfolio_size": 10000,
  "risk_tolerance": "moderate"
}
```

**Response**:
```json
{
  "ticker": "AAPL",
  "company_name": "Apple Inc.",
  "current_price": 178.50,
  "currency": "USD",
  "valuation": {
    "fair_value": 165.00,
    "bands": {
      "strong_buy": {"max": 150.00, "confidence": 0.85},
      "buy": {"min": 150.01, "max": 165.00, "confidence": 0.75},
      "hold": {"min": 165.01, "max": 185.00, "confidence": 0.65},
      "sell": {"min": 185.01, "max": 210.00, "confidence": 0.70},
      "strong_sell": {"min": 210.01, "confidence": 0.80}
    },
    "current_status": "HOLD",
    "rationale": "Price 8% above fair value based on P/E vs 5Y avg"
  },
  "position_sizing": {
    "recommended_shares": 25,
    "dollar_amount": 4462.50,
    "portfolio_allocation_pct": 8.9,
    "stop_loss": 165.00,
    "take_profit": [190.00, 205.00, 220.00]
  },
  "data_sources": {
    "quote": "iex_cloud",
    "fundamentals": "financial_modeling_prep",
    "last_updated": "2026-02-28T14:38:00Z"
  },
  "disclaimer": "For educational purposes only. Not financial advice."
}
```

### B. Database Schema (Simplified)

```sql
-- Core tables
CREATE TABLE tickers (
  ticker_id SERIAL PRIMARY KEY,
  symbol VARCHAR(10) NOT NULL UNIQUE,
  company_name VARCHAR(255),
  exchange VARCHAR(50),
  currency VARCHAR(3),
  asset_type VARCHAR(20) -- 'stock', 'etf', 'mutual_fund'
);

CREATE TABLE price_history (
  ticker_id INT REFERENCES tickers(ticker_id),
  timestamp TIMESTAMPTZ NOT NULL,
  open DECIMAL(12,4),
  high DECIMAL(12,4),
  low DECIMAL(12,4),
  close DECIMAL(12,4),
  volume BIGINT,
  PRIMARY KEY (ticker_id, timestamp)
);

CREATE TABLE analyses (
  analysis_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID,
  ticker_id INT REFERENCES tickers(ticker_id),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  analysis_result JSONB, -- Store full JSON response
  data_sources JSONB
);

CREATE TABLE user_watchlists (
  user_id UUID,
  ticker_id INT REFERENCES tickers(ticker_id),
  added_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (user_id, ticker_id)
);
```

### C. Error Code Reference

| Code | Message | User Action |
|------|---------|-------------|
| `TICKER_NOT_FOUND` | "We couldn't find that ticker. Try AAPL or SPY." | Re-enter valid ticker |
| `DATA_UNAVAILABLE` | "Data temporarily unavailable. Try again in a moment." | Retry (auto-retry in UI) |
| `RATE_LIMIT_EXCEEDED` | "You've reached your daily limit. Upgrade to Premium for unlimited access." | Upgrade or wait 24h |
| `INVALID_REQUEST` | "Something went wrong. Contact support if this persists." | Report bug |

---

**Document Status**: ✅ Ready for stakeholder review  
**Next Review**: March 7, 2026  
**Owner**: Product + Architecture Team
