# Valuation Methods

A fair value estimate without a shown method is a number with no derivation and no falsifiability. Use at least two independent methods and reconcile them.

---

## Method selection

| Company type | Primary | Cross-check |
|---|---|---|
| Profitable, stable, predictable | DCF, explicit 5yr + terminal | Peer multiple on NTM |
| Profitable, cyclical | Mid-cycle normalized EPS/EBITDA x through-cycle multiple | EV/Sales vs history |
| High growth, low or no profit | Terminal-year model | EV/gross profit vs peers |
| Pre-revenue biotech | rNPV by program | Cash + pipeline option value |
| Banks | P/TBV justified by ROTCE | P/E on normalized provisions |
| REITs | NAV (cap rate on forward NOI) | P/AFFO vs peers |
| E&P and miners | NAV on a stated commodity deck | EV per flowing unit |
| Multi-segment | Sum of the parts | Consolidated EV/EBITDA sanity check |
| Asset-heavy or distressed | Replacement cost, liquidation value | EV per unit of capacity |

---

## DCF discipline

If you run one, show all of it. A DCF whose assumptions are hidden is worse than no DCF, because it launders a guess into a number.

**Required disclosures:**

1. **Revenue path by year**, with a CAGR, and an explicit statement of how it differs from consensus and why.
2. **EBIT margin path to terminal**, with peer or historical evidence for the terminal level. A margin that expands every year to a level the company has never achieved needs an argument.
3. **Tax rate** (cash, not book, where they diverge), **capex as % of revenue**, and **change in net working capital as % of change in revenue**.
4. **WACC**, fully built:
   - Risk-free rate: the 10-year Treasury, with the date of the quote (see `data-sources.md` for the Treasury CSV).
   - Equity risk premium: state the number and the source. 4.5 to 5.5% is the common institutional range.
   - Beta: source it, and state whether it is raw or adjusted.
   - Cost of debt: the company's actual marginal borrowing rate where disclosed, not the average coupon on legacy debt.
   - Capital structure weights at market value, not book.
5. **Terminal value**: either a growth rate, which must not exceed long-run nominal GDP (roughly 3 to 4%), or an exit multiple with peer justification. Report **the percentage of total value coming from the terminal**. Above 75% and the DCF is a terminal multiple wearing a costume. Say so.
6. **Fully diluted share count including projected SBC dilution** across the forecast period. Using today's share count on year-five cash flows overstates per-share value, often materially.
7. **Sensitivity grid**: fair value across WACC ±1pt on one axis and terminal growth or terminal margin ±1pt on the other. If the grid spans a 2x range, the DCF is not telling you what you hoped.

```
FCFF = EBIT x (1 - tax rate) + D&A - capex - ΔNWC
Enterprise value = Σ FCFF_t / (1+WACC)^t  +  TV / (1+WACC)^n
Equity value = EV - net debt (+ investments, - minority interest, - pension deficit)
Per share = equity value / fully diluted future share count
```

---

## Reverse DCF: what the current price requires

The single highest-value step in the whole skill. Without it you have no way to know whether you disagree with the market, which is the only thing that matters.

**Recipe:**

1. Take the current market cap and add net debt to get enterprise value.
2. Fix everything you can defend independently: WACC, terminal margin, tax rate, capex intensity, terminal growth.
3. Solve for the **revenue CAGR over the forecast period** that makes the DCF output equal today's enterprise value. Do this numerically: guess, compute, adjust. Three iterations usually converge.
4. Alternatively fix growth at consensus and solve for the **terminal FCF margin** the price requires.
5. Now test the implied path for plausibility:
   - How does it compare to consensus?
   - How does it compare to company guidance?
   - How does it compare to what this company has actually delivered over the last five and ten years?
   - **Implied revenue in the terminal year, divided by the size of the addressable market.** Does the price require an implausible market share? This test kills more bad theses than any other.
6. State the disagreement in one sentence:

> "At $223.80, the market is pricing roughly 18% revenue CAGR for five years to a 32% terminal FCF margin. Consensus is 21%. The company delivered 34% over the last five years but decelerating. I think 15% is achievable because [evidence], which puts me below the market."

7. **If your implied path matches the market's, you have no edge.** Say so. "Fairly valued, no view" is a legitimate and frequently correct output, and far more useful than a manufactured opinion.

**Quick version** when a full model is not warranted: what EPS in year N justifies today's price at a normal exit multiple discounted at the cost of equity? Then ask what growth rate gets from today's EPS to that number.

---

## Terminal-year model, for high-growth non-earners

The honest way to value a company that does not yet earn anything.

```
1. Year-5 (or year-7) revenue         <- state the CAGR and defend it
2. Mature FCF margin at scale         <- from mature peers in the same model, not hope
3. Year-N FCF = revenue x margin
4. Exit multiple on FCF or EBITDA     <- what a mature version of this trades at
5. Terminal equity value
6. Discount back at the COST OF EQUITY, not WACC (these companies are equity funded)
   Use 10 to 15% for genuinely risky names. Using 8% here is the most common error.
7. Divide by FULLY DILUTED FUTURE share count, including:
   - SBC dilution at the current run rate compounded over the period
   - any capital raise the cash runway makes necessary, at a plausible price
```

