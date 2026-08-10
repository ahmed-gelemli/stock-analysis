# Stock Analysis Archive

Research-grade single-stock analyses produced with the `stock-analyst` skill. This is a
research log, not advice, and not a signal service — see the disclosure at the bottom of
every report.

## Structure

```
stock-analysis/
  CLAUDE.md               <- this file
  index.md                <- one-row-per-report log across all tickers, newest first
  _template.md             <- blank skeleton matching the skill's STANDARD output
  <TICKER>/
    <YYYY-MM-DD>.md        <- one file per report, dated to the day it was produced
```

- Each ticker gets its own folder (`DLO/`, `NVDA/`, ...). A ticker can accumulate multiple
  dated reports over time as the thesis is revisited — never overwrite an old report, add
  a new dated file next to it.
- The filename date is the report's `DATA AS-OF` / analysis date, not the price-as-of date
  (those can differ, e.g. a Monday report citing Friday's close).
- Every report file carries YAML frontmatter (ticker, mode, key scenario numbers) so the
  set can be scanned or queried without opening each file.

## Conventions carried over from the skill

- **Numbers discipline.** Every figure in a report is sourced, computed, or explicitly
  marked not-retrieved. Never edit a report to insert a number from memory.
- **Not advice.** No report states a position size, an allocation, or a buy/sell
  instruction. That constraint applies to this archive too — don't summarize these into
  a signal list.
- **Staleness.** Reports are snapshots. A report with an earnings date, guidance, or
  catalyst inside its horizon should be treated as stale the moment that event passes —
  re-run the skill for an update rather than trusting the old scenario numbers.
- **Mode** (QUICK / STANDARD / DEEP) is recorded in the frontmatter and the report header.
  It sets the depth/rigor the numbers below were held to.

## Adding a new report

1. Run the `stock-analyst` skill for the ticker.
2. Create `<TICKER>/<YYYY-MM-DD>.md` from `_template.md`, fill it in.
3. Add one row to `index.md` (newest entries at the top of the table).

## Report template (`_template.md`)

Every report file follows this skeleton — YAML frontmatter plus a fixed set of numbered
sections:

```markdown
---
ticker: ""
company: ""
exchange: ""
currency: ""
mode: ""              # QUICK | STANDARD | DEEP | DEGRADED
analysis_date: ""      # YYYY-MM-DD, date the report was produced
price_as_of: ""        # YYYY-MM-DD, date of the quoted price
price_at_analysis: null
next_catalyst: ""      # e.g. next earnings date, verified from IR/8-K/6-K
next_catalyst_date: ""
scenarios:
  bear: {prob: null, price: null}
  base: {prob: null, price: null}
  bull: {prob: null, price: null}
probability_weighted_value: null
escalation_class: "none"   # none | microcap | pump-and-dump | high-short-interest |
                            # leveraged-etf | options | spac | mnpi | vulnerable-user
---

# TICKER | Company | Exchange | Currency | Mode: ___

## DATA AS-OF
```
Quote:        ...
Session:      ...
Fundamentals: ...
Estimates:    ...
Positioning:  ...
Staleness:    ...
```

**NOT RETRIEVED:**

## The call in three lines
1. What the market is pricing:
2. Where I differ and why:
3. What would prove me wrong:

## 1. Price and positioning
## 2. Business and financials
## 3. Expectations
## 4. Catalysts
## 5. Macro, sector, competitive
## 6. Valuation
## 7. Bull case / bear case
## 8. Scenarios
## 9. Risks and frictions
## 10. What would change my mind
## 11. Sources

---
Research and analysis only. Not investment advice, not personalized to your circumstances,
no fiduciary relationship. Data as-of above; verify before acting.
```
