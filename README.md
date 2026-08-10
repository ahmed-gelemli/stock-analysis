# Stock Analysis Archive

A dated log of research-grade single-stock analyses. Each report is a snapshot: what the
market appeared to be pricing on a given day, where the analysis differed, and what would
have proven it wrong.

**[Browse the index →](index.md)**

## What's here

Each ticker has its own folder, with one file per report dated to the day it was produced
(`HROW/2026-08-09.md`). Reports are never overwritten — revisiting a thesis adds a new
dated file alongside the old one, so the archive preserves what was believed and when.

Every report carries YAML frontmatter (ticker, mode, scenario probabilities and prices,
probability-weighted value, next catalyst), so the set can be scanned or queried without
opening each file. `index.md` is the human-readable version of the same thing.

## How to read a report

- **Mode** — `QUICK`, `STANDARD`, or `DEEP`. Sets the depth and rigor the numbers were
  held to. A QUICK read is not a DEEP one with fewer words.
- **DATA AS-OF** — every report opens with the vintage of its inputs and an explicit
  **NOT RETRIEVED** list. Figures are sourced or computed, never recalled from memory;
  anything unavailable is named rather than filled in.
- **Scenarios** — bear/base/bull with explicit probabilities, not a single target. The
  spread is the point.
- **Staleness** — a report whose earnings date or catalyst has since passed should be
  treated as expired, not merely old. The scenario numbers were conditioned on that event
  being in the future.

## Not investment advice

Research and analysis only. Not personalized to anyone's circumstances, no fiduciary
relationship, no position sizes, allocations, or buy/sell instructions — and these are not
meant to be aggregated into a signal list. Data is as-of the date on each report; verify
independently before acting on anything here.
