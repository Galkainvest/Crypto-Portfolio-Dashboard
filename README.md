# 📊 Crypto Portfolio Dashboard

Minimal, readable crypto portfolio tracker.  
JSON in, clean console table out. No external Python packages required.

## ✨ Features
- JSON-based portfolio
- Live USD prices from CoinGecko (no API key)
- Automatic PnL and totals
- Pure Python, single script

## 📂 Structure
- `portfolio.json` – your assets (symbol, amount, buy_price_usd)
- `dashboard.py` – console dashboard
- `README.md` – this file

## ⚡ Usage
```bash
git clone https://github.com/Galkainvest/crypto-portfolio-dashboard
cd crypto-portfolio-dashboard
python dashboard.py
