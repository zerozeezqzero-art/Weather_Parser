from Config import API
from Config import link
import requests
import json
import sqlite3
from datetime import datetime
from datetime import datetime
from prettytable import PrettyTable

from db_utils import DatabaseManager


def db_menu(obj):
    while True:
        try:
            n = int(input("""1 - Вывести погоду
2 - Внести в базу данных погоду 
3 - Вывести базу данных
4 - Выйти из меню
5 - Отладка
"""))
        except ValueError:
            print("Неверный ввод!")
            continue

        if n == 1:
            print(obj.weather_for_user(input("Введите город\n")))
        elif n == 2:
            data = obj.weather_for_data_base(input("Введите город\n"))
            obj.dump_to_data_base(data)
        elif n == 3:
            print(obj.pretty_table_())
        elif n == 4:
            obj.data_base.close()
            break
        elif n == 5:
            obj.check_api()