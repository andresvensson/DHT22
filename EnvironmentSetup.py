import configparser
from typing import Dict

from Database import Database
from helpers import query_yes_no


class ConfigCreator:
    def __init__(self):
        self.config_dict: Dict[str, str] = {}
        self.config_file_name: str = ""
        self.cfg = None

    def create_section(self, key: str, values: list[str]):
        print(f'[{key}]')
        for v in values:
            self.config[key] = input(f'{v}: ')

    def create_config_file(self):
        conf = configparser.ConfigParser()
        for section in self.config_dict:
            conf.add_section(section)
            for key, value in self.config_dict[section]:
                conf.set(section, key, value)
        self.config_file_name = input('Set config file name: ')
        with open(self.config_file_name, 'w') as file:
            conf.write(file)
            print("Config file created: ", file.name)

    def print_config(self):
        print("-" * 20)
        print("Config")
        print("-" * 20)
        for section in self.config:
            print(f"[{section}]")
            for key, value in self.config[section]:
                print(key, ':', value)
        print("-" * 20)


def create_config():
    cfg = ConfigCreator()
    print("""Hello! Seems like it's your first time running this program,
            let's do some setup...
        """)
    cfg.create_section('database', ['host', 'user', 'password'])
    cfg.create_section('readwrite', ['database', 'table'])
    cfg.print_config()
    cfg.create_config_file()
    db = Database(cfg.config_file_name)
    if not db.connect():
        qst = f"[!] Create database \"{cfg['database']['database']}\"?"
        if query_yes_no(qst):
            db.create_new_database(cfg["database"]["database"])
            print("[*] Database Created.")
    if not db.table_exists():
        qst = f"""[!] The table {cfg['readwrite']['table']}
         doesn't exist. Create it?"""
        if query_yes_no(qst):
            db.create_table()
            print("[*] Table Created.")
            if query_yes_no("Create sample data?"):
                db.create_sample_data(input("How many rows?"))


if __name__ == "__main__":
    create_config()
    print("[*] Setup complete!")
