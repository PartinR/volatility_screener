import os
import pandas as pd
from src.utils import setup_logging, get_project_root, get_timestamp, ensure_directories
from src.scraper import fetch_spx_tickers, save_tickers
from src.engine import get_vol_rankings

logger = setup_logging()

def run_screener():
    """
    Main orchestration logic for the volatility framework.
    """
    # 1. Setup
    ensure_directories()
    timestamp = get_timestamp()
    root = get_project_root()

    logger.info("Starting Volatility Screener...")
    
    # 2. Fetch Tickers
    ticker_path = os.path.join(root, "data", "spx_tickers.csv")

    if os.path.exists(ticker_path):
        logger.info("Using existing ticker list.")
        tickers = pd.read_csv(ticker_path)["Ticker"].tolist()
    else:
        logger.info("Fetching new ticker list...")
        tickers = fetch_spx_tickers()
        if not tickers:
            logger.error("Could not obtain tickers. Exiting.")
            return
        save_tickers(tickers)

    # 3. Calculation Phase
    logger.info("Calculating volatility rankings...")
    rankings = get_vol_rankings(tickers)
    if rankings is None:
        logger.error("Failed to calculate rankings. Exiting.")
        return

    # 4. Save Results
    if rankings is not None and not rankings.empty:
        output_file = f"top_picks_{timestamp}.csv"
        output_path = os.path.join(root, "results", output_file)

        rankings.to_csv(output_path)

        logger.info(f"Results saved to {output_path}")
        print(rankings.head(10))
    else:
        logger.warning("No rankings generated. Check logs for errors.")

if __name__ == "__main__":
    run_screener()