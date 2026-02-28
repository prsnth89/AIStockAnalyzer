# AI Stock Analyzer - Copilot Instructions

## Project Overview
Global stocks and mutual-funds analysis platform that generates research-oriented "Buy range / Sell plan / Rationale" insights for educational purposes (not individualized financial advice).

## Current Status: Day 1 Prototype (v0.1)
**Scope**: US stocks only, Yahoo Finance free tier, simple Flask web app  
**Timeline**: 1 day build  
**Deployment**: Local dev server (http://localhost:5000)

## Day 1 Architecture (Simplified)

**Stack**:
- **Backend**: Python 3.11+, Flask (lightweight web framework)
- **Data Source**: Yahoo Finance (`yfinance` library) - free tier, US stocks
- **Frontend**: Simple HTML templates (Jinja2), minimal CSS
- **Storage**: None (stateless, fetch data on each request)
- **Deployment**: Local Flask dev server

**Data Flow**: User enters ticker → Flask route → Yahoo Finance API → Calculate valuation → Render HTML → Return to user

## Development Workflow

### Setup (15 minutes)
```powershell
# Create project structure
New-Item -ItemType Directory -Path src, tests, templates -Force

# Virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies (Day 1 minimal)
pip install flask yfinance pandas

# Test Yahoo Finance connection
python -c "import yfinance as yf; print(yf.Ticker('AAPL').info['currentPrice'])"
```

### Run Application
```powershell
# Start Flask dev server
python src/app.py

# Open browser: http://localhost:5000
```

### Testing (Manual for Day 1)
```powershell
# Test with various tickers
# AAPL (tech), JPM (finance), JNJ (healthcare), TSLA (volatile), BRK.B (edge case: no P/E)
```

## Project Structure (Day 1)

```
src/
├── app.py           # Flask app (routes, main entry point)
└── analyzer.py      # Core valuation logic (P/E bands, recommendations)
templates/
├── index.html       # Landing page (ticker search)
├── result.html      # Analysis results page
└── error.html       # Error handling page
requirements.txt     # Python dependencies (flask, yfinance, pandas)
venv/                # Python virtual environment (gitignored)
```

## Code Conventions (Day 1 Simplified)
    └── metrics.py       # Prometheus metrics (RED pattern)

frontend/
├── src/
│   ├── pages/
│   │   ├── Home.tsx     # Ticker search
│   │   └── Analysis.tsx # Valuation bands, buy/sell plan UI
│   ├── components/
│   │   ├── ValuationChart.tsx  # Price bands visualization
│   │   └── DisclaimerModal.tsx # FINRA-compliant educational disclaimer
│   └── api/
│       └── client.ts    # Axios instance with auth interceptors
```

## Code Conventions

### Python Style
- **PEP 8** + **Black** (line length: 100)
- **Type hints**: Required for all public functions
  ```python
  def calculate_valuation_bands(ticker: str, period: str = "5Y") -> ValuationBands:
  ```
- **Docstrings**: Google style with examples
  ```python
  def fetch_quote(ticker: str) -> Quote:
      """Fetch real-time quote with multi-provider fallback.
      
      Args:
          ticker: Stock symbol (e.g., "AAPL", "BRK.B")
      
      Returns:
          Quote object with price, volume, timestamp
      
      Raises:
          TickerNotFoundError: If ticker invalid across all providers
          DataUnavailableError: If all providers down (check circuit breaker)
      """
  ```

### API Response Format
Always include `data_sources` and `disclaimer` in responses:
```json
{
  "ticker": "AAPL",
  "valuation": {...},
  "data_sources": {
    "quote": "iex_cloud",
    "fundamentals": "financial_modeling_prep",
    "last_updated": "2026-02-28T14:38:00Z"
  },
  "disclaimer": "For educational purposes only. Not financial advice."
}
```

### Error Handling
Use custom exception hierarchy with error codes:
```python
class StockAnalyzerException(Exception):
    """Base exception with error_code for client handling."""
    error_code: str

class TickerNotFoundError(StockAnalyzerException):
    error_code = "TICKER_NOT_FOUND"

class DataUnavailableError(StockAnalyzerException):
    error_code = "DATA_UNAVAILABLE"
```

Map exceptions to HTTP status codes in middleware:
- `TickerNotFoundError` → 404
- `DataUnavailableError` → 503 (Service Unavailable)
- `RateLimitExceeded` → 429

### Logging Standards
Structured JSON logs with required fields:
```python
logger.info(
    "Analysis completed",
    extra={
        "ticker": ticker,
        "user_id": user_id,
        "latency_ms": latency,
        "cache_hit": cache_hit,
        "data_sources": ["iex_cloud", "financial_modeling_prep"]
    }
)
```

**Never log**: API keys, user PII (email, portfolio balances), raw error stack traces to user-facing logs

### Data Provider Patterns

**Multi-Provider Fallback**:
```python
async def fetch_with_fallback(ticker: str) -> Quote:
    providers = [IEXCloudProvider(), YahooFinanceProvider()]
    
    for provider in providers:
        try:
            quote = await provider.get_quote(ticker)
            return quote
        except ProviderError as e:
            logger.warning(f"{provider.name} failed", extra={"error": str(e)})
            continue
    
    raise DataUnavailableError("All providers unavailable")
```

**Caching Strategy**:
- Quotes: Redis TTL 5 minutes (balance freshness vs API cost)
- Fundamentals: TTL 24 hours (updated quarterly)
- Mutual fund NAV: TTL 1 hour (daily updates)
- Cache key format: `quote:{ticker}:{currency}` (e.g., `quote:AAPL:USD`)

**Currency Normalization**:
Always store prices in USD internally; convert on output:
```python
def normalize_price(price: Decimal, from_currency: str) -> Decimal:
    """Convert to USD using exchange rates from cache."""
    if from_currency == "USD":
        return price
    rate = get_exchange_rate(from_currency, "USD")  # Cached from ECB API
    return price * rate
```

### Analysis Engine Patterns

**Valuation Bands**:
- Use 5-year historical average as default (configurable: 3Y/5Y/10Y)
- Calculate confidence scores based on data completeness (penalize < 2 years history)
- Handle edge cases: negative P/E (use P/B), no earnings (use revenue multiples)

**Position Sizing**:
- Default portfolio: $10,000 (educational examples)
- Use ATR (14-day) for stop-loss distance
- Risk per trade: Conservative 1%, Moderate 2%, Aggressive 3%
- Formula: `position_size = (portfolio * risk_pct) / (current_price - stop_loss)`

**Timezone Handling**:
- Store all timestamps in UTC (PostgreSQL `TIMESTAMPTZ`)
- Convert to market timezone for display (NYSE: America/New_York)
- Handle market holidays via `pandas_market_calendars` library

### Compliance Patterns

**Disclaimers**:
- Show educational disclaimer on first app use (store acknowledgment in `user.disclaimers_accepted`)
- Include disclaimer footer on every analysis page
- Log all analyses for audit trail (retain 7 years per SEC guidance)

**Advisory Mode Guard**:
```python
def require_advisory_mode(func):
    """Decorator to enforce compliance checks for advisory features."""
    def wrapper(user: User, *args, **kwargs):
        if not user.advisory_mode_enabled:
            raise PermissionError("Advisory mode requires RIA partnership")
        if not user.risk_profile_completed:
            raise PermissionError("Complete risk profile first")
        return func(user, *args, **kwargs)
    return wrapper
```

### Testing Patterns

**Mock External APIs**:
```python
@pytest.fixture
def mock_iex_client(mocker):
    mock = mocker.patch("src.data.providers.iex.IEXCloudClient")
    mock.return_value.get_quote.return_value = Quote(
        ticker="AAPL", price=Decimal("178.50"), timestamp=datetime.utcnow()
    )
    return mock
```

**Fixture Data**:
- Store historical price CSVs in `tests/fixtures/` for reproducible backtests
- Use real tickers but snapshot data (avoid live API calls in tests)

**Acceptance Tests**:
- Tag slow tests: `@pytest.mark.slow` (skip in CI unless --slow flag)
- Run load tests nightly: `locust -f tests/load/locustfile.py --headless -u 1000 -r 100`

## Production Guardrails

**Feature Flags**: Use LaunchDarkly (or Unleash) for gradual rollouts
```python
if ld_client.variation("enable_plaid_integration", user_context, False):
    # Show broker connection UI
```

**Circuit Breakers**: Automatically open if error rate > 50% over 1 minute
```python
from pybreaker import CircuitBreaker

iex_breaker = CircuitBreaker(fail_max=5, timeout_duration=30)

@iex_breaker
async def fetch_from_iex(ticker: str) -> Quote:
    # Will raise CircuitBreakerError if circuit open
```

**Rate Limiting**: Redis-backed sliding window
```python
@app.post("/api/v1/analyze")
@limiter.limit("10/day", key_func=get_user_id)  # Free tier
async def analyze_ticker(ticker: str, user: User):
    ...
```

**Observability**:
- Prometheus metrics: `analysis_latency_seconds`, `data_provider_errors_total`
- Grafana dashboards: RED metrics per endpoint, cache hit rates, API quota usage
- Sentry: Error tracking with release tagging
- Audit logs: User analyses, OAuth grants, premium upgrades (retain 7 years)

## Key Decisions & Context

**Why FastAPI over Django**: Async support for concurrent API calls, auto-generated OpenAPI docs, better for microservices

**Why TimescaleDB**: Optimized for time-series data (price history), better compression than PostgreSQL BRIN indexes

**Why Redis over Memcached**: Supports more data structures (sorted sets for leaderboards), pub/sub for real-time alerts

**Data Provider Choice**: IEX Cloud (primary) for reliability + SLA; Yahoo Finance (fallback) for cost control

**No ML Models in MVP**: Rule-based valuation (P/E, P/B) is transparent and easier to debug; defer neural networks to v1.5+

## Common Pitfalls

❌ **Don't** commit API keys (use `.env` + `.gitignore`)  
❌ **Don't** log user portfolio balances (PII risk)  
❌ **Don't** make synchronous API calls in endpoints (use `async`/`await`)  
❌ **Don't** bypass circuit breakers (defeats purpose of failover)  
❌ **Don't** cache quotes > 5 minutes (stale data for volatile stocks)

✅ **Do** validate ticker format before API calls (regex: `^[A-Z]{1,5}(\.[A-Z]{1,2})?$`)  
✅ **Do** use currency normalization for international stocks  
✅ **Do** include confidence intervals on valuations (avoid false precision)  
✅ **Do** test with market holiday edge cases (NYSE closed, but crypto trading)  
✅ **Do** show data sources + timestamps ("Quote from IEX Cloud, updated 2m ago")

## Reference Documents

- Full product design: [docs/PRODUCT_DESIGN.md](../docs/PRODUCT_DESIGN.md)
- API documentation: http://localhost:8000/docs (auto-generated by FastAPI)
- Architecture diagrams: [docs/architecture/](../docs/architecture/)
- Compliance checklist: [docs/COMPLIANCE.md](../docs/COMPLIANCE.md)
