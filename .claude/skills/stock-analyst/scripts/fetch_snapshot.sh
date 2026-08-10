#!/usr/bin/env bash
# Provenance-stamped snapshot for a US-listed equity.
#
# Design principle: FAIL LOUDLY. Every field that could not be retrieved is
# emitted explicitly as "NOT_RETRIEVED" rather than omitted, because a partial
# object that reads as complete is exactly the surface where remembered numbers
# get substituted for retrieved ones.
#
# Usage:  ./fetch_snapshot.sh NVDA [contact-email]
#
# SEC requires a descriptive User-Agent with a contact. Pass one, or set
# SEC_CONTACT in the environment. The default is a placeholder and SEC may
# throttle it.

set -uo pipefail

TICKER="${1:-}"
if [[ -z "$TICKER" ]]; then
  echo "usage: $0 TICKER [contact-email]" >&2
  exit 2
fi
TICKER="$(echo "$TICKER" | tr '[:lower:]' '[:upper:]')"

CONTACT="${2:-${SEC_CONTACT:-stock-analyst-skill contact@example.com}}"
UA_SEC="stock-analyst-skill $CONTACT"
UA_WEB="Mozilla/5.0"

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

note() { echo "  $*"; }
fail() { echo "  NOT_RETRIEVED: $*"; }

echo "SNAPSHOT: $TICKER"
echo "Generated: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
echo "Contact UA for SEC: $CONTACT"
echo

# ---------------------------------------------------------------- quote + IV
echo "[1] QUOTE AND IMPLIED VOLATILITY (CBOE delayed)"
CBOE_CODE=$(curl -s -o "$TMP/cboe.json" -w '%{http_code}' --max-time 45 \
  "https://cdn.cboe.com/api/global/delayed_quotes/options/${TICKER}.json")

if [[ "$CBOE_CODE" == "200" ]]; then
  python3 - "$TMP/cboe.json" <<'PY'
import json, sys
p = json.load(open(sys.argv[1]))
d = p.get("data") or {}
print("  data_timestamp:   %s   <- THIS IS THE AS-OF. It can lag by a day or more." % p.get("timestamp"))
for label, key in [("last_trade", "current_price"), ("prior_close", "close"),
                   ("prev_day_close", "prev_day_close"), ("open", "open"),
                   ("high", "high"), ("low", "low"), ("volume", "volume"),
                   ("iv30_pct", "iv30")]:
    v = d.get(key)
    print("  %-17s %s" % (label + ":", v if v is not None else "NOT_RETRIEVED"))
opts = d.get("options") or []
print("  option_rows:      %d" % len(opts))
lt, cl = d.get("current_price"), d.get("close")
if lt is not None and cl is not None and abs(lt - cl) > 1e-9:
    print("  WARNING: last trade %.2f differs from close %.2f. State which you quote." % (lt, cl))
PY
else
  fail "CBOE returned HTTP $CBOE_CODE. A 403 usually means no listed options."
  note "No IV30. Fall back to realized vol via scripts/vol_bands.py --prices."
fi
echo

# --------------------------------------------------------------- CIK lookup
echo "[2] SEC IDENTITY"
CIK=""
if curl -s --max-time 45 -H "User-Agent: $UA_SEC" \
     "https://www.sec.gov/files/company_tickers.json" -o "$TMP/tickers.json"; then
  CIK=$(python3 - "$TMP/tickers.json" "$TICKER" <<'PY'
import json, sys
try:
    rows = json.load(open(sys.argv[1]))
except Exception:
    sys.exit(0)
want = sys.argv[2]
for r in rows.values():
    if r.get("ticker", "").upper() == want:
        print("%010d" % int(r["cik_str"]))
        break
PY
)
fi

if [[ -z "$CIK" ]]; then
  fail "CIK for $TICKER. Non-US listing, ADR under a different filer, or ticker changed."
  note "Everything below depends on the CIK. Stopping SEC section."
  echo
else
  note "cik: $CIK"
  if curl -s --max-time 45 -H "User-Agent: $UA_SEC" \
       "https://data.sec.gov/submissions/CIK${CIK}.json" -o "$TMP/sub.json"; then
    python3 - "$TMP/sub.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
fye = d.get("fiscalYearEnd") or "NOT_RETRIEVED"
print("  name:             %s" % d.get("name", "NOT_RETRIEVED"))
print("  exchanges:        %s" % ", ".join(d.get("exchanges") or []) or "NOT_RETRIEVED")
print("  sic:              %s" % d.get("sicDescription", "NOT_RETRIEVED"))
if fye != "NOT_RETRIEVED" and len(fye) == 4:
    print("  fiscal_year_end:  %s-%s   <- CHECK THIS. Off-calendar FY breaks YoY comparisons." % (fye[:2], fye[2:]))
