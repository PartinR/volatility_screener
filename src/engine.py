import pandas as pd
import numpy as np
import yfinance as yf
import logging
from src.utils import setup_logging

logger = setup_logging()

def get_historical_data(tickers, period="1y"):
    """
    Downloads adjusted closing prices for a list of tickers.
    """
    logger.info(f"Downloading data from {len(tickers)} tickers...")
    try:
        data = yf.download(tickers, period=period, interval="1d", group_by="ticker", auto_adjust=True)
        return data
    except Exception as e:
        logger.error(f"Error downloading data: {e}")
        return None

def calculate_volatility(prices_df):
    """
    Calculates the annualized volatility for each ticker.
    """        
    # 1. Calculate log returns
    log_returns = np.log(prices_df / prices_df.shift(1))

    # 2. Calculate daily standard deviation
    daily_vol = log_returns.std()

    # 3. Annualize (multiply by sqrt(252))
    annualized_vol = daily_vol * np.sqrt(252)

    return annualized_vol

def get_vol_rankings(tickers):
    """
    The main engine logic: Fetch -> Calculate -> Rank
    """
    # 1. Fetch Data
    data = get_historical_data(tickers)
    if data is None:
        return None
    
    # 2. Extract 'Close' prices for all tickers
    #yf.download returns a MultiIndex if multiple tickers are passed
    close_prices = data.iloc[:, data.columns.get_level_values(1) == 'Close']
    close_prices.columns = close_prices.columns.get_level_values(0)

    # 3. Calculate Volatility
    vols = calculate_volatility(close_prices)

    # 4. Rank
    rankings = vols.sort_values(ascending=False).to_frame(name="Annualized_Volatility")
    return rankings

if __name__ == "__main__":
    # Test the engine
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]
    rankings = get_vol_rankings(tickers)
    print(rankings)