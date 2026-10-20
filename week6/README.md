# 🌤️ Weather Dashboard

A Python-based command-line Weather Dashboard that retrieves real-time weather information and five-day forecasts for cities around the world using the OpenWeatherMap API.

## 📌 Project Overview

The Weather Dashboard provides current weather conditions, forecast information, city search suggestions, favorite city management, and temperature unit settings through an interactive command-line interface.

It uses Python, the Requests library, and the OpenWeatherMap API to retrieve and display weather data.

## ✨ Features

- **Current Weather:** View temperature, feels-like temperature, weather conditions, humidity, wind speed, pressure, and visibility.
- **Five-Day Forecast:** View daily forecast information, including temperatures, humidity, and weather conditions.
- **City Search:** Search for weather information by city name.
- **City Suggestions:** Find matching cities using the city search feature.
- **Favorite Cities:** Manage a list of favorite cities.
- **Temperature Conversion:** Configure temperature display in Celsius or Fahrenheit.
- **Weather Caching:** Cache weather data to reduce repeated API requests.
- **Error Handling:** Handle API errors, missing configuration, and unsuccessful requests.
- **Interactive CLI:** Navigate the dashboard through a simple numbered menu.
- **Cache Management:** Clear cached weather data when needed.
- **Help Menu:** View basic application usage instructions.

## 🛠️ Technologies Used

- Python
- OpenWeatherMap API
- Requests
- python-dotenv
- Pytest
- JSON
- Git and GitHub

## 📂 Project Structure

```text
week6/
├── weather_app/
│   ├── __init__.py
│   ├── config.py
│   ├── weather_api.py
│   ├── weather_parser.py
│   ├── weather_display.py
│   └── main.py
├── data/
│   ├── cache/
│   └── favorites.json
├── tests/
│   ├── test_api.py
│   ├── test_parser.py
│   └── test_display.py
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## ⚙️ Requirements

- Python 3.10 or later
- An OpenWeatherMap API key
- Internet connection
- pip package manager

## 🚀 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/rjayakumar692-ctrl/python-internship.git
```

Navigate to the Week 6 project directory:

```bash
cd python-internship/week6
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure the API key

Create an account at [OpenWeatherMap](https://openweathermap.org/api) and obtain an API key.

Copy the example environment file:

```powershell
Copy-Item .env.example .env
```

Open `.env` and configure your API key:

```env
OPENWEATHER_API_KEY=your_api_key_here
```

Replace the placeholder with your actual API key.

**Security:** Never commit your `.env` file or expose your API key publicly. The `.env` file is excluded through `.gitignore`.

### 5. Run the application

From the `week6` project directory, execute:

```bash
python -m weather_app.main
```

## 🖥️ Application Menu

```text
======================================================================
                         WEATHER DASHBOARD
======================================================================
1. Search weather
2. Search city suggestions
3. Favorite cities
4. Settings
5. Clear cache
6. Help
7. Exit
```

### How to Use

1. Run the application.
2. Select an option from the menu.
3. Enter a city name when prompted.
4. View current weather and forecast information.
5. Use the favorite cities and settings options as needed.
6. Select Exit to close the application.

## 🧪 Testing

The project uses Pytest for automated testing.

Run the tests from the `week6` directory:

```bash
python -m pytest -v
```

**Latest test result:** 6 tests passed.

The current test suite covers API behavior, dashboard display, temperature conversion, temperature formatting, and weather icon selection.

## 🔐 Environment Variables

| Variable | Description |
|---|---|
| `OPENWEATHER_API_KEY` | API key used to retrieve weather data |

Keep sensitive credentials in the local `.env` file.

## 🎯 Learning Outcomes

This project demonstrates practical experience with:

- Python modules and package organization
- REST API integration
- HTTP requests and JSON response handling
- Environment variable management
- Exception handling
- File and directory management
- JSON-based data storage
- Caching concepts
- Command-line application development
- Unit testing with Pytest
- Git and GitHub project organization

## 🔮 Future Enhancements

- Export weather reports to CSV.
- Add weather alerts and historical weather records.
- Add IP-based location detection.
- Compare weather conditions across multiple cities.
- Improve automated test coverage.

## 👨‍💻 Author

**Jayakumar Ravi**

- GitHub: [rjayakumar692-ctrl](https://github.com/rjayakumar692-ctrl)

## 📄 License

This project was developed for Python internship learning and practice. A formal open-source license can be added if the project is intended for public distribution.

---

*Built with Python to explore real-world API integration and command-line application development.*
