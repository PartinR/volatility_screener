# Volatility Screener

A modular Python framework for identifying high-volatility equities across the S&P 500. Built to translate raw market data into actionable risk signals through statistically grounded analytics.

---

## Overview

Markets reward those who can quantify uncertainty. **Volatility Screener** is an end-to-end data and analytics pipeline that ingests the S&P 500 ticker universe, computes volatility metrics from historical price action, and surfaces the names exhibiting the highest annualized volatility relative to their peers.

The project is designed around the same principles that govern enterprise data platforms: clean separation of concerns, reproducible outputs, defensive data handling, and a pipeline that any teammate can pick up, extend, and trust.

---

## Why This Project

Volatility is the heartbeat of risk. Whether the goal is portfolio construction, options strategy, or simply understanding where market stress is concentrating on a given day, having a repeatable, defensible methodology matters more than the answer itself. This screener was built to:

- Practice translating financial domain logic (log returns, annualized volatility) into production-style Python.
- Apply data engineering fundamentals — caching, modular ingestion, error handling — to a real-world, messy data source.
- Produce decision-ready output: a ranked CSV that a human analyst can act on, not just a notebook of charts.

### Origin Story: A Stock-Picking Bracket

This project started as my entry into a March Madness-style stock-picking competition. The format rewarded outsized moves, so the strategy was straightforward in concept but only useful with the right tooling: **find names with the highest volatility that were still trending positive.**

Running the pipeline surfaced **SanDisk (SNDK)** as the top candidate: highest volatility in the universe with a positive return profile. I picked it on that basis and returned **roughly 44%** over the competition window — a real-world validation that the methodology produces actionable, not just academic, output.

---

## Architecture

The codebase is intentionally modular. Each component has a single, testable responsibility — making the pipeline easy to extend, debug, and hand off.

```
volatility_screener/
│
├── data/                    # Local cache for scraped SPX ticker list (gitignored)
│   └── spx_tickers.csv
│
├── src/                     # Core engine
│   ├── __init__.py
│   ├── scraper.py           # Pulls S&P 500 tickers from Wikipedia
│   ├── engine.py            # Annualized volatility calculation and ranking
│   └── utils.py             # Logging, path helpers, directory setup
│
├── results/                 # Timestamped output of volatility rankings
│   └── top_picks_<YYYY-MM-DD>.csv
│
├── main.py                  # Orchestration: scraping → analytics → output
├── requirements.txt         # pandas, numpy, yfinance, requests, python-dotenv
├── README.md
└── LICENSE                  # MIT
```

---

## Methodology

The analytical core lives in `src/engine.py` and follows a deliberate, transparent sequence:

1. **Universe construction** — S&P 500 tickers are scraped from Wikipedia and cached locally to minimize redundant network calls and respect upstream rate limits.
2. **Price ingestion** — Adjusted close prices are pulled over a 1-year lookback window via `yfinance`.
3. **Log returns** — Daily log returns are computed for numerical stability and additivity over time.
4. **Annualized volatility** — Standard deviation of daily returns scaled by √252 to express risk on a comparable, annualized basis.
5. **Ranked output** — Results are sorted descending by annualized volatility and written to a timestamped CSV in `/results`, ready for downstream review.

---

## Engineering Practices

- **Separation of concerns.** Scraping, computation, and orchestration are isolated so any one layer can be swapped (e.g., switching from `yfinance` to a paid API) without touching the others.
- **Reproducibility.** Outputs are timestamped and deterministic given the same input window. No hidden state.
- **Defensive data handling.** Missing tickers, delisted symbols, and partial price histories are logged and skipped rather than silently corrupting downstream metrics.
- **Configuration over hardcoding.** Lookback windows, universe selection, and output paths are parameterized.
- **Environment variable support.** `python-dotenv` is wired in via `utils.py` to support future API key requirements without code changes.

---

## Quickstart

```bash
git clone https://github.com/<you>/volatility_screener.git
cd volatility_screener
pip install -r requirements.txt
python main.py
```

Outputs land in `/results` as `top_picks_<YYYY-MM-DD>.csv`.

---

## Roadmap

- Rolling-window volatility regimes (30D / 90D / 252D side-by-side)
- Z-score normalization to surface names that are *unusually* volatile relative to their peers, not just high in absolute terms
- GARCH(1,1) forecasts for forward-looking volatility estimates
- Sector-relative z-scores to neutralize industry beta
- Lightweight dashboard layer for non-technical reviewers
- Unit tests around the analytics module with synthetic price series

---

## Skills Demonstrated

- **Python** — object-oriented design, modular package structure, idiomatic `pandas` and `numpy`
- **Data & analytics** — statistical normalization, time-series math, financial domain modeling
- **Data engineering** — ingestion, caching, error handling, reproducible pipelines
- **Communication** — clear documentation, decision-ready outputs, code written to be read

---

## License

MIT. See [LICENSE](./LICENSE).
