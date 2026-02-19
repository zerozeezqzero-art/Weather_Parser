from Config import API
from Config import link
import requests
import json
import sqlite3
from datetime import datetime
from prettytable import PrettyTable

from menu import db_menu
from db_utils import DatabaseManager

from Config import data_base_path
from Config import translations_path


if __name__ == "__main__":
    DB = DatabaseManager(translations_path,data_base_path)
    db_menu(DB)
