import configparser
import mysql.connector
from helpers import bcolors


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
        try:
            self.cnx = mysql.connector.connect(
                host=self.config["database"]["host"],
                user=self.config["database"]["user"],
                password=self.config["database"]["password"]
                )
        except mysql.connector.Error as err:
            self.handle_error_code(err)
            raise err

        self.cursor = self.cnx.cursor()

    def create_new_database(self, database_name):
        try:
            self.cursor.execute("CREATE DATABASE {}".format(database_name))
        except mysql.connector.Error as err:
            print(bcolors.FAIL, "[!] Could not create database", bcolors.ENDC)
            raise err
        self.cnx.commit()

    def table_exists(self) -> bool:
        self.cursor.execute('SHOW TABLES')
        for table in self.cursor:
            return self.config["readwrite"]["table"] in table
        return False

    def create_table(self):
        query = f"""CREATE TABLE {self.config['readwrite']['table']}
                (readingtimestamp datetime, sensor varchar(20),
                temperature decimal, humidity decimal,
                location varchar(20));"""
        self.cursor.execute(query)
        self.cnx.commit()

    def describe_table(self, table_name):
        self.cursor.execute(f"DESCRIBE {self.config['readwrite']["table"]}")
        print(bcolors.UNDERLINE, "[ Table Columns ]", bcolors.ENDC)
        for row in self.cursor:
            print(row[0], ":", row[1])

    def insert_row(self, data):
        self.cursor.execute(self.INSERT_QUERY, data)
        self.cnx.commit()

    @staticmethod
    def handle_error_code(error: mysql.connector.Error):
        error_codes = {
            2003: "Please check that you supplied the correct host.",
            1045: "Wrong username or password.",
            1049: "The database does not exist."
        }
        if error_codes[error.errno]:
            print(bcolors.WARNING, error_codes[error.errno], bcolors.ENDC)


if __name__ == "__main__":
    db = Database()
