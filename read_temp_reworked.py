#!/usr/bin/python

import Adafruit_DHT, datetime, MySQLdb

#Setup vars
sensor = Adafruit_DHT.DHT22
PIN17 = 17
PIN27 = 27

#Define values
S1h, S1t = Adafruit_DHT.read_retry(sensor, PIN17)
S2h, S2t = Adafruit_DHT.read_retry(sensor, PIN27)

S1temp = "{0:0.1f}".format(S1t)
S1humidity = "{0:0.1f}".format(S1h)
S2temp = "{0:0.1f}".format(S2t)
S2humidity = "{0:0.1f}".format(S2h)

#Values that match my DB
print(S1temp), "S1temp"
print(S1humidity), "S1humidity"
print(S2temp), "S2temp"
print(S2humidity), "S2humidity"

Time = (datetime.datetime.now())
print(Time), "Time"

#Data Base
db = MySQLdb.connect("10.0.0.160","test","test123","test" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Prepare SQL query to INSERT a record into the database.
# PROBLEM! I need do replace 1, 2, 3, ... with my Values (S1temp,...
sql = """INSERT INTO test(S1temp, S1humidity, S2temp, S2humidity, Time)
         VALUES (1, 2, 3, 4, 5)"""
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Commit your changes in the database
   db.commit()
except:
   # Rollback in case there is any error
   db.rollback()


# disconnect from server
db.close()


# THINKERING
# Something makes the code loop one time?
# Corresponding values needs to be placed for INSERTion
# I need more print"error"-statements, where and how does it fail
#
