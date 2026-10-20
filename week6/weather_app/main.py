import json

from .config import FAVORITES_FILE, create_directories
from .weather_api import WeatherAPI, WeatherAPIError
from .weather_display import WeatherDisplay
from .weather_parser import WeatherParser


class WeatherApp:
    """Main weather dashboard application."""

    def __init__(self):
        create_directories()

        self.api = WeatherAPI()
        self.unit = "C"
        self.current_city = None

    # -------------------------------------------------
    # Favorites
    # -------------------------------------------------

    def load_favorites(self):
        """Load favorite cities from JSON."""

        try:
            with FAVORITES_FILE.open(
                "r",
                encoding="utf-8",
            ) as file:
                return json.load(file)

        except (
            OSError,
            json.JSONDecodeError,
        ):
            return []

    def save_favorites(self, favorites):
        """Save favorite cities."""

        with FAVORITES_FILE.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                favorites,
                file,
                indent=2,
            )

    def add_favorite(self, city):
        """Add a city to favorites."""

        favorites = self.load_favorites()

        if city.lower() not in [
            item.lower() for item in favorites
        ]:
            favorites.append(city)
            self.save_favorites(favorites)

            print(f"⭐ {city} added to favorites.")
        else:
            print("City is already in favorites.")

    # -------------------------------------------------
    # Weather
    # -------------------------------------------------

    def show_weather(self, city):
        """Fetch and display weather."""

        try:
            print(
                f"\nFetching weather for {city}..."
            )

            current_data = (
                self.api.get_current_weather(city)
            )

            forecast_data = (
                self.api.get_forecast(city)
            )

            current = (
                WeatherParser.parse_current(
                    current_data
                )
            )

            forecast = (
                WeatherParser.parse_forecast(
                    forecast_data
                )
            )

            self.current_city = current["city"]

            WeatherDisplay.display_current(
                current,
                self.unit,
            )

            WeatherDisplay.display_forecast(
                forecast,
                self.unit,
            )

            return forecast

        except WeatherAPIError as error:
            print(f"\n❌ {error}")

        except (KeyError, ValueError) as error:
            print(
                f"\n❌ Unable to process "
                f"weather data: {error}"
            )

        return None

    # -------------------------------------------------
    # City Search
    # -------------------------------------------------

    def city_search(self):
        """Search cities using autocomplete suggestions."""

        city = input(
            "\nEnter city name: "
        ).strip()

        if not city:
            print("Please enter a city name.")
            return

        try:
            suggestions = (
                self.api.search_cities(city)
            )

            WeatherDisplay.display_city_suggestions(
                suggestions
            )

            if suggestions:
                choice = input(
                    "\nEnter number to select "
                    "(or press Enter to cancel): "
                ).strip()

                if choice.isdigit():
                    index = int(choice) - 1

                    if 0 <= index < len(suggestions):
                        selected = suggestions[index]

                        city_name = selected["name"]

                        if selected.get("country"):
                            city_name += (
                                f", {selected['country']}"
                            )

                        self.show_weather(city_name)

        except WeatherAPIError as error:
            print(f"\n❌ {error}")

    # -------------------------------------------------
    # Settings
    # -------------------------------------------------

    def settings(self):
        """Application settings."""

        WeatherDisplay.header("⚙️ SETTINGS")

        print(
            f"Current temperature unit: "
            f"{self.unit}"
        )

        print("\n1. Celsius (°C)")
        print("2. Fahrenheit (°F)")

        choice = input(
            "\nSelect unit: "
        ).strip()

        if choice == "1":
            self.unit = "C"
            print("✅ Temperature unit set to Celsius.")

        elif choice == "2":
            self.unit = "F"
            print(
                "✅ Temperature unit set to Fahrenheit."
            )

        else:
            print("Invalid option.")

    # -------------------------------------------------
    # Main Menu
    # -------------------------------------------------

    def menu(self):
        """Display interactive menu."""

        while True:
            WeatherDisplay.header(
                "🌤️ WEATHER DASHBOARD"
            )

            print("1. Search weather")
            print("2. Search city suggestions")
            print("3. Favorite cities")
            print("4. Settings")
            print("5. Clear cache")
            print("6. Help")
            print("7. Exit")

            choice = input(
                "\nEnter your choice: "
            ).strip()

            if choice == "1":
                city = input(
                    "\nEnter city name: "
                ).strip()

                if city:
                    forecast = self.show_weather(city)

                    if forecast and self.current_city:
                        save = input(
                            "\nAdd this city to favorites? "
                            "(y/n): "
                        ).lower()

                        if save == "y":
                            self.add_favorite(
                                self.current_city
                            )

            elif choice == "2":
                self.city_search()

            elif choice == "3":
                favorites = self.load_favorites()

                WeatherDisplay.display_favorites(
                    favorites
                )

                if favorites:
                    choice = input(
                        "\nEnter number to view "
                        "(or Enter to go back): "
                    ).strip()

                    if choice.isdigit():
                        index = int(choice) - 1

                        if 0 <= index < len(favorites):
                            self.show_weather(
                                favorites[index]
                            )

            elif choice == "4":
                self.settings()

            elif choice == "5":
                self.api.clear_cache()
                print("✅ Weather cache cleared.")

            elif choice == "6":
                self.show_help()

            elif choice == "7":
                print(
                    "\nThank you for using "
                    "Weather Dashboard! 🌤️"
                )
                break

            else:
                print(
                    "\n❌ Invalid choice. "
                    "Please select 1-7."
                )

    @staticmethod
    def show_help():
        """Display application help."""

        WeatherDisplay.header("📖 HELP")

        print(
            """
Weather Dashboard Commands
--------------------------
1. Search weather
   Get current weather and 5-day forecast.

2. Search city suggestions
   Find cities using autocomplete suggestions.

3. Favorite cities
   Save and quickly access frequently used cities.

4. Settings
   Change Celsius/Fahrenheit temperature display.

5. Clear cache
   Remove locally cached API responses.

6. Help
   Display this information.

7. Exit
   Close the application.

API responses are cached for 10 minutes
to reduce unnecessary API requests.
"""
        )


def main():
    """Application entry point."""

    app = WeatherApp()
    app.menu()


if __name__ == "__main__":
    main()