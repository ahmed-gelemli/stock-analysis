# Sector Frameworks

Classify the company, then load its module before valuing anything. Generic P/E applied across sectors ranges from misleading to meaningless.

Each module gives: the KPI tree, the correct valuation metric and why the generic one fails, sector-specific red flags, and cycle indicators.

---

## Banks and lenders

**KPIs.** Net interest margin (NIM) and net interest income (NII). NII sensitivity to a 100bp parallel shift, disclosed in the 10-K. Deposit beta (how much of a rate move passes through to depositors) and deposit mix (non-interest-bearing is the prize). Loan growth by category. Net charge-offs, non-performing loans, allowance for credit losses and reserve coverage ratio. Provision expense, and whether the quarter had a reserve build or release. Efficiency ratio (opex / revenue). CET1 ratio versus the regulatory minimum plus buffer. ROTCE. Tangible book value per share. Held-to-maturity securities and their unrealized losses, which do not hit reported equity but are real.

**Valuation.** P/TBV justified by returns: `P/TBV = (ROTCE - g) / (Ke - g)`. Cross-check with P/E on normalized provisions. **P/E alone fails** because reported earnings swing with provisioning, which is a management estimate, and because leverage is the business rather than a financing choice.

**Red flags.** Rapid loan growth in one category. Reserve releases propping up EPS. Rising NPLs with flat provisions. Deposit outflows. Large HTM unrealized losses relative to equity. Heavy commercial real estate concentration, especially office. Reliance on brokered deposits or FHLB advances.

**Cycle.** Credit cycle position, the yield curve shape, unemployment as the leading driver of consumer credit losses.

---

## Insurers

**KPIs.** Combined ratio (under 100 means underwriting profit), split into loss ratio and expense ratio. Prior-year reserve development, favorable or adverse. Net premiums written growth and rate versus exposure. Float size and investment yield on it. Book value per share growth, which is the real scoreboard. Catastrophe losses versus the catastrophe load. Retention rates.

**Valuation.** P/BV against ROE. Life insurers on embedded value. **P/E fails** because reserve development and catastrophe timing make single-year earnings close to arbitrary.

**Red flags.** Persistent adverse development (reserves were too low, and probably still are). Growth well above market rate increases, which usually means buying business. Reaching for yield in the investment portfolio.

**Cycle.** Hard versus soft pricing market, and the reinsurance capacity cycle.

---

## REITs

**KPIs.** FFO and AFFO per share, not EPS. Same-store NOI growth. Occupancy and leasing spreads on renewal. Weighted average lease term (WALT). Tenant credit and concentration. Debt maturity ladder, weighted average interest rate, fixed versus floating mix. Net debt / EBITDA. Development pipeline and yield on cost versus market cap rates. Dividend coverage as AFFO payout ratio.

**Valuation.** NAV: forward NOI capitalized at a market cap rate, less net debt. And P/AFFO against peers. **EPS and P/E are meaningless** because depreciation on appreciating real estate dominates GAAP earnings.

**Red flags.** AFFO payout above 100%. Cap rate expansion in the property type. A maturity wall against a much higher current refinancing rate. Straight-line rent inflating reported revenue. Recurring capex understated in AFFO.

**Cycle.** Cap rates versus the 10-year Treasury, new supply in the submarket, and the direction of replacement cost.

---

## Biotech and pharma

**KPIs.** Pipeline by phase with indication and addressable population. Catalyst calendar: PDUFA dates, readouts, advisory committee meetings. Probability of success by phase (historical base rates in `calibration.md`). Cash runway in months at the current burn. Patent cliffs and loss-of-exclusivity dates by product. For commercial products: scripts, net versus gross pricing, payer coverage, and competitive launches.

**Valuation.** Risk-adjusted NPV by program: peak sales x probability of success x margin, discounted, then summed and adjusted for net cash. For commercial-stage pharma, sum of the parts by product with an LOE-adjusted terminal. **P/E fails** for pre-revenue names entirely and understates cliff risk for commercial ones.

**Red flags.** Single-asset dependency. Cash runway under twelve months, which makes dilution near certain. Endpoint changes mid-trial. Reliance on open-label or single-arm data. Partner walking away. Repeated "encouraging" interim data with no primary endpoint.

