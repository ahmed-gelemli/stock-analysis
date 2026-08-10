# Earnings Quality

Reported earnings are an opinion. Cash is a fact. This file is the checklist for finding the gap between them, with formulas and thresholds.

Run the full list in DEEP mode. In STANDARD mode, run it and report only what trips.

---

## 1. The non-GAAP to GAAP bridge

Pull the reconciliation table from the earnings release. For each add-back, ask whether it recurs.

| Add-back | Verdict |
|---|---|
| Stock-based compensation | **Recurring and real.** It is a cost paid in shares. Excluding it is the single largest distortion in modern reporting. |
| Amortization of acquired intangibles | Defensible for a serial acquirer only if you also treat the acquisitions as capex. |
| Restructuring charges | Legitimate once. Recurring for three or more years means it is the cost of doing business. |
| Litigation settlements | Legitimate if genuinely one-off. Check the history. |
| "Transformation" or "integration" costs | Usually recurring in disguise. |
| Impairments | Non-cash, but they mark a past capital allocation failure. Do not ignore, tally them. |

**Compute:** `SBC / revenue` and `SBC / FCF`. Above 10% of revenue is high for anything other than early-stage software. Above 50% of FCF means the "free" cash flow is being paid to employees in stock and offset by buybacks that are really compensation costs.

**Compute:** `adjusted EPS / GAAP EPS`. A widening ratio over time is a deteriorating quality trend even when both numbers rise.

---

## 2. Accruals

The strongest single documented predictor of earnings disappointment.

```
Accruals ratio (balance sheet) = (NOA_t - NOA_t-1) / average NOA
  where NOA = net operating assets = (total assets - cash) - (total liabilities - total debt)

Sloan accruals (cash flow) = (net income - CFO - CFI) / average total assets
```

Simple working version: `(net income - CFO) / total assets`.

**Threshold:** a rising accruals ratio, and particularly the top decile against the company's own history and its peer set, is a red flag. Earnings are being recognized ahead of cash.

---

## 3. Cash conversion

```
Cash conversion = FCF / net income
FCF = CFO - capex
```

**Threshold:** persistently below 0.8 needs an explanation. A growing company building working capital has one. A mature company that cannot convert earnings to cash usually has a problem.

Also check `CFO / EBITDA`. A widening gap points at working capital, cash taxes, or interest.

---

## 4. Working capital divergence

```
DSO = (accounts receivable / revenue) x days in period
DIO = (inventory / COGS) x days in period
DPO = (accounts payable / COGS) x days in period
Cash conversion cycle = DSO + DIO - DPO
```

**Thresholds:**
- Receivables growing more than 1.5x revenue growth: channel stuffing, extended terms to book revenue, or collection trouble.
- Inventory growing more than 1.5x revenue growth: a markdown cycle or demand deterioration not yet in the P&L.
- DPO stretching sharply: liquidity stress being financed by suppliers.
- Rising unbilled receivables or contract assets: revenue recognized ahead of the right to bill.

Compare the trend across eight quarters, not one. Single-quarter moves are frequently seasonal.

---

## 5. Revenue recognition and disclosure changes

Scan the 10-K and 10-Q for:
- Changes in revenue recognition policy or in the estimate of variable consideration.
- **Segment redefinition.** Almost always precedes or conceals deterioration in one segment. It also breaks historical comparability, which is often the point.
- Changes in a disclosed KPI's definition, or a KPI quietly dropped from the release. A metric that disappears was deteriorating.
- Changes in useful-life assumptions for depreciation, which flow straight to operating income.
- Capitalization thresholds changing for software development costs or contract acquisition costs.

Use EDGAR full-text search for "change in accounting estimate", "reclassified", "we revised".

---

## 6. Repeated one-time items

Tally "one-time", "non-recurring", "unusual", and "special" charges across the last five years. Three or more consecutive years of restructuring is a permanent cost line that management has renamed.

