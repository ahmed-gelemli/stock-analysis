# Stock Analysis Archive

Research-grade single-stock analyses produced with the `stock-analyst` skill. This is a
research log, not advice, and not a signal service — see the disclosure at the bottom of
every report.

## Structure

```
stock-analysis/
  CLAUDE.md               <- this file: how to work in this repo
  README.md               <- short orientation for people browsing the repo
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

## The template

`_template.md` is the single source of truth for report structure — YAML frontmatter plus
the fixed numbered sections. Read it rather than reconstructing the skeleton from memory,
and don't paste a second copy of it into this file: two copies drift, and a report that
silently diverges from the schema breaks the frontmatter-scanning the archive depends on.

If the skill's output format changes, update `_template.md`. Existing reports stay as they
were written — they're dated snapshots, not living documents.

