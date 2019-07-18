import configparser
import mysql.connector
from helpers import bcolors


class Database:
    INSERT_QUERY = "INSERT INTO " \
                   "readings(readingtimestamp, sensor, temperature, humidity, location) " \
                   "VALUES (%(timestamp)s, %(sensor)s, %(temp)s, %(humidity)s, %(location)s)"
    SELECT_QUERY = "SELECT * FROM readings WHERE {}"

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('database.cfg')
        try:
            self.cnx = mysql.connector.connect(host=self.config["database"]["host"], 
                                    user=self.config["database"]["user"],
                                    password=self.config["database"]["password"])
        except mysql.connector.Error as err:
            self.handle_error_code(err)
            raise err

        self.cursor = self.cnx.cursor()

    @staticmethod
    def handle_error_code(error: mysql.connector.Error):
            if error.errno == 2003:
                print("Please check that you supplied the correct host.")
            elif error.errno == 1045:
                print(bcolors.WARNING, "Wrong username or password.", bcolors.ENDC)
            elif error.errno == 1049:
                print(bcolors.WARNING, "The database does not exist.", bcolors.ENDC)

    def create_new_database(self, database_name):
        try:
            self.cursor.execute("CREATE DATABASE {}".format(database_name))
        except mysql.connector.Error as err:
            print(bcolors.FAIL, "[!] Could not create database", bcolors.ENDC)
            print(bcolors.FAIL, "[!] Error message: ", err, bcolors.ENDC)

        self.cnx.commit()

    def table_exists(self) -> bool:
        self.cursor.execute('SHOW TABLES')
        for table in self.cursor:
            return self.config["readwrite"]["table"] in table
        return False

    def create_table(self):
        self.cursor.execute("CREATE TABLE {} (readingtimestamp datetime, sensor varchar(20), "
                    "temperature decimal, humidity decimal, location varchar(20));".format(self.config["readwrite"]["table"]))
        self.cnx.commit()

    def describe_table(self, table_name):
        self.cursor.execute("DESCRIBE {}".format(self.config["readwrite"]["table"]))
        print(bcolors.UNDERLINE, "[ Table Columns ]", bcolors.ENDC)
        for row in self.cursor:
            print(row[0], ":", row[1])

    def insert_row(self, data):
        self.cursor.execute(Database.INSERT_QUERY, data)
        self.cnx.commit()

def get_reading_dict():
    read_dict = {"timestamp": "", "sensor": "", "temp": "", "humidity": "", "location": ""}
    return read_dict

if __name__ == "__main__":
    db = Database()
