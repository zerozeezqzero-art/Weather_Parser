from Config import API
from Config import link
import requests
import json
import sqlite3
from datetime import datetime
from prettytable import PrettyTable




class DatabaseManager:
    def __init__(self,translations_path='/home/zero/PYTHON/SQL_pogoda/translations.json',data_base_path='/home/zero/PYTHON/SQL_pogoda/weather.db'):
        self.translations_path = translations_path
        self.data_base = sqlite3.connect(data_base_path)
        
        self.cursor = self.data_base.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS weather (town TEXT,temp INT,feelslike INT,desc TEXT,time TEXT);')
        
        date = datetime.now()
        self.f_date =  date.strftime("%d.%m %H:%M")

    
    def weather_for_data_base(self,city):
        r = requests.get(f"{link}{city}").json()
        data = (city,r['current']['temperature'],r['current']['feelslike'],r['current']['weather_descriptions'][0],self.f_date) # город, погода, ощущается как, описание погоды 
        
        return data


    def weather_for_user(self,city):
        with open(self.translations_path,"r",encoding='UTF-8') as f:
            d = json.load(f)
        r = requests.get(f"{link}{city}").json()
        try:
            data = f"""Температура {r['current']['temperature']}
Ощущается как {r['current']['feelslike']}
{d[r['current']['weather_descriptions'][0]]}
"""
        except KeyError:
                data = f"""Температура = {r['current']['temperature']}
        Ощущается как {r['current']['feelslike']}
        {r['current']['weather_descriptions'][0]}
        """
        return data


    def check_api(self,city="Moscow"):
        """Функция для отладки API запросов"""

        print(f"1. Тестируем API с городом: {city}")
        print(f"2. Используемый link: {link}")

        try:
            # Отправляем запрос
            resp = requests.get(f"{link}{city}")
            print(f"3. Статус ответа: {resp.status_code}")
            
            # Пробуем получить JSON
            r = resp.json()
            print("4. Полный ответ API:")
            print(json.dumps(r, indent=2, ensure_ascii=False))
            
            # Проверяем наличие ключей
            print("\n5. Проверка ключей:")
            print(f"   - 'current' в ответе: {'current' in r}")
            print(f"   - 'error' в ответе: {'error' in r}")
            print(f"   - 'success' в ответе: {'success' in r}")
            
            if 'current' in r:
                print(f"6. Температура: {r['current']['temperature']}")
                print(f"   Описание: {r['current']['weather_descriptions'][0]}")
            elif 'error' in r:
                print(f"6. ОШИБКА API: {r['error']['info']}")
                
        except Exception as e:
            print(f"!!! Ошибка при выполнении запроса: {e}")


    def pretty_table_(self):
        self.cursor.execute("SELECT * FROM weather")
        data = self.cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["Город","Температура","Ощущается как","Погода","Время"]
        for row in data:
            table.add_row(row)
        return table


    def dump_to_data_base(self,data):
        self.cursor.execute('INSERT INTO weather (town,temp,feelslike,desc,time) VALUES (?,?,?,?,?);',data)
        self.data_base.commit()
