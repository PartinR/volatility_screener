# Volatility Screener
A modular Python framework to identify high volatility stocks.

/vol_screener
│
├── /data                # Local cache for scraped SPX/NQ ticker lists (ignored by git)
│   └── spx_tickers.csv
│
├── /src                 # The "Engine Room"
│   ├── __init__.py
│   ├── scraper.py       # Logic for pulling SPX/NQ tickers from Wikipedia/APIs
│   ├── engine.py        # Core math: Log returns, Annualized Vol, Z-Scores
│   └── utils.py         # Helper functions (date formatting, logging)
│
├── /results             # Output folder for your volatility rankings
│   └── top_picks_2026-03-10.csv
│
├── main.py              # The "Ignition": orchestrates the scraping and screening
├── requirements.txt     # List of dependencies (pandas, yfinance, etc.)
├── .gitignore           # Keeps the repo clean (ignores __pycache__, data/, and .env)
├── .env                 # Your private API keys (if using AlphaVantage/Polygon)
├── README.md            # The high-level pitch we discussed
└── LICENSE              # MIT License