Step 7 is where most of these models fail. A company burning cash with an 18-month runway will raise, and the raise is dilutive at a price you should estimate rather than ignore.

---

## Mid-cycle normalization, for cyclicals

A low P/E on peak earnings is the classic value trap. A high P/E on trough earnings is often the correct entry.

```
1. Pull 7 to 10 years of revenue and EBIT margin. Cover a full cycle.
2. Compute the average margin, excluding obvious one-offs but NOT excluding
   the bad years. The bad years are the point.
3. Mid-cycle EBIT = current revenue x average margin
4. Apply a through-cycle EV/EBIT multiple (the stock's own long-run average, not
   the current one)
5. State where in the cycle you believe we are, and the evidence: inventory levels,
   capacity utilization, pricing direction, order books, the industry orderbook or
   capex plans.
```

Never apply a multiple to peak or trough earnings without saying which you are doing.

---

## Bank valuation

```
Justified P/TBV = (ROTCE - g) / (Ke - g)

ROTCE = normalized return on tangible common equity (normalize the provision)
g     = sustainable growth, roughly ROTCE x (1 - payout ratio)
Ke    = risk-free + beta x ERP
```

Then: fair value = justified P/TBV x tangible book value per share.

Normalize the provision to a through-cycle charge-off rate before computing ROTCE. A bank earning its way through a reserve release is not earning that.

---

## REIT valuation

**NAV:**
```
Forward NOI / market cap rate = gross asset value
Gross asset value + other assets - total debt - preferred = net asset value
NAV per share = NAV / diluted shares
```
The cap rate is the whole answer. Source it from recent comparable transactions in the same property type and market, and state the source.

**P/AFFO:** compare against the peer set, adjusted for balance-sheet quality and growth.

```
FFO  = net income + real estate depreciation - gains on sale
AFFO = FFO - recurring maintenance capex - straight-line rent adjustment
       - amortization of above/below market leases
```
AFFO is the dividend-paying capacity. FFO flatters.

---

## rNPV, for biotech

```
Per program:
  Peak annual sales x probability of success (by current phase)
    x operating margin at maturity
    x years of exclusivity remaining, discounted
  less remaining development cost x probability-weighted

Sum across programs, add net cash, subtract corporate opex NPV.
```

Use published phase-transition probabilities of success. Base rates are in `calibration.md`. Discount rate for clinical-stage assets is typically 10 to 14%, higher for single-asset companies.

---

## Sum of the parts

Value each segment on its own framework. Then:

```
Σ segment enterprise values
  - corporate overhead capitalized (do not bury it in segments)
  - net debt
  - pension deficit, minority interests
  x (1 - holdco discount)
```

State the holdco discount explicitly, typically 10 to 25%, and justify it: conglomerate complexity, tax friction on any separation, capital allocation history, and controlling-shareholder issues.

Check: segment operating income should reconcile to consolidated operating income after corporate costs. If it does not, you have double counted.

---

## Mandatory cross-check: implied multiple

Whatever method produced your number, convert it back:

```
Implied forward P/E   = target price / NTM EPS
Implied EV/EBITDA     = (target market cap + net debt) / NTM EBITDA
Implied EV/Sales      = (target market cap + net debt) / NTM revenue
```

Compare to:
1. The stock's own three-to-five-year multiple range.
2. The current peer set.

If your target implies a multiple outside the historical range, you are making a re-rating call. Justify it explicitly (structurally higher margins, a durable growth inflection, a changed cost of capital) or revise the target. Most implausible price targets are implausible multiples that nobody converted back.

---

## Return decomposition

Every price target must break down into its sources:

```
Expected total return over horizon =
    EPS (or FCF/share) growth
  + multiple change (re-rating or de-rating)
  + dividend yield
  + net buyback yield (net of SBC issuance, not gross repurchases)
```

State each component as a percentage. **If more than half of the expected return comes from multiple expansion, label the call a re-rating bet** and defend why the multiple moves. Most bad price targets are hidden multiple bets that nobody named as such.

---

## ROIC versus WACC

The test of whether growth creates or destroys value, and the most useful single competitive statistic.

```
ROIC = NOPAT / invested capital
NOPAT = EBIT x (1 - cash tax rate)
Invested capital = total debt + equity - cash - non-operating assets
                   (or: net working capital + net PP&E + capitalized intangibles)
```

- ROIC > WACC: growth creates value. Growth is worth paying for, and a high multiple can be rational.
- ROIC < WACC: growth destroys value. Every dollar of growth capex makes the company smaller in value terms. A "cheap" multiple on such a business is usually correct.
- Compute ROIC over five years, not one. A single year is noise.
- For asset-light companies, capitalize R&D and S&M where the spend is genuinely an investment; otherwise ROIC prints implausibly high and tells you nothing.

---

## Anti-anchoring protocol

1. Build the valuation and write down every assumption.
2. Derive your fair value.
3. **Only then** look up the consensus price target and the current price.
4. Compare.
5. If your independently derived value lands within 5% of either the current price or the mean sell-side target, treat that as evidence of anchoring rather than as confirmation. Re-derive from the assumptions, not from the answer.

Price targets in the training distribution cluster 15 to 20% above spot regardless of the company. A model that skips this protocol reproduces that pattern.