**Cycle.** Biotech funding environment, XBI relative strength, FDA posture, and drug-pricing policy risk.

---

## Exploration and production, and miners

**KPIs.** Proved reserves and reserve life. Production volume and its decline rate. All-in sustaining cost (AISC) per unit, and where the company sits on the industry cost curve. Realized price versus the benchmark, including differentials. Hedge book: how much is hedged, at what price, out to when. Capex versus maintenance capex. Netback margin. Free cash flow breakeven price per barrel or ounce.

**Valuation.** NAV on a stated commodity deck (state the deck, it is the whole answer). EV/EBITDAX. EV per flowing barrel or per resource unit. **P/E fails** because earnings are a leveraged derivative of a commodity price nobody can forecast.

**Red flags.** Reserve write-downs. Rising AISC. Aggressive hedging at low prices locking in weak economics. Debt against reserves at a peak commodity price. Decline rates accelerating.

**Cycle.** Inventory levels, rig counts, spare capacity, and the futures curve shape (contango versus backwardation).

---

## Semiconductors

**KPIs.** Cycle position first, everything else second. Book-to-bill. Channel inventory in weeks, and inventory days on the balance sheet. Fab utilization. Capex intensity across the industry, since today's capex is next year's oversupply. Design win pipeline. Customer concentration, which is usually severe. Node transitions and the cost curve. For equipment names: WFE spend forecasts. For fabless: foundry pricing and allocation.

**Valuation.** Mid-cycle EPS x through-cycle multiple. EV/Sales against the historical range for a name whose margins swing hard. **A trailing P/E is actively misleading**: it is lowest at the top of the cycle and highest at the bottom.

**Red flags.** Inventory growing much faster than revenue. Distributor stuffing. A single customer above 20% of revenue. Guidance dependent on one product ramp. Capex announced by everyone at once.

**Cycle.** Semis lead the broad cycle. Watch lead times, spot pricing on commodity memory, and the gap between sell-in and sell-through.

---

## Software and SaaS

**KPIs.** Net revenue retention (NRR) and gross retention, separately. Annual recurring revenue growth and the split of new versus expansion. Remaining performance obligation (RPO) and current RPO, plus billings. CAC payback in months. Magic number (incremental ARR / prior-quarter S&M). Rule of 40 (growth % + FCF margin %). Gross margin, which should sit in the 70s or 80s for real software. SBC as % of revenue, which is frequently enormous and habitually excluded from "adjusted" numbers. Seat-based versus usage-based exposure, since usage models re-rate hard when customers optimize.

**Valuation.** EV/NTM revenue against the growth-adjusted peer set, plus EV/gross profit which normalizes for genuinely different cost structures. A terminal-year FCF model for anything with a credible path to profit. **P/E fails** while the company is unprofitable, and adjusted EPS that excludes SBC overstates economics for a company paying a fifth of revenue in stock.

**Red flags.** NRR falling below 100%. Billings decelerating faster than revenue (revenue is a lagging indicator here). Growth bought with S&M at rising CAC. Free-cash-flow "profitability" driven purely by SBC add-backs. Share count growing 4%+ a year. Reclassifying professional services into product revenue.

**Cycle.** IT budget growth, seat counts as a proxy for customer headcount, and the AI-substitution question for seat-based models.

---

## Internet and marketplaces

**KPIs.** GMV or gross bookings, take rate, and the trend in take rate. Monthly or daily actives and their growth. ARPU by geography. Cohort retention curves. Contribution margin per transaction after incentives. Customer acquisition cost and the mix of paid versus organic. Two-sided liquidity, meaning supply and demand growth together.

**Valuation.** EV/EBITDA once mature, EV/gross profit while scaling, and a cohort-based DCF where the data supports one. Sum of the parts when a profitable core is funding a loss-making segment.

**Red flags.** GMV growing while take rate falls (buying volume). Incentives and promotions growing faster than revenue. Actives growing while ARPU falls. Disclosure changes to metric definitions, which almost always precede deterioration.

---

## Retail and consumer

**KPIs.** Same-store or comparable sales, decomposed into traffic versus average ticket. Inventory-to-sales ratio and its direction. Gross margin versus promotional intensity. Store count, new-store productivity, and four-wall economics. E-commerce penetration and its margin drag. Private label mix. For staples: volume versus price mix, which separates real demand from inflation pass-through.

