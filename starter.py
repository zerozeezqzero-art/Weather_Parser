from menu import db_menu
from db_utils import DatabaseManager
from weather_logic import WeatherFormatter

from Config import data_base_path
from Config import translations_path


if __name__ == "__main__":
    DB = DatabaseManager(data_base_path)
    WF = WeatherFormatter()
    db_menu(DB,WF)

