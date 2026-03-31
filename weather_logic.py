class api_ex(Exception):
    pass


import requests
import json
import pandas as pd

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
    def __init__(self, api_link=link):
        self.__api_link = api_link

    def get_weather(self, city):
        link = self.__api_link + city
        r = requests.get(link)
        if r.status_code == 200:
            r = r.json()
            if "current" in r:
                return WeatherData(
                    city,
                    r["current"]["temperature"],
                    r["current"]["feelslike"],
                    r["current"]["weather_descriptions"][0],
                    datetime.now().strftime("%d.%m %H:%M"),
                )
        else:
            raise api_ex


class WeatherFormatter:
    def __init__(self):
        with open(translations_path, encoding="UTF-8") as f:
            self.translations = json.load(f)

    def data_for_user(self, city):

        api = WeatherApi()
        try:
            weather = api.get_weather(city)
            try:
                desc_translation = self.translations[weather.description.capitalize()]
            except KeyError:
                desc_translation = weather.description

            pd.set_option("display.max_columns", None)
            pd.set_option("display.width", None)
            pd.set_option("display.max_colwidth", None)
            pd.set_option("display.colheader_justify", "center")

            data = {
                "температура": [weather.temperature],
                "ощущается как": [weather.feels_like],
                "погода": [weather.description],
            }
            ind = [city]
            pandas_data = pd.DataFrame(data, index=ind)
            return pandas_data

        except api_ex:
            return "ОШИБКА API!"

    def data_for_data_base(self, city):
        api = WeatherApi()
        weather = api.get_weather(city)
        return (
            weather.city,
            weather.temperature,
            weather.feels_like,
            weather.description,
            weather.time,
        )
