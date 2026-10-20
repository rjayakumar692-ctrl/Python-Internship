from pathlib import Path
import os

from dotenv import load_dotenv


# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(BASE_DIR / ".env")


# API configuration
API_KEY = os.getenv("OPENWEATHER_API_KEY")

BASE_URL = "https://api.openweathermap.org/data/2.5"

# Application directories
DATA_DIR = BASE_DIR / "data"
CACHE_DIR = DATA_DIR / "cache"
FAVORITES_FILE = DATA_DIR / "favorites.json"

# Cache duration: 10 minutes
CACHE_DURATION = 600

# Request timeout
REQUEST_TIMEOUT = 10


def create_directories():
    """Create required application directories."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    if not FAVORITES_FILE.exists():
        FAVORITES_FILE.write_text("[]", encoding="utf-8")