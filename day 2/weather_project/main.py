import requests
import os

from dotenv import load_dotenv
from models import WeatherReport

# Load environment variables
load_dotenv()

# Get API key
API_KEY = os.getenv("API_KEY")
# City name
city = "Jaipur"

# API URL
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

# Send request
response = requests.get(url)

# Check success
if response.status_code == 200:

    data = response.json()

    # Validate using Pydantic
    weather_data = WeatherReport(

        city=data["name"],
        temperature=data["main"]["temp"],
        humidity=data["main"]["humidity"],
        weather=data["weather"][0]["description"]
    )

    # Create clean report
    report = f"""
    Weather Report
    -------------------
    City: {weather_data.city}
    Temperature: {weather_data.temperature}°C
    Humidity: {weather_data.humidity}%
    Weather: {weather_data.weather}
    """

    print(report)

    # Save report
    with open("report.txt", "w") as file:
        file.write(report)

    print("Report saved successfully!")

else:
    print("API Request Failed")
    print("Status Code:",response.status_code)
    print(response.text)