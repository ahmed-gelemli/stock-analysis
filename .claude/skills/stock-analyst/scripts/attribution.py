#!/usr/bin/env python3
"""Decompose a stock move into market, sector, and idiosyncratic components.

Most daily moves are beta plus noise. Attaching a company narrative to a move
that was entirely sector is the most common and most correctable error in
LLM equity analysis. Run this before explaining any move.

Usage:
  attribution.py NVDA SOXX SPY --days 5
  attribution.py TSLA XLY QQQ --days 21 --beta-window 126

Requires Yahoo's chart endpoint, which rate-limits aggressively. On failure it
says so rather than guessing.
"""

import argparse
import json
import math
import statistics
import sys
import urllib.request

CHART_URL = (
    "https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
    "?range={rng}&interval=1d"
)


def fetch_adjclose(ticker, rng="1y"):
    """Return (dates, adjusted closes). Adjusted, so splits and dividends are handled."""
    req = urllib.request.Request(
        CHART_URL.format(ticker=ticker.upper(), rng=rng),
        headers={"User-Agent": "Mozilla/5.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.load(resp)
    except Exception as exc:
        raise SystemExit(
            "NOT RETRIEVED: chart fetch failed for %s (%s).\n"
            "  Yahoo rate-limits and intermittently returns 429. Retry, or state\n"
            "  in the output that attribution could not be computed. Do NOT assert\n"
            "  an attribution you did not compute." % (ticker.upper(), exc)
        )

    result = (payload.get("chart") or {}).get("result")
    if not result:
        raise SystemExit("NOT RETRIEVED: no chart data for %s." % ticker.upper())

    node = result[0]
    stamps = node.get("timestamp") or []
    adj = (node.get("indicators", {}).get("adjclose") or [{}])[0].get("adjclose")
    if not adj:
        adj = (node.get("indicators", {}).get("quote") or [{}])[0].get("close")
        if not adj:
            raise SystemExit("NOT RETRIEVED: no price series for %s." % ticker.upper())
        print("  WARNING: %s using unadjusted close, splits/dividends not handled"
              % ticker.upper(), file=sys.stderr)

    pairs = [(t, p) for t, p in zip(stamps, adj) if p is not None]
    return [t for t, _ in pairs], [p for _, p in pairs]


def log_returns(prices):
    return [math.log(prices[i] / prices[i - 1]) for i in range(1, len(prices))]


def beta(stock_rets, bench_rets):
    n = min(len(stock_rets), len(bench_rets))
    if n < 20:
        raise SystemExit("NOT RETRIEVED: need >=20 overlapping returns for beta, got %d." % n)
    s, b = stock_rets[-n:], bench_rets[-n:]
    var = statistics.variance(b)
    if var == 0:
        raise SystemExit("Benchmark has zero variance; cannot compute beta.")
    mean_s, mean_b = statistics.mean(s), statistics.mean(b)
    cov = sum((s[i] - mean_s) * (b[i] - mean_b) for i in range(n)) / (n - 1)
    return cov / var


def total_return(prices, days):
    if len(prices) < days + 1:
        raise SystemExit(
            "NOT RETRIEVED: only %d observations, need %d for a %d-day window."
            % (len(prices), days + 1, days)
        )
    return prices[-1] / prices[-1 - days] - 1.0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ticker")
    ap.add_argument("sector_etf", help="Narrowest ETF containing the real peer set")
    ap.add_argument("index", nargs="?", default="SPY")
    ap.add_argument("--days", type=int, default=5, help="Trading days in the move window")
    ap.add_argument("--beta-window", type=int, default=252,
                    help="Trading days used to estimate beta")
    args = ap.parse_args()

    series = {}
    for name in (args.ticker, args.sector_etf, args.index):
        _, prices = fetch_adjclose(name)
        series[name.upper()] = prices

    tkr = args.ticker.upper()
    sec = args.sector_etf.upper()
    idx = args.index.upper()

    rets = {k: log_returns(v)[-args.beta_window:] for k, v in series.items()}
    n = min(len(rets[tkr]), len(rets[sec]), len(rets[idx]))
    rets = {k: v[-n:] for k, v in rets.items()}

    # Two-factor decomposition. Orthogonalize the sector against the market first,
    # so the two factors are uncorrelated and their loadings can be estimated
    # independently without double-counting the market exposure embedded in the
    # sector ETF. Regressing the stock directly on the sector ETF (rather than on
    # the orthogonalized residual) is the classic error here: it attributes the
    # sector's own market beta twice.
    sector_beta_to_mkt = beta(rets[sec], rets[idx])
    sec_excess_rets = [
        rets[sec][i] - sector_beta_to_mkt * rets[idx][i] for i in range(n)
    ]

    beta_mkt = beta(rets[tkr], rets[idx])
    beta_sec = beta(rets[tkr], sec_excess_rets)

    r_stock = total_return(series[tkr], args.days)
    r_sector = total_return(series[sec], args.days)
    r_index = total_return(series[idx], args.days)

    market_component = beta_mkt * r_index
    sector_excess = r_sector - sector_beta_to_mkt * r_index
    sector_component = beta_sec * sector_excess
    residual = r_stock - market_component - sector_component

    daily_vol = statistics.stdev(rets[tkr])
    window_vol = daily_vol * math.sqrt(args.days)
    sigmas = residual / window_vol if window_vol else 0.0

    print("MOVE ATTRIBUTION  %s over %d trading days" % (tkr, args.days))
    print("  beta(%s vs %s) = %.2f   beta(%s vs %s-excess) = %.2f   beta(%s vs %s) = %.2f"
          % (tkr, idx, beta_mkt, tkr, sec, beta_sec, sec, idx, sector_beta_to_mkt))
    print("  (beta window: %d trading days; sector orthogonalized to market)" % n)
    print()
    print("  %-28s %+7.2f%%" % ("%s total return" % tkr, r_stock * 100))
    print("  %-28s %+7.2f%%" % ("less market (beta x index)", market_component * 100))
    print("  %-28s %+7.2f%%" % ("less sector excess", sector_component * 100))
    print("  %-28s %+7.2f%%" % ("= IDIOSYNCRATIC", residual * 100))
    print()
    print("  Context: %s %+.2f%%, %s %+.2f%% over the same window."
          % (idx, r_index * 100, sec, r_sector * 100))
    print("  Residual is %.2f sigma of this stock's own %d-day move (1-sigma = %.2f%%)."
          % (sigmas, args.days, window_vol * 100))
    print()

    if abs(sigmas) < 1.0:
        print("  READ: the residual is under 1 sigma. The correct statement is that")
        print("  this was a market or sector move, NOT a company-specific one.")
        print("  Do not attach a company narrative to it.")
    else:
        print("  READ: the residual is %.1f sigma, so there is genuine company-specific" % abs(sigmas))
        print("  movement to explain. Explain the RESIDUAL only, not the headline move,")
        print("  and check that any news you cite predates the move.")


if __name__ == "__main__":
    sys.exit(main())
