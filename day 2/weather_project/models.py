from pydantic import BaseModel

class WeatherReport(BaseModel):
    city:str
    temperature:float
    humidity:int
    weather:str