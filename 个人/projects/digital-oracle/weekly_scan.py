"""Weekly market signal scan - 2026-05-15"""
import sys
import json
import traceback
from datetime import datetime

sys.path.insert(0, ".")

from digital_oracle.providers.fear_greed import FearGreedProvider
from digital_oracle.providers.treasury import USTreasuryProvider, YieldCurveQuery
from digital_oracle.providers.cftc import CftcCotProvider, CftcCotQuery
from digital_oracle.providers.coingecko import CoinGeckoProvider, CoinGeckoPriceQuery
from digital_oracle.providers.polymarket import PolymarketProvider, PolymarketEventQuery

results = {}

# 1. FearGreed Index
print("=" * 60)
print("[1/5] Fetching CNN Fear & Greed Index...")
try:
    fg = FearGreedProvider()
    snap = fg.get_index()
    results["fear_greed"] = {
        "score": snap.score,
        "rating": snap.rating,
        "previous_close": snap.previous_close,
        "one_week_ago": snap.one_week_ago,
        "one_month_ago": snap.one_month_ago,
        "one_year_ago": snap.one_year_ago,
        "timestamp": snap.timestamp,
    }
    print(f"  Score: {snap.score} ({snap.rating})")
    print(f"  1 Week Ago: {snap.one_week_ago}")
    print(f"  1 Month Ago: {snap.one_month_ago}")
except Exception as e:
    results["fear_greed"] = {"error": str(e)}
    print(f"  ERROR: {e}")
    traceback.print_exc()

# 2. Treasury Yield Curve (10Y-2Y spread)
print("\n" + "=" * 60)
print("[2/5] Fetching US Treasury Yield Curve...")
try:
    treas = USTreasuryProvider()
    curve = treas.latest_yield_curve(YieldCurveQuery(year=2026, curve_kind="nominal"))
    if curve:
        y10 = curve.yield_for("10Y")
        y2 = curve.yield_for("2Y")
        spread = curve.spread("10Y", "2Y") if y10 is not None and y2 is not None else None
        results["treasury"] = {
            "date": curve.date,
            "10Y": y10,
            "2Y": y2,
            "spread_10Y_2Y": spread,
            "all_points": {p.tenor: p.value for p in curve.points},
        }
        print(f"  Date: {curve.date}")
        print(f"  10Y: {y10}%")
        print(f"  2Y: {y2}%")
        print(f"  10Y-2Y Spread: {spread}%")
    else:
        results["treasury"] = {"error": "no data returned"}
        print("  No yield curve data returned")
except Exception as e:
    results["treasury"] = {"error": str(e)}
    print(f"  ERROR: {e}")
    traceback.print_exc()

# 3. CFTC COT - Gold and Crude Oil
print("\n" + "=" * 60)
print("[3/5] Fetching CFTC COT Data (Gold & Crude Oil)...")
try:
    cftc = CftcCotProvider()
    gold_reports = cftc.list_reports(CftcCotQuery(commodity_name="GOLD", limit=4))
    oil_reports = cftc.list_reports(CftcCotQuery(commodity_name="CRUDE OIL", limit=4))

    def report_to_dict(r):
        return {
            "date": r.report_date,
            "commodity": r.commodity,
            "market": r.market_name,
            "mm_long": r.mm_long,
            "mm_short": r.mm_short,
            "mm_net": r.mm_net,
            "prod_long": r.prod_long,
            "prod_short": r.prod_short,
            "prod_net": r.prod_net,
            "open_interest": r.open_interest,
        }

    results["cftc_gold"] = [report_to_dict(r) for r in gold_reports]
    results["cftc_oil"] = [report_to_dict(r) for r in oil_reports]

    if gold_reports:
        latest_gold = gold_reports[0]
        print(f"  Gold ({latest_gold.report_date}): MM Net={latest_gold.mm_net}, OI={latest_gold.open_interest}")
        if len(gold_reports) >= 2:
            prev_gold = gold_reports[1]
            if prev_gold.open_interest > 0:
                oi_change_pct = (latest_gold.open_interest - prev_gold.open_interest) / prev_gold.open_interest * 100
                print(f"    OI Change: {oi_change_pct:+.1f}%")
                results["gold_oi_change_pct"] = round(oi_change_pct, 2)
            if prev_gold.mm_net != 0:
                mm_change_pct = (latest_gold.mm_net - prev_gold.mm_net) / abs(prev_gold.mm_net) * 100
                print(f"    MM Net Change: {mm_change_pct:+.1f}%")
                results["gold_mm_change_pct"] = round(mm_change_pct, 2)

    if oil_reports:
        latest_oil = oil_reports[0]
        print(f"  Oil ({latest_oil.report_date}): MM Net={latest_oil.mm_net}, OI={latest_oil.open_interest}")
        if len(oil_reports) >= 2:
            prev_oil = oil_reports[1]
            if prev_oil.open_interest > 0:
                oi_change_pct = (latest_oil.open_interest - prev_oil.open_interest) / prev_oil.open_interest * 100
                print(f"    OI Change: {oi_change_pct:+.1f}%")
                results["oil_oi_change_pct"] = round(oi_change_pct, 2)
            if prev_oil.mm_net != 0:
                mm_change_pct = (latest_oil.mm_net - prev_oil.mm_net) / abs(prev_oil.mm_net) * 100
                print(f"    MM Net Change: {mm_change_pct:+.1f}%")
                results["oil_mm_change_pct"] = round(mm_change_pct, 2)