**Compute:** five-year sum of "one-time" charges as a percentage of five-year cumulative GAAP net income. Above 30% and the adjusted numbers are fiction.

---

## 7. Auditor and filing signals

These are the highest-specificity red flags in the list. Each is rare, and each is serious.

- **Auditor change**, especially to a smaller firm, and especially mid-year. Read the 8-K Item 4.01 for whether there were disagreements.
- **Material weakness in internal control over financial reporting**, disclosed in Item 9A.
- **Restatement**, including a non-reliance 8-K (Item 4.02). This is the loudest signal available.
- **Late filing**: an NT 10-K or NT 10-Q. Read the stated reason.
- **Going concern** language or "substantial doubt" in the audit opinion.
- **Critical audit matters (CAMs)** in the audit report: the auditor is telling you which estimates are hardest. Read them.

EDGAR full-text search terms: `"material weakness"`, `"non-reliance"`, `"substantial doubt"`, `"going concern"`.

---

## 8. Tax

```
Effective tax rate (book) vs cash taxes paid (cash flow statement supplemental)
```

**Threshold:** a large and widening gap between book and cash tax rates points at aggressive deferred tax positions or one-off benefits propping up EPS. A sudden drop in the effective rate that carries the entire EPS beat is not an operating result, and should be called out as such.

Also watch: valuation allowance releases on deferred tax assets, which can produce a large non-cash earnings gain that looks like a beat.

---

## 9. Related parties and unusual capitalization

- Related-party transactions in the notes and the proxy: revenue from entities the founder controls, leases from insiders, loans to executives.
- **Capitalized costs rising**: software development, contract acquisition costs, capitalized interest. Compare capitalized development spend against the R&D expense line. A shift from expensing to capitalizing lifts current earnings and defers the cost.
- Off-balance-sheet arrangements, variable interest entities, and receivables factoring or supply-chain finance programs, which flatter DPO and hide leverage.

---

## 10. Insider and governance signals

- **Form 4 clusters.** Distinguish discretionary sales from 10b5-1 plan sales (the form indicates plan participation). A cluster of discretionary sales by multiple officers is the meaningful pattern. Routine plan sales are noise.
- **CFO departure**, particularly an abrupt one without a named successor. The single most-watched personnel signal.
- Compensation structure: what metrics the incentive plan actually pays on. If it pays on adjusted EPS, expect adjusted EPS to be managed. If it pays on revenue growth, expect acquisitions.
- Dual-class structure, controlled-company exemptions, and a board without independent oversight of audit.
- Auditor fees: a large ratio of non-audit fees to audit fees compromises independence.

---

## 11. Debt and liquidity stress

- **Maturity wall**: the schedule by year from the 10-K debt note, against current market refinancing rates. A company with 4% coupons maturing into an 8% market has an earnings problem that has not appeared yet.
- Covenant headroom, and whether covenants were amended or waived.
- Revolver drawn versus available.
- For non-earners: `cash / quarterly burn` gives runway in months. Under 12 months makes dilution near certain, and the terms will be poor.
- Shelf registrations and ATM programs, which signal intended issuance. Check the S-3 and any 424B prospectus supplements.

---

## Scoring

There is no composite score. Report the checklist result plainly:

```
EARNINGS QUALITY: [n] flags tripped

Tripped:
  - Receivables +34% vs revenue +19% (Q2 10-Q, filed 2026-07-24). DSO up 11 days
    over four quarters. Company attributes to enterprise mix shift; unverified.
  - SBC 14% of revenue, 61% of FCF. Buybacks 0.9x SBC, so net share count +1.2% y/y.

Clean:
  - Cash conversion 1.06, stable
  - No auditor change, no material weakness, no restatement, filings timely
  - Book tax 21.4% vs cash tax 19.8%, gap stable

Not assessed: [list what you could not check and why]
```

Never present a clean bill of health for checks you did not run. "Not assessed" is a required category.
