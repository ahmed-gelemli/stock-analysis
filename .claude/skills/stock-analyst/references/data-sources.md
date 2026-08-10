# Data Sources

Endpoints below were tested and returned the stated results. Test dates are noted. Anything on the internet rots: check, do not assume, and fall back loudly.

---

## Source ladder

### Tier 1: authoritative. Use for anything load-bearing.

- **SEC EDGAR** filings and the `data.sec.gov` XBRL API. 10-K, 10-Q, 8-K, DEF 14A, S-1, 424B, 13D/G, 13F, Form 4, NT 10-K/10-Q.
- **Company IR**: press releases, earnings decks, prepared remarks, call transcripts, supplemental data files.
- **Exchange and CBOE** delayed quotes and options chains.
- **FINRA and Nasdaq** short interest.
- **Fed, BLS, BEA, Treasury** for macro. Never quote a macro print from a blog.

### Tier 2: context. Verify anything load-bearing against Tier 1.

Reuters, Bloomberg, WSJ, FT, Nikkei, Barron's, and trade press with named reporters. stockanalysis.com, Koyfin, Finviz, macrotrends for screening-grade figures.

### Tier 3: directional signal only. Never a citation for a number.

Sell-side notes as summarized in media, Seeking Alpha, Substack, YouTube, X, Reddit, StockTwits. These are evidence about positioning and sentiment, never about the company.

### Blocked. Do not use, and do not let them shape the narrative.

Paid IR "research" and stock-promotion newsletters. PR-wire-only coverage of microcaps. AI-generated finance content farms. Price-prediction sites ("XYZ stock forecast 2030"). Any page whose primary call to action is a subscription to trade alerts.

**Tells for AI-generated finance spam:** no named author, no dates attached to figures, generic filler ("the company continues to demonstrate strong fundamentals"), price-prediction tables running out to 2035, and dozens of ticker posts per day from the same site.

---

## Verified endpoints

Tested 2026-08-09.

### CBOE delayed quotes and full options chain

```bash
curl -s "https://cdn.cboe.com/api/global/delayed_quotes/options/NVDA.json"
```

Status: 200, about 1.7MB for a liquid name. No auth, no headers required.

Returns a top-level `timestamp` (this is the data timestamp, and it can lag by a day or more, especially over a weekend), plus `data` containing:

| Field | Meaning |
|---|---|
| `current_price` | Last trade the feed has |
| `close` | Prior regular-session close |
| `prev_day_close` | Session before that |
| `iv30` | 30-day implied volatility, in percent (e.g. `39.718`) |
| `open`, `high`, `low`, `volume` | Session OHLCV |
| `options[]` | Full chain, roughly 3,900 rows for a liquid name |

Each option row carries `option` (OCC symbol), `bid`, `ask`, `last_trade_price`, `iv`, `delta`, `gamma`, `theta`, `vega`, `open_interest`, `volume`.

**This is the single most valuable free endpoint for this skill.** It supplies IV30 for volatility-anchored ranges and the chain for the options-implied earnings move, without which Phase 8 is guesswork.

**Caution observed in testing:** the endpoint returned `timestamp: 2026-08-08 09:24:28` when queried on 2026-08-09, and `current_price` 223.80 against `close` 223.96. That is exactly the staleness and last-trade-versus-close ambiguity to surface in the as-of block, not paper over.

OCC symbol format: `NVDA260807C00050000` = ticker + YYMMDD + C/P + strike x 1000.

### SEC XBRL: single concept

```bash
curl -s -H "User-Agent: your-tool your-email@example.com" \
  "https://data.sec.gov/api/xbrl/companyconcept/CIK0001045810/us-gaap/Revenues.json"
```

Status: 200. **The User-Agent header with a contact is required by SEC policy.** Without a descriptive UA you will be blocked.

CIK must be zero-padded to 10 digits.

