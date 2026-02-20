from db_utils import DatabaseManager
from weather_logic import WeatherFormatter


def db_menu(db_manager, weather_formatter):
    while True:
        try:
            n = int(input("""1 - Вывести погоду
2 - Внести в базу данных погоду 
3 - Вывести базу данных
4 - Выйти из меню
"""))
        except ValueError:
            print("Неверный ввод!")
            continue

        if n == 1:
            print(weather_formatter.data_for_user(input("Введите город\n")))
        elif n == 2:
            db_manager.dump_to_data_base(weather_formatter.data_for_data_base(input('Введите город\n')))
        elif n == 3:
            print(db_manager.pretty_table_())
        elif n == 4:
            db_manager.close()
            break