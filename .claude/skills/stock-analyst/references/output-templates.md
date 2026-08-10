# Output Templates

Plain text. No emoji, no box drawing. The call comes first, provenance is at the top, and gaps are stated rather than hidden.

Rationale for the ordering: a reader wants the conclusion, then the reason to doubt it, then the evidence. Burying predictions under four sections of prose optimizes for looking thorough rather than for being used.

---

## QUICK

Default for "what's up with X", "why is X down", "thoughts on X". Six or fewer tool calls, 300 words or fewer, **no price targets.**

```
NVDA | NVIDIA Corp | NasdaqGS | USD | QUICK
Price: $223.96 (regular-session close, 2026-08-08 16:00 ET). Market closed (weekend).

WHAT MOVED
Down 4.2% over five sessions. Beta-adjusted decomposition: SOXX -3.1%, so about
-2.7% of that is sector, leaving roughly -1.5% idiosyncratic. This was mostly a
sector move, not a company-specific one.

WHY
1. [DISCLOSED] Export-license guidance updated in the 8-K filed Aug 4, affecting
   the [product] line. Company quantified the revenue exposure at $Xbn. [source]
2. [REPORTED] Reuters, Aug 6: two named customers deferring orders to Q1. [source]
3. The sector move traces to [macro or peer event] on Aug 5. [source]

NEXT CATALYST
Q2 earnings, Nov 19 (confirmed via IR). Options imply a ±8.4% move on the print
(IV30 39.7%).

PRICED IN
The export restriction is largely in the price; the stock fell 6% on the filing
date and has not recovered. The order deferrals are not, since the report is two
days old and the stock is flat since.

MAIN RISK
If the deferrals reflect demand rather than timing, the Q3 guide is at risk.

NOT RETRIEVED: current consensus estimates, short interest (last settlement is
stale), borrow cost.

Want the full workup? I can run valuation, expectations, and scenarios.

Research and analysis only, not investment advice.
```

---

## STANDARD

Default for "analyze X", "is X a buy". Roughly 20 tool calls.

```
[TICKER] | [Company] | [Exchange] | [Currency] | Mode: STANDARD

DATA AS-OF
  Quote:        $XXX.XX | type: [last trade / close / delayed 15m / pre / post]
                | as-of: YYYY-MM-DD HH:MM ET
  Session:      [regular open / closed / pre / post / weekend / holiday]
  Fundamentals: FY/Q ending YYYY-MM-DD, filed YYYY-MM-DD, source [10-K/10-Q/8-K]
  Estimates:    consensus as-of YYYY-MM-DD, provider [name], n = N analysts
  Positioning:  short interest settlement YYYY-MM-DD; 13F quarter ending YYYY-MM-DD
  Fiscal year:  ends [MM-DD]. Current quarter is FY__ Q_.
  Staleness:    [anything >5 trading days old that the thesis depends on]

NOT RETRIEVED
  - [each gap, explicitly. This list is decision-relevant, do not bury it]

THE CALL IN THREE LINES
1. What the market is pricing: at $X, roughly A% revenue CAGR to a B% terminal
   FCF margin.
2. Where I differ and why: [one sentence, with the evidence]
3. What would prove me wrong: [the single strongest falsifier]

---

## 1. Price and positioning

Price, adjusted total return over 5d/1m/3m/YTD/1y, 52-week range and distance
from each extreme, 50d and 200d MAs.

Relative strength vs [sector ETF] and vs [index] over the same windows.

Move attribution for the period in question:
  stock  -X.X%
  less beta x index    -X.X%
  less sector residual -X.X%
  = idiosyncratic      -X.X%    [and what that means]

Positioning: float, short interest % of float, days to cover, borrow, IV30 and
IV rank, options-implied earnings move, ADV in shares and dollars, index events
in the horizon, recent Form 4 activity (discretionary vs 10b5-1).

## 2. Business and financials

What the company does, by segment and geography, as % of revenue and % of profit.
Customer concentration.

Growth decomposition: organic / acquired / FX / price / volume. Share direction.
Margins: gross margin trend and driver, opex leverage, incremental margin.
Cash: FCF, FCF margin, cash conversion, capex intensity, working capital direction.
Balance sheet: net debt, EV, net debt/EBITDA, interest coverage, maturity wall
  against current refi rates.
Share count: diluted trend, SBC as % of revenue and FCF, net buyback yield.

EARNINGS QUALITY: [n] flags tripped
  Tripped: [specific, with the number and the filing it came from]
  Clean:   [what was checked and passed]
  Not assessed: [what could not be checked, and why]

## 3. Expectations

Consensus: revenue/EPS/[key metric] for current quarter and next FY. Provider,
  date, n analysts, high-low dispersion.
Guidance vs consensus: [above / in line / below], by how much.
Revisions momentum: EPS consensus direction over 1m and 3m.
Beat/miss history: last 8 quarters, magnitude, and the 1-day and 30-day reaction.
Guidance philosophy: [sandbagger / stretcher], with the evidence.

REVERSE DCF: at $X, holding WACC at Y% and terminal margin at Z%, the price
requires A% revenue CAGR over five years. Consensus is B%. The company delivered
C% over the last five years. Implied terminal-year revenue is D% of the addressable
market, versus E% today. [Plausible or not, and why.]

## 4. Catalysts

Deduplicated to primary events. Every causal link tagged.

[DATE] [Event] [DISCLOSED/REPORTED/ATTRIBUTED/INFERRED/UNKNOWN]
  What happened, with the source.
  Why it happened, one level deeper ONLY if sourced.
  Priced in? [evidence from the price reaction, not an assertion]

For every [INFERRED] link:
  Inferred: [claim]
  Competing explanation: [alternative]
  Distinguisher: [the observation that separates them, and when it is observable]

Disconfirming search run: [yes]. Strongest bear source found: [name, link].

## 5. Macro, sector, competitive

Only factors with a demonstrated transmission mechanism to this company, with the
mechanism stated. Sector performance and whether this name leads or lags it.

Comps table:
  Company | Rev growth | GM | EBIT margin | FCF margin | ROIC | ND/EBITDA |
  EV/Sales | EV/EBITDA | P/E

ROIC [X]% vs WACC [Y]%: growth here [creates / destroys] value.
Market share: [figure, source, direction].
Governance: [share structure, capital allocation record, anything material].

## 6. Valuation

Method 1: [name]
  Assumptions: [every one]
  Output: $X
Method 2: [name]
  Assumptions: [every one]
  Output: $Y
Reconciliation: [why they differ, and which you weight more]

Implied forward multiple at target: [X]x vs the stock's 3-5yr range of [A-B]x
and peers at [C]x. [Justification for any re-rating implied.]

Expected return decomposition to the base target:
  EPS growth        +X%
  Multiple change   +Y%     <- if this exceeds half the total, it is a re-rating bet
  Dividend yield    +Z%
  Net buyback yield +W%
  Total             +N%

## 7. Bull case / bear case

BULL (steelmanned): [the strongest version, as its holders would put it]
  Who holds it and why: [named, where retrievable]
BEAR (steelmanned): [the strongest version, as a short seller would put it]
  Who holds it and why: [named, where retrievable]
Where I land, and the specific point of disagreement:

## 8. Scenarios

  Bear  P=xx%  $xxx   [drivers]
  Base  P=xx%  $xxx   [drivers]
  Bull  P=xx%  $xxx   [drivers]
  Probabilities sum to 100%. Probability-weighted value: $xxx

  1-month ~68% band from IV: $xxx to $xxx   (IV30 = xx.x%, sigma_1m = x.xx)
  Center shifted [n] sigma [above/below] spot because [reason].
  Options-implied earnings move: ±x.x%
  P(up over 12 months) = xx%   [base rate is 53-57%; justification for the delta]

  Asymmetry: (upside to base) / (downside to bear) = x.x : 1

## 9. What would change my mind

1. [observable] [threshold] [by date] -> [conclusion]
2. [observable] [threshold] [by date] -> [conclusion]
3. [observable] [threshold] [by date] -> [conclusion]

Review triggers:
  Scheduled: [earnings date verified via IR, investor day, regulatory dates]
  Unscheduled: 8-K, guidance revision, >2-sigma one-day move, sector shock

## 10. Risks and frictions

Liquidity: ADV [X] shares / $[Y], typical spread [Z]%.
Event risk in the horizon: [earnings, regulatory, legal, binary readouts]
If bearish: borrow at [X]%, [availability], squeeze risk at [Y]% of float short.
Concentration: [if the user disclosed existing exposure]
Frictions: [spread, slippage, tax treatment at this horizon, jurisdiction caveat]

Good company vs good stock at this price: [answer both, separately]

## 11. Sources

[1] [Source name], [document type], [date]. [URL]
[2] ...

Research and analysis only. Not investment advice, not personalized to your
circumstances, no fiduciary relationship. Figures are as-of the timestamps above;
verify before acting.
```

