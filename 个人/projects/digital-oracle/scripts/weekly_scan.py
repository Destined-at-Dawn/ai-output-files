#!/usr/bin/env python3
"""Weekly market signal scan - 2026-06-12"""
import sys, json, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from digital_oracle.providers.fear_greed import FearGreedProvider
from digital_oracle.providers.treasury import USTreasuryProvider, YieldCurveQuery
from digital_oracle.providers.cftc import CftcCotProvider, CftcCotQuery
from digital_oracle.providers.coingecko import CoinGeckoProvider, CoinGeckoPriceQuery
from digital_oracle.providers.polymarket import PolymarketProvider, PolymarketEventQuery

results = {}

# 1. CNN Fear & Greed
print("=== Fetching FearGreed ===")
try:
    fg = FearGreedProvider()
    snap = fg.get_index()
    results["fear_greed"] = {
        "score": snap.score,
        "rating": snap.rating,
        "timestamp": snap.timestamp,
        "previous_close": snap.previous_close,
        "one_week_ago": snap.one_week_ago,
        "one_month_ago": snap.one_month_ago,
        "one_year_ago": snap.one_year_ago,
    }
    print(f"  Score: {snap.score} ({snap.rating})")
    print(f"  1w ago: {snap.one_week_ago}, 1m ago: {snap.one_month_ago}")
except Exception as e:
    results["fear_greed"] = {"error": str(e)}
    print(f"  ERROR: {e}")

# 2. US Treasury Yield Curve (10Y-2Y spread)
print("\n=== Fetching Treasury Yield Curve ===")
try:
    tr = USTreasuryProvider()
    curve = tr.latest_yield_curve(YieldCurveQuery(year=2026, curve_kind="nominal"))
    if curve:
        rates = {}
        for pt in curve.points:
            rates[pt.tenor] = pt.value
        # Find 10Y and 2Y by matching tenor labels
        y10 = None
        y2 = None
        for k, v in rates.items():
            kl = k.lower().replace(" ", "")
            if "10" in kl and "20" not in kl:
                y10 = v
            if "2" in kl and "20" not in kl and "32" not in kl:
                y2 = v
        spread = None
        if y10 is not None and y2 is not None:
            spread = round(y10 - y2, 4)
        results["treasury"] = {
            "date": curve.date,
            "spread_10y_2y": spread,
            "y10": y10,
            "y2": y2,
            "all_rates": {k: v for k, v in sorted(rates.items())},
        }
        print(f"  Date: {curve.date}")
        print(f"  10Y: {y10}%, 2Y: {y2}%, Spread: {spread}%")
        for k, v in sorted(rates.items()):
            print(f"    {k}: {v}%")
    else:
        results["treasury"] = {"error": "no data returned"}
        print("  No curve data")
except Exception as e:
    results["treasury"] = {"error": str(e)}
    print(f"  ERROR: {e}")

# 3. CFTC COT - Gold and Crude Oil
print("\n=== Fetching CFTC COT ===")
try:
    cftc = CftcCotProvider()
    gold_reports = cftc.list_reports(CftcCotQuery(commodity_name="GOLD", limit=6))
    results["cftc_gold"] = []
    for r in gold_reports[:3]:
        entry = {
            "date": r.report_date,
            "mm_long": r.mm_long,
            "mm_short": r.mm_short,
            "mm_net": r.mm_net,
            "open_interest": r.open_interest,
            "market": r.market_name,
        }
        results["cftc_gold"].append(entry)
        print(f"  Gold {r.report_date}: MM net={r.mm_net}, OI={r.open_interest}")
except Exception as e:
    results["cftc_gold"] = {"error": str(e)}
    print(f"  Gold ERROR: {e}")

