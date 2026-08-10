<div align="center">

# 📈 Stock Analysis Archive

**A dated log of research-grade single-stock analyses — and the [Claude Code skill](#-the-engine-the-stock-analyst-skill) that writes them.**

Each report is a snapshot: what the market appeared to be pricing on a given day,
where the analysis differed, and what would have proven it wrong.

<br>

[![Stars](https://img.shields.io/github/stars/ahmed-gelemli/stock-analysis?style=for-the-badge&label=stars&color=e3b341)](https://github.com/ahmed-gelemli/stock-analysis/stargazers)
[![Reports](https://img.shields.io/badge/reports-5-2f6feb?style=for-the-badge)](index.md)
[![Tickers](https://img.shields.io/badge/tickers-5-1f883d?style=for-the-badge)](index.md)
[![Skill](https://img.shields.io/badge/skill-stock--analyst-8250df?style=for-the-badge)](.claude/skills/stock-analyst/SKILL.md)
[![Not advice](https://img.shields.io/badge/not%20investment%20advice-d1242f?style=for-the-badge)](#-not-investment-advice)

### **[⚡ Read the skill →](.claude/skills/stock-analyst/SKILL.md)**  ·  **[📊 Browse the index →](index.md)**

<br>

⭐ **If the skill is useful to you, star the repo** — it's the only signal I get that
this is worth maintaining in public.

</div>

---

## ⚡ The engine: the `stock-analyst` skill

The reports here aren't hand-written. They're the output of a
[Claude Code skill](https://docs.claude.com/en/docs/claude-code/skills) checked into this
repo at **[`.claude/skills/stock-analyst/`](.claude/skills/stock-analyst/)** — roughly 2,000
lines of analytical protocol built to defeat the specific ways LLM stock analysis goes
wrong. It's the more interesting half of this repository, and it's yours to take.

**The two rules everything else serves:**

> **Rule 0 — Numbers discipline.** Every figure is `[S]` sourced this session (with unit,
> currency, timestamp, and URL), `[C]` computed from sourced inputs (with the formula), or
> `[N/A]` not retrieved. A number recalled from training data is a bug, not an
> approximation. If 3+ required fields are missing, the skill is forbidden from producing
> price targets and emits a `DEGRADED` report instead.
>
> **No unsourced causation.** Every causal link is tagged `[DISCLOSED]`, `[REPORTED]`,
> `[ATTRIBUTED]`, `[INFERRED]`, or `[UNKNOWN]` — and a chain may never contain more
> inferred links than sourced ones. "No identified catalyst" is a valid, encouraged output.

### What it actually does differently

| | |
|:---|:---|
| 🧮 **Attributes the move before explaining it** | `stock return − β×index − β-adjusted sector = residual`. If the residual is under ~1σ, the correct answer is "this was sector beta" — and the skill is barred from attaching a company narrative to it. |
| 🎯 **Reverse DCF before forming a view** | Solves for the growth and terminal margin the *current price* requires, so the output is a disagreement with a specific market-implied assumption rather than a free-floating target. "Fairly valued, no view" is a legitimate result. |
| 📏 **Volatility-anchored ranges** | Bands come from CBOE IV30 (or realized vol), not judgment: `σ_h = IV × √(days/252)`, lognormal. Conviction may shift the band's *center*, in stated σ units — it may never narrow it. |
| 🕵️ **Mandatory disconfirming search** | Runs bear-case, short-report, restatement, litigation, and downgrade queries *every time*, then steelmans the most credible bear source in full. Default queries skew bullish; SEO does the rest. |
| 🎲 **Calibrated probabilities, not adjectives** | Scenarios sum to 1.00, anchored to base rates (a large-cap is up in ~53–57% of 12-month windows). >80% confidence requires a *mechanical* reason — an all-cash deal, a dated index inclusion — not conviction. Confidence must be non-increasing with horizon. |
| 🧱 **Sector-correct valuation** | A P/E on a bank, a REIT, an E&P, or a pre-profit software company ranges from misleading to meaningless. Banks get P/TBV justified by ROTCE; REITs get NAV and P/AFFO; biotech gets rNPV by program; cyclicals get normalized through-cycle earnings. |
| 🛑 **Escalation classes** | Microcaps, pump-and-dump signatures, meme dynamics, leveraged ETFs, and MNPI each get a defined protocol. Vulnerable-user signals ("life savings", "margin call") **override everything else** and stop directional output entirely. |
| 🔴 **Red team before emit** | An 8-question adversarial pass, including: *would this output read identically with a different ticker swapped in?* If yes, it's generic and has no content. |

### Inside the skill

```
.claude/skills/stock-analyst/
├── SKILL.md                        ← 11 phases, pre-flight → red team, + completion gate
├── references/                     ← loaded on demand, not inlined every run
│   ├── data-sources.md             · working endpoints, tiered source ladder, conflict rules
│   ├── sector-frameworks.md        · the module that makes the multiple mean something
│   ├── valuation-methods.md        · DCF, reverse DCF, rNPV, SOTP, P/TBV templates
│   ├── earnings-quality.md         · accruals, non-GAAP bridges, auditor & restatement flags
│   ├── calibration.md              · base rates and band math
│   ├── compliance.md               · escalation wording
│   └── output-templates.md         · QUICK / STANDARD / DEEP / DEGRADED
└── scripts/                        ← run, never reimplement
    ├── fetch_snapshot.sh           · provenance-stamped quote + IV30 + SEC XBRL; fails loudly
    ├── vol_bands.py                · IV/realized-vol forecast bands
    └── attribution.py              · market / sector / idiosyncratic decomposition
```

Three modes set the rigor: **QUICK** (≤6 tool calls, ≤300 words, *no price targets*),
**STANDARD** (~20 calls, full phase set), **DEEP** (8-quarter history, segment detail, comps
table, sensitivity grid, named bull/bear steelman).

### Use it yourself

```bash
git clone https://github.com/ahmed-gelemli/stock-analysis.git

# use it globally, in any project
cp -r stock-analysis/.claude/skills/stock-analyst ~/.claude/skills/

# then just ask Claude Code — the skill triggers on natural phrasing:
#   "analyze HROW"  ·  "what's up with NVDA"  ·  "thoughts on TMDX"  ·  "why is PGY down"
```

Scripts need `bash`, `curl`, `jq`, and Python 3. `fetch_snapshot.sh` hits SEC EDGAR, which
requires a contact in the User-Agent — set `SEC_CONTACT="you@example.com"` or you may get
throttled. Everything it queries is free and public: SEC XBRL, CBOE delayed chains, FINRA
short interest.

<div align="center">
<br>

**⭐ [Star this repo](https://github.com/ahmed-gelemli/stock-analysis) if the skill saved you an afternoon.**

<sub>Issues and PRs welcome — especially additional sector modules and sharper base rates.</sub>

</div>

---

## 🗂 Latest reports

| Date | Ticker | Company | Mode | Price @ analysis | Bear / Base / Bull | Report |
|:---|:---|:---|:---:|---:|:---|:---:|
| 2026-08-09 | **HROW** | Harrow, Inc. | `STANDARD` | $40.44 | $28 / $49 / $71 | [→](HROW/2026-08-09.md) |
| 2026-08-09 | **TMDX** | TransMedics Group, Inc. | `STANDARD` | $83.89 | $52 / $80 / $120 | [→](TMDX/2026-08-09.md) |
| 2026-08-09 | **PGY** | Pagaya Technologies Ltd. | `STANDARD` | $21.28 | $15 / $29 / $42 | [→](PGY/2026-08-09.md) |
| 2026-08-09 | **AAOI** | Applied Optoelectronics, Inc. | `STANDARD` | $135.63 | $45 / $115 / $290 | [→](AAOI/2026-08-09.md) |
| 2026-08-09 | **DLO** | DLocal Limited | `STANDARD` | $14.41 | $9.21 / $17.38 / $29.51 | [→](DLO/2026-08-09.md) |

<sub>Probabilities, probability-weighted values and next catalysts live in **[index.md](index.md)**.</sub>

---

## 📁 What's here

```
stock-analysis/
├── .claude/skills/stock-analyst/   ← the skill that produces every report
├── index.md                        ← one row per report, newest first
├── _template.md                    ← the fixed report skeleton
└── <TICKER>/
    └── <YYYY-MM-DD>.md
```

Each ticker has its own folder, with one file per report dated to the day it was produced
(`HROW/2026-08-09.md`). Reports are **never overwritten** — revisiting a thesis adds a new
dated file alongside the old one, so the archive preserves what was believed and when.

Every report carries YAML frontmatter (ticker, mode, scenario probabilities and prices,
probability-weighted value, next catalyst), so the set can be scanned or queried without
opening each file. `index.md` is the human-readable version of the same thing.

---

## 🧭 How to read a report

| | |
|:---|:---|
| 🎚 **Mode** | `QUICK`, `STANDARD`, or `DEEP` — the depth and rigor the numbers were held to. A QUICK read is not a DEEP one with fewer words. |
| 📅 **DATA AS-OF** | Every report opens with the vintage of its inputs and an explicit **NOT RETRIEVED** list. Figures are sourced or computed, never recalled from memory; anything unavailable is named rather than filled in. |
| 🎲 **Scenarios** | Bear / base / bull with explicit probabilities, not a single target. The spread is the point. |
| ⏳ **Staleness** | A report whose earnings date or catalyst has since passed should be treated as **expired**, not merely old. The scenario numbers were conditioned on that event being in the future. |

---

## ⚠️ Not investment advice

> Research and analysis only. Not personalized to anyone's circumstances, no fiduciary
> relationship, no position sizes, allocations, or buy/sell instructions — and these are
> **not** meant to be aggregated into a signal list.
>
> Data is as-of the date on each report. Verify independently before acting on anything here.

<div align="center">
<sub>Every report ends with the same disclosure. It means it.</sub>
</div>