else:
    print("  fiscal_year_end:  %s" % fye)
r = (d.get("filings") or {}).get("recent") or {}
forms, dates, accs, docs = (r.get("form") or [], r.get("filingDate") or [],
                            r.get("accessionNumber") or [], r.get("primaryDocument") or [])
cik = str(int(d.get("cik", 0)))
print("  recent filings:")
shown = 0
for i, f in enumerate(forms):
    if f in ("8-K", "10-Q", "10-K", "NT 10-K", "NT 10-Q", "DEF 14A"):
        acc = accs[i].replace("-", "")
        url = "https://www.sec.gov/Archives/edgar/data/%s/%s/%s" % (cik, acc, docs[i])
        print("    %-8s %s  %s" % (f, dates[i], url))
        shown += 1
        if shown >= 8:
            break
if not shown:
    print("    NOT_RETRIEVED: no recent 8-K/10-Q/10-K found")
print()
print("  NEXT EARNINGS DATE: NOT_RETRIEVED by this script.")
print("  Verify from company IR or the most recent 8-K above. Do NOT infer it")
print("  from the last print. A wrong earnings date invalidates any 1-4 week view.")
PY
  else
    fail "SEC submissions for CIK $CIK"
  fi
  echo

  # ------------------------------------------------------------ fundamentals
  echo "[3] FUNDAMENTALS (SEC XBRL companyfacts, annual)"
  if curl -s --max-time 90 -H "User-Agent: $UA_SEC" \
       "https://data.sec.gov/api/xbrl/companyfacts/CIK${CIK}.json" -o "$TMP/cf.json"; then
    python3 - "$TMP/cf.json" <<'PY'
import json, sys
facts = (json.load(open(sys.argv[1])).get("facts") or {}).get("us-gaap") or {}

WANT = [
    ("revenue", ["RevenueFromContractWithCustomerExcludingAssessedTax",
                 "Revenues", "SalesRevenueNet", "RevenueFromContractWithCustomerIncludingAssessedTax"]),
    ("gross_profit", ["GrossProfit"]),
    ("operating_income", ["OperatingIncomeLoss"]),
    ("net_income", ["NetIncomeLoss", "ProfitLoss"]),
    ("cfo", ["NetCashProvidedByUsedInOperatingActivities",
             "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations"]),
    ("capex", ["PaymentsToAcquirePropertyPlantAndEquipment",
               "PaymentsToAcquireProductiveAssets",
               "PaymentsForCapitalImprovements",
               "PaymentsToAcquireOtherPropertyPlantAndEquipment"]),
    ("sbc", ["ShareBasedCompensation", "AllocatedShareBasedCompensationExpense"]),
    ("diluted_shares", ["WeightedAverageNumberOfDilutedSharesOutstanding"]),
    ("cash", ["CashAndCashEquivalentsAtCarryingValue",
              "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"]),
    ("total_assets", ["Assets"]),
    ("equity", ["StockholdersEquity"]),
    ("lt_debt_noncurrent", ["LongTermDebtNoncurrent", "LongTermDebt"]),
]

def annual(tags):
    """Merge FY rows across ALL candidate tags, keeping the latest-filed value
    per period end. Filers switch tags between years (NVDA moved off
    RevenueFromContractWithCustomer..., for example), so returning the first tag
    that has any rows silently yields a decade-old series."""
    merged = {}   # end -> (filed, val, tag, unit)
    for tag in tags:
        node = facts.get(tag)
        if not node:
            continue
        for unit, rows in (node.get("units") or {}).items():
            for r in rows or []:
                if r.get("form") != "10-K" or r.get("fp") != "FY":
                    continue
                end, filed = r.get("end"), r.get("filed", "")
                if not end or r.get("val") is None:
                    continue
                prev = merged.get(end)
                if prev is None or filed > prev[0]:
                    merged[end] = (filed, r["val"], tag, unit)
    if not merged:
        return None, None, None
    ends = sorted(merged)[-4:]
    tags_used = sorted({merged[e][2] for e in ends})
    unit = merged[ends[-1]][3]
    return ("+".join(tags_used), unit,
            [{"end": e, "val": merged[e][1], "filed": merged[e][0]} for e in ends])

