import os
import requests
import pandas as pd
import logging
from src.utils import get_project_root, setup_logging

# Initialize logging
logger = setup_logging()

def fetch_spx_tickers():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    # A standard User-Agent string to mimic a real browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        logger.info("Fetching S&P 500 tickers from Wikipedia...")
        
        # Use requests to get the page content with headers
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # This will catch 403, 404, etc.
        
        # Now pass the text (HTML) to pandas
        tables = pd.read_html(response.text)
        df = tables[0]
        
        tickers = df['Symbol'].str.replace('.', '-', regex=False).tolist()
        logger.info(f"Successfully retrieved {len(tickers)} tickers.")
        return tickers
    
    except Exception as e:
        logger.error(f"Failed to fetch S&P 500 tickers: {e}")
        return []

def save_tickers(tickers, filename="spx_tickers.csv"):
    """
    Saves the list of tickers to the /data directory.
    """
    try:
        root = get_project_root()
        data_dir = os.path.join(root, "data")
        os.makedirs(data_dir, exist_ok=True)
        filepath = os.path.join(data_dir, filename)
        
        df = pd.DataFrame(tickers, columns=["Ticker"])
        df.to_csv(filepath, index=False)
        logger.info(f"Tickers saved to {filepath}")
    except Exception as e:
        logger.error(f"Failed to save tickers to {filename}: {e}")

if __name__ == "__main__":
    # Test the scraper
    spx_list = fetch_spx_tickers()
    if spx_list:
        save_tickers(spx_list)