from weather_app.weather_parser import WeatherParser


def test_celsius_to_fahrenheit():
    result = WeatherParser.celsius_to_fahrenheit(0)

    assert result == 32


def test_temperature_format_celsius():
    result = WeatherParser.format_temperature(
        25,
        "C",
    )

    assert result == "25.0°C"


def test_temperature_format_fahrenheit():
    result = WeatherParser.format_temperature(
        25,
        "F",
    )

    assert result == "77.0°F"


def test_weather_icon():
    assert WeatherParser.WEATHER_ICONS["Clear"] == "☀️"