**Valuation.** EV/EBITDA and P/E on normalized margins, adjusted for lease-adjusted leverage. **Watch operating leases**, which are debt in substance.

**Red flags.** Inventory growing much faster than sales, which is a markdown cycle in the making. Comps driven entirely by price during inflation. Deferred maintenance capex. Gift card and loyalty liability changes flattering revenue.

**Cycle.** Real disposable income, consumer credit delinquencies, savings rate, and the goods-versus-services spending mix.

---

## Industrials and autos

**KPIs.** Backlog and book-to-bill. Incremental and decremental margins (ΔEBIT / ΔRevenue, both directions). Capacity utilization. Aftermarket versus original-equipment mix, since aftermarket is higher-margin and less cyclical. Input costs (steel, resin, energy) and the lag on pricing pass-through. For autos: units, ASP, mix, incentives per unit, dealer inventory days, and the financing arm treated as a separate business.

**Valuation.** Mid-cycle EBIT x through-cycle EV/EBIT. Sum of the parts where a captive finance arm exists, because consolidating a lender into an industrial distorts every ratio.

**Red flags.** Backlog quality deteriorating (cancellable orders). Margins held up by price with volumes falling. Dealer inventory building. Warranty reserves rising.

**Cycle.** PMI, capex intentions, and the fact that these are late-cycle businesses.

---

## Airlines

**KPIs.** RASM (revenue per available seat mile) and CASM ex-fuel. Load factor. Available seat miles growth versus industry capacity growth. Fuel cost per gallon and the hedge book. Fleet age and the capex commitment schedule. Corporate versus leisure mix. Loyalty program economics, which for the US majors are often worth more than the airline.

**Valuation.** EV/EBITDAR (rent-adjusted). Sum of the parts separating the loyalty program. **P/E fails** because of extreme operating leverage and fuel.

**Red flags.** Industry capacity growth outpacing demand. Unhedged fuel exposure into a rising oil market. Aging fleet with a deferred replacement cycle. Labor contract renegotiation.

---

## Telecom and utilities

**Telecom KPIs.** Subscriber net adds by segment, ARPU, churn, capex intensity (chronically high), spectrum holdings, and fiber or 5G build progress against the promised footprint. Leverage, which is structurally high.

**Utility KPIs.** Rate base and its growth rate, allowed ROE versus earned ROE, regulatory lag, pending rate cases and the jurisdiction's regulatory posture, capex plan and how it is financed, and the fuel mix with its transition capex.

**Valuation.** Utilities on P/E against the rate-base growth rate and against the sector, with an explicit bond-proxy sensitivity to the 10-year. Telecom on EV/EBITDA and FCF yield.

**Red flags.** Utilities: an adverse regulatory ruling, a dividend not covered by FCF after capex, wildfire or storm liability. Telecom: promotional subscriber adds, capex holidays that borrow from future competitiveness.

---

## Shipping and transport

**KPIs.** Day rates or freight rates versus operating breakeven. Fleet size, age, and the orderbook as % of the existing fleet, which is the single best supply indicator. Charter coverage and duration. Utilization. Scrapping rates.

**Valuation.** NAV on vessel values. EV/EBITDA on mid-cycle rates. **Never capitalize peak rates.**

**Red flags.** Orderbook above roughly 20% of the fleet. Equity raised at the top of the cycle. Rates below cash breakeven for an extended period.

---

## Asset managers and exchanges

**KPIs.** AUM by asset class, and flows separated from market appreciation, since only flows are a business result. Fee rate and its mix shift, usually downward. Operating margin. Performance fee dependence. For exchanges: volumes, capture rate per contract, and the data-and-analytics revenue mix, which is the higher-quality part.

**Valuation.** P/E adjusted for the quality of the earnings stream. EV/AUM as a cross-check.

**Red flags.** Persistent net outflows masked by market appreciation. Fee compression accelerating. Concentration in one strategy or one distribution channel.

---

## When the company spans sectors

Use sum of the parts. Value each segment on its own framework, apply an explicit holding-company discount (typically 10 to 25%, and say why), and check that segment operating income sums to the consolidated figure after corporate costs. State corporate overhead separately rather than burying it.
