import configparser
from typing import Dict
import mysql.connector


class Database:
    INSERT_QUERY = """INSERT INTO
                    readings(readingtimestamp, sensor,
                    temperature, humidity, location)
                    VALUES (
                        %(timestamp)s, %(sensor)s, %(temp)s,
                        %(humidity)s, %(location)s
                    )"""
    SELECT_QUERY = "SELECT * FROM readings WHERE {}"

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('database.cfg')
        self.table_name: str = self.config['readwrite']['table']
        self.self_db: str = self.config['readwrite']['database']
        try:
            self.cnx = mysql.connector.connect(
                    host=self.config["database"]["host"],
                    user=self.config["database"]["user"],
                    password=self.config["database"]["password"]
                    )
            self.cursor = self.cnx.cursor()
        except mysql.connector.error as err:
            self.handle_error_code(err)
            raise(err)

    def create_new_database(self):
        print(f"Creating database: {self.db_name}")
        try:
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_name}")
            self.cnx.commit()
        except mysql.connector.Error as err:
            print("[!] Could not create database")
            self.handle_error_code(err)
        finally:
            self.cursor.execute(f"USE {self.db_name}")

    def table_exists(self) -> bool:
        self.cursor.execute('SHOW TABLES')
        for table in self.cursor:
            return self.config["readwrite"]["table"] in table
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
    def handle_error_code(error: mysql.connector.Error):
        error_codes: Dict[int, str] = {
            2003: "Please check that you supplied the correct host.",
            1045: "Wrong username or password.",
            1049: "The database does not exist."
        }

        if error_codes.get(error.errno):
            print(error_codes[error.errno])


if __name__ == "__main__":
    db = Database()