Useful concepts: `Revenues`, `RevenueFromContractWithCustomerExcludingAssessedTax`, `NetIncomeLoss`, `NetCashProvidedByUsedInOperatingActivities`, `PaymentsToAcquirePropertyPlantAndEquipment`, `WeightedAverageNumberOfDilutedSharesOutstanding`, `CommonStockSharesOutstanding`, `Assets`, `Liabilities`, `StockholdersEquity`, `LongTermDebtNoncurrent`, `CashAndCashEquivalentsAtCarryingValue`, `ShareBasedCompensation`, `OperatingIncomeLoss`, `GrossProfit`.

Tag usage varies by filer. If a concept 404s, pull `companyfacts` and inspect what the company actually tags.

### SEC XBRL: everything

```bash
curl -s -H "User-Agent: your-tool your-email@example.com" \
  "https://data.sec.gov/api/xbrl/companyfacts/CIK0001045810.json"
```

Status: 200, about 4MB for a large filer. Every tagged fact with `start`, `end`, `val`, `fy`, `fp`, `form`, `filed`, and `accn`. Filter by `form` to separate 10-K from 10-Q, and always read `filed` so you can state when the data became public.

### SEC submissions: filing history, fiscal year end, exchange

```bash
curl -s -H "User-Agent: your-tool your-email@example.com" \
  "https://data.sec.gov/submissions/CIK0001045810.json"
```

Status: 200. Gives `name`, `fiscalYearEnd` (as `MMDD`, so `0131` means a January fiscal year end), `exchanges`, `sicDescription`, `tickers`, plus `filings.recent` with parallel arrays of `form`, `filingDate`, `accessionNumber`, `primaryDocument`.

**Use this in Phase 0 for the fiscal calendar**, and to find the most recent 8-K, which is where the earnings-date announcement lives.

Build a document URL as:
`https://www.sec.gov/Archives/edgar/data/{CIK_no_padding}/{accession_no_dashes}/{primaryDocument}`

### CIK lookup from ticker

```bash
curl -s -H "User-Agent: your-tool your-email@example.com" \
  "https://www.sec.gov/files/company_tickers.json"
```

Status: 200, about 800KB. Maps every ticker to `cik_str` and `title`.

### EDGAR full-text search

```bash
curl -s -H "User-Agent: your-tool your-email@example.com" \
  'https://efts.sec.gov/LATEST/search-index?q=%22material+weakness%22&forms=10-K'
```

Status: 200, Elasticsearch-shaped JSON. Covers 2001 forward. Use for phrase-level red flags: "material weakness", "restatement", "going concern", "substantial doubt", "related party".

### EDGAR browse (Atom)

```bash
curl -s -H "User-Agent: your-tool your-email@example.com" \
  'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=NVDA&type=8-K&count=5&output=atom'
```

Status: 200. Convenient for pulling recent filings of one type.

### Treasury yield curve, for the risk-free rate in a DCF

```bash
curl -s "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/2026/all?type=daily_treasury_yield_curve&field_tdr_date_value=2026&page&_format=csv"
```

Status: 200, CSV with a header row and one row per business day, most recent first. Columns run 1 Mo through 30 Yr. Take the 10 Yr for a standard equity DCF, and **cite the date of the row you used.** Change the year in both the path and the query string.

### Nasdaq short interest

```bash
curl -s -A "Mozilla/5.0" \
  "https://api.nasdaq.com/api/quote/NVDA/short-interest?assetClass=stocks"
```

Status: 200. Returns a table of settlement date, short interest, average daily share volume, and days to cover. Needs a browser User-Agent. Undocumented and unstable; if it fails, fall back to FINRA's published files or stockanalysis.com.

### Yahoo Finance chart, for price history

```bash
curl -s -A "Mozilla/5.0" \
  "https://query1.finance.yahoo.com/v8/finance/chart/NVDA?range=1y&interval=1d&events=div%2Csplit"
```

Status on 2026-08-09: 200. **But treat as unreliable.** A prior test in the same environment returned 429 from both `query1` and `query2` with a browser UA. It rate-limits aggressively and blocks intermittently. Always check the status code and fall back rather than assuming a working response.

