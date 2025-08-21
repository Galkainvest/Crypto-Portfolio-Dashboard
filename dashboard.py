#!/usr/bin/env python3
# Crypto Portfolio Dashboard
# Pure Python, no external deps. Fetches USD prices from CoinGecko (no API key).
# Falls back to buy_price if live price unavailable.

import json
import urllib.request
import urllib.error
from typing import Dict, List

PORTFOLIO_FILE = "portfolio.json"

# Map tickers -> CoinGecko IDs
CG_IDS = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "USDT": "tether",
    "BNB": "binancecoin",
    "XRP": "ripple",
    "DOGE": "dogecoin",
    "TON": "the-open-network",
    "ADA": "cardano",
    "ARB": "arbitrum",
    "OP":  "optimism"
}

def load_portfolio(path: str) -> List[Dict]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # normalize keys
    for a in data:
        a["symbol"] = a["symbol"].upper()
        a["amount"] = float(a["amount"])
        a["buy_price_usd"] = float(a["buy_price_usd"])
    return data

def fetch_prices(symbols: List[str]) -> Dict[str, float]:
    ids = [CG_IDS[s] for s in symbols if s in CG_IDS]
    if not ids:
        return {}
    url = (
        "https://api.coingecko.com/api/v3/simple/price"
        f"?ids={','.join(ids)}&vs_currencies=usd"
    )
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            raw = resp.read().decode("utf-8")
            data = json.loads(raw)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return {}

    # reverse-map ID -> symbol
    id_to_symbol = {v: k for k, v in CG_IDS.items()}
    prices = {}
    for cg_id, payload in data.items():
        sym = id_to_symbol.get(cg_id)
        if sym and "usd" in payload:
            prices[sym] = float(payload["usd"])
    return prices

def fmt_money(x: float) -> str:
    return f"${x:,.2f}"

def fmt_pct(x: float) -> str:
    sign = "+" if x >= 0 else ""
    return f"{sign}{x:.2f}%"

def print_table(rows: List[List[str]], headers: List[str]):
    # simple fixed-width table
    col_w = [max(len(h), *(len(r[i]) for r in rows)) for i, h in enumerate(headers)]
    def line(char="-"):
        print("+" + "+".join(char * (w + 2) for w in col_w) + "+")
    def row(items):
        print("| " + " | ".join(it.ljust(w) for it, w in zip(items, col_w)) + " |")

    line("=")
    row(headers)
    line("=")
    for r in rows:
        row(r)
    line("=")

def main():
    pf = load_portfolio(PORTFOLIO_FILE)
    symbols = sorted({a["symbol"] for a in pf})
    live = fetch_prices(symbols)

    rows = []
    total_cost = 0.0
    total_value = 0.0

    for a in pf:
        sym = a["symbol"]
        amt = a["amount"]
        buy = a["buy_price_usd"]
        live_price = live.get(sym, buy)  # fallback

        cost = amt * buy
        value = amt * live_price
        pnl = value - cost
        pnl_pct = (pnl / cost * 100.0) if cost else 0.0

        total_cost += cost
        total_value += value

        rows.append([
            sym,
            f"{amt:g}",
            fmt_money(buy),
            fmt_money(live_price),
            fmt_money(cost),
            fmt_money(value),
            fmt_money(pnl),
            fmt_pct(pnl_pct)
        ])

    headers = ["Asset", "Amount", "Buy/USD", "Price/USD", "Cost", "Value", "PnL", "PnL%"]
    print("\n📊 Crypto Portfolio Dashboard\n")
    print_table(rows, headers)

    total_pnl = total_value - total_cost
    total_pct = (total_pnl / total_cost * 100.0) if total_cost else 0.0
    print(f"Total Cost : {fmt_money(total_cost)}")
    print(f"Total Value: {fmt_money(total_value)}")
    print(f"Total PnL  : {fmt_money(total_pnl)}  ({fmt_pct(total_pct)})\n")

if __name__ == "__main__":
    main()
