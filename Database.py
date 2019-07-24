import configparser
import random
from datetime import datetime, timedelta
from typing import Dict

from mysql import connector

from TempReader import TempReader


class Database:
    INSERT_QUERY = """INSERT INTO
                    readings(readingtimestamp, sensor,
                    temperature, humidity, location)
                    VALUES (
                        %(timestamp)s, %(sensor)s, %(temp)s,
                        %(humidity)s, %(location)s
                    )"""
    SELECT_QUERY = "SELECT * FROM readings WHERE {}"

    def __init__(self, config_path: str = 'database.cfg'):
        self.config = configparser.ConfigParser()
        self.config.read(config_path)
        self.table_name: str = self.config['readwrite']['table']
        self.db_name: str = self.config['readwrite']['database']
        self.cnx = None
        self.cursor = None
        self.last_error = None
        self.connect()

    def connect(self) -> bool:
        try:
            self.cnx = connector.connect(
                host=self.config['database']['host'],
                user=self.config['database']['user'],
                password=self.config['database']['password']
            )
            self.cursor = self.cnx.cursor()
            return True
        except connector.error as err:
            self.handle_error_code(err)
            self.last_error = err
            return False

    def database_exists(self) -> bool:
        query = f"""SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA
        WHERE SCHEMA_NAME = '{self.db_name}'"""
        self.cursor.execute(query)
        for db in self.cursor:
            return self.db_name in db
        return False

    def create_new_database(self):
        print(f"Creating database: {self.db_name}")
        query = f"CREATE DATABASE IF NOT EXISTS {self.db_name}"
        try:
            self.cursor.execute(query)
            self.cnx.commit()
        except connector.Error as err:
            print("[!] Could not create database")
            self.handle_error_code(err)
        finally:
            self.cursor.execute(f"USE {self.db_name}")

    def table_exists(self) -> bool:
        self.cursor.execute('SHOW TABLES')
        for table in self.cursor:
            return self.table_name in table
        return False

    def set_use_db(self):
        self.cursor.execute(f"USE {self.db_name}")

    def create_table(self) -> None:
        if self.table_exists():
            return
        self.set_use_db()
        query = f"""CREATE TABLE {self.table_name}
                (readingtimestamp datetime, sensor varchar(20),
                temperature decimal, humidity decimal,
                location varchar(20));"""
        self.cursor.execute(query)
        self.cnx.commit()

    def describe_table(self):
        self.cursor.execute(f"DESCRIBE {self.table_name}")
        print("[ Table Columns ]")
        for row in self.cursor:
            print(row[0], ":", row[1])

    def insert_row(self, data):
        self.cursor.execute(self.INSERT_QUERY, data)
        self.cnx.commit()

    @staticmethod
    def handle_error_code(error: connector.Error):
        error_codes: Dict[int, str] = {
            2003: "Please check that you supplied the correct host.",
            1045: "Wrong username or password.",
            1049: "The database does not exist."
        }

        if error_codes.get(error.errno):
            print(error_codes[error.errno])

    def create_sample_data(no_of_rows):
        # readings(readingtimestamp, sensor, temperature, humidity, location)
        db = Database()
        for i in range(0, no_of_rows):
            sensor = random.randint(1, 2)
            location = "Sample" + str(sensor)
            reader = TempReader(0, location)
            reader.temperature = random.randint(10, 30)
            reader.humidity = random.randint(30, 100)
            fake_reading = reader.get_dict()
            fake_reading["timestamp"] = datetime.now() - timedelta(days=i)
            db.insert_row(fake_reading)


if __name__ == "__main__":
    db = Database()
