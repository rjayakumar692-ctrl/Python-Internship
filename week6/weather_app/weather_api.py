import hashlib
import json
import time
from pathlib import Path
from typing import Any, Optional

import requests

from .config import (
    API_KEY,
    BASE_URL,
    CACHE_DIR,
    CACHE_DURATION,
    REQUEST_TIMEOUT,
)


class WeatherAPIError(Exception):
    """Custom exception for weather API errors."""


class WeatherAPI:
    """Handles communication with OpenWeatherMap API."""

    def __init__(
        self,
        api_key: Optional[str] = API_KEY,
        base_url: str = BASE_URL,
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.cache_duration = CACHE_DURATION

    def _cache_key(self, endpoint: str, params: dict) -> str:
        """Generate a safe unique cache filename."""

        raw_key = f"{endpoint}_{sorted(params.items())}"

        return hashlib.md5(
            raw_key.encode("utf-8")
        ).hexdigest()

    def _get_cache(self, cache_key: str) -> Optional[dict]:
        """Return cached data if it is still valid."""

        cache_file = CACHE_DIR / f"{cache_key}.json"

        if not cache_file.exists():
            return None

        try:
            age = time.time() - cache_file.stat().st_mtime

            if age > self.cache_duration:
                return None

            with cache_file.open("r", encoding="utf-8") as file:
                return json.load(file)

        except (OSError, json.JSONDecodeError):
            return None

    def _save_cache(self, cache_key: str, data: dict) -> None:
        """Save API response to cache."""

        cache_file = CACHE_DIR / f"{cache_key}.json"

        try:
            with cache_file.open("w", encoding="utf-8") as file:
                json.dump(data, file, indent=2)

        except OSError:
            pass

    def _request(
        self,
        endpoint: str,
        params: dict,
    ) -> dict:
        """Make an API request with error handling."""

        if not self.api_key:
            raise WeatherAPIError(
                "API key not configured. "
                "Please add OPENWEATHER_API_KEY to .env"
            )

        params = {
            **params,
            "appid": self.api_key,
            "units": "metric",
        }

        cache_key = self._cache_key(endpoint, params)

        cached_data = self._get_cache(cache_key)

        if cached_data:
            return cached_data

        url = f"{self.base_url}/{endpoint}"

        try:
            response = requests.get(
                url,
                params=params,
                timeout=REQUEST_TIMEOUT,
            )

        except requests.exceptions.Timeout:
            raise WeatherAPIError(
                "Request timed out. Please try again."
            )

        except requests.exceptions.ConnectionError:
            raise WeatherAPIError(
                "Network connection error. "
                "Check your internet connection."
            )

        except requests.RequestException as error:
            raise WeatherAPIError(
                f"Request failed: {error}"
            )

        if response.status_code == 200:
            data = response.json()
            self._save_cache(cache_key, data)
            return data

        if response.status_code == 401:
            raise WeatherAPIError(
                "Invalid API key."
            )

        if response.status_code == 404:
            raise WeatherAPIError(
                "City not found."
            )

        if response.status_code == 429:
            raise WeatherAPIError(
                "API rate limit exceeded."
            )

        raise WeatherAPIError(
            f"API request failed "
            f"(HTTP {response.status_code})."
        )

    def get_current_weather(self, city: str) -> dict:
        """Fetch current weather for a city."""

        return self._request(
            "weather",
            {"q": city},
        )

    def get_forecast(self, city: str) -> dict:
        """Fetch 5-day / 3-hour forecast."""

        return self._request(
            "forecast",
            {"q": city},
        )

    def search_cities(self, city: str) -> list:
        """
        Search city suggestions.

        OpenWeatherMap free weather endpoints do not provide
        full autocomplete functionality, so this method uses
        the Geocoding API.
        """

        if not self.api_key:
            raise WeatherAPIError("API key not configured.")

        params = {
            "q": city,
            "limit": 5,
            "appid": self.api_key,
        }

        try:
            response = requests.get(
                "https://api.openweathermap.org/geo/1.0/direct",
                params=params,
                timeout=REQUEST_TIMEOUT,
            )

            if response.status_code == 200:
                return response.json()

            if response.status_code == 401:
                raise WeatherAPIError("Invalid API key.")

            raise WeatherAPIError(
                f"City search failed "
                f"(HTTP {response.status_code})."
            )

        except requests.exceptions.Timeout:
            raise WeatherAPIError("City search timed out.")

        except requests.exceptions.ConnectionError:
            raise WeatherAPIError("Network connection error.")

    def clear_cache(self) -> None:
        """Delete all cached API responses."""

        if not CACHE_DIR.exists():
            return

        for file in CACHE_DIR.glob("*.json"):
            try:
                file.unlink()
            except OSError:
                pass