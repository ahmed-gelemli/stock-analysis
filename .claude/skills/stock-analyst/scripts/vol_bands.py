#!/usr/bin/env python3
"""Volatility-anchored forecast bands.

Removes discretion from range construction. An eyeballed range is almost always
far too narrow; this computes the band the market's own volatility implies.

Usage:
  # From implied vol (preferred: forward-looking, and free from CBOE)
  vol_bands.py --spot 223.80 --iv 39.7 --horizon 1m

  # Pull spot and IV30 straight from CBOE
  vol_bands.py --ticker NVDA --horizon 1m

  # From a price history when no options exist
  vol_bands.py --spot 12.40 --prices prices.csv --horizon 3m

  # Shift the center for a view, stated in sigma units
  vol_bands.py --ticker NVDA --horizon 1m --shift 0.4

Horizons: 1w, 1m, 3m, 6m, 1y, or Nd for N trading days.
"""

import argparse
import json
import math
import sys
import urllib.request

TRADING_DAYS_PER_YEAR = 252

HORIZONS = {
    "1w": 5,
    "2w": 10,
    "1m": 21,
    "2m": 42,
    "3m": 63,
    "6m": 126,
    "9m": 189,
    "1y": 252,
    "2y": 504,
}

CBOE_URL = "https://cdn.cboe.com/api/global/delayed_quotes/options/{ticker}.json"


def parse_horizon(text):
    if text in HORIZONS:
        return HORIZONS[text], text
    if text.endswith("d"):
        try:
            days = int(text[:-1])
            return days, "%d trading days" % days
        except ValueError:
            pass
    raise SystemExit(
        "Unrecognized horizon %r. Use one of %s, or Nd for N trading days."
        % (text, ", ".join(HORIZONS))
    )


def fetch_cboe(ticker):
    """Return (spot, iv30_pct, timestamp, close). Raises on failure, loudly."""
    req = urllib.request.Request(
        CBOE_URL.format(ticker=ticker.upper()),
        headers={"User-Agent": "stock-analyst-skill/1.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.load(resp)
    except Exception as exc:  # network, HTTP, or malformed JSON
        raise SystemExit(
            "NOT RETRIEVED: CBOE lookup failed for %s (%s).\n"
            "  A 403 usually means no listed options for this ticker.\n"
            "  Fall back to --prices for realized vol. Do NOT substitute a "
            "remembered volatility." % (ticker.upper(), exc)
        )

    data = payload.get("data") or {}
    spot = data.get("current_price")
    iv30 = data.get("iv30")
    if spot is None or iv30 is None:
        raise SystemExit(
            "NOT RETRIEVED: CBOE returned no current_price/iv30 for %s. "
            "Do not substitute a remembered value." % ticker
        )
    return float(spot), float(iv30), payload.get("timestamp"), data.get("close")


def realized_vol_from_prices(path):
    """Annualized realized vol from a file of prices, one per line or CSV.

    Uses the last close in the file as the most recent observation. Accepts a
    bare list of numbers, or CSV where the last numeric field on each line is
    the price (so an adjusted-close column works).
    """
    values = []
    with open(path) as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            fields = [f.strip() for f in line.replace(",", " ").split()]
            for field in reversed(fields):
                try:
                    values.append(float(field))
                    break
                except ValueError:
                    continue

    if len(values) < 22:
        raise SystemExit(
            "NOT RETRIEVED: need at least 22 prices for a 21-day realized vol, got %d."
            % len(values)
        )

    window = values[-22:]
    returns = [math.log(window[i] / window[i - 1]) for i in range(1, len(window))]
    mean = sum(returns) / len(returns)
    variance = sum((r - mean) ** 2 for r in returns) / (len(returns) - 1)
    return math.sqrt(variance) * math.sqrt(TRADING_DAYS_PER_YEAR) * 100.0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ticker", help="Fetch spot and IV30 from CBOE")
    ap.add_argument("--spot", type=float, help="Current price")
    ap.add_argument("--iv", type=float, help="Annualized implied vol, in percent")
    ap.add_argument("--prices", help="File of historical prices for realized vol")
    ap.add_argument("--horizon", default="1m", help="1w, 1m, 3m, 6m, 1y, or Nd")
    ap.add_argument("--shift", type=float, default=0.0,
                    help="Shift the band center by N sigma to express a view")
    args = ap.parse_args()

    days, horizon_label = parse_horizon(args.horizon)

    spot = args.spot
    vol_pct = args.iv
    source = "user-supplied"
    stamp = None
    close = None

    if args.ticker:
        spot_cboe, iv30, stamp, close = fetch_cboe(args.ticker)
        if spot is None:
            spot = spot_cboe
        if vol_pct is None:
            vol_pct = iv30
        source = "CBOE delayed quote (data timestamp %s)" % stamp

    if vol_pct is None and args.prices:
        vol_pct = realized_vol_from_prices(args.prices)
        source = "21-day realized vol from %s" % args.prices

    if spot is None:
        raise SystemExit("NOT RETRIEVED: no spot price. Supply --spot or --ticker.")
    if vol_pct is None:
        raise SystemExit(
            "NOT RETRIEVED: no volatility input. Supply --iv, --prices, or --ticker."
        )

    vol = vol_pct / 100.0
    sigma_h = vol * math.sqrt(days / TRADING_DAYS_PER_YEAR)
    center = spot * math.exp(args.shift * sigma_h)

    def band(n):
        return center * math.exp(-n * sigma_h), center * math.exp(n * sigma_h)

    lo68, hi68 = band(1)
    lo95, hi95 = band(2)

    print("VOLATILITY-ANCHORED BAND")
    print("  Spot:        %.2f" % spot)
    if close is not None and abs(float(close) - spot) > 1e-9:
        print("  Prior close: %.2f   <- differs from last trade; state which you quote"
              % float(close))
    print("  Vol input:   %.2f%% annualized (%s)" % (vol_pct, source))
    print("  Horizon:     %s (%d trading days)" % (horizon_label, days))
    print("  sigma_h:     %.4f  = %.4f x sqrt(%d/252)" % (sigma_h, vol, days))
    if args.shift:
        print("  Center:      %.2f  (shifted %+.2f sigma from spot)" % (center, args.shift))
    print()
    print("  ~68%% band:   %.2f  to  %.2f    (%+.1f%% / %+.1f%%)"
          % (lo68, hi68, (lo68 / spot - 1) * 100, (hi68 / spot - 1) * 100))
    print("  ~95%% band:   %.2f  to  %.2f    (%+.1f%% / %+.1f%%)"
          % (lo95, hi95, (lo95 / spot - 1) * 100, (hi95 / spot - 1) * 100))
    print()
    print("  State the coverage whenever you quote a band. A range with no stated")
    print("  coverage communicates nothing. Do not narrow the band for conviction:")
    print("  narrowing requires a volatility argument, not a confidence one.")

    if stamp:
        print()
        print("  Data as-of %s. If that is not today's session, say so in the output."
              % stamp)


if __name__ == "__main__":
    sys.exit(main())
