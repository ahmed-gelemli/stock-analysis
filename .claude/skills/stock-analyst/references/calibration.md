# Calibration

Forecasts without calibration are decoration. This file covers band construction, probability discipline, base rates, falsifier construction, and scoring.

**A warning that applies to this whole file.** The base-rate anchors below are approximate, order-of-magnitude figures included so a forecast has something to be anchored against instead of nothing. They are not sourced this session. Treat them as [N/A] under Rule 0: use them to sanity-check your own reasoning, never quote them as retrieved facts in an output. Where a base rate is load-bearing for a call, go retrieve the current figure and cite it.

---

## Band construction

Do not eyeball a range. Run `scripts/vol_bands.py`.

```
1. Volatility input, in order of preference:
   a. IV30 from CBOE (field data.iv30, percent). Forward-looking, the market's own
      forecast, free.
   b. Realized vol: stdev(daily log returns over 21 sessions) x sqrt(252)
   c. Longer-window realized vol if the name is illiquid and 21d is noisy

2. Scale to the horizon:
   sigma_h = sigma_annual x sqrt(trading_days_in_horizon / 252)

   Trading days: 1 week = 5, 1 month = 21, 3 months = 63, 6 months = 126, 1 year = 252

3. Lognormal bands (prices are lognormal, not normal; the asymmetry matters at
   high vol and long horizons):
   ~68% band:  P x exp(-sigma_h)      to  P x exp(+sigma_h)
   ~95% band:  P x exp(-2 x sigma_h)  to  P x exp(+2 x sigma_h)

4. ALWAYS state which band and its coverage. A bare "range" communicates nothing.

5. Shift the CENTER for your view, and state the shift in sigma units:
   "centered 0.4 sigma above spot because [reason]"

6. Do NOT narrow the band because you feel confident. Narrowing requires a
   volatility argument (IV is elevated ahead of an event that will pass without
   resolution, for instance), never a conviction argument.
```

**Worked example** (real CBOE data, NVDA, 2026-08-08 snapshot):

```
spot = 223.80, IV30 = 39.7%
1-month horizon (21 trading days):
  sigma_h = 0.397 x sqrt(21/252) = 0.397 x 0.2887 = 0.1146
  68% band = 223.80 x exp(-0.1146)  to  223.80 x exp(+0.1146)
           = 199.55  to  250.97      (roughly -10.8% / +12.1%)
  95% band = 177.95  to  281.45
```

A stated range of "$215 to $235" against that volatility covers about 0.4 sigma, roughly 31% probability. That is not a forecast, it is a rounding of the current price. This is the most common failure in LLM-generated equity work.

**Sanity check.** If your one-month range is narrower than the options-implied earnings move and earnings fall inside the window, your range is wrong.

```
Implied earnings move ≈ (ATM call price + ATM put price) / spot
  using the first expiry after the earnings date
```

A cleaner version: compare the IV of the expiry straddling earnings against the IV of the expiry before it. The difference is the event premium.

---

## Probability discipline

- **Numeric percentages, not adjectives.** "High confidence" has no operational meaning and is never scored.
- **Scenario probabilities sum to 1.00.** Bull + base + bear = 100%. Check the arithmetic before emitting.
- **Direction is stated as P(up over horizon) = X%**, anchored against the base rate.
- **Confidence must be non-increasing with horizon.** If the twelve-month confidence exceeds the one-month confidence, that is an error, not a view. Uncertainty compounds.
- **Extreme probabilities require mechanical justification.** Anything above 80% or below 20% needs a named, verifiable, mechanical reason: an announced all-cash acquisition at a fixed price with regulatory approval received, an index inclusion with a published effective date, a contractual maturity. Analytical conviction does not earn an 85%.
- **Probability-weighted value** = Σ (probability x scenario price). Report it alongside the base case. When it differs materially from the base case, the distribution is skewed and that skew is the finding.

---

## Base-rate anchors

Approximate. Verify before quoting. Their purpose is to stop a forecast from floating free.

### Single-stock direction
An individual large-cap US equity is up over roughly 53 to 57% of rolling twelve-month windows, and roughly 50 to 52% of one-month windows. The equity risk premium is real but small at these horizons relative to volatility. **A claim of P(up) = 75% over one month is a claim of enormous edge.** Justify it against this anchor or lower it.

Return distributions are fat-tailed and right-skewed at the index level but heavily left-skewed for individual names: the median single stock underperforms the index over long horizons while a small minority drives the aggregate return. A random single stock is more likely than not to underperform the market over ten years, even in a rising market.

### Sell-side price targets
Twelve-month sell-side targets average roughly 15 to 20% above spot more or less regardless of the stock or the eventual outcome, and are close to uninformative directionally. Target **changes** and **estimate revisions** carry more information than target levels. Never treat the consensus target as a valuation.

### Post-earnings announcement drift
Stocks that beat and raise tend to drift in the direction of the surprise for weeks after the print, and stocks that miss tend to drift down. The effect is real, documented across decades, modest in magnitude, and largest in less-covered names. It is one of the few genuine soft edges available without proprietary data.

