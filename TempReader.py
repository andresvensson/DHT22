#!/usr/bin/python
import Adafruit_DHT
from Database import Database
from typing import Dict
from time import sleep
from datetime import datetime
import configparser
#Setup global variables

PIN17 = 17
PIN27 = 27
SLEEPY_TIME_MINUTES = 5

class TempReader:
    def __init__(self, pin: int, location: str, sensor=Adafruit_DHT.DHT22):
        self.pin = pin
        self.sensor = Adafruit_DHT.DHT22
        self.location = location
        self.config = configparser.ConfigParser()
        self.config.read('DHT22.cfg')
        self.temperature: float = 0
        self.humidity: float = 0

    def get_reading(self):
        self.humidity, self.temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
        if self.humidity is not None and self.temperature is not None:
            print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(self.temperature, self.humidity))
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
            # sensor.read_temperature()
            sensor.get_reading()
            data = sensor.get_dict()
            db.insert_row(data)
        sleep(SLEEPY_TIME_MINUTES * 60)

if __name__ == "__main__":
    main_loop()

