import requests 
import json

from dataclasses import dataclass
from datetime import datetime

from Config import link
from Config import translations_path

@dataclass
class WeatherData:
    city: str
    temperature: int
    feels_like: int
    description: str
    time: str


class WeatherApi:
    def __init__(self,api_link=link):
        self.__api_link = api_link

    def get_weather(self,city):
        link = self.__api_link + city
        r = requests.get(link).json()
        return WeatherData(
        city,
        r['current']['temperature'],
        r['current']['feelslike'],
        r['current']['weather_descriptions'][0],
        datetime.now().strftime("%d.%m %H:%M"))



class WeatherFormatter:
    def __init__(self):
        with open(translations_path,encoding='UTF-8') as f:
            self.translations = json.load(f)

    def data_for_user(self,city):
        api = WeatherApi()
        weather = api.get_weather(city)
        try:
            desc_translation = self.translations[weather.description.capitalize()]
        except KeyError:
            desc_translation = weather.description

        return F"""Температура {weather.temperature}
Ощущается как {weather.feels_like}
{desc_translation}"""


    def data_for_data_base(self,city):
        api = WeatherApi()
        weather = api.get_weather(city)
        return (
        weather.city,
        weather.temperature,
        weather.feels_like,
        weather.description,
        weather.time)
