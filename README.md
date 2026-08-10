<div align="center">

# 📈 Stock Analysis Archive

**A dated log of research-grade single-stock analyses.**

Each report is a snapshot: what the market appeared to be pricing on a given day,
where the analysis differed, and what would have proven it wrong.

<br>

[![Reports](https://img.shields.io/badge/reports-5-2f6feb?style=for-the-badge)](index.md)
[![Tickers](https://img.shields.io/badge/tickers-5-1f883d?style=for-the-badge)](index.md)
[![Last updated](https://img.shields.io/badge/updated-2026--08--09-8250df?style=for-the-badge)](index.md)
[![Not advice](https://img.shields.io/badge/not%20investment%20advice-d1242f?style=for-the-badge)](#-not-investment-advice)

### **[📊 Browse the full index →](index.md)**

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
├── index.md          ← one row per report, newest first
├── _template.md      ← the fixed report skeleton
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

## 🛠 The engine behind the reports

Nothing here is written off the cuff. Every report is produced by **`stock-analyst`** — a
research routine that lives right in this repo, at [`.claude/skills/stock-analyst/`](.claude/skills/stock-analyst/),
so anyone can read exactly how the work gets done.

It is built around one stubborn rule: **it is not allowed to make anything up.**

| | |
|:---|:---|
| 🔍 **Looks everything up, every time** | Prices, filings and analyst consensus are pulled fresh while the report is being written. No figure comes from memory. If something can't be retrieved, it gets named on the **NOT RETRIEVED** list instead of quietly filled in. |
| 📄 **Reads the filings, not the headlines** | It goes to the company's own financial statements and checks whether the profits are real cash, whether the growth is paid for, and whether the story management tells matches the numbers underneath it. |
| 🎯 **Asks what's already priced in** | The interesting question isn't "is this a good company" — it's what the current price already assumes, and where the evidence disagrees with it. |
| 🎲 **Gives a range, not a number** | Three futures — bear, base, bull — each with a probability attached. Anyone who hands you a single price target is hiding the uncertainty, not removing it. |
| 🚩 **Writes down what would prove it wrong** | Every report names, in advance, the specific things that would break its own case. You can check it later and see whether it held up. |
| 🛑 **Refuses to play along** | Penny stocks, pump-and-dumps, meme squeezes: it names the pattern, explains how people lose money in it, and declines to produce a price target rather than dress up a gamble as research. |

The same standard applies whether the conclusion turns out exciting or dull — and the boring
answer gets published just as readily as the dramatic one.

It doesn't predict the future. It just refuses to pretend.

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