---

## DEEP

The STANDARD structure, plus:

- **Section 2 expanded**: eight quarters of revenue, gross margin, EBIT margin, FCF, and diluted shares as a table. Segment detail with segment operating margin. The full earnings-quality checklist with every item marked pass, fail, or not assessed.
- **Section 5 expanded**: full comps table with five or more peers, ROIC over five years, and a market-share time series.
- **Section 6 expanded**: sensitivity grid (fair value across WACC ±1pt and terminal growth or margin ±1pt), and a third valuation method.
- **Section 7 expanded**: named holders on each side where retrievable from 13F and 13D data, with the caveat about filing lag, and the specific point at which the two theses become empirically distinguishable.
- **Section 8 expanded**: a scenario tree where a binary event sits inside the horizon, with the probability-weighted value computed at each node.

---

## DEGRADED

Emit this when three or more required snapshot fields are [N/A], or the completion gate fails. **No price targets, no directional call.**

```
[TICKER] | [Company] | Mode: DEGRADED

I could not retrieve enough to support a view. Here is what I have and what is
missing.

RETRIEVED
  [each item with its source, timestamp, and URL]

NOT RETRIEVED, and why
  - Current price: [what was attempted, what failed]
  - Consensus estimates: [what was attempted, what failed]
  - [etc]

WHAT THIS MEANS
Without [the specific missing items], I cannot [value the company / build a
volatility-anchored range / assess whether the news is priced in]. Producing a
target on what I have would mean filling the gaps from memory, and figures
recalled that way are stale by construction and indistinguishable in the output
from retrieved ones. So I am not doing it.

WHAT I CAN STILL SAY
  [any genuinely sourced observations, clearly bounded]

WHAT YOU CAN CHECK YOURSELF
  - [specific source and what to look for]
  - [specific source and what to look for]

Tell me if you can supply [the missing pieces] and I will complete the analysis.

Research and analysis only, not investment advice.
```

The DEGRADED output is a success, not a failure. Silent gap-filling is the failure.

---

## Formatting rules

- Plain text and markdown headers. No emoji, no box-drawing characters. They signal retail newsletter rather than research, and they make an unsourced number feel authoritative.
- Every number in the body traces to a numbered source, or to a computation whose inputs trace to sources.
- The NOT RETRIEVED list goes near the top, never in a footnote.
- Probabilities are numeric percentages that sum to 100%.
- Every range states its coverage.
- One disclaimer, at the end.
