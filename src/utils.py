import os
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def setup_logging(log_level=logging.INFO):
    """
    Configures a standard logger to track script progress and errors.
    """
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    return logging.getLogger("VolScreener")

def get_project_root():
    """
    Returns the root directory of the project.
    """
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_timestamp():
    """
    Returns the current timestamp in YYYYMMDD_HHMMSS format.
    """
    return datetime.now().strftime("%Y-%m-%d")

def ensure_directories():
    """
    Checks if /data and /results folders exist; creates them if they don't.
    """
    root = get_project_root()
    for folder in ["data", "results"]:
        path = os.path.join(root, folder)
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Created directory: {path}")

# Quick test when running the file directly
if __name__ == "__main__":
    ensure_directories()
    logger = setup_logging()
    logger.info(f"Project Root: {get_project_root()}")
    logger.info(f"Current Timestamp: {get_timestamp()}")