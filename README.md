<div align="center">

# 📈 Stock Analysis Archive

**Dated single-stock research — and the [Claude Code skill](.claude/skills/stock-analyst/SKILL.md) that writes it.**

[![Stars](https://img.shields.io/github/stars/ahmed-gelemli/stock-analysis?style=for-the-badge&label=stars&color=e3b341)](https://github.com/ahmed-gelemli/stock-analysis/stargazers)
[![Reports](https://img.shields.io/badge/reports-5-2f6feb?style=for-the-badge)](index.md)
[![Skill](https://img.shields.io/badge/skill-stock--analyst-8250df?style=for-the-badge)](.claude/skills/stock-analyst/SKILL.md)
[![Not advice](https://img.shields.io/badge/not%20investment%20advice-d1242f?style=for-the-badge)](#-not-investment-advice)

**[⚡ The skill →](.claude/skills/stock-analyst/SKILL.md)** · **[📊 The index →](index.md)**

</div>

---

## ⚡ The skill

Reports here are output, not hand-written. The engine is a
[Claude Code skill](.claude/skills/stock-analyst/) — ~2,000 lines built to defeat the
specific ways LLM stock analysis goes wrong. **It's the reusable half of this repo.**

- **Rule 0 — no remembered numbers.** Every figure is sourced this session (unit, timestamp, URL), computed from sourced inputs, or explicitly *not retrieved*. 3+ gaps ⇒ price targets are forbidden and it emits a `DEGRADED` report.
- **No unsourced causation.** Links tagged `[DISCLOSED]` / `[REPORTED]` / `[INFERRED]` / `[UNKNOWN]`, never more inferred than sourced. "No identified catalyst" is a valid answer.
- **Move attribution first.** `return − β×index − sector` — if the residual is under ~1σ, it's sector beta, and attaching a company story is barred.
- **Reverse DCF before a view.** Solves for what the *current price* requires, so the output is a disagreement with a specific assumption. "Fairly valued, no view" is allowed.
- **Ranges from IV, not judgment.** `σ_h = IV × √(days/252)`. Conviction may shift the band's center in stated σ units — never narrow it.
- **Mandatory bear search**, steelmanned. Probabilities sum to 1.00 against base rates. Sector-correct valuation (P/TBV for banks, rNPV for biotech, normalized earnings for cyclicals). Escalation protocols for microcaps, meme dynamics, and vulnerable-user signals.

```bash
git clone https://github.com/ahmed-gelemli/stock-analysis.git
cp -r stock-analysis/.claude/skills/stock-analyst ~/.claude/skills/
# then: "analyze HROW" · "what's up with NVDA" · "why is PGY down"
```

Needs `bash`, `curl`, `jq`, Python 3, and `SEC_CONTACT="you@example.com"` for EDGAR. All
sources are free and public.

<div align="center">

⭐ **[Star the repo](https://github.com/ahmed-gelemli/stock-analysis)** if it saved you an afternoon. Issues and PRs welcome.

</div>

---

## 🗂 Latest reports

| Date | Ticker | Company | Mode | Price | Bear / Base / Bull | |
|:---|:---|:---|:---:|---:|:---|:---:|
| 2026-08-09 | **HROW** | Harrow, Inc. | `STANDARD` | $40.44 | $28 / $49 / $71 | [→](HROW/2026-08-09.md) |
| 2026-08-09 | **TMDX** | TransMedics Group, Inc. | `STANDARD` | $83.89 | $52 / $80 / $120 | [→](TMDX/2026-08-09.md) |
| 2026-08-09 | **PGY** | Pagaya Technologies Ltd. | `STANDARD` | $21.28 | $15 / $29 / $42 | [→](PGY/2026-08-09.md) |
| 2026-08-09 | **AAOI** | Applied Optoelectronics, Inc. | `STANDARD` | $135.63 | $45 / $115 / $290 | [→](AAOI/2026-08-09.md) |
| 2026-08-09 | **DLO** | DLocal Limited | `STANDARD` | $14.41 | $9.21 / $17.38 / $29.51 | [→](DLO/2026-08-09.md) |

<sub>Probabilities and catalysts: **[index.md](index.md)**. One folder per ticker, one file per date — reports are never overwritten, only added to. Every report carries YAML frontmatter so the set is queryable without opening files.</sub>

---

## 🧭 Reading a report

**Mode** (`QUICK`/`STANDARD`/`DEEP`) sets the rigor the numbers were held to. **DATA AS-OF**
opens every report with its input vintage and an explicit *NOT RETRIEVED* list. **Scenarios**
are bear/base/bull with probabilities — the spread is the point. A report whose catalyst has
since passed is **expired**, not merely old.

---

## ⚠️ Not investment advice

> Research only. Not personalized, no fiduciary relationship, no position sizes or buy/sell
> instructions — and not meant to be aggregated into a signal list. Data is as-of the date on
> each report. Verify independently before acting.
