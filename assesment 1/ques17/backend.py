from flask import Flask, jsonify
from pydantic import BaseModel, ValidationError
from dotenv import load_dotenv
import requests
import os 
#load dot_env
load_dotenv()
API_KEY = os.getenv("API_KEY")
app = Flask(__name__)

#pydantic model 
class Weather(BaseModel):
    city: str
    temperature: float
    humidity: int
    description: str
@app.route("/weather/<city>")
def get_weather(city):
    url = (f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric")
    try:
        response = requests.get(url,timeout=10)
        response.raise_for_status()
        data = response.json()

        weather_data = Weather(
            city=data["name"],
            temperature=data["main"]["temp"],
            humidity=data["main"]["humidity"],
            description=data["weather"][0]["description"]
        )
        return jsonify({
            "success":True,
            "data":weather_data.dict()
        })
    except requests.exceptions.RequestException as e:
        return jsonify({
            "success":False,
            "error":f"Network Error: {str(e)}"
        }),500
    except ValidationError as e:
        return jsonify({
            "success":False,
            "error":"Validation Error",
            "details":e.errors()
        }),500
    except Exception as e:
        return jsonify({
            "success":False,
            "error":f"Unexpected Error : {str(e)}"
        }),500

if __name__ =="__main__":
    app.run(debug=True)