Returns `chart.result[0].meta` with `currency`, `exchangeName`, `regularMarketPrice`, `regularMarketTime` (epoch seconds), `fiftyTwoWeekHigh`, `fiftyTwoWeekLow`, and `chart.result[0].indicators.adjclose[0].adjclose` for the split- and dividend-adjusted series. **Use `adjclose`, not `close`, for any return calculation.**

Add `&range=1d&interval=1m` for intraday, which lets you timestamp a move and compare it to a news timestamp.

### stockanalysis.com

```bash
curl -s -A "Mozilla/5.0" "https://stockanalysis.com/stocks/nvda/"
```

Status: 200, HTML, about 150KB. Screening-grade multiples, financial history, and a peer list. Tier 2: fine for orientation, verify anything load-bearing against the filings.

---

## Known-blocked

- **stooq.com CSV** (`https://stooq.com/q/d/l/?s=nvda.us&i=d`): returns 200 with a JavaScript anti-bot challenge page, not CSV. Do not use.
- **Yahoo chart API**: works intermittently, returns 429 under load. Check the status code every time.

---

## Conflict resolution

```
Price:        >0.5% apart  -> do not average. Re-fetch. If still split, report both
                             with timestamps and use the later as-of.
Multiples:    >10% apart   -> almost always a definition mismatch. Resolve by
                             specifying GAAP vs adjusted, TTM vs NTM (and which
                             fiscal year), diluted vs basic share count. Report the
                             definition you chose.
Fundamentals: any disagreement with the filing -> the filing wins. Always.
```

Never silently average. Never present a reconciled-looking number you did not reconcile.

**Why multiples disagree**, in rough order of frequency: GAAP versus adjusted earnings; TTM versus NTM, and which fiscal year NTM refers to; basic versus diluted share count; whether SBC is added back; different consensus vendors; a stale share count from before a buyback or an offering; and market cap versus enterprise value.

---

## Adjustment and corporate actions

- Quote returns as split- and dividend-adjusted total return, labeled as such. If only price return is available, label it "price return, ex-dividends".
- Before quoting any multi-month return, check the window for splits, reverse splits, spin-offs, and special dividends. A 10:1 split shows a catastrophic one-year return on unadjusted data. A spin-off mechanically drops the price without any economic loss.
- A **reverse split is itself a signal**, usually of listing-compliance trouble. Note it.
- Ticker changes and reincorporations break naive history lookups.
- **ADRs:** report the local listing and the ADR ratio, and decompose the return into local performance plus FX. ADR ratios change, which produces spurious price jumps.
- **Non-USD reporters:** state the reporting currency for every financial metric. Never combine a USD market cap with local-currency revenue in a P/S ratio without converting and stating the rate and its date.

---

## Lag on every "positioning" dataset

| Dataset | Real lag |
|---|---|
| 13F holdings | Quarterly, filed up to 45 days after quarter end, so up to 4.5 months stale. Long positions only, excludes shorts and most derivatives. |
| Short interest | Bimonthly settlement, published roughly 9 business days later. |
| Form 4 insider | 2 business days after the transaction. Fast, and the most timely of these. |
| 13D | 5 business days after crossing 5%. 13G is much slower. |
| ETF flows | Often estimated, and revised. |
| Delayed quotes | 15 minutes during a session, and stale outside one. |

Phrase these correctly. "As of the Q2 filing, X held N shares" is right. "X is buying" is not.

---

## Sector ETFs for attribution and relative strength

```
Technology          XLK      Semiconductors      SOXX / SMH
Software            IGV      Communication svcs  XLC
Financials          XLF      Regional banks      KRE
Health care         XLV      Biotech             XBI / IBB
Consumer disc.      XLY      Consumer staples    XLP
Energy              XLE      Oil services        OIH
Industrials         XLI      Transports          IYT
Materials           XLB      Gold miners         GDX
Utilities           XLU      REITs               XLRE / VNQ
Homebuilders        XHB      Retail              XRT
Small cap           IWM      Broad market        SPY / QQQ
```

Use the narrowest ETF that genuinely contains the company's peer set. For a semiconductor name, SOXX beats XLK, which beats SPY.
