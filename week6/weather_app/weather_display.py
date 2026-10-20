import csv
from pathlib import Path
from typing import Dict, List

from .weather_parser import WeatherParser


class WeatherDisplay:
    """Handles terminal output."""

    WIDTH = 70

    @staticmethod
    def clear_screen() -> None:
        """Print spacing to visually clear the terminal."""

        print("\n" * 3)

    @staticmethod
    def header(title: str) -> None:
        """Display a formatted section header."""

        print("\n" + "=" * WeatherDisplay.WIDTH)
        print(title.center(WeatherDisplay.WIDTH))
        print("=" * WeatherDisplay.WIDTH)

    @staticmethod
    def display_current(
        weather: Dict,
        unit: str = "C",
    ) -> None:
        """Display current weather."""

        parser = WeatherParser

        WeatherDisplay.header(
            f"{weather['icon']} WEATHER DASHBOARD"
        )

        print(
            f"📍 Location : "
            f"{weather['city']}, {weather['country']}"
        )

        print(
            f"🕐 Updated  : "
            f"{weather['updated']}"
        )

        print("\nCurrent Weather")
        print("-" * 40)

        print(
            f"Temperature : "
            f"{parser.format_temperature(weather['temperature'], unit)}"
        )

        print(
            f"Feels Like  : "
            f"{parser.format_temperature(weather['feels_like'], unit)}"
        )

        print(
            f"Conditions  : "
            f"{weather['condition']} {weather['icon']}"
        )

        print(
            f"Humidity    : "
            f"{weather['humidity']}%"
        )

        print(
            f"Wind Speed  : "
            f"{weather['wind_speed']} m/s"
        )

        print(
            f"Pressure    : "
            f"{weather['pressure']} hPa"
        )

        print(
            f"Visibility  : "
            f"{weather['visibility']:.1f} km"
        )

        print(
            f"Sunrise     : "
            f"{weather['sunrise']}"
        )

        print(
            f"Sunset      : "
            f"{weather['sunset']}"
        )

    @staticmethod
    def display_forecast(
        forecast: List[Dict],
        unit: str = "C",
    ) -> None:
        """Display 5-day forecast."""

        parser = WeatherParser

        WeatherDisplay.header(
            "📅 5-DAY FORECAST"
        )

        for day in forecast:
            min_temp = parser.format_temperature(
                day["min_temp"],
                unit,
            )

            max_temp = parser.format_temperature(
                day["max_temp"],
                unit,
            )

            print(
                f"{day['date']:<12} "
                f"{day['icon']}  "
                f"{min_temp:>7} / {max_temp:<7} "
                f"Humidity: {day['humidity']}%"
            )

            print(
                f"{'':<12} "
                f"{day['condition']}"
            )

    @staticmethod
    def display_city_suggestions(
        suggestions: List[Dict],
    ) -> None:
        """Display autocomplete/search suggestions."""

        if not suggestions:
            print("No city suggestions found.")
            return

        WeatherDisplay.header("CITY SUGGESTIONS")

        for index, city in enumerate(
            suggestions,
            start=1,
        ):
            name = city.get("name", "Unknown")
            state = city.get("state", "")
            country = city.get("country", "")

            location = ", ".join(
                part
                for part in [name, state, country]
                if part
            )

            print(f"{index}. {location}")

    @staticmethod
    def display_favorites(
        favorites: List[str],
    ) -> None:
        """Display favorite cities."""

        WeatherDisplay.header("⭐ FAVORITE CITIES")

        if not favorites:
            print("No favorite cities yet.")
            return

        for index, city in enumerate(
            favorites,
            start=1,
        ):
            print(f"{index}. {city}")

    @staticmethod
    def export_csv(
        city: str,
        forecast: List[Dict],
        filename: str = "weather_forecast.csv",
    ) -> None:
        """Export forecast data to CSV."""

        path = Path(filename)

        with path.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "date",
                    "condition",
                    "min_temperature",
                    "max_temperature",
                    "humidity",
                ],
            )

            writer.writeheader()

            for day in forecast:
                writer.writerow(
                    {
                        "date": day["date"],
                        "condition": day["condition"],
                        "min_temperature": day["min_temp"],
                        "max_temperature": day["max_temp"],
                        "humidity": day["humidity"],
                    }
                )

        print(
            f"\n✅ Forecast exported successfully: "
            f"{path}"
        )