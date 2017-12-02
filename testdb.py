#!/usr/bin/python

import MySQLdb

db = MySQLdb.connect("10.0.0.160","test","test123","test" )

# prepare a cursor object using cursor() method
cursor = db.cursor()


# Prepare SQL query to INSERT a record into the database.
sql = """INSERT INTO test(S1temp, S1humidity, S2temp, S2humidity)
         VALUES (21, 35, 22, 40)"""
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
