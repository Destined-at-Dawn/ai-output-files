"""Weekly market signal scan - 2026-06-19"""
import sys, json, os
sys.path.insert(0, r"E:\ai产出文件\牛马\个人\个人\digital-oracle")

from digital_oracle.providers.fear_greed import FearGreedProvider
from digital_oracle.providers.treasury import USTreasuryProvider, YieldCurveQuery
from digital_oracle.providers.cftc import CftcCotProvider, CftcCotQuery
from digital_oracle.providers.coingecko import CoinGeckoProvider, CoinGeckoPriceQuery
from digital_oracle.providers.polymarket import PolymarketProvider, PolymarketEventQuery

results = {}

# 1. Fear & Greed
print("=== Fear & Greed ===")
try:
    fg = FearGreedProvider().get_index()
    results["fear_greed"] = {
        "score": fg.score,
        "rating": fg.rating,
        "timestamp": fg.timestamp,
        "previous_close": fg.previous_close,
        "one_week_ago": fg.one_week_ago,
        "one_month_ago": fg.one_month_ago,
        "one_year_ago": fg.one_year_ago,
    }
    print(f"Score: {fg.score} ({fg.rating})")
    print(f"Prev Close: {fg.previous_close}, 1W: {fg.one_week_ago}, 1M: {fg.one_month_ago}")
except Exception as e:
    results["fear_greed"] = {"error": str(e)}
    print(f"ERROR: {e}")

# 2. Treasury Yield Curve
print("\n=== Treasury Yield Curve ===")
try:
    treas = USTreasuryProvider()
    curve = treas.latest_yield_curve(YieldCurveQuery())
    if curve:
        y10 = curve.yield_for("10Y")
        y2 = curve.yield_for("2Y")
        y30 = curve.yield_for("30Y")
        spread = curve.spread("10Y", "2Y")
        results["treasury"] = {
            "date": curve.date,
            "y10": y10,
            "y2": y2,
            "y30": y30,
            "spread_10y_2y": spread,
            "all_points": {p.tenor: p.value for p in curve.points},
        }
        print(f"Date: {curve.date}")
        print(f"10Y: {y10}%, 2Y: {y2}%, 30Y: {y30}%")
        print(f"10Y-2Y Spread: {spread}%")
    else:
        results["treasury"] = {"error": "no data"}
        print("No yield curve data")
except Exception as e:
    results["treasury"] = {"error": str(e)}
    print(f"ERROR: {e}")

# 3. CFTC COT - Gold and Crude Oil
for commodity in ["GOLD", "CRUDE OIL"]:
    print(f"\n=== CFTC COT: {commodity} ===")
    try:
        cftc = CftcCotProvider()
        reports = cftc.list_reports(CftcCotQuery(commodity_name=commodity, limit=10))
        if reports:
            latest = reports[0]
            results[f"cftc_{commodity.lower().replace(' ', '_')}"] = {
                "date": latest.report_date,
                "market": latest.market_name,
                "mm_long": latest.mm_long,
                "mm_short": latest.mm_short,
                "mm_net": latest.mm_net,
                "prod_net": latest.prod_net,
                "open_interest": latest.open_interest,
                "all_reports": [
                    {
                        "date": r.report_date,
                        "mm_net": r.mm_net,
                        "open_interest": r.open_interest,
                    }
                    for r in reports[:5]
                ],
            }
            print(f"Date: {latest.report_date}")
            print(f"Market: {latest.market_name}")
            print(f"MM Net: {latest.mm_net} (L:{latest.mm_long} S:{latest.mm_short})")
            print(f"Prod Net: {latest.prod_net}")
            print(f"OI: {latest.open_interest}")
            for i, r in enumerate(reports[:5]):
                print(f"  [{i}] {r.report_date}: MM_net={r.mm_net}, OI={r.open_interest}")
        else:
            results[f"cftc_{commodity.lower().replace(' ', '_')}"] = {"error": "no data"}
            print(f"No CFTC data for {commodity}")
    except Exception as e:
        results[f"cftc_{commodity.lower().replace(' ', '_')}"] = {"error": str(e)}
        print(f"ERROR: {e}")

# 4. CoinGecko - BTC & ETH
print("\n=== CoinGecko: BTC & ETH ===")
try:
    cg = CoinGeckoProvider()
    prices = cg.get_prices(CoinGeckoPriceQuery(coin_ids=("bitcoin", "ethereum")))
    for p in prices:
        results[f"coingecko_{p.coin_id}"] = {
            "price_usd": p.price_usd,
            "market_cap_usd": p.market_cap_usd,
            "volume_24h_usd": p.volume_24h_usd,
            "price_change_24h_pct": p.price_change_24h_pct,
        }
        print(f"{p.coin_id}: ${p.price_usd:,.2f} | MCap: ${p.market_cap_usd/1e9:.2f}B | 24h Vol: ${p.volume_24h_usd/1e9:.2f}B | 24h Chg: {p.price_change_24h_pct:.2f}%")

    # Global data
    g = cg.get_global()
    results["crypto_global"] = {
        "total_market_cap_usd": g.total_market_cap_usd,
        "btc_dominance_pct": g.btc_dominance_pct,
        "eth_dominance_pct": g.eth_dominance_pct,
        "market_cap_change_24h_pct": g.market_cap_change_24h_pct,
    }
    print(f"Total MCap: ${g.total_market_cap_usd/1e9:.2f}B | BTC Dom: {g.btc_dominance_pct:.1f}% | ETH Dom: {g.eth_dominance_pct:.1f}%")
    print(f"MCap 24h Change: {g.market_cap_change_24h_pct:.2f}%")
except Exception as e:
    results["coingecko_error"] = {"error": str(e)}
    print(f"ERROR: {e}")

# 5. Polymarket - Top Events
print("\n=== Polymarket: Top Events ===")
try:
    pm = PolymarketProvider()
    events = pm.list_events(PolymarketEventQuery(limit=15, order="volume_24hr", active=True, closed=False))
    pm_results = []
    for ev in events[:12]:
        primary = ev.primary_market()
        yes_prob = primary.yes_probability if primary else None
        entry = {
            "title": ev.title,
            "slug": ev.slug,
            "volume_24hr": ev.volume_24hr,
            "liquidity": ev.liquidity,
            "yes_prob": yes_prob,
        }
        pm_results.append(entry)
        prob_str = f"{yes_prob*100:.1f}%" if yes_prob is not None else "N/A"
        print(f"  {ev.title} | Yes: {prob_str} | Vol24h: ${ev.volume_24hr:,.0f}" if ev.volume_24hr else f"  {ev.title} | Yes: {prob_str}")
    results["polymarket"] = pm_results
except Exception as e:
    results["polymarket_error"] = {"error": str(e)}
    print(f"ERROR: {e}")

# Save results
out_path = r"E:\ai产出文件\牛马\个人\个人\digital-oracle\scripts\scan_0619_results.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False, default=str)
print(f"\nResults saved to {out_path}")
