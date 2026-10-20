from weather_app.weather_display import WeatherDisplay


def test_header(capsys):

    WeatherDisplay.header(
        "WEATHER TEST"
    )

    captured = capsys.readouterr()

    assert "WEATHER TEST" in captured.out