from Database import Database
from TempReader import TempReader
from helpers import bcolors, query_yes_no
import configparser
from datetime import datetime, timedelta
import random


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


def get_database_connection_details(cfg):
    cfg["database"]["host"] = input("Database host: ")
    cfg["database"]["user"] = input("Database user: ")
    cfg["database"]["password"] = input("Password: ")


def get_database_and_table(cfg):
    cfg["database"]["database"] = input("Database name: ")
    cfg["readwrite"]["table"] = input("Database table name: ")


def create_config_file(cfg):
    conf = configparser.ConfigParser()
    print("-"*20)
    print("Your config: ")
    print("-" * 20)
    for key in cfg:
        conf.add_section(key)
        for key2 in cfg[key]:
            print(key2, ':', cfg[key][key2])
            conf.set(key, key2, cfg[key][key2])
    print("-" * 20)
    with open('DHT22.cfg', 'w') as file:
        conf.write(file)
        print("Config file created: ", file.name)
    print("-" * 20)


def do_setup():
    cfg = {"database": {}, "readwrite": {}}
    db = Database()
    print("""Hello! Seems like it's your first time running this program,
            let's do some setup...
        """)
    get_database_connection_details(cfg)
    #db.test_connection(cfg["database"], "connection")
    get_database_and_table(cfg)
    create_config_file(cfg)
    """
    if not db.test_connection(cfg["database"], "connection"):
        if query_yes_no("[!] The database \"{}\" doesn't exist. Create it?".format(cfg["database"]["database"])):
            db.create_new_database(cfg["database"]["database"])
            print(bcolors.OKGREEN, "[*] Database Created.", bcolors.ENDC)
    if not db.table_exists():
        if query_yes_no("[!] The table {} doesn't exist. Create it?".format(cfg["readwrite"]["table"])):
            db.create_table()
            print(bcolors.OKGREEN, "[*] Table Created.", bcolors.ENDC)
            if query_yes_no("Create sample data?"):
                create_sample_data(input("How many rows?"))
    """

if __name__ == "__main__":
    do_setup()
    print("[*] Setup complete!")
