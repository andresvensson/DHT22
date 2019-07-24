#!/usr/bin/python
import configparser
from datetime import datetime
from time import sleep
from typing import Dict

import Adafruit_DHT
from Database import Database

PIN17 = 17
PIN27 = 27
SLEEPY_TIME_MINUTES = 5


class TempReader:
    def __init__(self, pin: int, location: str, sensor=Adafruit_DHT.DHT22):
        self.pin = pin
        self.sensor = Adafruit_DHT.DHT22
        self.location = location
        self.config = configparser.ConfigParser()
        self.read_config()
        self.temperature: float = 0
        self.humidity: float = 0

    def read_config(self):
        self.config.read('DHT22.cfg')

    def get_reading(self):
        self.humidity, self.temperature = Adafruit_DHT.read_retry(self.sensor,
                                                                  self.pin)
        if self.humidity is not None and self.temperature is not None:
            print(f'''Temp={self.temperature:0.1f}*C
            Humidity={self.humidity:0.1f}%''')
        else:
            print('Failed to get reading. Try again!')
            self.humidity, self.temperature = 0, 0

    def get_dict(self) -> dict:
        return {
            "timestamp": datetime.now(),
            "sensor": self.sensor,
            "temp": self.temperature,
            "humidity": self.humidity,
            "location": self.location
        }


def main_loop():
    db = Database()
    sensors: Dict[TempReader] = {
        TempReader(PIN17, str(PIN17)),
        TempReader(PIN27, str(PIN27))
    }
    while True:
        for sensor in sensors:
            sensor.read_config()
            sensor.get_reading()
            data = sensor.get_dict()
            db.insert_row(data)
        sleep(SLEEPY_TIME_MINUTES * 60)


if __name__ == "__main__":
    main_loop()