except Exception as e:
    results["cftc_error"] = str(e)
    print(f"  ERROR: {e}")
    traceback.print_exc()

# 4. CoinGecko - BTC/ETH
print("\n" + "=" * 60)
print("[4/5] Fetching CoinGecko BTC/ETH Data...")
try:
    cg = CoinGeckoProvider()
    prices = cg.get_prices(CoinGeckoPriceQuery(
        coin_ids=("bitcoin", "ethereum"),
        include_market_cap=True,
        include_24h_vol=True,
    ))
    cg_global = cg.get_global()

    results["coingecko"] = {
        "prices": [
            {
                "coin": p.coin_id,
                "price_usd": p.price_usd,
                "market_cap": p.market_cap_usd,
                "vol_24h": p.volume_24h_usd,
                "change_24h_pct": p.price_change_24h_pct,
            }
            for p in prices
        ],
        "global": {
            "total_market_cap": cg_global.total_market_cap_usd,
            "total_vol_24h": cg_global.total_volume_24h_usd,
            "btc_dominance": cg_global.btc_dominance_pct,
            "eth_dominance": cg_global.eth_dominance_pct,
            "market_cap_change_24h_pct": cg_global.market_cap_change_24h_pct,
        },
    }

    for p in prices:
        print(f"  {p.coin_id.upper()}: ${p.price_usd:,.2f} (24h: {p.price_change_24h_pct:+.1f}%) MC: ${p.market_cap_usd:,.0f}")
    print(f"  BTC Dominance: {cg_global.btc_dominance_pct:.1f}%")
    print(f"  Total MC: ${cg_global.total_market_cap_usd:,.0f}")
except Exception as e:
    results["coingecko"] = {"error": str(e)}
    print(f"  ERROR: {e}")
    traceback.print_exc()

# 5. Polymarket - Hot Events
print("\n" + "=" * 60)
print("[5/5] Fetching Polymarket Hot Events...")
try:
    pm = PolymarketProvider()
    events = pm.list_events(PolymarketEventQuery(limit=15, active=True, closed=False, order="volume_24hr"))

    pm_results = []
    for ev in events[:10]:
        primary = ev.primary_market()
        yes_prob = primary.yes_probability if primary else None
        pm_results.append({
            "title": ev.title,
            "slug": ev.slug,
            "volume_24h": ev.volume_24hr,
            "liquidity": ev.liquidity,
            "yes_prob": yes_prob,
        })
        prob_str = f"{yes_prob*100:.1f}%" if yes_prob is not None else "N/A"
        print(f"  {ev.title[:60]} | Yes: {prob_str} | Vol24h: ${ev.volume_24hr:,.0f}" if ev.volume_24hr else f"  {ev.title[:60]} | Yes: {prob_str}")

    results["polymarket"] = pm_results
except Exception as e:
    results["polymarket"] = {"error": str(e)}
    print(f"  ERROR: {e}")
    traceback.print_exc()

# Output full JSON
print("\n" + "=" * 60)
print("FULL_JSON_START")
print(json.dumps(results, ensure_ascii=False, indent=2, default=str))
print("FULL_JSON_END")
