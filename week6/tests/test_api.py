from unittest.mock import Mock, patch

from weather_app.weather_api import WeatherAPI


@patch("weather_app.weather_api.requests.get")
def test_get_current_weather(mock_get):

    mock_response = Mock()

    mock_response.status_code = 200

    mock_response.json.return_value = {
        "name": "Chennai",
        "main": {
            "temp": 30
        }
    }

    mock_get.return_value = mock_response

    api = WeatherAPI(
        api_key="test-key"
    )

    result = api.get_current_weather(
        "Chennai"
    )

    assert result["name"] == "Chennai"