### Estimate revisions
Direction of consensus EPS revisions over one and three months is among the most durable publicly available signals. Rising revisions into a print beat falling revisions, consistently. Check this every time.

### Clinical trial success
Phase-transition probabilities of success, approximate and highly indication-dependent:
- Phase 1 to Phase 2: roughly 50 to 65%
- Phase 2 to Phase 3: roughly 25 to 40%. **This is where most assets die.**
- Phase 3 to filing: roughly 55 to 70%
- Filing to approval: roughly 85 to 90%
- Overall Phase 1 to approval: roughly 8 to 12%

Oncology runs materially below these; infectious disease and hematology above. For any specific program, retrieve indication-specific rates rather than using the aggregate.

### M&A
Announced all-cash strategic deals close a large majority of the time. Deal breaks cluster around antitrust review, financing conditions in leveraged deals, and material adverse change disputes. The spread between the deal price and the current price is the market's implied break probability, and it is usually better calibrated than a narrative. Compute it:

```
Implied P(close) ≈ (current price - standalone downside price) /
                   (deal price - standalone downside price)
```

### Drawdowns
A stock that has fallen 50% has no mechanical propensity to stop falling. The base rate of a further 50% decline conditional on a 50% decline is meaningfully above the unconditional rate, because the decline usually reflects deteriorating fundamentals rather than a mispricing. "It cannot go much lower" is not an argument.

### Guidance
Most companies guide conservatively enough to beat their own guidance most of the time. A company that beats its guide is meeting a bar it set, not the market's bar. The market's bar is higher, which is why stocks fall on "beats".

---

## Falsifier construction

Required, minimum three per call, all observable. Each names:
1. An observable metric or event
2. A threshold
3. A date by which it becomes observable
4. What you would conclude

```
Bad:  "If the AI narrative weakens."
      Unobservable, no threshold, no date, no conclusion. Unfalsifiable.

Bad:  "If growth slows meaningfully."
      "Meaningfully" is doing all the work and means nothing.

Good: "If Q3 data-center revenue prints below $28bn against $30bn guided, on the
       Nov 19 call, the capacity-constraint story is actually a demand story and
       the base case is wrong. Target cuts to $170."

Good: "If the stock closes below $195 for two consecutive weeks on above-average
       volume, the accumulation read is wrong and I would flatten the view."

Good: "If borrow fee rises above 8% annualized or short interest exceeds 15% of
       float (FINRA bimonthly), positioning risk dominates the fundamental view
       for this horizon."

Good: "If gross margin does not recover to 46%+ by the Q4 print (guide implies
       47%), the input-cost explanation was wrong and the real cause is
       discounting, which is structural rather than cyclical."
```

**Review triggers**, listed separately from falsifiers:
- Scheduled: earnings date (verified), investor day, regulatory or court dates, index rebalance, lockup expiry, debt maturity.
- Unscheduled: any 8-K, a guidance revision, a greater-than-2-sigma one-day move, a sector-wide shock, a short-seller report, a CFO departure.

---

## Horizon consistency check

Run before emitting:

1. Does the six-month range contain the one-month band's center path extended?
2. Is the long-term fair value reachable from the medium-term target under a stated growth path? If the twelve-month target is $200 and the fair value is $400, what happens in months 13 through 24 to double it? Name it or fix one of the numbers.
3. Is confidence non-increasing with horizon?
4. Do the scenario prices differ enough to be distinct scenarios? Bear $190 / base $200 / bull $215 on a 40-vol stock is one scenario written three times.
5. Is the bull-bear spread at least as wide as the 1-sigma band for the horizon? If not, the scenarios are not covering the actual distribution.

---

## Asymmetry test

```
Asymmetry = (base target - current price) / (current price - bear case)
```

Report the ratio. Below roughly 2:1, say plainly that the risk/reward does not support action at this price, and name the price at which it would. This is the single most useful line in a research note and it is almost always omitted.

---

## Scoring, for the calls log

If `calls-log.md` is being maintained, these are the scoring rules that make the calibration language enforceable rather than rhetorical.

**Brier score for direction:**
```
Brier = (1/N) x Σ (forecast_probability - outcome)^2
  where outcome = 1 if the event occurred, 0 if not

0.00 = perfect. 0.25 = the score of always saying 50%. Above 0.25 = worse than
a coin flip, which means the forecasts carry negative information.
```

**Range coverage:**
```
Over many calls, a stated 68% band should contain the realized price about 68%
of the time.
  Coverage well below 68%: bands too narrow (the usual failure, by a wide margin)
  Coverage well above 68%: bands too wide, forecasts are uninformative
```

**Log entry format:**
```
date | ticker | mode | horizon | P(up) | band_low | band_high | base_target |
thesis_one_line | falsifiers | resolution_date | outcome | realized_price
```

Score at least twenty calls before drawing any conclusion. Below that, the sample says nothing.
