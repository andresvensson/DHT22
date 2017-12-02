#!/usr/bin/python
import Adafruit_DHT
#Setup global variables
sensor = Adafruit_DHT.DHT22
PIN17 = 17
PIN27 = 27

humidity, temperature = Adafruit_DHT.read_retry(sensor, PIN17)
if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
else:
    print('Failed to get reading. Try again!')

# Testing a repeat with other pin
humidity, temperature = Adafruit_DHT.read_retry(sensor, PIN27)
if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
else:
    print('Failed to get reading. Try again!')


#TODO: Get some kind of a loop going.    
#TODO: Refactor current sensor calls to a function.
#TODO: Handle Prints, Remember they are still useful for debugging.
#TODO: Push data to DB.
  
