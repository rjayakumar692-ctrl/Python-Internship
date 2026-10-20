from datetime import datetime
from typing import Dict, List


class WeatherParser:
    """Processes OpenWeatherMap API responses."""

    WEATHER_ICONS = {
        "Clear": "☀️",
        "Clouds": "☁️",
        "Rain": "🌧️",
        "Drizzle": "🌦️",
        "Thunderstorm": "⛈️",
        "Snow": "❄️",
        "Mist": "🌫️",
        "Fog": "🌫️",
        "Haze": "🌫️",
    }

    @staticmethod
    def _icon(condition: str) -> str:
        """Return an emoji for a weather condition."""

        return WeatherParser.WEATHER_ICONS.get(
            condition,
            "🌤️",
        )

    @staticmethod
    def _format_time(timestamp: int) -> str:
        """Convert Unix timestamp into readable time."""

        return datetime.fromtimestamp(timestamp).strftime(
            "%H:%M"
        )

    @staticmethod
    def _format_date(timestamp: int) -> str:
        """Convert Unix timestamp into readable date."""

        return datetime.fromtimestamp(timestamp).strftime(
            "%a %d %b"
        )

    @staticmethod
    def parse_current(data: Dict) -> Dict:
        """Parse current weather response."""

        weather = data["weather"][0]
        main = data["main"]
        wind = data.get("wind", {})

        return {
            "city": data.get("name", "Unknown"),
            "country": data.get("sys", {}).get("country", ""),
            "temperature": main.get("temp"),
            "feels_like": main.get("feels_like"),
            "humidity": main.get("humidity"),
            "pressure": main.get("pressure"),
            "visibility": data.get("visibility", 0) / 1000,
            "wind_speed": wind.get("speed", 0),
            "wind_direction": wind.get("deg"),
            "condition": weather.get("description", "").title(),
            "icon": WeatherParser._icon(
                weather.get("main", "")
            ),
            "sunrise": WeatherParser._format_time(
                data["sys"]["sunrise"]
            ),
            "sunset": WeatherParser._format_time(
                data["sys"]["sunset"]
            ),
            "updated": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
        }

    @staticmethod
    def parse_forecast(data: Dict) -> List[Dict]:
        """
        Convert 3-hour forecast into daily summaries.
        """

        daily = {}

        for item in data.get("list", []):
            date = datetime.fromtimestamp(
                item["dt"]
            ).strftime("%Y-%m-%d")

            main = item["main"]
            weather = item["weather"][0]

            if date not in daily:
                daily[date] = {
                    "date": date,
                    "temps": [],
                    "humidity": [],
                    "conditions": [],
                    "icons": [],
                }

            daily[date]["temps"].append(
                main["temp"]
            )

            daily[date]["humidity"].append(
                main["humidity"]
            )

            daily[date]["conditions"].append(
                weather["description"].title()
            )

            daily[date]["icons"].append(
                WeatherParser._icon(
                    weather["main"]
                )
            )

        result = []

        for day in list(daily.values())[:5]:
            result.append(
                {
                    "date": datetime.strptime(
                        day["date"],
                        "%Y-%m-%d",
                    ).strftime("%a %d %b"),
                    "min_temp": round(min(day["temps"]), 1),
                    "max_temp": round(max(day["temps"]), 1),
                    "humidity": round(
                        sum(day["humidity"])
                        / len(day["humidity"])
                    ),
                    "condition": max(
                        set(day["conditions"]),
                        key=day["conditions"].count,
                    ),
                    "icon": max(
                        set(day["icons"]),
                        key=day["icons"].count,
                    ),
                }
            )

        return result

    @staticmethod
    def celsius_to_fahrenheit(celsius: float) -> float:
        """Convert Celsius to Fahrenheit."""

        return (celsius * 9 / 5) + 32

    @staticmethod
    def format_temperature(
        temperature: float,
        unit: str = "C",
    ) -> str:
        """Format temperature using selected unit."""

        if unit.upper() == "F":
            temperature = WeatherParser.celsius_to_fahrenheit(
                temperature
            )
            return f"{temperature:.1f}°F"

        return f"{temperature:.1f}°C"