store = {}
for label, tags in WANT:
    tag, unit, rows = annual(tags)
    if not rows:
        print("  %-20s NOT_RETRIEVED (tags tried: %s)" % (label + ":", ", ".join(tags)))
        continue
    store[label] = {r["end"]: r["val"] for r in rows}
    disp = "  ".join("%s=%s" % (r["end"][:7], format(r["val"], ",.0f")) for r in rows)
    print("  %-20s %s" % (label + ":", disp))
    print("  %-20s tag=%s unit=%s filed=%s" % ("", tag, unit, rows[-1].get("filed")))
    if "+" in tag:
        print("  %-20s WARNING: series spans multiple tags, so the definition may"
              % "")
        print("  %-20s change between years. Verify against the filing before use."
              % "")

# Derived, only where every input was actually retrieved.
print()
print("  DERIVED (computed only where inputs were retrieved):")
cfo, capex = store.get("cfo"), store.get("capex")
ni = store.get("net_income")
if cfo and capex:
    for end in sorted(set(cfo) & set(capex))[-3:]:
        fcf = cfo[end] - capex[end]
        line = "    FCF %s: %s" % (end[:7], format(fcf, ",.0f"))
        if ni and end in ni and ni[end]:
            line += "   cash_conversion=%.2f" % (fcf / ni[end])
        print(line)
else:
    print("    FCF: NOT_RETRIEVED (needs both cfo and capex)")

sbc, rev = store.get("sbc"), store.get("revenue")
if sbc and rev:
    for end in sorted(set(sbc) & set(rev))[-3:]:
        if rev[end]:
            print("    SBC/revenue %s: %.1f%%" % (end[:7], 100 * sbc[end] / rev[end]))
else:
    print("    SBC/revenue: NOT_RETRIEVED")

sh = store.get("diluted_shares")
if sh and len(sh) >= 2:
    ends = sorted(sh)
    print("    diluted share count %s -> %s: %+.1f%% (net of buybacks AND issuance)"
          % (ends[0][:7], ends[-1][:7], 100 * (sh[ends[-1]] / sh[ends[0]] - 1)))
else:
    print("    share count trend: NOT_RETRIEVED")

print()
print("  NOTE: XBRL tag usage varies by filer. A NOT_RETRIEVED above means this")
print("  company tags it differently, not that the figure does not exist. Check")
print("  the filing directly before reporting the field as unavailable.")
PY
  else
    fail "SEC companyfacts for CIK $CIK"
  fi
  echo
fi

# ------------------------------------------------------------- short interest
echo "[4] SHORT INTEREST (Nasdaq, undocumented endpoint)"
NQ_CODE=$(curl -s -o "$TMP/si.json" -w '%{http_code}' --max-time 30 -A "$UA_WEB" \
  "https://api.nasdaq.com/api/quote/${TICKER}/short-interest?assetClass=stocks")
if [[ "$NQ_CODE" == "200" ]]; then
  python3 - "$TMP/si.json" <<'PY'
import json, sys
try:
    d = json.load(open(sys.argv[1]))
except Exception:
    print("  NOT_RETRIEVED: unparseable response"); raise SystemExit
rows = (((d.get("data") or {}).get("shortInterestTable") or {}).get("rows")) or []
if not rows:
    print("  NOT_RETRIEVED: no short interest rows returned")
else:
    print("  settlement    short_interest      avg_daily_vol      days_to_cover")
    for r in rows[:4]:
        print("  %-13s %-19s %-18s %s" % (r.get("settlementDate", "?"),
                                          r.get("interest", "?"),
                                          r.get("avgDailyShareVolume", "?"),
                                          r.get("daysToCover", "?")))
    print()
    print("  Short interest is as of the SETTLEMENT DATE, published roughly 9")
    print("  business days later. It is not today's positioning. Say so.")
    print("  Short interest as % OF FLOAT: NOT_RETRIEVED (needs float; get from filings).")
PY
else
  fail "Nasdaq short interest returned HTTP $NQ_CODE. Fall back to FINRA files."
fi
echo

echo "=============================================================="
echo "REMINDERS"
echo "  - Every NOT_RETRIEVED above stays NOT_RETRIEVED in the output. Do not"
echo "    fill it from memory. Recalled figures are stale by construction and"
echo "    render identically to retrieved ones."
echo "  - The CBOE data_timestamp is the real as-of for price and IV. If it is"
echo "    not the current session, quote it as a close, not a current price."
echo "  - Verify the next earnings date from IR before any short-horizon view."
echo "  - This script covers US filers only. Foreign issuers file 20-F/40-F and"
echo "    are not covered by the us-gaap taxonomy pulls above."
echo "=============================================================="