try:
    cftc2 = CftcCotProvider()
    oil_reports = cftc2.list_reports(CftcCotQuery(commodity_name="CRUDE OIL", limit=6))
    results["cftc_oil"] = []
    for r in oil_reports[:3]:
        entry = {
            "date": r.report_date,
            "mm_long": r.mm_long,
            "mm_short": r.mm_short,
            "mm_net": r.mm_net,
            "open_interest": r.open_interest,
            "market": r.market_name,
        }
        results["cftc_oil"].append(entry)
        print(f"  Oil {r.report_date}: MM net={r.mm_net}, OI={r.open_interest}")
except Exception as e:
    results["cftc_oil"] = {"error": str(e)}
    print(f"  Oil ERROR: {e}")

# 4. CoinGecko - BTC/ETH prices and market cap
print("\n=== Fetching CoinGecko ===")
try:
    cg = CoinGeckoProvider()
    prices = cg.get_prices(CoinGeckoPriceQuery(
        coin_ids=("bitcoin", "ethereum"),
        include_market_cap=True,
        include_24h_vol=True,
    ))
    results["crypto_prices"] = {}
    for p in prices:
        results["crypto_prices"][p.coin_id] = {
            "price_usd": p.price_usd,
            "market_cap_usd": p.market_cap_usd,
            "volume_24h_usd": p.volume_24h_usd,
            "price_change_24h_pct": p.price_change_24h_pct,
        }
        print(f"  {p.coin_id}: ${p.price_usd:,.2f}, MCap=${(p.market_cap_usd or 0)/1e9:.2f}B, 24h={p.price_change_24h_pct or 0:+.2f}%")
except Exception as e:
    results["crypto_prices"] = {"error": str(e)}
    print(f"  Prices ERROR: {e}")

try:
    cg2 = CoinGeckoProvider()
    global_data = cg2.get_global()
    results["crypto_global"] = {
        "total_market_cap_usd": global_data.total_market_cap_usd,
        "total_volume_24h_usd": global_data.total_volume_24h_usd,
        "btc_dominance_pct": global_data.btc_dominance_pct,
        "eth_dominance_pct": global_data.eth_dominance_pct,
        "market_cap_change_24h_pct": global_data.market_cap_change_24h_pct,
        "active_cryptos": global_data.active_cryptocurrencies,
    }
    print(f"  Total MCap: ${global_data.total_market_cap_usd/1e12:.2f}T")
    print(f"  BTC Dom: {global_data.btc_dominance_pct:.2f}%")
except Exception as e:
    results["crypto_global"] = {"error": str(e)}
    print(f"  Global ERROR: {e}")

# 5. Polymarket - hot events
print("\n=== Fetching Polymarket ===")
for keyword in ["bitcoin", "fed", "recession", "iran", "ukraine", "gold"]:
    try:
        pm = PolymarketProvider()
        events = pm.list_events(PolymarketEventQuery(slug_contains=keyword, limit=5))
        key = f"pm_{keyword}"
        results[key] = []
        for ev in events[:3]:
            entry = {
                "title": ev.title,
                "slug": ev.slug,
                "end_date": ev.end_date,
            }
            if ev.markets:
                entry["markets"] = []
                for m in ev.markets[:3]:
                    # Build outcome info from outcomes tuple
                    outcomes_list = []
                    for o in m.outcomes:
                        outcomes_list.append({"name": o.name, "probability": o.probability})
                    mkt = {
                        "question": m.question,
                        "best_ask": m.best_ask,
                        "best_bid": m.best_bid,
                        "last_trade_price": m.last_trade_price,
                        "outcomes": outcomes_list,
                    }
                    entry["markets"].append(mkt)
            results[key].append(entry)
            mkts_info = ""
            if ev.markets:
                for m in ev.markets[:2]:
                    yes_p = m.yes_probability
                    mkts_info += f" [{m.question[:40]}: {yes_p}]"
            print(f"  [{keyword}] {ev.title[:60]}{mkts_info}")
    except Exception as e:
        results[f"pm_{keyword}"] = {"error": str(e)}
        print(f"  [{keyword}] ERROR: {e}")

# Write results to temp JSON
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scan_result_20260612.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2, default=str)
print(f"\n=== Results saved to {os.path.abspath(output_path)} ===")
