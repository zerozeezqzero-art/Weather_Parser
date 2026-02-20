import sqlite3
from prettytable import PrettyTable
class DatabaseManager:
    def __init__(self,data_base_path):
        self.data_base = sqlite3.connect(data_base_path)
        
        self.cursor = self.data_base.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS weather (town TEXT,temp INT,feelslike INT,desc TEXT,time TEXT);')
    
    def dump_to_data_base(self,data):
        self.cursor.execute("""INSERT INTO weather 
        (town,
        temp,
        feelslike,
        desc,
        time) 
        VALUES (?,?,?,?,?);""",
        data)
        self.data_base.commit()

    
    def pretty_table_(self):
        self.cursor.execute("SELECT * FROM weather")
        data = self.cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["Город","Температура","Ощущается как","Погода","Время"]
        for row in data:
            table.add_row(row)
        return table


    def close(self):
        self.data_base.close()